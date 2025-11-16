# -----------------------------
# core/db.py
# -----------------------------
"""Gestión de base de datos con SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from core.models import Base
import os

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