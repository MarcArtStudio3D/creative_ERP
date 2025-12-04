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
import logging
from modules.articulos.divisiones_view import DivisionesView
from core.db import init_db


def main():
    """Función principal"""
    logging.getLogger(__name__).info("=" * 60)
    logging.getLogger(__name__).info("DEMO: Gestión de Divisiones del Almacén")
    logging.getLogger(__name__).info("=" * 60)
    logging.getLogger(__name__).info("\nInicializando...")
    
    # Inicializar base de datos
    init_db()
    
    # Crear aplicación Qt
    app = QApplication(sys.argv)
    
    # Crear y mostrar el diálogo
    logging.getLogger(__name__).info("Abriendo diálogo de Divisiones...\n")
    dialog = DivisionesView()
    dialog.setWindowTitle("Demo - Divisiones del Almacén")
    
    # Mostrar instrucciones
    logging.getLogger(__name__).info("INSTRUCCIONES:")
    logging.getLogger(__name__).info("1. Click en 'Añadir sección' para crear una nueva sección")
    logging.getLogger(__name__).info("2. Selecciona una sección y click en 'Añadir familia'")
    logging.getLogger(__name__).info("3. Selecciona una familia y click en 'Añadir subfamilia'")
    logging.getLogger(__name__).info("4. Usa los botones 'Editar' y 'Borrar' para modificar/eliminar")
    logging.getLogger(__name__).info("5. El árbol superior muestra la jerarquía seleccionada")
    logging.getLogger(__name__).info("\nCierra el diálogo para finalizar la demo.\n")
    logging.getLogger(__name__).info("=" * 60)
    
    # Ejecutar
    result = dialog.exec()
    
    logging.getLogger(__name__).info("\n" + "=" * 60)
    logging.getLogger(__name__).info("Demo finalizada")
    logging.getLogger(__name__).info("=" * 60)
    
    return result


if __name__ == "__main__":
    sys.exit(main())
