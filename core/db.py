# -----------------------------
# core/db.py
# -----------------------------
"""Gestión de base de datos con SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from core.models import Base
import os
from sqlalchemy import inspect, text
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Date, Float, Text

# Ruta de la base de datos (por defecto SQLite local)
DB_PATH = os.environ.get('CREATIVE_ERP_DB', 'sqlite:///creative_erp.db')

# Motor de base de datos
engine = create_engine(
    DB_PATH, 
    connect_args={"check_same_thread": False} if 'sqlite' in DB_PATH else {}
)

# Sesión para queries
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


def get_session():
    """Obtiene una sesión de base de datos."""
    return SessionLocal()


def init_db():
    """Crea todas las tablas en la base de datos."""
    from . import models
    from modules.clientes import models as clientes_models
    
    models.Base.metadata.create_all(bind=engine)
    clientes_models.Base.metadata.create_all(bind=engine)
    # Attempt to add missing columns for SQLite databases. This will only add columns
    # and will not attempt destructive schema changes. It's a pragmatic helper
    # for development environments where migrations may be missing.
    if 'sqlite' in DB_PATH:
        _ensure_sqlite_columns(models.Base)
        try:
            _ensure_sqlite_columns(clientes_models.Base)
        except Exception:
            pass


def _ensure_sqlite_columns(base):
    inspector = inspect(engine)
    for table_name, table_obj in base.metadata.tables.items():
        if not inspector.has_table(table_name):
            continue
        existing_cols = {c['name'] for c in inspector.get_columns(table_name)}
        for col in table_obj.columns:
            col_name = col.name
            if col_name in existing_cols:
                continue
            # Skip primary key additions
            if col.primary_key:
                continue
            # Map SQLAlchemy types to SQLite types (simple mapping)
            sa_type = col.type
            sql_type = 'TEXT'
            if isinstance(sa_type, Integer):
                sql_type = 'INTEGER'
            elif isinstance(sa_type, Float):
                sql_type = 'REAL'
            elif isinstance(sa_type, DateTime):
                sql_type = 'DATETIME'
            elif isinstance(sa_type, Date):
                sql_type = 'DATE'
            elif isinstance(sa_type, Text):
                sql_type = 'TEXT'
            elif isinstance(sa_type, String):
                # honor length if present
                try:
                    length = sa_type.length
                    if length:
                        sql_type = f'VARCHAR({length})'
                    else:
                        sql_type = 'VARCHAR'
                except Exception:
                    sql_type = 'VARCHAR'

            # Compose ALTER TABLE statement. Make column nullable to avoid issues.
            stmt = text(f'ALTER TABLE "{table_name}" ADD COLUMN "{col_name}" {sql_type}')
            try:
                with engine.connect() as conn:
                    conn.execute(stmt)
            except Exception:
                # best-effort: ignore failures to avoid breaking startup
                continue