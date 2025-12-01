#!/usr/bin/env python3
"""
Script para agregar permisos del módulo divisiones_almacen a todos los roles
"""

import sys
import os
import json

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.gestor_modulos.model import RolePermissionsManager


def agregar_permisos_divisiones():
    """Agrega los permisos del módulo divisiones_almacen a todos los roles"""
    print("=" * 60)
    print("AGREGANDO PERMISOS PARA MÓDULO: divisiones_almacen")
    print("=" * 60)
    
    # Cargar el gestor de permisos
    manager = RolePermissionsManager()
    
    # Obtener todos los roles
    roles = manager.get_all_roles()
    
    if not roles:
        print("\n⚠️  No se encontraron roles en el sistema.")
        print("   Creando permisos para roles estándar...")
        roles = ['admin', 'sales', 'employee']
    
    print(f"\nRoles found: {', '.join(roles)}")
    
    # Permisos a otorgar (completos para admin, lectura para otros)
    permisos_completos = ['READ', 'CREATE', 'UPDATE', 'DELETE', 'ADMIN']
    permisos_lectura = ['READ']
    
    count = 0
    for role in roles:
        # Admin tiene permisos completos, otros solo lectura
        if role.lower() == 'admin':
            permisos = permisos_completos
            tipo = "completos"
        else:
            permisos = permisos_lectura
            tipo = "de lectura"
        
        # Establecer permisos
        manager.set_module_permissions(role, 'divisiones_almacen', permisos)
        print(f"   ✅ Rol '{role}': permisos {tipo} configurados")
        count += 1
    
    # Guardar cambios
    if manager.save():
        print(f"\n✅ Permisos guardados correctamente para {count} rol(es)")
        print(f"File: {manager.file_path}")
        
        # Mostrar contenido del módulo en el archivo
        print("\nConfiguration saved:")
        for role in roles:
            perms = manager.get_module_permissions(role, 'divisiones_almacen')
            print(f"   {role}: {', '.join(perms)}")
        
        print("\n" + "=" * 60)
        print("✓ PROCESO COMPLETADO")
        print("=" * 60)
        print("\nYou can now:")
        print("   1. Reiniciar la aplicación")
        print("   2. Seleccionar la categoría 'Almacén'")
        print("   3. Ver y usar el módulo 'Secciones Almacén'")
        
        return True
    else:
        print("\n❌ Error al guardar los permisos")
        return False


if __name__ == "__main__":
    try:
        exito = agregar_permisos_divisiones()
        sys.exit(0 if exito else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
