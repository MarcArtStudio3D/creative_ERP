#!/usr/bin/env python3
"""
Script para probar la conexión a la base de datos 'ArtStudio3D'
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_artstudio3d_database():
    """Prueba la conexión a la base de datos ArtStudio3D."""

    print("🎨 Probando conexión a la base de datos 'ArtStudio3D'...")

    try:
        # Configurar la conexión a ArtStudio3D
        artstudio_db_url = os.environ.get('ARTSTUDIO3D_DB',
                                         'mysql+pymysql://admin:admin123@127.0.0.1:3306/artstudio3d')

        from sqlalchemy import create_engine, text
        from sqlalchemy.orm import sessionmaker

        # Crear motor para ArtStudio3D
        artstudio_engine = create_engine(artstudio_db_url)

        # Probar consultas básicas
        with artstudio_engine.connect() as conn:
            print("   🏷️  Consultando tipos de cliente...")
            result = conn.execute(text("SELECT COUNT(*) FROM tipocliente_def"))
            row = result.fetchone()
            tipos_count = row[0] if row else 0
            print(f"      Encontrados: {tipos_count} tipos de cliente")

            print("   🏷️  Consultando subtipos de cliente...")
            result = conn.execute(text("SELECT COUNT(*) FROM tiposubcliente_def"))
            row = result.fetchone()
            subtipos_count = row[0] if row else 0
            print(f"      Encontrados: {subtipos_count} subtipos de cliente")

            print("   👥 Consultando clientes...")
            result = conn.execute(text("SELECT COUNT(*) FROM clientes"))
            row = result.fetchone()
            clientes_count = row[0] if row else 0
            print(f"      Encontrados: {clientes_count} clientes")

            print("   📍 Consultando direcciones alternativas...")
            result = conn.execute(text("SELECT COUNT(*) FROM direcciones_alternativas"))
            row = result.fetchone()
            direcciones_count = row[0] if row else 0
            print(f"      Encontrados: {direcciones_count} direcciones alternativas")

            # Mostrar algunos ejemplos
            if tipos_count > 0:
                print("\n   📋 Ejemplos de tipos de cliente:")
                result = conn.execute(text("SELECT id, nombre FROM tipocliente_def LIMIT 3"))
                for row in result:
                    print(f"      - {row[0]}: {row[1]}")

            if clientes_count > 0:
                print("\n   📋 Ejemplos de clientes:")
                result = conn.execute(text("SELECT id, codigo_cliente, nombre_fiscal FROM clientes LIMIT 3"))
                for row in result:
                    print(f"      - {row[1]}: {row[2] or 'Sin nombre fiscal'}")

        print("✅ Conexión exitosa a la base de datos 'ArtStudio3D'!")
        return True

    except Exception as e:
        print(f"❌ Error conectando a la base de datos 'ArtStudio3D': {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Prueba de Base de Datos ArtStudio3D")
    print("=" * 40)

    success = test_artstudio3d_database()
    if success:
        print("\n✅ La base de datos 'ArtStudio3D' está funcionando correctamente")
        print("📝 La migración de las tablas específicas ha sido exitosa!")
    else:
        print("\n❌ Hay problemas con la base de datos 'ArtStudio3D'")
        sys.exit(1)