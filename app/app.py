"""
Aplicación principal del Creative ERP.
Gestiona el inicio, login y navegación entre módulos.
"""

import atexit
import sys

from PySide6.QtWidgets import QApplication

from core.db import close_all_engines

# Registrar cierre de engines al salir de la aplicación
atexit.register(close_all_engines)

import logging

from core.auth import AuthenticationManager
from core.module_manager import ModuleManager


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
        self.qapp.setOrganizationDomain("artstudio3d.fr")

        # Cargar estilo moderno si está disponible (aplicar globalmente)
        try:
            import os

            qss_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "resources", "styles", "modern.qss"
            )
            if os.path.exists(qss_path):
                with open(qss_path, "r", encoding="utf-8") as f:
                    qss = f.read()
                    # Aplicar al QApplication
                    self.qapp.setStyleSheet(qss)
                    logging.getLogger(__name__).info(
                        "✓ Estilo moderno cargado desde %s", qss_path
                    )
            else:
                logging.getLogger(__name__).warning(
                    "modern.qss no encontrado en %s; se usará el estilo por defecto",
                    qss_path,
                )
        except Exception:
            logging.getLogger(__name__).exception("Error aplicando modern.qss")

        # Cargar traducciones según configuración guardada (si existe)
        try:
            from PySide6.QtCore import QSettings
            from core.translations import load_translation

            settings = QSettings()
            lang = settings.value("language", None)
            # Si hay un idioma guardado, intentar cargar su traductor
            translator = None
            if lang:
                try:
                    translator = load_translation(self.qapp, lang)
                except Exception:
                    logging.getLogger(__name__).exception(
                        "No se pudo cargar la traducción al iniciar: %s", lang
                    )
            # Guardar referencia en la instancia de QApplication para que otros
            # módulos puedan actualizarlo (change_language) en tiempo de ejecución.
            setattr(self.qapp, "_creative_erp_translator", translator)
            if lang is None:
                logging.getLogger(__name__).info(
                    "No hay preferencia de idioma en QSettings; se usa el idioma por defecto."
                )
            else:
                if translator:
                    logging.getLogger(__name__).info(
                        "✓ Traducción inicial cargada: %s", lang
                    )
                else:
                    logging.getLogger(__name__).warning(
                        "Se solicitó idioma %s pero no se pudo cargar la traducción (.qm faltante o inválido).",
                        lang,
                    )
        except Exception:
            # No debemos detener el inicio si algo falla en las traducciones
            logging.getLogger(__name__).debug(
                "No se pudo inicializar traducciones al arrancar."
            )

        # Set global application icon (try resource first, fallback to file path)
        try:
            from PySide6.QtGui import QIcon

            # resource path will exist after compiling designer.qrc -> modules/designer_rc.py
            # Try both prefixes in the qrc (some builds include it under PNG prefix)
            icon = QIcon(":/ICO/LogoIconoCreative.ico")
            if icon.isNull():
                icon = QIcon(":/PNG/LogoIconoCreative.ico")
            if icon.isNull():
                # Fallback to filesystem path in repository
                import os

                ico_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    "resources",
                    "icons",
                    "ico",
                    "LogoIconoCreative.ico",
                )
                if os.path.exists(ico_path):
                    icon = QIcon(ico_path)

            if not icon.isNull():
                self.qapp.setWindowIcon(icon)
                logging.getLogger(__name__).info(
                    "✓ Application icon set from LogoIconoCreative.ico"
                )
            else:
                logging.getLogger(__name__).warning(
                    "⚠️ Application icon not found (resource and fallback missing)"
                )
        except Exception as e:
            logging.getLogger(__name__).exception(
                f"⚠️ Error setting application icon: {e}"
            )

        # Nota: crear tablas en la base de datos es una acción explícita y
        # potencialmente destructiva. No la ejecutamos automáticamente al
        # iniciar la aplicación; la creación/migración de esquemas debe ser
        # una acción manual (admin) o parte de un flujo controlado.

        # Inicializar CompanyManager
        logging.getLogger(__name__).info("✓ CompanyManager inicializado")

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

        logging.getLogger(__name__).info(f"\n✓ Usuario: {session.user.full_name}")
        logging.getLogger(__name__).info(f"✓ Rol: {session.user.role.value}")

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
