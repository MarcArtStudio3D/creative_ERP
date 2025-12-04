#!/usr/bin/env python3
"""
Test that highlight animation is started when highlight_row_by_id is called.
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


def test_highlight_starts_animation():
    set_current_database('artstudio3d')
    ensure_qapp()

    v = ArticulosView()
    repo = ArticuloRepository()
    tarifa = repo.get_default_tarifa()

    # pick some article; ensure at least one oferta exists
    offers_found = None
    for a in repo.get_all(limit=5):
        art_id = a.get('id')
        offers = repo.get_ofertas_for_article(art_id)
        if offers:
            offers_found = (art_id, offers)
            break

    if not offers_found:
        # create an oferta for first article
        candidate = repo.get_all(limit=1)
        assert candidate, 'No articles for test'
        art_id = candidate[0]['id']
        res = repo.insert_oferta(art_id, tarifa, {'descripcion': 'AnimTest', 'activa': True})
        assert res
        # reload
        offers = repo.get_ofertas_for_article(art_id)
    else:
        art_id, offers = offers_found

    assert v.controller.load_by_id(art_id)
    # ensure UI populates model
    v._load_form_from_article()

    assert hasattr(v, 'ofertas_model')
    assert v.ofertas_model.rowCount() >= 1

    oferta_id = v.ofertas_model.offers[0].get('id')
    # trigger highlight animation
    v.ofertas_model.highlight_row_by_id(oferta_id, duration_ms=200)

    # Expect either an active animation reference or an opacity entry
    assert oferta_id in v.ofertas_model._active_animations or oferta_id in v.ofertas_model._highlighted_ids
