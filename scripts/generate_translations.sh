#!/bin/bash

# Script para generar archivos de traducción de Qt
# Uso: ./scripts/generate_translations.sh

echo "==================================="
echo "Generando archivos de traducción"
echo "==================================="

# Crear directorio de traducciones si no existe
mkdir -p translations

# Verificar si pyside6-lupdate está disponible
if ! command -v pyside6-lupdate &> /dev/null; then
    echo "ERROR: pyside6-lupdate no está instalado."
    echo "Instálalo con: pip install PySide6"
    exit 1
fi

# Generar archivos .ts desde el código fuente
echo ""
echo "Extrayendo textos traducibles..."
# Generar archivos .ts desde el código fuente
echo ""
echo "Extrayendo textos traducibles..."
# Generar lista de archivos a escanear (excluyendo designer_rc.py que causa crash)
FILES=$(find app core modules main.py -name "*.py" -o -name "*.ui" | grep -v "designer_rc.py")

# Escanear archivos
pyside6-lupdate $FILES -ts translations/creative_erp_fr.ts -no-obsolete

echo ""
echo "==================================="
echo "Archivos .ts generados en translations/"
echo "==================================="
echo ""
echo "Próximos pasos:"
echo "1. Edita los archivos .ts con Qt Linguist:"
echo "   linguist translations/creative_erp_es.ts"
echo ""
echo "2. Compila las traducciones con:"
echo "   ./scripts/compile_translations.sh"
echo ""
