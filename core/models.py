"""
Modelos y utilidades para el core de la aplicación.
Ahora usamos diccionarios en lugar de modelos ORM.
"""

from datetime import datetime
from typing import Dict, Optional
from werkzeug.security import check_password_hash, generate_password_hash


def verify_password(password_hash: str, password: str) -> bool:
    """
    Verifica una contraseña contra su hash.
    Soporta dos formatos:
    - Werkzeug (pbkdf2:sha256:..., scrypt:...)
    - Legacy SHA256 con salt (salt$hash)

    Args:
        password_hash: Hash almacenado
        password: Contraseña en texto plano

    Returns:
        True si la contraseña es correcta
    """
    if not password_hash:
        return False

    # Formato werkzeug (moderno)
    if password_hash.startswith(('pbkdf2:', 'scrypt:', 'argon2:')):
        return check_password_hash(password_hash, password)

    # Formato legacy (salt$hash)
    if '$' in password_hash:
        try:
            import hashlib
            salt, stored_hash = password_hash.split('$', 1)
            computed_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return computed_hash == stored_hash
        except:
            return False

    # Intentar con werkzeug de todas formas (puede no tener prefijo)
    try:
        return check_password_hash(password_hash, password)
    except:
        return False



def hash_password(password: str) -> str:
    """
    Genera un hash seguro de una contraseña.

    Args:
        password: Contraseña en texto plano

    Returns:
        Hash de la contraseña
    """
    return generate_password_hash(password)


def create_user_dict(
    username: str,
    email: str,
    full_name: str,
    password: str,
    role: str = "user",
    is_active: bool = True,
    allowed_groups: str = "[]"
) -> Dict:
    """
    Crea un diccionario con datos de usuario listo para insertar en BD.

    Args:
        username: Nombre de usuario
        email: Email
        full_name: Nombre completo
        password: Contraseña en texto plano (se hasheará)
        role: Rol del usuario
        is_active: Si el usuario está activo
        allowed_groups: JSON array de IDs de grupos permitidos

    Returns:
        Diccionario con los datos del usuario
    """
    return {
        'username': username,
        'email': email,
        'full_name': full_name,
        'password_hash': hash_password(password),
        'role': role,
        'is_active': 1 if is_active else 0,
        'created_at': datetime.utcnow(),
        'last_login': None,
        'allowed_groups': allowed_groups
    }


# Mantener compatibilidad con código legacy que importa estos nombres
# pero ya no son clases Model de Peewee
User = dict
BusinessGroup = dict
Empresa = dict
Cliente = dict
Articulo = dict

