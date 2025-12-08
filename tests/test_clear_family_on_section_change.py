#!/usr/bin/env python3
"""
Verifica que al cambiar la sección y guardar sin seleccionar nueva familia/subfamilia,
los campos id_familia e id_subfamilia queden a NULL en la base de datos.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text

from core.db import get_session, set_current_database
from modules.articulos.controller import ArticuloController


def test_clear_family_on_section_change():
    set_current_database("artstudio3d")
    controller = ArticuloController()
    session = get_session()

    # Buscar un artículo que tenga familia (y opcionalmente subfamilia)
    art = session.execute(
        text(
            "SELECT id, id_seccion, id_familia, id_subfamilia FROM articulos WHERE id_familia IS NOT NULL LIMIT 1"
        )
    ).fetchone()
    if not art:
        print("ℹ️ No hay artículos con familia en la BD; omitiendo la prueba")
        session.close()
        return

    art_id, orig_seccion, orig_familia, orig_sub = art
    print(
        f"Artículo de prueba: id={art_id}, seccion={orig_seccion}, familia={orig_familia}, sub={orig_sub}"
    )

    # Cargar el artículo
    controller.load_by_id(art_id)
    current = controller.get_current_article()
    assert current is not None
    assert current.get("id_familia") is not None

    # Seleccionar una sección diferente
    sec = session.execute(
        text("SELECT id, codigo, seccion FROM secciones WHERE id != :id LIMIT 1"),
        {"id": orig_seccion},
    ).fetchone()
    if not sec:
        print("ℹ️ No hay otra sección distinta en la BD; omitiendo la prueba")
        session.close()
        return

    new_sec_id, new_sec_code, new_sec_name = sec
    print(f"Cambiando a sección {new_sec_id} - {new_sec_code} / {new_sec_name}")

    # Simular selección de sección (controller debe limpiar familia/subfamilia)
    ok = controller.set_seccion_from_lookup(new_sec_id, new_sec_code, new_sec_name)
    assert ok

    # Preparamos datos de guardado mínimos
    art_now = controller.get_current_article()

    form_data = {
        "codigo": art_now.get("codigo"),
        "descripcion_reducida": art_now.get("descripcion_reducida") or "Test save",
        "id_seccion": art_now.get("id_seccion"),
        "id_familia": art_now.get("id_familia"),
        "id_subfamilia": art_now.get("id_subfamilia"),
    }

    print("Guardando... form_data:", form_data)
    success, msg = controller.save(form_data)
    assert success, f"Fallo al guardar: {msg}"

    # Comprobar en la BD que los campos han quedado a NULL
    db_row = session.execute(
        text("SELECT id_familia, id_subfamilia FROM articulos WHERE id = :id"),
        {"id": art_id},
    ).fetchone()
    print("Fila en BD tras guardado:", db_row)

    assert db_row is not None
    assert (
        db_row[0] is None
    ), "id_familia debería quedar NULL tras cambiar de sección y guardar"
    assert (
        db_row[1] is None
    ), "id_subfamilia debería quedar NULL tras cambiar de sección y guardar"

    # Recargar via controller y comprobar
    controller.load_by_id(art_id)
    reloaded = controller.get_current_article()
    assert reloaded.get("id_familia") is None
    assert reloaded.get("id_subfamilia") is None

    session.close()


if __name__ == "__main__":
    sys.exit(test_clear_family_on_section_change())
