# -----------------------------
# app/views/main_window.py
# -----------------------------

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableView, QLabel, QMessageBox
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Creative ERP')
        self.resize(1000, 700)
        
        # Widget central
        central = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel('Creative ERP — clientes, proyectos y facturas')
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        """Abre el diálogo para crear una nueva factura."""
        QMessageBox.information(self, 'Crear', 'Aquí abrirá el diálogo para crear una factura')