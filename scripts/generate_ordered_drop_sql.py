#!/usr/bin/env python3
"""Generate an ordered DROP TABLE script for `main` by walking FK dependencies.

Dry-run by default. To execute, pass --apply --confirm DELETE_MAIN (exact token).

Usage examples:
  # Dry-run, show SQL
  PYTHONPATH=$PWD .venv/bin/python scripts/generate_ordered_drop_sql.py --tables articulos,clientes

  # Write SQL into file
  PYTHONPATH=$PWD .venv/bin/python scripts/generate_ordered_drop_sql.py --tables articulos,clientes --out-file /tmp/drop.sql

  # Execute (dangerous)
  PYTHONPATH=$PWD .venv/bin/python scripts/generate_ordered_drop_sql.py --tables articulos,clientes --apply --confirm DELETE_MAIN

"""
from __future__ import annotations

import argparse
from typing import Dict, List, Set

from sqlalchemy import text

from core.db import get_engine, set_current_database


def find_children(engine, table: str) -> Set[str]:
    """Return set of tables that have FK referencing 'table' in the current DB."""
    sql = text(
        """
        SELECT TABLE_NAME
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE REFERENCED_TABLE_NAME = :table
          AND TABLE_SCHEMA = (SELECT DATABASE())
        """
    )
    children = set()
    with engine.connect() as conn:
        rows = conn.execute(sql, {"table": table}).fetchall()
        for r in rows:
            children.add(r[0])

    return children


def build_dependency_graph(engine, roots: List[str]) -> Dict[str, Set[str]]:
    """Build graph mapping node -> set(child_nodes)."""
    graph: Dict[str, Set[str]] = {}

    stack = list(roots)
    seen = set()

    while stack:
        t = stack.pop()
        if t in seen:
            continue
        seen.add(t)
        children = find_children(engine, t)
        graph[t] = children
        # ensure children are also examined (we might need to drop grandchildren first)
        for c in children:
            if c not in seen:
                stack.append(c)

    # Also ensure children nodes exist in graph even if they have no children
    for parent, children in list(graph.items()):
        for c in children:
            graph.setdefault(c, set())

    return graph


def dfs_postorder(graph: Dict[str, Set[str]]) -> List[str]:
    visited = set()
    order: List[str] = []

    def visit(node):
        if node in visited:
            return
        visited.add(node)
        for child in graph.get(node, []):
            visit(child)
        order.append(node)

    for n in list(graph.keys()):
        visit(n)

    # order now is children-first due to postorder
    # de-duplicate while preserving order
    seen = set()
    final = []
    for x in order:
        if x not in seen:
            final.append(x)
            seen.add(x)

    return final


def generate_drop_sql(order: List[str]) -> str:
    stmts = [f"DROP TABLE IF EXISTS `{t}`;" for t in order]
    return "\n".join(stmts)


def main():
    parser = argparse.ArgumentParser(
        description="Generate ordered DROP SQL for main DB by FK dependencies"
    )
    parser.add_argument(
        "--tables",
        help="Comma separated list of root tables to remove (default: articulos, clientes, familias, subfamilias, tarifas)",
    )
    parser.add_argument("--out-file", help="Write SQL to a file")
    parser.add_argument(
        "--apply", action="store_true", help="Execute the generated SQL (destructive)"
    )
    parser.add_argument(
        "--confirm",
        help="Confirmation token required to run destructive drops. Type 'DELETE_MAIN' to confirm",
    )

    args = parser.parse_args()

    roots = ["articulos", "clientes", "familias", "subfamilias", "tarifas"]
    if args.tables:
        roots = [t.strip() for t in args.tables.split(",") if t.strip()]

    set_current_database("main")
    engine = get_engine()

    print("Building dependency graph from roots:", roots)
    graph = build_dependency_graph(engine, roots)

    print("Dependency graph (parent -> children):")
    for parent, children in sorted(graph.items()):
        print(f" - {parent}: {sorted(children)}")

    order = dfs_postorder(graph)
    print("\nComputed drop order (child -> parent):")
    for i, t in enumerate(order, 1):
        print(f"{i:02d}. {t}")

    sql = generate_drop_sql(order)
    print("\nGenerated DROP SQL (dry-run):")
    print(sql)

    if args.out_file:
        with open(args.out_file, "w", encoding="utf-8") as fh:
            fh.write(sql)
        print("\nWrote SQL to", args.out_file)

    if not args.apply:
        print(
            "\nDry-run only. Use --apply and --confirm DELETE_MAIN to actually execute."
        )
        return

    if args.confirm != "DELETE_MAIN":
        print(
            "\nMissing or incorrect confirmation token. To execute drops you must pass --confirm DELETE_MAIN"
        )
        return

    print("\nExecuting DROP statements on main (this is destructive).")
    try:
        with engine.begin() as conn:
            for stmt in sql.splitlines():
                if not stmt.strip():
                    continue
                print("Executing:", stmt)
                conn.execute(text(stmt))
        print("\nAll statements executed.")
    except Exception as e:
        print("Error executing drops:", e)


if __name__ == "__main__":
    main()
