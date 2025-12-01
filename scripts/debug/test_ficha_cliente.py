#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de ficha de cliente.
"""

import sys
from pathlib import Path

# Configurar sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_ficha_import():
    """Prueba la importación de la ficha de cliente."""
    try:
        from modules.clientes.ficha_view import ClienteFichaView
        print("✅ ClienteFichaView importado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al importar ClienteFichaView: {e}")
        return False

def test_cliente_selected_signal():
    """Prueba que ClientesViewFull tenga la señal cliente_seleccionado."""
    try:
        from modules.clientes.view_full import ClientesViewFull
        from PySide6.QtCore import Signal
        
        # Verificar que la clase tiene la señal
        if hasattr(ClientesViewFull, 'cliente_seleccionado'):
            print("✅ Señal cliente_seleccionado encontrada en ClientesViewFull")
            return True
        else:
            print("❌ Señal cliente_seleccionado NO encontrada en ClientesViewFull")
            return False
    except Exception as e:
        print(f"❌ Error al verificar ClientesViewFull: {e}")
        return False

def main():
    print("CLIENT FORM FUNCTIONALITY TESTS")
    print("=" * 50)
    
    tests = [
        ("Importación ClienteFichaView", test_ficha_import),
        ("Señal cliente_selected", test_clientes_view_signal),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nChecking {test_name}:")
        if test_func():
            passed += 1
        
    print(f"\nFINAL RESULT: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed — functionality is ready.")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisar la implementación.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)