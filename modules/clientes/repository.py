"""
Repository Peewee para el módulo de Clientes.
Maneja todas las operaciones CRUD siguiendo el patrón MVC.
"""

import logging
from typing import Dict, List, Optional

from peewee import DoesNotExist, fn

from core.peewee_db import ensure_initialized

from .models import Cliente

logger = logging.getLogger(__name__)


class ClienteRepository:
    """Repositorio para operaciones con clientes usando Peewee."""

    def __init__(self):
        """Inicializar repositorio."""
        # Asegurar que la BD esté inicializada
        ensure_initialized()

    # ========== Conversión ==========

    def _model_to_dict(self, cliente: Cliente) -> Dict:
        """Convierte un modelo Peewee a diccionario."""
        try:
            return {
                'id': cliente.id,
                'id_web': cliente.id_web,
                'codigo_cliente': cliente.codigo_cliente,
                'apellido1': cliente.apellido1,
                'apellido2': cliente.apellido2,
                'nombre': cliente.nombre,
                'nombre_fiscal': cliente.nombre_fiscal,
                'nombre_comercial': cliente.nombre_comercial,
                'persona_contacto': cliente.persona_contacto,
                'cif_nif_siren': cliente.cif_nif_siren,
                'siret': cliente.siret,
                'cif_vies': cliente.cif_vies,
                'direccion1': cliente.direccion1,
                'direccion2': cliente.direccion2,
                'cp': cliente.cp,
                'poblacion': cliente.poblacion,
                'provincia': cliente.provincia,
                'pais': cliente.pais,
                'telefono1': cliente.telefono1,
                'telefono2': cliente.telefono2,
                'fax': cliente.fax,
                'movil': cliente.movil,
                'email': cliente.email,
                'web': cliente.web,
                'fecha_alta': cliente.fecha_alta,
                'fecha_ultima_compra': cliente.fecha_ultima_compra,
                'fecha_nacimiento': cliente.fecha_nacimiento,
                'acumulado_ventas': float(cliente.acumulado_ventas) if cliente.acumulado_ventas else 0.0,
                'ventas_ejercicio': float(cliente.ventas_ejercicio) if cliente.ventas_ejercicio else 0.0,
                'riesgo_maximo': float(cliente.riesgo_maximo) if cliente.riesgo_maximo else 0.0,
                'deuda_actual': float(cliente.deuda_actual) if cliente.deuda_actual else 0.0,
                'importe_pendiente': float(cliente.importe_pendiente) if cliente.importe_pendiente else 0.0,
                'comentarios': cliente.comentarios,
                'bloqueado': bool(cliente.bloqueado),
                'comentario_bloqueo': cliente.comentario_bloqueo,
                'observaciones': cliente.observaciones,
                'porc_dto_cliente': float(cliente.porc_dto_cliente) if cliente.porc_dto_cliente else 0.0,
                'recargo_equivalencia': bool(cliente.recargo_equivalencia),
                'irpf': bool(cliente.irpf),
                'grupo_iva': cliente.grupo_iva,
                'cuenta_contable': cliente.cuenta_contable,
                'cuenta_iva_repercutido': cliente.cuenta_iva_repercutido,
                'cuenta_deudas': cliente.cuenta_deudas,
                'cuenta_cobros': cliente.cuenta_cobros,
                'id_forma_pago': cliente.id_forma_pago,
                'dia_pago1': cliente.dia_pago1,
                'dia_pago2': cliente.dia_pago2,
                'entidad_bancaria': cliente.entidad_bancaria,
                'oficina_bancaria': cliente.oficina_bancaria,
                'dc': cliente.dc,
                'cuenta_corriente': cliente.cuenta_corriente,
                'importe_a_cuenta': float(cliente.importe_a_cuenta) if cliente.importe_a_cuenta else 0.0,
                'vales': float(cliente.vales) if cliente.vales else 0.0,
                'visa_distancia1': cliente.visa_distancia1,
                'visa_distancia2': cliente.visa_distancia2,
                'visa1_caduca_mes': cliente.visa1_caduca_mes,
                'visa2_caduca_mes': cliente.visa2_caduca_mes,
                'visa1_caduca_ano': cliente.visa1_caduca_ano,
                'visa2_caduca_ano': cliente.visa2_caduca_ano,
                'visa1_cod_valid': cliente.visa1_cod_valid,
                'visa2_cod_valid': cliente.visa2_cod_valid,
                'acceso_web': cliente.acceso_web,
                'password_web': cliente.password_web,
                'id_tarifa': cliente.id_tarifa,
                'id_divisa': cliente.id_divisa,
                'id_idioma_documentos': cliente.id_idioma_documentos,
                'id_agente': cliente.id_agente,
                'id_transportista': cliente.id_transportista,
            }
        except Exception as e:
            logger.exception("Error converting cliente to dict: %s", e)
            return {}

    # ========== CRUD Básico ==========

    def get_by_id(self, id_cliente: int) -> Optional[Dict]:
        """Obtiene un cliente por su ID."""
        try:
            cliente = Cliente.get_by_id(id_cliente)
            return self._model_to_dict(cliente)
        except DoesNotExist:
            return None
        except Exception as e:
            logger.exception("Error getting cliente by id %s: %s", id_cliente, e)
            return None

    def get_by_codigo(self, codigo: str) -> Optional[Dict]:
        """Obtiene un cliente por su código."""
        try:
            cliente = Cliente.get(Cliente.codigo_cliente == codigo)
            return self._model_to_dict(cliente)
        except DoesNotExist:
            return None
        except Exception as e:
            logger.exception("Error getting cliente by codigo %s: %s", codigo, e)
            return None

    def get_all(self, filtro: str = "", limit: int = None, offset: int = 0) -> List[Dict]:
        """Obtiene todos los clientes, opcionalmente filtrados."""
        try:
            query = Cliente.select().order_by(Cliente.nombre_fiscal)

            if filtro:
                filtro_like = f"%{filtro}%"
                query = query.where(
                    (Cliente.codigo_cliente.contains(filtro)) |
                    (Cliente.nombre_fiscal.contains(filtro)) |
                    (Cliente.nombre_comercial.contains(filtro)) |
                    (Cliente.cif_nif_siren.contains(filtro)) |
                    (Cliente.email.contains(filtro))
                )

            if limit:
                query = query.limit(limit).offset(offset)

            return [self._model_to_dict(c) for c in query]
        except Exception as e:
            logger.exception("Error getting all clientes: %s", e)
            return []

    def create(self, data: Dict) -> Optional[Dict]:
        """Crea un nuevo cliente."""
        try:
            # Generar código automático si no existe
            if not data.get('codigo_cliente'):
                data['codigo_cliente'] = self._generar_codigo()

            # Inicializar cuentas contables si no existen
            if not data.get('cuenta_contable'):
                data['cuenta_contable'] = f"430{data['codigo_cliente']}"

            # Convertir Decimales desde strings
            decimal_fields = ['acumulado_ventas', 'ventas_ejercicio', 'riesgo_maximo',
                             'deuda_actual', 'importe_pendiente', 'porc_dto_cliente',
                             'importe_a_cuenta', 'vales']
            for field in decimal_fields:
                if field in data and isinstance(data[field], str):
                    try:
                        data[field] = float(data[field])
                    except:
                        data[field] = 0.0

            cliente = Cliente.create(**data)
            return self._model_to_dict(cliente)
        except Exception as e:
            logger.exception("Error creating cliente: %s", e)
            return None

    def update(self, id_cliente: int, data: Dict) -> Optional[Dict]:
        """Actualiza un cliente existente."""
        try:
            cliente = Cliente.get_by_id(id_cliente)

            # Actualizar campos
            for key, value in data.items():
                if hasattr(cliente, key):
                    setattr(cliente, key, value)

            cliente.save()
            return self._model_to_dict(cliente)
        except DoesNotExist:
            logger.error("Cliente %s not found", id_cliente)
            return None
        except Exception as e:
            logger.exception("Error updating cliente %s: %s", id_cliente, e)
            return None

    def delete(self, id_cliente: int) -> bool:
        """Elimina un cliente."""
        try:
            cliente = Cliente.get_by_id(id_cliente)
            cliente.delete_instance()
            return True
        except DoesNotExist:
            logger.error("Cliente %s not found", id_cliente)
            return False
        except Exception as e:
            logger.exception("Error deleting cliente %s: %s", id_cliente, e)
            return False

    # ========== Navegación ==========

    def get_next(self, current_id: int) -> Optional[Dict]:
        """Obtiene el siguiente cliente por ID."""
        try:
            query = Cliente.select().where(Cliente.id > current_id).order_by(Cliente.id).limit(1)
            cliente = query.first()
            return self._model_to_dict(cliente) if cliente else None
        except Exception as e:
            logger.exception("Error getting next cliente: %s", e)
            return None

    def get_prev(self, current_id: int) -> Optional[Dict]:
        """Obtiene el cliente anterior por ID."""
        try:
            query = Cliente.select().where(Cliente.id < current_id).order_by(Cliente.id.desc()).limit(1)
            cliente = query.first()
            return self._model_to_dict(cliente) if cliente else None
        except Exception as e:
            logger.exception("Error getting prev cliente: %s", e)
            return None

    # ========== Utilidades ==========

    def _generar_codigo(self) -> str:
        """Genera un código automático para un nuevo cliente."""
        try:
            # Obtener el máximo código numérico actual
            max_cliente = Cliente.select(fn.MAX(Cliente.id)).scalar()
            if max_cliente:
                return str(max_cliente + 1).zfill(6)
            return "000001"
        except Exception as e:
            logger.exception("Error generating codigo: %s", e)
            return "000001"

    def count(self, filtro: str = "") -> int:
        """Cuenta el número total de clientes."""
        try:
            query = Cliente.select()
            if filtro:
                query = query.where(
                    (Cliente.codigo_cliente.contains(filtro)) |
                    (Cliente.nombre_fiscal.contains(filtro)) |
                    (Cliente.nombre_comercial.contains(filtro)) |
                    (Cliente.cif_nif_siren.contains(filtro)) |
                    (Cliente.email.contains(filtro))
                )
            return query.count()
        except Exception as e:
            logger.exception("Error counting clientes: %s", e)
            return 0

