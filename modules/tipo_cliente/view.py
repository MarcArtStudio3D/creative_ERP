"""
Vista del módulo de Tipos de Cliente
Basado en frmtipocliente.cpp
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QListView, QPushButton, QLabel, QLineEdit,
    QMessageBox, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QStringListModel
from PySide6.QtGui import QStandardItemModel, QStandardItem
from sqlalchemy.orm import Session
from typing import Optional

from modules.tipo_cliente.repository import TipoClienteRepository
from modules.tipo_cliente.models import TipoCliente, TipoSubCliente


class TipoClienteView(QDialog):
    """
    Vista para gestión de tipos y subtipos de clientes
    
    Características:
    - Lista de tipos de cliente (izquierda)
    - Lista de subtipos de cliente (derecha)
    - Formulario para editar nombre y descripción
    - Operaciones CRUD para tipos y subtipos
    """
    
    def __init__(self, session: Session, parent=None):
        super().__init__(parent)
        self.session = session
        self.repository = TipoClienteRepository(session)
        
        # Estado
        self.current_tipo_id: Optional[int] = None
        self.current_subtipo_id: Optional[int] = None
        self.edit_tipo = True  # True = editando tipo, False = editando subtipo
        
        self.setup_ui()
        self.load_tipos()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.setWindowTitle(self.tr("Tipos de Cliente"))
        self.setMinimumSize(676, 459)
        
        # Layout principal
        main_layout = QGridLayout()
        
        # ==================== SECCIÓN TIPOS (Izquierda) ====================
        tipos_layout = QGridLayout()
        
        # Lista de tipos
        self.lista_tipos = QListView()
        self.model_tipos = QStandardItemModel()
        self.lista_tipos.setModel(self.model_tipos)
        self.lista_tipos.clicked.connect(self.on_lista_tipos_clicked)
        tipos_layout.addWidget(self.lista_tipos, 0, 0, 1, 2)
        
        # Botones de tipos
        self.btnEditarTipo = QPushButton(self.tr("Guardar cambios"))
        self.btnEditarTipo.clicked.connect(self.on_btnEditarTipo_clicked)
        tipos_layout.addWidget(self.btnEditarTipo, 1, 0)
        
        self.btnBorrarTipo = QPushButton(self.tr("Borrar"))
        self.btnBorrarTipo.clicked.connect(self.on_btnBorrarTipo_clicked)
        tipos_layout.addWidget(self.btnBorrarTipo, 1, 1)
        
        main_layout.addLayout(tipos_layout, 0, 0)
        
        # ==================== SECCIÓN SUBTIPOS (Derecha) ====================
        subtipos_layout = QGridLayout()
        
        # Lista de subtipos
        self.lista_subtipos = QListView()
        self.model_subtipos = QStandardItemModel()
        self.lista_subtipos.setModel(self.model_subtipos)
        self.lista_subtipos.clicked.connect(self.on_lista_subtipos_clicked)
        subtipos_layout.addWidget(self.lista_subtipos, 0, 0, 1, 2)
        
        # Botones de subtipos
        self.btnEditarSubTipo = QPushButton(self.tr("Guardar cambios"))
        self.btnEditarSubTipo.clicked.connect(self.on_btnEditarSubTipo_clicked)
        subtipos_layout.addWidget(self.btnEditarSubTipo, 1, 0)
        
        self.btnBorrarSubTipo = QPushButton(self.tr("Borrar"))
        self.btnBorrarSubTipo.clicked.connect(self.on_btnBorrarSubTipo_clicked)
        subtipos_layout.addWidget(self.btnBorrarSubTipo, 1, 1)
        
        main_layout.addLayout(subtipos_layout, 0, 1)
        
        # ==================== FORMULARIO DE EDICIÓN ====================
        form_layout = QGridLayout()
        
        # Nombre
        label_nombre = QLabel(self.tr("Nombre"))
        label_nombre.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        form_layout.addWidget(label_nombre, 0, 0)
        
        self.txtNombre = QLineEdit()
        form_layout.addWidget(self.txtNombre, 0, 1)
        
        # Descripción
        label_desc = QLabel(self.tr("Descripción"))
        form_layout.addWidget(label_desc, 1, 0)
        
        self.txtDesc = QLineEdit()
        form_layout.addWidget(self.txtDesc, 1, 1)
        
        main_layout.addLayout(form_layout, 1, 0, 1, 2)
        
        # ==================== BOTONES INFERIORES ====================
        bottom_layout = QHBoxLayout()
        
        self.btnAddTipo = QPushButton(self.tr("Añadir Tipo cliente"))
        self.btnAddTipo.clicked.connect(self.on_btnAddTipo_clicked)
        bottom_layout.addWidget(self.btnAddTipo)
        
        self.btnAddSubTipo = QPushButton(self.tr("Añadir Subtipo cliente"))
        self.btnAddSubTipo.clicked.connect(self.on_btnAddSubTipo_clicked)
        bottom_layout.addWidget(self.btnAddSubTipo)
        
        # Spacer
        bottom_layout.addItem(QSpacerItem(287, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        self.btnSalir = QPushButton(self.tr("Salir"))
        self.btnSalir.clicked.connect(self.close)
        bottom_layout.addWidget(self.btnSalir)
        
        main_layout.addLayout(bottom_layout, 2, 0, 1, 2)
        
        self.setLayout(main_layout)
    
    # ==================== CARGA DE DATOS ====================
    
    def load_tipos(self):
        """Carga la lista de tipos de cliente"""
        self.model_tipos.clear()
        
        try:
            tipos = self.repository.obtener_todos_tipos()
            
            for tipo in tipos:
                item = QStandardItem(tipo.nombre)
                item.setData(tipo.id, Qt.ItemDataRole.UserRole)
                item.setEditable(False)
                self.model_tipos.appendRow(item)
                
        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr("Error"),
                self.tr("Error al cargar tipos de cliente: {}").format(str(e))
            )
    
    def load_subtipos(self, id_tipo: int):
        """Carga la lista de subtipos para un tipo específico"""
        self.model_subtipos.clear()
        
        try:
            subtipos = self.repository.obtener_subtipos(id_tipo)
            
            for subtipo in subtipos:
                item = QStandardItem(subtipo.nombre)
                item.setData(subtipo.id, Qt.ItemDataRole.UserRole)
                item.setEditable(False)
                self.model_subtipos.appendRow(item)
                
        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr("Error"),
                self.tr("Error al cargar subtipos: {}").format(str(e))
            )
    
    # ==================== EVENTOS DE SELECCIÓN ====================
    
    def on_lista_tipos_clicked(self, index):
        """Maneja el clic en la lista de tipos"""
        if not index.isValid():
            return
        
        item = self.model_tipos.itemFromIndex(index)
        tipo_id = item.data(Qt.ItemDataRole.UserRole)
        
        try:
            tipo = self.repository.obtener_tipo_por_id(tipo_id)
            if tipo:
                self.current_tipo_id = tipo_id
                self.current_subtipo_id = None
                self.edit_tipo = True
                
                self.txtNombre.setText(tipo.nombre)
                self.txtDesc.setText(tipo.desc or "")
                
                # Cargar subtipos
                self.load_subtipos(tipo_id)
                
        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr("Error"),
                self.tr("Error al cargar tipo: {}").format(str(e))
            )
    
    def on_lista_subtipos_clicked(self, index):
        """Maneja el clic en la lista de subtipos"""
        if not index.isValid():
            return
        
        item = self.model_subtipos.itemFromIndex(index)
        subtipo_id = item.data(Qt.ItemDataRole.UserRole)
        
        try:
            subtipo = self.repository.obtener_subtipo_por_id(subtipo_id)
            if subtipo:
                self.current_subtipo_id = subtipo_id
                self.edit_tipo = False
                
                self.txtNombre.setText(subtipo.nombre)
                self.txtDesc.setText(subtipo.desc or "")
                
        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr("Error"),
                self.tr("Error al cargar subtipo: {}").format(str(e))
            )
    
    # ==================== OPERACIONES CON TIPOS ====================
    
    def on_btnAddTipo_clicked(self):
        """Añade un nuevo tipo de cliente"""
        nombre = self.txtNombre.text().strip()
        desc = self.txtDesc.text().strip()
        
        if not nombre or not desc:
            QMessageBox.warning(
                self,
                self.tr("Campos vacíos"),
                self.tr("Por favor, rellene los datos antes de añadir")
            )
            return
        
        try:
            self.repository.crear_tipo(nombre, desc)
            self.load_tipos()
            
            # Limpiar campos
            self.txtNombre.clear()
            self.txtDesc.clear()
            
            QMessageBox.information(
                self,
                self.tr("Éxito"),
                self.tr("Tipo cliente insertado con éxito")
            )
            
        except ValueError as e:
            QMessageBox.warning(
                self,
                self.tr("Error de validación"),
                str(e)
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr("Error al añadir tipo cliente"),
                str(e)
            )
    
    def on_btnEditarTipo_clicked(self):
        """Edita el tipo de cliente seleccionado"""
        if self.current_tipo_id is None:
            QMessageBox.warning(
                self,
                self.tr("Seleccione tipo"),
                self.tr("Por favor, seleccione el tipo de cliente\nque desea editar.")
            )
            return
        
        nombre = self.txtNombre.text().strip()
        desc = self.txtDesc.text().strip()
        
        try:
            self.repository.actualizar_tipo(self.current_tipo_id, nombre, desc)
            self.load_tipos()
            
            QMessageBox.information(
                self,
                self.tr("Éxito"),
                self.tr("Tipo cliente actualizado con éxito")
            )
            
        except ValueError as e:
            QMessageBox.warning(
                self,
                self.tr("Error de validación"),
                str(e)
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr("Error al actualizar tipo cliente"),
                str(e)
            )
    
    def on_btnBorrarTipo_clicked(self):
        """Borra el tipo de cliente seleccionado"""
        if self.current_tipo_id is None:
            QMessageBox.warning(
                self,
                self.tr("Seleccione tipo"),
                self.tr("Por favor, seleccione el tipo de cliente\nque desea borrar.")
            )
            return
        
        # Confirmar eliminación
        reply = QMessageBox.question(
            self,
            self.tr("Confirmar eliminación"),
            self.tr("¿Está seguro de que desea borrar este tipo?\nSe eliminarán también todos sus subtipos."),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.No:
            return
        
        try:
            self.repository.eliminar_tipo(self.current_tipo_id)
            self.current_tipo_id = None
            self.current_subtipo_id = None
            
            self.load_tipos()
            self.model_subtipos.clear()
            self.txtNombre.clear()
            self.txtDesc.clear()
            
            QMessageBox.information(
                self,
                self.tr("Éxito"),
                self.tr("Tipo cliente borrado con éxito")
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr("Error al borrar tipo cliente"),
                str(e)
            )
    
    # ==================== OPERACIONES CON SUBTIPOS ====================
    
    def on_btnAddSubTipo_clicked(self):
        """Añade un nuevo subtipo de cliente"""
        nombre = self.txtNombre.text().strip()
        desc = self.txtDesc.text().strip()
        
        if not nombre or not desc:
            QMessageBox.warning(
                self,
                self.tr("Campos vacíos"),
                self.tr("Por favor, rellene los datos antes de añadir")
            )
            return
        
        if self.current_tipo_id is None:
            QMessageBox.warning(
                self,
                self.tr("Seleccione tipo"),
                self.tr("Por favor, seleccione el tipo de cliente\nal que desea añadir un subtipo.")
            )
            return
        
        try:
            self.repository.crear_subtipo(self.current_tipo_id, nombre, desc)
            self.load_subtipos(self.current_tipo_id)
            
            # Limpiar campos
            self.txtNombre.clear()
            self.txtDesc.clear()
            
            QMessageBox.information(
                self,
                self.tr("Éxito"),
                self.tr("Subtipo cliente insertado con éxito")
            )
            
        except ValueError as e:
            QMessageBox.warning(
                self,
                self.tr("Error de validación"),
                str(e)
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr("Error al añadir subtipo cliente"),
                str(e)
            )
    
    def on_btnEditarSubTipo_clicked(self):
        """Edita el subtipo de cliente seleccionado"""
        if self.current_subtipo_id is None:
            QMessageBox.warning(
                self,
                self.tr("Seleccione subtipo"),
                self.tr("Por favor, seleccione el subtipo de cliente\nque desea editar.")
            )
            return
        
        nombre = self.txtNombre.text().strip()
        desc = self.txtDesc.text().strip()
        
        try:
            self.repository.actualizar_subtipo(self.current_subtipo_id, nombre, desc)
            
            if self.current_tipo_id:
                self.load_subtipos(self.current_tipo_id)
            
            QMessageBox.information(
                self,
                self.tr("Éxito"),
                self.tr("Subtipo cliente actualizado con éxito")
            )
            
        except ValueError as e:
            QMessageBox.warning(
                self,
                self.tr("Error de validación"),
                str(e)
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr("Error al actualizar subtipo cliente"),
                str(e)
            )
    
    def on_btnBorrarSubTipo_clicked(self):
        """Borra el subtipo de cliente seleccionado"""
        if self.current_subtipo_id is None:
            QMessageBox.warning(
                self,
                self.tr("Seleccione subtipo"),
                self.tr("Por favor, seleccione el subtipo de cliente\nque desea borrar.")
            )
            return
        
        # Confirmar eliminación
        reply = QMessageBox.question(
            self,
            self.tr("Confirmar eliminación"),
            self.tr("¿Está seguro de que desea borrar este subtipo?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.No:
            return
        
        try:
            self.repository.eliminar_subtipo(self.current_subtipo_id)
            self.current_subtipo_id = None
            
            if self.current_tipo_id:
                self.load_subtipos(self.current_tipo_id)
            
            self.txtNombre.clear()
            self.txtDesc.clear()
            
            QMessageBox.information(
                self,
                self.tr("Éxito"),
                self.tr("Subtipo cliente borrado con éxito")
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                self.tr("Error al borrar subtipo cliente"),
                str(e)
            )
