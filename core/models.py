# -----------------------------
# core/models.py
# -----------------------------
"""Modelos de base de datos con SQLAlchemy."""

from sqlalchemy import Column, Integer, String, DateTime, Date, Float, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()


class Invoice(Base):
    """Modelo de Factura."""
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False, unique=True)
    client_id = Column(Integer, ForeignKey('clientes.id'))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default='draft')
    total = Column(Float, default=0.0)
    currency = Column(String, default='EUR')
    xml_path = Column(String, nullable=True)
    pdf_path = Column(String, nullable=True)
    
    # Relaciones
    # client = relationship('Cliente', back_populates='invoices')  # Deshabilitado por import circular
    lines = relationship('InvoiceLine', back_populates='invoice')


class InvoiceLine(Base):
    """Modelo de Línea de Factura."""
    __tablename__ = 'invoice_lines'
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    description = Column(Text)
    qty = Column(Float, default=1.0)
    unit_price = Column(Float, default=0.0)
    vat = Column(Float, default=0.0)
    
    # Relaciones
    invoice = relationship('Invoice', back_populates='lines')


class User(Base):
    """Modelo de Usuario para autenticación."""
    __tablename__ = 'users'
    
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
    allowed_groups = Column(Text, default='[]')  # JSON array of group IDs


class BusinessGroup(Base):
    """Modelo de Grupo Empresarial."""
    __tablename__ = 'business_groups'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Company(Base):
    """Modelo de Empresa."""
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('business_groups.id'), nullable=False)
    name = Column(String(100), nullable=False)
    legal_name = Column(String(200), nullable=False)
    vat_number = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relaciones
    group = relationship('BusinessGroup', backref='companies')


class Empresa(Base):
    """Modelo de Empresa."""
    __tablename__ = "empresas"
    
    id = Column(Integer, primary_key=True)
    codigo_empresa = Column(String(50), nullable=False, unique=True)
    nombre_fiscal = Column(String(200), nullable=False)
    nombre_comercial = Column(String(200))
    cif_nif = Column(String(50), nullable=False, unique=True)
    direccion = Column(String(255))
    cp = Column(String(10))
    poblacion = Column(String(100))
    provincia = Column(String(100))
    id_pais = Column(Integer, default=1)
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
    moneda_capital = Column(String(3), default='EUR')
    
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
    regimen_iva = Column(String(50), default='General')
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
