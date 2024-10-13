# templates/page1/modals/modal1.py
from PyQt5.QtWidgets import QLabel
from assets.modules.modal import Modal
from PyQt5.QtCore import Qt

class Modal1(Modal):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 300)  # Taille spécifique pour cette modale
        self.setWindowTitle("Modale 1")
        self.setup_content()

    def setup_content(self):
        """Définit le contenu spécifique de Modal1."""
        self.label = QLabel("Contenu de la Modale 1.")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.insertWidget(0, self.label)  # Ajouter en haut du layout
