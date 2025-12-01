"""
Script para eliminar las tablas no utilizadas (invoices, invoice_lines) de las bases de datos
"""
import sys
import sqlite3
from pathlib import Path
from sqlalchemy import create_engine, text

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configuración
SQLITE_DB_PATH = project_root / "creative_erp.db"
MARIADB_URL = "mysql+pymysql://admin:admin123@127.0.0.1:3306/creative_erp"

TABLES_TO_DROP = ["invoice_lines", "invoices"]

def clean_sqlite():
    print("\n" + "=" * 60)
    print("LIMPIEZA SQLITE")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        
        for table in TABLES_TO_DROP:
            print(f"Eliminando tabla: {table}")
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print("   ✅ Eliminada")
            
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error en SQLite: {e}")
        return False

def clean_mariadb():
    print("\n" + "=" * 60)
    print("LIMPIEZA MARIADB")
    print("=" * 60)
    
    try:
        engine = create_engine(MARIADB_URL)
        with engine.connect() as connection:
            for table in TABLES_TO_DROP:
                print(f"Eliminando tabla: {table}")
                connection.execute(text(f"DROP TABLE IF EXISTS `{table}`"))
                print("   ✅ Eliminada")
            
            connection.commit()
        return True
    except Exception as e:
        print(f"❌ Error en MariaDB: {e}")
        return False

if __name__ == "__main__":
    print("INICIANDO LIMPIEZA DE TABLAS NO UTILIZADAS")
    
    sqlite_ok = clean_sqlite()
    mariadb_ok = clean_mariadb()
    
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"SQLite:  {'✅ OK' if sqlite_ok else '❌ Error'}")
    print(f"MariaDB: {'✅ OK' if mariadb_ok else '❌ Error'}")
    print("=" * 60)
