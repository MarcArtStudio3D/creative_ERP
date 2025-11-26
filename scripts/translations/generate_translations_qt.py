#!/usr/bin/env python3
"""
Script para generar archivos de traducción usando pylupdate6 (oficial de Qt).
Este script extrae strings tanto de archivos .py como de archivos .ui

Uso: python scripts/generate_translations_qt.py
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    print("=" * 60)
    print("Generando archivos de traducción con pylupdate6")
    print("=" * 60)
    
    # Obtener el directorio raíz del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Crear directorio de traducciones si no existe
    translations_dir = project_root / "translations"
    translations_dir.mkdir(exist_ok=True)
    
    # Verificar si pylupdate6 está disponible
    pylupdate_cmd = None
    for cmd in ['pylupdate6', 'pyside6-lupdate']:
        try:
            result = subprocess.run(
                [cmd, "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                pylupdate_cmd = cmd
                print(f"✓ Usando: {cmd}")
                break
        except FileNotFoundError:
            continue
    
    if not pylupdate_cmd:
        print("\n⚠️  pylupdate6 no está disponible en el PATH.")
        print("\nOpciones:")
        print("1. Buscar pylupdate6 en la instalación de PySide6:")
        
        # Intentar encontrar pylupdate6 en site-packages
        try:
            import PySide6
            pyside_path = Path(PySide6.__file__).parent
            possible_paths = [
                pyside_path / "lupdate",
                pyside_path / "pylupdate6",
                pyside_path / "pyside6-lupdate",
            ]
            
            for path in possible_paths:
                if path.exists():
                    pylupdate_cmd = str(path)
                    print(f"   ✓ Encontrado: {pylupdate_cmd}")
                    break
        except ImportError:
            pass
        
        if not pylupdate_cmd:
            print("\n2. Usar el script alternativo (extract_all_strings.py):")
            print("   python scripts/extract_all_strings.py")
            print("\nNota: El script alternativo extrae strings de .py pero no de .ui")
            return 1
    
    # Generar archivos .ts desde el código fuente
    print("\nExtrayendo textos traducibles del archivo .pro...")
    pro_file = project_root / "creative_erp.pro"
    
    if not pro_file.exists():
        print(f"ERROR: No se encontró el archivo {pro_file}")
        return 1
    
    # Ejecutar pylupdate6
    result = subprocess.run(
        [pylupdate_cmd, "-verbose", str(pro_file)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        return 1
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    print("\n" + "=" * 60)
    print("Archivos .ts generados en translations/")
    print("=" * 60)
    
    # Contar strings en cada archivo
    for ts_file in translations_dir.glob("*.ts"):
        try:
            with open(ts_file, 'r', encoding='utf-8') as f:
                content = f.read()
                message_count = content.count('<message>')
                print(f"  {ts_file.name}: {message_count} mensajes")
        except Exception as e:
            print(f"  {ts_file.name}: Error al contar - {e}")
    
    print("\nPróximos pasos:")
    print("1. Edita los archivos .ts con Qt Linguist:")
    print("   linguist translations/creative_erp_fr.ts")
    print("\n2. O edítalos manualmente con cualquier editor de texto")
    print("\n3. Compila las traducciones con:")
    print("   python scripts/compile_translations.py")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
