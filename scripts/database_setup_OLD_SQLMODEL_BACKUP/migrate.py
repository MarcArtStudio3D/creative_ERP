#!/usr/bin/env python3
"""
Script para ejecutar migraciones de base de datos con Alembic.
Uso: python scripts/migrate.py [upgrade|downgrade|current|history]
"""

import os
import subprocess
import sys


def main():
    if len(sys.argv) < 2:
        print(
            "Uso: python scripts/migrate.py [upgrade|downgrade|current|history|revision]"
        )
        print("Ejemplos:")
        print(
            "  python scripts/migrate.py upgrade head    # Aplicar todas las migraciones"
        )
        print("  python scripts/migrate.py current         # Ver migración actual")
        print("  python scripts/migrate.py history         # Ver historial")
        print(
            "  python scripts/migrate.py revision -m 'Nueva migración'  # Crear nueva migración"
        )
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    # Ejecutar alembic con el comando
    cmd = [sys.executable, "-m", "alembic", command] + args
    # cwd debe ser la raíz del proyecto donde está alembic.ini
    # migrate.py está en scripts/database_setup/
    # .. -> scripts/
    # ../.. -> root/
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    result = subprocess.run(cmd, cwd=project_root)

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
