"""
Repository para Clientes usando SQL directo (sin ORM).
Optimizado para aplicación multi-empresa con MultiDBManager.
"""

import logging
from typing import Dict, List, Optional
from datetime import date, datetime
from decimal import Decimal

from core.base_repository import BaseRepository
from core.db_manager import get_db_manager

logger = logging.getLogger(__name__)


class ClienteRepository(BaseRepository):
    """
    Repositorio para operaciones con clientes usando SQL directo.

    Ventajas sobre Peewee/SQLAlchemy:
    - Cambio fluido entre bases de datos de empresa
    - Consultas cross-database (ATTACH en SQLite)
    - SQL visible y optimizable
    - Sin problemas de sesiones/contextos
    """

    # Campos de la tabla clientes
    CAMPOS_CLIENTE = [
        'id', 'id_web', 'codigo_cliente', 'apellido1', 'apellido2', 'nombre',
        'nombre_fiscal', 'nombre_comercial', 'persona_contacto', 'cif_nif_siren',
        'siret', 'cif_vies', 'direccion1', 'direccion2', 'cp', 'poblacion',
        'provincia', 'pais', 'telefono1', 'telefono2', 'fax', 'movil',
        'email', 'web', 'fecha_alta', 'fecha_ultima_compra', 'fecha_nacimiento',
        'acumulado_ventas', 'ventas_ejercicio', 'riesgo_maximo', 'deuda_actual',
        'importe_pendiente', 'comentarios', 'bloqueado', 'comentario_bloqueo',
        'observaciones', 'porc_dto_cliente', 'recargo_equivalencia', 'irpf',
        'grupo_iva', 'cuenta_contable', 'cuenta_iva_repercutido', 'cuenta_deudas',
        'cuenta_cobros', 'id_forma_pago', 'dia_pago1', 'dia_pago2',
        'entidad_bancaria', 'oficina_bancaria', 'dc', 'cuenta_corriente',
        'importe_a_cuenta', 'vales', 'visa_distancia1', 'visa_distancia2',
        'visa1_caduca_mes', 'visa2_caduca_mes', 'visa1_caduca_ano',
        'visa2_caduca_ano', 'visa1_cod_valid', 'visa2_cod_valid',
        'acceso_web', 'password_web', 'id_tarifa', 'id_divisa',
        'id_idioma_documentos', 'id_agente', 'id_transportista'
    ]

    def __init__(self):
        """Inicializa el repositorio con el DB manager global."""
        super().__init__()

    # ========== Consultas básicas ==========

    def obtener_todos(self, filtro: str = "", limit: int = None, offset: int = 0) -> List[dict]:
        """
        Obtiene todos los clientes, opcionalmente filtrados.

        Args:
            filtro: Texto a buscar en código, nombre, CIF, email
            limit: Límite de registros (None = todos)
            offset: Offset para paginación

        Returns:
            Lista de clientes como diccionarios
        """
        try:
            sql = "SELECT * FROM clientes WHERE 1=1"
            params = []

            if filtro:
                sql += """ AND (
                    codigo_cliente LIKE %s OR
                    nombre_fiscal LIKE %s OR
                    nombre_comercial LIKE %s OR
                    cif_nif_siren LIKE %s OR
                    email LIKE %s
                )"""
                filtro_like = f"%{filtro}%"
                params.extend([filtro_like] * 5)

            sql += " ORDER BY nombre_fiscal"

            if limit:
                sql += f" LIMIT {limit} OFFSET {offset}"

            return self._fetch_all(sql, tuple(params) if params else None)

        except Exception as e:
            logger.error(f"Error obteniendo todos los clientes: {e}")
            return []

    def obtener_por_id(self, id_cliente: int) -> Optional[dict]:
        """
        Obtiene un cliente por su ID.

        Args:
            id_cliente: ID del cliente

        Returns:
            Cliente como diccionario o None
        """
        try:
            sql = "SELECT * FROM clientes WHERE id = %s"
            return self._fetch_one(sql, (id_cliente,))
        except Exception as e:
            logger.error(f"Error obteniendo cliente por ID {id_cliente}: {e}")
            return None

    def obtener_por_codigo(self, codigo: str) -> Optional[dict]:
        """
        Obtiene un cliente por su código.

        Args:
            codigo: Código del cliente

        Returns:
            Cliente como diccionario o None
        """
        try:
            sql = "SELECT * FROM clientes WHERE codigo_cliente = %s"
            return self._fetch_one(sql, (codigo,))
        except Exception as e:
            logger.error(f"Error obteniendo cliente por código {codigo}: {e}")
            return None

    def obtener_por_cif(self, cif: str) -> Optional[dict]:
        """
        Obtiene un cliente por su CIF/NIF/SIREN.

        Args:
            cif: CIF/NIF/SIREN del cliente

        Returns:
            Cliente como diccionario o None
        """
        try:
            sql = "SELECT * FROM clientes WHERE cif_nif_siren = %s"
            return self._fetch_one(sql, (cif,))
        except Exception as e:
            logger.error(f"Error obteniendo cliente por CIF {cif}: {e}")
            return None

    # ========== Crear y actualizar ==========

    def crear(self, data: dict) -> Optional[dict]:
        """
        Crea un nuevo cliente.

        Args:
            data: Diccionario con datos del cliente

        Returns:
            Cliente creado como diccionario o None si falla
        """
        try:
            # Generar código automático si no existe
            if not data.get('codigo_cliente'):
                data['codigo_cliente'] = self._generar_codigo()

            # Asegurar código único
            max_attempts = 5
            attempts = 0
            while attempts < max_attempts:
                existing = self.obtener_por_codigo(data['codigo_cliente'])
                if existing is None:
                    break
                data['codigo_cliente'] = self._generar_codigo()
                attempts += 1

            # Inicializar cuenta contable si no existe
            if not data.get('cuenta_contable'):
                data['cuenta_contable'] = f"430{data['codigo_cliente']}"

            # Convertir tipos
            data = self._preparar_datos_para_insertar(data)

            # Insertar
            cliente_id = self._insert('clientes', data)

            # Retornar el cliente creado
            return self.obtener_por_id(cliente_id)

        except Exception as e:
            logger.error(f"Error creando cliente: {e}")
            return None

    def actualizar(self, id_cliente: int, data: dict) -> Optional[dict]:
        """
        Actualiza un cliente existente.

        Args:
            id_cliente: ID del cliente
            data: Diccionario con campos a actualizar

        Returns:
            Cliente actualizado como diccionario o None
        """
        try:
            # Preparar datos
            data = self._preparar_datos_para_insertar(data)

            # Actualizar
            rows_affected = self._update('clientes', data, 'id = %s', (id_cliente,))

            if rows_affected > 0:
                return self.obtener_por_id(id_cliente)
            else:
                logger.warning(f"No se actualizó ningún registro para cliente ID {id_cliente}")
                return None

        except Exception as e:
            logger.error(f"Error actualizando cliente {id_cliente}: {e}")
            return None

    def eliminar(self, id_cliente: int) -> bool:
        """
        Elimina un cliente.

        Args:
            id_cliente: ID del cliente

        Returns:
            True si se eliminó, False si no
        """
        try:
            rows_affected = self._delete('clientes', 'id = %s', (id_cliente,))
            return rows_affected > 0
        except Exception as e:
            logger.error(f"Error eliminando cliente {id_cliente}: {e}")
            return False

    def obtener_siguiente(self, id_cliente: int) -> Optional[dict]:
        """Obtiene el siguiente cliente después del ID actual."""
        try:
            sql = """
                SELECT * FROM clientes
                WHERE id > %s
                ORDER BY id ASC
                LIMIT 1
            """
            return self._fetch_one(sql, (id_cliente,))
        except Exception as e:
            logger.error(f"Error obteniendo siguiente cliente: {e}")
            return None

    def obtener_anterior(self, id_cliente: int) -> Optional[dict]:
        """Obtiene el cliente anterior al ID actual."""
        try:
            sql = """
                SELECT * FROM clientes
                WHERE id < %s
                ORDER BY id DESC
                LIMIT 1
            """
            return self._fetch_one(sql, (id_cliente,))
        except Exception as e:
            logger.error(f"Error obteniendo anterior cliente: {e}")
            return None

    def contar_todos(self, filtro: str = "") -> int:
        """Cuenta el total de clientes opcionalmente filtrados."""
        try:
            sql = "SELECT COUNT(*) as total FROM clientes WHERE 1=1"
            params = []

            if filtro:
                sql += """ AND (
                    codigo_cliente LIKE %s OR
                    nombre_fiscal LIKE %s OR
                    nombre_comercial LIKE %s OR
                    cif_nif_siren LIKE %s OR
                    email LIKE %s
                )"""
                filtro_like = f"%{filtro}%"
                params.extend([filtro_like] * 5)

            result = self._fetch_one(sql, tuple(params) if params else None)
            return result['total'] if result else 0
        except Exception as e:
            logger.error(f"Error contando clientes: {e}")
            return 0

    # ========== Direcciones alternativas ==========

    def obtener_direcciones(self, id_cliente: int) -> List[dict]:
        """
        Obtiene direcciones alternativas de un cliente.

        Args:
            id_cliente: ID del cliente

        Returns:
            Lista de direcciones como diccionarios
        """
        try:
            sql = """
                SELECT * FROM direcciones_alternativas
                WHERE id_cliente = %s
                ORDER BY id
            """
            return self._fetch_all(sql, (id_cliente,))
        except Exception as e:
            logger.error(f"Error obteniendo direcciones para cliente {id_cliente}: {e}")
            return []

    def obtener_direccion_por_id(self, id_direccion: int) -> Optional[dict]:
        """Obtiene una dirección alternativa por su ID."""
        try:
            sql = "SELECT * FROM direcciones_alternativas WHERE id = %s"
            return self._fetch_one(sql, (id_direccion,))
        except Exception as e:
            logger.error(f"Error obteniendo dirección {id_direccion}: {e}")
            return None

    def crear_direccion(self, data: dict) -> Optional[dict]:
        """Crea una dirección alternativa."""
        try:
            # Añadir timestamps
            now = datetime.now()
            data['fecha_creacion'] = now
            data['fecha_modificacion'] = now

            direccion_id = self._insert('direcciones_alternativas', data)
            return self.obtener_direccion_por_id(direccion_id)
        except Exception as e:
            logger.error(f"Error creando dirección: {e}")
            return None

    def actualizar_direccion(self, id_direccion: int, data: dict) -> Optional[dict]:
        """Actualiza una dirección alternativa."""
        try:
            data['fecha_modificacion'] = datetime.now()
            rows_affected = self._update('direcciones_alternativas', data, 'id = %s', (id_direccion,))

            if rows_affected > 0:
                return self.obtener_direccion_por_id(id_direccion)
            return None
        except Exception as e:
            logger.error(f"Error actualizando dirección {id_direccion}: {e}")
            return None

    def eliminar_direccion(self, id_direccion: int) -> bool:
        """Elimina una dirección alternativa."""
        try:
            rows_affected = self._delete('direcciones_alternativas', 'id = %s', (id_direccion,))
            return rows_affected > 0
        except Exception as e:
            logger.error(f"Error eliminando dirección {id_direccion}: {e}")
            return False

    # ========== Deudas y estadísticas ==========

    def obtener_deudas(self, id_cliente: int, solo_pendientes: bool = False) -> List[dict]:
        """Obtiene deudas de un cliente."""
        try:
            sql = "SELECT * FROM deudas WHERE id_cliente = %s"
            params = [id_cliente]

            if solo_pendientes:
                sql += " AND pagado = 0"

            sql += " ORDER BY fecha_vencimiento"

            return self._fetch_all(sql, tuple(params))
        except Exception as e:
            logger.error(f"Error obteniendo deudas para cliente {id_cliente}: {e}")
            return []

    def obtener_estadisticas_mes(self, id_cliente: int, anio: int) -> dict:
        """
        Obtiene estadísticas de ventas por mes para un cliente.

        Args:
            id_cliente: ID del cliente
            anio: Año para las estadísticas

        Returns:
            Diccionario {mes: importe}
        """
        try:
            sql = """
                SELECT 
                    MONTH(fecha) as mes,
                    SUM(total) as importe
                FROM facturas
                WHERE id_cliente = %s AND YEAR(fecha) = %s
                GROUP BY MONTH(fecha)
            """

            resultados = self._fetch_all(sql, (id_cliente, anio))

            # Convertir a diccionario {mes: importe}
            return {int(r['mes']): float(r['importe'] or 0) for r in resultados}

        except Exception as e:
            logger.error(f"Error obteniendo estadísticas para cliente {id_cliente}: {e}")
            return {}

    # ========== Tipos de cliente ==========

    def obtener_tipos_cliente(self, id_cliente: int) -> List[dict]:
        """Obtiene los tipos asociados a un cliente."""
        try:
            sql = """
                SELECT tc.*, t.nombre as tipo_nombre, st.nombre as subtipo_nombre
                FROM tipos_cliente tc
                LEFT JOIN tipos t ON tc.id_tipo = t.id
                LEFT JOIN subtipos st ON tc.id_subtipo = st.id
                WHERE tc.id_cliente = %s
                ORDER BY tc.id
            """
            return self._fetch_all(sql, (id_cliente,))
        except Exception as e:
            logger.error(f"Error obteniendo tipos para cliente {id_cliente}: {e}")
            return []

    def agregar_tipo_cliente(self, id_cliente: int, id_tipo: int, id_subtipo: Optional[int] = None) -> bool:
        """Agrega un tipo a un cliente."""
        try:
            data = {
                'id_cliente': id_cliente,
                'id_tipo': id_tipo,
                'id_subtipo': id_subtipo
            }
            self._insert('tipos_cliente', data)
            return True
        except Exception as e:
            logger.error(f"Error agregando tipo a cliente {id_cliente}: {e}")
            return False

    # ========== Helpers privados ==========

    def _generar_codigo(self) -> str:
        """Genera un código único para un cliente."""
        try:
            # Obtener el último código
            sql = """
                SELECT codigo_cliente 
                FROM clientes 
                WHERE codigo_cliente LIKE 'CLI-%'
                ORDER BY CAST(SUBSTRING(codigo_cliente, 5) AS UNSIGNED) DESC
                LIMIT 1
            """
            resultado = self._fetch_one(sql)

            if resultado and resultado.get('codigo_cliente'):
                ultimo_codigo = resultado['codigo_cliente']
                # Extraer número (ej: "CLI-123" -> 123)
                try:
                    numero = int(ultimo_codigo.split('-')[1])
                    siguiente = numero + 1
                except:
                    siguiente = 1
            else:
                siguiente = 1

            return f"CLI-{siguiente}"

        except Exception as e:
            logger.error(f"Error generando código: {e}")
            # Fallback: usar timestamp
            return f"CLI-{int(datetime.now().timestamp())}"

    def _preparar_datos_para_insertar(self, data: dict) -> dict:
        """
        Prepara datos para inserción/actualización.
        Convierte tipos y filtra campos inválidos.
        """
        resultado = {}

        for key, value in data.items():
            # Saltar campos que no existen en la tabla
            if key not in self.CAMPOS_CLIENTE or key == 'id':
                continue

            # Convertir None, strings vacíos
            if value == '' or value is None:
                resultado[key] = None
                continue

            # Convertir booleanos
            if key in ['bloqueado', 'recargo_equivalencia', 'irpf']:
                resultado[key] = 1 if value else 0
                continue

            # Convertir decimales
            if key in ['acumulado_ventas', 'ventas_ejercicio', 'riesgo_maximo',
                      'deuda_actual', 'importe_pendiente', 'porc_dto_cliente',
                      'importe_a_cuenta', 'vales']:
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
            if key in ['fecha_alta', 'fecha_ultima_compra', 'fecha_nacimiento']:
                if isinstance(value, (date, datetime)):
                    resultado[key] = value
                elif isinstance(value, str):
                    # Intentar parsear
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

