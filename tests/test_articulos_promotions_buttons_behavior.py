"""Tests ensuring promo-buttons behaviour (btnAnadirOferta / btnEditarOferta)
are correct: enabled only in edit mode AND when promotions tab is active; disabled otherwise.
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


def test_promo_buttons_enabled_only_when_editing_and_on_tab(qapp):
    v = ArticulosView()

    # Ensure promotions tab exists
    assert hasattr(v.ui, "tab_promociones")

    # Case 1: not editing (locked) -> buttons should be disabled even if on promotions tab
    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(True)
    assert hasattr(v.ui, "btnAnadirOferta") and not v.ui.btnAnadirOferta.isEnabled()
    assert hasattr(v.ui, "btnEditarOferta") and not v.ui.btnEditarOferta.isEnabled()
    # also check legacy name
    if hasattr(v.ui, "btnEditartarifa"):
        assert not v.ui.btnEditartarifa.isEnabled()

    # Case 2: editing + promotions tab -> buttons should be enabled
    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)
    assert hasattr(v.ui, "btnAnadirOferta") and v.ui.btnAnadirOferta.isEnabled()
    assert hasattr(v.ui, "btnEditarOferta") and v.ui.btnEditarOferta.isEnabled()
    if hasattr(v.ui, "btnEditartarifa"):
        assert v.ui.btnEditartarifa.isEnabled()


def test_promo_buttons_disabled_if_not_on_promotions_tab_even_when_editing(qapp):
    v = ArticulosView()

    # Ensure we're on article tab and editing
    v.ui.Pestanas.setCurrentIndex(0)
    v._lock_fields(False)

    if hasattr(v.ui, "btnAnadirOferta"):
        assert not v.ui.btnAnadirOferta.isEnabled()
    if hasattr(v.ui, "btnEditarOferta"):
        assert not v.ui.btnEditarOferta.isEnabled()
    if hasattr(v.ui, "btnEditartarifa"):
        assert not v.ui.btnEditartarifa.isEnabled()
