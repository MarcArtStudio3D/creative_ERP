#!/usr/bin/env python3
"""
Extrae cadenas etiquetadas con self.tr(...) y QCoreApplication.translate(...) de ficheros .py
(bajo app/ y modules/) y genera un archivo .ts básico en translations/ (sin traducciones,
marca type="unfinished").

Uso:
    python3 scripts/translations/extract_tr_from_py.py > /dev/null

No pretende reemplazar pylupdate6, pero ayuda cuando esta no está disponible.
"""

import re
import sys
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom

ROOT = Path(__file__).parent.parent.parent
SRC_DIRS = [ROOT / 'app', ROOT / 'modules']
TS_PATH = ROOT / 'translations' / 'creative_erp_fr_auto.ts'

# Regex patterns
RE_SELF_TR = re.compile(r'self\.tr\(\s*([rR]?["\\\'])(.*?)\1\s*\)')
RE_QT_TRANSLATE = re.compile(r'QCoreApplication\.translate\(\s*([rR]?["\\\'])(.*?)\1\s*,\s*([rR]?["\\\'])(.*?)\3\s*\)')
RE_CLASS = re.compile(r"^class\s+(\w+)\s*[:(]")

contexts = {}

for src in SRC_DIRS:
    if not src.exists():
        continue
    for path in src.rglob('*.py'):
        try:
            text = path.read_text(encoding='utf-8')
        except Exception:
            continue
        # find class names and map ranges
        class_names = []
        lines = text.splitlines()
        current_class = None
        for i, line in enumerate(lines):
            m = RE_CLASS.match(line)
            if m:
                current_class = m.group(1)
                class_names.append((i, current_class))
        # simple approach: collect self.tr occurrences and attribute them to the nearest previous class
        for m in RE_SELF_TR.finditer(text):
            s = m.group(2)
            # find position index to map to class
            pos = m.start()
            cls = None
            for idx, cname in reversed(class_names):
                # approximate: line number of class <-> pos
                # compute char index of line start
                char_index = sum(len(L)+1 for L in lines[:idx])
                if char_index <= pos:
                    cls = cname
                    break
            ctx = cls if cls else path.stem
            contexts.setdefault(ctx, set()).add(s)
        # QCoreApplication.translate(context, source)
        for m in RE_QT_TRANSLATE.finditer(text):
            ctx = m.group(2)
            srcs = m.group(4)
            contexts.setdefault(ctx, set()).add(srcs)

# Build XML .ts
TS = Element('TS')
TS.set('version', '2.1')
TS.set('language', 'fr')

for ctx_name, messages in sorted(contexts.items()):
    context = SubElement(TS, 'context')
    name = SubElement(context, 'name')
    name.text = ctx_name
    for msg in sorted(messages):
        message = SubElement(context, 'message')
        source = SubElement(message, 'source')
        source.text = msg
        translation = SubElement(message, 'translation')
        translation.set('type', 'unfinished')
        translation.text = ''

# Pretty print
raw = xml.dom.minidom.parseString(tostring(TS, 'utf-8')).toprettyxml(indent='  ', encoding='utf-8')
try:
    TS_PATH.write_bytes(raw)
    print(f'Wrote: {TS_PATH}', file=sys.stderr)
except Exception as e:
    print('Error writing ts:', e, file=sys.stderr)

print('Done', file=sys.stderr)
