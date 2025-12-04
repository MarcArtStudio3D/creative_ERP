#!/usr/bin/env python3
"""
Tests that saving/undoing an oferta updates the offers table model immediately.
"""
import os, sys
from datetime import date
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QDate

from core.db import set_current_database, get_session
from sqlalchemy import text
from modules.articulos.view import ArticulosView
from modules.articulos.repository import ArticuloRepository


def ensure_qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_save_oferta_refreshes_table():
    set_current_database('artstudio3d')
    ensure_qapp()

    v = ArticulosView()
    repo = ArticuloRepository()
    tarifa = repo.get_default_tarifa()

    session = get_session()
    # pick article with no ofertas for tarifa (or remove them)
    row = session.execute(
        text("SELECT a.id FROM articulos a LEFT JOIN articulos_ofertas ao ON a.id = ao.id_articulo AND ao.id_tarifa = :tarifa WHERE ao.id IS NULL LIMIT 1"),
        {"tarifa": tarifa}
    ).fetchone()
    if row:
        art_id = row[0]
    else:
        r2 = session.execute(text("SELECT id FROM articulos LIMIT 1")).fetchone()
        assert r2, 'No articles available for test'
        art_id = r2[0]
        session.execute(text("DELETE FROM articulos_ofertas WHERE id_articulo = :id AND id_tarifa = :tarifa"), {"id": art_id, "tarifa": tarifa})
        session.commit()

    assert v.controller.load_by_id(art_id)

    # Ensure the model is present and starts empty
    assert hasattr(v, 'ofertas_model')
    initial = v.ofertas_model.rowCount()

    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)
    v._on_add_oferta()

    # Fill basic fields
    v.ui.chkArticulo_promocionado.setChecked(True)
    v.ui.txtOferta_Fecha_ini.setDate(QDate(2025, 1, 1))
    v.ui.txtOferta_Fecha_fin.setDate(QDate(2025, 1, 31))
    if hasattr(v.ui, 'txtOferta_Descripcion_promocion'):
        v.ui.txtOferta_Descripcion_promocion.setText('Table-refresh test')

    # Save oferta (should persist AND refresh the model immediately)
    v._on_save_oferta()

    after = v.ofertas_model.rowCount()
    assert after >= initial + 1

    # The saved oferta should be selected in the UI table
    if hasattr(v.ui, 'tabla_ofertas'):
        sm = v.ui.tabla_ofertas.selectionModel()
        cur = sm.currentIndex()
        assert cur.isValid()
        selected_row = cur.row()
        assert v.ofertas_model.offers[selected_row].get('descripcion') == 'Table-refresh test'


def test_undo_oferta_refreshes_table_removes_created_row():
    set_current_database('artstudio3d')
    ensure_qapp()

    v = ArticulosView()
    repo = ArticuloRepository()
    tarifa = repo.get_default_tarifa()

    session = get_session()
    # pick article with no ofertas for tarifa (or remove them)
    row = session.execute(
        text("SELECT a.id FROM articulos a LEFT JOIN articulos_ofertas ao ON a.id = ao.id_articulo AND ao.id_tarifa = :tarifa WHERE ao.id IS NULL LIMIT 1"),
        {"tarifa": tarifa}
    ).fetchone()
    if row:
        art_id = row[0]
    else:
        r2 = session.execute(text("SELECT id FROM articulos LIMIT 1")).fetchone()
        assert r2, 'No articles available for test'
        art_id = r2[0]
        session.execute(text("DELETE FROM articulos_ofertas WHERE id_articulo = :id AND id_tarifa = :tarifa"), {"id": art_id, "tarifa": tarifa})
        session.commit()

    assert v.controller.load_by_id(art_id)

    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)

    initial = v.ofertas_model.rowCount()

    # Start add -> but then undo
    v._on_add_oferta()
    # Fill something
    if hasattr(v.ui, 'txtOferta_Descripcion_promocion'):
        v.ui.txtOferta_Descripcion_promocion.setText('Will be undone')

    # Undo should cancel the add and refresh the table (no new row)
    v._on_undo_oferta()

    after = v.ofertas_model.rowCount()
    assert after == initial
