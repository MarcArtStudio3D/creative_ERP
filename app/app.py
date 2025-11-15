"""
Aplicación principal del Creative ERP.
Gestiona el inicio, login y navegación entre módulos.
"""

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings
import sys

from core.db import init_db
from core.auth import AuthenticationManager
from core.modules import ModuleManager


class CreativeERPApp:
    """
    Aplicación principal del ERP.
    Gestiona el ciclo de vida completo de la aplicación.
    """
    
    def __init__(self):
        self.qapp = None
        self.auth_manager = AuthenticationManager()
        self.module_manager = ModuleManager()
        self.main_window = None
        self.login_window = None
    
    def initialize(self):
        """Inicializa la aplicación."""
        # Crear aplicación Qt
        self.qapp = QApplication(sys.argv)
        self.qapp.setApplicationName("Creative ERP")
        self.qapp.setOrganizationName("ArtStudio3D")
        self.qapp.setOrganizationDomain("artstudio3d.com")
        
        # Configurar estilo
        self.qapp.setStyle("Fusion")
        
        # Inicializar base de datos
        print("Inicializando base de datos...")
        init_db()
        print("✓ Base de datos lista")
        
        return True
    
    def show_login(self):
        """Muestra la ventana de login."""
        from app.views.login_window import LoginWindow
        
        self.login_window = LoginWindow(self.auth_manager)
        self.login_window.login_successful.connect(self.on_login_success)
        self.login_window.show()
    
    def on_login_success(self):
        """Callback cuando el login es exitoso."""
        self.login_window.close()
        self.show_main_window()
    
    def show_main_window(self):
        """Muestra la ventana principal con los módulos del usuario."""
        from app.views.main_window import MainWindow
        
        session = self.auth_manager.get_current_session()
        if not session:
            self.show_login()
            return
        
        # Obtener módulos disponibles para el usuario
        user_permissions = session.user.get_effective_permissions()
        available_modules = self.module_manager.get_available_modules(user_permissions)
        
        print(f"\n✓ Usuario: {session.user.full_name}")
        print(f"✓ Rol: {session.user.role.value}")
        print(f"✓ Módulos disponibles: {len(available_modules)}")
        
        self.main_window = MainWindow(session, available_modules, self.module_manager)
        self.main_window.show()
    
    def run(self):
        """Ejecuta la aplicación."""
        if not self.initialize():
            return 1
        
        # Mostrar login al inicio
        self.show_login()
        
        # Ejecutar loop de eventos Qt
        return self.qapp.exec()


def run_app():
    """Punto de entrada de la aplicación."""
    app = CreativeERPApp()
    sys.exit(app.run())