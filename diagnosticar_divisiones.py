#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la configuración del módulo divisiones_almacen
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.module_manager import ModuleManager, Permission, AVAILABLE_MODULES, ModuleCategory
import logging
from modules.gestor_modulos.model import RolePermissionsManager


def diagnosticar():
    logging.getLogger(__name__).info("=" * 70)
    logging.getLogger(__name__).info("DIAGNÓSTICO DEL MÓDULO divisiones_almacen")
    logging.getLogger(__name__).info("=" * 70)
    
    # 1. Verificar que el módulo existe en AVAILABLE_MODULES
    logging.getLogger(__name__).info("\n1️⃣  Verificando registro en AVAILABLE_MODULES...")
    if 'divisiones_almacen' in AVAILABLE_MODULES:
        mod = AVAILABLE_MODULES['divisiones_almacen']
        logging.getLogger(__name__).info("   ✅ Módulo encontrado:")
        logging.getLogger(__name__).debug(f"      - ID: {mod.id}")
        logging.getLogger(__name__).debug(f"      - Nombre: {mod.name}")
        logging.getLogger(__name__).debug(f"      - Descripción: {mod.description}")
        logging.getLogger(__name__).debug(f"      - Icono: {mod.icon}")
        logging.getLogger(__name__).debug(f"      - Categoría: {mod.category}")
        logging.getLogger(__name__).debug(f"      - Permisos requeridos: {[p.value for p in mod.required_permissions]}")
        logging.getLogger(__name__).debug(f"      - Habilitado: {mod.enabled}")
    else:
        logging.getLogger(__name__).warning("   ❌ Módulo NO encontrado en AVAILABLE_MODULES")
        return False
    
    # 2. Verificar permisos en role_permissions.json
    logging.getLogger(__name__).info("\n2️⃣  Verificando permisos en role_permissions.json...")
    rpm = RolePermissionsManager()
    roles = rpm.get_all_roles()
    logging.getLogger(__name__).debug(f"   Roles found: {', '.join(roles)}")
    
    for role in roles:
        perms = rpm.get_module_permissions(role, 'divisiones_almacen')
        if perms:
            logging.getLogger(__name__).info(f"   ✅ Rol '{role}': {', '.join(perms)}")
        else:
            logging.getLogger(__name__).warning(f"   ⚠️  Rol '{role}': Sin permisos")
    
    # 3. Verificar disponibilidad para admin
    logging.getLogger(__name__).info("\n3️⃣  Verificando disponibilidad para rol admin...")
    mm = ModuleManager()
    
    # Simular permisos de admin (todos los módulos con todos los permisos)
    admin_perms = {}
    for mod_id in AVAILABLE_MODULES.keys():
        admin_perms[mod_id] = [Permission.ADMIN, Permission.READ, Permission.CREATE, 
                              Permission.UPDATE, Permission.DELETE]
    
    available = mm.get_available_modules(admin_perms)
    available_ids = [m.id for m in available]
    
    if 'divisiones_almacen' in available_ids:
        logging.getLogger(__name__).info("   ✅ Módulo disponible para admin")
    else:
        logging.getLogger(__name__).warning("   ❌ Módulo NO disponible para admin")
        logging.getLogger(__name__).debug(f"   Available modules: {', '.join(available_ids[:10])}...")
    
    # 4. Verificar módulos de ALMACEN
    logging.getLogger(__name__).info("\n4️⃣  Verificando módulos de la categoría ALMACEN...")
    almacen_modules = [m for m in available if m.category == ModuleCategory.ALMACEN]
    logging.getLogger(__name__).debug(f"   Almacen modules found: {len(almacen_modules)}")
    for mod in almacen_modules:
            logging.getLogger(__name__).debug(f"      - {mod.icon} {mod.name} ({mod.id})")
    
    # 5. Verificar que el archivo de vista existe
    logging.getLogger(__name__).info("\n5️⃣  Verificando archivos del módulo...")
    view_path = os.path.join(os.path.dirname(__file__), '..', 'modules', 'divisiones_almacen', 'view.py')
    if os.path.exists(view_path):
        logging.getLogger(__name__).info(f"   ✅ Archivo view.py existe: {view_path}")
    else:
        logging.getLogger(__name__).warning(f"   ❌ Archivo view.py NO existe: {view_path}")
    
    init_path = os.path.join(os.path.dirname(__file__), '..', 'modules', 'divisiones_almacen', '__init__.py')
    if os.path.exists(init_path):
        logging.getLogger(__name__).info(f"   ✅ Archivo __init__.py existe: {init_path}")
    else:
        logging.getLogger(__name__).warning(f"   ❌ Archivo __init__.py NO existe: {init_path}")
    
    # 6. Intentar importar el módulo
    logging.getLogger(__name__).info("\n6️⃣  Intentando importar el módulo...")
    try:
        from modules.divisiones_almacen.view import DivisionesAlmacenView
        logging.getLogger(__name__).info("   ✅ Importación exitosa de DivisionesAlmacenView")
    except Exception:
        logging.getLogger(__name__).exception("   ❌ Error al importar DivisionesAlmacenView")
    
    logging.getLogger(__name__).info("\n" + "=" * 70)
    logging.getLogger(__name__).info("✓ DIAGNÓSTICO COMPLETADO")
    logging.getLogger(__name__).info("=" * 70)
    
    logging.getLogger(__name__).info("\nSOLUTION:")
    logging.getLogger(__name__).info("   1. Asegúrate de haber reiniciado completamente la aplicación")
    logging.getLogger(__name__).info("   2. Verifica que iniciaste sesión con el usuario 'admin'")
    logging.getLogger(__name__).info("   3. Ve a la categoría 'Almacén' en la barra lateral")
    logging.getLogger(__name__).info("   4. You should see the 'Secciones Almacén' button")
    
    return True


if __name__ == "__main__":
    try:
        diagnosticar()
    except Exception:
        logging.getLogger(__name__).exception("❌ ERROR diagnosticar_divisiones")
        sys.exit(1)
