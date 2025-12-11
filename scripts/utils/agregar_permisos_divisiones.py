#!/usr/bin/env python3
"""
Script para agregar permisos del módulo divisiones_almacen a todos los roles
"""

import os
import sys

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging

from modules.gestor_modulos.model import RolePermissionsManager


def agregar_permisos_divisiones():
    """Agrega los permisos del módulo divisiones_almacen a todos los roles"""
    logging.getLogger(__name__).info("=" * 60)
    logging.getLogger(__name__).info(
        "AGREGANDO PERMISOS PARA MÓDULO: divisiones_almacen"
    )
    logging.getLogger(__name__).info("=" * 60)

    # Cargar el gestor de permisos
    manager = RolePermissionsManager()

    # Obtener todos los roles
    roles = manager.get_all_roles()

    if not roles:
        logging.getLogger(__name__).warning(
            "\n⚠️  No se encontraron roles en el sistema."
        )
        logging.getLogger(__name__).info("   Creando permisos para roles estándar...")
        roles = ["admin", "sales", "employee"]

    logging.getLogger(__name__).debug(f"\nRoles found: {', '.join(roles)}")

    # Permisos a otorgar (completos para admin, lectura para otros)
    permisos_completos = ["READ", "CREATE", "UPDATE", "DELETE", "ADMIN"]
    permisos_lectura = ["READ"]

    count = 0
    for role in roles:
        # Admin tiene permisos completos, otros solo lectura
        if role.lower() == "admin":
            permisos = permisos_completos
            tipo = "completos"
        else:
            permisos = permisos_lectura
            tipo = "de lectura"

        # Establecer permisos
        manager.set_module_permissions(role, "divisiones_almacen", permisos)
        logging.getLogger(__name__).info(
            f"   ✅ Rol '{role}': permisos {tipo} configurados"
        )
        count += 1

    # Guardar cambios
    if manager.save():
        logging.getLogger(__name__).info(
            f"\n✅ Permisos guardados correctamente para {count} rol(es)"
        )
        logging.getLogger(__name__).info(f"File: {manager.file_path}")

        # Mostrar contenido del módulo en el archivo
        logging.getLogger(__name__).info("\nConfiguration saved:")
        for role in roles:
            perms = manager.get_module_permissions(role, "divisiones_almacen")
            logging.getLogger(__name__).info(f"   {role}: {', '.join(perms)}")

        logging.getLogger(__name__).info("\n" + "=" * 60)
        logging.getLogger(__name__).info("✓ PROCESO COMPLETADO")
        logging.getLogger(__name__).info("=" * 60)
        logging.getLogger(__name__).info("\nYou can now:")
        logging.getLogger(__name__).info("   1. Reiniciar la aplicación")
        logging.getLogger(__name__).info("   2. Seleccionar la categoría 'Almacén'")
        logging.getLogger(__name__).info(
            "   3. Ver y usar el módulo 'Secciones Almacén'"
        )

        return True
    else:
        logging.getLogger(__name__).error("\n❌ Error al guardar los permisos")
        return False


if __name__ == "__main__":
    try:
        exito = agregar_permisos_divisiones()
        sys.exit(0 if exito else 1)
    except Exception:
        logging.getLogger(__name__).exception("\n❌ ERROR agregar_permisos_divisiones")
        sys.exit(1)
