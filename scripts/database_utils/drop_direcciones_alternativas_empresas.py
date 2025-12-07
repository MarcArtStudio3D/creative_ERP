#!/usr/bin/env python3
"""
Script para eliminar la tabla direcciones_alternativas_empresas de las bases de datos.
Esta tabla ya no se usa en la aplicación.
"""

import sys
import os
from pathlib import Path

# Añadir el directorio raíz al path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core.db import get_session, get_engine_for_database, get_engine_from_url
import logging
from sqlalchemy import text, inspect


def drop_table_if_exists(engine, table_name: str):
    """Elimina una tabla si existe."""
    inspector = inspect(engine)
    
    if table_name in inspector.get_table_names():
        logging.getLogger(__name__).info(f"  ✓ Tabla '{table_name}' encontrada, eliminando...")
        with engine.connect() as conn:
            conn.execute(text(f"DROP TABLE {table_name}"))
            conn.commit()
        logging.getLogger(__name__).info(f"  ✅ Tabla '{table_name}' eliminada correctamente")
    else:
        logging.getLogger(__name__).info(f"  ℹ️  Tabla '{table_name}' no existe, nada que hacer")


def main():
    """Elimina la tabla direcciones_alternativas_empresas de todas las bases de datos."""
    
    logging.getLogger(__name__).info("=" * 60)
    logging.getLogger(__name__).info("Eliminando tabla 'direcciones_alternativas_empresas'")
    logging.getLogger(__name__).info("=" * 60)
    
    # 1. Base de datos principal (main)
    logging.getLogger(__name__).info("\n1️⃣  Base de datos MAIN:")
    try:
        main_engine = get_engine_for_database('main')
        drop_table_if_exists(main_engine, 'direcciones_alternativas_empresas')
    except Exception as e:
        print(f"  ❌ Error en base de datos main: {e}")
    
    # 2. Obtener todas las empresas para limpiar sus bases de datos
    logging.getLogger(__name__).info("\n2️⃣  Bases de datos de EMPRESAS:")
    try:
        from core.models import Empresa
        from sqlmodel import select
        session = get_session()
        empresas = session.exec(select(Empresa)).all()

        if not empresas:
            logging.getLogger(__name__).info("  ℹ️  No hay empresas registradas")
        else:
            for empresa in empresas:
                logging.getLogger(__name__).info(f"\n  Empresa: {empresa.nombre_fiscal} (ID: {empresa.id})")
                try:
                    # Obtener URL de la base de datos de la empresa
                    from core.config import get_database_url_for_company
                    db_url = get_database_url_for_company(empresa.id)
                    
                    # Crear engine para esta empresa (centralizado por URL)
                    empresa_engine = get_engine_from_url(db_url)

                    drop_table_if_exists(empresa_engine, 'direcciones_alternativas_empresas')
                    try:
                        empresa_engine.dispose()
                    except Exception:
                        pass

                except Exception as e:
                    logging.getLogger(__name__).exception(f"    ❌ Error procesando empresa {empresa.id}")
        
        session.close()
        
    except Exception:
        logging.getLogger(__name__).exception("  ❌ Error obteniendo empresas")
    
    logging.getLogger(__name__).info("\n" + "=" * 60)
    logging.getLogger(__name__).info("✅ Proceso completado")
    logging.getLogger(__name__).info("=" * 60)


if __name__ == "__main__":
    main()
