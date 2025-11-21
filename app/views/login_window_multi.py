"""
Ventana de login multi-empresa.
Basada en el diseño de RedFox SGC.
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QFrame, QComboBox)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QPixmap

from core.repositories import UserRepository, BusinessGroupRepository, CompanyRepository
from core.auth import AuthenticationManager, User, UserRole
from core.business import BusinessGroup, Company, CompanyContext


class LoginWindowMultiCompany(QDialog):
    """
    Ventana de login multi-empresa.
    
    Permite seleccionar:
    - Usuario
    - Grupo empresarial
    - Empresa
    """
    
    login_successful = Signal(object)  # Emite el CompanyContext
    
    def __init__(self, auth_manager: AuthenticationManager):
        super().__init__()
        self.auth_manager = auth_manager
        self.setup_ui()
        self.load_demo_data()
    
    def setup_ui(self):
        """Configura la interfaz tipo RedFox SGC."""
        self.setWindowTitle("Creative ERP - Acceso Usuarios")
        self.setFixedSize(700, 520)
        self.setModal(True)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # ========== PANEL IZQUIERDO (Botones laterales) ==========
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel)
        
        # ========== PANEL CENTRAL (Logo + Formulario) ==========
        center_layout = QVBoxLayout()
        center_layout.setSpacing(15)
        center_layout.setContentsMargins(30, 30, 30, 30)
        
        # Logo grande (tipo NEUX Software)
        logo_container = QFrame()
        logo_container.setFrameShape(QFrame.Shape.StyledPanel)
        logo_container.setMaximumHeight(90)
        logo_layout = QVBoxLayout()
        logo_layout.setContentsMargins(0, 10, 0, 10)
        logo_layout.setSpacing(2)
        
        logo_label = QLabel("CREATIVE ERP")
        logo_font = QFont()
        logo_font.setPointSize(24)
        logo_font.setBold(True)
        logo_label.setFont(logo_font)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_label)
        
        subtitle = QLabel("Sistema de Gestión Empresarial")
        subtitle_font = QFont()
        subtitle_font.setPointSize(9)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(subtitle)
        
        logo_container.setLayout(logo_layout)
        center_layout.addWidget(logo_container)
        
        # Formulario de login
        form_container = QFrame()
        form_layout = QVBoxLayout()
        form_layout.setSpacing(3)
        form_layout.setContentsMargins(0, 0, 0, 0)
        
        # Usuario
        user_label = QLabel("Usuario:")
        user_font = QFont()
        user_font.setBold(True)
        user_font.setPointSize(9)
        user_label.setFont(user_font)
        user_label.setMaximumHeight(18)
        form_layout.addWidget(user_label)
        
        self.user_combo = QComboBox()
        self.user_combo.setMinimumHeight(32)
        self.user_combo.setMaximumHeight(32)
        form_layout.addWidget(self.user_combo)
        form_layout.addSpacing(8)
        
        # Contraseña
        password_label = QLabel("Contraseña:")
        password_label.setFont(user_font)
        password_label.setMaximumHeight(18)
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(32)
        self.password_input.setMaximumHeight(32)
        self.password_input.returnPressed.connect(self.on_login_clicked)
        form_layout.addWidget(self.password_input)
        form_layout.addSpacing(8)
        
        # Grupo
        group_label = QLabel("Grupo:")
        group_label.setFont(user_font)
        group_label.setMaximumHeight(18)
        form_layout.addWidget(group_label)
        
        self.group_combo = QComboBox()
        self.group_combo.setMinimumHeight(32)
        self.group_combo.setMaximumHeight(32)
        self.group_combo.currentIndexChanged.connect(self.on_group_changed)
        form_layout.addWidget(self.group_combo)
        form_layout.addSpacing(8)
        
        # Empresa
        company_label = QLabel("Empresa:")
        company_label.setFont(user_font)
        company_label.setMaximumHeight(18)
        form_layout.addWidget(company_label)
        
        self.company_combo = QComboBox()
        self.company_combo.setMinimumHeight(32)
        self.company_combo.setMaximumHeight(32)
        form_layout.addWidget(self.company_combo)
        
        form_container.setLayout(form_layout)
        
        center_layout.addWidget(form_container)
        
        # Espaciado antes de los botones
        center_layout.addSpacing(40)
        
        center_layout.addStretch()
        
        # Botones inferiores
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.access_button = QPushButton("Acceder")
        self.access_button.setMinimumHeight(40)
        access_font = QFont()
        access_font.setBold(True)
        access_font.setPointSize(11)
        self.access_button.setFont(access_font)
        self.access_button.clicked.connect(self.on_login_clicked)
        button_layout.addWidget(self.access_button)
        
        self.close_button = QPushButton("Cerrar")
        self.close_button.setMinimumHeight(40)
        self.close_button.setFont(access_font)
        self.close_button.clicked.connect(self.reject)
        button_layout.addWidget(self.close_button)
        
        center_layout.addLayout(button_layout)
        
        main_layout.addLayout(center_layout, 3)
        
        # ========== PANEL DERECHO (Imagen corporativa) ==========
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 2)
        
        self.setLayout(main_layout)
    
    def create_left_panel(self) -> QFrame:
        """Crea el panel izquierdo con botones laterales."""
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.StyledPanel)
        panel.setMaximumWidth(150)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 20, 10, 20)
        
        # Botón Configuración
        config_btn = QPushButton("⚙️\nConfiguración")
        config_btn.setMinimumHeight(80)
        config_btn.clicked.connect(self.open_config)
        layout.addWidget(config_btn)
        
        # Botón Empresas
        companies_btn = QPushButton("🏢\nEmpresas")
        companies_btn.setMinimumHeight(80)
        companies_btn.clicked.connect(self.manage_companies)
        layout.addWidget(companies_btn)
        
        layout.addStretch()
        
        panel.setLayout(layout)
        return panel
    
    def create_right_panel(self) -> QFrame:
        """Crea el panel derecho con imagen corporativa."""
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.StyledPanel)
        panel.setMinimumWidth(200)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Aquí iría el logo/imagen corporativa
        # Por ahora solo texto
        image_label = QLabel("🎨\n\nArtStudio3D\n\nCreative Solutions")
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setWordWrap(True)
        layout.addWidget(image_label)
        
        panel.setLayout(layout)
        return panel
    
    def load_demo_data(self):
        """Carga datos de usuarios, grupos y empresas desde la base de datos."""
        # Cargar usuarios
        users = UserRepository.get_all_users()
        for user in users:
            self.user_combo.addItem(user.username, user)  # type: ignore
        
        # Cargar grupos empresariales
        groups = BusinessGroupRepository.get_all_groups()
        for group in groups:
            self.group_combo.addItem(group.name, group)  # type: ignore
        
        # Las empresas se cargarán al seleccionar grupo
        if groups:
            self.on_group_changed(0)
    
    def on_group_changed(self, index: int):
        """Cuando cambia el grupo, cargar las empresas de ese grupo."""
        self.company_combo.clear()
        
        group = self.group_combo.currentData()
        if not group:
            return
        
        # Cargar empresas desde la base de datos
        companies = CompanyRepository.get_companies_by_group(group.id)
        for company in companies:
            self.company_combo.addItem(company.name, company)  # type: ignore
    
    def on_login_clicked(self):
        """Maneja el click en Acceder."""
        username = self.user_combo.currentText()
        password = self.password_input.text()
        
        if not username or not password:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", "Ingresa usuario y contraseña")
            return
        
        group = self.group_combo.currentData()
        company = self.company_combo.currentData()
        
        if not group or not company:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", "Selecciona grupo y empresa")
            return
        
        # Intentar login
        if self.try_login(username, password):
            # Crear contexto de empresa
            context = CompanyContext(group=group, company=company)
            
            # Guardar en la sesión
            self.auth_manager._current_session.company_context = context  # type: ignore
            
            self.login_successful.emit(context)
        else:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")
            self.password_input.clear()
    
    def try_login(self, username: str, password: str) -> bool:
        """Intenta autenticar (usa los usuarios demo)."""
        demo_users = self.create_demo_users()
        
        for user in demo_users:
            if user.username == username and user.verify_password(password):
                from core.auth import Session
                from datetime import datetime
                import secrets
                
                session = Session(
                    user=user,
                    login_time=datetime.now(),
                    token=secrets.token_urlsafe(32)
                )
                
                self.auth_manager._current_session = session
                return True
        
        return False
    
    def create_demo_users(self):
        """Crea usuarios de demostración."""
        from core.auth import User, UserRole
        from datetime import datetime
        
        return [
            User(
                id=1,
                username="admin",
                email="admin@artstudio3d.com",
                full_name="Administrador",
                password_hash=User.hash_password("admin"),
                role=UserRole.ADMIN,
                is_active=True,
                created_at=datetime.now(),
                allowed_groups=[1, 2],
                allowed_companies=[1, 2, 3]
            ),
            User(
                id=2,
                username="manager",
                email="manager@artstudio3d.com",
                full_name="Gestor Principal",
                password_hash=User.hash_password("manager"),
                role=UserRole.MANAGER,
                is_active=True,
                created_at=datetime.now(),
                allowed_groups=[1],
                allowed_companies=[1, 2]
            ),
            User(
                id=3,
                username="user",
                email="user@artstudio3d.com",
                full_name="Usuario Normal",
                password_hash=User.hash_password("user"),
                role=UserRole.EMPLOYEE,
                is_active=True,
                created_at=datetime.now(),
                allowed_groups=[1],
                allowed_companies=[1]
            ),
        ]
    
    def open_config(self):
        """Abre la configuración."""
        from app.views.config_dialog import ConfigDialog
        
        dialog = ConfigDialog(self)
        
        # Conectar señal de cambio de idioma
        dialog.language_changed.connect(self.on_language_changed)
        
        dialog.exec()
    
    def on_language_changed(self, language_code: str):
        """Maneja el cambio de idioma."""
        from core.translations import change_language
        from PySide6.QtWidgets import QApplication
        
        app = QApplication.instance()
        if app:
            # Cambiar el idioma (necesitaremos guardar el translator en algún lugar)
            # Por ahora solo guardamos la preferencia, el cambio real se hará al reiniciar
            print(f"Idioma cambiado a: {language_code}")
            print("La aplicación debe reiniciarse para aplicar todos los cambios")
    
    def manage_companies(self):
        """Gestiona empresas."""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Empresas", "Gestión de empresas (próximamente)")
