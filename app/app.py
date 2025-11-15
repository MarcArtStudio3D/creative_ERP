# -----------------------------
# app/app.py
# -----------------------------

from PySide6 import QtWidgets
from .views.main_window import MainWindow
import sys




def run_app():
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())