#!/usr/bin/env python3
"""
Script para probar la conexión a la nueva base de datos principal
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_main_database():
    """Prueba la conexión a la base de datos principal."""

    print("🔍 Probando conexión a la base de datos principal...")

    try:
        from core.db import get_session, init_main_db
        from core.models import User, BusinessGroup, Empresa

        # Inicializar la base de datos principal
        init_main_db()

        # Probar la conexión obteniendo una sesión
        session = get_session()

        # Probar consultas básicas
        print("   👤 Consultando usuarios...")
        users = session.query(User).all()
        print(f"      Encontrados: {len(users)} usuarios")

        print("   🏢 Consultando grupos empresariales...")
        groups = session.query(BusinessGroup).all()
        print(f"      Encontrados: {len(groups)} grupos")

        print("   🏭 Consultando empresas...")
        empresas = session.query(Empresa).all()
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
    print("🧪 Prueba de Base de Datos Principal")
    print("=" * 40)

    success = test_main_database()
    if success:
        print("\n✅ La base de datos principal está funcionando correctamente")
        print("📝 La refactorización de la arquitectura de base de datos ha sido exitosa!")
    else:
        print("\n❌ Hay problemas con la base de datos principal")
        sys.exit(1)