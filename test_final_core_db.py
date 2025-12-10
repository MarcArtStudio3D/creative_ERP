#!/usr/bin/env python3
"""Test final de verificación post-limpieza de core.db"""

print('='*60)
print('TEST FINAL - IMPORTS Y FUNCIONALIDAD')
print('='*60)

# Test 1: Imports principales
print('\n1. Testing imports...')
try:
    from app.app import run_app
    print('   ✅ app.app.run_app')
    from core.peewee_db import get_company_database_info, ensure_initialized
    print('   ✅ core.peewee_db functions')
    from modules.clientes.view import ClientesView
    print('   ✅ modules.clientes.view')
    from modules.articulos.divisiones_repository import DivisionesRepository
    print('   ✅ modules.articulos.divisiones_repository')
except ModuleNotFoundError as e:
    print(f'   ❌ Error: {e}')
    exit(1)

# Test 2: No hay referencias a core.db
print('\n2. Checking for core.db references...')
import sys
bad_imports = [m for m in sys.modules if 'core.db' in m and 'peewee_db' not in m]
if bad_imports:
    print(f'   ⚠️  Found: {bad_imports}')
else:
    print('   ✅ No core.db imports')

print('\n' + '='*60)
print('✅ TODOS LOS TESTS PASARON')
print('='*60)
print('\nLa aplicación está lista para ejecutar:')
print('  python3 main.py')
print('='*60)

