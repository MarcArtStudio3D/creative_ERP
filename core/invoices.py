# -----------------------------
# core/invoices.py
# -----------------------------
# (guardar como core/invoices.py)
import os
from jinja2 import Environment, FileSystemLoader
from .db import SessionLocal
from .models import Invoice, InvoiceLine
from datetime import datetime


TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', 'xml_templates')


env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))




def generate_invoice_files(invoice_id: int):
"""Genera PDF y XML (placeholders)."""
db = SessionLocal()
inv = db.query(Invoice).filter(Invoice.id == invoice_id).first()
if not inv:
raise ValueError('Invoice not found')


# Rellenar datos para la plantilla XML
template = env.get_template('facturae_template.xml.j2' if inv.client.country == 'ES' else 'facturx_template.xml.j2')
xml_content = template.render(invoice=inv)


out_dir = os.path.join(os.getcwd(), 'out')
os.makedirs(out_dir, exist_ok=True)
xml_path = os.path.join(out_dir, f'invoice_{inv.id}.xml')
with open(xml_path, 'wb') as f:
f.write(xml_content.encode('utf-8'))


# Generar PDF simple: guardamos un HTML renderizado (implementación simple — luego usar QtWebEngine o reportlab)
pdf_path = os.path.join(out_dir, f'invoice_{inv.id}.pdf')
with open(pdf_path, 'wb') as f:
f.write(b'%PDF-1.4\n% PDF placeholder for invoice')


inv.xml_path = xml_path
inv.pdf_path = pdf_path
db.commit()
return xml_path, pdf_path

