"""
Sistema de gestión de base de datos con Peewee.
Reemplazo completo de SQLModel/SQLAlchemy.
"""

import logging
import os
import re
from typing import Optional
from urllib.parse import urlparse, parse_qs

from peewee import MySQLDatabase, SqliteDatabase, DatabaseProxy

from .config import config as env_config

logger = logging.getLogger(__name__)

# Proxy de base de datos que permite cambiar la BD en tiempo de ejecución
database_proxy = DatabaseProxy()

# Configuraciones de base de datos disponibles
DATABASE_CONFIGS = {
    "main": env_config.get_database_url("main"),
    "artstudio3d": env_config.get_database_url("artstudio3d"),
}

# Base de datos por defecto
DEFAULT_DB = os.environ.get("CREATIVE_ERP_DEFAULT_DB", "main")

# Base de datos actual
_current_db = DEFAULT_DB
_current_database = None


def get_database_url(db_name: str = "main") -> str:
    """Obtiene la URL de conexión para una base de datos específica."""
    return DATABASE_CONFIGS.get(db_name, DATABASE_CONFIGS["main"])


def get_current_database() -> str:
    """Obtiene el nombre de la base de datos actual."""
    return _current_db


def _convert_sqlalchemy_url_to_peewee(db_url: str):
    """
    Convierte una URL de SQLAlchemy a una conexión Peewee.

    Ejemplos:
    - mysql+pymysql://user:pass@host:port/dbname -> MySQLDatabase
    - sqlite:///path/to/db.sqlite -> SqliteDatabase
    """
    try:
        # Reemplazar mysql+pymysql por mysql para parsing
        url = db_url.replace("mysql+pymysql://", "mysql://")

        parsed = urlparse(url)

        # SQLite
        if parsed.scheme == "sqlite":
            db_path = parsed.path
            if db_path.startswith("///"):
                db_path = db_path[3:]  # Absoluto
            elif db_path.startswith("//"):
                db_path = db_path[2:]  # Relativo

            return SqliteDatabase(db_path)

        # MySQL/MariaDB
        elif parsed.scheme == "mysql":
            # Extraer componentes
            username = parsed.username or "root"
            password = parsed.password or ""
            host = parsed.hostname or "localhost"
            port = parsed.port or 3306
            database = parsed.path.lstrip("/") if parsed.path else None

            if not database:
                raise ValueError(f"No database specified in URL: {db_url}")

            return MySQLDatabase(
                database,
                user=username,
                password=password,
                host=host,
                port=port,
                charset='utf8mb4'
            )

        else:
            raise ValueError(f"Unsupported scheme: {parsed.scheme}")

    except Exception as e:
        logger.exception("Error converting URL %s: %s", db_url, e)
        raise


def create_database(db_url: str):
    """Crea una conexión de base de datos Peewee desde una URL."""
    try:
        db = _convert_sqlalchemy_url_to_peewee(db_url)
        return db
    except Exception as e:
        logger.exception("Error creating database connection: %s", e)
        raise


def set_database_for_company(company_id: int) -> bool:
    """
    Cambia la base de datos según la empresa seleccionada.
    Obtiene la configuración desde la tabla de empresas en la BD main.

    Args:
        company_id: ID de la empresa

    Returns:
        True si se cambió correctamente
    """
    global _current_db, _current_database

    try:
        # PASO 1: Cambiar temporalmente a BD main para consultar la tabla empresas
        original_db_name = _current_db

        # Si no estamos en main, cambiar a main primero
        if _current_db != "main":
            set_current_database("main")

        # PASO 2: Consultar la configuración de la empresa
        from core.models import Empresa

        try:
            empresa = Empresa.get_by_id(company_id)
        except Exception as e:
            logger.error("No se encontró empresa con ID %s: %s", company_id, e)
            return False

        # PASO 3: Construir la URL de la BD según el motor configurado
        motor = empresa.motor_base_datos.lower()

        if motor == "mariadb" or motor == "mysql":
            db_url = (
                f"mysql+pymysql://{empresa.usuario_mariadb}:{empresa.password_mariadb}"
                f"@{empresa.host_mariadb}:{empresa.puerto_mariadb}/{empresa.nombre_base_datos_maria_db}"
            )
        elif motor == "postgresql":
            db_url = (
                f"postgresql://{empresa.usuario_postgresql}:{empresa.password_postgresql}"
                f"@{empresa.host_postgresql}:{empresa.puerto_postgresql}/{empresa.nombre_base_datos_postgresql}"
            )
        elif motor == "sqlite":
            db_url = f"sqlite:///{empresa.ruta_base_datos_sqlite}"
        else:
            logger.error("Motor de BD no soportado: %s", motor)
            return False

        # PASO 4: Registrar la BD de la empresa
        db_name = f"company_{company_id}"
        DATABASE_CONFIGS[db_name] = db_url

        # PASO 5: Cambiar a la BD de la empresa
        return set_current_database(db_name)

    except Exception as e:
        logger.exception("Error setting database for company %s: %s", company_id, e)
        return False


def set_current_database(db_name: str) -> bool:
    """
    Cambia la base de datos actual.

    Args:
        db_name: Nombre de la base de datos

    Returns:
        True si se cambió correctamente
    """
    global _current_db, _current_database

    if db_name not in DATABASE_CONFIGS:
        logger.error(
            "Base de datos '%s' no configurada. Opciones: %s",
            db_name,
            list(DATABASE_CONFIGS.keys())
        )
        return False

    try:
        # Cerrar conexión anterior si existe
        if _current_database is not None:
            try:
                _current_database.close()
            except Exception:
                pass

        # Crear nueva conexión
        db_url = get_database_url(db_name)
        _current_database = create_database(db_url)

        # Inicializar el proxy
        database_proxy.initialize(_current_database)

        _current_db = db_name
        logger.debug("Database switched to: %s (%s)", db_name, db_url)

        return True

    except Exception as e:
        logger.exception("Error switching database to %s: %s", db_name, e)
        return False


def get_database():
    """Obtiene la instancia de base de datos actual."""
    global _current_database

    if _current_database is None:
        # Inicializar con la BD por defecto
        set_current_database(DEFAULT_DB)

    return _current_database


def ensure_initialized():
    """
    Asegura que el database_proxy está inicializado correctamente.
    Si no hay BD actual, inicializa con la BD por defecto.
    """
    global _current_database

    if _current_database is None or not database_proxy.obj:
        logger.debug("Initializing database proxy with default DB")
        set_current_database(DEFAULT_DB)

    return database_proxy


def init_database(db_name: str = DEFAULT_DB) -> bool:
    """
    Inicializa el sistema de base de datos.

    Args:
        db_name: Nombre de la base de datos inicial

    Returns:
        True si se inicializó correctamente
    """
    try:
        success = set_current_database(db_name)
        if success:
            logger.info("Database system initialized with: %s", db_name)
        return success
    except Exception as e:
        logger.exception("Error initializing database: %s", e)
        return False


def close_database():
    """Cierra la conexión de base de datos actual."""
    global _current_database

    if _current_database is not None:
        try:
            _current_database.close()
            _current_database = None
            logger.debug("Database connection closed")
        except Exception as e:
            logger.exception("Error closing database: %s", e)


# NO inicializar automáticamente al importar - dejar que la app lo haga explícitamente
# Esto evita errores en imports antes de que la configuración esté lista
_initialized = False

def ensure_initialized():
    """Asegurar que la BD está inicializada. Llamar antes de usar.

    Solo inicializa si el proxy nunca ha sido configurado. Si ya hay una BD
    activa (por ejemplo, seleccionada por company_manager), la respeta.
    """
    global _initialized, _current_database

    # Si ya tenemos una BD activa, no hacer nada
    if _current_database is not None:
        return

    # Solo inicializar si nunca se ha inicializado
    if not _initialized:
        try:
            init_database()
            _initialized = True
        except Exception as e:
            logger.error("Failed to initialize database: %s", e)

