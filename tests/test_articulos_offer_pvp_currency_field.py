#!/usr/bin/env python3
"""
Tests for the PVP fixed-price input: formatting and saving.
"""
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from core.db import set_current_database
from modules.articulos.view import ArticulosView
from modules.articulos.repository import ArticuloRepository


def ensure_qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_pvp_field_formats_and_saves():
    set_current_database('artstudio3d')
    ensure_qapp()

    v = ArticulosView()
    repo = ArticuloRepository()

    # choose a target article where we can insert an oferta (no oferta for default tarifa)
    tarifa = repo.get_default_tarifa()

    # find an article with no oferta for the tarifa
    art = None
    for a in repo.get_all(limit=10):
        exists = repo.get_oferta_for_article(a['id'], tarifa)
        if not exists:
            art = a
            break

    if art is None:
        # fallback to first article but ensure offers are removed for the test
        all_a = repo.get_all(limit=1)
        assert all_a
        art = all_a[0]
        repo.delete_ofertas_for_article(art['id'])

    assert v.controller.load_by_id(art['id'])

    # go to promotions, enable editing
    v.ui.Pestanas.setCurrentWidget(v.ui.tab_promociones)
    v._lock_fields(False)
    v._on_add_oferta()

    # canonical widget name
    pvp_widget = getattr(v.ui, 'txtofertaPvpFijo', None)
    assert pvp_widget is not None, 'No PVP fixed-price widget available in this UI generation'

    # enter a value using thousands separator and comma decimal
    pvp_widget.setText('1.234,56')
    # simulate user finishing editing so formatting hook runs
    try:
        pvp_widget.editingFinished.emit()
    except Exception:
        # Some test envs may not have a running loop; call formatting helper directly
        v._format_price_field(pvp_widget)

    # Expect formatted result (company uses comma separator and default decimals)
    formatted = pvp_widget.text()
    assert formatted != ''

    # Save offer and verify persisted value
    v._on_save_oferta()

    oferta = repo.get_oferta_for_article(art['id'], tarifa)
    assert oferta is not None
    # precio_final stored as numeric value in DB - should equal parsed float
    assert abs((float(oferta.get('precio_final') or 0) - 1234.56)) < 0.001
