from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QLineEdit, QHBoxLayout
from core.ui_helpers import show_warning, show_info, show_critical
from PySide6.QtCore import Qt

from core.company_manager import company_manager
from core.db import set_database_for_company


class AdminInitCompanyDBDialog(QDialog):
    """Dialogo simple para permitir a un admin inicializar el esquema de una empresa.

    - Lista empresas disponibles desde la BD principal
    - Botón de validación para probar conexión
    - Requiere confirmación escribiendo 'CONFIRM_INIT' para proceder
    """

    def __init__(self, parent=None, current_session=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Inicializar BD de Empresa (Administración)"))
        self.session = current_session

        self.layout = QVBoxLayout()

        self.info = QLabel(self.tr("Seleccione una empresa y confirme para crear/inicializar su esquema de base de datos."))
        self.info.setWordWrap(True)
        self.layout.addWidget(self.info)

        self.combo = QComboBox()
        self._populate_companies()
        self.layout.addWidget(self.combo)

        btn_layout = QHBoxLayout()
        self.validate_btn = QPushButton(self.tr("Validar conexión"))
        self.validate_btn.clicked.connect(self._on_validate)
        btn_layout.addWidget(self.validate_btn)

        self.init_btn = QPushButton(self.tr("Inicializar BD (requiere confirmación)"))
        self.init_btn.clicked.connect(self._on_init)
        btn_layout.addWidget(self.init_btn)

        self.layout.addLayout(btn_layout)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText(self.tr("Escriba CONFIRM_INIT para confirmar"))
        self.layout.addWidget(self.confirm_input)

        self.setLayout(self.layout)

    def _populate_companies(self):
        try:
            companies = company_manager.get_available_companies()
            self.combo.clear()
            for c in companies:
                self.combo.addItem(f"{c['id']} — {c['codigo']} - {c['nombre']}", c['id'])
        except Exception as e:
            show_critical(self, self.tr("Error"), str(e))

    def _on_validate(self):
        cid = self.combo.currentData()
        if not cid:
            show_warning(self, self.tr("Seleccione"), self.tr("Seleccione una empresa"))
            return
        result = company_manager.validate_company_database(cid)
        if result.get('valid'):
            show_info(self, self.tr("OK"), self.tr("Conexión a la BD de la empresa válida"))
        else:
            show_warning(self, self.tr("Falló"), result.get('message') or self.tr('Error de conexión'))

    def _on_init(self):
        cid = self.combo.currentData()
        if not cid:
            show_warning(self, self.tr("Seleccione"), self.tr("Seleccione una empresa"))
            return

        if self.confirm_input.text().strip() != 'CONFIRM_INIT':
            show_warning(self, self.tr("Confirmación"), self.tr("Debe escribir CONFIRM_INIT para confirmar la acción"))
            return

        # Who initiated this? Prefer session username if provided
        initiator = None
        try:
            if self.session and getattr(self.session, 'user', None):
                initiator = getattr(self.session.user, 'username', None)
        except Exception:
            initiator = None

        try:
            # Switch to company DB and initialize (explicit)
            set_database_for_company(cid, init=True, initiator=initiator)
            show_info(self, self.tr("Hecho"), self.tr("Inicialización completada. Revise logs para detalles."))
            self.close()
        except Exception as e:
            show_critical(self, self.tr("Error"), str(e))
