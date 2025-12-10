#!/usr/bin/env bash
set -euo pipefail
# Calcular raíz del repo: dos niveles arriba desde este script (scripts/translations)
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

echo "Running extractor..."
python3 scripts/translations/extract_tr_from_py.py

AUTO_TS="translations/creative_erp_fr_auto.ts"
BASE_TS="translations/creative_erp_fr.ts"
OUT_TS="translations/creative_erp_fr_merged.ts"

if [ ! -f "$AUTO_TS" ]; then
  echo "Extractor did not produce $AUTO_TS"
  exit 1
fi

echo "Merging $AUTO_TS into $BASE_TS -> $OUT_TS"
python3 scripts/translations/merge_ts.py --add "$AUTO_TS" --base "$BASE_TS" --out "$OUT_TS"

echo "Listing merged head (first 80 lines):"
sed -n '1,80p' "$OUT_TS" || true

# Move merged to base (backup if needed)
if [ -f "$OUT_TS" ]; then
  cp "$BASE_TS" "${BASE_TS}.bak" || true
  mv "$OUT_TS" "$BASE_TS"
  echo "Replaced $BASE_TS (backup at ${BASE_TS}.bak)"
fi

# Check lrelease exists
if ! command -v lrelease >/dev/null 2>&1; then
  echo "Warning: lrelease not found in PATH. Install qttools5-dev-tools (Debian/Ubuntu) or Qt to compile .ts to .qm."
  echo "Skipping compilation step."
else
  # Compile all ts in translations/
  echo "Compiling .ts -> .qm using lrelease"
  for ts in translations/*.ts; do
    qm="${ts%.ts}.qm"
    echo "Compiling $ts -> $qm"
    lrelease "$ts" -qm "$qm"
  done

  echo "Listing translations/*.qm"
  ls -la translations/*.qm || true
fi

echo "Done. Verify with: grep -n 'LoginWindowMultiCompany' $BASE_TS || true"
