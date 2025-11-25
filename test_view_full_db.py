#!/usr/bin/env python3
"""
Script de prueba para verificar que view_full.py usa la base de datos correcta.
"""

import sys
from pathlib import Path

# Configurar sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_view_full_database_connection():
    """Prueba que view_full.py use la sesión de la base de datos correcta."""
    print("🔍 Probando conexión de base de datos en view_full.py...")
    
    try:
        # Configurar el sistema para usar la base de datos de empresa
        from core.company_manager import CompanyDatabaseManager
        from core.db import get_session
        
        company_manager = CompanyDatabaseManager()
        
        # Listar empresas disponibles primero
        empresas = company_manager.get_available_companies()
        print(f"📊 Empresas disponibles: {len(empresas)}")
        
        for emp in empresas:
            print(f"   - ID: {emp['id']}, Nombre: {emp.get('nombre', 'N/A')}")
            # Obtener info de la base de datos para cada empresa
            db_info = company_manager.validate_company_database(emp['id'])
            print(f"     BD: {db_info.get('database_name', 'N/A')}")
        
        # Buscar una empresa que use la BD artstudio3d (o usar la primera disponible)
        target_company = None
        for empresa in empresas:
            db_info = company_manager.validate_company_database(empresa['id'])
            db_name = db_info.get('database_name', '')
            print(f"🔍 Verificando empresa {empresa['id']}: BD={db_name}")
            if 'artstudio3d' in db_name.lower():
                target_company = empresa
                break
        
        # Si no hay BD artstudio3d, usar la primera empresa disponible para la prueba
        if not target_company and empresas:
            target_company = empresas[0]
            print("⚠️  No se encontró BD artstudio3d, usando primera empresa disponible para la prueba")
        
        if not target_company:
            print("❌ No hay empresas disponibles para la prueba")
            return False
        
        company_id = target_company['id']
        print(f"🎯 Usando empresa: {company_id} (BD: {target_company.get('database_name')})")
        
        # Seleccionar empresa
        success = company_manager.select_company(company_id)
        if not success:
            print(f"❌ No se pudo seleccionar la empresa {company_id}")
            return False
        
        print(f"✅ Empresa {company_id} seleccionada")
        
        # Obtener sesión de la base de datos actual
        session = get_session()
        print(f"✅ Sesión de BD obtenida: {session.bind}")
        
        # Crear instancia de ClientesViewFull con la sesión correcta
        from modules.clientes.view_full import ClientesViewFull
        from PySide6.QtWidgets import QApplication
        
        # Necesitamos una aplicación Qt para crear widgets
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        view_full = ClientesViewFull(session=session)
        print("✅ ClientesViewFull creado con sesión de empresa")
        
        # Verificar que el repositorio use la sesión correcta
        if view_full.repository.session == session:
            print("✅ El repositorio usa la sesión correcta")
        else:
            print("❌ El repositorio NO usa la sesión correcta")
            return False
        
        # Intentar cargar clientes para verificar la conexión
        try:
            clientes = view_full.repository.obtener_todos()
            print(f"✅ {len(clientes)} clientes encontrados en la BD de empresa")
            
            if len(clientes) > 0:
                primer_cliente = clientes[0]
                print(f"   Ejemplo: {primer_cliente.nombre_fiscal} (ID: {primer_cliente.id})")
            
        except Exception as e:
            print(f"❌ Error al obtener clientes: {e}")
            return False
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🧪 PRUEBA DE CONEXIÓN DE BASE DE DATOS EN VIEW_FULL")
    print("=" * 55)
    
    if test_view_full_database_connection():
        print("\n🎉 ¡PROBLEMA RESUELTO!")
        print("✅ view_full.py ahora usa la base de datos de empresa correcta")
        return True
    else:
        print("\n❌ Aún hay problemas con la conexión de base de datos")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)