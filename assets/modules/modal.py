# assets/modules/modal.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
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

        # Contenu de la modal
        self.label = QLabel("Ceci est une fenêtre modale de test.")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.close_button = QPushButton("Fermer")
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button)
