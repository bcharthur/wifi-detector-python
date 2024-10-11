# assets/modules/sidebar.py
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("sidebar")

        # Layout de la sidebar
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Définir la politique de taille
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # Ajouter des boutons avec icônes
        self.add_sidebar_button("Accueil", "home.svg")
        self.add_sidebar_button("Profil", "user.svg")
        self.add_sidebar_button("Paramètres", "settings.svg")

        # Stretch pour pousser les éléments vers le haut
        self.layout.addStretch()

        # État du menu latéral
        self.sidebar_width = 200  # Largeur initiale
        self.setFixedWidth(self.sidebar_width)
        self.setMinimumWidth(self.sidebar_width)

    def add_sidebar_button(self, text, icon_filename):
        button = QPushButton(text)
        button.setObjectName("sidebar_button")

        # Charger l'icône SVG avec chemin absolu
        icon_path = self.resource_path(icon_filename)
        icon = QIcon(icon_path)
        button.setIcon(icon)
        button.setIconSize(QSize(24, 24))

        self.layout.addWidget(button)

    def resource_path(self, filename):
        """
        Retourne le chemin absolu vers le fichier d'icône.
        """
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, "icons", filename)
