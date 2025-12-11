"""
Clase base para repositorios usando SQL directo.

Proporciona métodos comunes para acceso a base de datos sin ORM,
con soporte para multi-database vía MultiDBManager.
"""

from typing import List, Optional, Dict, Any
from core.db_manager import get_db_manager, MultiDBManager
import logging

logger = logging.getLogger(__name__)


class BaseRepository:
    """
    Clase base para repositorios con acceso SQL directo.

    Ventajas sobre ORM:
    - Flexibilidad total con multi-database
    - SQL visible y optimizable
    - Sin overhead de mapeo objeto-relacional
    - Fácil debugging
    """

    def __init__(self, db_manager: Optional[MultiDBManager] = None):
        """
        Inicializa el repositorio.

        Args:
            db_manager: Gestor de bases de datos (si None, usa el global)
        """
        self.db = db_manager or get_db_manager()

    def _execute(self, sql: str, params=None, use_main: bool = False) -> Any:
        """
        Ejecuta SQL y devuelve cursor.

        Args:
            sql: Sentencia SQL
            params: Parámetros
            use_main: Si True, ejecuta en DB principal

        Returns:
            Cursor con resultados
        """
        return self.db.execute(sql, params, use_main)

    def _fetch_all(self, sql: str, params=None, use_main: bool = False) -> List[dict]:
        """
        Ejecuta SELECT y devuelve lista de dicts.

        Args:
            sql: Sentencia SELECT
            params: Parámetros
            use_main: Si True, consulta en DB principal

        Returns:
            Lista de registros como diccionarios
        """
        return self.db.fetch_all(sql, params, use_main)

    def _fetch_one(self, sql: str, params=None, use_main: bool = False) -> Optional[dict]:
        """
        Ejecuta SELECT y devuelve un solo registro.

        Args:
            sql: Sentencia SELECT
            params: Parámetros
            use_main: Si True, consulta en DB principal

        Returns:
            Registro como diccionario o None
        """
        return self.db.fetch_one(sql, params, use_main)

    def _insert(self, table: str, data: dict, use_main: bool = False) -> int:
        """
        Inserta un registro.

        Args:
            table: Nombre de la tabla
            data: Diccionario con columna: valor
            use_main: Si True, inserta en DB principal

        Returns:
            ID del registro insertado
        """
        return self.db.insert(table, data, use_main)

    def _update(self, table: str, data: dict, where: str, params: tuple, use_main: bool = False) -> int:
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
        return self.db.update(table, data, where, params, use_main)

    def _delete(self, table: str, where: str, params: tuple, use_main: bool = False) -> int:
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
        return self.db.delete(table, where, params, use_main)

    def _model_to_dict(self, obj: Any, fields: List[str]) -> dict:
        """
        Convierte un objeto/modelo a diccionario.

        Args:
            obj: Objeto fuente
            fields: Lista de campos a extraer

        Returns:
            Diccionario con los campos
        """
        result = {}
        for field in fields:
            value = getattr(obj, field, None)
            if value is not None:
                result[field] = value
        return result

    def _sanitize_for_insert(self, data: dict, allowed_fields: List[str]) -> dict:
        """
        Filtra un diccionario para incluir solo campos permitidos.

        Args:
            data: Diccionario con datos
            allowed_fields: Lista de campos permitidos

        Returns:
            Diccionario filtrado
        """
        return {k: v for k, v in data.items() if k in allowed_fields}

    def _build_where_clause(self, filters: Dict[str, Any]) -> tuple[str, tuple]:
        """
        Construye una cláusula WHERE a partir de un diccionario de filtros.

        Args:
            filters: Diccionario con campo: valor

        Returns:
            Tupla (where_clause, params)

        Ejemplo:
            filters = {'activo': 1, 'empresa_id': 5}
            -> ("activo = %s AND empresa_id = %s", (1, 5))
        """
        if not filters:
            return ("1=1", ())

        conditions = []
        params = []

        for key, value in filters.items():
            if value is None:
                conditions.append(f"`{key}` IS NULL")
            else:
                conditions.append(f"`{key}` = %s")
                params.append(value)

        where_clause = " AND ".join(conditions)
        return (where_clause, tuple(params))

    def exists(self, table: str, where: str, params: tuple, use_main: bool = False) -> bool:
        """
        Verifica si existe al menos un registro que cumple la condición.

        Args:
            table: Nombre de la tabla
            where: Cláusula WHERE
            params: Parámetros
            use_main: Si True, consulta en DB principal

        Returns:
            True si existe, False si no
        """
        sql = f"SELECT 1 FROM `{table}` WHERE {where} LIMIT 1"
        result = self._fetch_one(sql, params, use_main)
        return result is not None

    def count(self, table: str, where: str = "1=1", params: tuple = (), use_main: bool = False) -> int:
        """
        Cuenta registros que cumplen la condición.

        Args:
            table: Nombre de la tabla
            where: Cláusula WHERE (por defecto cuenta todos)
            params: Parámetros
            use_main: Si True, consulta en DB principal

        Returns:
            Número de registros
        """
        sql = f"SELECT COUNT(*) as total FROM `{table}` WHERE {where}"
        result = self._fetch_one(sql, params, use_main)
        return result['total'] if result else 0

