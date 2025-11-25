#!/usr/bin/env python3
"""
Script para crear las tablas faltantes en la base de datos artstudio3d.
"""

import sys
from pathlib import Path

# Configurar sys.path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def create_missing_tables():
    """Crea las tablas faltantes en la base de datos."""
    try:
        from core.company_manager import CompanyDatabaseManager
        from core.db import get_session, init_db, get_engine
        from sqlalchemy import text, inspect
        
        print("🔧 CREACIÓN DE TABLAS FALTANTES")
        print("=" * 40)
        
        # Configurar empresa
        company_manager = CompanyDatabaseManager()
        empresas = company_manager.get_available_companies()
        
        if not empresas:
            print("❌ No hay empresas disponibles")
            return False
        
        # Usar primera empresa (debería ser artstudio3d)
        company_id = empresas[0]['id']
        success = company_manager.select_company(company_id)
        
        if not success:
            print(f"❌ No se pudo seleccionar empresa {company_id}")
            return False
        
        print(f"✅ Empresa {company_id} seleccionada")
        
        # Obtener engine actual
        engine = get_engine()
        inspector = inspect(engine)
        
        print(f"🔍 Base de datos actual: {engine.url}")
        print(f"📊 Tablas existentes: {inspector.get_table_names()}")
        
        # Importar todos los modelos necesarios
        print("\n🔄 Importando modelos...")
        from modules.clientes import models as clientes_models
        from modules.tipo_cliente import models as tipo_cliente_models
        
        # Verificar tablas específicas
        tables_to_check = [
            ('clientes', 'Cliente'),
            ('historial_clientes', 'HistorialCliente'),
            ('deudas_clientes', 'DeudaCliente'),
            ('estadisticas_clientes_mes', 'EstadisticaClienteMes'),
            ('direcciones_alternativas', 'DireccionAlternativa'),
            ('tipos_cliente', 'TipoCliente'),
            ('subtipos_cliente', 'TipoSubCliente')
        ]
        
        existing_tables = inspector.get_table_names()
        missing_tables = []
        
        for table_name, model_name in tables_to_check:
            if table_name not in existing_tables:
                missing_tables.append((table_name, model_name))
                print(f"❌ Tabla faltante: {table_name}")
            else:
                print(f"✅ Tabla existe: {table_name}")
        
        if not missing_tables:
            print("\n🎉 ¡Todas las tablas están presentes!")
            return True
        
        print(f"\n⚠️  Se encontraron {len(missing_tables)} tablas faltantes")
        print("🔄 Creando tablas faltantes...")
        
        # Crear todas las tablas
        try:
            clientes_models.Base.metadata.create_all(bind=engine)
            print("✅ Tablas de clientes creadas")
        except Exception as e:
            print(f"❌ Error creando tablas de clientes: {e}")
        
        try:
            tipo_cliente_models.Base.metadata.create_all(bind=engine)
            print("✅ Tablas de tipos de cliente creadas")
        except Exception as e:
            print(f"❌ Error creando tablas de tipos de cliente: {e}")
        
        # Verificar que se crearon
        print("\n🔍 Verificando tablas creadas...")
        inspector = inspect(engine)
        new_existing_tables = inspector.get_table_names()
        
        all_created = True
        for table_name, model_name in missing_tables:
            if table_name in new_existing_tables:
                print(f"✅ {table_name} creada correctamente")
            else:
                print(f"❌ {table_name} NO se pudo crear")
                all_created = False
        
        return all_created
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    if create_missing_tables():
        print("\n🎉 ¡Todas las tablas han sido creadas correctamente!")
        print("✅ Ahora el guardado de clientes debería funcionar sin errores")
        return True
    else:
        print("\n❌ Hubo problemas creando algunas tablas")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)