#!/usr/bin/env python3
"""
Test para verificar la funcionalidad de selección de sección en artículos
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from PySide6.QtWidgets import QApplication
from modules.articulos.view import ArticulosView
from core.db import set_current_database

def test_seccion_lookup():
    """Test de selección de sección"""
    app = QApplication.instance() or QApplication(sys.argv)
    
    # Configurar base de datos
    set_current_database('artstudio3d')
    print("✅ Base de datos configurada a: artstudio3d")
    
    # Crear ventana de artículos
    window = ArticulosView()
    window.show()
    
    print("🔧 Ventana de artículos abierta con funcionalidad de sección:")
    print("   - Navega a la segunda pestaña")
    print("   - Haz clic en el botón de búsqueda junto a 'txtseccion'")
    print("   - Selecciona una sección de la lista")
    print("   - El valor debe aparecer en el campo txtseccion")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(test_seccion_lookup())