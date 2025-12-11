"""
Modelos Dataclass para el módulo Core.
Arquitectura MVC pura sin ORM.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """Modelo para Usuario del sistema"""
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    full_name: str = ""
    password_hash: str = ""
    role: str = "user"
    is_active: bool = True
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    allowed_groups: str = "[]"  # JSON array de IDs de grupos permitidos

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Crea una instancia desde un diccionario (SQL row)"""
        if not data:
            return None
        return cls(
            id=data.get('id'),
            username=data.get('username', ''),
            email=data.get('email', ''),
            full_name=data.get('full_name', ''),
            password_hash=data.get('password_hash', ''),
            role=data.get('role', 'user'),
            is_active=bool(data.get('is_active', True)),
            created_at=data.get('created_at'),
            last_login=data.get('last_login'),
            allowed_groups=data.get('allowed_groups', '[]')
        )

    def to_dict(self) -> dict:
        """Convierte a diccionario para SQL INSERT/UPDATE"""
        result = {
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'password_hash': self.password_hash,
            'role': self.role,
            'is_active': 1 if self.is_active else 0,
            'created_at': self.created_at,
            'last_login': self.last_login,
            'allowed_groups': self.allowed_groups
        }
        if self.id is not None:
            result['id'] = self.id
        return result

    def verify_password(self, password: str) -> bool:
        """Verifica una contraseña contra el hash almacenado"""
        from core.models import verify_password
        return verify_password(self.password_hash, password)

    def set_password(self, password: str):
        """Establece una nueva contraseña (la hashea)"""
        from core.models import hash_password
        self.password_hash = hash_password(password)


@dataclass
class BusinessGroup:
    """Modelo para Grupo Empresarial"""
    id: Optional[int] = None
    name: str = ""
    code: str = ""
    description: Optional[str] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'BusinessGroup':
        """Crea una instancia desde un diccionario (SQL row)"""
        if not data:
            return None
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            code=data.get('code', ''),
            description=data.get('description'),
            created_at=data.get('created_at')
        )

    def to_dict(self) -> dict:
        """Convierte a diccionario para SQL INSERT/UPDATE"""
        result = {
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'created_at': self.created_at
        }
        if self.id is not None:
            result['id'] = self.id
        return result


@dataclass
class Permission:
    """Modelo para Permiso de usuario"""
    id: Optional[int] = None
    user_id: Optional[int] = None
    module_id: Optional[int] = None
    can_read: bool = False
    can_write: bool = False
    can_delete: bool = False
    can_export: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> 'Permission':
        """Crea una instancia desde un diccionario (SQL row)"""
        if not data:
            return None
        return cls(
            id=data.get('id'),
            user_id=data.get('user_id'),
            module_id=data.get('module_id'),
            can_read=bool(data.get('can_read', False)),
            can_write=bool(data.get('can_write', False)),
            can_delete=bool(data.get('can_delete', False)),
            can_export=bool(data.get('can_export', False))
        )

    def to_dict(self) -> dict:
        """Convierte a diccionario para SQL INSERT/UPDATE"""
        result = {
            'user_id': self.user_id,
            'module_id': self.module_id,
            'can_read': 1 if self.can_read else 0,
            'can_write': 1 if self.can_write else 0,
            'can_delete': 1 if self.can_delete else 0,
            'can_export': 1 if self.can_export else 0
        }
        if self.id is not None:
            result['id'] = self.id
        return result


@dataclass
class Module:
    """Modelo para Módulo del sistema"""
    id: Optional[int] = None
    name: str = ""
    code: str = ""
    description: Optional[str] = None
    icon: Optional[str] = None
    order: int = 0
    active: bool = True
    parent_id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Module':
        """Crea una instancia desde un diccionario (SQL row)"""
        if not data:
            return None
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            code=data.get('code', ''),
            description=data.get('description'),
            icon=data.get('icon'),
            order=data.get('order', 0),
            active=bool(data.get('active', True)),
            parent_id=data.get('parent_id')
        )

    def to_dict(self) -> dict:
        """Convierte a diccionario para SQL INSERT/UPDATE"""
        result = {
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'icon': self.icon,
            'order': self.order,
            'active': 1 if self.active else 0,
            'parent_id': self.parent_id
        }
        if self.id is not None:
            result['id'] = self.id
        return result

