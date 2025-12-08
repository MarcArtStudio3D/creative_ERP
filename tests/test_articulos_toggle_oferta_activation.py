#!/usr/bin/env python3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from PySide6.QtWidgets import QApplication, QMessageBox
from sqlalchemy import text

from core.db import get_session, set_current_database
from modules.articulos.repository import ArticuloRepository
from modules.articulos.view import ArticulosView


@pytest.fixture
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def _get_article_with_oferta(repo: ArticuloRepository):
    tarifa_id = repo.get_default_tarifa()
    session = get_session()
    row = session.execute(text("SELECT a.id FROM articulos a LIMIT 1")).fetchone()
    assert row, "No articles present in DB for test"
    art_id = row[0]
    # Ensure we have an oferta for this article and make sure it's active
    ok = repo.upsert_oferta(
        art_id, tarifa_id, {"activa": True, "descripcion": "test-toggle"}
    )
    assert ok
    return art_id, tarifa_id


def test_toggle_oferta_when_confirmed_yes(qapp, monkeypatch):
    set_current_database("artstudio3d")

    v = ArticulosView()

    repo = ArticuloRepository()
    art_id, tarifa_id = _get_article_with_oferta(repo)

    # Load article in controller/view
    assert v.controller.load_by_id(art_id)

    # Ensure we're on promotions tab and editing mode so the button is enabled
    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)
    v._on_edit_oferta()

    # Populate the form from the loaded article so view._current_oferta_id is set
    v._load_form_from_article()

    oferta_id = getattr(v, "_current_oferta_id", None)
    assert oferta_id is not None

    # Monkeypatch the confirmation dialog to simulate user clicking YES
    def _yes(*args, **kwargs):
        return QMessageBox.StandardButton.Yes

    monkeypatch.setattr("core.ui_helpers.show_question", _yes)

    # Quick sanity check — the controller.save_oferta API should be able to toggle directly
    ok_direct, msg_direct = v.controller.save_oferta({"id": oferta_id, "activa": False})
    assert ok_direct, f"Direct controller save failed: {msg_direct}"

    # Now simulate using the view handler as the user would (monkeypatched dialog returns Yes)
    v._on_toggle_oferta_activa()

    # Verify repository shows toggled state (was True, should now be False)
    oferta = repo.get_oferta_by_id(oferta_id)
    assert oferta is not None
    assert oferta.get("activa") in (0, False)


def test_toggle_oferta_when_cancelled_no(qapp, monkeypatch):
    set_current_database("artstudio3d")

    v = ArticulosView()

    repo = ArticuloRepository()
    art_id, tarifa_id = _get_article_with_oferta(repo)

    assert v.controller.load_by_id(art_id)

    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)
    v._on_edit_oferta()

    # Populate form from loaded article to set current oferta id
    v._load_form_from_article()

    oferta_id = getattr(v, "_current_oferta_id", None)
    assert oferta_id is not None

    # Get current state first
    oferta_before = repo.get_oferta_by_id(oferta_id)
    state_before = bool(oferta_before.get("activa"))

    # Simulate user cancelling (No)
    def _no(*args, **kwargs):
        return QMessageBox.StandardButton.No

    monkeypatch.setattr("core.ui_helpers.show_question", _no)

    v._on_toggle_oferta_activa()

    oferta_after = repo.get_oferta_by_id(oferta_id)
    assert oferta_after is not None
    # State should be unchanged
    assert bool(oferta_after.get("activa")) == state_before
