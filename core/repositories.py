"""
Repositorios Peewee para acceso a datos del core.
Migración completa desde SQLModel a Peewee.
"""

from typing import List, Optional
from peewee import DoesNotExist

from modules.clientes.models import Cliente
from core.peewee_db import ensure_initialized, get_current_database, set_current_database
from core.models import BusinessGroup, Empresa, User


class UserRepository:
    """Repositorio para operaciones con usuarios usando Peewee."""

    @staticmethod
    def get_all_users() -> List[User]:
        """Obtener todos los usuarios."""
        try:
            # Asegurar que estamos en la BD main
            original_db = get_current_database()
            if original_db != "main":
                set_current_database("main")

            try:
                ensure_initialized()
                return list(User.select())
            finally:
                if original_db and original_db != "main":
                    set_current_database(original_db)
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []

    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """Obtener usuario por nombre de usuario."""
        try:
            # Asegurar que estamos en la BD main
            original_db = get_current_database()
            if original_db != "main":
                set_current_database("main")

            try:
                ensure_initialized()
                return User.get(User.username == username)
            finally:
                if original_db and original_db != "main":
                    set_current_database(original_db)
        except DoesNotExist:
            return None
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Obtener usuario por ID."""
        try:
            # Asegurar que estamos en la BD main
            original_db = get_current_database()
            if original_db != "main":
                set_current_database("main")

            try:
                ensure_initialized()
                return User.get_by_id(user_id)
            finally:
                if original_db and original_db != "main":
                    set_current_database(original_db)
        except DoesNotExist:
            return None
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None

    @staticmethod
    def create_user(**kwargs) -> Optional[User]:
        """Crear un nuevo usuario."""
        try:
            # Asegurar que estamos en la BD main
            original_db = get_current_database()
            if original_db != "main":
                set_current_database("main")

            try:
                ensure_initialized()
                user = User.create(**kwargs)
                return user
            finally:
                if original_db and original_db != "main":
                    set_current_database(original_db)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None


class BusinessGroupRepository:
    """Repositorio para operaciones con grupos empresariales usando Peewee."""

    @staticmethod
    def get_all_groups() -> List[BusinessGroup]:
        """Obtener todos los grupos empresariales."""
        try:
            # Asegurar que estamos en la BD main
            original_db = get_current_database()
            if original_db != "main":
                set_current_database("main")

            try:
                ensure_initialized()
                return list(BusinessGroup.select())
            finally:
                if original_db and original_db != "main":
                    set_current_database(original_db)
        except Exception as e:
            print(f"Error getting all groups: {e}")
            return []

    @staticmethod
    def get_group_by_id(group_id: int) -> Optional[BusinessGroup]:
        """Obtener grupo por ID."""
        try:
            # Asegurar que estamos en la BD main
            original_db = get_current_database()
            if original_db != "main":
                set_current_database("main")

            try:
                ensure_initialized()
                return BusinessGroup.get_by_id(group_id)
            finally:
                if original_db and original_db != "main":
                    set_current_database(original_db)
        except DoesNotExist:
            return None
        except Exception as e:
            print(f"Error getting group by id: {e}")
            return None


class CompanyRepository:
    """Repositorio para operaciones con empresas usando Peewee."""

    @staticmethod
    def get_empresas_by_group(group_id: int) -> List[Empresa]:
        """Obtener empresas de un grupo específico."""
        try:
            # Asegurar que estamos en la BD main
            original_db = get_current_database()
            if original_db != "main":
                set_current_database("main")

            try:
                ensure_initialized()
                return list(Empresa.select().where(Empresa.group_id == group_id))
            finally:
                if original_db and original_db != "main":
                    set_current_database(original_db)
        except Exception as e:
            print(f"Error getting empresas by group: {e}")
            return []

    @staticmethod
    def get_all_empresas() -> List[Empresa]:
        """Obtener todas las empresas."""
        try:
            # Asegurar que estamos en la BD main
            original_db = get_current_database()
            if original_db != "main":
                set_current_database("main")

            try:
                ensure_initialized()
                return list(Empresa.select())
            finally:
                if original_db and original_db != "main":
                    set_current_database(original_db)
        except Exception as e:
            print(f"Error getting all empresas: {e}")
            return []

    @staticmethod
    def get_empresa_by_id(empresa_id: int) -> Optional[Empresa]:
        """Obtener empresa por ID."""
        try:
            # Asegurar que estamos en la BD main
            original_db = get_current_database()
            if original_db != "main":
                set_current_database("main")

            try:
                ensure_initialized()
                return Empresa.get_by_id(empresa_id)
            finally:
                if original_db and original_db != "main":
                    set_current_database(original_db)
        except DoesNotExist:
            return None
        except Exception as e:
            print(f"Error getting empresa by id: {e}")
            return None


class ClientRepo:
    """Repositorio de clientes usando Peewee.

    IMPORTANTE: Los clientes están en la BD de la empresa actual,
    NO en la BD main. Por eso NO cambiamos de BD aquí.
    """

    @staticmethod
    def get_all() -> List[Cliente]:
        """Obtiene todos los clientes de la empresa actual."""
        try:
            # NO cambiar de BD - los clientes están en la BD de la empresa actual
            ensure_initialized()
            return list(Cliente.select())
        except Exception as e:
            print(f"Error getting all clientes: {e}")
            return []

    @staticmethod
    def get_by_id(client_id: int) -> Optional[Cliente]:
        """Obtiene un cliente por ID de la empresa actual."""
        try:
            # NO cambiar de BD - los clientes están en la BD de la empresa actual
            ensure_initialized()
            return Cliente.get_by_id(client_id)
        except DoesNotExist:
            return None
        except Exception as e:
            print(f"Error getting cliente by id: {e}")
            return None

    @staticmethod
    def create(**kwargs) -> Optional[Cliente]:
        """Crea un nuevo cliente en la empresa actual."""
        try:
            # NO cambiar de BD - los clientes están en la BD de la empresa actual
            ensure_initialized()
            cliente = Cliente.create(**kwargs)
            return cliente
        except Exception as e:
            print(f"Error creating cliente: {e}")
            return None

