"""
Repository SQL directo para Divisiones del Almacén (Secciones, Familias, Subfamilias)
Migrado de Peewee a SQL directo con MultiDBManager.
Retorna objetos Dataclass para mantener arquitectura MVC pura.
"""
from typing import List, Optional
import logging
from core.base_repository import BaseRepository
from modules.articulos.models import Seccion, Familia, Subfamilia
logger = logging.getLogger(__name__)
class DivisionesRepository(BaseRepository):
    """Repository para gestionar Secciones, Familias y Subfamilias con SQL directo"""
    def __init__(self):
        """Inicializa el repository con el DB manager global."""
        super().__init__()
    # ==================== SECCIONES ====================
    def obtener_todas_secciones(self) -> List[Seccion]:
        """Obtiene todas las secciones ordenadas por código"""
        try:
            query = "SELECT * FROM secciones ORDER BY codigo"
            rows = self._fetch_all(query)
            return [Seccion.from_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error obteniendo secciones: {e}")
            return []
    def obtener_seccion_por_id(self, id_: int) -> Optional[Seccion]:
        """Obtiene una sección por ID"""
        try:
            query = "SELECT * FROM secciones WHERE id = %s"
            row = self._fetch_one(query, (id_,))
            return Seccion.from_dict(row) if row else None
        except Exception as e:
            logger.error(f"Error obteniendo sección {id_}: {e}")
            return None
    def obtener_seccion_por_codigo(self, codigo: str) -> Optional[Seccion]:
        """Obtiene una sección por código"""
        try:
            query = "SELECT * FROM secciones WHERE codigo = %s"
            row = self._fetch_one(query, (codigo,))
            return Seccion.from_dict(row) if row else None
        except Exception as e:
            logger.error(f"Error obteniendo sección por código: {e}")
            return None
    def guardar_seccion(self, seccion: Seccion) -> Optional[Seccion]:
        """Guarda o actualiza una sección"""
        try:
            data = seccion.to_dict()
            if seccion.id:
                # Actualizar
                self._update('secciones', data, 'id = %s', (seccion.id,))
                return self.obtener_seccion_por_id(seccion.id)
            else:
                # Crear
                new_id = self._insert('secciones', data)
                return self.obtener_seccion_por_id(new_id)
        except Exception as e:
            logger.error(f"Error guardando sección: {e}")
            return None
    def borrar_seccion(self, seccion_id: int) -> bool:
        """Borra una sección y todas sus familias y subfamilias asociadas"""
        try:
            # Primero borrar subfamilias de familias de esta sección
            query = """
                DELETE sf FROM subfamilias sf
                INNER JOIN familias f ON sf.id_familia = f.id
                WHERE f.id_seccion = %s
            """
            self._execute(query, (seccion_id,))
            # Luego borrar familias de esta sección
            self._delete('familias', 'id_seccion = %s', (seccion_id,))
            # Finalmente borrar la sección
            rows_deleted = self._delete('secciones', 'id = %s', (seccion_id,))
            return rows_deleted > 0
        except Exception as e:
            logger.error(f"Error borrando sección: {e}")
            return False
    # ==================== FAMILIAS ====================
    def obtener_todas_familias(self) -> List[Familia]:
        """Obtiene todas las familias ordenadas por código"""
        try:
            query = "SELECT * FROM familias ORDER BY codigo"
            rows = self._fetch_all(query)
            return [Familia.from_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error obteniendo familias: {e}")
            return []
    def obtener_familias_por_seccion(self, id_seccion: int) -> List[Familia]:
        """Obtiene todas las familias de una sección"""
        try:
            query = "SELECT * FROM familias WHERE id_seccion = %s ORDER BY codigo"
            rows = self._fetch_all(query, (id_seccion,))
            return [Familia.from_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error obteniendo familias de sección: {e}")
            return []
    def obtener_familia_por_id(self, id_: int) -> Optional[Familia]:
        """Obtiene una familia por ID"""
        try:
            query = "SELECT * FROM familias WHERE id = %s"
            row = self._fetch_one(query, (id_,))
            return Familia.from_dict(row) if row else None
        except Exception as e:
            logger.error(f"Error obteniendo familia {id_}: {e}")
            return None
    def obtener_familia_por_codigo(self, codigo: str) -> Optional[Familia]:
        """Obtiene una familia por código"""
        try:
            query = "SELECT * FROM familias WHERE codigo = %s"
            row = self._fetch_one(query, (codigo,))
            return Familia.from_dict(row) if row else None
        except Exception as e:
            logger.error(f"Error obteniendo familia por código: {e}")
            return None
    def guardar_familia(self, familia: Familia) -> Optional[Familia]:
        """Guarda o actualiza una familia"""
        try:
            data = familia.to_dict()
            if familia.id:
                # Actualizar
                self._update('familias', data, 'id = %s', (familia.id,))
                return self.obtener_familia_por_id(familia.id)
            else:
                # Crear
                new_id = self._insert('familias', data)
                return self.obtener_familia_por_id(new_id)
        except Exception as e:
            logger.error(f"Error guardando familia: {e}")
            return None
    def borrar_familia(self, familia_id: int) -> bool:
        """Borra una familia y todas sus subfamilias asociadas"""
        try:
            # Primero borrar subfamilias
            self._delete('subfamilias', 'id_familia = %s', (familia_id,))
            # Luego borrar la familia
            rows_deleted = self._delete('familias', 'id = %s', (familia_id,))
            return rows_deleted > 0
        except Exception as e:
            logger.error(f"Error borrando familia: {e}")
            return False
    # ==================== SUBFAMILIAS ====================
    def obtener_todas_subfamilias(self) -> List[Subfamilia]:
        """Obtiene todas las subfamilias ordenadas por código"""
        try:
            query = "SELECT * FROM subfamilias ORDER BY codigo"
            rows = self._fetch_all(query)
            return [Subfamilia.from_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error obteniendo subfamilias: {e}")
            return []
    def obtener_subfamilias_por_familia(self, id_familia: int) -> List[Subfamilia]:
        """Obtiene todas las subfamilias de una familia"""
        try:
            query = "SELECT * FROM subfamilias WHERE id_familia = %s ORDER BY codigo"
            rows = self._fetch_all(query, (id_familia,))
            return [Subfamilia.from_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error obteniendo subfamilias de familia: {e}")
            return []
    def obtener_subfamilia_por_id(self, id_: int) -> Optional[Subfamilia]:
        """Obtiene una subfamilia por ID"""
        try:
            query = "SELECT * FROM subfamilias WHERE id = %s"
            row = self._fetch_one(query, (id_,))
            return Subfamilia.from_dict(row) if row else None
        except Exception as e:
            logger.error(f"Error obteniendo subfamilia {id_}: {e}")
            return None
    def obtener_subfamilias_por_codigo(self, codigo: str) -> Optional[Subfamilia]:
        """Obtiene una subfamilia por código"""
        try:
            query = "SELECT * FROM subfamilias WHERE codigo = %s"
            row = self._fetch_one(query, (codigo,))
            return Subfamilia.from_dict(row) if row else None
        except Exception as e:
            logger.error(f"Error obteniendo subfamilia por código: {e}")
            return None
    def guardar_subfamilia(self, subfamilia: Subfamilia) -> Optional[Subfamilia]:
        """Guarda o actualiza una subfamilia"""
        try:
            data = subfamilia.to_dict()
            if subfamilia.id:
                # Actualizar
                self._update('subfamilias', data, 'id = %s', (subfamilia.id,))
                return self.obtener_subfamilia_por_id(subfamilia.id)
            else:
                # Crear
                new_id = self._insert('subfamilias', data)
                return self.obtener_subfamilia_por_id(new_id)
        except Exception as e:
            logger.error(f"Error guardando subfamilia: {e}")
            return None
    def borrar_subfamilia(self, subfamilia_id: int) -> bool:
        """Borra una subfamilia"""
        try:
            rows_deleted = self._delete('subfamilias', 'id = %s', (subfamilia_id,))
            return rows_deleted > 0
        except Exception as e:
            logger.error(f"Error borrando subfamilia: {e}")
            return False
