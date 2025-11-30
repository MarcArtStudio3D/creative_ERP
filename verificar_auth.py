#!/usr/bin/env python3
"""
Script para verificar que core.auth aplica correctamente los overrides de permisos
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.auth import get_role_permissions, UserRole
from core.module_manager import Permission

def verificar_auth():
    print("=" * 60)
    print("VERIFICACIÓN DE CORE.AUTH")
    print("=" * 60)
    
    # Verificar permisos para ADMIN
    print("\n1. Verificando permisos de ADMIN...")
    perms = get_role_permissions(UserRole.ADMIN)
    
    if "divisiones_almacen" in perms:
        print("   ✅ 'divisiones_almacen' encontrado en permisos de ADMIN")
        print(f"   📋 Permisos: {[p.value for p in perms['divisiones_almacen']]}")
    else:
        print("   ❌ 'divisiones_almacen' NO encontrado en permisos de ADMIN")
        return False
        
    # Verificar permisos para EMPLOYEE
    print("\n2. Verificando permisos de EMPLOYEE...")
    perms = get_role_permissions(UserRole.EMPLOYEE)
    
    if "divisiones_almacen" in perms:
        print("   ✅ 'divisiones_almacen' encontrado en permisos de EMPLOYEE")
        print(f"   📋 Permisos: {[p.value for p in perms['divisiones_almacen']]}")
    else:
        print("   ❌ 'divisiones_almacen' NO encontrado en permisos de EMPLOYEE")
        return False
    
    print("\n" + "=" * 60)
    print("✓ VERIFICACIÓN EXITOSA")
    print("=" * 60)
    print("El sistema de autenticación ahora lee correctamente los permisos")
    print("del archivo role_permissions.json.")
    
    return True

if __name__ == "__main__":
    try:
        exito = verificar_auth()
        sys.exit(0 if exito else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
