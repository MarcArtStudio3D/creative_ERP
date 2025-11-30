#!/usr/bin/env python3
"""
Demo interactivo del módulo de Divisiones del Almacén
Ejecuta el diálogo de gestión de Secciones, Familias y Subfamilias
"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from PySide6.QtWidgets import QApplication
from modules.articulos.divisiones_view import DivisionesView
from core.db import init_db


def main():
    """Función principal"""
    print("=" * 60)
    print("DEMO: Gestión de Divisiones del Almacén")
    print("=" * 60)
    print("\nInicializando...")
    
    # Inicializar base de datos
    init_db()
    
    # Crear aplicación Qt
    app = QApplication(sys.argv)
    
    # Crear y mostrar el diálogo
    print("Abriendo diálogo de Divisiones...\n")
    dialog = DivisionesView()
    dialog.setWindowTitle("Demo - Divisiones del Almacén")
    
    # Mostrar instrucciones
    print("INSTRUCCIONES:")
    print("1. Click en 'Añadir sección' para crear una nueva sección")
    print("2. Selecciona una sección y click en 'Añadir familia'")
    print("3. Selecciona una familia y click en 'Añadir subfamilia'")
    print("4. Usa los botones 'Editar' y 'Borrar' para modificar/eliminar")
    print("5. El árbol superior muestra la jerarquía seleccionada")
    print("\nCierra el diálogo para finalizar la demo.\n")
    print("=" * 60)
    
    # Ejecutar
    result = dialog.exec()
    
    print("\n" + "=" * 60)
    print("Demo finalizada")
    print("=" * 60)
    
    return result


if __name__ == "__main__":
    sys.exit(main())
