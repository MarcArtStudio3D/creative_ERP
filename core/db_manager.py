"""
Sistema de gestión de múltiples bases de datos para aplicación multi-empresa.

Este módulo proporciona una capa de abstracción para trabajar con múltiples
bases de datos SQLite/MariaDB de forma simultánea, permitiendo:
- Cambio fluido entre bases de datos de diferentes empresas
- Consultas cross-database (ATTACH en SQLite)
- Pool de conexiones por empresa
- Acceso a DB principal (main) y DBs de empresa
"""

import sqlite3
from dataclasses import dataclass
from typing import Dict, Optional, Any, List
import pymysql
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


@dataclass
class ConnectionConfig:
    """Configuración de conexión para una base de datos."""
    empresa_id: int
    db_type: str  # 'sqlite', 'mariadb', 'postgresql'
    connection: Optional[Any] = None

    # SQLite
    db_path: Optional[str] = None

    # MariaDB/PostgreSQL
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None


class MultiDBManager:
    """Gestiona conexiones a múltiples bases de datos."""

    def __init__(self, main_db_config: dict):
        """
        Inicializa el gestor con la configuración de la DB principal.

        Args:
            main_db_config: dict con 'type', 'path' (SQLite) o 'host', 'port',
                          'database', 'user', 'password' (MariaDB)
        """
        self.main_db_config = main_db_config
        self.main_db_type = main_db_config.get('type', 'sqlite')
        self.main_connection = self._create_connection(main_db_config)

        # Pool de conexiones por empresa
        self.empresa_connections: Dict[int, ConnectionConfig] = {}
        self.current_empresa_id: Optional[int] = None

        logger.info(f"MultiDBManager inicializado con DB principal tipo: {self.main_db_type}")

    def _create_connection(self, config: dict) -> Any:
        """Crea una conexión según el tipo de base de datos."""
        db_type = config.get('type', 'sqlite')

        if db_type == 'sqlite':
            conn = sqlite3.connect(config['path'], check_same_thread=False)
            conn.row_factory = sqlite3.Row  # Acceso por nombre de columna
            # Habilitar claves foráneas
            conn.execute("PRAGMA foreign_keys = ON")
            return conn

        elif db_type == 'mariadb' or db_type == 'mysql':
            conn = pymysql.connect(
                host=config['host'],
                port=config.get('port', 3306),
                user=config['user'],
                password=config['password'],
                database=config['database'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )
            return conn

        else:
            raise ValueError(f"Tipo de DB no soportado: {db_type}")

    def register_empresa(self, empresa_id: int, db_config: dict):
        """
        Registra una empresa y su base de datos.

        Args:
            empresa_id: ID de la empresa
            db_config: dict con configuración de la DB de la empresa
        """
        db_type = db_config.get('type', 'sqlite')
        connection = self._create_connection(db_config)

        config = ConnectionConfig(
            empresa_id=empresa_id,
            db_type=db_type,
            connection=connection,
            db_path=db_config.get('path'),
            host=db_config.get('host'),
            port=db_config.get('port'),
            database=db_config.get('database'),
            user=db_config.get('user'),
            password=db_config.get('password')
        )

        self.empresa_connections[empresa_id] = config
        logger.debug(f"Empresa {empresa_id} registrada con DB tipo: {db_type}")

    def switch_empresa(self, empresa_id: int):
        """
        Cambia la empresa activa.

        Args:
            empresa_id: ID de la empresa a activar
        """
        if empresa_id not in self.empresa_connections:
            raise ValueError(f"Empresa {empresa_id} no registrada. Usa register_empresa() primero.")

        self.current_empresa_id = empresa_id
        logger.debug(f"Cambiado a empresa {empresa_id}")

    def get_main_conn(self) -> Any:
        """Obtiene la conexión a la base de datos principal."""
        return self.main_connection

    def get_current_conn(self) -> Any:
        """Obtiene la conexión a la DB de la empresa activa."""
        if not self.current_empresa_id:
            raise RuntimeError("No hay empresa activa. Usa switch_empresa() primero.")
        return self.empresa_connections[self.current_empresa_id].connection

    def get_empresa_conn(self, empresa_id: int) -> Any:
        """Obtiene la conexión a una empresa específica."""
        if empresa_id not in self.empresa_connections:
            raise ValueError(f"Empresa {empresa_id} no registrada")
        return self.empresa_connections[empresa_id].connection

    @contextmanager
    def transaction(self, use_main: bool = False):
        """
        Context manager para transacciones.

        Args:
            use_main: Si True, usa la DB principal; si False, usa la DB de empresa actual

        Uso:
            with db_manager.transaction():
                db_manager.execute("INSERT ...")
                db_manager.execute("UPDATE ...")
            # Auto-commit si no hay excepciones, rollback si hay error
        """
        conn = self.get_main_conn() if use_main else self.get_current_conn()

        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Rollback en transacción: {e}")
            raise

    def execute(self, sql: str, params=None, use_main: bool = False) -> Any:
        """
        Ejecuta SQL y devuelve cursor.

        Args:
            sql: Sentencia SQL
            params: Parámetros (tupla o dict)
            use_main: Si True, ejecuta en DB principal

        Returns:
            Cursor con resultados
        """
        conn = self.get_main_conn() if use_main else self.get_current_conn()
        cursor = conn.cursor()

        try:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            logger.debug(f"SQL ejecutado: {sql[:100]}...")
            return cursor

        except Exception as e:
            logger.error(f"Error ejecutando SQL: {sql}\nParams: {params}\nError: {e}")
            raise

    def fetch_all(self, sql: str, params=None, use_main: bool = False) -> List[dict]:
        """
        Ejecuta SELECT y devuelve lista de diccionarios.

        Args:
            sql: Sentencia SELECT
            params: Parámetros
            use_main: Si True, consulta en DB principal

        Returns:
            Lista de registros como diccionarios
        """
        cursor = self.execute(sql, params, use_main)

        if self.main_db_type == 'sqlite' or (not use_main and self.get_current_empresa_db_type() == 'sqlite'):
            # SQLite con row_factory ya devuelve Row objects
            return [dict(row) for row in cursor.fetchall()]
        else:
            # MariaDB con DictCursor ya devuelve dicts
            return cursor.fetchall()

    def fetch_one(self, sql: str, params=None, use_main: bool = False) -> Optional[dict]:
        """
        Ejecuta SELECT y devuelve un solo registro.

        Args:
            sql: Sentencia SELECT
            params: Parámetros
            use_main: Si True, consulta en DB principal

        Returns:
            Registro como diccionario o None
        """
        cursor = self.execute(sql, params, use_main)
        row = cursor.fetchone()

        if not row:
            return None

        if self.main_db_type == 'sqlite' or (not use_main and self.get_current_empresa_db_type() == 'sqlite'):
            return dict(row)
        else:
            return row

    def insert(self, table: str, data: dict, use_main: bool = False) -> int:
        """
        Inserta un registro y devuelve el ID generado.

        Args:
            table: Nombre de la tabla
            data: Diccionario con columna: valor
            use_main: Si True, inserta en DB principal

        Returns:
            ID del registro insertado
        """
        cols = ", ".join(f"`{k}`" for k in data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO `{table}` ({cols}) VALUES ({placeholders})"

        cursor = self.execute(sql, tuple(data.values()), use_main)
        conn = self.get_main_conn() if use_main else self.get_current_conn()
        conn.commit()

        return cursor.lastrowid

    def update(self, table: str, data: dict, where: str, params: tuple, use_main: bool = False) -> int:
        """
        Actualiza registros.

        Args:
            table: Nombre de la tabla
            data: Diccionario con columna: valor a actualizar
            where: Cláusula WHERE (ej: "id = %s")
            params: Parámetros para WHERE
            use_main: Si True, actualiza en DB principal

        Returns:
            Número de filas afectadas
        """
        set_clause = ", ".join(f"`{k}` = %s" for k in data.keys())
        sql = f"UPDATE `{table}` SET {set_clause} WHERE {where}"

        cursor = self.execute(sql, (*data.values(), *params), use_main)
        conn = self.get_main_conn() if use_main else self.get_current_conn()
        conn.commit()

        return cursor.rowcount

    def delete(self, table: str, where: str, params: tuple, use_main: bool = False) -> int:
        """
        Elimina registros.

        Args:
            table: Nombre de la tabla
            where: Cláusula WHERE
            params: Parámetros
            use_main: Si True, elimina de DB principal

        Returns:
            Número de filas eliminadas
        """
        sql = f"DELETE FROM `{table}` WHERE {where}"
        cursor = self.execute(sql, params, use_main)
        conn = self.get_main_conn() if use_main else self.get_current_conn()
        conn.commit()

        return cursor.rowcount

    def get_current_empresa_db_type(self) -> str:
        """Obtiene el tipo de DB de la empresa actual."""
        if not self.current_empresa_id:
            raise RuntimeError("No hay empresa activa")
        return self.empresa_connections[self.current_empresa_id].db_type

    def attach_database(self, target_empresa_id: int, alias: str):
        """
        Adjunta otra base de datos para consultas cross-database (solo SQLite).

        Args:
            target_empresa_id: ID de la empresa cuya DB se adjuntará
            alias: Alias para usar en las queries (ej: 'emp2')

        Nota: Solo funciona con SQLite. Para MariaDB usa FEDERATED o consultas separadas.
        """
        if self.get_current_empresa_db_type() != 'sqlite':
            raise NotImplementedError("ATTACH DATABASE solo funciona con SQLite")

        if target_empresa_id not in self.empresa_connections:
            raise ValueError(f"Empresa {target_empresa_id} no registrada")

        target_config = self.empresa_connections[target_empresa_id]
        if target_config.db_type != 'sqlite':
            raise ValueError("Solo se pueden adjuntar DBs SQLite")

        current_conn = self.get_current_conn()
        current_conn.execute(f"ATTACH DATABASE '{target_config.db_path}' AS {alias}")

        logger.debug(f"DB de empresa {target_empresa_id} adjuntada como '{alias}'")

    def detach_database(self, alias: str):
        """
        Desadjunta una base de datos previamente adjuntada (solo SQLite).

        Args:
            alias: Alias de la DB a desadjuntar
        """
        if self.get_current_empresa_db_type() != 'sqlite':
            return

        current_conn = self.get_current_conn()
        current_conn.execute(f"DETACH DATABASE {alias}")
        logger.debug(f"DB '{alias}' desadjuntada")

    def close_all(self):
        """Cierra todas las conexiones."""
        try:
            self.main_connection.close()
            logger.debug("Conexión principal cerrada")
        except Exception as e:
            logger.error(f"Error cerrando conexión principal: {e}")

        for empresa_id, config in self.empresa_connections.items():
            try:
                config.connection.close()
                logger.debug(f"Conexión empresa {empresa_id} cerrada")
            except Exception as e:
                logger.error(f"Error cerrando conexión empresa {empresa_id}: {e}")


# Instancia global (se inicializa en app startup)
_db_manager: Optional[MultiDBManager] = None


def init_db_manager(main_db_config: dict) -> MultiDBManager:
    """
    Inicializa el gestor global de bases de datos.

    Args:
        main_db_config: Configuración de la DB principal

    Returns:
        Instancia de MultiDBManager
    """
    global _db_manager
    _db_manager = MultiDBManager(main_db_config)
    return _db_manager


def get_db_manager() -> MultiDBManager:
    """
    Obtiene la instancia global del gestor de bases de datos.

    Returns:
        MultiDBManager instance

    Raises:
        RuntimeError: Si no se ha inicializado
    """
    if _db_manager is None:
        raise RuntimeError("DB Manager no inicializado. Llama a init_db_manager() primero.")
    return _db_manager

