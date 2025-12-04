#!/usr/bin/env python
"""
Script para migrar las tablas de artículos a la base de datos
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.db import init_db, set_database_for_company, get_current_database
import logging

def migrate_articulos():
    """Migrate articulos tables to database"""
    logging.getLogger(__name__).info("=" * 60)
    logging.getLogger(__name__).info("MIGRACIÓN DE TABLAS DE ARTÍCULOS")
    logging.getLogger(__name__).info("=" * 60)
    
    # Get company ID from command line or use default
    company_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    logging.getLogger(__name__).info(f"\nConfiguring database for company {company_id}...")
    set_database_for_company(company_id)
    
    logging.getLogger(__name__).info(f"\nCreating tables in: {get_current_database()}")
    logging.getLogger(__name__).info("-" * 60)
    
    # Run migration
    init_db()
    
    logging.getLogger(__name__).info("-" * 60)
    logging.getLogger(__name__).info("\n✅ Migración completada")
    logging.getLogger(__name__).info("=" * 60)

if __name__ == "__main__":
    migrate_articulos()
