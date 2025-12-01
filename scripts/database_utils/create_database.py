"""
Script para crear la base de datos creative_erp en PostgreSQL
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

HOST = "192.168.1.28"
PORT = 5432
USER = "admin"
PASSWORD = "admin123"
DB_NAME = "creative_erp"

print("=" * 60)
print("CREACIÓN DE BASE DE DATOS creative_erp")
print("=" * 60)

try:
    # Conectar a la base de datos por defecto 'postgres'
    print(f"\nConnecting to PostgreSQL at {HOST}:{PORT}...")
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database="postgres"
    )
    
    # Necesario para CREATE DATABASE
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Verificar si la base de datos ya existe
    print(f"\nChecking if '{DB_NAME}' exists...")
    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        (DB_NAME,)
    )
    exists = cursor.fetchone()
    
    if exists:
        print(f"   WARNING: The database '{DB_NAME}' already exists")
        print(f"   Checking permissions...")
        
        cursor.execute(
            "SELECT has_database_privilege(%s, %s, 'CONNECT')",
            (USER, DB_NAME)
        )
        can_connect = cursor.fetchone()[0]
        
        if can_connect:
            print(f"   User '{USER}' can connect to '{DB_NAME}'")
        else:
            print(f"   User '{USER}' CANNOT connect to '{DB_NAME}'")
            print(f"   Granting permissions...")
            cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {USER}")
            print(f"   ✅ Permisos otorgados")
    else:
        print(f"   The database '{DB_NAME}' does NOT exist")
        print(f"\nCreating database '{DB_NAME}'...")
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"   ✅ Base de datos creada exitosamente")
        
        print(f"\nGranting permissions to user '{USER}'...")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {USER}")
        print(f"   ✅ Permisos otorgados")
    
    # Listar todas las bases de datos
    print(f"\nAvailable databases:")
    cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname")
    for row in cursor.fetchall():
        marker = "->" if row[0] == DB_NAME else "  "
        print(f"   {marker} {row[0]}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("PROCESS COMPLETED")
    print("=" * 60)
    
except Exception as e:
    print(f"\nERROR: {e}")
    print(f"Tipo: {type(e).__name__}")
