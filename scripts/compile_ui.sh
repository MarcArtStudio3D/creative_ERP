#!/usr/bin/env bash
set -euo pipefail

# Compile UI (.ui) and resource (.qrc) files and patch imports to ensure designer_rc is importable
# Usage: ./scripts/compile_ui.sh

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
UI_DIR="$ROOT_DIR/app/ui"
MODULES_DIR="$ROOT_DIR/modules"
APP_VIEWS_DIR="$ROOT_DIR/app/views"
VENV_BIN="$ROOT_DIR/.venv/bin"

PYUIC="${VENV_BIN}/pyside6-uic"
PYRCC="${VENV_BIN}/pyside6-rcc"

if [ ! -x "$PYUIC" ]; then
    PYUIC=$(command -v pyside6-uic || true)
fi
if [ ! -x "$PYRCC" ]; then
    PYRCC=$(command -v pyside6-rcc || true)
fi

if [ -z "$PYUIC" ] || [ -z "$PYRCC" ]; then
    echo "Error: pyside6-uic or pyside6-rcc not found. Activate your virtualenv or install PySide6." >&2
    exit 1
fi

echo "Using pyside6-uic: $PYUIC"
echo "Using pyside6-rcc: $PYRCC"

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

echo "Finding existing generated UI python files and mapping them to source .ui files..."
mapfile -t generated_files < <(find "$ROOT_DIR" -type f -name 'ui_*.py' -print)

for gen in "${generated_files[@]}"; do
    # try to find header line containing the original ui filename
    header=$(sed -n '1,60p' "$gen" | tr -d '\r' | tr '\n' ' ')
    ui_name=$(echo "$header" | grep -o "reading UI file '[^']*'" | sed "s/reading UI file '//; s/'$//" || true)
    if [ -n "$ui_name" ]; then
        ui_path="$UI_DIR/$ui_name"
        if [ -e "$ui_path" ]; then
            echo " - Compiling $ui_path -> $gen"
            "$PYUIC" --from-imports "$ui_path" -o "$gen"
            # Patch any 'import designer_rc' or 'from . import designer_rc' to 'from modules import designer_rc'
            # Only patch designer_rc import to ensure modules/ directory usage
            perl -0777 -pe 's/^import designer_rc\b/from modules import designer_rc/igm; s/^from\s+\.\s+import\s+designer_rc\b/from modules import designer_rc/igm' -i "$gen"
        fi
    else
        echo " - Skipping $gen (no UI header found)"
    fi
done

echo "Patching done. You can now import generated UI modules." 

echo "Note: This script assumes compiled resources are accessible under 'modules' package."

exit 0
