#!/usr/bin/env python3
"""
Script de demostración del selector de idioma.
Abre solo el diálogo de configuración para mostrar la funcionalidad.
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings

# Importar el diálogo
from app.views.config_dialog import ConfigDialog


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Creative ERP")
    app.setOrganizationName("ArtStudio3D")
    
    # Mostrar idioma actual
    settings = QSettings()
    current_lang = settings.value("language", "es")
    print(f"Idioma actual: {current_lang}")
    
    # Crear y mostrar el diálogo
    dialog = ConfigDialog()
    
    # Conectar señal para ver el cambio
    def on_language_changed(lang_code):
        print(f"✓ Idioma cambiado a: {lang_code}")
    
    dialog.language_changed.connect(on_language_changed)
    
    # Mostrar diálogo
    result = dialog.exec()
    
    if result:
        print("Usuario aceptó los cambios")
        new_lang = settings.value("language", "es")
        print(f"Nuevo idioma guardado: {new_lang}")
    else:
        print("Usuario canceló")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
