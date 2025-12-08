#!/usr/bin/env python3
"""
Verify that saving via the view/controller updates the oferta identified by its own id
and not only by the article id. This allows multiple ofertas per article.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from sqlalchemy import text

from core.db import get_session, set_current_database
from modules.articulos.repository import ArticuloRepository
from modules.articulos.view import ArticulosView


def ensure_qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_save_updates_specific_oferta_by_id():
    set_current_database("artstudio3d")

    ensure_qapp()

    v = ArticulosView()
    repo = ArticuloRepository()
    tarifa_id = repo.get_default_tarifa()

    session = get_session()
    # choose a simple article
    row = session.execute(text("SELECT id FROM articulos LIMIT 1")).fetchone()
    assert row, "No articles in DB for test"
    art_id = row[0]

    # Create two ofertas for the same article
    a = repo.insert_oferta(art_id, tarifa_id, {"descripcion": "first", "unidades": 2})
    b = repo.insert_oferta(art_id, tarifa_id, {"descripcion": "second", "unidades": 4})
    assert a and b and a.get("id") != b.get("id")

    id_a = a.get("id")
    id_b = b.get("id")

    # Load article into controller/view
    assert v.controller.load_by_id(art_id)

    # Simulate selecting the second oferta for editing in the GUI
    v._current_oferta_id = id_b
    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)
    v._on_edit_oferta()

    # Change unidades for oferta b and save
    if hasattr(v.ui, "txtOfertaPorCada"):
        v.ui.txtOfertaPorCada.setText("9")

    v._on_save_oferta()

    # Verify oferta b updated but oferta a unchanged
    updated_a = repo.get_oferta_by_id(id_a)
    updated_b = repo.get_oferta_by_id(id_b)

    assert updated_a is not None
    assert updated_b is not None
    assert float(updated_a.get("unidades") or 0) == 2.0
    assert float(updated_b.get("unidades") or 0) == 9.0
