#!/usr/bin/env python3
"""
Post-process generated UI python files to make connections to .accept() safe.
Replaces lines like:
    self.btn.clicked.connect(frX.accept)
with:
    try:
        self.btn.clicked.connect(frX.accept)
    except Exception:
        try:
            self.btn.clicked.connect(frX.close)
        except Exception:
            pass

This keeps the project robust when UI output is used with QWidget objects that do not implement accept().
"""

import sys
import re
from pathlib import Path

pattern = re.compile(r"^(?P<indent>\s*)(?P<call>[^\n]*\.connect\([^\n]*\.accept\)\s*)$")

if len(sys.argv) < 2:
    print('Usage: fix_accept_connections.py <file1.py> [file2.py ...]')
    sys.exit(1)

for file in sys.argv[1:]:
    p = Path(file)
    if not p.exists():
        print(f"Skipping {file}: not found")
        continue
    text = p.read_text(encoding='utf-8')
    lines = text.splitlines()
    new_lines = []
    changed = False
    for ln in lines:
        m = pattern.match(ln)
        if m:
            indent = m.group('indent')
            call = m.group('call').rstrip()
            # build replacement
            rep = [f"{indent}try:",
                   f"{indent}    {call}",
                   f"{indent}except Exception:",
                   f"{indent}    try:",
                   f"{indent}        {call.replace('.accept)', '.close)')}",
                   f"{indent}    except Exception:",
                   f"{indent}        pass"]
            new_lines.extend(rep)
            changed = True
        else:
            new_lines.append(ln)
    if changed:
        p.write_text('\n'.join(new_lines) + '\n', encoding='utf-8')
        print(f'Patched accept connects in: {file}')
    else:
        print(f'No matches in: {file}')
