#!/usr/bin/env python3
"""
Test UI refresh of txtsubfamilia when subfamily is set via lookup
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from sqlalchemy import text

from core.db import get_session, set_current_database
from modules.articulos.controller import ArticuloController
from modules.articulos.view import ArticulosView


def test_view_subfamilia_refresh():
    print("🧪 Test UI: txtsubfamilia refresh")
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

    # Obtener una subfamilia
    sub_row = session.execute(
        text("SELECT id, subfamilia FROM subfamilias ORDER BY id LIMIT 1")
    ).fetchone()
    if not sub_row:
        print("❌ No hay subfamilias en BD")
        return

    sub_id, sub_nombre = sub_row

    # Simular selección en controller
    controller.set_subfamilia_from_lookup(sub_id, "SF1", sub_nombre)

    # Crear la vista y enlazar el controller
    view = ArticulosView()
    view.controller = controller

    # Forzar carga en la vista desde current_article
    view._load_form_from_article()

    txt = view.ui.txtsubfamilia.text()
    print(f"txtsubfamilia: '{txt}' (esperado: '{sub_nombre}')")

    if txt == sub_nombre:
        print("✅ txtsubfamilia actualizado correctamente")
    else:
        print("❌ txtsubfamilia NO se actualizó")

    session.close()


if __name__ == "__main__":
    test_view_subfamilia_refresh()
