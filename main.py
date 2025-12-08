# -----------------------------
# main.py
# -----------------------------
# (guardar como main.py)
from app.app import run_app
from core.logging_config import configure_logging

# Configure logging early using environment or config
configure_logging()


if __name__ == "__main__":
    run_app()
