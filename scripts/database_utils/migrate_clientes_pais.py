"""
Script para migrar la columna id_pais de la tabla clientes de INT a VARCHAR(100).
"""
import sys
from pathlib import Path
from sqlalchemy import create_engine, text

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configuración
MARIADB_URL = "mysql+pymysql://admin:admin123@127.0.0.1:3306/creative_erp"

def migrate_mariadb():
    print("\n" + "=" * 60)
    print("MIGRACIÓN MARIADB - CLIENTES.ID_PAIS")
    print("=" * 60)
    
    try:
        engine = create_engine(MARIADB_URL)
        with engine.connect() as connection:
            # 1. Modificar columna id_pais
            print("🛠️  Modificando columna id_pais a VARCHAR(100)...")
            try:
                # En MariaDB/MySQL usamos MODIFY COLUMN
                connection.execute(text("ALTER TABLE clientes MODIFY COLUMN id_pais VARCHAR(100) DEFAULT 'España'"))
                print("   ✅ Columna modificada")
            except Exception as e:
                print(f"   ❌ Error al modificar columna: {e}")
                return False
            
            # 2. Actualizar valores numéricos antiguos (opcional, asumiendo 1=España)
            print("🔄 Normalizando valores antiguos...")
            try:
                result = connection.execute(text("UPDATE clientes SET id_pais = 'España' WHERE id_pais = '1'"))
                print(f"   ✅ Registros actualizados ('1' -> 'España'): {result.rowcount}")
            except Exception as e:
                print(f"   ⚠️  Error al actualizar datos: {e}")

            connection.commit()
        return True
    except Exception as e:
        print(f"❌ Error de conexión o ejecución: {e}")
        return False

if __name__ == "__main__":
    migrate_mariadb()
