# -----------------------------
# core/models.py
# -----------------------------

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import declarative_base, relationship
import datetime


Base = declarative_base()


class Client(Base):
__tablename__ = 'clients'
id = Column(Integer, primary_key=True)
name = Column(String, nullable=False)
email = Column(String)
country = Column(String, nullable=False) # 'ES' or 'FR'
vat_number = Column(String)
address = Column(Text)
created_at = Column(DateTime, default=datetime.datetime.utcnow)


invoices = relationship('Invoice', back_populates='client')


class Invoice(Base):
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


client = relationship('Client', back_populates='invoices')


class InvoiceLine(Base):
__tablename__ = 'invoice_lines'
id = Column(Integer, primary_key=True)
invoice_id = Column(Integer, ForeignKey('invoices.id'))
description = Column(Text)
qty = Column(Float, default=1.0)
unit_price = Column(Float, default=0.0)
vat = Column(Float, default=0.0)