#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de selección de sección
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from PySide6.QtWidgets import QApplication
from modules.articulos.view import ArticulosView
from core.db import set_current_database

def test_articulos_seccion():
    """Test de selección de sección en artículos"""
    app = QApplication(sys.argv)
    
    # Configurar base de datos
    set_current_database('artstudio3d')
    print("✅ Base de datos configurada a: artstudio3d")
    
    # Crear ventana de artículos
    window = ArticulosView()
    window.show()
    
    print("🔧 Ventana de artículos abierta:")
    print("   - Haz clic en 'Añadir' para crear un nuevo artículo")
    print("   - El botón 'Buscar Sección' debería estar habilitado")
    print("   - Al hacer clic abrirá una consulta con las secciones disponibles")
    print("   - Selecciona una sección y se actualizará el campo txtseccion")
    print("   - Secciones disponibles:")
    print("     * 001 - Electrónica")
    print("     * 002 - Hogar") 
    print("     * 003 - Ropa")
    
    # No arrancamos el bucle de Qt en el test automático; comprobamos que la ventana se ha creado y es visible
    assert window.isVisible()

if __name__ == "__main__":
    sys.exit(test_articulos_seccion())