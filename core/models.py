# -----------------------------
# core/models.py
# -----------------------------
"""Modelos de base de datos con SQLModel."""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date


class User(SQLModel, table=True):
    """Modelo de Usuario para autenticación."""
    __tablename__ = 'users'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True, index=True)
    email: str = Field(max_length=100, unique=True, index=True)
    full_name: str = Field(max_length=100)
    password_hash: str = Field(max_length=255)
    role: str = Field(max_length=20)  # UserRole enum as string
    is_active: int = Field(default=1)  # SQLite boolean
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    # Multi-empresa
    allowed_groups: str = Field(default='[]')  # JSON array of group IDs


class BusinessGroup(SQLModel, table=True):
    """Modelo de Grupo Empresarial."""
    __tablename__ = 'business_groups'
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    code: str = Field(max_length=10, unique=True, index=True)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relaciones
    empresas: List["Empresa"] = Relationship(back_populates="group")


class Empresa(SQLModel, table=True):
    """Modelo de Empresa."""
    __tablename__ = "empresas"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="business_groups.id", default=1)
    codigo_empresa: str = Field(max_length=50, unique=True, index=True)
    nombre_fiscal: str = Field(max_length=200)
    nombre_comercial: Optional[str] = Field(default=None, max_length=200)
    cif_nif: str = Field(max_length=50, unique=True, index=True)
    direccion: Optional[str] = Field(default=None, max_length=255)
    cp: Optional[str] = Field(default=None, max_length=10)
    poblacion: Optional[str] = Field(default=None, max_length=100)
    provincia: Optional[str] = Field(default=None, max_length=100)
    pais: str = Field(default='España', max_length=100)
    telefono: Optional[str] = Field(default=None, max_length=50)
    email: Optional[str] = Field(default=None, max_length=200)
    web: Optional[str] = Field(default=None, max_length=200)
    fecha_alta: datetime = Field(default_factory=datetime.utcnow)
    activa: int = Field(default=1)  # Boolean en SQLite
    notas: Optional[str] = None
    
    # Información fiscal adicional
    tipo_sociedad: Optional[str] = Field(default=None, max_length=100)  # S.L., S.A., etc.
    fecha_constitucion: Optional[date] = None
    objeto_social: Optional[str] = None
    capital_social: float = Field(default=0.0)
    moneda_capital: str = Field(default='EUR', max_length=3)
    
    # Datos de contacto adicionales
    persona_contacto: Optional[str] = Field(default=None, max_length=200)
    cargo_contacto: Optional[str] = Field(default=None, max_length=100)
    telefono_contacto: Optional[str] = Field(default=None, max_length=50)
    movil_contacto: Optional[str] = Field(default=None, max_length=50)
    fax: Optional[str] = Field(default=None, max_length=50)
    
    # Dirección fiscal (si es diferente)
    direccion_fiscal: Optional[str] = Field(default=None, max_length=255)
    cp_fiscal: Optional[str] = Field(default=None, max_length=10)
    poblacion_fiscal: Optional[str] = Field(default=None, max_length=100)
    provincia_fiscal: Optional[str] = Field(default=None, max_length=100)
    
    # Información bancaria
    banco: Optional[str] = Field(default=None, max_length=100)
    sucursal: Optional[str] = Field(default=None, max_length=100)
    dc: Optional[str] = Field(default=None, max_length=2)  # Dígitos de control
    numero_cuenta: Optional[str] = Field(default=None, max_length=10)
    iban: Optional[str] = Field(default=None, max_length=34)
    swift_bic: Optional[str] = Field(default=None, max_length=11)
    
    # Configuración fiscal
    regimen_iva: str = Field(default='General', max_length=50)
    tipo_retencion: Optional[str] = Field(default=None, max_length=50)
    porcentaje_retencion: float = Field(default=0.0)
    exento_iva: int = Field(default=0)  # Boolean
    intracomunitario: int = Field(default=0)  # Boolean
    
    # Límites y condiciones comerciales
    limite_credito: float = Field(default=0.0)
    dias_pago: int = Field(default=30)
    descuento_general: float = Field(default=0.0)
    forma_pago_predeterminada: Optional[str] = Field(default=None, max_length=50)
    
    # Información adicional
    sector_actividad: Optional[str] = Field(default=None, max_length=100)
    numero_empleados: Optional[int] = None
    facturacion_anual: Optional[float] = None
    sitio_web: Optional[str] = Field(default=None, max_length=200)
    observaciones_internas: Optional[str] = None
    
    # Metadatos
    fecha_modificacion: datetime = Field(default_factory=datetime.utcnow)
    usuario_modificacion: Optional[str] = Field(default=None, max_length=100)

    # Configuración de base de datos por empresa
    motor_base_datos: str = Field(default='mariadb', max_length=20)
    nombre_base_datos_maria_db: Optional[str] = Field(default=None, max_length=100)
    nombre_base_datos_postgresql: Optional[str] = Field(default=None, max_length=100)
    host_mariadb: str = Field(default='localhost', max_length=100)
    puerto_mariadb: int = Field(default=3306)
    usuario_mariadb: str = Field(default='admin', max_length=50)
    password_mariadb: str = Field(default='admin123', max_length=255)
    host_postgresql: str = Field(default='localhost', max_length=100)
    puerto_postgresql: int = Field(default=5432)
    usuario_postgresql: str = Field(default='postgres', max_length=50)
    password_postgresql: str = Field(default='postgres', max_length=255)
    
    # SQLite
    ruta_base_datos_sqlite: Optional[str] = Field(default=None, max_length=255)

    # Configuración y Divisas
    moneda_predeterminada: str = Field(default='EUR', max_length=10)
    actualizar_divisas: int = Field(default=0)
    aplicar_irpf: int = Field(default=0)
    porcentaje_irpf: float = Field(default=0.0)
    decimales_totales: int = Field(default=2)
    decimales_precios: int = Field(default=2)

    # Facturación
    digitos_factura: int = Field(default=7)
    serie_factura: Optional[str] = Field(default=None, max_length=20)
    dia_cierre_ejercicio: int = Field(default=31)
    mes_cierre_ejercicio: int = Field(default=12)

    # Varios y Artículos
    enlace_web_activo: int = Field(default=0)
    gestion_internacional: int = Field(default=0)
    autocodificar_articulos: int = Field(default=1)
    tamano_codigo_articulo: int = Field(default=15)
    tarifa_predeterminada: Optional[str] = Field(default=None, max_length=50)
    margen_general: float = Field(default=0.0)
    margen_minimo: float = Field(default=0.0)

    # Logotipo y Comentarios
    ruta_logo: Optional[str] = Field(default=None, max_length=255)
    comentario_albaran: Optional[str] = None
    comentario_factura: Optional[str] = None

    # Horarios
    horario_lunes: Optional[str] = Field(default=None, max_length=100)
    horario_martes: Optional[str] = Field(default=None, max_length=100)
    horario_miercoles: Optional[str] = Field(default=None, max_length=100)
    horario_jueves: Optional[str] = Field(default=None, max_length=100)
    horario_viernes: Optional[str] = Field(default=None, max_length=100)
    horario_sabado: Optional[str] = Field(default=None, max_length=100)
    horario_domingo: Optional[str] = Field(default=None, max_length=100)

    # Integraciones (Google)
    google_calendar_id: Optional[str] = Field(default=None, max_length=255)
    google_oauth_token: Optional[str] = None
    google_refresh_token: Optional[str] = None
    google_token_expiry: Optional[str] = Field(default=None, max_length=100)

    # Contabilidad
    activar_contabilidad: int = Field(default=1)
    cuenta_venta_servicios: Optional[str] = Field(default=None, max_length=20)
    cuenta_venta_mercaderias: Optional[str] = Field(default=None, max_length=20)
    cuenta_acreedores: Optional[str] = Field(default=None, max_length=20)
    cuenta_proveedores: Optional[str] = Field(default=None, max_length=20)
    digitos_cuentas_contables: int = Field(default=8)
    cuenta_clientes: Optional[str] = Field(default=None, max_length=20)
    cuenta_cobros: Optional[str] = Field(default=None, max_length=20)
    cuenta_pagos: Optional[str] = Field(default=None, max_length=20)
    
    # Cuentas IVA (Repercutido y Soportado)
    cuenta_iva_repercutido_1: Optional[str] = Field(default=None, max_length=20)
    cuenta_iva_repercutido_2: Optional[str] = Field(default=None, max_length=20)
    cuenta_iva_repercutido_3: Optional[str] = Field(default=None, max_length=20)
    cuenta_iva_repercutido_4: Optional[str] = Field(default=None, max_length=20)
    
    cuenta_iva_repercutido_re_1: Optional[str] = Field(default=None, max_length=20)
    cuenta_iva_repercutido_re_2: Optional[str] = Field(default=None, max_length=20)
    cuenta_iva_repercutido_re_3: Optional[str] = Field(default=None, max_length=20)
    cuenta_iva_repercutido_re_4: Optional[str] = Field(default=None, max_length=20)
    
    cuenta_iva_soportado_1: Optional[str] = Field(default=None, max_length=20)
    cuenta_iva_soportado_2: Optional[str] = Field(default=None, max_length=20)
    cuenta_iva_soportado_3: Optional[str] = Field(default=None, max_length=20)
    cuenta_iva_soportado_4: Optional[str] = Field(default=None, max_length=20)
    
    cuenta_iva_soportado_re_1: Optional[str] = Field(default=None, max_length=20)
    cuenta_iva_soportado_re_2: Optional[str] = Field(default=None, max_length=20)
    cuenta_iva_soportado_re_3: Optional[str] = Field(default=None, max_length=20)
    cuenta_iva_soportado_re_4: Optional[str] = Field(default=None, max_length=20)

    # Datos Registrales Adicionales
    inscripcion_registro: Optional[str] = Field(default=None, max_length=200)
    ciudad_rcs: Optional[str] = Field(default=None, max_length=100)
    numero_rcs: Optional[str] = Field(default=None, max_length=50)
    numero_rm: Optional[str] = Field(default=None, max_length=50)
    siret: Optional[str] = Field(default=None, max_length=50)
    ape_naf: Optional[str] = Field(default=None, max_length=20)

    # Relación
    group: Optional[BusinessGroup] = Relationship(back_populates="empresas")

