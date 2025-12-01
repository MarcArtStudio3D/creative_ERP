#!/usr/bin/env python3
"""
Test de guardado de subfamilia en artículos
Verifica que el id_subfamilia se guarda correctamente en la base de datos
"""

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.db import set_current_database, get_session
from sqlalchemy import text
from modules.articulos.controller import ArticuloController


def test_save_subfamilia():
    print("🧪 Test de guardado de subfamilia en artículo")
    set_current_database('artstudio3d')

    controller = ArticuloController()
    session = get_session()

    # Obtener un artículo de prueba
    art = session.execute(text("SELECT id, codigo FROM articulos WHERE codigo IN ('ART001','ART002','ART003') LIMIT 1")).fetchone()
    if not art:
        print('❌ No se encontraron artículos de prueba')
        return

    article_id = art[0]
    print(f"📄 Artículo usado: {art[1]} (ID {article_id})")

    controller.load_by_id(article_id)

    # Obtener una subfamilia (sin filtrar por familia para la prueba)
    sub = session.execute(text("SELECT id, id_familia, codigo, subfamilia FROM subfamilias ORDER BY id LIMIT 1")).fetchone()
    if not sub:
        print('❌ No hay subfamilias para seleccionar en la BD')
        return

    sub_id, id_familia, sub_codigo, sub_nombre = sub
    print(f"🔍 Seleccionando subfamilia: {sub_codigo} - {sub_nombre} (ID {sub_id})")

    success = controller.set_subfamilia_from_lookup(sub_id, sub_codigo, sub_nombre)
    if not success:
        print('❌ Error al establecer subfamilia en controller')
        return

    print('✅ Subfamilia establecida en controller. Simulando guardado...')

    form_data = {
        'codigo': controller.get_current_article().get('codigo'),
        'descripcion_reducida': controller.get_current_article().get('descripcion_reducida', 'Test'),
        'coste': controller.get_current_article().get('coste', 0),
        'id_subfamilia': controller.get_current_article().get('id_subfamilia')
    }

    ok, msg = controller.save(form_data)
    print(f"Resultado al guardar: {ok} - {msg}")
    if not ok:
        print('❌ No se pudo guardar el artículo')
        return

    # Verificar en BD
    db_res = session.execute(text('SELECT id, codigo, id_subfamilia FROM articulos WHERE id = :id'), {'id': article_id}).fetchone()
    print(f"🔎 En BD: id_subfamilia = {db_res[2]}")

    if db_res[2] == sub_id:
        print('✅ Subfamilia guardada correctamente en la base de datos')
    else:
        print(f"❌ ERROR: id_subfamilia esperado {sub_id}, obtenido {db_res[2]}")

    session.close()

if __name__ == '__main__':
    test_save_subfamilia()
