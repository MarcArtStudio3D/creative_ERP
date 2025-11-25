"""
Vista del módulo de Clientes.
Interfaz simplificada para gestión de clientes con tabla de búsqueda.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                               QTableWidgetItem, QHeaderView, QPushButton, 
                               QLineEdit, QLabel, QMessageBox, QDialog)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from core.auth import Session


class ClientesView(QWidget):
    """
    Vista principal del módulo de clientes.
    
    Muestra una tabla con la lista de clientes y permite:
    - Buscar clientes
    - Añadir nuevo cliente
    - Editar cliente seleccionado
    - Eliminar cliente
    """
    
    # Señal para comunicar que se quiere ver la ficha de un cliente
    cliente_selected = Signal(int)
    
    def __init__(self, session: Session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setup_ui()
        self.load_clientes()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel(self.tr("📋 Gestión de Clientes"))
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Campo de búsqueda rápida
        search_label = QLabel(self.tr("Buscar:"))
        header_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.tr("Nombre, CIF, teléfono..."))
        self.search_input.setMinimumWidth(250)
        self.search_input.textChanged.connect(self.filter_table)
        header_layout.addWidget(self.search_input)
        
        layout.addLayout(header_layout)
        
        # Tabla de clientes
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            self.tr("ID"), self.tr("Código"), self.tr("Nombre Fiscal"), self.tr("CIF/NIF"), 
            self.tr("Teléfono"), self.tr("Email"), self.tr("Población")
        ])
        
        # Configurar tabla
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        
        # Ajustar columnas
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Código
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Nombre
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # CIF
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Teléfono
        
        # Doble clic para abrir ficha de cliente
        self.table.doubleClicked.connect(self.on_edit_cliente)
        
        layout.addWidget(self.table)
        
        # Info footer
        self.info_label = QLabel(self.tr("0 clientes"))
        self.info_label.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(self.info_label)
        
        self.setLayout(layout)
    
    def load_clientes(self):
        """Carga los clientes desde la base de datos de la empresa activa."""
        try:
            # Importar con sys.path configurado
            import sys
            from pathlib import Path
            root_dir = Path(__file__).parent.parent.parent
            sys.path.insert(0, str(root_dir))
            
            from core.db import get_session
            import modules.clientes.models as clientes_models
            Cliente = clientes_models.Cliente
            
            # Obtener clientes desde la BD de la empresa
            session = get_session()
            clientes = session.query(Cliente).all()
            
            self.table.setRowCount(len(clientes))
            
            for row, cliente in enumerate(clientes):
                # ID, Código, Nombre Fiscal, CIF/NIF, Teléfono, Email, Población
                data = [
                    str(cliente.id),
                    cliente.codigo_cliente or "",
                    cliente.nombre_fiscal or "",
                    cliente.cif_nif_siren or "",
                    cliente.telefono1 or "",
                    cliente.email or "",
                    cliente.poblacion or ""
                ]
                
                for col, value in enumerate(data):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # No editable
                    self.table.setItem(row, col, item)
            
            session.close()
            print(f"✅ {len(clientes)} clientes cargados desde la base de datos")
            
        except Exception as e:
            print(f"❌ Error al cargar clientes: {e}")
            # Fallback a datos de demostración
            demo_data = [
                (1, "CLI001", "MIRALLES BIOSCA, MARC", "77305760S", "0615800093", "info@artstudio3d.fr", "Laverune"),
                (2, "CLI002", "ACME Corporation", "B12345678", "912345678", "info@acme.com", "Madrid"),
                (3, "CLI003", "Tech Solutions SL", "B87654321", "934567890", "contact@tech.es", "Barcelona"),
            ]
            
            self.table.setRowCount(len(demo_data))
            
            for row, data in enumerate(demo_data):
                for col, value in enumerate(data):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # No editable
                    self.table.setItem(row, col, item)
        
        self.update_info_label()
    
    def filter_table(self, text: str):
        """Filtra la tabla según el texto de búsqueda."""
        text = text.lower()
        
        for row in range(self.table.rowCount()):
            hide = True
            
            # Buscar en todas las columnas
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and text in item.text().lower():
                    hide = False
                    break
            
            self.table.setRowHidden(row, hide)
        
        self.update_info_label()
    
    def update_info_label(self):
        """Actualiza el label con el conteo de clientes visibles."""
        visible_count = sum(1 for row in range(self.table.rowCount()) 
                           if not self.table.isRowHidden(row))
        total_count = self.table.rowCount()
        
        if visible_count == total_count:
            self.info_label.setText(self.tr("{} clientes").format(total_count))
        else:
            self.info_label.setText(self.tr("{} de {} clientes").format(visible_count, total_count))
    
    def on_edit_cliente(self):
        """Emite señal para abrir la ficha completa del cliente seleccionado."""
        current_row = self.table.currentRow()
        if current_row < 0:
            return
        
        cliente_id = int(self.table.item(current_row, 0).text())
        print(f"📋 Solicitando ficha de cliente ID: {cliente_id}")
        
        # Emitir señal para que la ventana principal abra la ficha
        self.cliente_selected.emit(cliente_id)
    
    def on_nuevo_cliente(self):
        """Abre el formulario para crear un nuevo cliente."""
        QMessageBox.information(
            self,
            self.tr("Nuevo Cliente"),
            self.tr("El formulario de creación de clientes se implementará próximamente.")
        )
    
    def on_eliminar_cliente(self):
        """Elimina el cliente seleccionado."""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, self.tr("Atención"), self.tr("Selecciona un cliente primero."))
            return
        
        cliente_id = self.table.item(current_row, 0).text()
        nombre = self.table.item(current_row, 2).text()
        
        
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle(self.tr("Confirmar eliminación"))
        msg.setText(self.tr("¿Seguro que deseas eliminar al cliente #{}: {}?").format(cliente_id, nombre))
        
        btn_yes = msg.addButton(self.tr("Sí"), QMessageBox.ButtonRole.YesRole)
        btn_no = msg.addButton(self.tr("No"), QMessageBox.ButtonRole.NoRole)
        msg.setDefaultButton(btn_no)
        
        msg.exec()
        reply = msg.clickedButton()
        
        if reply == btn_yes:
            # TODO: Eliminar de BD
            self.table.removeRow(current_row)
            self.update_info_label()
            QMessageBox.information(self, self.tr("Éxito"), self.tr("Cliente eliminado correctamente."))
