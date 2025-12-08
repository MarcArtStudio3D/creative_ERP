#!/usr/bin/env python3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from PySide6.QtWidgets import QApplication
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


def test_saving_article_without_promotion_does_not_create_oferta(qapp):
    set_current_database("artstudio3d")

    v = ArticulosView()

    repo = ArticuloRepository()
    tarifa_id = repo.get_default_tarifa()

    session = get_session()
    row = session.execute(
        text(
            "SELECT a.id FROM articulos a LEFT JOIN articulos_ofertas ao ON a.id = ao.id_articulo AND ao.id_tarifa = :tarifa WHERE ao.id IS NULL LIMIT 1"
        ),
        {"tarifa": tarifa_id},
    ).fetchone()

    if row:
        art_id = row[0]
    else:
        row2 = session.execute(text("SELECT id FROM articulos LIMIT 1")).fetchone()
        assert row2, "No articles present in DB for test"
        art_id = row2[0]
        # Ensure no ofertas for this article so we can test creation is not automatic
        session.execute(
            text(
                "DELETE FROM articulos_ofertas WHERE id_articulo = :id AND id_tarifa = :tarifa"
            ),
            {"id": art_id, "tarifa": tarifa_id},
        )
        session.commit()

    # Load article in controller/view
    assert v.controller.load_by_id(art_id)
    # Ensure form reflects loaded article (this populates oferta-related keys)
    v._load_form_from_article()

    # Make a non-offer modification and save the article
    try:
        v.ui.txtdescripcionResumida.setText("changed-no-offer")
    except Exception:
        # If the field doesn't exist in some UI variants, skip modification
        pass

    # Save article - this should NOT create an articulos_ofertas row
    v._on_save_clicked()

    created = repo.get_oferta_for_article(art_id, tarifa_id)
    assert (
        created is None
    ), "Saving article without meaningful oferta data should NOT create oferta rows"
