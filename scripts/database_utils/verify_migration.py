"""
Script para verificar que la migración se realizó correctamente
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import psycopg2
import pymysql

POSTGRES_CONFIG = {
    "host": "192.168.1.28",
    "port": 5432,
    "user": "admin",
    "password": "admin123",
    "database": "creative_erp",
}

MARIADB_CONFIG = {
    "host": "192.168.1.28",
    "port": 3306,
    "user": "admin",
    "password": "admin123",
    "database": "creative_erp",
}


def verify_postgres():
    print("=" * 80)
    print("VERIFICACIÓN POSTGRESQL")
    print("=" * 80)
    print(f"Host: {POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}")
    print(f"Usuario: {POSTGRES_CONFIG['user']}")
    print(f"Base de datos: {POSTGRES_CONFIG['database']}")
    print()

    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor()

        # Listar tablas
        cursor.execute(
            """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """
        )
        tables = cursor.fetchall()

        print("✅ Conexión exitosa")
        print(f"Tables found ({len(tables)}):\n")

        total_records = 0
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            total_records += count
            status = "✅" if count > 0 else "  "
            print(f"   {status} {table_name}: {count} registros")

        print(f"\nTotal records: {total_records}")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def verify_mariadb():
    print("\n" + "=" * 80)
    print("VERIFICACIÓN MARIADB")
    print("=" * 80)
    print(f"Host: {MARIADB_CONFIG['host']}:{MARIADB_CONFIG['port']}")
    print(f"Usuario: {MARIADB_CONFIG['user']}")
    print(f"Base de datos: {MARIADB_CONFIG['database']}")
    print()

    try:
        conn = pymysql.connect(**MARIADB_CONFIG)
        cursor = conn.cursor()

        # Verificar si la base de datos existe
        cursor.execute("SHOW DATABASES LIKE 'creative_erp'")
        db_exists = cursor.fetchone()

        if not db_exists:
            print("⚠️  La base de datos 'creative_erp' NO existe en MariaDB")
            print("\nNote: To create the database, run:")
            print("   CREATE DATABASE creative_erp;")
            print("   GRANT ALL PRIVILEGES ON creative_erp.* TO 'admin'@'%';")
            print("   FLUSH PRIVILEGES;")
            cursor.close()
            conn.close()
            return False

        # Listar tablas
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        print("✅ Conexión exitosa")
        print(f"Tables found ({len(tables)}):\n")

        total_records = 0
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            total_records += count
            status = "✅" if count > 0 else "  "
            print(f"   {status} {table_name}: {count} registros")

        print(f"\nTotal records: {total_records}")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    pg_ok = verify_postgres()
    mb_ok = verify_mariadb()

    print("\n" + "=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print(f"PostgreSQL: {'✅ OK' if pg_ok else '❌ Error'}")
    print(f"MariaDB:    {'✅ OK' if mb_ok else '❌ Error'}")
    print("=" * 80)
