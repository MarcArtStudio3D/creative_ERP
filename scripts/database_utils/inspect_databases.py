"""
Script para inspeccionar las bases de datos SQLite disponibles
"""
import sqlite3
from pathlib import Path

# Bases de datos a inspeccionar
databases = [
    "../creative_erp.db",
    "dev.db",
    "france.db",
]

print("=" * 80)
print("INSPECCIÓN DE BASES DE DATOS SQLITE")
print("=" * 80)

for db_path in databases:
    full_path = Path(__file__).parent / db_path
    
    if not full_path.exists():
        print(f"\n❌ {db_path} - NO EXISTE")
        continue
    
    print(f"\n📁 {db_path}")
    print(f"   Ruta: {full_path}")
    print(f"   Tamaño: {full_path.stat().st_size / 1024:.2f} KB")
    
    try:
        conn = sqlite3.connect(full_path)
        cursor = conn.cursor()
        
        # Obtener lista de tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        if not tables:
            print("   ⚠️  Base de datos vacía (sin tablas)")
        else:
            print(f"   📊 Tablas encontradas ({len(tables)}):")
            for table in tables:
                table_name = table[0]
                # Contar registros
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"      - {table_name}: {count} registros")
        
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 80)
print("FIN DE LA INSPECCIÓN")
print("=" * 80)
