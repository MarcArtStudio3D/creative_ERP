#!/usr/bin/env python3
"""
Test UI refresh of txtfamilia when family is set via lookup
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from sqlalchemy import text

from core.db import get_session, set_current_database
from modules.articulos.controller import ArticuloController
from modules.articulos.view import ArticulosView


def test_view_familia_refresh():
    print("🧪 Test UI: txtfamilia refresh")
    set_current_database("artstudio3d")

    QApplication.instance() or QApplication(sys.argv)

    controller = ArticuloController()
    session = get_session()

    # Cargar artículo de prueba
    article_row = session.execute(
        text("SELECT id FROM articulos WHERE codigo = 'ART001' LIMIT 1")
    ).fetchone()
    if not article_row:
        print("❌ No se encontró ART001")
        return

    article_id = article_row[0]
    controller.load_by_id(article_id)

    # Obtener una familia distinta
    fam_row = session.execute(
        text("SELECT id, codigo, familia FROM familias ORDER BY id LIMIT 1")
    ).fetchone()
    if not fam_row:
        print("❌ No hay familias en BD")
        return

    familia_id, familia_codigo, familia_nombre = fam_row

    # Simular selección en controller
    controller.set_familia_from_lookup(familia_id, familia_codigo, familia_nombre)

    # Crear la vista y enlazar el controller
    view = ArticulosView()
    view.controller = controller

    # Forzar carga en la vista desde current_article
    view._load_form_from_article()

    txt = view.ui.txtfamilia.text()
    print(f"txtfamilia: '{txt}' (esperado: '{familia_nombre}')")

    if txt == familia_nombre:
        print("✅ txtfamilia actualizado correctamente")
    else:
        print("❌ txtfamilia NO se actualizó")

    session.close()


if __name__ == "__main__":
    test_view_familia_refresh()
