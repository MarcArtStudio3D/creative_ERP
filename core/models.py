"""
Modelos Peewee para el core de la aplicación.
Migración completa desde SQLModel a Peewee.
"""

from datetime import datetime
from peewee import (
    Model,
    AutoField,
    CharField,
    TextField,
    IntegerField,
    FloatField,
    DateField,
    DateTimeField,
)

from core.peewee_db import database_proxy


class BaseModel(Model):
    """Modelo base que usa el proxy de base de datos."""
    class Meta:
        database = database_proxy


class User(BaseModel):
    """Modelo de Usuario para autenticación."""

    id = AutoField(primary_key=True)
    username = CharField(max_length=50, unique=True, index=True)
    email = CharField(max_length=100, unique=True, index=True)
    full_name = CharField(max_length=100)
    password_hash = CharField(max_length=255)
    role = CharField(max_length=20)
    is_active = IntegerField(default=1)
    created_at = DateTimeField(default=datetime.utcnow)
    last_login = DateTimeField(null=True)

    # Multi-empresa
    allowed_groups = CharField(default="[]")  # JSON array of group IDs

    class Meta:
        table_name = 'users'

    def verify_password(self, password: str) -> bool:
        """Verifica la contraseña del usuario."""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)


class BusinessGroup(BaseModel):
    """Modelo de Grupo Empresarial."""

    id = AutoField(primary_key=True)
    name = CharField(max_length=100)
    code = CharField(max_length=10, unique=True, index=True)
    description = TextField(null=True)
    created_at = DateTimeField(default=datetime.utcnow)

    class Meta:
        table_name = 'business_groups'


class Empresa(BaseModel):
    """Modelo de Empresa."""

    id = AutoField(primary_key=True)
    group_id = IntegerField(default=1)  # ForeignKey a business_groups
    codigo_empresa = CharField(max_length=50, unique=True, index=True)
    nombre_fiscal = CharField(max_length=200)
    nombre_comercial = CharField(max_length=200, null=True)
    cif_nif = CharField(max_length=50, unique=True, index=True)
    direccion = CharField(max_length=255, null=True)
    cp = CharField(max_length=10, null=True)
    poblacion = CharField(max_length=100, null=True)
    provincia = CharField(max_length=100, null=True)
    pais = CharField(max_length=100, default="España")
    telefono = CharField(max_length=50, null=True)
    email = CharField(max_length=200, null=True)
    web = CharField(max_length=200, null=True)
    fecha_alta = DateTimeField(default=datetime.utcnow)
    activa = IntegerField(default=1)
    notas = TextField(null=True)

    # Información fiscal adicional
    tipo_sociedad = CharField(max_length=100, null=True)
    fecha_constitucion = DateField(null=True)
    objeto_social = TextField(null=True)
    capital_social = FloatField(default=0.0)
    moneda_capital = CharField(max_length=3, default="EUR")

    # Datos de contacto adicionales
    persona_contacto = CharField(max_length=200, null=True)
    cargo_contacto = CharField(max_length=100, null=True)
    telefono_contacto = CharField(max_length=50, null=True)
    movil_contacto = CharField(max_length=50, null=True)
    fax = CharField(max_length=50, null=True)

    # Dirección fiscal (si es diferente)
    direccion_fiscal = CharField(max_length=255, null=True)
    cp_fiscal = CharField(max_length=10, null=True)
    poblacion_fiscal = CharField(max_length=100, null=True)
    provincia_fiscal = CharField(max_length=100, null=True)

    # Información bancaria
    banco = CharField(max_length=100, null=True)
    sucursal = CharField(max_length=100, null=True)
    dc = CharField(max_length=2, null=True)
    numero_cuenta = CharField(max_length=10, null=True)
    iban = CharField(max_length=34, null=True)
    swift_bic = CharField(max_length=11, null=True)

    # Configuración fiscal
    regimen_iva = CharField(max_length=50, default="General")
    tipo_retencion = CharField(max_length=50, null=True)
    porcentaje_retencion = FloatField(default=0.0)
    exento_iva = IntegerField(default=0)
    intracomunitario = IntegerField(default=0)

    # Límites y condiciones comerciales
    limite_credito = FloatField(default=0.0)
    dias_pago = IntegerField(default=30)
    descuento_general = FloatField(default=0.0)
    forma_pago_predeterminada = CharField(max_length=50, null=True)

    # Información adicional
    sector_actividad = CharField(max_length=100, null=True)
    numero_empleados = IntegerField(null=True)
    facturacion_anual = FloatField(null=True)
    sitio_web = CharField(max_length=200, null=True)
    observaciones_internas = TextField(null=True)

    # Metadatos
    fecha_modificacion = DateTimeField(default=datetime.utcnow)
    usuario_modificacion = CharField(max_length=100, null=True)

    # Configuración de base de datos por empresa
    motor_base_datos = CharField(max_length=20, default="mariadb")
    nombre_base_datos_maria_db = CharField(max_length=100, null=True)
    nombre_base_datos_postgresql = CharField(max_length=100, null=True)
    host_mariadb = CharField(max_length=100, default="localhost")
    puerto_mariadb = IntegerField(default=3306)
    usuario_mariadb = CharField(max_length=50, default="admin")
    password_mariadb = CharField(max_length=255, default="admin123")
    host_postgresql = CharField(max_length=100, default="localhost")
    puerto_postgresql = IntegerField(default=5432)
    usuario_postgresql = CharField(max_length=50, default="postgres")
    password_postgresql = CharField(max_length=255, default="postgres")

    # SQLite
    ruta_base_datos_sqlite = CharField(max_length=255, null=True)

    # Configuración y Divisas
    moneda_predeterminada = CharField(max_length=10, default="EUR")
    actualizar_divisas = IntegerField(default=0)
    aplicar_irpf = IntegerField(default=0)
    porcentaje_irpf = FloatField(default=0.0)
    decimales_totales = IntegerField(default=2)
    decimales_precios = IntegerField(default=2)

    # Facturación
    digitos_factura = IntegerField(default=7)
    serie_factura = CharField(max_length=20, null=True)
    dia_cierre_ejercicio = IntegerField(default=31)
    mes_cierre_ejercicio = IntegerField(default=12)

    # Varios y Artículos
    enlace_web_activo = IntegerField(default=0)
    gestion_internacional = IntegerField(default=0)
    autocodificar_articulos = IntegerField(default=1)
    tamano_codigo_articulo = IntegerField(default=15)
    tarifa_predeterminada = CharField(max_length=50, null=True)
    margen_general = FloatField(default=0.0)
    margen_minimo = FloatField(default=0.0)

    # Logotipo y Comentarios
    ruta_logo = CharField(max_length=255, null=True)
    comentario_albaran = TextField(null=True)
    comentario_factura = TextField(null=True)

    # Horarios
    horario_lunes = CharField(max_length=100, null=True)
    horario_martes = CharField(max_length=100, null=True)
    horario_miercoles = CharField(max_length=100, null=True)
    horario_jueves = CharField(max_length=100, null=True)
    horario_viernes = CharField(max_length=100, null=True)
    horario_sabado = CharField(max_length=100, null=True)
    horario_domingo = CharField(max_length=100, null=True)

    # Integraciones (Google)
    google_calendar_id = CharField(max_length=255, null=True)
    google_oauth_token = TextField(null=True)
    google_refresh_token = TextField(null=True)
    google_token_expiry = CharField(max_length=100, null=True)

    # Contabilidad
    activar_contabilidad = IntegerField(default=1)
    cuenta_venta_servicios = CharField(max_length=20, null=True)
    cuenta_venta_mercaderias = CharField(max_length=20, null=True)
    cuenta_acreedores = CharField(max_length=20, null=True)
    cuenta_proveedores = CharField(max_length=20, null=True)
    digitos_cuentas_contables = IntegerField(default=8)
    cuenta_clientes = CharField(max_length=20, null=True)
    cuenta_cobros = CharField(max_length=20, null=True)
    cuenta_pagos = CharField(max_length=20, null=True)

    # Cuentas IVA (Repercutido y Soportado)
    cuenta_iva_repercutido_1 = CharField(max_length=20, null=True)
    cuenta_iva_repercutido_2 = CharField(max_length=20, null=True)
    cuenta_iva_repercutido_3 = CharField(max_length=20, null=True)
    cuenta_iva_repercutido_4 = CharField(max_length=20, null=True)

    cuenta_iva_repercutido_re_1 = CharField(max_length=20, null=True)
    cuenta_iva_repercutido_re_2 = CharField(max_length=20, null=True)
    cuenta_iva_repercutido_re_3 = CharField(max_length=20, null=True)

    cuenta_iva_soportado_1 = CharField(max_length=20, null=True)
    cuenta_iva_soportado_2 = CharField(max_length=20, null=True)
    cuenta_iva_soportado_3 = CharField(max_length=20, null=True)
    cuenta_iva_soportado_4 = CharField(max_length=20, null=True)

    cuenta_iva_soportado_re_1 = CharField(max_length=20, null=True)
    cuenta_iva_soportado_re_2 = CharField(max_length=20, null=True)
    cuenta_iva_soportado_re_3 = CharField(max_length=20, null=True)

    class Meta:
        table_name = 'empresas'

