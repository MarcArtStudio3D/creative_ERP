#!/usr/bin/env python3
"""Verifica que la vista Divisiones del Almacén no contiene emojis en sus textos UI."""

from pathlib import Path

EMOJIS = ['📁', '🔧', '💡']


def test_divisiones_no_emojis():
    p = Path(__file__).parents[1] / 'modules' / 'divisiones_almacen' / 'view.py'
    content = p.read_text(encoding='utf-8')
    for e in EMOJIS:
        assert e not in content, f"Emoji {e} should not be present in divisiones view"


if __name__ == '__main__':
    test_divisiones_no_emojis()
