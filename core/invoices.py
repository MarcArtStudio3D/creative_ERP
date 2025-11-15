# -----------------------------
# core/invoices.py
# -----------------------------
"""Generación de facturas en PDF y XML (Facturae/FacturX)."""

import os
from jinja2 import Environment, FileSystemLoader
from .db import SessionLocal
from .models import Invoice, InvoiceLine
from datetime import datetime

# Directorio de plantillas XML
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', 'xml')

# Motor de templates Jinja2
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


def generate_invoice_files(invoice_id: int):
    """
    Genera archivos PDF y XML para una factura.
    
    Args:
        invoice_id: ID de la factura
        
    Returns:
        Tupla (xml_path, pdf_path)
    """
    db = SessionLocal()
    try:
        inv = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not inv:
            raise ValueError('Invoice not found')
        
        # Seleccionar plantilla según país del cliente
        if inv.client.country == 'ES':
            template_name = 'facturae_template.xml'
        else:
            template_name = 'facturx-template.xml'
        
        template = env.get_template(template_name)
        xml_content = template.render(invoice=inv)
        
        # Crear directorio de salida
        out_dir = os.path.join(os.getcwd(), 'out')
        os.makedirs(out_dir, exist_ok=True)
        
        # Guardar XML
        xml_path = os.path.join(out_dir, f'invoice_{inv.id}.xml')
        with open(xml_path, 'wb') as f:
            f.write(xml_content.encode('utf-8'))
        
        # Generar PDF (placeholder - implementar con reportlab o QtWebEngine)
        pdf_path = os.path.join(out_dir, f'invoice_{inv.id}.pdf')
        with open(pdf_path, 'wb') as f:
            f.write(b'%PDF-1.4\n% PDF placeholder for invoice')
        
        # Actualizar rutas en la base de datos
        inv.xml_path = xml_path
        inv.pdf_path = pdf_path
        db.commit()
        
        return xml_path, pdf_path
    
    finally:
        db.close()

