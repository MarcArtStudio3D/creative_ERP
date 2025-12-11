"""
Test rápido para verificar que la carga de clientes funciona correctamente.
"""

import logging
logging.basicConfig(level=logging.DEBUG)

print("=" * 60)
print("TEST: Carga de clientes en tabla")
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

# 2. Obtener y registrar empresa
print("\n2️⃣ Obteniendo empresa...")
empresa = db_manager.fetch_one(
    "SELECT * FROM empresas WHERE id = 1",
    use_main=True
)

if not empresa:
    print("❌ No se encontró empresa con ID 1")
    exit(1)

print(f"✅ Empresa: {empresa['nombre_fiscal']}")

# 3. Registrar empresa
print(f"\n3️⃣ Registrando empresa {empresa['id']}...")
db_config = {
    'type': 'mariadb',
    'host': empresa.get('host_mariadb', 'localhost'),
    'port': empresa.get('puerto_mariadb', 3306),
    'user': empresa.get('usuario_mariadb', 'admin'),
    'password': empresa.get('password_mariadb', 'admin123'),
    'database': empresa.get('nombre_base_datos_maria_db')
}

try:
    db_manager.register_empresa(empresa['id'], db_config)
    print(f"✅ Empresa {empresa['id']} registrada")
except Exception as e:
    print(f"⚠️ Empresa ya registrada: {e}")

db_manager.switch_empresa(empresa['id'])
print(f"✅ Cambiado a empresa {empresa['id']}")

# 4. Crear controller
print(f"\n4️⃣ Creando ClientesController...")
from modules.clientes.controller import ClientesController
from PySide6.QtCore import QCoreApplication
import sys

# Necesitamos una QApplication para QStandardItemModel
app = QCoreApplication(sys.argv)

controller = ClientesController()
print(f"✅ Controller creado")

# 5. Cargar clientes
print(f"\n5️⃣ Cargando clientes...")
try:
    clientes = controller.get_clientes()
    print(f"✅ Obtenidos {len(clientes)} clientes desde repository")

    # Mostrar primeros 3
    for i, cliente in enumerate(clientes[:3]):
        print(f"   - {cliente.get('codigo_cliente')}: {cliente.get('nombre_fiscal')}")

except Exception as e:
    print(f"❌ Error obteniendo clientes: {e}")
    import traceback
    traceback.print_exc()

# 6. Cargar en el modelo Qt
print(f"\n6️⃣ Cargando clientes en modelo Qt...")
try:
    controller.cargar_clientes()
    print(f"✅ Modelo Qt tiene {controller.model.rowCount()} filas")

    # Mostrar primeras 3 filas
    for i in range(min(3, controller.model.rowCount())):
        codigo = controller.model.item(i, 0).text()
        nif = controller.model.item(i, 1).text()
        nombre = controller.model.item(i, 2).text()
        print(f"   Fila {i}: {codigo} - {nombre}")

except Exception as e:
    print(f"❌ Error cargando en modelo Qt: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ TEST COMPLETADO")
print("=" * 60)

# Cerrar
db_manager.close_all()

