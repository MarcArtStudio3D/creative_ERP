#!/usr/bin/env bash
set -euo pipefail
# Search for literal 'print(' at the beginning of non-test Python files and fail if found.
# We ignore files under tests/ and .venv, and we also ignore generated files and translations by default.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "Checking for stray print() statements (excluding tests/)..."

# Use git grep (works for both tracked and untracked files with --untracked)
# Match beginning-of-line optional whitespace + print(
mapfile -t matches < <(git grep -n --untracked -E "^[[:space:]]*print\(" -- '*.py' || true)

# Filter out allowed paths
filtered=()
for m in "${matches[@]:-}"; do
  # path is before first ':'
  file=$(echo "$m" | cut -d: -f1)
  # ignore tests/, .venv and alembic/versions
  if [[ "$file" == tests/* ]] || [[ "$file" == .venv/* ]] || [[ "$file" == alembic/versions/* ]]; then
    continue
  fi
  # ignore scripts/check_no_prints.sh itself
  if [[ "$file" == scripts/check_no_prints.sh ]]; then
    continue
  fi
  filtered+=("$m")
done

if [ ${#filtered[@]} -gt 0 ]; then
  echo "Found stray print() occurrences in non-test code:" >&2
  printf '%s\n' "${filtered[@]}" >&2
  echo "Please replace these prints with logging.* or add a rationale in .github/allowlist_prints.md" >&2
  exit 2
fi

echo "No stray prints found in non-test code. ✅"
exit 0
