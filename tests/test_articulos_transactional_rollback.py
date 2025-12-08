#!/usr/bin/env python3
"""
Test that save is transactional: if oferta upsert fails, the article update is rolled back.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text

from core.db import get_session, set_current_database
from modules.articulos.controller import ArticuloController
from modules.articulos.repository import ArticuloRepository


def test_save_rolls_back_when_upsert_fails():
    set_current_database("artstudio3d")

    controller = ArticuloController()
    ArticuloRepository()

    session = get_session()
    row = session.execute(text("SELECT id, codigo FROM articulos LIMIT 1")).fetchone()
    assert row, "No articulo available in DB to run transactional test"

    art_id, orig_codigo = row[0], row[1]

    controller.load_by_id(art_id)

    # Patch the repository method to simulate failure during upsert
    import modules.articulos.repository as repo_mod

    original_upsert = repo_mod.ArticuloRepository.upsert_oferta

    def failing_upsert(self, articulo_id, id_tarifa, oferta_data):
        raise Exception("Simulated failure during oferta upsert")

    try:
        repo_mod.ArticuloRepository.upsert_oferta = failing_upsert

        # Prepare form that would update the article
        form_data = {
            "codigo": orig_codigo or "X_TEST",
            "descripcion_reducida": "Transactional rollback test",
            "articulo_promocionado": True,
            "oferta_fecha_inicio": None,
            "oferta_fecha_fin": None,
        }

        success, message = controller.save(form_data)

        # Save should fail because upsert raises
        assert not success, f"Expected save to fail but it succeeded: {message}"

        # Reload from DB to ensure original codigo wasn't changed
        db_row = session.execute(
            text("SELECT codigo FROM articulos WHERE id = :id"), {"id": art_id}
        ).fetchone()
        assert db_row is not None
        assert db_row[0] == orig_codigo, "Article update was not rolled back"

    finally:
        # Restore original method
        repo_mod.ArticuloRepository.upsert_oferta = original_upsert
        session.close()


if __name__ == "__main__":
    test_save_rolls_back_when_upsert_fails()
