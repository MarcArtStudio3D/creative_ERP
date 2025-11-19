"""
Migración completa desde SQLite hacia PostgreSQL o MariaDB.
Funciona automáticamente con todos tus modelos SQLAlchemy.

Uso:
    python migrate_sqlite_to_engine.py postgres
    python migrate_sqlite_to_engine.py mariadb
"""

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from core.models import Base  # Tus modelos

# ------------------------------
# CONFIGURACIÓN
# ------------------------------

SQLITE_URL = "sqlite:///./dev.db"

POSTGRES_URL = "postgresql://admin:admin123@192.168.1.27:5432/testdb"

MARIADB_URL = "mysql+pymysql://admin:admin123@192.168.1.27:3306/testdb"


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

    # Crear tablas destino si no existen
    print("📌 Creando tablas destino si no existen…")
    Base.metadata.create_all(dest_engine)

    try:
        for table in Base.metadata.sorted_tables:
            print(f"➡ Migrando tabla: {table.name}")

            # ORM models asociados
            model = Base._decl_class_registry.get(table.name)
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
                    setattr(dest_row, col.name, value)

                dest_session.add(dest_row)

            dest_session.commit()
            print("   ✔ OK")

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
