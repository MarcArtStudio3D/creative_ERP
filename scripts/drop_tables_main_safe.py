#!/usr/bin/env python3
"""Script seguro para ayudar a borrar tablas de la base de datos `main`.

Este script no toca la BD por defecto (dry-run). Requiere dos pasos explícitos
para hacer la operación destructiva:

- Paso 1: ejecutar con --apply    -> muestra las sentencias SQL que se ejecutarían
- Paso 2: añadir --confirm DELETE_MAIN (texto exacto) para ejecutar realmente

Uso ejemplo (dry-run):
  PYTHONPATH=$PWD .venv/bin/python scripts/drop_tables_main_safe.py --tables articulos,clientes

Ejecutar (riesgoso — asegúrate de tener backups):
  PYTHONPATH=$PWD .venv/bin/python scripts/drop_tables_main_safe.py --tables articulos,clientes --apply --confirm DELETE_MAIN

El script imprime todo y puede escribir un SQL en --out-file para ejecución manual.
"""
from __future__ import annotations

import argparse
import sys

from sqlalchemy import text

from core.db import get_database_url, get_engine, set_current_database

DEFAULT_TABLES = [
    "articulos",
    "articulos_imagenes",
    "articulos_ofertas",
    "clientes",
    "familias",
    "subfamilias",
    "tarifas",
    "kits",
    "proveedores_frecuentes",
    "direcciones_alternativas",
    "deudas_clientes",
    "estadisticas_clientes_mes",
    "historial_clientes",
]


def generate_drop_sql(tables):
    stmts = [f"DROP TABLE IF EXISTS `{t}`;" for t in tables]
    return "\n".join(stmts)


def main():
    parser = argparse.ArgumentParser(
        description="Safe drop tables in main DB (dry-run by default)"
    )
    parser.add_argument(
        "--tables",
        help="Comma-separated list of tables to drop (default: common module tables)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Show SQL and (with --confirm) execute drops",
    )
    parser.add_argument(
        "--confirm",
        help="Confirmation token required to run destructive drops. Type 'DELETE_MAIN' to confirm",
    )
    parser.add_argument(
        "--out-file",
        help="Optional path to write the generated SQL for manual execution",
    )

    args = parser.parse_args()

    if args.tables:
        tables = [t.strip() for t in args.tables.split(",") if t.strip()]
    else:
        tables = DEFAULT_TABLES

    sql = generate_drop_sql(tables)

    print("Target DB: main (this script will operate on the `main` DB)")
    print("-- Tables selected:")
    for t in tables:
        print("  -", t)
    print("\n-- Generated SQL (dry-run) --")
    print(sql)

    if args.out_file:
        with open(args.out_file, "w", encoding="utf-8") as fh:
            fh.write(sql)
        print(f"Wrote SQL to: {args.out_file}")

    if not args.apply:
        print(
            "\nDry-run only. Use --apply and --confirm DELETE_MAIN to actually execute."
        )
        sys.exit(0)

    # Must supply confirmation token
    if args.confirm != "DELETE_MAIN":
        print(
            "\nMissing or incorrect confirmation token. To execute drops you must pass --confirm DELETE_MAIN"
        )
        sys.exit(2)

    # Safety: ensure we're pointing to main
    set_current_database("main")
    db_url = get_database_url("main")
    print(f"\nExecuting against: main -> {db_url}")

    engine = get_engine()

    try:
        with engine.begin() as conn:
            for t in tables:
                print(f"Executing: DROP TABLE IF EXISTS {t}")
                conn.execute(text(f"DROP TABLE IF EXISTS `{t}`"))
        print("\nDone. Tables dropped.")
    except Exception as e:
        print("Error executing drops:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
