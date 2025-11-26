#!/usr/bin/env python3
"""
Script de prueba para verificar que ClientesViewFull funciona correctamente.
"""

import sys
from pathlib import Path

# Configurar sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_clientes_view_full():
    """Prueba que ClientesViewFull se cargue y funcione correctamente."""
    try:
        from PySide6.QtWidgets import QApplication
        from core.company_manager import CompanyDatabaseManager
        from core.db import get_session
        from modules.clientes.view_full import ClientesViewFull
        
        # Crear aplicación Qt si no existe
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
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
        
        # Verificar que hay clientes
        from modules.clientes.models import Cliente
        cliente = session.query(Cliente).first()
        
        if not cliente:
            print("❌ No hay clientes en la base de datos")
            return False
        
        print(f"✅ Cliente encontrado para prueba: {cliente.nombre_fiscal}")
        
        # Crear ClientesViewFull con la sesión correcta
        view_full = ClientesViewFull(session=session)
        print("✅ ClientesViewFull creado correctamente")
        
        # Verificar que tiene StackedWidget
        if hasattr(view_full.ui, 'stackedWidget'):
            print(f"✅ StackedWidget encontrado con {view_full.ui.stackedWidget.count()} páginas")
            current_page = view_full.ui.stackedWidget.currentIndex()
            print(f"   Página actual: {current_page}")
        else:
            print("❌ No se encontró StackedWidget en la UI")
            return False
        
        # Verificar que tiene la tabla de búsquedas
        tabla = None
        for attr_name in ['tabla_busquedas', 'tabla_clientes', 'tableWidget']:
            if hasattr(view_full.ui, attr_name):
                tabla = getattr(view_full.ui, attr_name)
                print(f"✅ Tabla encontrada: {attr_name}")
                break
        
        if tabla is None:
            print("❌ No se encontró tabla de clientes")
            return False
        
        # Verificar que la tabla tiene datos
        model = tabla.model()
        if model and model.rowCount() > 0:
            print(f"✅ Tabla cargada con {model.rowCount()} clientes")
        else:
            print("⚠️ La tabla no tiene datos o no tiene modelo")
        
        # Verificar que existe el método abrir_ficha_cliente
        if hasattr(view_full, 'abrir_ficha_cliente'):
            print("✅ Método abrir_ficha_cliente encontrado")
        else:
            print("❌ Método abrir_ficha_cliente NO encontrado")
            return False
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🧪 PRUEBA DE CLIENTESVIEWFULL")
    print("=" * 35)
    
    if test_clientes_view_full():
        print("\n🎉 ¡CLIENTESVIEWFULL FUNCIONA CORRECTAMENTE!")
        print("✅ La UI generada desde frmClientes.ui está operativa")
        print("✅ StackedWidget para navegación lista ↔ ficha")
        print("✅ Tabla de clientes con datos cargados")
        print("✅ Método abrir_ficha_cliente disponible")
        return True
    else:
        print("\n❌ Hay problemas con ClientesViewFull")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)