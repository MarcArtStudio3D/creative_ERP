#!/usr/bin/env python3
"""
Test de guardado de precio_venta en artículos
Verifica que el campo precio_venta se persiste correctamente en la base de datos
"""

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.db import set_current_database, get_session
from sqlalchemy import text
from modules.articulos.controller import ArticuloController


def test_save_precio_venta():
    print("🧪 Test de guardado de precio_venta en artículo")
    set_current_database('artstudio3d')

    controller = ArticuloController()
    session = get_session()

    # Obtener un artículo de prueba
    art = session.execute(text("SELECT id, codigo FROM articulos WHERE codigo IN ('ART001','ART002','ART003') LIMIT 1")).fetchone()
    if not art:
        print('❌ No se encontraron artículos de prueba')
        session.close()
        return

    article_id = art[0]
    print(f"📄 Artículo usado: {art[1]} (ID {article_id})")

    success = controller.load_by_id(article_id)
    if not success:
        print('❌ No se pudo cargar el artículo en el controller')
        session.close()
        return

    # Simular edición: asignar precio_venta
    pv_value = 123.45
    form_data = {
        'codigo': controller.get_current_article().get('codigo'),
        'descripcion_reducida': controller.get_current_article().get('descripcion_reducida', 'Test Precio'),
        'coste': controller.get_current_article().get('coste', 0),
        'precio_venta': pv_value
    }

    ok, msg = controller.save(form_data)
    print(f"Resultado al guardar: {ok} - {msg}")
    if not ok:
        print('❌ No se pudo guardar el artículo')
        session.close()
        return

    # Verificar en BD
    db_res = session.execute(text('SELECT precio_venta FROM articulos WHERE id = :id'), {'id': article_id}).fetchone()
    print(f"🔎 En BD: precio_venta = {db_res[0]}")

    # Comparing floats - allow small epsilon
    try:
        assert db_res is not None
        assert abs(float(db_res[0]) - pv_value) < 0.0001
        print('✅ precio_venta guardado correctamente en la base de datos')
    except AssertionError:
        print(f"❌ ERROR: precio_venta esperado {pv_value}, obtenido {db_res[0]}")

    session.close()


if __name__ == '__main__':
    test_save_precio_venta()
