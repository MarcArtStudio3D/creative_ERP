"""
Repository para Artículos usando SQL directo (sin ORM).
Optimizado para aplicación multi-empresa con MultiDBManager.
"""

import logging
from datetime import date, datetime
from typing import Dict, List, Optional
from decimal import Decimal

from core.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class ArticuloRepository(BaseRepository):
    """
    Repositorio para operaciones con artículos usando SQL directo.

    Gestiona artículos, tarifas, promociones, secciones, familias y subfamilias.
    """

    # Campos principales de la tabla articulos
    CAMPOS_ARTICULO = [
        'id', 'codigo', 'codigo_barras', 'codigo_tipo', 'descripcion_reducida',
        'descripcion_ampliada', 'descripcion_proveedor', 'activo', 'id_seccion',
        'id_familia', 'id_subfamilia', 'id_proveedor', 'fecha_alta',
        'coste', 'precio_venta', 'precio_compra',
        'iva', 'req_eq', 'stock_real', 'stock_minimo', 'stock_maximo',
        'peso', 'volumen', 'ubicacion', 'imagen', 'observaciones',
        'visible_web', 'destacado_web', 'oferta_web', 'novedad_web',
        'meta_title', 'meta_description', 'meta_keywords'
    ]

    def __init__(self):
        """Inicializa el repositorio con el DB manager global."""
        super().__init__()

    # ==================== CRUD Básico ====================

    def obtener_todos(
        self,
        limit: int = None,
        offset: int = 0,
        order_by: str = "descripcion_reducida",
        order_dir: str = "ASC",
        filtro: str = ""
    ) -> List[dict]:
        """
        Obtiene todos los artículos con paginación y filtros.

        Args:
            limit: Límite de registros
            offset: Offset para paginación
            order_by: Campo para ordenar
            order_dir: Dirección (ASC/DESC)
            filtro: Texto a buscar en código, descripción o código de barras

        Returns:
            Lista de artículos como diccionarios
        """
        try:
            sql = "SELECT * FROM articulos WHERE 1=1"
            params = []

            if filtro:
                sql += """ AND (
                    codigo LIKE %s OR
                    descripcion_reducida LIKE %s OR
                    codigo_barras LIKE %s
                )"""
                filtro_like = f"%{filtro}%"
                params.extend([filtro_like] * 3)

            # Ordenar
            sql += f" ORDER BY `{order_by}` {order_dir}"

            # Paginar
            if limit:
                sql += f" LIMIT {limit} OFFSET {offset}"

            return self._fetch_all(sql, tuple(params) if params else None)

        except Exception as e:
            logger.error(f"Error obteniendo artículos: {e}")
            return []

    def contar_todos(self, filtro: str = "") -> int:
        """Cuenta el total de artículos."""
        try:
            sql = "SELECT COUNT(*) as total FROM articulos WHERE 1=1"
            params = []

            if filtro:
                sql += """ AND (
                    codigo LIKE %s OR
                    descripcion_reducida LIKE %s OR
                    codigo_barras LIKE %s
                )"""
                filtro_like = f"%{filtro}%"
                params.extend([filtro_like] * 3)

            result = self._fetch_one(sql, tuple(params) if params else None)
            return result['total'] if result else 0

        except Exception as e:
            logger.error(f"Error contando artículos: {e}")
            return 0

    def obtener_por_id(self, articulo_id: int) -> Optional[dict]:
        """Obtiene un artículo por su ID."""
        try:
            sql = "SELECT * FROM articulos WHERE id = %s"
            return self._fetch_one(sql, (articulo_id,))
        except Exception as e:
            logger.error(f"Error obteniendo artículo por ID {articulo_id}: {e}")
            return None

    def obtener_por_codigo(self, codigo: str) -> Optional[dict]:
        """Obtiene un artículo por su código."""
        try:
            sql = "SELECT * FROM articulos WHERE codigo = %s"
            return self._fetch_one(sql, (codigo,))
        except Exception as e:
            logger.error(f"Error obteniendo artículo por código {codigo}: {e}")
            return None

    def obtener_siguiente(self, current_id: int) -> Optional[dict]:
        """Obtiene el siguiente artículo después del ID actual."""
        try:
            sql = """
                SELECT * FROM articulos
                WHERE id > %s
                ORDER BY id ASC
                LIMIT 1
            """
            return self._fetch_one(sql, (current_id,))
        except Exception as e:
            logger.error(f"Error obteniendo siguiente artículo: {e}")
            return None

    def obtener_anterior(self, current_id: int) -> Optional[dict]:
        """Obtiene el artículo anterior al ID actual."""
        try:
            sql = """
                SELECT * FROM articulos
                WHERE id < %s
                ORDER BY id DESC
                LIMIT 1
            """
            return self._fetch_one(sql, (current_id,))
        except Exception as e:
            logger.error(f"Error obteniendo artículo anterior: {e}")
            return None

    def crear(self, data: dict = None) -> Optional[dict]:
        """
        Crea un nuevo artículo.

        Args:
            data: Diccionario con datos del artículo

        Returns:
            Artículo creado como diccionario o None
        """
        try:
            if not data:
                data = {}

            # Generar código temporal si no existe
            if 'codigo' not in data or not data['codigo']:
                data['codigo'] = self._generar_codigo_temporal()

            # Valores por defecto
            if 'descripcion_reducida' not in data:
                data['descripcion_reducida'] = 'Nuevo artículo'
            if 'fecha_alta' not in data:
                data['fecha_alta'] = date.today()
            if 'activo' not in data:
                data['activo'] = 1
            if 'precio_venta' not in data:
                data['precio_venta'] = 0.0
            if 'coste' not in data:
                data['coste'] = 0.0
            if 'stock_real' not in data:
                data['stock_real'] = 0.0

            # Preparar datos
            data = self._preparar_datos_para_insertar(data)

            # Insertar
            articulo_id = self._insert('articulos', data)

            # Crear tarifas por defecto
            self.crear_tarifas_para_articulo(articulo_id)

            return self.obtener_por_id(articulo_id)

        except Exception as e:
            logger.error(f"Error creando artículo: {e}")
            return None

    def actualizar(self, articulo_id: int, data: dict) -> Optional[dict]:
        """
        Actualiza un artículo existente.

        Args:
            articulo_id: ID del artículo
            data: Diccionario con campos a actualizar

        Returns:
            Artículo actualizado como diccionario o None
        """
        try:

            # Preparar datos
            data = self._preparar_datos_para_insertar(data)

            # Actualizar
            rows_affected = self._update('articulos', data, 'id = %s', (articulo_id,))

            if rows_affected > 0:
                return self.obtener_por_id(articulo_id)
            else:
                logger.warning(f"No se actualizó ningún artículo con ID {articulo_id}")
                return None

        except Exception as e:
            logger.error(f"Error actualizando artículo {articulo_id}: {e}")
            return None

    def eliminar(self, articulo_id: int) -> bool:
        """Elimina un artículo."""
        try:
            # Primero eliminar tarifas y promociones asociadas
            self._delete('tarifas', 'id_articulo = %s', (articulo_id,))
            self._delete('articulos_ofertas', 'id_articulo = %s', (articulo_id,))

            # Eliminar artículo
            rows_affected = self._delete('articulos', 'id = %s', (articulo_id,))
            return rows_affected > 0
        except Exception as e:
            logger.error(f"Error eliminando artículo {articulo_id}: {e}")
            return False

    # ==================== Tarifas ====================

    def obtener_tarifas(self, articulo_id: int) -> List[dict]:
        """
        Obtiene todas las tarifas de un artículo.

        Args:
            articulo_id: ID del artículo

        Returns:
            Lista de tarifas con información del tipo de tarifa
        """
        try:
            sql = """
                SELECT 
                    t.id,
                    t.id_articulo,
                    t.id_tarifa_tipo,
                    t.precio,
                    t.porc_dto,
                    t.precio_final,
                    tt.codigo,
                    tt.descripcion
                FROM tarifas t
                LEFT JOIN tarifas_tipos tt ON t.id_tarifa_tipo = tt.id
                WHERE t.id_articulo = %s
                ORDER BY tt.codigo
            """
            return self._fetch_all(sql, (articulo_id,))
        except Exception as e:
            logger.error(f"Error obteniendo tarifas para artículo {articulo_id}: {e}")
            return []

    def actualizar_tarifa(self, tarifa_id: int, data: dict) -> bool:
        """Actualiza una tarifa."""
        try:
            rows_affected = self._update('tarifas', data, 'id = %s', (tarifa_id,))
            return rows_affected > 0
        except Exception as e:
            logger.error(f"Error actualizando tarifa {tarifa_id}: {e}")
            return False

    def crear_tarifas_para_articulo(self, articulo_id: int) -> bool:
        """
        Crea tarifas por defecto para un artículo nuevo.

        Args:
            articulo_id: ID del artículo

        Returns:
            True si se crearon correctamente
        """
        try:
            # Obtener todos los tipos de tarifa activos
            sql = "SELECT id FROM tarifas_tipos WHERE activa = 1"
            tipos = self._fetch_all(sql)

            for tipo in tipos:
                tarifa_data = {
                    'id_articulo': articulo_id,
                    'id_tarifa_tipo': tipo['id'],
                    'precio': 0.0,
                    'porc_dto': 0.0,
                    'precio_final': 0.0
                }
                self._insert('tarifas', tarifa_data)

            return True

        except Exception as e:
            logger.error(f"Error creando tarifas para artículo {articulo_id}: {e}")
            return False

    # ==================== Promociones ====================

    def obtener_promociones(self, articulo_id: int) -> List[dict]:
        """Obtiene todas las promociones de un artículo."""
        try:
            query = """
                SELECT * FROM articulos_ofertas
                WHERE id_articulo = %s
                ORDER BY fecha_inicio DESC
            """
            return self._fetch_all(sql, (articulo_id,))
        except Exception as e:
            logger.error(f"Error obteniendo promociones para artículo {articulo_id}: {e}")
            return []

    def obtener_promocion_por_id(self, promocion_id: int) -> Optional[dict]:
        """Obtiene una promoción por su ID."""
        try:
            sql = "SELECT * FROM articulos_ofertas WHERE id = %s"
            return self._fetch_one(sql, (promocion_id,))
        except Exception as e:
            logger.error(f"Error obteniendo promoción {promocion_id}: {e}")
            return None

    def crear_promocion(self, data: dict) -> Optional[dict]:
        """Crea una nueva promoción."""
        try:
            promocion_id = self._insert('articulos_ofertas', data)
            return self.obtener_promocion_por_id(promocion_id)
        except Exception as e:
            logger.error(f"Error creando promoción: {e}")
            return None

    def actualizar_promocion(self, promocion_id: int, data: dict) -> Optional[dict]:
        """Actualiza una promoción."""
        try:
            rows_affected = self._update('articulos_ofertas', data, 'id = %s', (promocion_id,))

            if rows_affected > 0:
                return self.obtener_promocion_por_id(promocion_id)
            return None
        except Exception as e:
            logger.error(f"Error actualizando promoción {promocion_id}: {e}")
            return None

    def eliminar_promocion(self, promocion_id: int) -> bool:
        """Elimina una promoción."""
        try:
            rows_affected = self._delete('articulos_ofertas', 'id = %s', (promocion_id,))
            return rows_affected > 0
        except Exception as e:
            logger.error(f"Error eliminando promoción {promocion_id}: {e}")
            return False

    # ==================== Secciones, Familias y Subfamilias ====================

    def obtener_secciones(self) -> List[dict]:
        """Obtiene todas las secciones."""
        try:
            sql = "SELECT * FROM secciones ORDER BY codigo"
            return self._fetch_all(sql)
        except Exception as e:
            logger.error(f"Error obteniendo secciones: {e}")
            return []

    def obtener_familias(self, id_seccion: int = None) -> List[dict]:
        """Obtiene familias, opcionalmente filtradas por sección."""
        try:
            if id_seccion:
                sql = "SELECT * FROM familias WHERE id_seccion = %s ORDER BY codigo"
                return self._fetch_all(sql, (id_seccion,))
            else:
                sql = "SELECT * FROM familias ORDER BY codigo"
                return self._fetch_all(sql)
        except Exception as e:
            logger.error(f"Error obteniendo familias: {e}")
            return []

    def obtener_subfamilias(self, id_familia: int = None) -> List[dict]:
        """Obtiene subfamilias, opcionalmente filtradas por familia."""
        try:
            if id_familia:
                sql = "SELECT * FROM subfamilias WHERE id_familia = %s ORDER BY codigo"
                return self._fetch_all(sql, (id_familia,))
            else:
                sql = "SELECT * FROM subfamilias ORDER BY codigo"
                return self._fetch_all(sql)
        except Exception as e:
            logger.error(f"Error obteniendo subfamilias: {e}")
            return []

    def obtener_seccion_por_id(self, id_seccion: int) -> Optional[dict]:
        """Obtiene una sección por su ID."""
        try:
            sql = "SELECT * FROM secciones WHERE id = %s"
            return self._fetch_one(sql, (id_seccion,))
        except Exception as e:
            logger.error(f"Error obteniendo sección {id_seccion}: {e}")
            return None

    def obtener_familia_por_id(self, id_familia: int) -> Optional[dict]:
        """Obtiene una familia por su ID."""
        try:
            sql = "SELECT * FROM familias WHERE id = %s"
            return self._fetch_one(sql, (id_familia,))
        except Exception as e:
            logger.error(f"Error obteniendo familia {id_familia}: {e}")
            return None

    def obtener_subfamilia_por_id(self, id_subfamilia: int) -> Optional[dict]:
        """Obtiene una subfamilia por su ID."""
        try:
            sql = "SELECT * FROM subfamilias WHERE id = %s"
            return self._fetch_one(sql, (id_subfamilia,))
        except Exception as e:
            logger.error(f"Error obteniendo subfamilia {id_subfamilia}: {e}")
            return None

    # ==================== Proveedores ====================

    def obtener_proveedores(self) -> List[dict]:
        """Obtiene todos los proveedores."""
        try:
            sql = "SELECT id, codigo_proveedor, nombre_fiscal FROM proveedores ORDER BY nombre_fiscal"
            return self._fetch_all(sql)
        except Exception as e:
            logger.error(f"Error obteniendo proveedores: {e}")
            return []

    # ==================== Helpers privados ====================

    def _generar_codigo_temporal(self) -> str:
        """Genera un código temporal único para un artículo."""
        try:
            # Obtener el máximo ID
            sql = "SELECT MAX(id) as max_id FROM articulos"
            result = self._fetch_one(sql)
            max_id = result['max_id'] if result and result['max_id'] else 0

            return f"TEMP{max_id + 1:06d}"

        except Exception as e:
            logger.error(f"Error generando código temporal: {e}")
            return f"TEMP{int(datetime.now().timestamp())}"

    def _preparar_datos_para_insertar(self, data: dict) -> dict:
        """
        Prepara datos para inserción/actualización.
        Convierte tipos y filtra campos inválidos.
        """
        resultado = {}

        for key, value in data.items():
            # Saltar campos que no existen en la tabla
            if key not in self.CAMPOS_ARTICULO or key == 'id':
                continue

            # Convertir None, strings vacíos
            if value == '' or value is None:
                resultado[key] = None
                continue

            # Convertir booleanos
            if key in ['activo', 'visible_web', 'destacado_web', 'oferta_web', 'novedad_web']:
                resultado[key] = 1 if value else 0
                continue

            # Convertir decimales
            if key in ['coste', 'precio_venta', 'precio_compra', 'iva', 'req_eq',
                      'stock_real', 'stock_minimo', 'stock_maximo', 'peso', 'volumen']:
                if isinstance(value, (int, float, Decimal)):
                    resultado[key] = float(value)
                elif isinstance(value, str):
                    try:
                        resultado[key] = float(value)
                    except:
                        resultado[key] = 0.0
                else:
                    resultado[key] = 0.0
                continue

            # Convertir fechas
            if key == 'fecha_alta':
                if isinstance(value, (date, datetime)):
                    resultado[key] = value
                elif isinstance(value, str):
                    try:
                        resultado[key] = datetime.strptime(value, '%Y-%m-%d').date()
                    except:
                        resultado[key] = None
                else:
                    resultado[key] = None
                continue

            # El resto se pasa tal cual
            resultado[key] = value

        return resultado

