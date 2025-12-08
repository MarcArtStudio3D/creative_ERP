#!/usr/bin/env python3
"""
Tests to ensure promotion input fields are enabled when entering offer edit mode
via btnAnadirOferta / btnEditarOferta and disabled after saving/undo.
"""
import pytest
from PySide6.QtWidgets import QApplication

from modules.articulos.view import ArticulosView


@pytest.fixture
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def _is_enabled(view, name):
    if not hasattr(view.ui, name):
        return False
    try:
        return getattr(view.ui, name).isEnabled()
    except Exception:
        return False


def test_add_enables_promotion_fields(qapp):
    v = ArticulosView()

    # Simulate entering article edit mode and switching to promotions tab
    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)

    # Start adding an offer
    v._on_add_oferta()

    # Check some representative promotion fields are enabled
    assert _is_enabled(v, "txtOferta_Descripcion_promocion")
    assert _is_enabled(v, "txtofertaPvpFijo") or _is_enabled(v, "txtOfertaPorCada")
    # The activation and delete buttons should be enabled while editing an oferta
    if hasattr(v.ui, "btnActivarOferta"):
        assert v.ui.btnActivarOferta.isEnabled()
    if hasattr(v.ui, "btnBorrarOferta"):
        assert v.ui.btnBorrarOferta.isEnabled()
    assert _is_enabled(v, "chkOferta_32") or _is_enabled(v, "chkOferta_dto")
    # Date fields should become enabled (because add triggers editing and checkbox should be allowed)
    # The checkbox itself must be enabled too
    assert _is_enabled(v, "chkArticulo_promocionado")


def test_edit_enables_promotion_fields(qapp):
    v = ArticulosView()

    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)

    v._on_edit_oferta()

    assert _is_enabled(v, "txtOferta_Descripcion_promocion")
    assert _is_enabled(v, "txtofertaPvpFijo") or _is_enabled(v, "txtOfertaPorCada")
    # Activation & delete buttons should also be enabled while editing
    if hasattr(v.ui, "btnActivarOferta"):
        assert v.ui.btnActivarOferta.isEnabled()
    if hasattr(v.ui, "btnBorrarOferta"):
        assert v.ui.btnBorrarOferta.isEnabled()
    assert _is_enabled(v, "chkOferta_32") or _is_enabled(v, "chkOferta_dto")


def test_save_or_undo_disables_promotion_fields(qapp):
    v = ArticulosView()

    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)

    v._on_add_oferta()
    # Save -> UI should exit editing mode
    v._on_save_oferta()

    assert not _is_enabled(v, "txtOferta_Descripcion_promocion")
    # Also validate date fields are not enabled (unless article-level editing allows it)
    assert not _is_enabled(v, "txtOferta_Fecha_ini")
    assert not _is_enabled(v, "txtOferta_Fecha_fin")

    # Now re-enter editing and cancel -> should also disable fields
    v._on_add_oferta()
    v._on_undo_oferta()

    assert not _is_enabled(v, "txtOferta_Descripcion_promocion")
    # After saving/undo the action buttons should be disabled
    if hasattr(v.ui, "btnActivarOferta"):
        assert not v.ui.btnActivarOferta.isEnabled()
    if hasattr(v.ui, "btnBorrarOferta"):
        assert not v.ui.btnBorrarOferta.isEnabled()
