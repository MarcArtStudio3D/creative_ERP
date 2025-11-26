#!/usr/bin/env python3
"""
Script Python para generar archivos de traducción de Qt.
Alternativa a generate_translations.sh que funciona en cualquier plataforma.

Uso: python scripts/generate_translations.py
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    print("=" * 50)
    print("Generando archivos de traducción")
    print("=" * 50)
    
    # Obtener el directorio raíz del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Crear directorio de traducciones si no existe
    translations_dir = project_root / "translations"
    translations_dir.mkdir(exist_ok=True)
    
    # Verificar si pylupdate6 está disponible
    try:
        result = subprocess.run(
            ["pylupdate6", "--version"],
            capture_output=True,
            text=True
        )
        print(f"Usando: {result.stdout.strip()}")
    except FileNotFoundError:
        print("ERROR: pylupdate6 no está instalado.")
        print("Instálalo con: pip install PySide6")
        sys.exit(1)
    
    # Generar archivos .ts desde el código fuente
    print("\nExtrayendo textos traducibles...")
    pro_file = project_root / "creative_erp.pro"
    
    if not pro_file.exists():
        print(f"ERROR: No se encontró el archivo {pro_file}")
        sys.exit(1)
    
    result = subprocess.run(
        ["pylupdate6", str(pro_file)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        sys.exit(1)
    
    print(result.stdout)
    
    print("\n" + "=" * 50)
    print("Archivos .ts generados en translations/")
    print("=" * 50)
    print("\nPróximos pasos:")
    print("1. Edita los archivos .ts con Qt Linguist:")
    print("   linguist translations/creative_erp_es.ts")
    print("\n2. Compila las traducciones con:")
    print("   python scripts/compile_translations.py")
    print()

if __name__ == "__main__":
    main()
