"""
Script para listar todas las tablas y sus registros en MariaDB
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import inspect, text

from core.db import get_engine_from_url

MARIADB_URL = "mysql+pymysql://admin:admin123@127.0.0.1:3306/creative_erp"

print("=" * 70)
print("LISTADO DE TABLAS EN MARIADB - creative_erp")
print("=" * 70)

try:
    engine = get_engine_from_url(MARIADB_URL, echo=False)

    # Verificar conexión
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE();"))
        db = result.fetchone()
        print(f"\n✅ Conectado a base de datos: {db[0]}")

        result = connection.execute(text("SELECT VERSION();"))
        version = result.fetchone()
        print(f"MariaDB version: {version[0]}\n")

    # Obtener lista de tablas
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if not tables:
        print("WARNING: NO TABLES FOUND")
        print("\nLa base de datos existe pero está vacía.")
        print("Esto sugiere que la migración no se completó correctamente.")
    else:
        print(f"TOTAL TABLES: {len(tables)}\n")
        print("-" * 70)

        total_records = 0

        for i, table in enumerate(sorted(tables), 1):
            # Contar registros
            with engine.connect() as connection:
                result = connection.execute(text(f"SELECT COUNT(*) FROM `{table}`;"))
                count = result.fetchone()[0]
                total_records += count

            # Obtener columnas
            columns = inspector.get_columns(table)
            col_count = len(columns)

            print(f"{i:2}. {table}")
            print(f"    └─ {count} registros, {col_count} columnas")

            # Mostrar primeras 3 columnas como ejemplo
            if columns:
                col_names = [col["name"] for col in columns[:3]]
                more = f" (+{col_count - 3} más)" if col_count > 3 else ""
                print(f"       Columnas: {', '.join(col_names)}{more}")
            print()

        print("-" * 70)
        print("\nSUMMARY:")
        print(f"   • Total de tablas: {len(tables)}")
        print(f"   • Total de registros: {total_records}")

    engine.dispose()

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print(f"   Tipo: {type(e).__name__}")

    if "Unknown database" in str(e):
        print("\nNote: The 'creative_erp' database DOES NOT EXIST")
        print("   Necesitas crearla primero.")
    elif "Access denied" in str(e):
        print("\nNote: Authentication problem")
        print("   Verifica usuario/contraseña de MariaDB")
    elif "Can't connect" in str(e):
        print("\nNote: Cannot connect to the MariaDB server")
        print("   Check that MariaDB is running at 127.0.0.1:3306")

print("\n" + "=" * 70)
