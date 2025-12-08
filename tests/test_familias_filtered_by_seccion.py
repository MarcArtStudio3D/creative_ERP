#!/usr/bin/env python3
"""
Comprueba que `get_familias_data` devuelve sólo familias pertenecientes a la sección indicada.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text

from core.db import get_session, set_current_database
from modules.articulos.controller import ArticuloController
from modules.articulos.repository import ArticuloRepository


def test_familias_filtered_by_seccion():
    set_current_database("artstudio3d")
    repo = ArticuloRepository()
    controller = ArticuloController()
    session = get_session()

    # Obtener dos secciones distintas que tengan familias
    rows = session.execute(
        text("SELECT id FROM secciones ORDER BY id LIMIT 2")
    ).fetchall()
    if len(rows) < 2:
        print("ℹ️ No hay suficientes secciones para probar el filtrado; omitiendo test")
        session.close()
        return

    sec1 = rows[0][0]
    sec2 = rows[1][0]

    # Obtener familias para cada sección desde BD usando SQL directo
    fams1 = session.execute(
        text("SELECT id FROM familias WHERE id_seccion = :sid ORDER BY id"),
        {"sid": sec1},
    ).fetchall()
    fams2 = session.execute(
        text("SELECT id FROM familias WHERE id_seccion = :sid ORDER BY id"),
        {"sid": sec2},
    ).fetchall()

    if not fams1 or not fams2:
        print("ℹ️ Una de las secciones no tiene familias; omitiendo test")
        session.close()
        return

    # Llamadas al repo y controller para comprobar filtrado
    repo_f1 = repo.get_familias_data(sec1)
    repo_f2 = repo.get_familias_data(sec2)

    controller_f1 = controller.get_familias_data(sec1)
    controller_f2 = controller.get_familias_data(sec2)

    # Extraer ids
    repo_ids1 = set([f["id"] for f in repo_f1])
    repo_ids2 = set([f["id"] for f in repo_f2])
    ctrl_ids1 = set([f["id"] for f in controller_f1])
    set([f["id"] for f in controller_f2])

    assert (
        repo_ids1 == ctrl_ids1
    ), "Controller debe delegar en el repo y devolver los mismos ids"

    # Asegurarse que los sets no se mezclan
    if repo_ids1 and repo_ids2:
        assert repo_ids1.isdisjoint(
            repo_ids2
        ), "Familias de diferentes secciones no deben mezclarse"

    session.close()


if __name__ == "__main__":
    sys.exit(test_familias_filtered_by_seccion())
