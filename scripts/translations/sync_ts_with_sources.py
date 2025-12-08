#!/usr/bin/env python3
"""
Scan Python sources to collect translatable strings and merge any missing
messages into existing Qt .ts translation files under translations/.

Behavior:
- Extract strings from calls to: self.tr(), tr(), QCoreApplication.translate(...),
  show_info/show_warning/show_critical/show_question calls, QLabel/QPushButton literal args
- Group messages by context (class name if found, otherwise module filepath)
- For each translations/creative_erp_*.ts file, add missing <message><source>...</source>
  entries preserving existing <translation> elements (leave unfinished for new messages).

This script is intended as a convenience assistant for keeping .ts files in sync
with the source. It is *not* a replacement for pyside6-lupdate but helps fill
missing entries programmatically when desired.

Usage:
  python scripts/translations/sync_ts_with_sources.py [--dry-run]

"""

import ast
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Set, Tuple


def collect_strings_from_file(path: Path) -> Dict[str, Set[str]]:
    """Return mapping context -> set(source strings) extracted from a python file.

    Context heuristics:
    - If string is extracted via self.tr(...) or tr(...), context = enclosing class name if any, otherwise module name
    - If via QCoreApplication.translate(ctx, src) then context=ctx arg value
    - For show_* calls and QLabel/QPushButton constructors with literal strings, use enclosing class or module
    """

    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(path))

    contexts: Dict[str, Set[str]] = {}

    # Walk AST and capture calls
    class ContextVisitor(ast.NodeVisitor):
        def __init__(self):
            self.class_stack = []

        def _add(self, ctx: str, text: str):
            if not text:
                return
            contexts.setdefault(ctx, set()).add(text)

        def visit_ClassDef(self, node: ast.ClassDef):
            self.class_stack.append(node.name)
            self.generic_visit(node)
            self.class_stack.pop()

        def visit_Call(self, node: ast.Call):
            # Helper to get literal string value
            def literal_str(n):
                if isinstance(n, ast.Constant) and isinstance(n.value, str):
                    return n.value
                return None

            # Function names
            func = node.func
            func_name = None
            if isinstance(func, ast.Attribute):
                func_name = func.attr
            elif isinstance(func, ast.Name):
                func_name = func.id

            ctx_name = self.class_stack[-1] if self.class_stack else path.stem

            # self.tr(...) or tr(...)
            if func_name == "tr":
                # first argument string
                if node.args:
                    s = literal_str(node.args[0])
                    if s is not None:
                        self._add(ctx_name, s)

            # QCoreApplication.translate(context, source)
            if (
                isinstance(func, ast.Attribute)
                and getattr(func.value, "id", "") == "QCoreApplication"
                and func.attr == "translate"
            ):
                if len(node.args) >= 2:
                    ctx = literal_str(node.args[0]) or ctx_name
                    src_txt = literal_str(node.args[1])
                    if src_txt:
                        self._add(ctx, src_txt)

            # show_info/show_warning/show_critical/show_question - often (self, title, message)
            if func_name in ("show_info", "show_warning", "show_critical"):
                # expect title and message (title first arg after self)
                # find the first two string literals in args
                strs = [
                    literal_str(a)
                    for a in node.args
                    if isinstance(a, ast.Constant) and isinstance(a.value, str)
                ]
                if strs:
                    # add title and body under context
                    for s in strs[:2]:
                        self._add(ctx_name, s)

            if func_name == "show_question":
                strs = [
                    literal_str(a)
                    for a in node.args
                    if isinstance(a, ast.Constant) and isinstance(a.value, str)
                ]
                for s in strs[:2]:
                    if s:
                        self._add(ctx_name, s)

            # QLabel("literal"), QPushButton("literal") constructors: attempt to capture
            # If func is Name like QLabel or QPushButton (in code), capture first literal arg
            if isinstance(func, ast.Name) and func.id in ("QLabel", "QPushButton"):
                if node.args:
                    s = literal_str(node.args[0])
                    if s:
                        self._add(ctx_name, s)

            # Recurse
            self.generic_visit(node)

    v = ContextVisitor()
    v.visit(tree)
    return contexts


def collect_all_sources(root: Path) -> Dict[str, Set[str]]:
    aggregated: Dict[str, Set[str]] = {}
    for p in root.rglob("*.py"):
        # Skip translations tools and tests that aren't part of UI if desired
        if "translations" in p.parts or p.match("*/.venv/*"):
            continue
        try:
            file_contexts = collect_strings_from_file(p)
            for ctx, sset in file_contexts.items():
                aggregated.setdefault(ctx, set()).update(sset)
        except Exception:
            # best-effort extraction; skip files that fail parsing
            continue
    return aggregated


def merge_into_ts(
    ts_path: Path, source_map: Dict[str, Set[str]], dry_run: bool = False
) -> Tuple[int, int]:
    """Merge missing messages from source_map into ts_path.

    Returns (added_count, total_missing_checked)
    """
    tree = ET.parse(ts_path)
    root = tree.getroot()

    # Build existing messages mapping: context -> set(source)
    existing: Dict[str, Set[str]] = {}
    for ctx in root.findall("context"):
        name_elem = ctx.find("name")
        if name_elem is None:
            continue
        name = name_elem.text or ""
        existing.setdefault(name, set())
        for msg in ctx.findall("message"):
            s = msg.find("source")
            if s is not None and s.text is not None:
                existing[name].add(s.text)

    added = 0
    checked = 0

    for ctx, srcs in source_map.items():
        checked += len(srcs)
        ctx_node = None
        for c in root.findall("context"):
            name_elem = c.find("name")
            if name_elem is not None and name_elem.text == ctx:
                ctx_node = c
                break

        if ctx_node is None:
            if dry_run:
                # report
                added += len(srcs)
                continue
            ctx_node = ET.SubElement(root, "context")
            n = ET.SubElement(ctx_node, "name")
            n.text = ctx
            existing.setdefault(ctx, set())

        for src in sorted(srcs):
            if src in existing.get(ctx, set()):
                continue
            # Add message
            if dry_run:
                added += 1
                continue

            msg = ET.SubElement(ctx_node, "message")
            source_elem = ET.SubElement(msg, "source")
            source_elem.text = src
            trans = ET.SubElement(msg, "translation")
            trans.set("type", "unfinished")
            added += 1

    if not dry_run and added:
        tree.write(ts_path, encoding="utf-8", xml_declaration=True)

    return added, checked


def run_lupdate(ts_files: list[Path]) -> bool:
    """Try to run pyside6-lupdate or lupdate to update .ts files from sources.

    Returns True if command succeeded, False otherwise.
    """
    # Prefer venv pyside6-lupdate, then global pyside6-lupdate, then lupdate
    candidates = []
    venv_bin = Path(".venv/bin/pyside6-lupdate")
    if venv_bin.exists():
        candidates.append(str(venv_bin))
    # system paths
    for name in ("pyside6-lupdate", "lupdate"):
        path = shutil.which(name)
        if path:
            candidates.append(path)

    if not candidates:
        print("No pyside6-lupdate / lupdate binary found on PATH or in .venv/bin")
        return False

    cmd = [candidates[0], "."]
    # Attach all target ts files as -ts args
    for ts in ts_files:
        cmd.extend(["-ts", str(ts)])
    cmd.append("-no-obsolete")

    print("Running external lupdate command:", " ".join(cmd))
    try:
        res = subprocess.run(cmd, check=False)
        return res.returncode == 0
    except Exception as e:
        print("lupdate execution failed:", e)
        return False


def main():
    root = Path(".").resolve()
    translations_dir = root / "translations"
    if not translations_dir.exists():
        print("No translations/ directory found; aborting.")
        return 1

    print("Collecting strings from source files...")
    source_map = collect_all_sources(root)

    ts_files = list(translations_dir.glob("creative_erp_*.ts"))
    if not ts_files:
        print("No .ts files found in translations/ — aborting")
        return 1

    import argparse

    parser = argparse.ArgumentParser(
        description="Sync translation .ts with source strings and optionally run lupdate"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Do not modify .ts, only report"
    )
    parser.add_argument(
        "--run-lupdate",
        action="store_true",
        help="Run pyside6-lupdate/lupdate before scanning",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes into .ts files (opposite of dry-run)",
    )
    args = parser.parse_args()

    dry_run = args.dry_run or not args.apply
    run_lup = args.run_lupdate
    if run_lup:
        print("Attempting to run lupdate/pyside6-lupdate to refresh .ts files first...")
        ok = run_lupdate(ts_files)
        print("lupdate completed:", ok)

    for ts in ts_files:
        print(f"Merging into {ts.name} (dry_run={dry_run})...")
        added, checked = merge_into_ts(ts, source_map, dry_run=dry_run)
        print(f"  missing checked: {checked}, added: {added}")

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
