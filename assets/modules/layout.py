# layout.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy
)
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtCore import QRect
from templates.page1 import index # Assurez-vous que cet import est correct
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
        self.sidebar_layout.setSpacing(0)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
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

        # Bouton pour basculer le menu latéral
        self.toggle_button = QPushButton("Toggle Menu")
        self.toggle_button.clicked.connect(self.toggle_sidebar)

        # Ajouter des widgets au menu latéral
        self.sidebar_layout.addWidget(QPushButton("Home"))
        self.sidebar_layout.addWidget(QPushButton("User"))
        self.sidebar_layout.addWidget(QPushButton("Settings"))

        # Ajouter des widgets au contenu principal
        self.content_layout.addWidget(self.toggle_button)

        # Ajouter le menu latéral et le contenu principal au layout principal
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content)

        # État du menu latéral
        self.sidebar_shown = True
        self.sidebar_width = 200  # Largeur initiale du menu latéral
        self.sidebar.setFixedWidth(self.sidebar_width)
        self.sidebar.setMinimumWidth(self.sidebar_width)

        # Ajouter cet attribut après la création du widget sidebar
        self.sidebar.setObjectName("sidebar")

        # Instance de la page Index1
        self.index1 = Index1()
        self.content_layout.addWidget(self.index1)

    def toggle_sidebar(self):
        if self.sidebar_shown:
            # Cacher le menu latéral
            self.animate_sidebar(0)
        else:
            # Afficher le menu latéral
            self.animate_sidebar(self.sidebar_width)
        self.sidebar_shown = not self.sidebar_shown

    def animate_sidebar(self, width):
        self.animation = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.sidebar.width())
        self.animation.setEndValue(width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()
