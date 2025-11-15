# -----------------------------
# app/views/main_window.py
# -----------------------------

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableView, QLabel
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
def __init__(self, parent=None):
super().__init__(parent)
self.setWindowTitle('Creative ERP')
self.resize(1000, 700)


central = QWidget()
layout = QVBoxLayout()


header = QLabel('Creative ERP — clientes, proyectos y facturas')
header.setAlignment(Qt.AlignCenter)
layout.addWidget(header)


# Botones rápidos
btn_new_invoice = QPushButton('Nueva factura')
btn_new_invoice.clicked.connect(self.open_new_invoice)
layout.addWidget(btn_new_invoice)


# Placeholder tabla de facturas
self.table = QTableView()
layout.addWidget(self.table)


central.setLayout(layout)
self.setCentralWidget(central)


def open_new_invoice(self):
# abrir diálogo para crear factura (implementar)
from PySide6.QtWidgets import QMessageBox
QMessageBox.information(self, 'Crear', 'Aquí abrirá el diálogo para crear una factura')