# templates/page1/fragments/scan_button.py
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
import os


class ScanButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.button = QPushButton("Scan Wi-Fi")
        self.button.setIcon(self.create_white_icon(self.resource_path("scan.svg"), QSize(24, 24)))
        self.button.setIconSize(QSize(24, 24))
        self.button.setFixedHeight(40)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        layout.addWidget(self.button)

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

    def set_enabled_scan(self, enabled):
        """
        Active ou désactive le bouton de scan.

        Args:
            enabled (bool): État d'activation.
        """
        self.button.setEnabled(enabled)

    def connect_scan(self, callback):
        """
        Connecte le bouton de scan à une fonction de rappel.

        Args:
            callback (callable): Fonction à appeler lors du clic.
        """
        self.button.clicked.connect(callback)
