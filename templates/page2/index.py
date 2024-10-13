# templates/page1/index.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from templates.page1.modals.modal1 import Modal1
from templates.page2.modals.modal2 import Modal2


class Index2(QWidget):
    def __init__(self):
        super().__init__()

        # Créer la mise en page principale
        layout = QVBoxLayout()

        # Ajouter un label de bienvenue
        label = QLabel("Bienvenue sur la User ")
        label.setObjectName("index_label")
        layout.addWidget(label)

        # Ajouter un bouton pour ouvrir Modal2
        self.open_modal2_button = QPushButton("Ouvrir la Modale 2")
        self.open_modal2_button.clicked.connect(self.show_modal2)
        layout.addWidget(self.open_modal2_button)

        # Définir la mise en page pour ce widget
        self.setLayout(layout)

    def show_modal2(self):
        """Méthode pour afficher Modal2."""
        modal = Modal2(self)  # Créer une instance de Modal2
        modal.exec_()  # Afficher la modal de manière modale
