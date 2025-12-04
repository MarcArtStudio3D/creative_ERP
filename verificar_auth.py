#!/usr/bin/env python3
"""
Script para verificar que core.auth aplica correctamente los overrides de permisos
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.auth import get_role_permissions, UserRole
import logging
from core.module_manager import Permission

def verificar_auth():
    logging.getLogger(__name__).info("=" * 60)
    logging.getLogger(__name__).info("VERIFICACIÓN DE CORE.AUTH")
    logging.getLogger(__name__).info("=" * 60)
    
    # Verificar permisos para ADMIN
    logging.getLogger(__name__).info("\n1. Verificando permisos de ADMIN...")
    perms = get_role_permissions(UserRole.ADMIN)
    
    if "divisiones_almacen" in perms:
        logging.getLogger(__name__).info("   ✅ 'divisiones_almacen' encontrado en permisos de ADMIN")
        logging.getLogger(__name__).debug(f"   Permissions: {[p.value for p in perms['divisiones_almacen']]}")
    else:
        logging.getLogger(__name__).warning("   ❌ 'divisiones_almacen' NO encontrado en permisos de ADMIN")
        return False
        
    # Verificar permisos para EMPLOYEE
    logging.getLogger(__name__).info("\n2. Verificando permisos de EMPLOYEE...")
    perms = get_role_permissions(UserRole.EMPLOYEE)
    
    if "divisiones_almacen" in perms:
        logging.getLogger(__name__).info("   ✅ 'divisiones_almacen' encontrado en permisos de EMPLOYEE")
        logging.getLogger(__name__).debug(f"   Permissions: {[p.value for p in perms['divisiones_almacen']]}")
    else:
        logging.getLogger(__name__).warning("   ❌ 'divisiones_almacen' NO encontrado en permisos de EMPLOYEE")
        return False
    
    logging.getLogger(__name__).info("\n" + "=" * 60)
    logging.getLogger(__name__).info("✓ VERIFICACIÓN EXITOSA")
    logging.getLogger(__name__).info("=" * 60)
    logging.getLogger(__name__).info("El sistema de autenticación ahora lee correctamente los permisos")
    logging.getLogger(__name__).info("del archivo role_permissions.json.")
    
    return True

if __name__ == "__main__":
    try:
        exito = verificar_auth()
        sys.exit(0 if exito else 1)
    except Exception:
        logging.getLogger(__name__).exception("❌ ERROR verificar_auth")
        sys.exit(1)
