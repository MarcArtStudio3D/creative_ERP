"""
Sistema de gestión de usuarios, roles y permisos.

Define la estructura de usuarios, roles predefinidos y control de acceso.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, TYPE_CHECKING
from enum import Enum
from datetime import datetime
import hashlib
import secrets

from core.modules import Permission
import json
import os

if TYPE_CHECKING:
    from core.business import CompanyContext


class UserRole(Enum):
    """
    Roles predefinidos del sistema.
    Cada rol tiene un conjunto de permisos asociados.
    """
    ADMIN = "admin"                    # Acceso total al sistema
    MANAGER = "manager"                # Gestor: acceso a todo excepto configuración
    ACCOUNTANT = "accountant"          # Contable: acceso a contabilidad y finanzas
    SALES = "sales"                    # Ventas: clientes, presupuestos, facturas
    PROJECT_MANAGER = "project_manager" # Gestor de proyectos
    EMPLOYEE = "employee"              # Empleado básico: solo sus proyectos y tiempo
    VIEWER = "viewer"                  # Solo lectura


@dataclass
class User:
    """
    Representa un usuario del sistema.
    """
    id: int
    username: str                      # Nombre de usuario (login)
    email: str
    full_name: str                     # Nombre completo
    password_hash: str                 # Hash de la contraseña (nunca guardar en texto plano)
    role: UserRole                     # Rol principal del usuario
    is_active: bool = True             # Si el usuario está activo
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    
    # Multi-empresa
    allowed_groups: List[int] = field(default_factory=list)      # IDs de grupos a los que tiene acceso
    allowed_companies: List[int] = field(default_factory=list)   # IDs de empresas a las que tiene acceso
    
    # Permisos personalizados por módulo (sobrescriben los del rol)
    custom_permissions: Dict[str, List[Permission]] = field(default_factory=dict)
    
    def __post_init__(self):
        """Inicializa permisos si no existen."""
        if not self.custom_permissions:
            self.custom_permissions = {}
    
    def get_effective_permissions(self) -> Dict[str, List[Permission]]:
        """
        Obtiene los permisos efectivos del usuario.
        Combina los permisos del rol con los personalizados.
        """
        # Permisos base según el rol
        role_permissions = get_role_permissions(self.role)
        
        # Combinar con permisos personalizados
        effective = role_permissions.copy()
        for module_id, perms in self.custom_permissions.items():
            if module_id in effective:
                # Añadir permisos adicionales sin duplicar
                effective[module_id] = list(set(effective[module_id] + perms))
            else:
                effective[module_id] = perms
        
        return effective
    
    def has_permission(self, module_id: str, permission: Permission) -> bool:
        """
        Verifica si el usuario tiene un permiso específico en un módulo.
        
        Args:
            module_id: ID del módulo
            permission: Permiso a verificar
        
        Returns:
            True si tiene el permiso
        """
        perms = self.get_effective_permissions()
        module_perms = perms.get(module_id, [])
        
        # Admin siempre tiene acceso
        if Permission.ADMIN in module_perms:
            return True
        
        return permission in module_perms
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Genera un hash seguro de la contraseña.
        Usa SHA256 con salt. En producción considera bcrypt o argon2.
        """
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}${pwd_hash}"
    
    def verify_password(self, password: str) -> bool:
        """Verifica si la contraseña es correcta."""
        try:
            salt, stored_hash = self.password_hash.split('$')
            pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return pwd_hash == stored_hash
        except:
            return False


def get_role_permissions(role: UserRole) -> Dict[str, List[Permission]]:
    """
    Obtiene los permisos predefinidos para cada rol.
    
    Returns:
        Diccionario {module_id: [permissions]}
    """
    
    # ADMIN: Acceso total a todo
    if role == UserRole.ADMIN:
        return {
            "clientes": [Permission.ADMIN],
            "facturas": [Permission.ADMIN],
            "albaranes": [Permission.ADMIN],
            "presupuestos": [Permission.ADMIN],
            "proveedores": [Permission.ADMIN],
            "facturas_compra": [Permission.ADMIN],
            "articulos": [Permission.ADMIN],
            "almacen": [Permission.ADMIN],
            "contabilidad": [Permission.ADMIN],
            "tesoreria": [Permission.ADMIN],
            "proyectos": [Permission.ADMIN],
            "tiempo": [Permission.ADMIN],
            "usuarios": [Permission.ADMIN],
                "configuracion": [Permission.ADMIN],
                "informes": [Permission.ADMIN],
                "empresas": [Permission.ADMIN],
        }
    
    # MANAGER: Gestión completa excepto usuarios y configuración
    elif role == UserRole.MANAGER:
        return {
            "clientes": [Permission.READ, Permission.CREATE, Permission.UPDATE, Permission.DELETE],
            "facturas": [Permission.READ, Permission.CREATE, Permission.UPDATE, Permission.DELETE, Permission.EXPORT, Permission.PRINT],
            "albaranes": [Permission.READ, Permission.CREATE, Permission.UPDATE, Permission.DELETE, Permission.PRINT],
            "presupuestos": [Permission.READ, Permission.CREATE, Permission.UPDATE, Permission.DELETE, Permission.PRINT],
            "proveedores": [Permission.READ, Permission.CREATE, Permission.UPDATE],
            "facturas_compra": [Permission.READ, Permission.CREATE, Permission.UPDATE],
            "articulos": [Permission.READ, Permission.CREATE, Permission.UPDATE],
            "almacen": [Permission.READ, Permission.UPDATE],
            "contabilidad": [Permission.READ],
            "tesoreria": [Permission.READ, Permission.CREATE, Permission.UPDATE],
            "proyectos": [Permission.READ, Permission.CREATE, Permission.UPDATE, Permission.DELETE],
            "tiempo": [Permission.READ, Permission.CREATE, Permission.UPDATE],
            "informes": [Permission.READ, Permission.EXPORT],
                "empresas": [Permission.READ, Permission.CREATE, Permission.UPDATE, Permission.DELETE],
        }
    
    # ACCOUNTANT: Contabilidad y finanzas
    elif role == UserRole.ACCOUNTANT:
        return {
            "clientes": [Permission.READ],
            "facturas": [Permission.READ, Permission.EXPORT],
            "proveedores": [Permission.READ],
            "facturas_compra": [Permission.READ, Permission.CREATE, Permission.UPDATE],
            "contabilidad": [Permission.ADMIN],
            "tesoreria": [Permission.READ, Permission.CREATE, Permission.UPDATE],
            "informes": [Permission.READ, Permission.EXPORT],
        }
    
    # SALES: Ventas y clientes
    elif role == UserRole.SALES:
        return {
            "clientes": [Permission.READ, Permission.CREATE, Permission.UPDATE],
            "facturas": [Permission.READ, Permission.CREATE, Permission.PRINT],
            "albaranes": [Permission.READ, Permission.CREATE, Permission.PRINT],
            "presupuestos": [Permission.READ, Permission.CREATE, Permission.UPDATE, Permission.PRINT],
            "articulos": [Permission.READ],
            "proyectos": [Permission.READ],
            "informes": [Permission.READ],
        }
    
    # PROJECT_MANAGER: Gestión de proyectos
    elif role == UserRole.PROJECT_MANAGER:
        return {
            "clientes": [Permission.READ],
            "proyectos": [Permission.READ, Permission.CREATE, Permission.UPDATE],
            "tiempo": [Permission.READ, Permission.CREATE, Permission.UPDATE],
            "articulos": [Permission.READ],
            "presupuestos": [Permission.READ, Permission.CREATE],
            "informes": [Permission.READ],
        }
    
    # EMPLOYEE: Empleado básico
    elif role == UserRole.EMPLOYEE:
        return {
            "proyectos": [Permission.READ],  # Solo sus proyectos
            "tiempo": [Permission.READ, Permission.CREATE, Permission.UPDATE],  # Su tiempo
            "clientes": [Permission.READ],
        }
    
    # VIEWER: Solo lectura
    elif role == UserRole.VIEWER:
        return {
            "clientes": [Permission.READ],
            "facturas": [Permission.READ],
            "albaranes": [Permission.READ],
            "presupuestos": [Permission.READ],
            "articulos": [Permission.READ],
            "proyectos": [Permission.READ],
            "informes": [Permission.READ],
        }
    
    return {}


def _load_role_overrides() -> Dict[str, Dict]:
    """Carga overrides de permisos por rol desde `role_permissions.json` en la raíz del repo."""
    try:
        base = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(base, 'role_permissions.json')
        if not os.path.exists(path):
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception:
        return {}


# Aplicar overrides al cargar (si existen)
_ROLE_OVERRIDES = _load_role_overrides()


def _perm_from_str(s: str):
    """Map string to Permission enum if possible, else None."""
    try:
        # Normalize common names
        key = s.strip().upper()
        mapping = {
            'READ': Permission.READ,
            'CREATE': Permission.CREATE,
            'UPDATE': Permission.UPDATE,
            'DELETE': Permission.DELETE,
            'ADMIN': Permission.ADMIN,
            'EXPORT': Permission.EXPORT,
            'IMPORT': Permission.IMPORT,
            'PRINT': Permission.PRINT,
        }
        return mapping.get(key)
    except Exception:
        return None


def _apply_overrides_for_role(role: UserRole, base: Dict[str, List[Permission]]) -> Dict[str, List[Permission]]:
    """Merge overrides from `_ROLE_OVERRIDES` into the base permission map for `role`.

    Overrides file structure expected: { "admin": { "empresas": ["ADMIN"], ... }, ... }
    """
    try:
        role_key = role.value if isinstance(role, UserRole) else str(role)
        overrides = _ROLE_OVERRIDES.get(role_key, {})
        if not overrides:
            return base

        result = {k: list(v) for k, v in base.items()}
        for module_id, perm_list in overrides.items():
            if not isinstance(perm_list, list):
                continue
            converted = []
            for p in perm_list:
                if not isinstance(p, str):
                    continue
                perm = _perm_from_str(p)
                if perm is not None:
                    converted.append(perm)
            if not converted:
                continue
            if module_id in result:
                # union existing and overrides
                result[module_id] = list(set(result[module_id] + converted))
            else:
                result[module_id] = converted

        return result
    except Exception:
        return base


@dataclass
class Session:
    """
    Representa una sesión de usuario activa.
    """
    user: User
    login_time: datetime
    token: str  # Token de sesión para validación
    company_context: Optional['CompanyContext'] = None  # Contexto multi-empresa
    
    def is_valid(self) -> bool:
        """Verifica si la sesión es válida."""
        return self.user.is_active
    
    def has_permission(self, module_id: str, permission: Permission) -> bool:
        """Shortcut para verificar permisos desde la sesión."""
        return self.user.has_permission(module_id, permission)
    
    def get_company_name(self) -> str:
        """Obtiene el nombre de la empresa activa."""
        if self.company_context:
            return self.company_context.company.name
        return "Sin empresa"
    
    def get_group_name(self) -> str:
        """Obtiene el nombre del grupo activo."""
        if self.company_context:
            return self.company_context.group.name
        return "Sin grupo"


class AuthenticationManager:
    """
    Gestor de autenticación y sesiones.
    """
    
    def __init__(self):
        self._current_session: Optional[Session] = None
    
    def login(self, username: str, password: str, user_repository) -> Optional[Session]:
        """
        Intenta autenticar un usuario.
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            user_repository: Repositorio de usuarios (inyección de dependencia)
        
        Returns:
            Session si el login es exitoso, None en caso contrario
        """
        user = user_repository.get_by_username(username)
        
        if user and user.is_active and user.verify_password(password):
            token = secrets.token_urlsafe(32)
            session = Session(
                user=user,
                login_time=datetime.now(),
                token=token
            )
            self._current_session = session
            user.last_login = datetime.now()
            user_repository.update(user)
            return session
        
        return None
    
    def logout(self):
        """Cierra la sesión actual."""
        self._current_session = None
    
    def get_current_session(self) -> Optional[Session]:
        """Obtiene la sesión actual."""
        return self._current_session
    
    def require_permission(self, module_id: str, permission: Permission) -> bool:
        """
        Verifica si la sesión actual tiene un permiso.
        Útil para decoradores o validaciones.
        
        Returns:
            True si tiene permiso, False si no
        """
        if not self._current_session:
            return False
        
        return self._current_session.has_permission(module_id, permission)
