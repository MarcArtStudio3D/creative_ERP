# -----------------------------
# main.py
# -----------------------------
# (guardar como main.py)
from core.logging_config import configure_logging
from app.app import run_app

# Configure logging early using environment or config
configure_logging()


if __name__ == '__main__':
    run_app()