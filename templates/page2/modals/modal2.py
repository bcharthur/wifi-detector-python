# templates/page2/modals/modal2.py
from PyQt5.QtWidgets import QLabel
from assets.modules.modal import Modal
from PyQt5.QtCore import Qt

class Modal2(Modal):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(350, 250)  # Taille spécifique pour cette modale
        self.setWindowTitle("Modale 2")
        self.setup_content()

    def setup_content(self):
        """Définit le contenu spécifique de Modal2."""
        self.label = QLabel("Contenu de la Modale 2 avec des informations différentes.")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.insertWidget(0, self.label)  # Ajouter en haut du layout
