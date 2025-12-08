#!/usr/bin/env python3
"""
Script de migración automática de SQLAlchemy a SQLModel
"""
import os
import re
from pathlib import Path


def migrate_import_section(content):
    """Migra la sección de imports"""
    # Reemplazar imports de SQLAlchemy
    content = re.sub(r"from sqlalchemy import.*\n", "", content)
    content = re.sub(r"from sqlalchemy\.orm import.*\n", "", content)

    # Añadir imports de SQLModel al inicio (después del docstring)
    lines = content.split("\n")
    new_lines = []
    docstring_end = False
    imports_added = False

    for line in lines:
        if '"""' in line or "'''" in line:
            if not docstring_end:
                new_lines.append(line)
                if line.count('"""') == 2 or line.count("'''") == 2:
                    docstring_end = True
                continue
            else:
                docstring_end = True

        if (
            docstring_end
            and not imports_added
            and line.strip()
            and not line.startswith("#")
        ):
            # Añadir imports de SQLModel
            new_lines.append("")
            new_lines.append("from sqlmodel import SQLModel, Field, Relationship")
            new_lines.append("from typing import Optional, List")
            new_lines.append("from datetime import datetime, date")
            new_lines.append("")
            imports_added = True

        new_lines.append(line)

    return "\n".join(new_lines)


def migrate_base_reference(content):
    """Migra referencias a Base"""
    # Eliminar import de Base
    content = re.sub(r"from core\.db import Base\n", "", content)

    # Reemplazar class X(Base): por class X(SQLModel, table=True):
    content = re.sub(
        r"class (\w+)\(Base\):", r"class \1(SQLModel, table=True):", content
    )

    return content


def migrate_mapped_column(content):
    """Migra mapped_column a Field"""
    # Patrón para Mapped[tipo] = mapped_column(...)
    pattern = r"(\w+):\s*Mapped\[([^\]]+)\]\s*=\s*mapped_column\(([^)]+)\)"

    def replace_mapped(match):
        field_name = match.group(1)
        field_type = match.group(2)
        args = match.group(3)

        # Parsear argumentos
        new_args = []

        # Primary key
        if "primary_key=True" in args:
            field_type = (
                f'Optional[{field_type.replace("Optional[", "").replace("]", "")}]'
            )
            new_args.append("default=None")
            new_args.append("primary_key=True")

        # Nullable
        if "nullable=True" in args or "Optional[" in field_type:
            if "Optional[" not in field_type:
                field_type = f"Optional[{field_type}]"

        # Unique
        if "unique=True" in args:
            new_args.append("unique=True")

        # Index
        if "index=True" in args:
            new_args.append("index=True")

        # Default
        default_match = re.search(r"default=([^,)]+)", args)
        if default_match:
            default_val = default_match.group(1)
            new_args.append(f"default={default_val}")

        # String length
        if "String(" in args:
            length_match = re.search(r"String\((\d+)\)", args)
            if length_match:
                new_args.append(f"max_length={length_match.group(1)}")

        # Foreign key
        if "ForeignKey(" in args:
            fk_match = re.search(r"ForeignKey\(['\"]([^'\"]+)['\"]\)", args)
            if fk_match:
                new_args.append(f'foreign_key="{fk_match.group(1)}"')

        field_str = f'{field_name}: {field_type} = Field({", ".join(new_args)})'
        return field_str

    content = re.sub(pattern, replace_mapped, content)
    return content


def migrate_relationship(content):
    """Migra relationship a Relationship"""
    content = re.sub(r"relationship\(", "Relationship(", content)
    content = re.sub(r"backref=", "back_populates=", content)
    return content


def migrate_file(file_path):
    """Migra un archivo completo"""
    print(f"Migrando {file_path}...")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Hacer backup
    backup_path = str(file_path) + ".sqlalchemy_backup"
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Backup creado: {backup_path}")

    # Aplicar migraciones
    content = migrate_base_reference(content)
    content = migrate_mapped_column(content)
    content = migrate_relationship(content)
    content = migrate_import_section(content)

    # Guardar archivo migrado
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("  ✓ Migrado exitosamente")


def find_model_files(base_path):
    """Encuentra todos los archivos models.py en el proyecto"""
    model_files = []
    base = Path(base_path)

    # Buscar en modules/
    modules_path = base / "modules"
    if modules_path.exists():
        for models_file in modules_path.rglob("models.py"):
            model_files.append(str(models_file))

    return model_files


def main():
    import sys

    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = os.getcwd()

    print("=" * 60)
    print("MIGRACIÓN AUTOMÁTICA: SQLAlchemy -> SQLModel")
    print("=" * 60)
    print()

    # Encontrar archivos
    model_files = find_model_files(base_path)

    print(f"Archivos encontrados: {len(model_files)}")
    for f in model_files:
        print(f"  - {f}")
    print()

    # Confirmar
    response = input("¿Desea continuar con la migración? (s/n): ")
    if response.lower() != "s":
        print("Migración cancelada.")
        return

    # Migrar cada archivo
    for model_file in model_files:
        try:
            migrate_file(model_file)
        except Exception as e:
            print(f"  ✗ Error migrando {model_file}: {e}")

    print()
    print("=" * 60)
    print("MIGRACIÓN COMPLETADA")
    print("=" * 60)
    print("Revise los archivos migrados y ejecute los tests.")
    print("Los backups están disponibles con extensión .sqlalchemy_backup")


if __name__ == "__main__":
    main()
