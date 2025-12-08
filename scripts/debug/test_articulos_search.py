#!/usr/bin/env python3
"""
Test script for Articulos search functionality
Tests the search dialog integration and Ctrl+F keyboard shortcut
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication

from core.db import init_database, set_current_database
from modules.articulos.view import ArticulosView


def test_search_integration():
    """Test the search dialog integration"""
    print("Testing Articulos Search Integration...")

    app = QApplication(sys.argv)

    try:
        # Initialize database
        print("Inicializando base de datos...")
        init_database()
        set_current_database("artstudio3d")

        # Create view
        print("Creando vista de Artículos...")
        view = ArticulosView()

        # Verify search shortcut exists
        print("⌨️  Verifying Ctrl+F keyboard shortcut...")
        assert hasattr(view, "search_shortcut"), "Search shortcut not found!"
        assert (
            view.search_shortcut.key().toString() == "Ctrl+F"
        ), "Shortcut key mismatch!"
        print("✅ Keyboard shortcut configured correctly")

        # Verify search button connection
        print("Verificando la conexión del botón de búsqueda...")
        assert (
            view.ui.btnBuscar.receivers(view.ui.btnBuscar.clicked) > 0
        ), "Search button not connected!"
        print("✅ Search button connected")

        # Show the view for manual testing
        print("\nListado de instrucciones manuales:")
        print("   1. Click the 'Buscar' button or press Ctrl+F")
        print("   2. The search dialog should appear")
        print("   3. Type in the search box to filter articles")
        print("   4. Select an article and click 'Aceptar'")
        print("   5. The article should load in the form view")
        print("\nLaunching Articulos view for manual testing...")

        view.show()
        sys.exit(app.exec())

    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_search_integration()
