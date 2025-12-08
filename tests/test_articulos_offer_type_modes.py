#!/usr/bin/env python3
"""
Tests for offer-type field enabling behavior for all modes: 3x2, dto local, dto web, pvp.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication

from core.db import set_current_database
from modules.articulos.view import ArticulosView


def ensure_qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def _collect_widgets(view, names):
    present = {}
    for n in names:
        present[n] = getattr(view.ui, n, None)
    return present


def test_3x2_mode_enables_por_cada_and_regalo():
    set_current_database("artstudio3d")
    ensure_qapp()

    v = ArticulosView()
    v._on_add_oferta()

    if not hasattr(v.ui, "chkOferta_32"):
        return

    v.ui.chkOferta_32.setChecked(True)
    v._sync_oferta_type_fields()

    # fields to be enabled (canonical UI names)
    enabled_names = ["txtOfertaPorCada", "txtOfertaregaloUnidades"]
    disabled_names = ["txtOfertaDtoOferta", "txtOferta_dto_web", "txtofertaPvpFijo"]

    for name in enabled_names:
        w = getattr(v.ui, name, None)
        if w is not None:
            assert w.isEnabled(), f"{name} should be enabled for 3x2"

    for name in disabled_names:
        w = getattr(v.ui, name, None)
        if w is not None:
            assert not w.isEnabled(), f"{name} should be disabled for 3x2"


def test_dto_local_mode_enables_dto_local_only():
    set_current_database("artstudio3d")
    ensure_qapp()

    v = ArticulosView()
    v._on_add_oferta()

    if not hasattr(v.ui, "chkOferta_dto"):
        return

    v.ui.chkOferta_dto.setChecked(True)
    v._sync_oferta_type_fields()

    # enabled
    if hasattr(v.ui, "txtOfertaDtoOferta"):
        assert v.ui.txtOfertaDtoOferta.isEnabled()
    if hasattr(v.ui, "txtOfertaDto"):
        assert v.ui.txtOfertaDto.isEnabled()

    # disabled
    for name in [
        "txtOferta_dto_web",
        "txtofertaPvpFijo",
        "txtOfertaPorCada",
        "txtOfertaregaloUnidades",
    ]:
        w = getattr(v.ui, name, None)
        if w is not None:
            assert not w.isEnabled(), f"{name} should be disabled for dto local"


def test_dto_web_mode_enables_dto_web_only():
    set_current_database("artstudio3d")
    ensure_qapp()

    v = ArticulosView()
    v._on_add_oferta()

    if not hasattr(v.ui, "chkOferta_web"):
        return

    v.ui.chkOferta_web.setChecked(True)
    v._sync_oferta_type_fields()

    # enabled
    for name in ["txtOferta_dto_web"]:
        w = getattr(v.ui, name, None)
        if w is not None:
            assert w.isEnabled(), f"{name} should be enabled for dto web"

    # disabled
    for name in [
        "txtOfertaDtoOferta",
        "txtofertaPvpFijo",
        "txtOfertaPorCada",
        "txtOfertaregaloUnidades",
    ]:
        w = getattr(v.ui, name, None)
        if w is not None:
            assert not w.isEnabled(), f"{name} should be disabled for dto web"


def test_pvp_mode_enables_precio_fijo_only():
    set_current_database("artstudio3d")
    ensure_qapp()

    v = ArticulosView()
    v._on_add_oferta()

    if not hasattr(v.ui, "chkOfertaPvp"):
        return

    v.ui.chkOfertaPvp.setChecked(True)
    v._sync_oferta_type_fields()

    # enabled
    for name in ["txtofertaPvpFijo"]:
        w = getattr(v.ui, name, None)
        if w is not None:
            assert w.isEnabled(), f"{name} should be enabled for pvp"

    # disabled
    for name in [
        "txtOfertaDtoOferta",
        "txtOferta_dto_web",
        "txtOfertaPorCada",
        "txtOfertaregaloUnidades",
    ]:
        w = getattr(v.ui, name, None)
        if w is not None:
            assert not w.isEnabled(), f"{name} should be disabled for pvp"
