#!/usr/bin/env python3
"""
Script para probar la conexión a la nueva base de datos principal
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))


def test_main_database():
    """Prueba la conexión a la base de datos principal."""

    print("Testing connection to the main database...")

    try:
        from sqlmodel import select

        from core.db import get_session, init_main_db
        from core.models import BusinessGroup, Empresa, User

        # Inicializar la base de datos principal
        init_main_db()

        # Probar la conexión obteniendo una sesión
        session = get_session()

        # Probar consultas básicas
        print("   Querying users...")
        users = session.exec(select(User)).all()
        print(f"      Encontrados: {len(users)} usuarios")

        print("   Querying company groups...")
        groups = session.exec(select(BusinessGroup)).all()
        print(f"      Encontrados: {len(groups)} grupos")

        print("   Querying companies...")
        empresas = session.exec(select(Empresa)).all()
        print(f"      Encontrados: {len(empresas)} empresas")

        session.close()

        print("✅ Conexión exitosa a la base de datos principal!")
        return True

    except Exception as e:
        print(f"❌ Error conectando a la base de datos principal: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("MAIN DATABASE TEST")
    print("=" * 40)

    success = test_main_database()
    if success:
        print("\n✅ La base de datos principal está funcionando correctamente")
        print("Database architecture refactor check: success!")
    else:
        print("\n❌ Hay problemas con la base de datos principal")
        sys.exit(1)
