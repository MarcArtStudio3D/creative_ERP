"""
Script simple para verificar MariaDB usando solo SQLAlchemy
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text, inspect

MARIADB_URL = "mysql+pymysql://root:1234@127.0.0.1:3306/creative_erp"

print("=" * 60)
print("VERIFICACIÓN MARIADB CON SQLALCHEMY")
print("=" * 60)

print("\nAttempting to connect to MariaDB...")
print(f"   URL: {MARIADB_URL}")

try:
    engine = create_engine(MARIADB_URL, echo=False)
    
    # Test connection
    with engine.connect() as connection:
        print("\nCONNECTION SUCCESSFUL")
        
        # Get current database
        result = connection.execute(text("SELECT DATABASE();"))
        db = result.fetchone()
        print(f"\nCurrent database: {db[0]}")
        
        # Get MariaDB version
        result = connection.execute(text("SELECT VERSION();"))
        version = result.fetchone()
        print(f"Version: {version[0]}")
    
    # Use inspector to get tables
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"\nTABLES FOUND: {len(tables)}")
    if tables:
        for i, table in enumerate(tables, 1):
            print(f"   {i}. {table}")
            
            # Count records in each table
            with engine.connect() as connection:
                result = connection.execute(text(f"SELECT COUNT(*) FROM `{table}`;"))
                count = result.fetchone()[0]
                print(f"      → {count} registros")
    else:
        print("\nWARNING: NO TABLES FOUND IN THE DATABASE")
        print("\nPossible causes:")
        print("   1. La base de datos existe pero está vacía")
        print("   2. La migración no se ejecutó correctamente")
        print("   3. Las tablas se crearon en otra base de datos")
    
    engine.dispose()
    
except Exception as e:
    print(f"\nERROR: {e}")
    print(f"   Tipo: {type(e).__name__}")
    
    if "Unknown database" in str(e):
        print("\nNote: The 'creative_erp' database does NOT exist")
        print("   Necesitas crearla primero con:")
        print("   CREATE DATABASE creative_erp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    elif "Access denied" in str(e):
        print("\nNote: Authentication problem")
        print("   Check MariaDB username/password")

print("\n" + "=" * 60)
