#!/usr/bin/env python3
"""
Comprueba el comportamiento del botón de subfamilia respecto a modo edición y existencia de familia.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from sqlalchemy import text

from core.db import get_session, set_current_database
from modules.articulos.controller import ArticuloController
from modules.articulos.view import ArticulosView


def test_subfamily_button_conditions():
    set_current_database("artstudio3d")
    QApplication.instance() or QApplication(sys.argv)

    view = ArticulosView()
    controller = ArticuloController()

    # Cargar un artículo sin familia
    session = get_session()
    art = session.execute(
        text("SELECT id FROM articulos WHERE id_familia IS NULL LIMIT 1")
    ).fetchone()
    if not art:
        print("ℹ️ No hay artículos sin familia para probar — buscando otro")
        art = session.execute(text("SELECT id FROM articulos LIMIT 1")).fetchone()
    article_id = art[0]
    controller.load_by_id(article_id)
    view.controller = controller

    # Estado por defecto: bloqueo -> botones lookup deshabilitados
    view._lock_fields(True)
    assert not view.ui.botBuscarSubfamilia.isEnabled()

    # Modo edición pero sin familia -> subfamilia sigue deshabilitada
    view._lock_fields(False)
    # Asegurar que el articulo no tiene familia
    current = controller.get_current_article()
    if current.get("id_familia"):
        # Si tiene familia, vamos a borrarla temporalmente para la prueba
        current["id_familia"] = None
    assert not view.ui.botBuscarSubfamilia.isEnabled()

    # Ahora asignamos una familia al artículo vía controller y comprobamos que, estando en edición, el botón se habilita
    fam = session.execute(
        text("SELECT id, codigo, familia FROM familias LIMIT 1")
    ).fetchone()
    if not fam:
        print("❌ No hay familias en la BD para la prueba")
        session.close()
        return
    familia_id, codigo, nombre = fam

    controller.set_familia_from_lookup(familia_id, codigo, nombre)
    # Simular que estamos en modo edición
    view._lock_fields(False)
    # La vista debería haber activado el botón de búsqueda de subfamilia
    assert view.ui.botBuscarSubfamilia.isEnabled()

    print("✅ Comportamiento de botBuscarSubfamilia correcto")
    session.close()


if __name__ == "__main__":
    test_subfamily_button_conditions()
