"""
Script de diagnóstico para verificar la conexión a PostgreSQL
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import psycopg2
from sqlalchemy import text

from core.db import get_engine_from_url

POSTGRES_URL = "postgresql://admin:admin123@192.168.1.28:5432/creative_erp"

print("=" * 60)
print("DIAGNÓSTICO DE CONEXIÓN POSTGRESQL")
print("=" * 60)

# Test 1: Conexión directa con psycopg2
print("\n1️⃣ Probando conexión directa con psycopg2...")
try:
    conn = psycopg2.connect(
        host="192.168.1.28",
        port=5432,
        user="admin",
        password="admin123",
        database="creative_erp",
    )
    print("   ✅ Conexión exitosa con psycopg2")

    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"   PostgreSQL version: {version[0]}")

    cursor.execute("SELECT current_database();")
    db = cursor.fetchone()
    print(f"   Current database: {db[0]}")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"   ❌ Error con psycopg2: {e}")
    print(f"   Tipo de error: {type(e).__name__}")

# Test 2: Listar bases de datos disponibles
print("\n2️⃣ Listando bases de datos disponibles...")
try:
    conn = psycopg2.connect(
        host="192.168.1.28",
        port=5432,
        user="admin",
        password="admin123",
        database="postgres",  # Conectar a la BD por defecto
    )
    cursor = conn.cursor()
    cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
    databases = cursor.fetchall()
    print("   Databases found:")
    for db in databases:
        print(f"      - {db[0]}")

    # Verificar permisos del usuario admin
    print("\n   Checking privileges for user 'admin'...")
    cursor.execute(
        """
        SELECT datname, has_database_privilege('admin', datname, 'CONNECT') as can_connect
        FROM pg_database 
        WHERE datistemplate = false;
    """
    )
    perms = cursor.fetchall()
    for db, can_connect in perms:
        status = "✅" if can_connect else "❌"
        print(
            f"      {status} {db}: {'Puede conectar' if can_connect else 'NO puede conectar'}"
        )

    cursor.close()
    conn.close()

except Exception as e:
    print(f"   ❌ Error listando bases de datos: {e}")

# Test 3: Conexión con SQLAlchemy
print("\n3️⃣ Probando conexión con SQLAlchemy...")
try:
    engine = get_engine_from_url(POSTGRES_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT current_database();"))
        db = result.fetchone()
        print("   ✅ Conexión exitosa con SQLAlchemy")
        print(f"   Database: {db[0]}")

except Exception as e:
    print(f"   ❌ Error con SQLAlchemy: {e}")
    print(f"   Tipo de error: {type(e).__name__}")

print("\n" + "=" * 60)
print("FIN DEL DIAGNÓSTICO")
print("=" * 60)
