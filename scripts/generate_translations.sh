#!/bin/bash

# Script para generar archivos de traducción de Qt
# Uso: ./scripts/generate_translations.sh

echo "==================================="
echo "Generando archivos de traducción"
echo "==================================="

# Crear directorio de traducciones si no existe
mkdir -p translations

# Verificar si pylupdate6 está disponible
if ! command -v pylupdate6 &> /dev/null; then
    echo "ERROR: pylupdate6 no está instalado."
    echo "Instálalo con: pip install PySide6"
    exit 1
fi

# Generar archivos .ts desde el código fuente
echo ""
echo "Extrayendo textos traducibles..."
pylupdate6 creative_erp.pro

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
