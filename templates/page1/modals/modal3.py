# templates/page1/modals/modal3.py
from PyQt5.QtWidgets import QLabel
from assets.modules.modal import Modal
from PyQt5.QtCore import Qt

class Modal3(Modal):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(500, 400)
        self.setWindowTitle("Modale 3")
        self.setup_content()

    def setup_content(self):
        """Définit le contenu spécifique de Modal3."""
        self.label = QLabel("Bienvenue dans la Modale 3 !")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.insertWidget(0, self.label)
