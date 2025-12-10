#!/usr/bin/env python3
"""Script simple para verificar que la aplicación se importa correctamente."""

import sys
import os

# Añadir directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*60)
print("VERIFICACIÓN POST-CORRECCIÓN")
print("="*60)

# Test 1: Import de app.app
print("\n1. Intentando importar app.app...")
try:
    from app.app import run_app
    print("   ✓ app.app importado correctamente")
except ModuleNotFoundError as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"   ✗ Error inesperado: {e}")
    sys.exit(1)

# Test 2: Verificar que no hay referencias a core.db
print("\n2. Verificando que no hay referencias a core.db...")
import app.app
import inspect
source = inspect.getsource(app.app)
if 'core.db' in source:
    print("   ⚠ Todavía hay referencias a core.db")
else:
    print("   ✓ Sin referencias a core.db")

# Test 3: Verificar imports de Peewee
print("\n3. Verificando imports de Peewee...")
try:
    from core.peewee_db import database_proxy, ensure_initialized
    print("   ✓ core.peewee_db funciona correctamente")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*60)
print("✅ APLICACIÓN LISTA PARA EJECUTAR")
print("="*60)

