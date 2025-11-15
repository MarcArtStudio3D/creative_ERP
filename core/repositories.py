# -----------------------------
# core/repositories.py
# -----------------------------
"""Repositorios para acceso a datos."""

from typing import List, Optional, TypeVar, Generic
from .db import SessionLocal
from .models import Client, Invoice

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    Repositorio base genérico.
    Similar a los repositorios que tenías en C++.
    """
    
    def __init__(self, db_connection, table_name: str):
        self.db = db_connection
        self.table_name = table_name
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Obtiene una entidad por su ID."""
        raise NotImplementedError
    
    def get_all(self) -> List[T]:
        """Obtiene todas las entidades."""
        raise NotImplementedError


class ClientRepo:
    """Repositorio de clientes."""
    
    @staticmethod
    def get_all() -> List[Client]:
        """Obtiene todos los clientes."""
        db = SessionLocal()
        try:
            return db.query(Client).all()
        finally:
            db.close()
    
    @staticmethod
    def get_by_id(client_id: int) -> Optional[Client]:
        """Obtiene un cliente por ID."""
        db = SessionLocal()
        try:
            return db.query(Client).filter(Client.id == client_id).first()
        finally:
            db.close()
    
    @staticmethod
    def create(**kwargs) -> Client:
        """Crea un nuevo cliente."""
        db = SessionLocal()
        try:
            c = Client(**kwargs)
            db.add(c)
            db.commit()
            db.refresh(c)
            return c
        finally:
            db.close()


class InvoiceRepo:
    """Repositorio de facturas."""
    
    @staticmethod
    def get_all() -> List[Invoice]:
        """Obtiene todas las facturas."""
        db = SessionLocal()
        try:
            return db.query(Invoice).all()
        finally:
            db.close()
    
    @staticmethod
    def create(**kwargs) -> Invoice:
        """Crea una nueva factura."""
        db = SessionLocal()
        try:
            inv = Invoice(**kwargs)
            db.add(inv)
            db.commit()
            db.refresh(inv)
            return inv
        finally:
            db.close()