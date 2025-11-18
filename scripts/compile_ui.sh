#!/usr/bin/env bash
set -euo pipefail

# Compile UI (.ui) and resource (.qrc) files and patch imports to ensure designer_rc is importable
# Also fixes Qt constants for better Pylance compatibility
# Usage: ./scripts/compile_ui.sh

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
UI_DIR="$ROOT_DIR/app/ui"
MODULES_DIR="$ROOT_DIR/modules"
APP_VIEWS_DIR="$ROOT_DIR/app/views"
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

echo "Compiling UI files..."
for ui_file in "$UI_DIR"/*.ui; do
    [ -e "$ui_file" ] || continue
    base=$(basename "$ui_file" .ui)
    
    # Determine output location
    if [[ "$base" == "frmClientes" ]]; then
        # Special case: frmClientes.ui generates files in both app/views and modules/clientes
        out_app="$APP_VIEWS_DIR/ui_${base}.py"
        out_modules="$MODULES_DIR/clientes/ui_${base}.py"
        
        echo " - Compiling $ui_file -> $out_app"
        "$PYUIC" --from-imports "$ui_file" -o "$out_app"
        # Remove palette code to allow system themes to work
        echo "   - Removing palette code from $out_app"
        "$PYTHON" "$SCRIPTS_DIR/remove_palette.py" "$out_app"
        # Patch imports
        perl -0777 -pe 's/^import designer_rc\b/from modules import designer_rc/igm; s/^from\s+\.\s+import\s+designer_rc\b/from modules import designer_rc/igm' -i "$out_app"
        # Fix Qt constants
        echo "   - Fixing Qt constants in $out_app"
        "$PYTHON" "$SCRIPTS_DIR/fix_qt_constants.py" "$out_app"
        
        # Copy to modules location
        cp "$out_app" "$out_modules"
        echo "   - Copied to $out_modules"
    else
        # Default: put in app/views/
        out="$APP_VIEWS_DIR/ui_${base}.py"
        echo " - Compiling $ui_file -> $out"
        "$PYUIC" --from-imports "$ui_file" -o "$out"
        # Remove palette code to allow system themes to work
        echo "   - Removing palette code from $out"
        "$PYTHON" "$SCRIPTS_DIR/remove_palette.py" "$out"
        # Patch imports
        perl -0777 -pe 's/^import designer_rc\b/from modules import designer_rc/igm; s/^from\s+\.\s+import\s+designer_rc\b/from modules import designer_rc/igm' -i "$out"
        # Fix Qt constants
        echo "   - Fixing Qt constants in $out"
        "$PYTHON" "$SCRIPTS_DIR/fix_qt_constants.py" "$out"
    fi
done

echo "Running UI import tests..."
"$PYTHON" "$SCRIPTS_DIR/test_ui_imports.py" "$ROOT_DIR"

echo "Compilation and testing done. You can now import generated UI modules."

echo "Note: This script assumes compiled resources are accessible under 'modules' package."

exit 0
