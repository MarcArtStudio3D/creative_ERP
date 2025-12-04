#!/usr/bin/env bash
set -euo pipefail
# Check for stray print() occurrences under core/ and fail if any found

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "Checking for stray print() statements under core/ ..."

TMPF=$(mktemp)
git grep -n --untracked -E "^[[:space:]]*print\(" -- core/*.py > "$TMPF" || true

if [ -s "$TMPF" ]; then
  echo "Found stray print() occurrences under core/:" >&2
  cat "$TMPF" >&2
  echo "Core modules should log via logging.* (avoid print())." >&2
  rm -f "$TMPF"
  exit 2
fi

rm -f "$TMPF"
echo "No stray prints found under core/. ✅"
exit 0
