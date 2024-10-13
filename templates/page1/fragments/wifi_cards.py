# templates/page1/fragments/wifi_cards.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QScrollArea, QLabel, QButtonGroup
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from templates.page1.functions.wifi_card_detect import detect_wifi_adapters
from .wifi_card import WifiCard
import os


class WifiCards(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_adapter = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        self.setLayout(layout)

        # Titre et bouton Refresh
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(10)

        frame_label = QLabel("Cartes Wi-Fi Détectées")
        frame_label.setFont(QFont("Arial", 14, QFont.Bold))
        frame_label.setStyleSheet("color: #333;")
        frame_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_layout.addWidget(frame_label)

        refresh_button = QPushButton()
        refresh_button.setIcon(self.create_white_icon(self.resource_path("refresh.svg"), QSize(24, 24)))
        refresh_button.setIconSize(QSize(24, 24))
        refresh_button.setFixedSize(40, 40)
        refresh_button.setToolTip("Actualiser la liste des cartes Wi-Fi")
        refresh_button.clicked.connect(self.refresh_wifi_cards)
        title_layout.addWidget(refresh_button)

        layout.addLayout(title_layout)

        # Scroll Area pour les cartes Wi-Fi
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
        """)
        layout.addWidget(scroll_area)

        # Widget contenant les cartes Wi-Fi
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(10)
        scroll_content.setLayout(self.scroll_layout)

        scroll_area.setWidget(scroll_content)

        # Initialiser le groupe de boutons radio pour la sélection
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        self.button_group.buttonClicked.connect(self.update_selected_adapter)

        # Récupérer les cartes Wi-Fi détectées
        self.load_wifi_cards()

    def create_white_icon(self, svg_path, size):
        """
        Charge un fichier SVG, le colore en blanc et retourne un QIcon.

        Args:
            svg_path (str): Chemin vers le fichier SVG.
            size (QSize): Taille souhaitée de l'icône.

        Returns:
            QIcon: Icône teintée en blanc.
        """
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)

        renderer = QSvgRenderer(svg_path)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()

        white_pixmap = QPixmap(size)
        white_pixmap.fill(Qt.white)

        white_icon = QPixmap(size)
        white_icon.fill(Qt.transparent)
        painter = QPainter(white_icon)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.drawPixmap(0, 0, white_pixmap)
        painter.end()

        return QIcon(white_icon)

    def resource_path(self, filename):
        """
        Retourne le chemin absolu vers le fichier d'icône SVG.
        """
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..','..', 'assets', 'icons')
        return os.path.join(base_path, filename)

    def load_wifi_cards(self):
        """
        Charge et affiche les cartes Wi-Fi détectées.
        """
        self.clear_wifi_cards()
        adapters = detect_wifi_adapters()

        if adapters:
            for adapter in adapters:
                card = WifiCard(adapter, self.button_group)
                self.scroll_layout.addWidget(card)
        else:
            no_wifi_label = QLabel("Aucune carte Wi-Fi USB détectée.")
            no_wifi_label.setFont(QFont("Arial", 12))
            no_wifi_label.setStyleSheet("color: #666;")
            no_wifi_label.setAlignment(Qt.AlignCenter)
            self.scroll_layout.addWidget(no_wifi_label)

        self.scroll_layout.addStretch()

    def clear_wifi_cards(self):
        """
        Supprime toutes les cartes Wi-Fi du layout.
        """
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def refresh_wifi_cards(self):
        """
        Rafraîchit la liste des cartes Wi-Fi détectées.
        """
        self.load_wifi_cards()

    def update_selected_adapter(self, button):
        """
        Met à jour l'adaptateur Wi-Fi sélectionné.

        Args:
            button (QRadioButton): Le bouton radio sélectionné.
        """
        card = button.parent()
        self.selected_adapter = card.adapter_info.get('Name') or card.adapter_info.get('Device') or None
        self.parent().parent().scan_button.set_enabled_scan(True)
