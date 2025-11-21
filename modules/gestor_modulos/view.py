"""
Vista del gestor de módulos.

Interfaz gráfica para gestionar permisos de módulos por rol.
"""

from typing import Dict
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget,
    QListWidgetItem, QComboBox, QMessageBox, QCheckBox, QGridLayout
)
from core.modules import AVAILABLE_MODULES
from core.auth import UserRole
from .model import RolePermissionsManager


class GestorModulosView(QWidget):
    """
    Interfaz gráfica para gestionar permisos de módulos por rol.
    
    Permite:
    - Seleccionar uno o múltiples módulos (Ctrl+Click, Shift+Click)
    - Asignar permisos por rol
    - Seleccionar/deseleccionar todos los permisos rápidamente
    - Guardar cambios en role_permissions.json
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Modelo de negocio
        self.manager = RolePermissionsManager()
        
        # Construir interfaz
        self._build_ui()

    def _build_ui(self):
        """Construye la interfaz gráfica."""
        layout = QVBoxLayout(self)
        
        # Encabezado
        header = QLabel('Gestor de Módulos y Permisos por Rol')
        header.setStyleSheet('font-weight: bold; font-size: 16pt;')
        layout.addWidget(header)

        # Lista de módulos con selección múltiple
        self.list_modules = QListWidget()
        self.list_modules.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        
        for mid, m in AVAILABLE_MODULES.items():
            item = QListWidgetItem(f"{m.icon} {m.name} ({mid})")
            item.setData(1, mid)
            self.list_modules.addItem(item)
        
        layout.addWidget(self.list_modules)
        
        # Etiqueta de contador de selección
        self.selection_label = QLabel('Ningún módulo seleccionado')
        self.selection_label.setStyleSheet('color: gray; font-style: italic;')
        layout.addWidget(self.selection_label)
        
        # Controles: Rol + Permisos + Botones
        controls = QHBoxLayout()
        
        # Selector de rol
        controls.addWidget(QLabel('Rol:'))
        self.cbo_role = QComboBox()
        for r in UserRole:
            self.cbo_role.addItem(r.value)
        controls.addWidget(self.cbo_role)

        # Permisos como checkboxes en cuadrícula
        perms_widget = QWidget()
        perms_layout = QGridLayout()
        perms_widget.setLayout(perms_layout)

        self.perm_checks: Dict[str, QCheckBox] = {}
        perm_names = ['READ', 'CREATE', 'UPDATE', 'DELETE', 'ADMIN', 'EXPORT', 'IMPORT', 'PRINT']
        
        for idx, pname in enumerate(perm_names):
            cb = QCheckBox(pname.capitalize())
            self.perm_checks[pname] = cb
            perms_layout.addWidget(cb, idx // 4, idx % 4)

        controls.addWidget(perms_widget)

        # Botones de selección rápida
        btn_select_all = QPushButton('✓ Todos')
        btn_select_all.setToolTip('Seleccionar todos los permisos')
        btn_select_all.clicked.connect(self._select_all_permissions)
        controls.addWidget(btn_select_all)

        btn_deselect_all = QPushButton('✗ Ninguno')
        btn_deselect_all.setToolTip('Deseleccionar todos los permisos')
        btn_deselect_all.clicked.connect(self._deselect_all_permissions)
        controls.addWidget(btn_deselect_all)

        # Botón asignar
        btn_set = QPushButton('Asignar')
        btn_set.clicked.connect(self._assign_permissions)
        controls.addWidget(btn_set)

        layout.addLayout(controls)

        # Botón guardar cambios
        btn_save = QPushButton('Guardar cambios')
        btn_save.clicked.connect(self._save_changes)
        layout.addWidget(btn_save)

        # Conectar eventos
        self.list_modules.itemSelectionChanged.connect(self._on_selection_changed)
        self.cbo_role.currentIndexChanged.connect(lambda: self._on_selection_changed())

        # Inicializar vista
        self._on_selection_changed()

    def _on_selection_changed(self):
        """Maneja cambios en la selección de módulos o rol."""
        selected_items = self.list_modules.selectedItems()
        role = self.cbo_role.currentText()
        
        # Actualizar etiqueta de selección
        if not selected_items:
            self.selection_label.setText('Ningún módulo seleccionado')
        elif len(selected_items) == 1:
            self.selection_label.setText(f'1 módulo seleccionado: {selected_items[0].data(1)}')
        else:
            self.selection_label.setText(f'{len(selected_items)} módulos seleccionados')
        
        # Resetear checkboxes
        for cb in self.perm_checks.values():
            cb.setChecked(False)

        if not selected_items or not role:
            return
        
        # Cargar permisos
        if len(selected_items) == 1:
            # Un solo módulo: mostrar sus permisos
            module_id = selected_items[0].data(1)
            perms = self.manager.get_module_permissions(role, module_id)
            self._set_checkboxes(perms)
        else:
            # Múltiples módulos: mostrar permisos comunes
            module_ids = [item.data(1) for item in selected_items]
            common_perms = self.manager.get_common_permissions(role, module_ids)
            self._set_checkboxes(list(common_perms))

    def _set_checkboxes(self, perms: list):
        """Marca los checkboxes según la lista de permisos."""
        for perm in perms:
            if not isinstance(perm, str):
                continue
            key = perm.strip().upper()
            cb = self.perm_checks.get(key)
            if cb:
                cb.setChecked(True)

    def _get_selected_permissions(self) -> list:
        """Obtiene los permisos seleccionados en los checkboxes."""
        selected = []
        for key, cb in self.perm_checks.items():
            if cb.isChecked():
                selected.append(key)
        return selected

    def _select_all_permissions(self):
        """Marca todos los checkboxes de permisos."""
        for cb in self.perm_checks.values():
            cb.setChecked(True)

    def _deselect_all_permissions(self):
        """Desmarca todos los checkboxes de permisos."""
        for cb in self.perm_checks.values():
            cb.setChecked(False)

    def _assign_permissions(self):
        """Asigna los permisos seleccionados a los módulos seleccionados."""
        selected_items = self.list_modules.selectedItems()
        
        if not selected_items:
            QMessageBox.information(
                self, 
                'Selecciona', 
                'Selecciona al menos un módulo primero'
            )
            return
        
        role = self.cbo_role.currentText()
        perms = self._get_selected_permissions()
        
        # Aplicar permisos a todos los módulos seleccionados
        module_ids = [item.data(1) for item in selected_items]
        count = self.manager.set_multiple_modules_permissions(role, module_ids, perms)
        
        # Mensaje informativo
        if count == 1:
            QMessageBox.information(
                self, 
                'Asignado', 
                f'Asignados {perms} a {role} en {module_ids[0]}'
            )
        else:
            modules_preview = ', '.join(module_ids[:5])
            if len(module_ids) > 5:
                modules_preview += '...'
            
            QMessageBox.information(
                self, 
                'Asignado', 
                f'Asignados {perms} a {role} en {count} módulos:\n{modules_preview}'
            )

    def _save_changes(self):
        """Guarda los cambios en el archivo JSON."""
        if self.manager.save():
            QMessageBox.information(self, 'Guardado', 'Permisos guardados correctamente.')
        else:
            QMessageBox.warning(self, 'Error', 'No se pudo guardar los permisos.')
