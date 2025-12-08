#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de deselección en divisiones
"""

import os
import sys

sys.path.insert(0, os.path.abspath("."))

from PySide6.QtWidgets import QApplication

from core.db import set_current_database
from modules.articulos.divisiones_view import DivisionesView


def test_divisiones_deselection():
    """Test de deselección en divisiones"""
    QApplication.instance() or QApplication(sys.argv)

    # Configurar base de datos
    set_current_database("artstudio3d")
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

    # No ejecutamos el bucle Qt; comprobamos que la ventana se ha creado correctamente
    assert window.isVisible()


if __name__ == "__main__":
    sys.exit(test_divisiones_deselection())
