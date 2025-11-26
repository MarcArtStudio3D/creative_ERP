# -----------------------------
# setup_build.sh
# -----------------------------
# (guardar como setup_build.sh)
#!/usr/bin/env bash
set -e
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Inicializar DB
python - <<'PY'
from core.db import init_db
init_db()
print('DB inicializada')
PY