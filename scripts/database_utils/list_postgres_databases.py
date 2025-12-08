"""
Script simple para listar bases de datos en PostgreSQL
"""

import psycopg2

conn = psycopg2.connect(
    host="192.168.1.28",
    port=5432,
    user="admin",
    password="admin123",
    database="postgres",  # Conectar a la BD por defecto
)

cursor = conn.cursor()

print("=" * 60)
print("BASES DE DATOS EN POSTGRESQL (192.168.1.28)")
print("=" * 60)

cursor.execute(
    """
    SELECT datname, 
           pg_size_pretty(pg_database_size(datname)) as size
    FROM pg_database 
    WHERE datistemplate = false
    ORDER BY datname
"""
)

databases = cursor.fetchall()

for db_name, size in databases:
    marker = "->" if db_name == "creative_erp" else "  "
    print(f"{marker} {db_name:20} ({size})")

cursor.close()
conn.close()

print("=" * 60)
print("\nNote: If you don't see 'creative_erp' in Antares:")
print("   1. Haz clic derecho en la conexión → Refresh/Reload")
print("   2. O desconecta y reconecta")
print("   3. O reinicia Antares")
