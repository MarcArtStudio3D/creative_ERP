#!/usr/bin/env python3
"""
Script Python para compilar archivos de traducción .ts a .qm.
Alternativa a compile_translations.sh que funciona en cualquier plataforma.

Uso: python scripts/translations/compile_translations.py
"""

import os
import subprocess
import sys
from pathlib import Path


def main():
    print("=" * 50)
    print("Compilando traducciones")
    print("=" * 50)

    # Obtener el directorio raíz del proyecto (tres niveles arriba: scripts/translations/.. -> repo root)
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)

    translations_dir = project_root / "translations"

    if not translations_dir.exists():
        print(f"Aviso: no se encontró el directorio {translations_dir}")
        # No salimos aún — quizá haya traducciones en módulos

    # Verificar si lrelease está disponible
    try:
        result = subprocess.run([
            "lrelease",
            "-version",
        ], capture_output=True, text=True)
        print(f"Usando: {result.stdout.strip()}")
    except FileNotFoundError:
        print("ERROR: lrelease no está instalado.")
        print("Instálalo con:")
        print("  - Ubuntu/Debian: sudo apt-get install qttools5-dev-tools")
        print("  - macOS: brew install qt")
        print("  - Windows: Instala Qt desde https://www.qt.io/download")
        sys.exit(1)

    # Compilar todos los archivos .ts a .qm
    print("\nCompilando archivos .ts...")

    ts_files = []

    # 1) translations/*.ts
    if translations_dir.exists():
        ts_files.extend(sorted(translations_dir.glob("*.ts")))

    # 2) modules/translations/*.ts (algunos proyectos colocan traducciones en modules/translations)
    modules_translations_dir = project_root / "modules" / "translations"
    if modules_translations_dir.exists():
        ts_files.extend(sorted(modules_translations_dir.glob("*.ts")))

    # 3) modules/*/translations/*.ts (cada módulo puede tener una carpeta translations)
    ts_files.extend(sorted(project_root.glob("modules/*/translations/*.ts")))

    # 4) modules/**/translations/*.ts (recursivo por si hay submódulos)
    ts_files.extend(sorted(project_root.glob("modules/**/translations/*.ts")))

    # 5) Como última opción, buscar recursivamente cualquier .ts bajo project_root
    # (comentado por defecto, descomenta si quieres compilar todas las .ts encontradas)
    # ts_files.extend(sorted(project_root.rglob('*.ts')))

    # Eliminar duplicados conservando orden
    seen = set()
    unique_ts = []
    for p in ts_files:
        try:
            p_abs = p.resolve()
        except Exception:
            p_abs = p
        if p_abs not in seen and str(p).endswith('.ts'):
            seen.add(p_abs)
            unique_ts.append(p)

    ts_files = unique_ts

    if not ts_files:
        print("No se encontraron archivos .ts en las rutas esperadas (búsqueda realizada desde:")
        print(f"  project_root = {project_root}")
        print("Rutas comprobadas:")
        print(f" - {translations_dir}")
        print(f" - {modules_translations_dir}")
        print(" - modules/*/translations/")
        print(" - modules/**/translations/")
        print("Si tus archivos .ts están en otra ruta, indícala o muévalos a una de las anteriores.")
        sys.exit(1)

    print(f"Se encontraron {len(ts_files)} archivo(s) .ts:")
    for f in ts_files:
        print(" -", f)

    # El bucle compila cada .ts en su propio directorio (lrelease coloca el .qm junto al .ts)
    for ts_file in ts_files:
        print(f"Compilando: {ts_file}")
        result = subprocess.run(["lrelease", str(ts_file)], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"ERROR compilando {ts_file}: {result.stderr}")
        else:
            qm_path = ts_file.with_suffix('.qm')
            print(f"  ✓ {qm_path} generado")

    print("\n" + "=" * 50)
    print("Archivos .qm generados")
    print("=" * 50)
    print("\nLas traducciones están listas para usar en la aplicación.")
    print()


if __name__ == "__main__":
    main()
