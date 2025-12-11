"""
Modelos de datos para el módulo de Clientes.
Dataclasses para mantener arquitectura MVC pura sin ORM.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import date
from decimal import Decimal


@dataclass
class Cliente:
    """Modelo para Cliente"""
    id: Optional[int] = None
    id_web: Optional[int] = None
    codigo_cliente: str = ""
    apellido1: Optional[str] = None
    apellido2: Optional[str] = None
    nombre: Optional[str] = None
    nombre_fiscal: str = ""
    nombre_comercial: Optional[str] = None
    persona_contacto: Optional[str] = None
    cif_nif_siren: Optional[str] = None
    siret: Optional[str] = None
    cif_vies: Optional[str] = None
    direccion1: Optional[str] = None
    direccion2: Optional[str] = None
    cp: Optional[str] = None
    poblacion: Optional[str] = None
    provincia: Optional[str] = None
    pais: str = "España"
    telefono1: Optional[str] = None
    telefono2: Optional[str] = None
    fax: Optional[str] = None
    movil: Optional[str] = None
    email: Optional[str] = None
    web: Optional[str] = None
    fecha_alta: Optional[date] = None
    fecha_ultima_compra: Optional[date] = None
    fecha_nacimiento: Optional[date] = None
    acumulado_ventas: Decimal = Decimal('0.00')
    ventas_ejercicio: Decimal = Decimal('0.00')
    riesgo_maximo: Decimal = Decimal('0.00')
    deuda_actual: Decimal = Decimal('0.00')
    importe_pendiente: Decimal = Decimal('0.00')
    comentarios: Optional[str] = None
    bloqueado: bool = False
    comentario_bloqueo: Optional[str] = None
    observaciones: Optional[str] = None
    porc_dto_cliente: Decimal = Decimal('0.00')
    recargo_equivalencia: bool = False
    irpf: Decimal = Decimal('0.00')
    grupo_iva: int = 1
    cuenta_contable: Optional[str] = None
    cuenta_iva_repercutido: Optional[str] = None
    cuenta_deudas: Optional[str] = None
    cuenta_cobros: Optional[str] = None
    id_forma_pago: int = -1
    dia_pago1: int = 0
    dia_pago2: int = 0
    entidad_bancaria: Optional[str] = None
    oficina_bancaria: Optional[str] = None
    dc: Optional[str] = None
    cuenta_corriente: Optional[str] = None
    importe_a_cuenta: Decimal = Decimal('0.00')
    vales: Decimal = Decimal('0.00')
    visa_distancia1: Optional[str] = None
    visa_distancia2: Optional[str] = None
    visa1_caduca_mes: int = 0
    visa2_caduca_mes: int = 0
    visa1_caduca_ano: int = 0
    visa2_caduca_ano: int = 0
    visa1_cod_valid: int = 0
    visa2_cod_valid: int = 0
    acceso_web: Optional[str] = None
    password_web: Optional[str] = None
    id_tarifa: int = -1
    id_divisa: int = -1
    id_idioma_documentos: int = -1
    id_agente: int = -1
    id_transportista: int = -1

    @classmethod
    def from_dict(cls, data: dict) -> 'Cliente':
        """Crea una instancia desde un diccionario (SQL row)"""
        if not data:
            return None

        # Helper para convertir a Decimal de forma segura
        def to_decimal(value, default='0.00'):
            if value is None:
                return Decimal(default)
            return Decimal(str(value))

        # Helper para convertir a int de forma segura
        def to_int(value, default=0):
            if value is None:
                return default
            try:
                return int(value)
            except (ValueError, TypeError):
                return default

        return cls(
            id=data.get('id'),
            id_web=data.get('id_web'),
            codigo_cliente=data.get('codigo_cliente', ''),
            apellido1=data.get('apellido1'),
            apellido2=data.get('apellido2'),
            nombre=data.get('nombre'),
            nombre_fiscal=data.get('nombre_fiscal', ''),
            nombre_comercial=data.get('nombre_comercial'),
            persona_contacto=data.get('persona_contacto'),
            cif_nif_siren=data.get('cif_nif_siren'),
            siret=data.get('siret'),
            cif_vies=data.get('cif_vies'),
            direccion1=data.get('direccion1'),
            direccion2=data.get('direccion2'),
            cp=data.get('cp'),
            poblacion=data.get('poblacion'),
            provincia=data.get('provincia'),
            pais=data.get('pais', 'España'),
            telefono1=data.get('telefono1'),
            telefono2=data.get('telefono2'),
            fax=data.get('fax'),
            movil=data.get('movil'),
            email=data.get('email'),
            web=data.get('web'),
            fecha_alta=data.get('fecha_alta'),
            fecha_ultima_compra=data.get('fecha_ultima_compra'),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            acumulado_ventas=to_decimal(data.get('acumulado_ventas')),
            ventas_ejercicio=to_decimal(data.get('ventas_ejercicio')),
            riesgo_maximo=to_decimal(data.get('riesgo_maximo')),
            deuda_actual=to_decimal(data.get('deuda_actual')),
            importe_pendiente=to_decimal(data.get('importe_pendiente')),
            comentarios=data.get('comentarios'),
            bloqueado=bool(data.get('bloqueado', False)),
            comentario_bloqueo=data.get('comentario_bloqueo'),
            observaciones=data.get('observaciones'),
            porc_dto_cliente=to_decimal(data.get('porc_dto_cliente')),
            recargo_equivalencia=bool(data.get('recargo_equivalencia', False)),
            irpf=to_decimal(data.get('irpf')),
            grupo_iva=to_int(data.get('grupo_iva'), 1),
            cuenta_contable=data.get('cuenta_contable'),
            cuenta_iva_repercutido=data.get('cuenta_iva_repercutido'),
            cuenta_deudas=data.get('cuenta_deudas'),
            cuenta_cobros=data.get('cuenta_cobros'),
            id_forma_pago=to_int(data.get('id_forma_pago'), -1),
            dia_pago1=to_int(data.get('dia_pago1')),
            dia_pago2=to_int(data.get('dia_pago2')),
            entidad_bancaria=data.get('entidad_bancaria'),
            oficina_bancaria=data.get('oficina_bancaria'),
            dc=data.get('dc'),
            cuenta_corriente=data.get('cuenta_corriente'),
            importe_a_cuenta=to_decimal(data.get('importe_a_cuenta')),
            vales=to_decimal(data.get('vales')),
            visa_distancia1=data.get('visa_distancia1'),
            visa_distancia2=data.get('visa_distancia2'),
            visa1_caduca_mes=to_int(data.get('visa1_caduca_mes')),
            visa2_caduca_mes=to_int(data.get('visa2_caduca_mes')),
            visa1_caduca_ano=to_int(data.get('visa1_caduca_ano')),
            visa2_caduca_ano=to_int(data.get('visa2_caduca_ano')),
            visa1_cod_valid=to_int(data.get('visa1_cod_valid')),
            visa2_cod_valid=to_int(data.get('visa2_cod_valid')),
            acceso_web=data.get('acceso_web'),
            password_web=data.get('password_web'),
            id_tarifa=to_int(data.get('id_tarifa'), -1),
            id_divisa=to_int(data.get('id_divisa'), -1),
            id_idioma_documentos=to_int(data.get('id_idioma_documentos'), -1),
            id_agente=to_int(data.get('id_agente'), -1),
            id_transportista=to_int(data.get('id_transportista'), -1)
        )

    def to_dict(self) -> dict:
        """Convierte a diccionario para SQL INSERT/UPDATE"""
        result = {
            'id_web': self.id_web,
            'codigo_cliente': self.codigo_cliente,
            'apellido1': self.apellido1,
            'apellido2': self.apellido2,
            'nombre': self.nombre,
            'nombre_fiscal': self.nombre_fiscal,
            'nombre_comercial': self.nombre_comercial,
            'persona_contacto': self.persona_contacto,
            'cif_nif_siren': self.cif_nif_siren,
            'siret': self.siret,
            'cif_vies': self.cif_vies,
            'direccion1': self.direccion1,
            'direccion2': self.direccion2,
            'cp': self.cp,
            'poblacion': self.poblacion,
            'provincia': self.provincia,
            'pais': self.pais,
            'telefono1': self.telefono1,
            'telefono2': self.telefono2,
            'fax': self.fax,
            'movil': self.movil,
            'email': self.email,
            'web': self.web,
            'fecha_alta': self.fecha_alta,
            'fecha_ultima_compra': self.fecha_ultima_compra,
            'fecha_nacimiento': self.fecha_nacimiento,
            'acumulado_ventas': float(self.acumulado_ventas),
            'ventas_ejercicio': float(self.ventas_ejercicio),
            'riesgo_maximo': float(self.riesgo_maximo),
            'deuda_actual': float(self.deuda_actual),
            'importe_pendiente': float(self.importe_pendiente),
            'comentarios': self.comentarios,
            'bloqueado': self.bloqueado,
            'comentario_bloqueo': self.comentario_bloqueo,
            'observaciones': self.observaciones,
            'porc_dto_cliente': float(self.porc_dto_cliente),
            'recargo_equivalencia': self.recargo_equivalencia,
            'irpf': float(self.irpf),
            'grupo_iva': self.grupo_iva,
            'cuenta_contable': self.cuenta_contable,
            'cuenta_iva_repercutido': self.cuenta_iva_repercutido,
            'cuenta_deudas': self.cuenta_deudas,
            'cuenta_cobros': self.cuenta_cobros,
            'id_forma_pago': self.id_forma_pago,
            'dia_pago1': self.dia_pago1,
            'dia_pago2': self.dia_pago2,
            'entidad_bancaria': self.entidad_bancaria,
            'oficina_bancaria': self.oficina_bancaria,
            'dc': self.dc,
            'cuenta_corriente': self.cuenta_corriente,
            'importe_a_cuenta': float(self.importe_a_cuenta),
            'vales': float(self.vales),
            'visa_distancia1': self.visa_distancia1,
            'visa_distancia2': self.visa_distancia2,
            'visa1_caduca_mes': self.visa1_caduca_mes,
            'visa2_caduca_mes': self.visa2_caduca_mes,
            'visa1_caduca_ano': self.visa1_caduca_ano,
            'visa2_caduca_ano': self.visa2_caduca_ano,
            'visa1_cod_valid': self.visa1_cod_valid,
            'visa2_cod_valid': self.visa2_cod_valid,
            'acceso_web': self.acceso_web,
            'password_web': self.password_web,
            'id_tarifa': self.id_tarifa,
            'id_divisa': self.id_divisa,
            'id_idioma_documentos': self.id_idioma_documentos,
            'id_agente': self.id_agente,
            'id_transportista': self.id_transportista
        }
        if self.id is not None:
            result['id'] = self.id
        return result


@dataclass
class DireccionAlternativa:
    """Modelo para Direcciones Alternativas de clientes"""
    id: Optional[int] = None
    id_cliente: Optional[int] = None
    descripcion: str = ""
    direccion1: Optional[str] = None
    direccion2: Optional[str] = None
    cp: Optional[str] = None
    poblacion: Optional[str] = None
    provincia: Optional[str] = None
    pais: str = "España"
    email: Optional[str] = None
    telefono: Optional[str] = None
    comentarios: Optional[str] = None
    fecha_creacion: Optional[date] = None
    fecha_modificacion: Optional[date] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'DireccionAlternativa':
        """Crea una instancia desde un diccionario (SQL row)"""
        if not data:
            return None
        return cls(
            id=data.get('id'),
            id_cliente=data.get('id_cliente'),
            descripcion=data.get('descripcion', ''),
            direccion1=data.get('direccion1'),
            direccion2=data.get('direccion2'),
            cp=data.get('cp'),
            poblacion=data.get('poblacion'),
            provincia=data.get('provincia'),
            pais=data.get('pais', 'España'),
            email=data.get('email'),
            telefono=data.get('telefono'),
            comentarios=data.get('comentarios'),
            fecha_creacion=data.get('fecha_creacion'),
            fecha_modificacion=data.get('fecha_modificacion')
        )

    def to_dict(self) -> dict:
        """Convierte a diccionario para SQL INSERT/UPDATE"""
        result = {
            'id_cliente': self.id_cliente,
            'descripcion': self.descripcion,
            'direccion1': self.direccion1,
            'direccion2': self.direccion2,
            'cp': self.cp,
            'poblacion': self.poblacion,
            'provincia': self.provincia,
            'pais': self.pais,
            'email': self.email,
            'telefono': self.telefono,
            'comentarios': self.comentarios,
            'fecha_creacion': self.fecha_creacion,
            'fecha_modificacion': self.fecha_modificacion
        }
        if self.id is not None:
            result['id'] = self.id
        return result

