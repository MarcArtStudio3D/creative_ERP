"""
Repositorios SQL directo para acceso a datos del core.
Migrado de Peewee a SQL directo con MultiDBManager.
Retorna objetos Dataclass para mantener arquitectura MVC pura.
"""
from typing import List, Optional, TYPE_CHECKING
import logging
from core.base_repository import BaseRepository
from core.models_dataclass import User, BusinessGroup

if TYPE_CHECKING:
    from modules.empresas.models import Empresa

logger = logging.getLogger(__name__)
class UserRepository(BaseRepository):
    """Repositorio para operaciones con usuarios usando SQL directo."""
    def __init__(self):
        super().__init__()
    @staticmethod
    def get_all_users() -> List[User]:
        """Obtener todos los usuarios."""
        try:
            repo = UserRepository()
            query = "SELECT * FROM users"
            rows = repo._fetch_all(query, use_main=True)
            return [User.from_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            return []
    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """Obtener usuario por nombre de usuario."""
        try:
            repo = UserRepository()
            query = "SELECT * FROM users WHERE username = %s"
            row = repo._fetch_one(query, (username,), use_main=True)
            return User.from_dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting user by username: {e}")
            return None
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Obtener usuario por ID."""
        try:
            repo = UserRepository()
            query = "SELECT * FROM users WHERE id = %s"
            row = repo._fetch_one(query, (user_id,), use_main=True)
            return User.from_dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
    @staticmethod
    def create_user(user: User) -> Optional[User]:
        """Crear un nuevo usuario."""
        try:
            repo = UserRepository()
            data = user.to_dict()
            new_id = repo._insert('users', data, use_main=True)
            if new_id:
                return UserRepository.get_user_by_id(new_id)
            return None
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    @staticmethod
    def update_user(user_id: int, user: User) -> Optional[User]:
        """Actualizar un usuario."""
        try:
            repo = UserRepository()
            data = user.to_dict()
            rows_affected = repo._update('users', data, 'id = %s', (user_id,), use_main=True)
            if rows_affected > 0:
                return UserRepository.get_user_by_id(user_id)
            return None
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return None
class BusinessGroupRepository(BaseRepository):
    """Repositorio para operaciones con grupos empresariales."""
    def __init__(self):
        super().__init__()
    @staticmethod
    def get_all_groups() -> List[BusinessGroup]:
        """Obtener todos los grupos empresariales."""
        try:
            repo = BusinessGroupRepository()
            query = "SELECT * FROM business_groups ORDER BY name"
            rows = repo._fetch_all(query, use_main=True)
            return [BusinessGroup.from_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting all groups: {e}")
            return []
    @staticmethod
    def get_group_by_id(group_id: int) -> Optional[BusinessGroup]:
        """Obtener grupo por ID."""
        try:
            repo = BusinessGroupRepository()
            query = "SELECT * FROM business_groups WHERE id = %s"
            row = repo._fetch_one(query, (group_id,), use_main=True)
            return BusinessGroup.from_dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting group by ID: {e}")
            return None
    @staticmethod
    def get_group_by_code(code: str) -> Optional[BusinessGroup]:
        """Obtener grupo por código."""
        try:
            repo = BusinessGroupRepository()
            query = "SELECT * FROM business_groups WHERE code = %s"
            row = repo._fetch_one(query, (code,), use_main=True)
            return BusinessGroup.from_dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting group by code: {e}")
            return None
class CompanyRepository(BaseRepository):
    """Repositorio para operaciones con empresas."""
    def __init__(self):
        super().__init__()
    @staticmethod
    def get_all_companies(group_id: Optional[int] = None) -> List['Empresa']:
        """Obtener todas las empresas, opcionalmente filtradas por grupo."""
        try:
            from modules.empresas.models import Empresa
            repo = CompanyRepository()
            if group_id is not None:
                query = "SELECT * FROM empresas WHERE group_id = %s ORDER BY nombre_fiscal"
                rows = repo._fetch_all(query, (group_id,), use_main=True)
            else:
                query = "SELECT * FROM empresas ORDER BY nombre_fiscal"
                rows = repo._fetch_all(query, use_main=True)
            return [Empresa.from_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting all companies: {e}")
            return []
    @staticmethod
    def get_company_by_id(company_id: int) -> Optional['Empresa']:
        """Obtener empresa por ID."""
        try:
            from modules.empresas.models import Empresa
            repo = CompanyRepository()
            query = "SELECT * FROM empresas WHERE id = %s"
            row = repo._fetch_one(query, (company_id,), use_main=True)
            return Empresa.from_dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting company by ID: {e}")
            return None
    @staticmethod
    def get_companies_by_group(group_id: int) -> List['Empresa']:
        """Obtener empresas de un grupo."""
        return CompanyRepository.get_all_companies(group_id)
# Alias para compatibilidad
EmpresaRepository = CompanyRepository
__all__ = [
    'UserRepository',
    'BusinessGroupRepository', 
    'CompanyRepository',
    'EmpresaRepository',
]
