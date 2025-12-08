#!/usr/bin/env python3
"""Verifica que el login muestre el logo usando pixmap y no emojis en el label."""

import sys

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication

from app.views.login_window_multi import LoginWindowMultiCompany


class DummyAuthManager:
    def __init__(self):
        self._current_session = None


def test_login_logo_is_pixmap():
    QApplication.instance() or QApplication(sys.argv)
    auth = DummyAuthManager()

    w = LoginWindowMultiCompany(auth)

    assert hasattr(w, "login_logo")
    lbl = w.login_logo

    # If pixmap is available the label should show it, otherwise fallback text
    pm = lbl.pixmap()
    if pm is not None:
        assert isinstance(pm, QPixmap)
    else:
        # fallback: text must not contain emoji characters
        text = lbl.text() or ""
        for ch in ["🎨", "🗑", "⚙", "🛠", "📝", "➕", "📋"]:
            assert ch not in text


if __name__ == "__main__":
    sys.exit(test_login_logo_is_pixmap())
