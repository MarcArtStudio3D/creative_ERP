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


# -----------------------------
# Repositorios para autenticación y multi-empresa
# -----------------------------

from .models import User, BusinessGroup, Company


class UserRepository:
    """Repositorio para operaciones con usuarios."""
    
    @staticmethod
    def get_all_users() -> List[User]:
        """Obtener todos los usuarios."""
        db = SessionLocal()
        try:
            return db.query(User).all()
        finally:
            db.close()
    
    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """Obtener usuario por nombre de usuario."""
        db = SessionLocal()
        try:
            return db.query(User).filter(User.username == username).first()
        finally:
            db.close()


class BusinessGroupRepository:
    """Repositorio para operaciones con grupos empresariales."""
    
    @staticmethod
    def get_all_groups() -> List[BusinessGroup]:
        """Obtener todos los grupos empresariales."""
        db = SessionLocal()
        try:
            return db.query(BusinessGroup).all()
        finally:
            db.close()


class CompanyRepository:
    """Repositorio para operaciones con empresas."""
    
    @staticmethod
    def get_companies_by_group(group_id: int) -> List[Company]:
        """Obtener empresas de un grupo específico."""
        db = SessionLocal()
        try:
            return db.query(Company).filter(Company.group_id == group_id).all()
        finally:
            db.close()