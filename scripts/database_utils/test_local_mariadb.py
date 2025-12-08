"""
Verificar conexión a MariaDB LOCAL (127.0.0.1)
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import inspect, text

from core.db import get_engine_from_url

# Probar diferentes combinaciones de host
configs = [
    ("127.0.0.1", "mysql+pymysql://root:1234@127.0.0.1:3306/creative_erp"),
    ("localhost", "mysql+pymysql://root:1234@localhost:3306/creative_erp"),
]

for host_name, url in configs:
    print(f"\n{'='*70}")
    print(f"Probando conexión a: {host_name}")
    print(f"{'='*70}")

    try:
        engine = get_engine_from_url(url, echo=False)

        with engine.connect() as connection:
            result = connection.execute(text("SELECT DATABASE(), VERSION();"))
            db, version = result.fetchone()
            print("✅ CONEXIÓN EXITOSA")
            print(f"   Base de datos: {db}")
            print(f"   Versión: {version}")

        # Listar tablas
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print(f"\nTables found: {len(tables)}")

        if tables:
            total_records = 0
            for table in sorted(tables):
                with engine.connect() as connection:
                    result = connection.execute(
                        text(f"SELECT COUNT(*) FROM `{table}`;")
                    )
                    count = result.fetchone()[0]
                    total_records += count
                    print(f"   • {table}: {count} registros")

            print(f"\nTotal records: {total_records}")
            print("\n✅ ¡LA MIGRACIÓN FUE EXITOSA!")
            print("\nNote: To connect with Antares/DBeaver use:")
            print(f"   Host: {host_name}")
            print("   Puerto: 3306")
            print("   Usuario: root")
            print("   Contraseña: 1234")
            print("   Base de datos: creative_erp")
        else:
            print("   ⚠️  No hay tablas (base de datos vacía)")

        engine.dispose()
        break  # Si funciona, no probar más

    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"   Tipo: {type(e).__name__}")

print(f"\n{'='*70}\n")
