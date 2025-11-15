# -----------------------------
# core/models.py
# -----------------------------
"""Modelos de base de datos con SQLAlchemy."""

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()


class Client(Base):
    """Modelo de Cliente."""
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    country = Column(String, nullable=False)  # 'ES' or 'FR'
    vat_number = Column(String)
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relaciones
    invoices = relationship('Invoice', back_populates='client')


class Invoice(Base):
    """Modelo de Factura."""
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False, unique=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default='draft')
    total = Column(Float, default=0.0)
    currency = Column(String, default='EUR')
    xml_path = Column(String, nullable=True)
    pdf_path = Column(String, nullable=True)
    
    # Relaciones
    client = relationship('Client', back_populates='invoices')
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