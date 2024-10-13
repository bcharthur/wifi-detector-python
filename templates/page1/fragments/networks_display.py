# templates/page1/fragments/networks_display.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class NetworksDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        self.setLayout(layout)

        # Label pour les réseaux
        networks_label = QLabel("Réseaux Wi-Fi Disponibles")
        networks_label.setFont(QFont("Arial", 14, QFont.Bold))
        networks_label.setStyleSheet("color: #333;")
        networks_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(networks_label)

        # Liste pour afficher les réseaux
        self.networks_list = QListWidget()
        self.networks_list.setStyleSheet("""
            QListWidget {
                background-color: #f9f9f9;
                border: none;
                border-radius: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:last-child {
                border-bottom: none;
            }
        """)
        layout.addWidget(self.networks_list)

    def display_networks(self, networks):
        """
        Affiche les réseaux Wi-Fi dans la liste.

        Args:
            networks (list of dict): Liste des réseaux Wi-Fi détectés.
        """
        self.networks_list.clear()
        if networks:
            for network in networks:
                ssid = network.get('SSID', 'N/A')
                bssid = network.get('BSSID', 'N/A')
                signal = network.get('Signal', 0)
                auth = network.get('Authentication', 'N/A')
                cipher = network.get('Cipher', 'N/A')
                item_text = f"SSID: {ssid} | Signal: {signal}% | Auth: {auth} | Cipher: {cipher}"
                item = QListWidgetItem(item_text)
                self.networks_list.addItem(item)
        else:
            self.networks_list.addItem("Aucun réseau Wi-Fi détecté.")
