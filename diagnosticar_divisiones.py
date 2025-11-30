#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la configuración del módulo divisiones_almacen
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.module_manager import ModuleManager, Permission, AVAILABLE_MODULES, ModuleCategory
from modules.gestor_modulos.model import RolePermissionsManager


def diagnosticar():
    print("=" * 70)
    print("DIAGNÓSTICO DEL MÓDULO divisiones_almacen")
    print("=" * 70)
    
    # 1. Verificar que el módulo existe en AVAILABLE_MODULES
    print("\n1️⃣  Verificando registro en AVAILABLE_MODULES...")
    if 'divisiones_almacen' in AVAILABLE_MODULES:
        mod = AVAILABLE_MODULES['divisiones_almacen']
        print(f"   ✅ Módulo encontrado:")
        print(f"      - ID: {mod.id}")
        print(f"      - Nombre: {mod.name}")
        print(f"      - Descripción: {mod.description}")
        print(f"      - Icono: {mod.icon}")
        print(f"      - Categoría: {mod.category}")
        print(f"      - Permisos requeridos: {[p.value for p in mod.required_permissions]}")
        print(f"      - Habilitado: {mod.enabled}")
    else:
        print("   ❌ Módulo NO encontrado en AVAILABLE_MODULES")
        return False
    
    # 2. Verificar permisos en role_permissions.json
    print("\n2️⃣  Verificando permisos en role_permissions.json...")
    rpm = RolePermissionsManager()
    roles = rpm.get_all_roles()
    print(f"   📋 Roles encontrados: {', '.join(roles)}")
    
    for role in roles:
        perms = rpm.get_module_permissions(role, 'divisiones_almacen')
        if perms:
            print(f"   ✅ Rol '{role}': {', '.join(perms)}")
        else:
            print(f"   ⚠️  Rol '{role}': Sin permisos")
    
    # 3. Verificar disponibilidad para admin
    print("\n3️⃣  Verificando disponibilidad para rol admin...")
    mm = ModuleManager()
    
    # Simular permisos de admin (todos los módulos con todos los permisos)
    admin_perms = {}
    for mod_id in AVAILABLE_MODULES.keys():
        admin_perms[mod_id] = [Permission.ADMIN, Permission.READ, Permission.CREATE, 
                              Permission.UPDATE, Permission.DELETE]
    
    available = mm.get_available_modules(admin_perms)
    available_ids = [m.id for m in available]
    
    if 'divisiones_almacen' in available_ids:
        print("   ✅ Módulo disponible para admin")
    else:
        print("   ❌ Módulo NO disponible para admin")
        print(f"   📋 Módulos disponibles: {', '.join(available_ids[:10])}...")
    
    # 4. Verificar módulos de ALMACEN
    print("\n4️⃣  Verificando módulos de la categoría ALMACEN...")
    almacen_modules = [m for m in available if m.category == ModuleCategory.ALMACEN]
    print(f"   📦 Módulos ALMACEN encontrados: {len(almacen_modules)}")
    for mod in almacen_modules:
        print(f"      - {mod.icon} {mod.name} ({mod.id})")
    
    # 5. Verificar que el archivo de vista existe
    print("\n5️⃣  Verificando archivos del módulo...")
    view_path = os.path.join(os.path.dirname(__file__), '..', 'modules', 'divisiones_almacen', 'view.py')
    if os.path.exists(view_path):
        print(f"   ✅ Archivo view.py existe: {view_path}")
    else:
        print(f"   ❌ Archivo view.py NO existe: {view_path}")
    
    init_path = os.path.join(os.path.dirname(__file__), '..', 'modules', 'divisiones_almacen', '__init__.py')
    if os.path.exists(init_path):
        print(f"   ✅ Archivo __init__.py existe: {init_path}")
    else:
        print(f"   ❌ Archivo __init__.py NO existe: {init_path}")
    
    # 6. Intentar importar el módulo
    print("\n6️⃣  Intentando importar el módulo...")
    try:
        from modules.divisiones_almacen.view import DivisionesAlmacenView
        print("   ✅ Importación exitosa de DivisionesAlmacenView")
    except Exception as e:
        print(f"   ❌ Error al importar: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("✓ DIAGNÓSTICO COMPLETADO")
    print("=" * 70)
    
    print("\n💡 SOLUCIÓN:")
    print("   1. Asegúrate de haber reiniciado completamente la aplicación")
    print("   2. Verifica que iniciaste sesión con el usuario 'admin'")
    print("   3. Ve a la categoría 'Almacén' en la barra lateral")
    print("   4. Deberías ver el botón '📁 Secciones Almacén'")
    
    return True


if __name__ == "__main__":
    try:
        diagnosticar()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
