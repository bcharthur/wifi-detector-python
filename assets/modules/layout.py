# layout.py
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QSizePolicy
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QSize, Qt
from templates.page1.index import Index1

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application avec Menu Latéral")

        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(self.main_layout)
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setSpacing(10)  # Espacement entre les éléments
        self.sidebar_layout.setContentsMargins(10, 10, 10, 10)  # Marges autour du contenu de la sidebar
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Widgets
        self.sidebar = QWidget()
        self.sidebar.setLayout(self.sidebar_layout)
        self.content = QWidget()
        self.content.setLayout(self.content_layout)

        # Définir les politiques de taille
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Titre de la sidebar
        self.sidebar_title = QLabel("Menu Principal")
        self.sidebar_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.sidebar_title.setAlignment(Qt.AlignCenter)  # Centrer le texte

        # Ajouter le titre au début du layout de la sidebar
        self.sidebar_layout.addWidget(self.sidebar_title)

        # Bouton pour basculer le menu latéral avec une icône SVG (bars.svg)
        self.toggle_button = QPushButton()
        self.toggle_button.setIcon(QIcon(self.resource_path("bars.svg")))
        self.toggle_button.setIconSize(QSize(24, 24))  # Taille de l'icône
        self.toggle_button.setFixedSize(40, 40)  # Taille du bouton
        self.toggle_button.clicked.connect(self.toggle_sidebar)

        # Créer les boutons avec icônes pour le menu latéral
        self.home_button = self.create_sidebar_button("Home", "home.svg")
        self.user_button = self.create_sidebar_button("User", "user.svg")
        self.settings_button = self.create_sidebar_button("Settings", "settings.svg")

        # Ajouter les boutons avec icônes au menu latéral
        self.sidebar_layout.addWidget(self.home_button)
        self.sidebar_layout.addWidget(self.user_button)
        self.sidebar_layout.addWidget(self.settings_button)

        # Ajouter des widgets au contenu principal
        self.content_layout.addWidget(self.toggle_button)

        # Ajouter le menu latéral et le contenu principal au layout principal
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content)

        # État du menu latéral
        self.sidebar_shown = True
        self.sidebar_width = 200  # Largeur initiale du menu latéral
        self.sidebar_collapsed_width = 60  # Largeur lorsque le menu est replié
        self.sidebar.setFixedWidth(self.sidebar_width)
        self.sidebar.setMinimumWidth(self.sidebar_width)

        # Ajouter cet attribut après la création du widget sidebar
        self.sidebar.setObjectName("sidebar")

        # Instance de la page Index1
        self.index1 = Index1()
        self.content_layout.addWidget(self.index1)

    def create_sidebar_button(self, text, icon_filename):
        """
        Crée un bouton de la sidebar avec une icône SVG.
        """
        button = QPushButton(text)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        icon_path = self.resource_path(icon_filename)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(24, 24))  # Taille de l'icône
        return button

    def resource_path(self, filename):
        """
        Retourne le chemin absolu vers le fichier d'icône SVG.
        """
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'icons')
        return os.path.join(base_path, filename)

    def toggle_sidebar(self):
        if self.sidebar_shown:
            # Réduire la sidebar à la largeur "collapse"
            self.animate_sidebar(self.sidebar_collapsed_width)
            # Changer le titre en "MP" et masquer immédiatement les textes des boutons
            self.sidebar_title.setText("MP")
            self.home_button.setText("")
            self.user_button.setText("")
            self.settings_button.setText("")
        else:
            # Agrandir la sidebar à sa largeur normale et attendre la fin de l'animation pour afficher les textes et le titre
            self.animate_sidebar(self.sidebar_width, self.show_sidebar_text)

        self.sidebar_shown = not self.sidebar_shown

    def show_sidebar_text(self):
        """
        Réaffiche le texte des boutons et change le titre après que l'animation est terminée.
        """
        self.sidebar_title.setText("Menu Principal")  # Remettre le titre complet
        self.home_button.setText("Home")
        self.user_button.setText("User")
        self.settings_button.setText("Settings")

    def animate_sidebar(self, width, on_finished=None):
        """
        Anime la largeur de la sidebar entre la largeur actuelle et la nouvelle largeur donnée.
        """
        self.animation = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.sidebar.width())
        self.animation.setEndValue(width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        if on_finished:
            self.animation.finished.connect(on_finished)  # Connecte la fonction à appeler après l'animation
        self.animation.start()
