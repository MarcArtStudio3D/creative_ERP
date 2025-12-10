#!/usr/bin/env python3
"""
Mergea un archivo .ts "auto" (generado por extract_tr_from_py.py) dentro del .ts principal
(`translations/creative_erp_fr.ts`) conservando traducciones existentes.

Uso:
  python3 scripts/translations/merge_ts.py \
      --base translations/creative_erp_fr.ts \
      --add  translations/creative_erp_fr_auto.ts

Crea una copia de seguridad de base con sufijo .bak antes de sobrescribir.
"""
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET
import xml.dom.minidom


def parse_ts(path: Path):
    tree = ET.parse(path)
    root = tree.getroot()
    contexts = {}
    for ctx in root.findall('context'):
        name_el = ctx.find('name')
        if name_el is None or name_el.text is None:
            continue
        ctx_name = name_el.text
        msgs = {}
        for m in ctx.findall('message'):
            src = m.find('source')
            if src is None or src.text is None:
                continue
            src_text = src.text
            msgs[src_text] = m
        contexts[ctx_name] = msgs
    return root, contexts


def merge(base_path: Path, add_path: Path, out_path: Path):
    if not base_path.exists():
        # If base doesn't exist, just copy add -> out
        print(f'Base {base_path} not found, copying {add_path} -> {out_path}')
        out_path.write_bytes(add_path.read_bytes())
        return

    base_root, base_ctxs = parse_ts(base_path)
    add_root, add_ctxs = parse_ts(add_path)

    # For each context in add, ensure it exists in base; add missing messages
    for ctx_name, msgs in add_ctxs.items():
        if ctx_name in base_ctxs:
            base_msgs = base_ctxs[ctx_name]
            base_context_el = None
            # find context element
            for c in base_root.findall('context'):
                n = c.find('name')
                if n is not None and n.text == ctx_name:
                    base_context_el = c
                    break
            if base_context_el is None:
                continue
            for src_text, msg_el in msgs.items():
                if src_text not in base_msgs:
                    # append a copy of message
                    base_context_el.append(msg_el)
        else:
            # append entire context
            base_root.append([c for c in add_root.findall('context') if c.find('name') is not None and c.find('name').text == ctx_name][0])

    # Pretty print and write backup
    bak = base_path.with_suffix(base_path.suffix + '.bak')
    if not bak.exists():
        bak.write_bytes(base_path.read_bytes())
        print(f'Backup written to {bak}')

    raw = xml.dom.minidom.parseString(ET.tostring(base_root, encoding='utf-8')).toprettyxml(indent='  ', encoding='utf-8')
    out_path.write_bytes(raw)
    print(f'Merged written to {out_path}')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--base', default='translations/creative_erp_fr.ts')
    p.add_argument('--add', default='translations/creative_erp_fr_auto.ts')
    p.add_argument('--out', default='translations/creative_erp_fr.ts')
    args = p.parse_args()
    base = Path(args.base)
    add = Path(args.add)
    out = Path(args.out)
    if not add.exists():
        print('Add file not found:', add)
        raise SystemExit(1)
    merge(base, add, out)
