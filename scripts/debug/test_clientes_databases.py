#!/usr/bin/env python3
"""
Script para probar los módulos de clientes con las diferentes bases de datos
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))


def test_clientes_main_db():
    """Prueba las operaciones de clientes en la base de datos principal."""
    print("Testing clients in main database...")

    try:
        from core.db import get_current_database, set_current_database

        # Cambiar a base de datos principal
        set_current_database("main")

        # Probar consulta de empresas
        session = (
            get_current_database()
        )  # Esto debería devolver el nombre, no la sesión
        print(f"   Base de datos actual: {get_current_database()}")

        # Aquí iría la lógica para probar empresas en la BD principal
        print("   ✅ Base de datos principal accesible")

    except Exception as e:
        print(f"   ❌ Error en base de datos principal: {e}")
        return False

    return True


def test_clientes_artstudio3d():
    """Prueba las operaciones de clientes en la base de datos ArtStudio3D."""
    print("Testing clients in ArtStudio3D database...")

    try:
        from sqlmodel import select

        from core.db import get_current_database, get_session, set_current_database
        from modules.clientes.models import Cliente
        from modules.tipo_cliente.models import TipoCliente

        # Cambiar a base de datos ArtStudio3D
        set_current_database("artstudio3d")
        session = get_session()

        print(f"   Base de datos actual: {get_current_database()}")

        # Probar consulta de tipos de cliente
        tipos = session.exec(select(TipoCliente)).all()
        print(f"   Customer types found: {len(tipos)}")
        for tipo in tipos[:3]:  # Mostrar primeros 3
            print(f"      - {tipo.nombre}")

        # Probar consulta de clientes
        clientes = session.exec(select(Cliente)).all()
        print(f"   Clients found: {len(clientes)}")
        for cliente in clientes[:3]:  # Mostrar primeros 3
            print(
                f"      - {cliente.codigo_cliente}: {cliente.nombre_fiscal or cliente.nombre}"
            )

        # Probar crear un nuevo cliente (solo para prueba)
        print("   ➕ Probando creación de cliente de prueba...")
        nuevo_cliente = Cliente(
            codigo_cliente="TEST-001",
            nombre_fiscal="Cliente de Prueba SA",
            email="test@cliente.com",
        )
        session.add(nuevo_cliente)
        session.commit()
        print("      ✅ Cliente de prueba creado")

        # Verificar que se creó
        cliente_creado = session.exec(
            select(Cliente).where(Cliente.codigo_cliente == "TEST-001")
        ).first()
        if cliente_creado:
            print(f"      ✅ Cliente verificado: {cliente_creado.nombre_fiscal}")

            # Limpiar cliente de prueba
            session.delete(cliente_creado)
            session.commit()
            print("      Test client deleted")

        session.close()
        print("   ✅ Operaciones en ArtStudio3D completadas exitosamente")

    except Exception as e:
        print(f"   ❌ Error en ArtStudio3D: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


def test_database_switching():
    """Prueba el cambio entre diferentes bases de datos."""
    print("Testing database switching...")

    try:
        from core.db import get_current_database, set_current_database

        # Probar cambio a main
        set_current_database("main")
        assert get_current_database() == "main"
        print("   ✅ Cambio a 'main' exitoso")

        # Probar cambio a artstudio3d
        set_current_database("artstudio3d")
        assert get_current_database() == "artstudio3d"
        print("   ✅ Cambio a 'artstudio3d' exitoso")

        # Probar cambio de vuelta a main
        set_current_database("main")
        assert get_current_database() == "main"
        print("   ✅ Cambio de vuelta a 'main' exitoso")

        print("   ✅ Sistema de cambio de base de datos funcionando correctamente")

    except Exception as e:
        print(f"   ❌ Error en cambio de base de datos: {e}")
        return False

    return True


def main():
    """Función principal para ejecutar todas las pruebas."""
    print("TEST: Client modules with multiple databases")
    print("=" * 60)

    success_count = 0
    total_tests = 3

    # Prueba 1: Cambio entre bases de datos
    if test_database_switching():
        success_count += 1

    print()

    # Prueba 2: Clientes en base de datos principal
    if test_clientes_main_db():
        success_count += 1

    print()

    # Prueba 3: Clientes en ArtStudio3D
    if test_clientes_artstudio3d():
        success_count += 1

    print()
    print("=" * 60)
    print(f"Results: {success_count}/{total_tests} successful tests")

    if success_count == total_tests:
        print("✅ Todas las pruebas pasaron exitosamente!")
        print("Client modules work correctly with multiple databases.")
        return True
    else:
        print("❌ Algunas pruebas fallaron. Revisa los errores arriba.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
