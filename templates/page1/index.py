# templates/page1/index.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from templates.page1.fragments.header import Header
from templates.page1.fragments.wifi_cards import WifiCards
from templates.page1.fragments.scan_button import ScanButton
from templates.page1.fragments.networks_display import NetworksDisplay
from templates.page1.functions.scan_wifi import scan_wifi


class Index1(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_adapter = None
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)

        # Ajouter le header
        self.header = Header()
        main_layout.addWidget(self.header)

        # Cadre gris pour les cartes Wi-Fi et le Scan button
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

        # Ajouter le widget WifiCards
        self.wifi_cards = WifiCards()
        wifi_layout.addWidget(self.wifi_cards)

        # Ajouter le ScanButton
        self.scan_button = ScanButton()
        self.scan_button.set_enabled_scan(False)  # Désactiver initialement
        self.scan_button.connect_scan(self.scan_wifi_networks)
        wifi_layout.addWidget(self.scan_button)

        # Ajouter le wifi_frame au layout principal
        main_layout.addWidget(wifi_frame)

        # Cadre pour les réseaux Wi-Fi disponibles
        networks_frame = QFrame()
        networks_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
        """)
        networks_layout = QVBoxLayout()
        networks_layout.setContentsMargins(10, 10, 10, 10)
        networks_layout.setSpacing(10)
        networks_frame.setLayout(networks_layout)

        # Ajouter le widget NetworksDisplay
        self.networks_display = NetworksDisplay()
        networks_layout.addWidget(self.networks_display)

        # Ajouter le networks_frame au layout principal
        main_layout.addWidget(networks_frame)

    def scan_wifi_networks(self):
        """
        Lance le scan des réseaux Wi-Fi en utilisant l'adaptateur sélectionné.
        """
        if not self.wifi_cards.selected_adapter:
            QMessageBox.warning(self, "Avertissement", "Veuillez sélectionner une carte Wi-Fi avant de scanner.")
            return

        # Afficher un message de chargement ou désactiver le bouton scan
        QMessageBox.information(self, "Scan en cours",
                                f"Scanning Wi-Fi networks using adapter: {self.wifi_cards.selected_adapter}")

        # Effectuer le scan
        networks = scan_wifi(self.wifi_cards.selected_adapter)

        # Afficher les réseaux dans la liste
        self.networks_display.display_networks(networks)
