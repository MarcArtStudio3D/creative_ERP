#!/usr/bin/env python3
"""
Test de guardado de familia en artículos
Verifica que el id_familia se guarda correctamente en la base de datos
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text

from core.db import get_session, set_current_database
from modules.articulos.controller import ArticuloController


def test_save_familia():
    print("🧪 Test de guardado de familia en artículo")
    set_current_database("artstudio3d")

    controller = ArticuloController()
    session = get_session()

    # Obtener un artículo de prueba
    art = session.execute(
        text(
            "SELECT id, codigo, id_familia FROM articulos WHERE codigo IN ('ART001','ART002','ART003') LIMIT 1"
        )
    ).fetchone()
    if not art:
        print("❌ No se encontraron artículos de prueba")
        return

    article_id = art[0]
    print(f"📄 Artículo usado: {art[1]} (ID {article_id}), id_familia actual: {art[2]}")

    controller.load_by_id(article_id)

    # Obtener familias disponibles
    familias = session.execute(
        text("SELECT id, codigo, familia FROM familias ORDER BY id LIMIT 2")
    ).fetchall()
    if not familias or len(familias) < 1:
        print("❌ No hay familias para seleccionar en la BD")
        return

    # Seleccionar la primera familia
    f = familias[0]
    familia_id = f[0]
    familia_codigo = f[1]
    familia_nombre = f[2]

    print(
        f"🔍 Seleccionando familia: {familia_codigo} - {familia_nombre} (ID {familia_id})"
    )

    success = controller.set_familia_from_lookup(
        familia_id, familia_codigo, familia_nombre
    )
    if not success:
        print("❌ Error al establecer familia en controller")
        return

    print("✅ Familia establecida en controller. Simulando guardado...")

    form_data = {
        "codigo": controller.get_current_article().get("codigo"),
        "descripcion_reducida": controller.get_current_article().get(
            "descripcion_reducida", "Test"
        ),
        "coste": controller.get_current_article().get("coste", 0),
        "id_familia": controller.get_current_article().get("id_familia"),
    }

    ok, msg = controller.save(form_data)
    print(f"Resultado al guardar: {ok} - {msg}")
    if not ok:
        print("❌ No se pudo guardar el artículo")
        return

    # Verificar en BD
    db_res = session.execute(
        text("SELECT id, codigo, id_familia FROM articulos WHERE id = :id"),
        {"id": article_id},
    ).fetchone()
    # Acceso robusto por nombre de columna cuando SQLAlchemy Row lo soporta; caer a índice si no
    try:
        id_familia_bd = None
        if hasattr(db_res, "_mapping"):
            id_familia_bd = db_res._mapping.get("id_familia")
        else:
            # fallback to positional index
            id_familia_bd = db_res[2] if len(db_res) > 2 else None
    except Exception:
        id_familia_bd = None

    print(f"🔎 En BD: id_familia = {id_familia_bd}")

    if id_familia_bd == familia_id:
        print("✅ Familia guardada correctamente en la base de datos")
    else:
        print(f"❌ ERROR: id_familia esperado {familia_id}, obtenido {id_familia_bd}")

    session.close()


if __name__ == "__main__":
    test_save_familia()
