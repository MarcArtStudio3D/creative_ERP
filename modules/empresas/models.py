"""
Modelos de datos para el módulo de Empresas.
Dataclasses para mantener arquitectura MVC pura sin ORM.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


@dataclass
class Empresa:
    """Modelo para Empresa"""
    id: Optional[int] = None
    group_id: Optional[int] = None
    codigo_empresa: str = ""
    nombre_fiscal: str = ""
    nombre_comercial: Optional[str] = None
    cif_nif: Optional[str] = None
    direccion: Optional[str] = None
    cp: Optional[str] = None
    poblacion: Optional[str] = None
    provincia: Optional[str] = None
    pais: str = "España"
    telefono: Optional[str] = None
    email: Optional[str] = None
    web: Optional[str] = None
    fecha_alta: Optional[date] = None
    activa: bool = True
    notas: Optional[str] = None

    # Datos legales
    tipo_sociedad: Optional[str] = None
    fecha_constitucion: Optional[date] = None
    objeto_social: Optional[str] = None
    capital_social: Decimal = Decimal('0.00')
    moneda_capital: str = "EUR"

    # Contacto
    persona_contacto: Optional[str] = None
    cargo_contacto: Optional[str] = None
    telefono_contacto: Optional[str] = None
    movil_contacto: Optional[str] = None
    fax: Optional[str] = None

    # Dirección fiscal
    direccion_fiscal: Optional[str] = None
    cp_fiscal: Optional[str] = None
    poblacion_fiscal: Optional[str] = None
    provincia_fiscal: Optional[str] = None

    # Datos bancarios
    banco: Optional[str] = None
    sucursal: Optional[str] = None
    dc: Optional[str] = None
    numero_cuenta: Optional[str] = None
    iban: Optional[str] = None
    swift_bic: Optional[str] = None

    # Configuración fiscal
    regimen_iva: str = "General"
    tipo_retencion: Optional[str] = None
    porcentaje_retencion: Decimal = Decimal('0.00')
    exento_iva: bool = False
    intracomunitario: bool = False

    # Configuración comercial
    limite_credito: Decimal = Decimal('0.00')
    dias_pago: int = 30
    descuento_general: Decimal = Decimal('0.00')
    forma_pago_predeterminada: Optional[str] = None

    # Información adicional
    sector_actividad: Optional[str] = None
    numero_empleados: Optional[int] = None
    facturacion_anual: Decimal = Decimal('0.00')
    sitio_web: Optional[str] = None
    observaciones_internas: Optional[str] = None

    # Metadatos
    fecha_modificacion: Optional[datetime] = None
    usuario_modificacion: Optional[str] = None

    # Configuración de base de datos
    motor_base_datos: str = "mariadb"
    nombre_base_datos_maria_db: Optional[str] = None
    nombre_base_datos_postgresql: Optional[str] = None
    host_mariadb: str = "localhost"
    puerto_mariadb: int = 3306
    usuario_mariadb: str = "admin"
    password_mariadb: Optional[str] = None
    host_postgresql: str = "localhost"
    puerto_postgresql: int = 5432
    usuario_postgresql: str = "admin"
    password_postgresql: Optional[str] = None
    ruta_base_datos_sqlite: Optional[str] = None

    # Configuración general
    moneda_predeterminada: str = "EUR"
    actualizar_divisas: bool = False
    aplicar_irpf: bool = False
    porcentaje_irpf: Decimal = Decimal('0.00')
    decimales_totales: int = 2
    decimales_precios: int = 2
    digitos_factura: int = 6
    serie_factura: str = "A"
    dia_cierre_ejercicio: int = 31
    mes_cierre_ejercicio: int = 12

    # Configuración web
    enlace_web_activo: bool = False
    gestion_internacional: bool = False

    # Configuración artículos
    autocodificar_articulos: bool = True
    tamano_codigo_articulo: int = 6
    tarifa_predeterminada: int = 1
    margen_general: Decimal = Decimal('0.00')
    margen_minimo: Decimal = Decimal('0.00')

    # Plantillas
    ruta_logo: Optional[str] = None
    comentario_albaran: Optional[str] = None
    comentario_factura: Optional[str] = None

    # Horarios
    horario_lunes: Optional[str] = None
    horario_martes: Optional[str] = None
    horario_miercoles: Optional[str] = None
    horario_jueves: Optional[str] = None
    horario_viernes: Optional[str] = None
    horario_sabado: Optional[str] = None
    horario_domingo: Optional[str] = None

    # Integración Google Calendar
    google_calendar_id: Optional[str] = None
    google_oauth_token: Optional[str] = None
    google_refresh_token: Optional[str] = None
    google_token_expiry: Optional[datetime] = None

    # Contabilidad
    activar_contabilidad: bool = False
    cuenta_venta_servicios: Optional[str] = None
    cuenta_venta_mercaderias: Optional[str] = None
    cuenta_acreedores: Optional[str] = None
    cuenta_proveedores: Optional[str] = None
    digitos_cuentas_contables: int = 10
    cuenta_clientes: Optional[str] = None
    cuenta_cobros: Optional[str] = None
    cuenta_pagos: Optional[str] = None

    # Cuentas IVA repercutido
    cuenta_iva_repercutido_1: Optional[str] = None
    cuenta_iva_repercutido_2: Optional[str] = None
    cuenta_iva_repercutido_3: Optional[str] = None
    cuenta_iva_repercutido_4: Optional[str] = None
    cuenta_iva_repercutido_re_1: Optional[str] = None
    cuenta_iva_repercutido_re_2: Optional[str] = None
    cuenta_iva_repercutido_re_3: Optional[str] = None

    # Cuentas IVA soportado
    cuenta_iva_soportado_1: Optional[str] = None
    cuenta_iva_soportado_2: Optional[str] = None
    cuenta_iva_soportado_3: Optional[str] = None
    cuenta_iva_soportado_4: Optional[str] = None
    cuenta_iva_soportado_re_1: Optional[str] = None
    cuenta_iva_soportado_re_2: Optional[str] = None
    cuenta_iva_soportado_re_3: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Empresa':
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
            group_id=data.get('group_id'),
            codigo_empresa=data.get('codigo_empresa', ''),
            nombre_fiscal=data.get('nombre_fiscal', ''),
            nombre_comercial=data.get('nombre_comercial'),
            cif_nif=data.get('cif_nif'),
            direccion=data.get('direccion'),
            cp=data.get('cp'),
            poblacion=data.get('poblacion'),
            provincia=data.get('provincia'),
            pais=data.get('pais', 'España'),
            telefono=data.get('telefono'),
            email=data.get('email'),
            web=data.get('web'),
            fecha_alta=data.get('fecha_alta'),
            activa=bool(data.get('activa', True)),
            notas=data.get('notas'),
            tipo_sociedad=data.get('tipo_sociedad'),
            fecha_constitucion=data.get('fecha_constitucion'),
            objeto_social=data.get('objeto_social'),
            capital_social=to_decimal(data.get('capital_social')),
            moneda_capital=data.get('moneda_capital', 'EUR'),
            persona_contacto=data.get('persona_contacto'),
            cargo_contacto=data.get('cargo_contacto'),
            telefono_contacto=data.get('telefono_contacto'),
            movil_contacto=data.get('movil_contacto'),
            fax=data.get('fax'),
            direccion_fiscal=data.get('direccion_fiscal'),
            cp_fiscal=data.get('cp_fiscal'),
            poblacion_fiscal=data.get('poblacion_fiscal'),
            provincia_fiscal=data.get('provincia_fiscal'),
            banco=data.get('banco'),
            sucursal=data.get('sucursal'),
            dc=data.get('dc'),
            numero_cuenta=data.get('numero_cuenta'),
            iban=data.get('iban'),
            swift_bic=data.get('swift_bic'),
            regimen_iva=data.get('regimen_iva', 'General'),
            tipo_retencion=data.get('tipo_retencion'),
            porcentaje_retencion=to_decimal(data.get('porcentaje_retencion')),
            exento_iva=bool(data.get('exento_iva', False)),
            intracomunitario=bool(data.get('intracomunitario', False)),
            limite_credito=to_decimal(data.get('limite_credito')),
            dias_pago=to_int(data.get('dias_pago'), 30),
            descuento_general=to_decimal(data.get('descuento_general')),
            forma_pago_predeterminada=data.get('forma_pago_predeterminada'),
            sector_actividad=data.get('sector_actividad'),
            numero_empleados=to_int(data.get('numero_empleados')) if data.get('numero_empleados') else None,
            facturacion_anual=to_decimal(data.get('facturacion_anual')),
            sitio_web=data.get('sitio_web'),
            observaciones_internas=data.get('observaciones_internas'),
            fecha_modificacion=data.get('fecha_modificacion'),
            usuario_modificacion=data.get('usuario_modificacion'),
            motor_base_datos=data.get('motor_base_datos', 'mariadb'),
            nombre_base_datos_maria_db=data.get('nombre_base_datos_maria_db'),
            nombre_base_datos_postgresql=data.get('nombre_base_datos_postgresql'),
            host_mariadb=data.get('host_mariadb', 'localhost'),
            puerto_mariadb=to_int(data.get('puerto_mariadb'), 3306),
            usuario_mariadb=data.get('usuario_mariadb', 'admin'),
            password_mariadb=data.get('password_mariadb'),
            host_postgresql=data.get('host_postgresql', 'localhost'),
            puerto_postgresql=to_int(data.get('puerto_postgresql'), 5432),
            usuario_postgresql=data.get('usuario_postgresql', 'admin'),
            password_postgresql=data.get('password_postgresql'),
            ruta_base_datos_sqlite=data.get('ruta_base_datos_sqlite'),
            moneda_predeterminada=data.get('moneda_predeterminada', 'EUR'),
            actualizar_divisas=bool(data.get('actualizar_divisas', False)),
            aplicar_irpf=bool(data.get('aplicar_irpf', False)),
            porcentaje_irpf=to_decimal(data.get('porcentaje_irpf')),
            decimales_totales=to_int(data.get('decimales_totales'), 2),
            decimales_precios=to_int(data.get('decimales_precios'), 2),
            digitos_factura=to_int(data.get('digitos_factura'), 6),
            serie_factura=data.get('serie_factura', 'A'),
            dia_cierre_ejercicio=to_int(data.get('dia_cierre_ejercicio'), 31),
            mes_cierre_ejercicio=to_int(data.get('mes_cierre_ejercicio'), 12),
            enlace_web_activo=bool(data.get('enlace_web_activo', False)),
            gestion_internacional=bool(data.get('gestion_internacional', False)),
            autocodificar_articulos=bool(data.get('autocodificar_articulos', True)),
            tamano_codigo_articulo=to_int(data.get('tamano_codigo_articulo'), 6),
            tarifa_predeterminada=to_int(data.get('tarifa_predeterminada'), 1),
            margen_general=to_decimal(data.get('margen_general')),
            margen_minimo=to_decimal(data.get('margen_minimo')),
            ruta_logo=data.get('ruta_logo'),
            comentario_albaran=data.get('comentario_albaran'),
            comentario_factura=data.get('comentario_factura'),
            horario_lunes=data.get('horario_lunes'),
            horario_martes=data.get('horario_martes'),
            horario_miercoles=data.get('horario_miercoles'),
            horario_jueves=data.get('horario_jueves'),
            horario_viernes=data.get('horario_viernes'),
            horario_sabado=data.get('horario_sabado'),
            horario_domingo=data.get('horario_domingo'),
            google_calendar_id=data.get('google_calendar_id'),
            google_oauth_token=data.get('google_oauth_token'),
            google_refresh_token=data.get('google_refresh_token'),
            google_token_expiry=data.get('google_token_expiry'),
            activar_contabilidad=bool(data.get('activar_contabilidad', False)),
            cuenta_venta_servicios=data.get('cuenta_venta_servicios'),
            cuenta_venta_mercaderias=data.get('cuenta_venta_mercaderias'),
            cuenta_acreedores=data.get('cuenta_acreedores'),
            cuenta_proveedores=data.get('cuenta_proveedores'),
            digitos_cuentas_contables=to_int(data.get('digitos_cuentas_contables'), 10),
            cuenta_clientes=data.get('cuenta_clientes'),
            cuenta_cobros=data.get('cuenta_cobros'),
            cuenta_pagos=data.get('cuenta_pagos'),
            cuenta_iva_repercutido_1=data.get('cuenta_iva_repercutido_1'),
            cuenta_iva_repercutido_2=data.get('cuenta_iva_repercutido_2'),
            cuenta_iva_repercutido_3=data.get('cuenta_iva_repercutido_3'),
            cuenta_iva_repercutido_4=data.get('cuenta_iva_repercutido_4'),
            cuenta_iva_repercutido_re_1=data.get('cuenta_iva_repercutido_re_1'),
            cuenta_iva_repercutido_re_2=data.get('cuenta_iva_repercutido_re_2'),
            cuenta_iva_repercutido_re_3=data.get('cuenta_iva_repercutido_re_3'),
            cuenta_iva_soportado_1=data.get('cuenta_iva_soportado_1'),
            cuenta_iva_soportado_2=data.get('cuenta_iva_soportado_2'),
            cuenta_iva_soportado_3=data.get('cuenta_iva_soportado_3'),
            cuenta_iva_soportado_4=data.get('cuenta_iva_soportado_4'),
            cuenta_iva_soportado_re_1=data.get('cuenta_iva_soportado_re_1'),
            cuenta_iva_soportado_re_2=data.get('cuenta_iva_soportado_re_2'),
            cuenta_iva_soportado_re_3=data.get('cuenta_iva_soportado_re_3')
        )

    def to_dict(self) -> dict:
        """Convierte a diccionario para SQL INSERT/UPDATE (solo campos principales)"""
        # Simplificado - incluir solo los campos más usados
        # Para un UPDATE completo, se pueden incluir todos los campos
        result = {
            'group_id': self.group_id,
            'codigo_empresa': self.codigo_empresa,
            'nombre_fiscal': self.nombre_fiscal,
            'nombre_comercial': self.nombre_comercial,
            'cif_nif': self.cif_nif,
            'direccion': self.direccion,
            'cp': self.cp,
            'poblacion': self.poblacion,
            'provincia': self.provincia,
            'pais': self.pais,
            'telefono': self.telefono,
            'email': self.email,
            'web': self.web,
            'fecha_alta': self.fecha_alta,
            'activa': self.activa,
            'motor_base_datos': self.motor_base_datos,
            'nombre_base_datos_maria_db': self.nombre_base_datos_maria_db,
            'host_mariadb': self.host_mariadb,
            'puerto_mariadb': self.puerto_mariadb,
            'usuario_mariadb': self.usuario_mariadb,
            'password_mariadb': self.password_mariadb
        }
        if self.id is not None:
            result['id'] = self.id
        return result

