"""Núcleo del sistema - modelos y lógica de negocio."""

# Auth
from .auth import (
    AuthenticationManager,
    Session,
    User,
    UserRole,
    get_role_permissions,
)

# Company Management
from .company_manager import (
    company_manager,
    get_current_company_context,
)

# Database - Ahora usando MultiDBManager con SQL directo
from .db_manager import get_db_manager, init_db_manager

# Models - Ahora son helpers y tipos de compatibilidad
from .models import (
    BusinessGroup,
    Empresa,
)

# NOTE: We DO NOT import `core.repositories` here to avoid circular imports
# that can occur when modules under `modules.*` import `core.peewee_db`.
# If callers need repositories, import them explicitly:
#   from core import repositories
# or
#   from core.repositories import UserRepository

__all__ = [
    # Auth
    "AuthenticationManager",
    "Session",
    "User",
    "UserRole",
    "get_role_permissions",
    # Company Management
    "company_manager",
    "get_current_company_context",
    # Database
    "get_db_manager",
    "init_db_manager",
    # Models
    "BusinessGroup",
    "Empresa",
]
