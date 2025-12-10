#!/usr/bin/env python3
"""
Script de diagnóstico para verificar que el módulo de clientes funciona correctamente.
"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("DIAGNÓSTICO DEL MÓDULO DE CLIENTES")
print("="*60)

# 1. Test de imports
print("\n1. Probando imports...")
try:
    from core.peewee_db import set_database_for_company, get_current_database
    print("  ✓ core.peewee_db")
except Exception as e:
    print(f"  ✗ core.peewee_db: {e}")
    sys.exit(1)

try:
    from modules.clientes.models import Cliente
    print("  ✓ modules.clientes.models")
except Exception as e:
    print(f"  ✗ modules.clientes.models: {e}")
    sys.exit(1)

try:
    from modules.clientes.repository import ClienteRepository
    print("  ✓ modules.clientes.repository")
except Exception as e:
    print(f"  ✗ modules.clientes.repository: {e}")
    sys.exit(1)

try:
    from modules.clientes.controller import ClientesController
    print("  ✓ modules.clientes.controller")
except Exception as e:
    print(f"  ✗ modules.clientes.controller: {e}")
    sys.exit(1)

# 2. Test de configuración de BD
print("\n2. Configurando base de datos...")
try:
    set_database_for_company(1)
    current_db = get_current_database()
    print(f"  ✓ BD actual: {current_db}")
except Exception as e:
    print(f"  ✗ Error configurando BD: {e}")
    sys.exit(1)

# 3. Test de repository
print("\n3. Probando ClienteRepository...")
try:
    # Verificar BD actual antes de consultar
    from core.peewee_db import database_proxy
    print(f"  → BD conectada: {database_proxy.database if database_proxy.obj else 'No inicializada'}")

    repo = ClienteRepository()
    print("  ✓ Repository creado")

    clientes = repo.get_all(limit=5)
    print(f"  ✓ Clientes obtenidos: {len(clientes)}")

    if clientes:
        primer_cliente = clientes[0]
        print(f"  ✓ Primer cliente ID: {primer_cliente.get('id')}")
        print(f"  ✓ Primer cliente nombre: {primer_cliente.get('nombre_fiscal')}")
    else:
        print("  ⚠ No hay clientes en la BD")

except Exception as e:
    print(f"  ✗ Error en repository: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. Test de controller
print("\n4. Probando ClientesController...")
try:
    ctrl = ClientesController()
    print("  ✓ Controller creado")

    ctrl.cargar_clientes()
    print(f"  ✓ Clientes cargados en modelo")

    filas = ctrl.model.rowCount()
    print(f"  ✓ Filas en modelo: {filas}")

    if filas > 0:
        first_item = ctrl.model.item(0, 0)
        if first_item:
            codigo = first_item.text()
            id_cliente = first_item.data()
            print(f"  ✓ Primer cliente código: {codigo}")
            print(f"  ✓ Primer cliente ID: {id_cliente}")
    else:
        print("  ⚠ No hay clientes en el modelo")

except Exception as e:
    print(f"  ✗ Error en controller: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("✅ TODOS LOS TESTS PASARON")
print("="*60)

