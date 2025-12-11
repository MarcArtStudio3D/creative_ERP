"""
Script de prueba para MultiDBManager.
Verifica que el nuevo sistema funciona correctamente.
"""

import logging
logging.basicConfig(level=logging.DEBUG)

print("=" * 60)
print("PRUEBA DE MULTIDBMANAGER")
print("=" * 60)

# 1. Inicializar MultiDBManager
print("\n1️⃣ Inicializando MultiDBManager...")
from core.db_manager import init_db_manager

main_db_config = {
    'type': 'mariadb',
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'admin',
    'password': 'admin123',
    'database': 'creative_erp_main'
}

db_manager = init_db_manager(main_db_config)
print("✅ MultiDBManager inicializado")

# 2. Consultar empresas desde BD principal
print("\n2️⃣ Consultando empresas desde BD principal...")
empresas = db_manager.fetch_all(
    "SELECT id, nombre_fiscal, motor_base_datos FROM empresas WHERE activa = 1",
    use_main=True
)

print(f"✅ Encontradas {len(empresas)} empresas:")
for emp in empresas:
    print(f"   - ID {emp['id']}: {emp['nombre_fiscal']} ({emp['motor_base_datos']})")

# 3. Registrar empresa 1
if empresas:
    empresa = empresas[0]
    print(f"\n3️⃣ Registrando empresa {empresa['id']} ({empresa['nombre_fiscal']})...")

    # Obtener configuración completa de la empresa
    emp_full = db_manager.fetch_one(
        "SELECT * FROM empresas WHERE id = %s",
        (empresa['id'],),
        use_main=True
    )

    db_config = {
        'type': 'mariadb',
        'host': emp_full.get('host_mariadb', 'localhost'),
        'port': emp_full.get('puerto_mariadb', 3306),
        'user': emp_full.get('usuario_mariadb', 'admin'),
        'password': emp_full.get('password_mariadb', 'admin123'),
        'database': emp_full.get('nombre_base_datos_maria_db')
    }

    db_manager.register_empresa(empresa['id'], db_config)
    print(f"✅ Empresa {empresa['id']} registrada")

    # 4. Cambiar a empresa
    print(f"\n4️⃣ Cambiando a empresa {empresa['id']}...")
    db_manager.switch_empresa(empresa['id'])
    print(f"✅ Empresa activa: {empresa['id']}")

    # 5. Consultar clientes de la empresa
    print(f"\n5️⃣ Consultando clientes de la empresa {empresa['id']}...")
    try:
        clientes = db_manager.fetch_all(
            "SELECT id, codigo_cliente, nombre_fiscal FROM clientes LIMIT 5"
        )

        print(f"✅ Encontrados {len(clientes)} clientes (primeros 5):")
        for cliente in clientes:
            print(f"   - {cliente['codigo_cliente']}: {cliente['nombre_fiscal']}")
    except Exception as e:
        print(f"⚠️ Error consultando clientes: {e}")

    # 6. Probar el nuevo ClienteRepository
    print(f"\n6️⃣ Probando ClienteRepository con SQL directo...")
    from modules.clientes.repository_sql import ClienteRepository

    repo = ClienteRepository()
    clientes = repo.obtener_todos(limit=3)

    print(f"✅ ClienteRepository.obtener_todos() retornó {len(clientes)} clientes:")
    for cliente in clientes:
        print(f"   - {cliente['codigo_cliente']}: {cliente['nombre_fiscal']}")

    # 7. Probar obtener un cliente por ID
    if clientes:
        cliente_id = clientes[0]['id']
        print(f"\n7️⃣ Probando obtener cliente por ID {cliente_id}...")
        cliente = repo.obtener_por_id(cliente_id)

        if cliente:
            print(f"✅ Cliente encontrado:")
            print(f"   - Código: {cliente['codigo_cliente']}")
            print(f"   - Nombre: {cliente['nombre_fiscal']}")
            print(f"   - CIF: {cliente.get('cif_nif_siren', 'N/A')}")
            print(f"   - Email: {cliente.get('email', 'N/A')}")

print("\n" + "=" * 60)
print("✅ TODAS LAS PRUEBAS COMPLETADAS")
print("=" * 60)

# Cerrar conexiones
db_manager.close_all()
print("\n🔒 Conexiones cerradas")

