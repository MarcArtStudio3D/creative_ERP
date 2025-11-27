#!/usr/bin/env bash
set -euo pipefail

# Compile UI (.ui) and resource (.qrc) files and patch imports to ensure designer_rc is importable
# Also fixes Qt constants for better Pylance compatibility
# Usage: ./scripts/compile_ui.sh

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
UI_DIR="$ROOT_DIR/app/ui"
MODULES_DIR="$ROOT_DIR/modules"
VENV_BIN="$ROOT_DIR/.venv/bin"
SCRIPTS_DIR="$ROOT_DIR/scripts"

PYUIC="${VENV_BIN}/pyside6-uic"
PYRCC="${VENV_BIN}/pyside6-rcc"
PYTHON="${VENV_BIN}/python"

if [ ! -x "$PYUIC" ]; then
    PYUIC=$(command -v pyside6-uic || true)
fi
if [ ! -x "$PYRCC" ]; then
    PYRCC=$(command -v pyside6-rcc || true)
fi
if [ ! -x "$PYTHON" ]; then
    PYTHON=$(command -v python3 || true)
fi

if [ -z "$PYUIC" ] || [ -z "$PYRCC" ] || [ -z "$PYTHON" ]; then
    echo "Error: pyside6-uic, pyside6-rcc, or python not found. Activate your virtualenv or install PySide6." >&2
    exit 1
fi

echo "Using pyside6-uic: $PYUIC"
echo "Using pyside6-rcc: $PYRCC"
echo "Using python: $PYTHON"

echo "Compiling QRC files..."
echo "Cleaning python caches and compiled files (excluding .venv)..."
# remove __pycache__ and .pyc under repo but not in .venv
find "$ROOT_DIR" -path "$ROOT_DIR/.venv" -prune -o -type d -name '__pycache__' -print -exec rm -rf {} + || true
# Use exec rm instead of -delete to avoid prune/-depth conflicts
find "$ROOT_DIR" -path "$ROOT_DIR/.venv" -prune -o -type f -name '*.pyc' -print -exec rm -f {} + || true

for qrc in "$UI_DIR"/*.qrc; do
    [ -e "$qrc" ] || continue
    base=$(basename "$qrc" .qrc)
    out="$MODULES_DIR/${base}_rc.py"
    echo " - $qrc -> $out"
    "$PYRCC" "$qrc" -o "$out"
done

# Function to compile a UI file to its target module
compile_ui_file() {
    local ui_file="$1"
    local output_file="$2"
    
    echo " - Compiling $ui_file -> $output_file"
    "$PYUIC" --from-imports "$ui_file" -o "$output_file"
    
    # Remove palette code to allow system themes to work
    echo "   - Removing palette code from $output_file"
    "$PYTHON" "$SCRIPTS_DIR/ui_tools/remove_palette.py" "$output_file"
    
    # Patch imports
    perl -0777 -pe 's/^import designer_rc\b/from modules import designer_rc/igm; s/^from\s+\.\s+import\s+designer_rc\b/from modules import designer_rc/igm' -i "$output_file"
    
    # Fix Qt constants
    echo "   - Fixing Qt constants in $output_file"
    "$PYTHON" "$SCRIPTS_DIR/ui_tools/fix_qt_constants.py" "$output_file"
}

echo "Compiling UI files..."

# Map UI files to their corresponding modules
# Format: "ui_filename:module_name"
declare -A UI_MODULE_MAP=(
    ["frmClientes.ui"]="clientes"
    ["frmempresas.ui"]="empresas"
    ["frmtipocliente.ui"]="tipo_cliente"
    ["db_consulta_view.ui"]="common"
    ["frmConfig.ui"]="common"
    ["frmeditaravisos.ui"]="common"
    ["frmformas_pago.ui"]="common"
    ["frmnuevosavisos.ui"]="common"
)

for ui_file in "$UI_DIR"/*.ui; do
    [ -e "$ui_file" ] || continue
    base=$(basename "$ui_file")
    
    # Check if this UI file has a module mapping
    if [[ -v UI_MODULE_MAP["$base"] ]]; then
        module="${UI_MODULE_MAP[$base]}"
        out="$MODULES_DIR/$module/ui_${base%.ui}.py"
        compile_ui_file "$ui_file" "$out"
    else
        # If no mapping exists, skip or warn
        echo " - WARNING: No module mapping for $base, skipping..."
    fi
done

echo "Running UI import tests..."
"$PYTHON" "$SCRIPTS_DIR/ui_tools/test_ui_imports.py" "$ROOT_DIR"

echo "Compilation and testing done. You can now import generated UI modules."

echo "Note: This script assumes compiled resources are accessible under 'modules' package."

exit 0
