#!/usr/bin/env python3
"""Comprueba que main_window_v2.py no contiene emojis problemáticos en sus textos UI.

Este test es estático (analiza el fichero fuente) y evita que emojis vuelvan a introducirse por accidente.
"""

import sys
from pathlib import Path

EMOJIS_TO_CHECK = ["🎨", "🗑", "⚙", "🛠", "📝", "➕", "📋", "📦", "💰", "📁"]


def test_main_window_no_ui_emoji():
    p = Path(__file__).parents[1] / "app" / "views" / "main_window_v2.py"
    content = p.read_text(encoding="utf-8")
    for e in EMOJIS_TO_CHECK:
        assert (
            e not in content
        ), f"Emoji {e} should not appear in main_window_v2.py UI texts"


if __name__ == "__main__":
    sys.exit(test_main_window_no_ui_emoji())
