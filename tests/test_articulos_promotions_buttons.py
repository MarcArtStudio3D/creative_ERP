"""Tests for promotions-related button states in ArticulosView.

Ensure that while editing an article and the promotions tab is active, the "Añadir" and
"Editar" buttons remain enabled so the user can manage promotional tariffs.
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


def test_add_edit_buttons_enabled_on_promotions_while_editing(qapp):
    v = ArticulosView()

    # Ensure promotions tab widget exists
    assert hasattr(v.ui, "tab_promociones"), "Promotions tab missing in UI"

    # Switch to promotions tab and then enter edit mode
    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)

    # Promotion-specific buttons should be enabled while editing
    assert hasattr(v.ui, "btnAnadirOferta") and v.ui.btnAnadirOferta.isEnabled()
    assert hasattr(v.ui, "btnEditarOferta") and v.ui.btnEditarOferta.isEnabled()
    if hasattr(v.ui, "btnEditartarifa"):
        assert v.ui.btnEditartarifa.isEnabled()


def test_add_edit_buttons_disabled_when_editing_other_tabs(qapp):
    v = ArticulosView()

    # Ensure we're not on promotions tab
    # Choose first tab (article tab) which has object name != 'tab_promociones'
    v.ui.Pestanas.setCurrentIndex(0)

    # Simulate editing mode
    v._lock_fields(False)

    assert (
        not v.ui.botAnadir.isEnabled()
    ), "botAnadir should be disabled while editing in non-promotions tabs"
    assert (
        not v.ui.botEditar.isEnabled()
    ), "botEditar should be disabled while editing in non-promotions tabs"


def test_add_edit_buttons_enabled_when_not_editing(qapp):
    v = ArticulosView()

    # Ensure not editing (locked state)
    v._lock_fields(True)

    assert v.ui.botAnadir.isEnabled(), "botAnadir should be enabled when not editing"
    assert v.ui.botEditar.isEnabled(), "botEditar should be enabled when not editing"
