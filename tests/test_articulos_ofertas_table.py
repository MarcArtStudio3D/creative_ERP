#!/usr/bin/env python3
"""
Tests for the ofertas table view/model: first column shows indicator for activa,
second column contains descripcion.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from core.db import get_session, set_current_database
from modules.articulos.repository import ArticuloRepository
from modules.articulos.view import ArticulosView


def ensure_qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_offers_table_shows_active_indicator_and_description():
    set_current_database("artstudio3d")
    ensure_qapp()

    v = ArticulosView()
    repo = ArticuloRepository()
    tarifa = repo.get_default_tarifa()

    session = get_session()
    from sqlalchemy import text

    row = session.execute(text("SELECT id FROM articulos LIMIT 1")).fetchone()
    assert row, "Requires at least one article"
    art_id = row[0]

    # Clear any existing ofertas and create two offers for the target article
    session.execute(
        text("DELETE FROM articulos_ofertas WHERE id_articulo = :id"), {"id": art_id}
    )
    session.commit()

    o1 = repo.insert_oferta(art_id, tarifa, {"descripcion": "First", "activa": True})
    o2 = repo.insert_oferta(art_id, tarifa, {"descripcion": "Second", "activa": False})
    assert o1 and o2

    # Also create an oferta for another article to ensure it's not listed
    row2 = session.execute(
        text("SELECT id FROM articulos WHERE id != :id LIMIT 1"), {"id": art_id}
    ).fetchone()
    if row2:
        other = row2[0]
        repo.insert_oferta(other, tarifa, {"descripcion": "Other", "activa": True})

    # Load article and refresh offers table
    assert v.controller.load_by_id(art_id)
    v._load_form_from_article()

    # Model should be present and contain exactly 2 rows (only offers for this article)
    model = v.ofertas_model
    assert model.rowCount() == 2

    # Active flag should show decoration (green pixmap) in first column for first row
    index0 = model.index(0, 0)
    dec0 = model.data(index0, Qt.ItemDataRole.DecorationRole)
    disp0 = model.data(index0, Qt.ItemDataRole.DisplayRole)
    align0 = model.data(index0, Qt.ItemDataRole.TextAlignmentRole)
    assert dec0 is not None
    assert disp0 == ""
    # alignment should be centered for first column
    assert align0 in (Qt.AlignmentFlag.AlignCenter, int(Qt.AlignmentFlag.AlignCenter))

    # Description in second column should match
    index1 = model.index(0, 1)
    desc = model.data(index1, Qt.ItemDataRole.DisplayRole)
    assert desc == "First"

    # Second row (inactive) should not have decoration
    index_inactive = model.index(1, 0)
    dec1 = model.data(index_inactive, Qt.ItemDataRole.DecorationRole)
    disp1 = model.data(index_inactive, Qt.ItemDataRole.DisplayRole)
    align1 = model.data(index_inactive, Qt.ItemDataRole.TextAlignmentRole)
    assert dec1 is None
    assert disp1 == ""
    assert align1 in (Qt.AlignmentFlag.AlignCenter, int(Qt.AlignmentFlag.AlignCenter))
