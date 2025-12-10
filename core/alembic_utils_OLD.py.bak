"""Utilities to protect Alembic migrations from running where they shouldn't."""

import os


def ensure_not_running_migrations_on_main(url: str):
    """Block running Alembic migrations against the global `main` DB by default.

    If the supplied SQLAlchemy URL contains the production-ish database name
    `creative_erp_main` this function will raise unless the environment variable
    ALLOW_ALMIGRATE_MAIN is set to '1', 'true' or 'yes'.
    """
    if "creative_erp_main" in (url or ""):
        allow = os.environ.get("ALLOW_ALMIGRATE_MAIN", "")
        if allow.lower() not in ("1", "true", "yes"):
            raise RuntimeError(
                "Refusing to run Alembic migrations against 'creative_erp_main' by default. "
                "If you intentionally want to run migrations against main, set the environment "
                "variable ALLOW_ALMIGRATE_MAIN=1 and re-run the command."
            )
