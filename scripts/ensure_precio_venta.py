#!/usr/bin/env python3
"""
Script seguro para propagar la columna `precio_venta` en la tabla `articulos`
a todas las bases de datos configuradas en `core/db.DATABASE_CONFIGS`.

Es idempotente: primero comprueba si la columna existe y sólo la añade si falta.
Incluye modo dry-run por defecto. Usa `--apply` para ejecutar los ALTER TABLE.

Usage:
  python scripts/ensure_precio_venta.py            # dry-run (no cambios)
  python scripts/ensure_precio_venta.py --apply    # realiza los cambios

"""
from __future__ import annotations
import argparse
import sys
from sqlalchemy import inspect, text

from core.db import list_available_databases, set_current_database, get_engine, get_database_url, get_session


def detect_column(engine, table_name: str, column_name: str) -> bool:
    inspector = inspect(engine)
    if not inspector.has_table(table_name):
        return False
    existing_cols = {c['name'] for c in inspector.get_columns(table_name)}
    return column_name in existing_cols


def add_column(engine, dialect: str, table_name: str, column_name: str) -> None:
    if dialect == 'sqlite':
        sql = f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" REAL'
    elif dialect == 'mysql':
        # Use DOUBLE for better precision on MySQL/MariaDB
        sql = f'ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` DOUBLE DEFAULT 0.0 NOT NULL'
    else:
        # Fallback to generic FLOAT
        sql = f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" FLOAT DEFAULT 0.0 NOT NULL'

    with engine.connect() as conn:
        conn.execute(text(sql))


def main():
    parser = argparse.ArgumentParser(description='Propaga columna precio_venta a las DBs configuradas')
    parser.add_argument('--apply', action='store_true', help='Aplicar los cambios (por defecto dry-run)')
    parser.add_argument('--dbs', help='Lista separada por comas de DBs a afectar (ej: artstudio3d,company_1)')
    parser.add_argument('--all-companies', action='store_true', help='Detectar y añadir empresas (company_*) desde la BD principal')
    args = parser.parse_args()

    targets = list_available_databases()
    if args.dbs:
        requested = [d.strip() for d in args.dbs.split(',') if d.strip()]
        targets = [d for d in targets if d in requested]

    if args.all_companies:
        # Query main DB for companies and add their DB keys dynamically
        try:
            set_current_database('main')
            session = get_session()
            rows = session.execute(text('SELECT id FROM empresas')).fetchall()
            company_ids = [r[0] for r in rows]
            for cid in company_ids:
                db_key = f'company_{cid}'
                # set_database_for_company will add DATABASE_CONFIGS entry
                try:
                    # Importing here to avoid top-level circular imports
                    from core.db import set_database_for_company
                    set_database_for_company(cid)
                except Exception:
                    # ignore; we only want to populate DATABASE_CONFIGS
                    pass

            # refresh targets after adding companies
            targets = list_available_databases()
        except Exception as e:
            print(f'Error fetching companies from main DB: {e}')

    if not targets:
        print('No hay bases de datos configuradas para procesar.')
        sys.exit(0)

    summary = []

    for db_key in targets:
        try:
            set_current_database(db_key)
            engine = get_engine()
            db_url = get_database_url(db_key)
            dialect = 'sqlite' if 'sqlite' in db_url else ('mysql' if 'mysql' in db_url or 'mariadb' in db_url else 'other')

            print(f'-- Processing {db_key} ({db_url}) -> dialect={dialect}')

            table = 'articulos'
            col = 'precio_venta'

            exists = detect_column(engine, table, col)
            if exists:
                print(f'   ✓ Columna ya existe: {table}.{col}')
                summary.append((db_key, True, 'exists'))
                continue

            print(f'   ⚠️ Columna faltante: {table}.{col}')

            if not args.apply:
                print('     (dry-run) no se aplicarán cambios. Usa --apply para añadir la columna.')
                summary.append((db_key, False, 'dry-run'))
                continue

            # Try to add column
            try:
                add_column(engine, dialect, table, col)
                print(f'   ✅ Columna {col} añadida en {db_key}')
                summary.append((db_key, True, 'added'))
            except Exception as e:
                print(f'   ❌ Error al añadir columna en {db_key}: {e}')
                summary.append((db_key, False, f'error: {e}'))

        except Exception as e:
            print(f'Failed processing {db_key}: {e}')
            summary.append((db_key, False, f'error: {e}'))

    print('\nResumen:')
    for row in summary:
        print(f' - {row[0]} -> ok={row[1]}  note={row[2]}')


if __name__ == '__main__':
    main()
