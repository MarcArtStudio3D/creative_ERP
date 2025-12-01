#!/usr/bin/env python3
"""
Script para eliminar la tabla direcciones_alternativas_empresas de las bases de datos.
Esta tabla ya no se usa en la aplicación.
"""

import sys
import os
from pathlib import Path

# Añadir el directorio raíz al path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core.db import get_session, get_engine, get_database_url
from sqlalchemy import text, inspect


def drop_table_if_exists(engine, table_name: str):
    """Elimina una tabla si existe."""
    inspector = inspect(engine)
    
    if table_name in inspector.get_table_names():
        print(f"  ✓ Tabla '{table_name}' encontrada, eliminando...")
        with engine.connect() as conn:
            conn.execute(text(f"DROP TABLE {table_name}"))
            conn.commit()
        print(f"  ✅ Tabla '{table_name}' eliminada correctamente")
    else:
        print(f"  ℹ️  Tabla '{table_name}' no existe, nada que hacer")


def main():
    """Elimina la tabla direcciones_alternativas_empresas de todas las bases de datos."""
    
    print("=" * 60)
    print("Eliminando tabla 'direcciones_alternativas_empresas'")
    print("=" * 60)
    
    # 1. Base de datos principal (main)
    print("\n1️⃣  Base de datos MAIN:")
    try:
        main_engine = get_engine('main')
        drop_table_if_exists(main_engine, 'direcciones_alternativas_empresas')
    except Exception as e:
        print(f"  ❌ Error en base de datos main: {e}")
    
    # 2. Obtener todas las empresas para limpiar sus bases de datos
    print("\n2️⃣  Bases de datos de EMPRESAS:")
    try:
        from core.models import Empresa
        session = get_session()
        empresas = session.query(Empresa).all()
        
        if not empresas:
            print("  ℹ️  No hay empresas registradas")
        else:
            for empresa in empresas:
                print(f"\n  Empresa: {empresa.nombre_fiscal} (ID: {empresa.id})")
                try:
                    # Obtener URL de la base de datos de la empresa
                    from core.config import get_database_url_for_company
                    db_url = get_database_url_for_company(empresa.id)
                    
                    # Crear engine para esta empresa
                    from sqlalchemy import create_engine
                    empresa_engine = create_engine(db_url)
                    
                    drop_table_if_exists(empresa_engine, 'direcciones_alternativas_empresas')
                    
                    empresa_engine.dispose()
                    
                except Exception as e:
                    print(f"    ❌ Error procesando empresa {empresa.id}: {e}")
        
        session.close()
        
    except Exception as e:
        print(f"  ❌ Error obteniendo empresas: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Proceso completado")
    print("=" * 60)


if __name__ == "__main__":
    main()
