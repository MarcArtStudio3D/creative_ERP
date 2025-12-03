#!/usr/bin/env python3
"""
Tests verifying that the view handler for saving offers persists to the DB:
- If the user adds an offer and clicks save, a new articulos_ofertas row is created
- If the user edits an existing offer and clicks save, the existing row is updated
"""
import sys
import os
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QDate

from core.db import set_current_database, get_session
from sqlalchemy import text
from modules.articulos.view import ArticulosView
from modules.articulos.repository import ArticuloRepository


@pytest.fixture
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def test_view_save_creates_new_oferta(qapp):
    set_current_database('artstudio3d')

    v = ArticulosView()

    # Try to find an article that doesn't already have an oferta for default tarifa.
    repo = ArticuloRepository()
    tarifa_id = repo.get_default_tarifa()

    session = get_session()
    row = session.execute(
        text("""
        SELECT a.id FROM articulos a
        LEFT JOIN articulos_ofertas ao ON a.id = ao.id_articulo AND ao.id_tarifa = :tarifa
        WHERE ao.id IS NULL LIMIT 1
        """),
        {"tarifa": tarifa_id}
    ).fetchone()

    if row:
        art_id = row[0]
        ok = v.controller.load_by_id(art_id)
        assert ok
        art = v.controller.get_current_article()
    else:
        # No clean article found. Try to pick a first article and remove any oferta so we can test insert
        row2 = session.execute(text("SELECT id FROM articulos LIMIT 1")).fetchone()
        assert row2, "No articles present in DB for test"
        art_id = row2[0]
        # Ensure the articulos_ofertas rows for this article and tarifa are removed to simulate no oferta
        session.execute(text("DELETE FROM articulos_ofertas WHERE id_articulo = :id AND id_tarifa = :tarifa"), {"id": art_id, "tarifa": tarifa_id})
        session.commit()
        ok = v.controller.load_by_id(art_id)
        assert ok
        art = v.controller.get_current_article()

    repo = ArticuloRepository()
    # Ensure no oferta exists
    existing = repo.get_oferta_for_article(art_id, tarifa_id)
    assert existing is None

    # Switch to promotions tab and enable editing
    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)

    v._on_add_oferta()

    # Fill fields
    v.ui.chkArticulo_promocionado.setChecked(True)
    v.ui.txtOferta_Fecha_ini.setDate(QDate(2025, 1, 1))
    v.ui.txtOferta_Fecha_fin.setDate(QDate(2025, 1, 31))

    # Save oferta via view handler
    v._on_save_oferta()

    # Verify oferta now present
    oferta = repo.get_oferta_for_article(art_id, tarifa_id)
    assert oferta is not None
    assert oferta.get('fecha_inicio') == date(2025, 1, 1)
    assert oferta.get('fecha_fin') == date(2025, 1, 31)
    assert oferta.get('activa') in (1, True)


def test_view_save_updates_existing_oferta(qapp):
    set_current_database('artstudio3d')

    v = ArticulosView()

    # Find or create an article we can manipulate
    repo = ArticuloRepository()
    tarifa_id = repo.get_default_tarifa()

    session = get_session()
    row = session.execute(text("SELECT id FROM articulos LIMIT 1")).fetchone()
    assert row, "No articles present in DB for test"
    art_id = row[0]
    ok = v.controller.load_by_id(art_id)
    assert ok
    art = v.controller.get_current_article()

    repo = ArticuloRepository()
    tarifa_id = repo.get_default_tarifa()

    # Insert an initial oferta
    repo.upsert_oferta(art_id, tarifa_id, {
        'fecha_inicio': date(2025, 1, 1),
        'fecha_fin': date(2025, 1, 31),
        'activa': True,
        'descripcion': 'initial'
    })

    # Reload controller to pick up oferta
    v.controller.load_by_id(art_id)

    # Start editing
    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)
    v._on_edit_oferta()

    # Change dates and activa flag
    v.ui.chkArticulo_promocionado.setChecked(False)
    v.ui.txtOferta_Fecha_ini.setDate(QDate(2026, 2, 2))
    v.ui.txtOferta_Fecha_fin.setDate(QDate(2026, 2, 28))

    v._on_save_oferta()

    # Verify the row updated
    oferta = repo.get_oferta_for_article(art_id, tarifa_id)
    assert oferta is not None
    assert oferta.get('fecha_inicio') == date(2026, 2, 2)
    assert oferta.get('fecha_fin') == date(2026, 2, 28)
    # activa should reflect False (0) now
    assert oferta.get('activa') in (0, False, None) or oferta.get('activa') == False
