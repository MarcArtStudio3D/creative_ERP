#!/usr/bin/env python3
"""
Ejemplo de uso de múltiples bases de datos en la aplicación Creative ERP

Este script demuestra cómo alternar entre diferentes bases de datos
y realizar operaciones específicas según el contexto.
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def ejemplo_uso_basico():
    """Ejemplo básico de cambio entre bases de datos."""
    print("📚 Ejemplo Básico: Cambio entre Bases de Datos")
    print("-" * 50)

    from core.db import set_current_database, get_current_database, get_session

    # Cambiar a base de datos principal para operaciones globales
    print("1. Usando base de datos principal para datos globales:")
    set_current_database('main')
    print(f"   Base actual: {get_current_database()}")

    # Aquí irían operaciones con usuarios, empresas, grupos empresariales
    session_main = get_session()
    # Ejemplo: consultar empresas
    print("   ✅ Listo para operaciones globales (usuarios, empresas, grupos)")

    # Cambiar a base de datos ArtStudio3D para operaciones específicas
    print("\n2. Usando base de datos ArtStudio3D para clientes:")
    set_current_database('artstudio3d')
    print(f"   Base actual: {get_current_database()}")

    # Aquí irían operaciones con clientes específicos de ArtStudio3D
    session_artstudio = get_session()
    # Ejemplo: consultar clientes
    print("   ✅ Listo para operaciones de clientes")

    session_main.close()
    session_artstudio.close()

def ejemplo_operaciones_clientes():
    """Ejemplo de operaciones CRUD con clientes en ArtStudio3D."""
    print("\n📚 Ejemplo Avanzado: Operaciones CRUD con Clientes")
    print("-" * 55)

    from core.db import set_current_database, get_session
    from modules.clientes.models import Cliente
    from modules.tipo_cliente.models import TipoCliente

    # Cambiar a ArtStudio3D
    set_current_database('artstudio3d')
    session = get_session()

    try:
        print("1. 📊 Consultando tipos de cliente:")
        tipos = session.query(TipoCliente).all()
        for tipo in tipos:
            print(f"   - {tipo.nombre}: {tipo.desc or 'Sin descripción'}")

        print("\n2. 👥 Consultando clientes activos:")
        clientes = session.query(Cliente).filter(Cliente.bloqueado == False).limit(5).all()
        for cliente in clientes:
            nombre = cliente.nombre_fiscal or cliente.nombre_comercial or cliente.nombre or "Sin nombre"
            print(f"   - {cliente.codigo_cliente}: {nombre}")

        print("\n3. ➕ Creando un nuevo cliente:")
        nuevo_cliente = Cliente(
            codigo_cliente="EJEMPLO-001",
            nombre_fiscal="Empresa de Ejemplo SL",
            nombre_comercial="Ejemplo Corp",
            cif_nif_siren="B12345678",
            email="contacto@ejemplo.com",
            telefono1="912345678",
            direccion1="Calle Ejemplo 123",
            cp="28001",
            poblacion="Madrid",
            provincia="Madrid",
            id_pais="España"
        )

        session.add(nuevo_cliente)
        session.commit()
        print("   ✅ Cliente creado exitosamente")

        # Verificar creación
        cliente_verificado = session.query(Cliente).filter_by(codigo_cliente="EJEMPLO-001").first()
        if cliente_verificado:
            print(f"   ✅ Verificado: {cliente_verificado.nombre_fiscal}")

        print("\n4. 🗑️  Limpiando datos de ejemplo:")
        session.delete(cliente_verificado)
        session.commit()
        print("   ✅ Cliente de ejemplo eliminado")

    except Exception as e:
        print(f"❌ Error en operaciones: {e}")
        session.rollback()
    finally:
        session.close()

def ejemplo_contexto_manager():
    """Ejemplo usando un context manager para cambio automático de BD."""
    print("\n📚 Ejemplo Avanzado: Context Manager para Bases de Datos")
    print("-" * 58)

    from contextlib import contextmanager
    from core.db import set_current_database, get_current_database

    @contextmanager
    def usar_base_datos(db_name):
        """Context manager para cambiar temporalmente de base de datos."""
        db_actual = get_current_database()
        try:
            set_current_database(db_name)
            print(f"   🔄 Cambiado a base de datos: {db_name}")
            yield
        finally:
            set_current_database(db_actual)
            print(f"   🔄 Restaurado a base de datos: {db_actual}")

    # Usar context manager
    print("1. Operaciones en base principal:")
    with usar_base_datos('main'):
        # Aquí irían operaciones con datos globales
        print("   ✅ Operaciones globales completadas")

    print("\n2. Operaciones en ArtStudio3D:")
    with usar_base_datos('artstudio3d'):
        # Aquí irían operaciones con clientes
        print("   ✅ Operaciones de clientes completadas")

def mostrar_configuracion():
    """Muestra la configuración actual de bases de datos."""
    print("\n📚 Configuración de Bases de Datos")
    print("-" * 40)

    from core.db import DATABASE_CONFIGS, DEFAULT_DB

    print(f"Base de datos por defecto: {DEFAULT_DB}")
    print("\nConfiguraciones disponibles:")
    for name, url in DATABASE_CONFIGS.items():
        # Ocultar credenciales en la URL para seguridad
        display_url = url.replace('admin:admin123@', '***:***@')
        print(f"  {name}: {display_url}")

    print("\nPara cambiar la base por defecto, establece la variable de entorno:")
    print("  export CREATIVE_ERP_DEFAULT_DB=artstudio3d")

def main():
    """Función principal del ejemplo."""
    print("🎨 Creative ERP - Ejemplo de Uso de Múltiples Bases de Datos")
    print("=" * 65)
    print("Este ejemplo muestra cómo trabajar con diferentes bases de datos")
    print("en la aplicación Creative ERP.\n")

    # Mostrar configuración
    mostrar_configuracion()

    # Ejecutar ejemplos
    ejemplo_uso_basico()
    ejemplo_operaciones_clientes()
    ejemplo_contexto_manager()

    print("\n" + "=" * 65)
    print("✅ Ejemplos completados exitosamente!")
    print("\n💡 Consejos de uso:")
    print("   • Usa set_current_database() para cambiar entre bases de datos")
    print("   • Cada base de datos tiene sus propias tablas y datos")
    print("   • Las sesiones son independientes por base de datos")
    print("   • Recuerda cerrar las sesiones después de usarlas")

if __name__ == "__main__":
    main()