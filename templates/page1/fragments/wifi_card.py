# templates/page1/fragments/wifi_card.py
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QRadioButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class WifiCard(QFrame):
    """
    Représente une carte Wi-Fi affichant les informations de la carte.
    """
    def __init__(self, adapter_info, button_group, parent=None):
        super().__init__(parent)
        self.adapter_info = adapter_info
        self.selected = False
        self.button_group = button_group
        self.setup_ui()

    def setup_ui(self):
        # Style de la carte
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QFrame:hover {
                border: 1px solid #0078d7;
            }
        """)
        self.setFixedHeight(100)

        # Layout de la carte
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Bouton radio pour la sélection
        self.radio_button = QRadioButton()
        self.button_group.addButton(self.radio_button)
        layout.addWidget(self.radio_button)

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

    def is_selected(self):
        return self.radio_button.isChecked()
