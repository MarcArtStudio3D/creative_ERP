# -----------------------------
# core/models.py
# -----------------------------
"""Modelos de base de datos con SQLAlchemy."""

import datetime

from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    """Modelo de Usuario para autenticación."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # UserRole enum as string
    is_active = Column(Integer, default=1)  # SQLite boolean
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Multi-empresa
    allowed_groups = Column(Text, default="[]")  # JSON array of group IDs


class BusinessGroup(Base):
    """Modelo de Grupo Empresarial."""

    __tablename__ = "business_groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Empresa(Base):
    """Modelo de Empresa."""

    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True)
    group_id = Column(
        Integer, ForeignKey("business_groups.id"), nullable=False, default=1
    )
    codigo_empresa = Column(String(50), nullable=False, unique=True)
    nombre_fiscal = Column(String(200), nullable=False)
    nombre_comercial = Column(String(200))
    cif_nif = Column(String(50), nullable=False, unique=True)
    direccion = Column(String(255))
    cp = Column(String(10))
    poblacion = Column(String(100))
    provincia = Column(String(100))
    pais = Column(String(100), default="España")
    telefono = Column(String(50))
    email = Column(String(200))
    web = Column(String(200))
    fecha_alta = Column(DateTime, default=datetime.datetime.utcnow)
    activa = Column(Integer, default=1)  # Boolean en SQLite
    notas = Column(Text)

    # Información fiscal adicional
    tipo_sociedad = Column(String(100))  # S.L., S.A., etc.
    fecha_constitucion = Column(Date)
    objeto_social = Column(Text)
    capital_social = Column(Float, default=0.0)
    moneda_capital = Column(String(3), default="EUR")

    # Datos de contacto adicionales
    persona_contacto = Column(String(200))
    cargo_contacto = Column(String(100))
    telefono_contacto = Column(String(50))
    movil_contacto = Column(String(50))
    fax = Column(String(50))

    # Dirección fiscal (si es diferente)
    direccion_fiscal = Column(String(255))
    cp_fiscal = Column(String(10))
    poblacion_fiscal = Column(String(100))
    provincia_fiscal = Column(String(100))

    # Información bancaria
    banco = Column(String(100))
    sucursal = Column(String(100))
    dc = Column(String(2))  # Dígitos de control
    numero_cuenta = Column(String(10))
    iban = Column(String(34))
    swift_bic = Column(String(11))

    # Configuración fiscal
    regimen_iva = Column(String(50), default="General")
    tipo_retencion = Column(String(50))
    porcentaje_retencion = Column(Float, default=0.0)
    exento_iva = Column(Integer, default=0)  # Boolean
    intracomunitario = Column(Integer, default=0)  # Boolean

    # Límites y condiciones comerciales
    limite_credito = Column(Float, default=0.0)
    dias_pago = Column(Integer, default=30)
    descuento_general = Column(Float, default=0.0)
    forma_pago_predeterminada = Column(String(50))

    # Información adicional
    sector_actividad = Column(String(100))
    numero_empleados = Column(Integer)
    facturacion_anual = Column(Float)
    sitio_web = Column(String(200))  # Campo adicional para web
    observaciones_internas = Column(Text)

    # Metadatos
    fecha_modificacion = Column(DateTime, default=datetime.datetime.utcnow)
    usuario_modificacion = Column(String(100))

    # Configuración de base de datos por empresa
    motor_base_datos = Column(
        String(20),
        default="mariadb",
        comment="Motor de base de datos: mariadb o postgresql",
    )
    nombre_base_datos_maria_db = Column(
        String(100), comment="Nombre de la base de datos MariaDB"
    )
    nombre_base_datos_postgresql = Column(
        String(100), comment="Nombre de la base de datos PostgreSQL"
    )
    host_mariadb = Column(
        String(100), default="localhost", comment="Host del servidor MariaDB"
    )
    puerto_mariadb = Column(
        Integer, default=3306, comment="Puerto del servidor MariaDB"
    )
    usuario_mariadb = Column(String(50), default="admin", comment="Usuario MariaDB")
    password_mariadb = Column(
        String(255), default="admin123", comment="Contraseña MariaDB"
    )
    host_postgresql = Column(
        String(100), default="localhost", comment="Host del servidor PostgreSQL"
    )
    puerto_postgresql = Column(
        Integer, default=5432, comment="Puerto del servidor PostgreSQL"
    )
    usuario_postgresql = Column(
        String(50), default="postgres", comment="Usuario PostgreSQL"
    )
    password_postgresql = Column(
        String(255), default="postgres", comment="Contraseña PostgreSQL"
    )

    # SQLite
    ruta_base_datos_sqlite = Column(
        String(255), comment="Ruta relativa o absoluta a la BD SQLite"
    )

    # --- NUEVOS CAMPOS AÑADIDOS ---

    # Configuración y Divisas
    moneda_predeterminada = Column(String(10), default="EUR")
    actualizar_divisas = Column(Integer, default=0)
    aplicar_irpf = Column(Integer, default=0)
    porcentaje_irpf = Column(Float, default=0.0)
    decimales_totales = Column(Integer, default=2)
    decimales_precios = Column(Integer, default=2)

    # Facturación
    digitos_factura = Column(Integer, default=7)
    serie_factura = Column(String(20))
    dia_cierre_ejercicio = Column(Integer, default=31)
    mes_cierre_ejercicio = Column(Integer, default=12)

    # Varios y Artículos
    enlace_web_activo = Column(Integer, default=0)
    gestion_internacional = Column(Integer, default=0)
    autocodificar_articulos = Column(Integer, default=1)
    tamano_codigo_articulo = Column(Integer, default=15)
    tarifa_predeterminada = Column(String(50))
    margen_general = Column(Float, default=0.0)
    margen_minimo = Column(Float, default=0.0)

    # Logotipo y Comentarios
    ruta_logo = Column(String(255))
    comentario_albaran = Column(Text)
    comentario_factura = Column(Text)

    # Horarios
    horario_lunes = Column(String(100))
    horario_martes = Column(String(100))
    horario_miercoles = Column(String(100))
    horario_jueves = Column(String(100))
    horario_viernes = Column(String(100))
    horario_sabado = Column(String(100))
    horario_domingo = Column(String(100))

    # Integraciones (Google)
    google_calendar_id = Column(String(255))
    google_oauth_token = Column(Text)
    google_refresh_token = Column(Text)
    google_token_expiry = Column(String(100))

    # Contabilidad
    activar_contabilidad = Column(Integer, default=1)
    cuenta_venta_servicios = Column(String(20))
    cuenta_venta_mercaderias = Column(String(20))
    cuenta_acreedores = Column(String(20))
    cuenta_proveedores = Column(String(20))
    digitos_cuentas_contables = Column(Integer, default=8)
    cuenta_clientes = Column(String(20))
    cuenta_cobros = Column(String(20))
    cuenta_pagos = Column(String(20))

    # Cuentas IVA (Repercutido y Soportado)
    cuenta_iva_repercutido_1 = Column(String(20))
    cuenta_iva_repercutido_2 = Column(String(20))
    cuenta_iva_repercutido_3 = Column(String(20))
    cuenta_iva_repercutido_4 = Column(String(20))

    cuenta_iva_repercutido_re_1 = Column(String(20))
    cuenta_iva_repercutido_re_2 = Column(String(20))
    cuenta_iva_repercutido_re_3 = Column(String(20))
    cuenta_iva_repercutido_re_4 = Column(String(20))

    cuenta_iva_soportado_1 = Column(String(20))
    cuenta_iva_soportado_2 = Column(String(20))
    cuenta_iva_soportado_3 = Column(String(20))
    cuenta_iva_soportado_4 = Column(String(20))

    cuenta_iva_soportado_re_1 = Column(String(20))
    cuenta_iva_soportado_re_2 = Column(String(20))
    cuenta_iva_soportado_re_3 = Column(String(20))
    cuenta_iva_soportado_re_4 = Column(String(20))

    # Datos Registrales Adicionales
    inscripcion_registro = Column(String(200))
    ciudad_rcs = Column(String(100))
    numero_rcs = Column(String(50))
    numero_rm = Column(String(50))
    siret = Column(String(50))
    ape_naf = Column(String(20))

    # Relaciones
    group = relationship("BusinessGroup", backref="empresas")
