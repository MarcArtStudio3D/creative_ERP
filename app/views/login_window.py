"""
Ventana de login del sistema.
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QMessageBox, QFrame)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QIcon

from core.auth import AuthenticationManager, User, UserRole
from core.repositories import BaseRepository


class LoginWindow(QDialog):
    """
    Ventana de inicio de sesión.
    Permite autenticar usuarios en el sistema.
    """
    
    # Señal emitida cuando el login es exitoso
    login_successful = Signal()
    
    def __init__(self, auth_manager: AuthenticationManager):
        super().__init__()
        self.auth_manager = auth_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        self.setWindowTitle("Creative ERP - Login")
        self.setFixedSize(450, 380)
        self.setModal(True)
        
        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 30, 40, 30)
        
        # Título
        title = QLabel("Creative ERP")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("Gestión para creativos")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        subtitle.setFont(subtitle_font)
        layout.addWidget(subtitle)
        
        # Espaciador
        layout.addSpacing(10)
        
        # Campo de usuario
        user_label = QLabel("Usuario:")
        user_label_font = QFont()
        user_label_font.setBold(True)
        user_label.setFont(user_label_font)
        layout.addWidget(user_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingresa tu nombre de usuario")
        self.username_input.setMinimumHeight(40)
        input_font = QFont()
        input_font.setPointSize(11)
        self.username_input.setFont(input_font)
        self.username_input.returnPressed.connect(self.on_login_clicked)
        layout.addWidget(self.username_input)
        
        # Espaciador entre campos
        layout.addSpacing(5)
        
        # Campo de contraseña
        password_label = QLabel("Contraseña:")
        password_label_font = QFont()
        password_label_font.setBold(True)
        password_label.setFont(password_label_font)
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingresa tu contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.setFont(input_font)
        self.password_input.returnPressed.connect(self.on_login_clicked)
        layout.addWidget(self.password_input)
        
        # Espaciador
        layout.addSpacing(15)
        
        # Botones
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.setDefault(True)
        self.login_button.clicked.connect(self.on_login_clicked)
        self.login_button.setMinimumHeight(40)
        button_font = QFont()
        button_font.setBold(True)
        button_font.setPointSize(11)
        self.login_button.setFont(button_font)
        button_layout.addWidget(self.login_button, 2)
        
        # Botón de usuario de prueba (solo desarrollo)
        demo_button = QPushButton("Demo")
        demo_button.clicked.connect(self.on_demo_clicked)
        demo_button.setMinimumHeight(40)
        demo_button.setFont(button_font)
        button_layout.addWidget(demo_button, 1)
        
        layout.addLayout(button_layout)
        
        # Info de usuarios demo
        info = QLabel("💡 Demo: admin/admin, manager/manager, user/user")
        info_font = QFont()
        info_font.setPointSize(9)
        info.setFont(info_font)
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        
        self.setLayout(layout)
        
        # Focus en el campo de usuario
        self.username_input.setFocus()
    
    def on_login_clicked(self):
        """Maneja el click en el botón de login."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor ingresa usuario y contraseña")
            return
        
        # Intentar login (aquí usamos usuarios de prueba)
        # En producción esto consultaría la base de datos
        if self.try_login(username, password):
            self.login_successful.emit()
        else:
            QMessageBox.warning(
                self, 
                "Error de autenticación", 
                "Usuario o contraseña incorrectos"
            )
            self.password_input.clear()
            self.password_input.setFocus()
    
    def on_demo_clicked(self):
        """Login automático con usuario demo."""
        self.username_input.setText("admin")
        self.password_input.setText("admin")
        self.on_login_clicked()
    
    def try_login(self, username: str, password: str) -> bool:
        """
        Intenta autenticar al usuario.
        
        NOTA: Esta es una implementación temporal con usuarios hardcoded.
        En producción, esto consultaría la base de datos.
        """
        # Usuarios de prueba
        demo_users = self.create_demo_users()
        
        for user in demo_users:
            if user.username == username and user.verify_password(password):
                # Crear sesión
                from core.auth import Session
                from datetime import datetime
                import secrets
                
                session = Session(
                    user=user,
                    login_time=datetime.now(),
                    token=secrets.token_urlsafe(32)
                )
                
                # Guardar en el auth manager
                self.auth_manager._current_session = session
                return True
        
        return False
    
    def create_demo_users(self):
        """
        Crea usuarios de demostración.
        
        TODO: Mover esto a una migración de base de datos o script de setup.
        """
        from core.auth import User, UserRole
        from datetime import datetime
        
        return [
            # Admin - acceso total
            User(
                id=1,
                username="admin",
                email="admin@artstudio3d.com",
                full_name="Administrador",
                password_hash=User.hash_password("admin"),
                role=UserRole.ADMIN,
                is_active=True,
                created_at=datetime.now()
            ),
            
            # Manager - gestión general
            User(
                id=2,
                username="manager",
                email="manager@artstudio3d.com",
                full_name="Gestor Principal",
                password_hash=User.hash_password("manager"),
                role=UserRole.MANAGER,
                is_active=True,
                created_at=datetime.now()
            ),
            
            # Usuario normal
            User(
                id=3,
                username="user",
                email="user@artstudio3d.com",
                full_name="Usuario Normal",
                password_hash=User.hash_password("user"),
                role=UserRole.EMPLOYEE,
                is_active=True,
                created_at=datetime.now()
            ),
            
            # Contable
            User(
                id=4,
                username="contable",
                email="contable@artstudio3d.com",
                full_name="Departamento Contable",
                password_hash=User.hash_password("contable"),
                role=UserRole.ACCOUNTANT,
                is_active=True,
                created_at=datetime.now()
            ),
            
            # Ventas
            User(
                id=5,
                username="ventas",
                email="ventas@artstudio3d.com",
                full_name="Departamento Ventas",
                password_hash=User.hash_password("ventas"),
                role=UserRole.SALES,
                is_active=True,
                created_at=datetime.now()
            ),
        ]
