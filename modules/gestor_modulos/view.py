from typing import Dict, List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget,
    QListWidgetItem, QDialog, QComboBox, QMessageBox
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

        hl = QHBoxLayout()
        hl.addWidget(QLabel('Rol:'))
        self.cbo_role = QComboBox()
        for r in UserRole:
            self.cbo_role.addItem(r.value)
        hl.addWidget(self.cbo_role)

        self.cbo_perm = QComboBox()
        self.cbo_perm.addItems(['none', 'read', 'create', 'update', 'delete', 'admin', 'export', 'import', 'print'])
        hl.addWidget(QLabel('Permiso:'))
        hl.addWidget(self.cbo_perm)

        btn_set = QPushButton('Asignar')
        btn_set.clicked.connect(self.asignar_permiso)
        hl.addWidget(btn_set)

        layout.addLayout(hl)

        btn_save = QPushButton('Guardar cambios')
        btn_save.clicked.connect(self._save_overrides)
        layout.addWidget(btn_save)

    def asignar_permiso(self):
        item = self.list_modules.currentItem()
        if not item:
            QMessageBox.information(self, 'Selecciona', 'Selecciona un módulo primero')
            return
        mid = item.data(1)
        role = self.cbo_role.currentText()
        perm = self.cbo_perm.currentText()

        # Escribe en overrides
        if role not in self.overrides:
            self.overrides[role] = {}
        # Simplificar: guardar una lista con permisos por módulo
        self.overrides[role][mid] = [perm]
        QMessageBox.information(self, 'Asignado', f'Asignado {perm} a {role} en {mid}')
