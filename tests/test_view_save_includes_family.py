#!/usr/bin/env python3
"""
Test that view._save_form_to_article includes id_familia and id_subfamilia when set in controller
"""

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from core.db import set_current_database, get_session
from sqlalchemy import text
from modules.articulos.controller import ArticuloController
from modules.articulos.view import ArticulosView


def test_view_save_includes_family():
    print('🧪 Test UI: _save_form_to_article incluye id_familia/id_subfamilia')
    set_current_database('artstudio3d')

    app = QApplication.instance() or QApplication(sys.argv)

    controller = ArticuloController()
    session = get_session()

    # Cargar artículo de prueba
    article_row = session.execute(text("SELECT id FROM articulos WHERE codigo = 'ART001' LIMIT 1")).fetchone()
    if not article_row:
        print('❌ No se encontró ART001')
        return
    article_id = article_row[0]
    controller.load_by_id(article_id)

    # Seleccionar familia y subfamilia desde BD
    fam = session.execute(text("SELECT id, codigo, familia FROM familias ORDER BY id LIMIT 1")).fetchone()
    if not fam:
        print('❌ No hay familias en BD')
        return
    familia_id, familia_codigo, familia_nombre = fam

    # Intentamos subfamilia (puede no existir)
    sub = session.execute(text("SELECT id, subfamilia FROM subfamilias WHERE id_familia = :fid ORDER BY id LIMIT 1"), {'fid': familia_id}).fetchone()
    if sub:
        sub_id = sub[0]
    else:
        sub_id = None

    # Set in controller
    controller.set_familia_from_lookup(familia_id, familia_codigo, familia_nombre)
    if sub_id:
        # Add method to controller if needed (we set directly for test)
        controller.current_article['id_subfamilia'] = sub_id

    # Create view and attach controller
    view = ArticulosView()
    view.controller = controller

    # Ensure some fields are set so _save_form_to_article doesn't complain
    view.ui.txtcodigo.setText(controller.get_current_article().get('codigo'))
    view.ui.txtdescripcionResumida.setText(controller.get_current_article().get('descripcion_reducida', 'Test'))

    data = view._save_form_to_article()
    print('Datos devueltos por _save_form_to_article:', data)

    if 'id_familia' in data and data['id_familia'] == familia_id:
        print('✅ id_familia incluido correctamente')
    else:
        print('❌ id_familia NO incluido')

    if sub_id:
        if 'id_subfamilia' in data and data['id_subfamilia'] == sub_id:
            print('✅ id_subfamilia incluido correctamente')
        else:
            print('❌ id_subfamilia NO incluido')
    else:
        print('ℹ️ No había subfamilias para esta familia en la BD, omitiendo comprobación de subfamilia')

    session.close()

if __name__ == '__main__':
    test_view_save_includes_family()
