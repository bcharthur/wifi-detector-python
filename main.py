# main.py
import sys
import os
from PyQt5.QtWidgets import QApplication
from assets.modules.layout import MainWindow

def load_stylesheet():
    """
    Charge et concatène tous les fichiers QSS du dossier assets/styles.
    """
    style_files = [
        os.path.join("assets", "styles", "layout.qss"),
        os.path.join("assets", "styles", "button.qss"),
        os.path.join("assets", "styles", "modal.qss"),
        os.path.join("assets", "styles", "sidebar.qss"),
    ]
    style = ""
    for file in style_files:
        if os.path.exists(file):
            with open(file, "r") as f:
                style += f.read() + "\n"
        else:
            print(f"Le fichier de style {file} n'a pas été trouvé.")
    return style

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Charger le style QSS
    style = load_stylesheet()
    app.setStyleSheet(style)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
