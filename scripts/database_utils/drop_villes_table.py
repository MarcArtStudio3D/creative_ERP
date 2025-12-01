"""
Script para eliminar la tabla 'villes' de la base de datos MariaDB.
Esta tabla no se usa en la aplicación principal (se usa france.db SQLite para búsquedas).
"""
import sys
from pathlib import Path
from sqlalchemy import create_engine, text

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configuración
MARIADB_URL = "mysql+pymysql://admin:admin123@127.0.0.1:3306/creative_erp"

def drop_villes_table():
    print("\n" + "=" * 60)
    print("LIMPIEZA MARIADB - ELIMINAR TABLA VILLES")
    print("=" * 60)
    
    try:
        engine = create_engine(MARIADB_URL)
        with engine.connect() as connection:
            print("Deleting table 'villes'...")
            try:
                connection.execute(text("DROP TABLE IF EXISTS villes"))
                print("   ✅ Tabla eliminada correctamente")
            except Exception as e:
                print(f"   ❌ Error al eliminar tabla: {e}")
                return False
            
            connection.commit()
        return True
    except Exception as e:
        print(f"❌ Error de conexión o ejecución: {e}")
        return False

if __name__ == "__main__":
    drop_villes_table()
