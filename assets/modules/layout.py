import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QSizePolicy
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QSize, Qt
from templates.page1.index import Index1
from templates.page2.index import Index2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application avec Menu Latéral")
        self.resize(800, 500)  # Définir la taille initiale de la fenêtre (largeur, hauteur)

        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts principaux
        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(self.main_layout)

        # Layout pour la sidebar
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setSpacing(10)  # Espacement entre les éléments
        self.sidebar_layout.setContentsMargins(10, 10, 10, 10)  # Marges autour du contenu de la sidebar

        # Widgets de la sidebar
        self.sidebar = QWidget()
        self.sidebar.setLayout(self.sidebar_layout)

        # Définir les politiques de taille de la sidebar
        self.sidebar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # Titre de la sidebar avec hauteur fixe et fond blanc
        self.sidebar_title = QLabel("Menu Principal")
        self.sidebar_title.setFixedHeight(60)  # Hauteur fixe
        self.sidebar_title.setStyleSheet("""
            background-color: white;
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
        """)
        self.sidebar_title.setAlignment(Qt.AlignCenter)  # Centrer le texte
        self.sidebar_layout.addWidget(self.sidebar_title)

        # Créer les boutons avec icônes pour le menu latéral
        self.home_button = self.create_sidebar_button("Home", "home.svg")
        self.user_button = self.create_sidebar_button("User", "user.svg")
        self.settings_button = self.create_sidebar_button("Settings", "settings.svg")

        # Ajouter les boutons avec icônes au menu latéral
        self.sidebar_layout.addWidget(self.home_button)
        self.sidebar_layout.addWidget(self.user_button)
        self.sidebar_layout.addWidget(self.settings_button)

        # Connecter les boutons aux fonctions de navigation
        self.home_button.clicked.connect(self.show_home_page)
        self.user_button.clicked.connect(self.show_user_page)

        # Créer la topbar
        self.topbar = QWidget()
        self.topbar_layout = QHBoxLayout()
        self.topbar_layout.setContentsMargins(10, 10, 10, 10)  # Marges autour du contenu de la topbar
        self.topbar_layout.setSpacing(0)
        self.topbar.setLayout(self.topbar_layout)
        self.topbar.setFixedHeight(60)  # Hauteur fixe pour la topbar
        self.topbar.setStyleSheet("background-color: #f0f0f0;")  # Couleur de fond de la topbar

        # Bouton pour basculer le menu latéral avec une icône SVG (bars.svg)
        self.toggle_button = QPushButton()
        self.toggle_button.setIcon(QIcon(self.resource_path("bars.svg")))
        self.toggle_button.setIconSize(QSize(24, 24))  # Taille de l'icône
        self.toggle_button.setFixedSize(40, 40)  # Taille du bouton
        self.toggle_button.clicked.connect(self.toggle_sidebar)

        # Ajouter le bouton toggle à la topbar, aligné à droite
        self.topbar_layout.addStretch()  # Espace flexible pour pousser le bouton à droite
        self.topbar_layout.addWidget(self.toggle_button)

        # Layout pour le contenu de la page (avec la topbar en haut)
        self.content_with_topbar_layout = QVBoxLayout()
        self.content_with_topbar_layout.setSpacing(0)
        self.content_with_topbar_layout.setContentsMargins(0, 0, 0, 0)

        # Ajouter la topbar au layout de contenu
        self.content_with_topbar_layout.addWidget(self.topbar)

        # Layout pour le contenu des pages (Index1 et Index2)
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Ajouter le layout de contenu des pages juste en dessous de la topbar
        self.content_with_topbar_layout.addLayout(self.content_layout)

        # Widget de contenu principal
        self.content = QWidget()
        self.content.setLayout(self.content_with_topbar_layout)

        # Définir les politiques de taille
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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

    def show_home_page(self):
        # Supprimer tous les widgets actuels du layout de contenu
        self.clear_content_layout()

        # Ajouter la page Index1 (page Home)
        self.index1 = Index1()
        self.content_layout.addWidget(self.index1)

    def show_user_page(self):
        # Supprimer tous les widgets actuels du layout de contenu
        self.clear_content_layout()

        # Ajouter la page Index2 (page User)
        self.index2 = Index2()
        self.content_layout.addWidget(self.index2)

    def clear_content_layout(self):
        # Supprimer uniquement les widgets de content_layout (pas le bouton toggle)
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def create_sidebar_button(self, text, icon_filename):
        """
        Crée un bouton de la sidebar avec une icône SVG.
        Ajuste la politique de taille pour permettre l'expansion horizontale.
        """
        button = QPushButton(text)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Permet l'expansion horizontale
        icon_path = self.resource_path(icon_filename)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(24, 24))  # Taille de l'icône
        button.setStyleSheet("text-align: left; padding: 10px;")  # Optionnel: alignement du texte
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

            # Optionnel: Ajuster les icônes si nécessaire
            # self.home_button.setIcon(QIcon(self.resource_path("home_collapsed.svg")))
            # self.user_button.setIcon(QIcon(self.resource_path("user_collapsed.svg")))
            # self.settings_button.setIcon(QIcon(self.resource_path("settings_collapsed.svg")))
        else:
            # Agrandir la sidebar à sa largeur normale et attendre la fin de l'animation pour afficher les textes et le titre
            self.animate_sidebar(self.sidebar_width, self.show_sidebar_text)

        # Inverser l'état de la sidebar une seule fois
        self.sidebar_shown = not self.sidebar_shown

    def show_sidebar_text(self):
        """
        Réaffiche le texte des boutons et change le titre après que l'animation est terminée.
        Ajuste la largeur maximale des boutons pour correspondre à la largeur déployée de la sidebar.
        """
        self.sidebar_title.setText("Menu Principal")  # Remettre le titre complet
        self.home_button.setText("Home")
        self.user_button.setText("User")
        self.settings_button.setText("Settings")

        # Optionnel: Réajuster les icônes si nécessaire
        # self.home_button.setIcon(QIcon(self.resource_path("home.svg")))
        # self.user_button.setIcon(QIcon(self.resource_path("user.svg")))
        # self.settings_button.setIcon(QIcon(self.resource_path("settings.svg")))

        # Optionnel: Forcer la mise à jour des boutons
        self.home_button.updateGeometry()
        self.user_button.updateGeometry()
        self.settings_button.updateGeometry()

    def animate_sidebar(self, width, on_finished=None):
        """
        Anime la largeur de la sidebar entre la largeur actuelle et la nouvelle largeur donnée.
        """
        self.animation = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.sidebar.width())
        self.animation.setEndValue(width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.valueChanged.connect(self.adjust_button_sizes)

        if on_finished:
            self.animation.finished.connect(on_finished)  # Connecte la fonction à appeler après l'animation
        self.animation.start()

    def adjust_button_sizes(self, value):
        """
        Ajuste la largeur des boutons en fonction de la largeur actuelle de la sidebar.
        """
        self.home_button.setMaximumWidth(value)
        self.user_button.setMaximumWidth(value)
        self.settings_button.setMaximumWidth(value)

