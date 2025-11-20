from typing import Dict, List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget,
    QListWidgetItem, QDialog, QComboBox, QMessageBox, QCheckBox, QGridLayout, QWidgetItem
)
from core.modules import AVAILABLE_MODULES
from core.auth import UserRole
import json, os


class GestorModulosView(QWidget):
    """Interfaz simple para listar módulos y asignar permisos por rol.

    Nota: Es una implementación mínima para administrar `role_permissions.json`.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._load_overrides()
        self._build_ui()

    def _load_overrides(self):
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.path = os.path.join(base, 'role_permissions.json')
        try:
            if os.path.exists(self.path):
                with open(self.path, 'r', encoding='utf-8') as f:
                    self.overrides = json.load(f)
            else:
                self.overrides = {}
        except Exception:
            self.overrides = {}
        # Normalizar al cargar
        self._normalize_overrides()

    def _normalize_overrides(self):
        """Ensure overrides use canonical uppercase permission names and lists."""
        valid = {'READ', 'CREATE', 'UPDATE', 'DELETE', 'ADMIN', 'EXPORT', 'IMPORT', 'PRINT'}
        changed = False
        try:
            new = {}
            for role, modules in (self.overrides or {}).items():
                if not isinstance(modules, dict):
                    continue
                new_modules = {}
                for mid, perms in modules.items():
                    if not isinstance(perms, list):
                        continue
                    cleaned = []
                    for p in perms:
                        if not isinstance(p, str):
                            continue
                        key = p.strip().upper()
                        if key == 'NONE' or key == '':
                            continue
                        if key in valid:
                            cleaned.append(key)
                    if cleaned:
                        new_modules[mid] = sorted(list(set(cleaned)))
                if new_modules:
                    new[role] = new_modules
            if new != (self.overrides or {}):
                self.overrides = new
                changed = True
        except Exception:
            return
        # If normalization changed content, persist it
        if changed:
            try:
                with open(self.path, 'w', encoding='utf-8') as f:
                    json.dump(self.overrides, f, indent=2, ensure_ascii=False)
            except Exception:
                pass

    def _save_overrides(self):
        try:
            # Normalizar antes de guardar
            self._normalize_overrides()
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.overrides, f, indent=2, ensure_ascii=False)
            QMessageBox.information(self, 'Guardado', 'Permisos guardados.')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'No se pudo guardar: {e}')

    def _build_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel('Gestor de Módulos y Permisos por Rol')
        header.setStyleSheet('font-weight: bold; font-size: 16pt;')
        layout.addWidget(header)

        self.list_modules = QListWidget()
        # Habilitar selección múltiple con Ctrl+Click y Shift+Click
        self.list_modules.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        for mid, m in AVAILABLE_MODULES.items():
            item = QListWidgetItem(f"{m.icon} {m.name} ({mid})")
            item.setData(1, mid)
            self.list_modules.addItem(item)
        layout.addWidget(self.list_modules)
        
        # Etiqueta para mostrar cuántos módulos están seleccionados
        self.selection_label = QLabel('Ningún módulo seleccionado')
        self.selection_label.setStyleSheet('color: gray; font-style: italic;')
        layout.addWidget(self.selection_label)
        
        # Controles para seleccionar rol y permisos (checkboxes)
        controls = QHBoxLayout()
        controls.addWidget(QLabel('Rol:'))
        self.cbo_role = QComboBox()
        for r in UserRole:
            self.cbo_role.addItem(r.value)
        controls.addWidget(self.cbo_role)

        # Permisos como checkboxes en una cuadrícula
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

        # Botones para seleccionar/deseleccionar todos los permisos
        btn_select_all = QPushButton('✓ Todos')
        btn_select_all.setToolTip('Seleccionar todos los permisos')
        btn_select_all.clicked.connect(self.seleccionar_todos_permisos)
        controls.addWidget(btn_select_all)

        btn_deselect_all = QPushButton('✗ Ninguno')
        btn_deselect_all.setToolTip('Deseleccionar todos los permisos')
        btn_deselect_all.clicked.connect(self.deseleccionar_todos_permisos)
        controls.addWidget(btn_deselect_all)

        btn_set = QPushButton('Asignar')
        btn_set.clicked.connect(self.asignar_permisos)
        controls.addWidget(btn_set)

        layout.addLayout(controls)

        btn_save = QPushButton('Guardar cambios')
        btn_save.clicked.connect(self._save_overrides)
        layout.addWidget(btn_save)

        # Cuando se cambia la selección de módulos o rol, cargar los checks actuales
        self.list_modules.itemSelectionChanged.connect(self._load_checks_from_overrides)
        self.cbo_role.currentIndexChanged.connect(lambda idx: self._load_checks_from_overrides())

        # Inicializar checks
        self._load_checks_from_overrides()

    def _load_checks_from_overrides(self):
        selected_items = self.list_modules.selectedItems()
        role = self.cbo_role.currentText()
        
        # Actualizar etiqueta de selección
        if not selected_items:
            self.selection_label.setText('Ningún módulo seleccionado')
        elif len(selected_items) == 1:
            self.selection_label.setText(f'1 módulo seleccionado: {selected_items[0].data(1)}')
        else:
            self.selection_label.setText(f'{len(selected_items)} módulos seleccionados')
        
        # Reset todos los checkboxes
        for cb in self.perm_checks.values():
            cb.setChecked(False)

        if not selected_items or not role:
            return
        
        # Si hay múltiples módulos seleccionados, mostrar solo permisos comunes
        if len(selected_items) > 1:
            # Obtener permisos del primer módulo
            first_mid = selected_items[0].data(1)
            role_map = self.overrides.get(role, {})
            common_perms = set(role_map.get(first_mid, []))
            
            # Intersección con permisos de los demás módulos
            for item in selected_items[1:]:
                mid = item.data(1)
                perms = set(role_map.get(mid, []))
                common_perms &= perms
            
            # Marcar solo los permisos comunes
            for p in common_perms:
                if not isinstance(p, str):
                    continue
                key = p.strip().upper()
                cb = self.perm_checks.get(key)
                if cb:
                    cb.setChecked(True)
        else:
            # Un solo módulo seleccionado
            mid = selected_items[0].data(1)
            role_map = self.overrides.get(role, {})
            perms = role_map.get(mid, [])
            for p in perms:
                if not isinstance(p, str):
                    continue
                key = p.strip().upper()
                cb = self.perm_checks.get(key)
                if cb:
                    cb.setChecked(True)

    def asignar_permisos(self):
        selected_items = self.list_modules.selectedItems()
        if not selected_items:
            QMessageBox.information(self, 'Selecciona', 'Selecciona al menos un módulo primero')
            return
        
        role = self.cbo_role.currentText()

        # Obtener permisos seleccionados
        selected = []
        for key, cb in self.perm_checks.items():
            if cb.isChecked():
                selected.append(key)

        if role not in self.overrides:
            self.overrides[role] = {}
        
        # Aplicar permisos a todos los módulos seleccionados
        module_names = []
        for item in selected_items:
            mid = item.data(1)
            self.overrides[role][mid] = selected
            module_names.append(mid)
        
        # Mensaje informativo
        if len(module_names) == 1:
            QMessageBox.information(self, 'Asignado', 
                f'Asignados {selected} a {role} en {module_names[0]}')
        else:
            QMessageBox.information(self, 'Asignado', 
                f'Asignados {selected} a {role} en {len(module_names)} módulos:\n' + 
                ', '.join(module_names[:5]) + ('...' if len(module_names) > 5 else ''))

    def seleccionar_todos_permisos(self):
        """Marca todos los checkboxes de permisos."""
        for cb in self.perm_checks.values():
            cb.setChecked(True)

    def deseleccionar_todos_permisos(self):
        """Desmarca todos los checkboxes de permisos."""
        for cb in self.perm_checks.values():
            cb.setChecked(False)
