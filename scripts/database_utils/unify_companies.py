"""
Script para migrar y unificar las tablas companies y empresas.
1. Añade columna group_id a la tabla empresas.
2. Asigna group_id=1 a todas las empresas existentes.
3. Elimina la tabla companies.
"""
import sys
import sqlite3
from pathlib import Path
from sqlalchemy import text

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configuración
SQLITE_DB_PATH = project_root / "creative_erp.db"
MARIADB_URL = "mysql+pymysql://admin:admin123@127.0.0.1:3306/creative_erp"

def migrate_sqlite():
    print("\n" + "=" * 60)
    print("MIGRACIÓN SQLITE")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        # 1. Añadir columna group_id si no existe
        print("Verificando columna group_id en empresas...")
        try:
            cursor.execute("ALTER TABLE empresas ADD COLUMN group_id INTEGER DEFAULT 1")
            print("   ✅ Columna añadida")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("   ℹ️  La columna ya existe")
            else:
                raise e
        
        # 2. Actualizar group_id para registros existentes
        print("Updating existing records...")
        cursor.execute("UPDATE empresas SET group_id = 1 WHERE group_id IS NULL")
        print(f"   ✅ Registros actualizados: {cursor.rowcount}")
        
        # 3. Eliminar tabla companies
        print("Eliminando tabla companies...")
        cursor.execute("DROP TABLE IF EXISTS companies")
        print("   ✅ Tabla eliminada")
            
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error en SQLite: {e}")
        return False

def migrate_mariadb():
    print("\n" + "=" * 60)
    print("MIGRACIÓN MARIADB")
    print("=" * 60)
    
    try:
        from core.db import get_engine_from_url
        engine = get_engine_from_url(MARIADB_URL)
        with engine.connect() as connection:
            # 1. Añadir columna group_id si no existe
            print("Verificando columna group_id en empresas...")
            try:
                connection.execute(text("ALTER TABLE empresas ADD COLUMN group_id INTEGER DEFAULT 1"))
                print("   ✅ Columna añadida")
            except Exception as e:
                if "Duplicate column name" in str(e):
                    print("   ℹ️  La columna ya existe")
                else:
                    # Si falla, intentamos continuar (puede que ya exista)
                    print(f"   ⚠️  Nota: {e}")
            
            # 2. Actualizar group_id para registros existentes
            print("Updating existing records...")
            result = connection.execute(text("UPDATE empresas SET group_id = 1 WHERE group_id IS NULL"))
            print(f"   ✅ Registros actualizados: {result.rowcount}")
            
            # 3. Eliminar tabla companies
            print("Eliminando tabla companies...")
            connection.execute(text("DROP TABLE IF EXISTS companies"))
            print("   ✅ Tabla eliminada")
            
            connection.commit()
        return True
    except Exception as e:
        print(f"❌ Error en MariaDB: {e}")
        return False

if __name__ == "__main__":
    print("INICIANDO UNIFICACIÓN DE TABLAS DE EMPRESAS")
    
    sqlite_ok = migrate_sqlite()
    mariadb_ok = migrate_mariadb()
    
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"SQLite:  {'✅ OK' if sqlite_ok else '❌ Error'}")
    print(f"MariaDB: {'✅ OK' if mariadb_ok else '❌ Error'}")
    print("=" * 60)
