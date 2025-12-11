"""
Repository Peewee para el módulo de Artículos.
Maneja todas las operaciones CRUD siguiendo el patrón MVC.
"""

import logging
from datetime import date
from typing import Dict, List, Optional

from peewee import DoesNotExist, fn

from core.peewee_db import ensure_initialized

from .models import (
    Articulo,
    Seccion,
    Familia,
    Subfamilia,
    ArticuloTipo,
    Tarifa,
    TarifaTipo,
    Promocion,
)

logger = logging.getLogger(__name__)


class ArticuloRepository:
    """Repositorio para operaciones con artículos usando Peewee."""

    def __init__(self):
        """Inicializar repositorio."""
        # Asegurar que la BD esté inicializada
        ensure_initialized()

    # ==================== CRUD Básico ====================

    def get_by_id(self, articulo_id: int) -> Optional[Dict]:
        """Obtener un artículo por su ID."""
        try:
            articulo = Articulo.get_by_id(articulo_id)
            return self._model_to_dict(articulo)
        except DoesNotExist:
            return None
        except Exception as e:
            logger.exception("Error getting articulo by id %s: %s", articulo_id, e)
            return None

    def get_by_codigo(self, codigo: str) -> Optional[Dict]:
        """Obtener un artículo por su código."""
        try:
            articulo = Articulo.get(Articulo.codigo == codigo)
            return self._model_to_dict(articulo)
        except DoesNotExist:
            return None
        except Exception as e:
            logger.exception("Error getting articulo by codigo %s: %s", codigo, e)
            return None

    def get_all(
        self,
        limit: int = None,
        offset: int = 0,
        order_by: str = "descripcion_reducida",
        order_dir: str = "ASC",
        filtro: str = ""
    ) -> List[Dict]:
        """Obtener todos los artículos con paginación y filtros opcionales."""
        try:
            query = Articulo.select()

            # Aplicar filtro si existe
            if filtro:
                query = query.where(
                    (Articulo.codigo.contains(filtro)) |
                    (Articulo.descripcion_reducida.contains(filtro)) |
                    (Articulo.codigo_barras.contains(filtro))
                )

            # Ordenar
            order_field = getattr(Articulo, order_by, Articulo.descripcion_reducida)
            if order_dir.upper() == "DESC":
                query = query.order_by(order_field.desc())
            else:
                query = query.order_by(order_field)

            # Paginar
            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)

            return [self._model_to_dict(a) for a in query]

        except Exception as e:
            logger.exception("Error getting all articulos: %s", e)
            return []

    def count_all(self, filtro: str = "") -> int:
        """Contar el total de artículos."""
        try:
            query = Articulo.select()

            if filtro:
                query = query.where(
                    (Articulo.codigo.contains(filtro)) |
                    (Articulo.descripcion_reducida.contains(filtro)) |
                    (Articulo.codigo_barras.contains(filtro))
                )

            return query.count()

        except Exception as e:
            logger.exception("Error counting articulos: %s", e)
            return 0

    def get_next(self, current_id: int) -> Optional[Dict]:
        """Obtener el siguiente artículo después del ID actual."""
        try:
            articulo = (
                Articulo.select()
                .where(Articulo.id > current_id)
                .order_by(Articulo.id)
                .first()
            )
            return self._model_to_dict(articulo) if articulo else None

        except Exception as e:
            logger.exception("Error getting next articulo: %s", e)
            return None

    def get_prev(self, current_id: int) -> Optional[Dict]:
        """Obtener el artículo anterior al ID actual."""
        try:
            articulo = (
                Articulo.select()
                .where(Articulo.id < current_id)
                .order_by(Articulo.id.desc())
                .first()
            )
            return self._model_to_dict(articulo) if articulo else None

        except Exception as e:
            logger.exception("Error getting prev articulo: %s", e)
            return None

    def create(self, data: Dict = None) -> Optional[int]:
        """Crear un nuevo artículo."""
        try:
            # Generar código temporal si no se proporciona
            if not data:
                data = {}

            if "codigo" not in data or not data["codigo"]:
                # Generar código temporal único
                max_id = Articulo.select(fn.MAX(Articulo.id)).scalar() or 0
                data["codigo"] = f"TEMP{max_id + 1:06d}"

            # Valores por defecto
            defaults = {
                "descripcion_reducida": "Nuevo artículo",
                "fecha_alta": date.today(),
                "activo": True,
                "precio_venta": 0.0,
                "coste": 0.0,
                "stock_real": 0.0,
            }

            for key, value in defaults.items():
                if key not in data:
                    data[key] = value

            articulo = Articulo.create(**data)
            return articulo.id

        except Exception as e:
            logger.exception("Error creating articulo: %s", e)
            return None

    def update(self, articulo_id: int, data: Dict) -> bool:
        """Actualizar un artículo existente."""
        try:
            query = Articulo.update(**data).where(Articulo.id == articulo_id)
            rows = query.execute()
            return rows > 0

        except Exception as e:
            logger.exception("Error updating articulo %s: %s", articulo_id, e)
            return False

    def delete(self, articulo_id: int) -> bool:
        """Eliminar un artículo."""
        try:
            articulo = Articulo.get_by_id(articulo_id)
            articulo.delete_instance()
            return True

        except DoesNotExist:
            return False
        except Exception as e:
            logger.exception("Error deleting articulo %s: %s", articulo_id, e)
            return False

    # ==================== Tarifas ====================

    def get_tarifas(self, articulo_id: int) -> List[Dict]:
        """Obtener todas las tarifas de un artículo."""
        try:
            tarifas = (
                Tarifa.select(Tarifa, TarifaTipo)
                .join(TarifaTipo)
                .where(Tarifa.id_articulo == articulo_id)
            )

            result = []
            for tarifa in tarifas:
                result.append({
                    "id": tarifa.id,
                    "id_tarifa_tipo": tarifa.id_tarifa_tipo.id,
                    "codigo": tarifa.id_tarifa_tipo.codigo,
                    "descripcion": tarifa.id_tarifa_tipo.descripcion,
                    "precio": tarifa.precio,
                    "porc_dto": tarifa.porc_dto,
                    "precio_final": tarifa.precio_final,
                })

            return result

        except Exception as e:
            logger.exception("Error getting tarifas for articulo %s: %s", articulo_id, e)
            return []

    def update_tarifa(self, tarifa_id: int, data: Dict) -> bool:
        """Actualizar una tarifa."""
        try:
            query = Tarifa.update(**data).where(Tarifa.id == tarifa_id)
            rows = query.execute()
            return rows > 0

        except Exception as e:
            logger.exception("Error updating tarifa %s: %s", tarifa_id, e)
            return False

    def create_tarifas_for_article(self, articulo_id: int) -> bool:
        """Crear tarifas por defecto para un artículo nuevo."""
        try:
            # Obtener todos los tipos de tarifa activos
            tipos = TarifaTipo.select().where(TarifaTipo.activa == True)

            for tipo in tipos:
                Tarifa.create(
                    id_articulo=articulo_id,
                    id_tarifa_tipo=tipo.id,
                    precio=0.0,
                    porc_dto=0.0,
                    precio_final=0.0,
                )

            return True

        except Exception as e:
            logger.exception("Error creating tarifas for articulo %s: %s", articulo_id, e)
            return False

    # ==================== Promociones ====================

    def get_promociones(self, articulo_id: int) -> List[Dict]:
        """Obtener todas las promociones de un artículo."""
        try:
            promociones = Promocion.select().where(Promocion.id_articulo == articulo_id)
            return [self._promocion_to_dict(p) for p in promociones]

        except Exception as e:
            logger.exception("Error getting promociones for articulo %s: %s", articulo_id, e)
            return []

    def get_promocion_by_id(self, promocion_id: int) -> Optional[Dict]:
        """Obtener una promoción por su ID."""
        try:
            promocion = Promocion.get_by_id(promocion_id)
            return self._promocion_to_dict(promocion)
        except DoesNotExist:
            return None
        except Exception as e:
            logger.exception("Error getting promocion by id %s: %s", promocion_id, e)
            return None

    def create_promocion(self, data: Dict) -> Optional[int]:
        """Crear una nueva promoción."""
        try:
            promocion = Promocion.create(**data)
            return promocion.id
        except Exception as e:
            logger.exception("Error creating promocion: %s", e)
            return None

    def update_promocion(self, promocion_id: int, data: Dict) -> bool:
        """Actualizar una promoción."""
        try:
            query = Promocion.update(**data).where(Promocion.id == promocion_id)
            rows = query.execute()
            return rows > 0
        except Exception as e:
            logger.exception("Error updating promocion %s: %s", promocion_id, e)
            return False

    def delete_promocion(self, promocion_id: int) -> bool:
        """Eliminar una promoción."""
        try:
            promocion = Promocion.get_by_id(promocion_id)
            promocion.delete_instance()
            return True
        except DoesNotExist:
            return False
        except Exception as e:
            logger.exception("Error deleting promocion %s: %s", promocion_id, e)
            return False

    # ==================== Helpers ====================

    def _model_to_dict(self, model) -> Dict:
        """Convertir un modelo Peewee a diccionario."""
        if model is None:
            return {}

        data = {}
        for field in model._meta.fields.values():
            value = getattr(model, field.name)

            # Convertir ForeignKey a ID
            if hasattr(value, 'id'):
                data[field.name] = value.id
            else:
                data[field.name] = value

        return data

    def _promocion_to_dict(self, promocion: Promocion) -> Dict:
        """Convertir una promoción a diccionario."""
        return {
            "id": promocion.id,
            "id_articulo": promocion.id_articulo.id if hasattr(promocion.id_articulo, 'id') else promocion.id_articulo,
            "descripcion": promocion.descripcion,
            "fecha_inicio": promocion.fecha_inicio,
            "fecha_fin": promocion.fecha_fin,
            "tipo_promocion": promocion.tipo_promocion,
            "por_cada": promocion.por_cada,
            "regalo": promocion.regalo,
            "dto_local": promocion.dto_local,
            "dto_web": promocion.dto_web,
            "precio_final": promocion.precio_final,
            "activa": promocion.activa,
        }

    # ==================== Lookups ====================

    def get_secciones(self) -> List[Dict]:
        """Obtener todas las secciones."""
        try:
            secciones = Seccion.select().order_by(Seccion.seccion)
            return [self._model_to_dict(s) for s in secciones]
        except Exception as e:
            logger.exception("Error getting secciones: %s", e)
            return []

    def get_familias(self, id_seccion: int = None) -> List[Dict]:
        """Obtener familias, opcionalmente filtradas por sección."""
        try:
            query = Familia.select()
            if id_seccion:
                query = query.where(Familia.id_seccion == id_seccion)

            query = query.order_by(Familia.familia)
            return [self._model_to_dict(f) for f in query]
        except Exception as e:
            logger.exception("Error getting familias: %s", e)
            return []

    def get_subfamilias(self, id_familia: int = None) -> List[Dict]:
        """Obtener subfamilias, opcionalmente filtradas por familia."""
        try:
            query = Subfamilia.select()
            if id_familia:
                query = query.where(Subfamilia.id_familia == id_familia)

            query = query.order_by(Subfamilia.subfamilia)
            return [self._model_to_dict(s) for s in query]
        except Exception as e:
            logger.exception("Error getting subfamilias: %s", e)
            return []

    def get_tipos(self) -> List[Dict]:
        """Obtener todos los tipos de artículo."""
        try:
            tipos = ArticuloTipo.select().order_by(ArticuloTipo.descripcion)
            return [self._model_to_dict(t) for t in tipos]
        except Exception as e:
            logger.exception("Error getting tipos: %s", e)
            return []

