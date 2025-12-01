#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de deselección en divisiones
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from PySide6.QtWidgets import QApplication
from modules.articulos.divisiones_view import DivisionesView
from core.db import set_current_database

def test_divisiones_deselection():
    """Test de deselección en divisiones"""
    app = QApplication.instance() or QApplication(sys.argv)
    
    # Configurar base de datos
    set_current_database('artstudio3d')
    print("✅ Base de datos configurada a: artstudio3d")
    
    # Crear ventana de divisiones
    window = DivisionesView()
    window.show()
    
    print("🔧 Ventana de divisiones abierta con mejoras:")
    print("   - Clic en área vacía deselecciona")
    print("   - Clic en elemento seleccionado lo deselecciona")
    print("   - Tecla Escape limpia todas las selecciones")
    print("   - Los botones se habilitan/deshabilitan correctamente")
    print("   - Los campos se pueden editar después de deseleccionar")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(test_divisiones_deselection())