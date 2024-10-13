# templates/page1/index.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from templates.page1.modals.modal1 import Modal1
from templates.page1.modals.modal3 import Modal3


class Index1(QWidget):
    def __init__(self):
        super().__init__()

        # Créer la mise en page principale
        layout = QVBoxLayout()

        # Ajouter un label de bienvenue
        label = QLabel("Bienvenue sur la Home ")
        label.setObjectName("index_label")
        layout.addWidget(label)

        # Ajouter un bouton pour ouvrir Modal1
        self.open_modal1_button = QPushButton("Ouvrir la Modale 1")
        self.open_modal1_button.clicked.connect(self.show_modal1)
        layout.addWidget(self.open_modal1_button)

        # Ajouter un bouton pour ouvrir Modal3
        self.open_modal3_button = QPushButton("Ouvrir la Modale 3")
        self.open_modal3_button.clicked.connect(self.show_modal3)
        layout.addWidget(self.open_modal3_button)

        # Définir la mise en page pour ce widget
        self.setLayout(layout)

    def show_modal1(self):
        """Méthode pour afficher Modal1."""
        modal = Modal1(self)  # Créer une instance de Modal1
        modal.exec_()  # Afficher la modal de manière modale

    def show_modal3(self):
        """Méthode pour afficher Modal3."""
        modal = Modal3(self)  # Créer une instance de Modal3
        modal.exec_()  # Afficher la modal de manière modale