#!/usr/bin/env bash
set -euo pipefail

# Usage: scripts/check_resource_imports.sh [module1 module2 ...]
# The script checks generated UI python files (ui_*.py and *_rc.py) for imports of a list of disallowed modules

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DISALLOWED=${@:-${DISALLOWED_RESOURCE_MODULES:-maya_rc}}

if [ -z "$DISALLOWED" ]; then
    echo "No disallowed resource modules specified. Exiting." >&2
    exit 0
fi

echo "Checking for disallowed resource modules: $DISALLOWED"

IFS=' ' read -r -a modules <<< "$DISALLOWED"

# Collect candidate files to check (generated UI + resource modules)
mapfile -t files_to_check < <(find "$ROOT_DIR" -type f \( -name 'ui_*.py' -o -name '*_rc.py' \) -print)

if [ ${#files_to_check[@]} -eq 0 ]; then
    echo "No generated UI/resource files found to check. Nothing to do." >&2
    exit 0
fi

errors=0
for mod in "${modules[@]}"; do
    pat="\\b${mod}\\b"
    echo " - Searching for module: ${mod}"
    for f in "${files_to_check[@]}"; do
        if grep -E --line-number --binary-files=without-match -n "$pat" "$f" >/dev/null 2>&1; then
            echo "Found disallowed reference to '$mod' in $f:" 
            grep -n "$pat" "$f" | sed -n '1,200p'
            errors=1
        fi
    done
done

if [ $errors -ne 0 ]; then
    echo "Error: One or more disallowed resource modules were found in generated files." >&2
    exit 1
fi

echo "No disallowed resource module references found in generated files."
exit 0
