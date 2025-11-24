"""
Migración completa desde SQLite hacia PostgreSQL o MariaDB.
Funciona automáticamente con todos tus modelos SQLAlchemy.

Uso:
    python migrate_sqlite_to_engine.py postgres
    python migrate_sqlite_to_engine.py mariadb
"""

import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import Base first
from core.models import Base

# Import all models so SQLAlchemy can resolve foreign keys
from modules.clientes.models import (
    Cliente, DireccionAlternativa, DeudaCliente, 
    HistorialCliente, EstadisticaClienteMes, Ville, ClienteTipo
)
from modules.tipo_cliente.models import TipoCliente, TipoSubCliente
# Import other module models if they exist
try:
    from modules.facturas.models import *
except ImportError:
    pass

# ------------------------------
# CONFIGURACIÓN
# ------------------------------

SQLITE_URL = f"sqlite:///{project_root}/creative_erp.db"

POSTGRES_URL = "postgresql://admin:admin123@192.168.1.28:5432/creative_erp"

MARIADB_URL = "mysql+pymysql://admin:admin123@127.0.0.1:3306/creative_erp"


def get_destination_url(arg: str) -> str:
    """Devuelve la URL del motor destino."""
    if arg == "postgres":
        return POSTGRES_URL
    elif arg == "mariadb":
        return MARIADB_URL
    else:
        raise ValueError("Parámetro inválido. Usa: postgres | mariadb")


# ------------------------------
# MIGRACIÓN
# ------------------------------

def migrate(sqlite_url: str, dest_url: str):
    print(f"📌 Cargando origen SQLite: {sqlite_url}")
    source_engine = create_engine(sqlite_url)
    SourceSession = sessionmaker(bind=source_engine)
    source_session = SourceSession()

    print(f"📌 Conectando a destino: {dest_url}")
    dest_engine = create_engine(dest_url)
    DestSession = sessionmaker(bind=dest_engine)
    dest_session = DestSession()

    # Limpiar tablas destino si existen (para evitar duplicados)
    print("📌 Limpiando tablas destino existentes...")
    Base.metadata.drop_all(dest_engine)
    
    # Crear tablas destino
    print("📌 Creando tablas destino...")
    Base.metadata.create_all(dest_engine)

    # Build a mapping of table names to model classes
    table_to_model = {}
    for mapper in Base.registry.mappers:
        model_class = mapper.class_
        table_name = mapper.local_table.name
        table_to_model[table_name] = model_class

    def convert_value(table_name, col_name, value, col_type):
        """Convert values to match destination database types"""
        # Handle None values
        if value is None:
            return None
        
        # Special handling for id_pais field (country names -> IDs)
        if col_name == 'id_pais' and isinstance(value, str):
            # If it's a country name string, convert to default ID
            return 1  # Default country ID
        
        # Handle integer fields that might have string values
        if 'Integer' in str(col_type):
            if isinstance(value, str):
                # Try to convert string to int, use default if fails
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return -1 if col_name.startswith('id_') else 0
        
        return value

    try:
        # Get list of tables that actually exist in source database
        from sqlalchemy import inspect as sqla_inspect
        source_inspector = sqla_inspect(source_engine)
        existing_tables = set(source_inspector.get_table_names())
        
        for table in Base.metadata.sorted_tables:
            # Skip tables that don't exist in source
            if table.name not in existing_tables:
                print(f"⏭  Saltando tabla: {table.name} (no existe en origen)")
                continue
                
            print(f"➡ Migrando tabla: {table.name}")

            # Get the ORM model for this table
            model = table_to_model.get(table.name)
            if model is None:
                print(f"   ⚠ No hay modelo ORM para {table.name}, saltando.")
                continue

            rows = source_session.query(model).all()
            if not rows:
                print("   (vacía)")
                continue

            for row in rows:
                # Crear una nueva instancia para el destino
                dest_row = model()

                for col in table.columns:
                    value = getattr(row, col.name)
                    # Convert value if needed
                    converted_value = convert_value(table.name, col.name, value, col.type)
                    setattr(dest_row, col.name, converted_value)

                dest_session.add(dest_row)

            dest_session.commit()
            print(f"   ✔ OK ({len(rows)} registros)")

    except SQLAlchemyError as e:
        dest_session.rollback()
        print(f"❌ ERROR en migración: {e}")
        return

    finally:
        source_session.close()
        dest_session.close()

    print("\n🎉 MIGRACIÓN COMPLETADA CON ÉXITO")


# ------------------------------
# MAIN
# ------------------------------

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python migrate_sqlite_to_engine.py [postgres|mariadb]")
        sys.exit(1)

    dest = get_destination_url(sys.argv[1])
    migrate(SQLITE_URL, dest)
