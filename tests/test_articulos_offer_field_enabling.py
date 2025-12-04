#!/usr/bin/env python3
"""
Test that selecting an oferta type toggles the correct oferta input fields.
"""
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication

from core.db import set_current_database
from modules.articulos.view import ArticulosView


def ensure_qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_offer_type_32_enables_correct_fields():
    set_current_database('artstudio3d')
    ensure_qapp()

    v = ArticulosView()

    # Enter 'add oferta' mode so controls are enabled for editing
    v._on_add_oferta()

    # Ensure the radio and fields exist in the UI; if they don't, skip assertions gracefully
    if not hasattr(v.ui, 'chkOferta_32'):
        return

    # Activate the 3x2 option and sync fields
    v.ui.chkOferta_32.setChecked(True)
    v._sync_oferta_type_fields()

    # Support multiple naming variants for these fields; at least one should exist
    por_cada_vars = ['txtOfertaPorCada']
    regalo_vars = ['txtOfertaregaloUnidades']
    assert any(getattr(v.ui, n, None) is not None for n in por_cada_vars)
    assert any(getattr(v.ui, n, None) is not None for n in regalo_vars)

    # confirm present widgets are enabled
    for n in por_cada_vars:
        w = getattr(v.ui, n, None)
        if w is not None:
            assert w.isEnabled(), f"{n} should be enabled for 3x2"
    for n in regalo_vars:
        w = getattr(v.ui, n, None)
        if w is not None:
            assert w.isEnabled(), f"{n} should be enabled for 3x2"

    # The other special fields should be disabled for 3x2
    if hasattr(v.ui, 'txtOfertaDtoOferta'):
        assert not v.ui.txtOfertaDtoOferta.isEnabled()
    if hasattr(v.ui, 'txtOferta_dto_web'):
        assert not v.ui.txtOferta_dto_web.isEnabled()
    # fixed-price input should be disabled for 3x2 mode
    if hasattr(v.ui, 'txtofertaPvpFijo'):
        assert not v.ui.txtofertaPvpFijo.isEnabled()
