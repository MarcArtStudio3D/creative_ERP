#!/usr/bin/env python3
"""
Selector sencillo para consultas/búsqueda de datos
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                              QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                              QHeaderView, QAbstractItemView)
from PySide6.QtCore import Qt


class SimpleDataSelector(QDialog):
    """Diálogo sencillo para selección de datos"""
    
    def __init__(self, parent=None, title="Seleccionar elemento", headers=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr(title))
        self.setModal(True)
        self.resize(600, 400)
        
        self.selected_data = None
        self.data = []
        self.headers = headers or []
        self.filtered_data = []
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Configurar la interfaz de usuario (UI)"""
        layout = QVBoxLayout(self)
        
        # Search section
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel(self.tr("Buscar:")))
        
        self.search_edit = QLineEdit()
        self.search_edit.textChanged.connect(self._filter_data)
        search_layout.addWidget(self.search_edit)
        
        layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self.accept)
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.accept_btn = QPushButton(self.tr("Aceptar"))
        self.accept_btn.clicked.connect(self._on_accept)
        self.accept_btn.setDefault(True)
        button_layout.addWidget(self.accept_btn)
        
        cancel_btn = QPushButton(self.tr("Cancelar"))
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
    def set_data(self, data, headers=None):
        """Establecer los datos a mostrar"""
        self.data = data
        self.filtered_data = data.copy()
        if headers:
            self.headers = headers
            
        self._update_table()
        
    def _update_table(self):
        """Actualizar la tabla con los datos actualmente filtrados"""
        if not self.headers or not self.filtered_data:
            return
            
        self.table.setRowCount(len(self.filtered_data))
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        
        for row, item_data in enumerate(self.filtered_data):
            for col, header in enumerate(self.headers):
                # Convert header to lowercase key
                key = header.lower()
                if key == 'id':
                    key = 'id'
                elif key == 'código':
                    key = 'codigo'
                elif key == 'sección':
                    key = 'seccion'
                    
                value = item_data.get(key, '')
                table_item = QTableWidgetItem(str(value))
                table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, table_item)
        
        # Adjust column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        if len(self.headers) > 2:
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            
    def _filter_data(self, text):
        """Filtrar datos según el texto de búsqueda"""
        text = text.lower()
        if not text:
            self.filtered_data = self.data.copy()
        else:
            self.filtered_data = []
            for item in self.data:
                # Search in codigo and seccion fields
                codigo = str(item.get('codigo', '')).lower()
                seccion = str(item.get('seccion', '')).lower()
                if text in codigo or text in seccion:
                    self.filtered_data.append(item)
                    
        self._update_table()
        
    def _on_accept(self):
        """Gestionar pulsación del botón aceptar"""
        current_row = self.table.currentRow()
        if current_row >= 0 and current_row < len(self.filtered_data):
            self.selected_data = self.filtered_data[current_row]
            self.accept()
        
    def get_selected_data(self):
        """Devolver los datos seleccionados"""
        return self.selected_data
    
    @staticmethod
    def select_data(parent, data, headers, title="Seleccionar elemento"):
        """Método estático que muestra el diálogo y devuelve la fila seleccionada"""
        dialog = SimpleDataSelector(parent, title, headers)
        dialog.set_data(data, headers)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return dialog.get_selected_data()
        return None