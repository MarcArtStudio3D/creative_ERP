#!/bin/bash

# Script para compilar archivos de traducción .ts a .qm
# Uso: ./scripts/compile_translations.sh

echo "==================================="
echo "Compilando traducciones"
echo "==================================="

# Verificar si lrelease está disponible
if ! command -v lrelease &> /dev/null; then
    echo "ERROR: lrelease no está instalado."
    echo "Instálalo con: sudo apt-get install qttools5-dev-tools"
    echo "O en macOS: brew install qt"
    exit 1
fi

# Compilar todos los archivos .ts a .qm
echo ""
echo "Compilando archivos .ts..."

for ts_file in translations/*.ts; do
    if [ -f "$ts_file" ]; then
        echo "Compilando: $ts_file"
        lrelease "$ts_file"
    fi
done

echo ""
echo "==================================="
echo "Archivos .qm generados en translations/"
echo "==================================="
echo ""
echo "Las traducciones están listas para usar en la aplicación."
echo ""
