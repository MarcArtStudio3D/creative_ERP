#!/usr/bin/env python3
"""
Script para inspeccionar la estructura de las tablas de divisiones en MariaDB
"""

import sys
import os
from sqlalchemy import create_engine, inspect
import logging

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config import get_database_url_for_company

def inspeccionar_tablas():
    logging.getLogger(__name__).info("=" * 60)
    logging.getLogger(__name__).info("INSPECCIÓN DE TABLAS DE DIVISIONES (MariaDB)")
    logging.getLogger(__name__).info("=" * 60)
    
    # Usar la base de datos de la empresa 1 (Artstudio3d) que usa MariaDB
    try:
        db_url = get_database_url_for_company(1)
        logging.getLogger(__name__).info(f"Conectando a: {db_url}")
        
        engine = create_engine(db_url)
        inspector = inspect(engine)
        
        tablas = ['secciones', 'familias', 'subfamilias']
        
        for tabla in tablas:
            logging.getLogger(__name__).info(f"\nTable: {tabla}")
            if not inspector.has_table(tabla):
                logging.getLogger(__name__).warning("   ❌ La tabla no existe")
                continue
                
            columns = inspector.get_columns(tabla)
            for col in columns:
                logging.getLogger(__name__).info(f"   - {col['name']} ({col['type']})")
                
    except Exception:
        logging.getLogger(__name__).exception("❌ ERROR inspeccionar_tablas")

if __name__ == "__main__":
    inspeccionar_tablas()
