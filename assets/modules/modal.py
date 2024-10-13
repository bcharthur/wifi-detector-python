# assets/modules/modal.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class Modal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("modal")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True)
        self.setFixedSize(300, 200)

        # Layout de la modal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        # Bouton de fermeture commun à toutes les modales
        self.close_button = QPushButton("Fermer")
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button)

    def setup_content(self):
        """Méthode à surcharger pour définir le contenu spécifique de la modale."""
        pass
