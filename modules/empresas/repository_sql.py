"""
Repository SQL directo para el módulo de Empresas.
Migrado de Peewee a SQL directo con MultiDBManager.
Retorna objetos Dataclass para mantener arquitectura MVC pura.
"""

import logging
from typing import List, Optional
from datetime import datetime

from core.base_repository import BaseRepository
from modules.empresas.models import Empresa

logger = logging.getLogger(__name__)


class EmpresaRepository(BaseRepository):
    """Repository para gestión de empresas usando SQL directo."""

    def __init__(self):
        """Inicializa el repositorio con el DB manager global."""
        super().__init__()

    # ==================== CRUD Básico ====================

    def obtener_todos(self, group_id: Optional[int] = None) -> List[Empresa]:
        """
        Obtiene todas las empresas.

        Args:
            group_id: ID del grupo (opcional, para filtrar)

        Returns:
            Lista de empresas como objetos Empresa
        """
        try:
            if group_id is not None:
                query = "SELECT * FROM empresas WHERE group_id = %s ORDER BY nombre_fiscal"
                rows = self._fetch_all(query, (group_id,), use_main=True)
            else:
                query = "SELECT * FROM empresas ORDER BY nombre_fiscal"
                rows = self._fetch_all(query, use_main=True)
            return [Empresa.from_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error obteniendo empresas: {e}")
            return []

    def obtener_por_id(self, empresa_id: int) -> Optional[Empresa]:
        """
        Obtiene una empresa por ID.

        Args:
            empresa_id: ID de la empresa

        Returns:
            Empresa como objeto Empresa o None
        """
        try:
            query = "SELECT * FROM empresas WHERE id = %s"
            row = self._fetch_one(query, (empresa_id,), use_main=True)
            return Empresa.from_dict(row) if row else None
        except Exception as e:
            logger.error(f"Error obteniendo empresa {empresa_id}: {e}")
            return None

    def crear(self, empresa: Empresa) -> Optional[Empresa]:
        """
        Crea una nueva empresa.

        Args:
            empresa: Objeto Empresa con los datos

        Returns:
            Empresa creada como objeto Empresa o None
        """
        try:
            # Convertir a dict y preparar datos
            data = empresa.to_dict()
            insert_data = self._preparar_datos(data)

            # Insertar
            new_id = self._insert('empresas', insert_data, use_main=True)

            if new_id:
                return self.obtener_por_id(new_id)
            return None
        except Exception as e:
            logger.error(f"Error creando empresa: {e}")
            return None

    def actualizar(self, empresa_id: int, empresa: Empresa) -> Optional[Empresa]:
        """
        Actualiza una empresa existente.

        Args:
            empresa_id: ID de la empresa
            empresa: Objeto Empresa con los datos a actualizar

        Returns:
            Empresa actualizada como objeto Empresa o None
        """
        try:
            # Convertir a dict y preparar datos
            data = empresa.to_dict()
            update_data = self._preparar_datos(data)

            # Actualizar
            rows_affected = self._update('empresas', update_data, 'id = %s', (empresa_id,), use_main=True)

            if rows_affected > 0:
                return self.obtener_por_id(empresa_id)
            else:
                logger.warning(f"No se actualizó ninguna empresa con ID {empresa_id}")
                return None
        except Exception as e:
            logger.error(f"Error actualizando empresa {empresa_id}: {e}")
            return None

    def eliminar(self, empresa_id: int) -> bool:
        """
        Elimina una empresa.

        Args:
            empresa_id: ID de la empresa

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            rows_deleted = self._delete('empresas', 'id = %s', (empresa_id,), use_main=True)
            return rows_deleted > 0
        except Exception as e:
            logger.error(f"Error eliminando empresa {empresa_id}: {e}")
            return False

    # ==================== Grupos Empresariales ====================

    def obtener_grupos(self) -> List[Empresa]:
        """
        Obtiene todos los grupos empresariales.

        Returns:
            Lista de grupos como diccionarios
        """
        try:
            query = "SELECT * FROM business_groups ORDER BY name"
            return self._fetch_all(query, use_main=True)
        except Exception as e:
            logger.error(f"Error obteniendo grupos: {e}")
            return []

    def obtener_grupo_por_id(self, group_id: int) -> Optional[Empresa]:
        """
        Obtiene un grupo por ID.

        Args:
            group_id: ID del grupo

        Returns:
            Grupo como diccionario o None
        """
        try:
            query = "SELECT * FROM business_groups WHERE id = %s"
            return self._fetch_one(query, (group_id,), use_main=True)
        except Exception as e:
            logger.error(f"Error obteniendo grupo {group_id}: {e}")
            return None

    # ==================== Métodos auxiliares ====================

    def _preparar_datos(self, data: dict) -> dict:
        """
        Prepara los datos para insertar/actualizar en la BD.

        Args:
            data: Diccionario con los datos

        Returns:
            Diccionario con datos preparados
        """
        resultado = {}

        for key, value in data.items():
            # Manejar campos de fecha
            if key in ['fecha_alta', 'fecha_modificacion', 'fecha_constitucion']:
                if isinstance(value, datetime):
                    resultado[key] = value
                elif isinstance(value, str):
                    try:
                        resultado[key] = datetime.strptime(value, '%Y-%m-%d').date()
                    except:
                        resultado[key] = None
                else:
                    resultado[key] = None
                continue

            # Manejar campos booleanos
            if key in ['activa', 'exento_iva', 'intracomunitario', 'actualizar_divisas',
                       'aplicar_irpf', 'enlace_web_activo', 'gestion_internacional',
                       'autocodificar_articulos', 'activar_contabilidad']:
                resultado[key] = bool(value) if value is not None else False
                continue

            # Manejar campos numéricos
            if key in ['group_id', 'numero_empleados', 'decimales_totales', 'decimales_precios',
                       'digitos_factura', 'dia_cierre_ejercicio', 'mes_cierre_ejercicio',
                       'tamano_codigo_articulo', 'digitos_cuentas_contables', 'puerto_mariadb',
                       'puerto_postgresql']:
                if value is not None:
                    try:
                        resultado[key] = int(value)
                    except (ValueError, TypeError):
                        resultado[key] = None
                else:
                    resultado[key] = None
                continue

            # Manejar campos float
            if key in ['capital_social', 'porcentaje_retencion', 'limite_credito',
                       'descuento_general', 'facturacion_anual', 'porcentaje_irpf',
                       'margen_general', 'margen_minimo']:
                if value is not None:
                    try:
                        resultado[key] = float(value)
                    except (ValueError, TypeError):
                        resultado[key] = None
                else:
                    resultado[key] = None
                continue

            # Resto de campos (strings, etc.)
            resultado[key] = value if value is not None else None

        return resultado

