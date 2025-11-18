# -----------------------------
# core/models.py
# -----------------------------
"""Modelos de base de datos con SQLAlchemy."""

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
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
    client = relationship('Cliente', back_populates='invoices')
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