#!/usr/bin/env python3
"""
Script para convertir archivos .ui de Qt Designer a código Python.

Uso:
    python convert_ui.py                    # Convierte todos los .ui en app/ui/
    python convert_ui.py archivo.ui         # Convierte un archivo específico
    python convert_ui.py --watch            # Modo watch: reconvierte automáticamente al detectar cambios

Los archivos generados se guardan en app/ui_generated/
"""

import os
import sys
import subprocess
from pathlib import Path
import time

# Directorios del proyecto
UI_DIR = Path(__file__).parent / "app" / "ui"
OUTPUT_DIR = Path(__file__).parent / "app" / "ui_generated"


def convert_ui_file(ui_file: Path) -> bool:
    """
    Convierte un archivo .ui a Python usando pyuic6.
    
    Args:
        ui_file: Ruta al archivo .ui
        
    Returns:
        True si la conversión fue exitosa, False en caso contrario
    """
    # Nombre del archivo de salida: mainwindow.ui -> ui_mainwindow.py
    output_name = f"ui_{ui_file.stem}.py"
    output_file = OUTPUT_DIR / output_name
    
    try:
        # pyuic6 es la herramienta de PyQt6 para convertir .ui a .py
        # Equivalente a uic en Qt/C++
        result = subprocess.run(
            ["pyuic6", str(ui_file), "-o", str(output_file)],
            capture_output=True,
            text=True,
            check=True
        )
        
        print(f"✓ Convertido: {ui_file.name} -> {output_name}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error al convertir {ui_file.name}:")
        print(f"  {e.stderr}")
        return False
    except FileNotFoundError:
        print("✗ Error: pyuic6 no encontrado.")
        print("  Instala PyQt6-tools: pip install PyQt6-tools")
        return False


def convert_all_ui_files():
    """Convierte todos los archivos .ui encontrados en el directorio UI_DIR."""
    if not UI_DIR.exists():
        print(f"✗ Directorio no encontrado: {UI_DIR}")
        return
    
    # Asegurarse de que existe el directorio de salida
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Buscar todos los archivos .ui
    ui_files = list(UI_DIR.glob("*.ui"))
    
    if not ui_files:
        print(f"No se encontraron archivos .ui en {UI_DIR}")
        return
    
    print(f"\nConvirtiendo {len(ui_files)} archivo(s) .ui...\n")
    
    success_count = 0
    for ui_file in ui_files:
        if convert_ui_file(ui_file):
            success_count += 1
    
    print(f"\n{success_count}/{len(ui_files)} archivos convertidos exitosamente")


def watch_mode():
    """
    Modo watch: monitoriza cambios en los archivos .ui y reconvierte automáticamente.
    Útil durante el desarrollo con Qt Designer.
    """
    print("Modo watch activado. Monitorizando cambios en archivos .ui...")
    print("Presiona Ctrl+C para salir\n")
    
    # Guardar timestamps de los archivos
    file_timestamps = {}
    
    try:
        while True:
            if not UI_DIR.exists():
                time.sleep(1)
                continue
                
            ui_files = list(UI_DIR.glob("*.ui"))
            
            for ui_file in ui_files:
                current_mtime = ui_file.stat().st_mtime
                
                # Si el archivo es nuevo o fue modificado
                if ui_file not in file_timestamps or file_timestamps[ui_file] != current_mtime:
                    print(f"\nCambio detectado en {ui_file.name}")
                    convert_ui_file(ui_file)
                    file_timestamps[ui_file] = current_mtime
            
            time.sleep(1)  # Chequear cada segundo
            
    except KeyboardInterrupt:
        print("\n\nWatch mode detenido.")


def main():
    """Función principal del script."""
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--watch" or arg == "-w":
            watch_mode()
        elif arg.endswith(".ui"):
            # Convertir un archivo específico
            ui_file = Path(arg)
            if not ui_file.exists():
                ui_file = UI_DIR / arg
            
            if ui_file.exists():
                convert_ui_file(ui_file)
            else:
                print(f"✗ Archivo no encontrado: {arg}")
        else:
            print(__doc__)
    else:
        # Convertir todos los archivos
        convert_all_ui_files()


if __name__ == "__main__":
    main()
