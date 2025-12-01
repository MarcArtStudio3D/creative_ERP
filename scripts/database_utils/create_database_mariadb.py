"""
Script para crear la base de datos creative_erp en MariaDB
"""
import pymysql
from pymysql.constants import CLIENT

HOST = "192.168.1.28"
PORT = 3306
USER = "admin"
PASSWORD = "admin123"
DB_NAME = "creative_erp"

print("=" * 80)
print("CREACIÓN DE BASE DE DATOS creative_erp EN MARIADB")
print("=" * 80)

try:
    # Intentar conectar sin especificar base de datos
    print(f"\nConnecting to MariaDB at {HOST}:{PORT} as '{USER}'...")
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        client_flag=CLIENT.MULTI_STATEMENTS
    )
    
    cursor = conn.cursor()
    
    # Verificar privilegios del usuario
    print(f"\nChecking privileges for user '{USER}'...")
    cursor.execute("SHOW GRANTS FOR CURRENT_USER()")
    grants = cursor.fetchall()
    print("   Privilegios actuales:")
    for grant in grants:
        print(f"   - {grant[0]}")
    
    # Verificar si la base de datos ya existe
    print(f"\nChecking if '{DB_NAME}' exists...")
    cursor.execute("SHOW DATABASES LIKE %s", (DB_NAME,))
    exists = cursor.fetchone()
    
    if exists:
        print(f"   WARNING: The database '{DB_NAME}' already exists")
        
        # Verificar si podemos acceder
        try:
            cursor.execute(f"USE {DB_NAME}")
            print(f"   Can access '{DB_NAME}'")
            
            # Listar tablas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"   Tables found: {len(tables)}")
            
        except pymysql.err.OperationalError as e:
            print(f"   Cannot access '{DB_NAME}': {e}")
            print(f"\nNote: An administrator should run:")
            print(f"   GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '{USER}'@'%';")
            print(f"   FLUSH PRIVILEGES;")
    else:
        print(f"   The database '{DB_NAME}' does NOT exist")
        print(f"\nAttempting to create database '{DB_NAME}'...")
        
        try:
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"   Database created successfully")
            
            print(f"\nGranting permissions to user '{USER}'...")
            cursor.execute(f"GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '{USER}'@'%'")
            cursor.execute("FLUSH PRIVILEGES")
            print(f"   ✅ Permisos otorgados")
            
        except pymysql.err.OperationalError as e:
            print(f"   Error creating database: {e}")
            print(f"\nNote: User '{USER}' may not have CREATE DATABASE privilege")
            print(f"   Necesitas que un administrador (root) ejecute:")
            print(f"   CREATE DATABASE {DB_NAME};")
            print(f"   GRANT ALL PRIVILEGES ON {DB_NAME}.* TO '{USER}'@'%';")
            print(f"   FLUSH PRIVILEGES;")
    
    # Listar todas las bases de datos accesibles
    print(f"\nDatabases accessible for '{USER}':")
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    for db in databases:
        marker = "->" if db[0] == DB_NAME else "  "
        print(f"   {marker} {db[0]}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 80)
    print("PROCESS COMPLETED")
    print("=" * 80)
    
except Exception as e:
    print(f"\nERROR: {e}")
    print(f"Tipo: {type(e).__name__}")
    print("\nNote: Check that:")
    print("   1. El servidor MariaDB esté accesible en 192.168.1.28:3306")
    print("   2. El usuario 'admin' existe y tiene la contraseña correcta")
    print("   3. El usuario tiene permisos suficientes")
