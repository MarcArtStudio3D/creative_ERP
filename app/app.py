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
        self.translator = None  # Guardar referencia al translator
    
    def initialize(self):
        """Inicializa la aplicación."""
        # Leer idioma guardado en configuración ANTES de crear QApplication
        from PySide6.QtCore import QSettings, QLocale
        settings = QSettings("ArtStudio3D", "Creative ERP")
        lang = settings.value("language", "es")
        
        # Establecer el locale ANTES de crear QApplication
        locale = QLocale(lang)
        QLocale.setDefault(locale)
        
        # Crear aplicación Qt
        self.qapp = QApplication(sys.argv)
        self.qapp.setApplicationName("Creative ERP")
        self.qapp.setOrganizationName("ArtStudio3D")
        self.qapp.setOrganizationDomain("artstudio3d.com")
        
        # Cargar traducciones
        print("Cargando traducciones...")
        from core.translations import load_translation
        
        # Cargar traducción con el idioma configurado
        self.translator = load_translation(self.qapp, lang)
        if self.translator:
            print(f"✓ Idioma cargado: {lang}")
        else:
            print("⚠ No se pudo cargar el archivo de traducción")
        
        # Configurar estilo - usar el estilo nativo del sistema para compatibilidad con dark themes
        # self.qapp.setStyle("Fusion")  # Comentado para permitir temas del sistema
        
        # Inicializar base de datos
        print("Inicializando base de datos...")
        init_db()
        print("✓ Base de datos lista")
        
        return True
    
    def show_login(self):
        """Muestra la ventana de login multi-empresa."""
        from app.views.login_window_multi import LoginWindowMultiCompany
        
        self.login_window = LoginWindowMultiCompany(self.auth_manager)
        self.login_window.login_successful.connect(self.on_login_success)
        self.login_window.show()
    
    def on_login_success(self):
        """Callback cuando el login es exitoso."""
        if self.login_window is not None:
            try:
                self.login_window.close()
            except Exception:
                pass
        self.show_main_window()
    
    def show_main_window(self):
        """Muestra la ventana principal con los módulos del usuario."""
        from app.views.main_window_v2 import MainWindowV2
        
        session = self.auth_manager.get_current_session()
        if not session:
            self.show_login()
            return
        
        print(f"\n✓ Usuario: {session.user.full_name}")
        print(f"✓ Rol: {session.user.role.value}")
        
        self.main_window = MainWindowV2(session)
        self.main_window.logout_requested.connect(self.on_logout)
        self.main_window.show()
    
    def on_logout(self):
        """Callback cuando se cierra sesión."""
        if self.main_window:
            self.main_window.close()
        self.auth_manager.logout()
        self.show_login()
    
    def run(self):
        """Ejecuta la aplicación."""
        if not self.initialize():
            return 1
        
        # Mostrar login al inicio
        self.show_login()
        
        # Ejecutar loop de eventos Qt
        # Asegurar para el analizador de tipos que `qapp` no es None
        qapp = self.qapp
        if qapp is None:
            return 1
        return qapp.exec()


def run_app():
    """Punto de entrada de la aplicación."""
    app = CreativeERPApp()
    sys.exit(app.run())