#!/usr/bin/env python3
"""
Script para crear las tablas de clientes en todas las bases de datos de empresas.
"""

import sys
import os
from pathlib import Path

# Añadir el directorio raíz al path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core.db import get_session, Base
from core.models import Empresa
from core.config import get_database_url_for_company
from sqlalchemy import create_engine

# Importar todos los modelos para que SQLAlchemy los conozca
from modules.clientes.models import (
    Cliente, DireccionAlternativa, DeudaCliente, 
    HistorialCliente, EstadisticaClienteMes, ClienteTipo
)
from modules.tipo_cliente.models import TipoCliente, TipoSubCliente


def create_tables_for_company(empresa: Empresa):
    """Crea las tablas de clientes en la base de datos de una empresa."""
    print(f"\nCompany: {empresa.nombre_fiscal} (ID: {empresa.id})")
    print(f"   Motor: {empresa.motor_base_datos}")
    
    try:
        # Obtener URL de la base de datos
        db_url = get_database_url_for_company(empresa.id)
        print(f"   URL: {db_url.split('@')[1] if '@' in db_url else db_url}")  # Ocultar password
        
        # Crear engine
        engine = create_engine(db_url)
        
        # Crear todas las tablas
        Base.metadata.create_all(engine)
        
        print("   ✅ Tablas creadas correctamente")
        
        engine.dispose()
        
    except Exception as e:
        print(f"   ❌ Error: {e}")


def main():
    """Crea las tablas de clientes en todas las bases de datos de empresas."""
    
    print("=" * 80)
    print("Creando tablas de clientes en bases de datos de empresas")
    print("=" * 80)
    
    try:
        # Obtener todas las empresas
        session = get_session()
        empresas = session.query(Empresa).all()
        
        if not empresas:
            print("\n⚠️  No hay empresas registradas")
            return
        
        print(f"\nEncontradas {len(empresas)} empresa(s)")
        
        for empresa in empresas:
            create_tables_for_company(empresa)
        
        session.close()
        
        print("\n" + "=" * 80)
        print("✅ Proceso completado")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error general: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
