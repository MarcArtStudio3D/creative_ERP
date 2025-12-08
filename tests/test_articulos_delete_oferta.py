#!/usr/bin/env python3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from PySide6.QtWidgets import QApplication, QMessageBox

from core.db import set_current_database
from modules.articulos.repository import ArticuloRepository
from modules.articulos.view import ArticulosView


@pytest.fixture
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def _ensure_article_with_oferta(repo: ArticuloRepository):
    tarifa_id = repo.get_default_tarifa()
    # Use first article and ensure there's at least one oferta
    art = repo.get_all(limit=1)
    assert art and len(art) > 0
    art_id = art[0]["id"]
    oferta = repo.get_oferta_for_article(art_id, tarifa_id)
    if oferta is None:
        ok = repo.upsert_oferta(
            art_id, tarifa_id, {"activa": True, "descripcion": "to-delete"}
        )
        assert ok
        oferta = repo.get_oferta_for_article(art_id, tarifa_id)
    return art_id, tarifa_id, oferta


def test_delete_selected_oferta_confirmed(qapp, monkeypatch):
    set_current_database("artstudio3d")

    v = ArticulosView()
    repo = ArticuloRepository()

    art_id, tarifa_id, oferta = _ensure_article_with_oferta(repo)

    assert v.controller.load_by_id(art_id)
    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)
    # Populate UI from loaded article so _current_oferta_id is set
    v._load_form_from_article()

    oferta_id = getattr(v, "_current_oferta_id", None)
    assert oferta_id is not None

    def _yes(*args, **kwargs):
        return QMessageBox.StandardButton.Yes

    monkeypatch.setattr("core.ui_helpers.show_question", _yes)

    v._on_borrar_oferta()

    assert repo.get_oferta_by_id(oferta_id) is None


def test_delete_selected_oferta_cancelled(qapp, monkeypatch):
    set_current_database("artstudio3d")

    v = ArticulosView()
    repo = ArticuloRepository()

    art_id, tarifa_id, oferta = _ensure_article_with_oferta(repo)

    assert v.controller.load_by_id(art_id)
    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)
    v._load_form_from_article()

    oferta_id = getattr(v, "_current_oferta_id", None)
    assert oferta_id is not None

    def _no(*args, **kwargs):
        return QMessageBox.StandardButton.No

    monkeypatch.setattr("core.ui_helpers.show_question", _no)

    v._on_borrar_oferta()

    # Should still be present
    assert repo.get_oferta_by_id(oferta_id) is not None
