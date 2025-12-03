#!/usr/bin/env python3
"""Read-only diagnostic tool: compare configured databases (tables + row counts + samples).

Usage:
    .venv/bin/python scripts/db_diff_report.py --databases main artstudio3d --sample 3

This script uses the project's core.db helpers so it runs using the project's DB URLs.
"""
import argparse
import csv
import os
from core.db import DATABASE_CONFIGS, set_current_database, get_engine
from sqlalchemy import inspect, text


def get_tables_and_counts(db_key):
    set_current_database(db_key)
    engine = get_engine()
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    table_info = {}
    with engine.connect() as conn:
        for t in tables:
            try:
                # Use COUNT(*) for an accurate, read-only row count
                res = conn.execute(text(f"SELECT COUNT(*) as c FROM `{t}`"))
                count = int(next(res)['c']) if res.returns_rows else 0
            except Exception:
                # Some meta tables may not be readable in some drivers; fallback to -1
                try:
                    res = conn.execute(text(f"SELECT COUNT(*) as c FROM \"{t}\""))
                    count = int(next(res)['c']) if res.returns_rows else 0
                except Exception:
                    count = -1

            table_info[t] = {'rows': count}

    return table_info


def sample_rows(db_key, table_name, sample_limit=3):
    set_current_database(db_key)
    engine = get_engine()
    with engine.connect() as conn:
        try:
            # Try a simple select limited result (works on MySQL/Postgres)
            res = conn.execute(text(f"SELECT * FROM `{table_name}` LIMIT {sample_limit}"))
            rows = [dict(r) for r in res.fetchall()]
        except Exception:
            # Try alternative quoting
            try:
                res = conn.execute(text(f"SELECT * FROM \"{table_name}\" LIMIT {sample_limit}"))
                rows = [dict(r) for r in res.fetchall()]
            except Exception:
                rows = []

    return rows


def main():
    parser = argparse.ArgumentParser(description="Compare configured DBs and produce table/row counts + sample rows")
    parser.add_argument('--databases', nargs='+', default=list(DATABASE_CONFIGS.keys()), help='Database keys to inspect (default: all configured)')
    parser.add_argument('--sample', type=int, default=0, help='Number of sample rows per suspicious table')
    parser.add_argument('--output-csv', help='Optional directory to dump CSV samples for inspected tables')

    args = parser.parse_args()

    keys = [k for k in args.databases if k in DATABASE_CONFIGS]

    if not keys:
        print('No valid databases selected. Available keys:', list(DATABASE_CONFIGS.keys()))
        return

    print('Configured DBs to compare:', keys)

    # Map db_key -> {table: {rows}}
    db_tables = {}

    for k in keys:
        print('\n---', k, '---')
        try:
            info = get_tables_and_counts(k)
            db_tables[k] = info
            print(f"Total tables: {len(info)}")
            for t, meta in sorted(info.items()):
                print(f"{t}: rows={meta['rows']}")
        except Exception as e:
            print('Error inspecting', k, e)

    # Compare table sets
    if len(keys) >= 2:
        all_tables_sets = {k: set(db_tables.get(k, {}).keys()) for k in keys}

        base = keys[0]
        for other in keys[1:]:
            only_in_base = sorted(list(all_tables_sets[base] - all_tables_sets[other]))
            only_in_other = sorted(list(all_tables_sets[other] - all_tables_sets[base]))

            print(f"\nComparison: {base} vs {other}")
            print('  Only in', base, ':', only_in_base or '(none)')
            print('  Only in', other, ':', only_in_other or '(none)')

            # Check common tables where row counts differ
            common = sorted(list(all_tables_sets[base].intersection(all_tables_sets[other])))
            diffs = []
            for t in common:
                a = db_tables[base].get(t, {}).get('rows', -1)
                b = db_tables[other].get(t, {}).get('rows', -1)
                if a != b:
                    diffs.append((t, a, b))

            if diffs:
                print('\n  Tables with differing row counts:')
                for t, a, b in diffs:
                    print(f"    {t}: {base}={a} vs {other}={b}")
            else:
                print('\n  No differing row counts detected for common tables.')

    # Produce sample rows for suspicious tables (e.g., tables present in 'main' but that look module-specific)
    if args.sample and 'main' in db_tables:
        suspicious = [t for t in db_tables['main'].keys() if t.lower() in ('articulos', 'clientes', 'facturas', 'albaranes', 'familias', 'subfamilias')]
        if suspicious:
            print('\n--- Sample rows for suspicious tables in main ---')
            for t in suspicious:
                print(f'\nTable: {t}')
                rows = sample_rows('main', t, sample_limit=args.sample)
                if rows:
                    for r in rows:
                        print(' ', {k: v for k, v in r.items() if k in list(r.keys())[:6]})
                else:
                    print('  (no sample or cannot read rows)')

                if args.output_csv:
                    os.makedirs(args.output_csv, exist_ok=True)
                    csvpath = os.path.join(args.output_csv, f"{t}.sample.csv")
                    try:
                        with open(csvpath, 'w', newline='', encoding='utf-8') as fh:
                            if rows:
                                writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
                                writer.writeheader()
                                writer.writerows(rows)
                            else:
                                fh.write('')
                        print('  Wrote sample to', csvpath)
                    except Exception as e:
                        print('  Error writing CSV:', e)


if __name__ == '__main__':
    main()
