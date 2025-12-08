"""
Script para listar todas las tablas en la base de datos SQLite
"""

import sqlite3
from pathlib import Path

# Get absolute path to database
DB_PATH = Path(__file__).parent.parent / "creative_erp.db"

print("=" * 70)
print("TABLAS EN SQLITE - creative_erp.db")
print("=" * 70)
print()

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Obtener lista de tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = cursor.fetchall()

    print(f"Total tables: {len(tables)}\n")

    for i, (table_name,) in enumerate(tables, 1):
        # Contar registros
        cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`;")
        count = cursor.fetchone()[0]

        # Obtener columnas
        cursor.execute(f"PRAGMA table_info(`{table_name}`);")
        columns = cursor.fetchall()

        print(f"{i:2}. {table_name}")
        print(f"    └─ {count} registros, {len(columns)} columnas")

        # Mostrar primeras 3 columnas
        if columns:
            col_names = [col[1] for col in columns[:3]]
            more = f" (+{len(columns) - 3} más)" if len(columns) > 3 else ""
            print(f"       Columnas: {', '.join(col_names)}{more}")
        print()

    conn.close()

except Exception as e:
    print(f"❌ Error: {e}")

print("=" * 70)
