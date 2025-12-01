#!/usr/bin/env python
"""
Script para migrar las tablas de artículos a la base de datos
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.db import init_db, set_database_for_company, get_current_database

def migrate_articulos():
    """Migrate articulos tables to database"""
    print("=" * 60)
    print("MIGRACIÓN DE TABLAS DE ARTÍCULOS")
    print("=" * 60)
    
    # Get company ID from command line or use default
    company_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    print(f"\nConfiguring database for company {company_id}...")
    set_database_for_company(company_id)
    
    print(f"\nCreating tables in: {get_current_database()}")
    print("-" * 60)
    
    # Run migration
    init_db()
    
    print("-" * 60)
    print("\n✅ Migración completada")
    print("=" * 60)

if __name__ == "__main__":
    migrate_articulos()
