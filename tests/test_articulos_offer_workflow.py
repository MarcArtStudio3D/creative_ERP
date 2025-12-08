"""Tests for offer workflow buttons in ArticulosView:
- Clicking 'Añadir oferta' enables save and undo, disables add/edit.
- After 'Guardar oferta' or 'Deshacer oferta' the buttons revert to non-edit state.
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


def test_click_add_enables_save_and_undo(qapp):
    v = ArticulosView()

    # switch to promotions tab and enter article edit mode
    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)

    assert v.ui.btnAnadirOferta.isEnabled()
    assert v.ui.btnEditarOferta.isEnabled()

    # simulate clicking add oferta
    v._on_add_oferta()

    # expect save and undo enabled, add/edit disabled
    assert v.ui.btnguardar_oferta.isEnabled()
    assert v.ui.btnDeshacerOferta.isEnabled()
    assert not v.ui.btnAnadirOferta.isEnabled()
    assert not v.ui.btnEditarOferta.isEnabled()


def test_save_reverts_buttons(qapp):
    v = ArticulosView()
    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)

    v._on_add_oferta()
    # simulate saving oferta
    v._on_save_oferta()

    # save & undo should be disabled, add/edit re-enabled
    assert not v.ui.btnguardar_oferta.isEnabled()
    assert not v.ui.btnDeshacerOferta.isEnabled()
    assert v.ui.btnAnadirOferta.isEnabled()
    assert v.ui.btnEditarOferta.isEnabled()


def test_undo_reverts_buttons(qapp):
    v = ArticulosView()
    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)

    v._on_add_oferta()
    v._on_undo_oferta()

    assert not v.ui.btnguardar_oferta.isEnabled()
    assert not v.ui.btnDeshacerOferta.isEnabled()
    assert v.ui.btnAnadirOferta.isEnabled()
    assert v.ui.btnEditarOferta.isEnabled()
