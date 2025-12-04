import logging
import os
from typing import Optional

from core.config import config


def configure_logging(env: Optional[str] = None):
    """Configure logging for the application.

    - In 'development' mode: log to console (DEBUG) and file (DEBUG).
    - In other modes: log only to file (INFO) and do not print errors to console.
    """
    if env is None:
        env = os.environ.get('ENVIRONMENT') or config.get_current_env()

    # Basic logger
    root = logging.getLogger()
    # Prevent adding multiple handlers if configure_logging called more than once
    if getattr(root, '_configured_by_app', False):
        return

    # Set global level generous; handlers will filter
    root.setLevel(logging.DEBUG)

    # File handler (always present) - level depends on environment
    log_file = os.environ.get('LOG_FILE') or config.get('logging.file', 'logs/creative_erp.log')
    try:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
    except Exception:
        pass

    file_level_name = os.environ.get('LOG_LEVEL') or config.get('logging.level', 'INFO')
    try:
        file_level = getattr(logging, file_level_name.upper())
    except Exception:
        file_level = logging.INFO

    fh = logging.FileHandler(log_file)
    fh.setLevel(file_level)
    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    fh.setFormatter(fmt)
    root.addHandler(fh)

    # Console handler only in development — user requested errors only in DEV
    if str(env).lower() == 'development':
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        root.addHandler(ch)

    # mark configured
    setattr(root, '_configured_by_app', True)
