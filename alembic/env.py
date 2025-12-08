import os
from logging.config import fileConfig

from sqlalchemy import create_engine

from alembic import context
from core.alembic_utils import ensure_not_running_migrations_on_main
from core.models import Base  # Tus modelos

# Alembic config
config = context.config

# Logging
cfg_file = config.config_file_name
if cfg_file is not None:
    fileConfig(cfg_file)  # type: ignore

# Target metadata (tus modelos)
target_metadata = Base.metadata


def get_url():
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        raise ValueError("sqlalchemy.url no está definido en alembic.ini")
    return url


def _ensure_not_running_migrations_on_main(url: str):
    """Block running Alembic migrations against the global `main` DB by default.

    This prevents accidental application of module migrations in the `creative_erp_main`
    database. To override intentionally, set the env var ALLOW_ALMIGRATE_MAIN=1.
    """
    # simple check: if database name includes the known main DB name
    if "creative_erp_main" in (url or ""):
        allow = os.environ.get("ALLOW_ALMIGRATE_MAIN", "")
        if allow.lower() not in ("1", "true", "yes"):
            raise RuntimeError(
                "Refusing to run Alembic migrations against 'creative_erp_main' by default. "
                "If you intentionally want to run migrations against main, set the environment "
                "variable ALLOW_ALMIGRATE_MAIN=1 and re-run the command."
            )


def run_migrations_offline():
    """Modo offline: genera SQL sin ejecutar."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
        # render_as_batch=True,   # Solo para SQLite
        # dialect_opts={"paramstyle": "named"},  # Solo para SQLite
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Modo online: ejecuta migraciones."""
    url = get_url()

    # Safety: do not allow running migrations on the 'main' DB unless explicitly authorised
    ensure_not_running_migrations_on_main(url)

    engine = create_engine(url)

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Detecta cambios en columnas
            compare_server_default=True,  # Detecta cambios de default
            render_as_batch=context.get_x_argument(as_dictionary=True).get(
                "batch", False
            ),  # Necesario para SQLite # type: ignore
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
