# templates/page1/index.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class Index1(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Bienvenue sur la page 2 ")
        label.setObjectName("index_label")
        layout.addWidget(label)
        self.setLayout(layout)
