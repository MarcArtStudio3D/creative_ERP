#!/usr/bin/env python3
"""Verifica que el botón de configuración del login tenga un icono establecido."""

import sys
from PySide6.QtWidgets import QApplication

from app.views.login_window_multi import LoginWindowMultiCompany


class DummyAuthManager:
    def __init__(self):
        self._current_session = None


def test_login_config_has_icon():
    app = QApplication.instance() or QApplication(sys.argv)
    auth = DummyAuthManager()

    w = LoginWindowMultiCompany(auth)

    assert hasattr(w, 'config_btn'), "El botón de configuración debe estar en la instancia"
    icon = w.config_btn.icon()
    assert not icon.isNull(), "El botón de configuración debe tener un icono asignado"


if __name__ == '__main__':
    sys.exit(test_login_config_has_icon())
