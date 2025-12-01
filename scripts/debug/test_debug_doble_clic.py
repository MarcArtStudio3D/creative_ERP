#!/usr/bin/env python3
"""
Script de prueba con debug para verificar el problema del doble clic.
"""

import sys
from pathlib import Path

# Configurar sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_debug_double_click():
    """Prueba con debug para verificar el problema del doble clic."""
    try:
        from PySide6.QtWidgets import QApplication
        from core.company_manager import CompanyDatabaseManager
        from core.db import get_session
        from modules.clientes.view_full import ClientesViewFull
        
        # Crear aplicación Qt si no existe
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        print("DEBUG: Configuring company...")
        
        # Configurar empresa
        company_manager = CompanyDatabaseManager()
        empresas = company_manager.get_available_companies()
        
        if not empresas:
            print("❌ No hay empresas disponibles")
            return False
        
        # Usar primera empresa
        company_id = empresas[0]['id']
        success = company_manager.select_company(company_id)
        
        if not success:
            print(f"❌ No se pudo seleccionar empresa {company_id}")
            return False
        
        print(f"✅ Empresa {company_id} seleccionada")
        
        # Obtener sesión correcta
        session = get_session()
        
        print("DEBUG: Creating ClientesViewFull...")
        
        # Crear ClientesViewFull con la sesión correcta
        view_full = ClientesViewFull(session=session)
        print("✅ ClientesViewFull creado")
        
        print("DEBUG: Info about created view:")
        
        # Verificar StackedWidget
        if hasattr(view_full.ui, 'stackedWidget'):
            current_page = view_full.ui.stackedWidget.currentIndex()
            page_count = view_full.ui.stackedWidget.count()
            print(f"   • StackedWidget: {page_count} páginas, actual: {current_page}")
        else:
            print("   • ❌ No hay StackedWidget")
        
        # Verificar tabla
        tabla = None
        tabla_names = ['tabla_busquedas', 'tabla_clientes', 'tableWidget']
        for name in tabla_names:
            if hasattr(view_full.ui, name):
                tabla = getattr(view_full.ui, name)
                print(f"   • Tabla encontrada: {name} ({type(tabla).__name__})")
                break
        
        if tabla is None:
            print("   • ❌ No se encontró tabla")
        else:
            # Verificar modelo de la tabla
            model = tabla.model()
            if model:
                row_count = model.rowCount()
                print(f"   • Modelo: {type(model).__name__} con {row_count} filas")
                
                # Verificar si hay datos en UserRole
                if row_count > 0:
                    try:
                        first_item = model.item(0, 0)
                        if first_item:
                            from PySide6.QtCore import Qt
                            user_data = first_item.data(Qt.ItemDataRole.UserRole)
                            print(f"   • Primer item UserData: {user_data}")
                        else:
                            print("   • ❌ Primer item es None")
                    except Exception as e:
                        print(f"   • ❌ Error accediendo UserData: {e}")
            else:
                print("   • ❌ No hay modelo en la tabla")
        
        # Verificar el repositorio
        if hasattr(view_full, 'repository'):
            print(f"   • Repositorio: {type(view_full.repository).__name__}")
            try:
                clientes_count = len(view_full.repository.obtener_todos())
                print(f"   • Clientes en repositorio: {clientes_count}")
            except Exception as e:
                print(f"   • ❌ Error obteniendo clientes: {e}")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("DEBUG: DOUBLE CLICK ISSUE IN CLIENTS")
    print("=" * 50)
    
    if test_debug_double_click():
        print("\nDebug complete - review messages above")
        return True
    else:
        print("\n❌ Error en debug")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)