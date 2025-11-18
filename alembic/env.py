from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from core.models import Base  # Tus modelos

# Alembic config
config = context.config

# Logging
cfg_file = config.config_file_name
if cfg_file is not None:
    fileConfig(cfg_file) # type: ignore

# Target metadata (tus modelos)
target_metadata = Base.metadata


def get_url():
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        raise ValueError("sqlalchemy.url no está definido en alembic.ini")
    return url


def run_migrations_offline():
    """Modo offline: genera SQL sin ejecutar."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
        render_as_batch=True,   # Muy importante para SQLite
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Modo online: ejecuta migraciones."""
    engine = create_engine(get_url())

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,             # Detecta cambios en columnas
            compare_server_default=True,   # Detecta cambios de default
            render_as_batch=context.get_x_argument(
                as_dictionary=True
            ).get("batch", False),         # Necesario para SQLite # type: ignore
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

