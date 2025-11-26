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

def test_clientes_view_signal():
    """Prueba que ClientesView tenga la señal cliente_selected."""
    try:
        from modules.clientes.view import ClientesView
        from PySide6.QtCore import Signal
        
        # Verificar que tiene la señal
        if hasattr(ClientesView, 'cliente_selected'):
            print("✅ Señal cliente_selected encontrada en ClientesView")
            return True
        else:
            print("❌ Señal cliente_selected NO encontrada en ClientesView")
            return False
    except Exception as e:
        print(f"❌ Error al verificar ClientesView: {e}")
        return False

def main():
    print("🧪 PRUEBAS DE FUNCIONALIDAD FICHA DE CLIENTE")
    print("=" * 50)
    
    tests = [
        ("Importación ClienteFichaView", test_ficha_import),
        ("Señal cliente_selected", test_clientes_view_signal),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        if test_func():
            passed += 1
        
    print(f"\n📊 RESULTADO FINAL: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! La funcionalidad está lista.")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisar la implementación.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)