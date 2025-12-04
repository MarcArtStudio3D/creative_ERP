#!/usr/bin/env python3
"""
Test selecting a row in tabla_ofertas populates the promotion form and allows editing/saving.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from core.db import set_current_database, get_session
from modules.articulos.view import ArticulosView
from modules.articulos.repository import ArticuloRepository


def ensure_qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_select_row_populates_form_and_save_updates_activa():
    set_current_database('artstudio3d')
    ensure_qapp()

    v = ArticulosView()
    repo = ArticuloRepository()

    session = get_session()
    from sqlalchemy import text
    row = session.execute(text("SELECT id FROM articulos LIMIT 1")).fetchone()
    assert row, 'Requires at least one article'
    art_id = row[0]

    # Remove any existing ofertas for target article and create one inactive oferta
    session.execute(text("DELETE FROM articulos_ofertas WHERE id_articulo = :id"), {"id": art_id})
    session.commit()

    tarifa = repo.get_default_tarifa()
    created = repo.insert_oferta(art_id, tarifa, {'descripcion': 'Selectable', 'activa': False})
    assert created
    oferta_id = created.get('id')

    # Load article into view
    assert v.controller.load_by_id(art_id)
    v._load_form_from_article()

    # Ensure table has one row and selecting it populates fields
    model = v.ofertas_model
    assert model.rowCount() == 1

    idx = model.index(0, 0)
    # Simulate click handler
    v._on_tabla_ofertas_clicked(idx)

    # Check fields populated
    assert getattr(v, '_current_oferta_id', None) == oferta_id
    if hasattr(v.ui, 'txtOferta_Descripcion_promocion'):
        assert v.ui.txtOferta_Descripcion_promocion.text() == 'Selectable'
    # Offer was created inactive
    if hasattr(v.ui, 'chkArticulo_promocionado'):
        assert v.ui.chkArticulo_promocionado.isChecked() is False

    # Enable editing and toggle activa
    v._on_edit_oferta()
    if hasattr(v.ui, 'chkArticulo_promocionado'):
        v.ui.chkArticulo_promocionado.setChecked(True)

    # Save oferta
    v._on_save_oferta()

    # Validate repository shows oferta activated
    updated = repo.get_oferta_by_id(oferta_id)
    assert updated
    assert bool(updated.get('activa')) is True

    # Refresh UI and ensure table decoration now present
    v._load_form_from_article()
    dec = model.data(model.index(0, 0), Qt.ItemDataRole.DecorationRole)
    assert dec is not None
