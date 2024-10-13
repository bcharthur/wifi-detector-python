# templates/page1/index.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea, QSizePolicy, QPushButton
)
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QSize, Qt
from PyQt5.QtGui import QFont, QIcon
from assets.modules.modal import Modal
from templates.page1.functions.wifi_card_detect import detect_wifi_adapters
import os


class WifiCard(QFrame):
    """
    Représente une carte Wi-Fi affichant les informations de la carte.
    """

    def __init__(self, adapter_info, parent=None):
        super().__init__(parent)
        self.adapter_info = adapter_info
        self.setup_ui()

    def setup_ui(self):
        # Style de la carte
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)
        self.setFixedHeight(100)

        # Layout de la carte
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Informations de la carte Wi-Fi
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)

        # Nom de l'interface
        name = self.adapter_info.get('Name') or self.adapter_info.get('Device') or "N/A"
        interface_label = QLabel(f"Nom: {name}")
        interface_label.setFont(QFont("Arial", 12, QFont.Bold))
        interface_label.setStyleSheet("color: #333;")

        # Description / Hardware Port / ESSID
        if 'InterfaceDescription' in self.adapter_info:
            description = self.adapter_info['InterfaceDescription']
            desc_label = QLabel(f"Description: {description}")
        elif 'Hardware Port' in self.adapter_info:
            hardware_port = self.adapter_info['Hardware Port']
            desc_label = QLabel(f"Port Matériel: {hardware_port}")
        elif 'ESSID' in self.adapter_info:
            essid = self.adapter_info['ESSID']
            desc_label = QLabel(f"SSID: {essid}")
        else:
            desc_label = QLabel("Informations supplémentaires: N/A")

        desc_label.setFont(QFont("Arial", 10))
        desc_label.setStyleSheet("color: #555;")

        # Adresse MAC
        mac_address = self.adapter_info.get('MacAddress') or self.adapter_info.get('Ethernet Address', 'N/A')
        mac_label = QLabel(f"Adresse MAC: {mac_address}")
        mac_label.setFont(QFont("Arial", 10))
        mac_label.setStyleSheet("color: #555;")

        # État de la carte (Windows)
        if 'Status' in self.adapter_info:
            status = self.adapter_info['Status']
            status_label = QLabel(f"État: {status}")
            status_label.setFont(QFont("Arial", 10))
            status_label.setStyleSheet("color: #555;")
            info_layout.addWidget(status_label)

        # Ajouter les labels au layout d'informations
        info_layout.addWidget(interface_label)
        info_layout.addWidget(desc_label)
        info_layout.addWidget(mac_label)

        # Ajouter le layout d'informations au layout principal de la carte
        layout.addLayout(info_layout)

        # Si connecté (Windows), afficher le signal ou Access Point
        if 'Signal' in self.adapter_info:
            signal = self.adapter_info['Signal']
            signal_label = QLabel(f"Signal: {signal}")
            signal_label.setFont(QFont("Arial", 10))
            signal_label.setStyleSheet("color: #555;")
            signal_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            layout.addWidget(signal_label)
        elif 'Access Point' in self.adapter_info:
            ap = self.adapter_info['Access Point']
            ap_label = QLabel(f"Access Point: {ap}")
            ap_label.setFont(QFont("Arial", 10))
            ap_label.setStyleSheet("color: #555;")
            ap_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            layout.addWidget(ap_label)


class Index1(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)

        # Label de bienvenue
        welcome_label = QLabel("Bienvenue sur la Home")
        welcome_label.setObjectName("index_label")
        welcome_label.setFont(QFont("Arial", 16, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(welcome_label)

        # Cadre gris pour les cartes Wi-Fi
        wifi_frame = QFrame()
        wifi_frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        wifi_layout = QVBoxLayout()
        wifi_layout.setContentsMargins(10, 10, 10, 10)
        wifi_layout.setSpacing(10)
        wifi_frame.setLayout(wifi_layout)

        # Layout pour le titre et le bouton Refresh
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(10)

        # Label pour le cadre
        frame_label = QLabel("Cartes Wi-Fi Détectées")
        frame_label.setFont(QFont("Arial", 14, QFont.Bold))
        frame_label.setStyleSheet("color: #333;")
        frame_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_layout.addWidget(frame_label)

        # Bouton Refresh
        refresh_button = QPushButton()
        refresh_button.setIcon(QIcon(self.resource_path("refresh.svg")))
        refresh_button.setIconSize(QSize(24, 24))
        refresh_button.setFixedSize(40, 40)
        refresh_button.setToolTip("Actualiser la liste des cartes Wi-Fi")
        refresh_button.clicked.connect(self.refresh_wifi_cards)
        title_layout.addWidget(refresh_button)

        # Ajouter le layout titre au layout wifi
        wifi_layout.addLayout(title_layout)

        # Scroll Area pour les cartes Wi-Fi
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
        """)
        wifi_layout.addWidget(scroll_area)

        # Widget contenant les cartes Wi-Fi
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(10)
        scroll_content.setLayout(self.scroll_layout)

        scroll_area.setWidget(scroll_content)

        # Récupérer les cartes Wi-Fi détectées
        self.load_wifi_cards()

        # Ajouter le cadre au layout principal
        main_layout.addWidget(wifi_frame)

    def resource_path(self, filename):
        """
        Retourne le chemin absolu vers le fichier d'icône SVG.
        """
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets', 'icons')
        return os.path.join(base_path, filename)

    def load_wifi_cards(self):
        """
        Charge et affiche les cartes Wi-Fi détectées.
        """
        # Supprimer les cartes actuelles
        self.clear_wifi_cards()

        # Récupérer les cartes Wi-Fi détectées
        adapters = detect_wifi_adapters()

        if adapters:
            for adapter in adapters:
                card = WifiCard(adapter)
                self.scroll_layout.addWidget(card)
        else:
            no_wifi_label = QLabel("Aucune carte Wi-Fi USB détectée.")
            no_wifi_label.setFont(QFont("Arial", 12))
            no_wifi_label.setStyleSheet("color: #666;")
            no_wifi_label.setAlignment(Qt.AlignCenter)
            self.scroll_layout.addWidget(no_wifi_label)

        # Ajouter un stretch pour pousser les cartes vers le haut
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
