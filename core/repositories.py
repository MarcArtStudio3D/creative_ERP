# -----------------------------
# core/repositories.py
# -----------------------------
"""Repositorios para acceso a datos."""

from typing import Generic, List, Optional, TypeVar

from sqlmodel import select

from modules.clientes.models import Cliente

from .db import SessionLocal

T = TypeVar("T")


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
    def get_all() -> List[Cliente]:
        """Obtiene todos los clientes."""
        db = SessionLocal()
        try:
            statement = select(Cliente)
            return db.exec(statement).all()
        finally:
            db.close()

    @staticmethod
    def get_by_id(client_id: int) -> Optional[Cliente]:
        """Obtiene un cliente por ID."""
        db = SessionLocal()
        try:
            statement = select(Cliente).where(Cliente.id == client_id)
            return db.exec(statement).first()
        finally:
            db.close()

    @staticmethod
    def create(**kwargs) -> Cliente:
        """Crea un nuevo cliente."""
        db = SessionLocal()
        try:
            c = Cliente(**kwargs)
            db.add(c)
            db.commit()
            db.refresh(c)
            return c
        finally:
            db.close()


# -----------------------------
# Repositorios para autenticación y multi-empresa
# -----------------------------

from .models import BusinessGroup, Empresa, User


class UserRepository:
    """Repositorio para operaciones con usuarios."""

    @staticmethod
    def get_all_users() -> List[User]:
        """Obtener todos los usuarios."""
        db = SessionLocal()
        try:
            statement = select(User)
            return db.exec(statement).all()
        finally:
            db.close()

    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """Obtener usuario por nombre de usuario."""
        db = SessionLocal()
        try:
            statement = select(User).where(User.username == username)
            return db.exec(statement).first()
        finally:
            db.close()


class BusinessGroupRepository:
    """Repositorio para operaciones con grupos empresariales."""

    @staticmethod
    def get_all_groups() -> List[BusinessGroup]:
        """Obtener todos los grupos empresariales."""
        db = SessionLocal()
        try:
            statement = select(BusinessGroup)
            return db.exec(statement).all()
        finally:
            db.close()


class CompanyRepository:
    """Repositorio para operaciones con empresas."""

    @staticmethod
    def get_empresas_by_group(group_id: int) -> List[Empresa]:
        """Obtener empresas de un grupo específico."""
        db = SessionLocal()
        try:
            statement = select(Empresa).where(Empresa.group_id == group_id)
            return db.exec(statement).all()
        finally:
            db.close()
