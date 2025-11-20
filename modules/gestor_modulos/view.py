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

    def _save_overrides(self):
        try:
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
        for mid, m in AVAILABLE_MODULES.items():
            item = QListWidgetItem(f"{m.icon} {m.name} ({mid})")
            item.setData(1, mid)
            self.list_modules.addItem(item)
        layout.addWidget(self.list_modules)
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

        btn_set = QPushButton('Asignar')
        btn_set.clicked.connect(self.asignar_permisos)
        controls.addWidget(btn_set)

        layout.addLayout(controls)

        btn_save = QPushButton('Guardar cambios')
        btn_save.clicked.connect(self._save_overrides)
        layout.addWidget(btn_save)

        # Cuando se cambia el módulo o rol, cargar los checks actuales
        self.list_modules.currentItemChanged.connect(lambda cur, prev: self._load_checks_from_overrides())
        self.cbo_role.currentIndexChanged.connect(lambda idx: self._load_checks_from_overrides())

        # Inicializar checks
        self._load_checks_from_overrides()

    def _load_checks_from_overrides(self):
        item = self.list_modules.currentItem()
        role = self.cbo_role.currentText()
        # Reset
        for cb in self.perm_checks.values():
            cb.setChecked(False)

        if not item or not role:
            return
        mid = item.data(1)
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
        item = self.list_modules.currentItem()
        if not item:
            QMessageBox.information(self, 'Selecciona', 'Selecciona un módulo primero')
            return
        mid = item.data(1)
        role = self.cbo_role.currentText()

        selected = []
        for key, cb in self.perm_checks.items():
            if cb.isChecked():
                selected.append(key)

        if role not in self.overrides:
            self.overrides[role] = {}
        # Guardar la lista de permisos como strings
        self.overrides[role][mid] = selected
        QMessageBox.information(self, 'Asignado', f'Asignados {selected} a {role} en {mid}')
