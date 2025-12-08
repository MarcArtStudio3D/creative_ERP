#!/usr/bin/env python3
"""
Comprueba que `get_subfamilias_data(id_familia)` devuelve sólo subfamilias de esa familia.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text

from core.db import get_session, set_current_database
from modules.articulos.controller import ArticuloController
from modules.articulos.repository import ArticuloRepository


def test_subfamilias_filtered_by_familia():
    set_current_database("artstudio3d")
    repo = ArticuloRepository()
    controller = ArticuloController()
    session = get_session()

    # Obtener una familia con subfamilias
    fam = session.execute(text("SELECT id FROM familias LIMIT 1")).fetchone()
    if not fam:
        print("ℹ️ No hay familias en BD; omitiendo test")
        session.close()
        return
    fam_id = fam[0]

    subs = session.execute(
        text("SELECT id FROM subfamilias WHERE id_familia = :fid LIMIT 1"),
        {"fid": fam_id},
    ).fetchall()
    if not subs:
        print("ℹ️ La familia seleccionada no tiene subfamilias; omitiendo test")
        session.close()
        return

    repo_res = repo.get_subfamilias_data(fam_id)
    ctrl_res = controller.get_subfamilias_data(fam_id)

    repo_ids = set([r["id"] for r in repo_res])
    ctrl_ids = set([r["id"] for r in ctrl_res])

    assert repo_ids == ctrl_ids
    # Verify none of returned have different id_familia
    for item in repo_res:
        # ensure id_familia present when query was filtered
        # repository returns id/subfamily/code but not id_familia; we'll query DB to confirm
        row = session.execute(
            text("SELECT id_familia FROM subfamilias WHERE id = :id"),
            {"id": item["id"]},
        ).fetchone()
        assert row[0] == fam_id

    session.close()


if __name__ == "__main__":
    sys.exit(test_subfamilias_filtered_by_familia())
