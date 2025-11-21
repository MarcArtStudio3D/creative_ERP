#!/usr/bin/env python3
"""
Script Python para compilar archivos de traducción .ts a .qm.
Alternativa a compile_translations.sh que funciona en cualquier plataforma.

Uso: python scripts/compile_translations.py
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    print("=" * 50)
    print("Compilando traducciones")
    print("=" * 50)
    
    # Obtener el directorio raíz del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    translations_dir = project_root / "translations"
    
    if not translations_dir.exists():
        print(f"ERROR: No se encontró el directorio {translations_dir}")
        sys.exit(1)
    
    # Verificar si lrelease está disponible
    try:
        result = subprocess.run(
            ["lrelease", "-version"],
            capture_output=True,
            text=True
        )
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
    
    ts_files = list(translations_dir.glob("*.ts"))
    
    if not ts_files:
        print(f"No se encontraron archivos .ts en {translations_dir}")
        sys.exit(1)
    
    for ts_file in ts_files:
        print(f"Compilando: {ts_file.name}")
        result = subprocess.run(
            ["lrelease", str(ts_file)],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"ERROR compilando {ts_file.name}: {result.stderr}")
        else:
            print(f"  ✓ {ts_file.stem}.qm generado")
    
    print("\n" + "=" * 50)
    print("Archivos .qm generados en translations/")
    print("=" * 50)
    print("\nLas traducciones están listas para usar en la aplicación.")
    print()

if __name__ == "__main__":
    main()
