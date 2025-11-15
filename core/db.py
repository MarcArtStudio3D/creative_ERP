# -----------------------------
# core/db.py
# -----------------------------
# (guardar como core/db.py)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os


DB_PATH = os.environ.get('CREATIVE_ERP_DB', 'sqlite:///creative_erp.db')


engine = create_engine(DB_PATH, connect_args={"check_same_thread": False} if 'sqlite' in DB_PATH else {})
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))




def init_db():
from . import models
models.Base.metadata.create_all(bind=engine)