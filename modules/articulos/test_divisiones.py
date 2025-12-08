"""
Script de prueba para verificar que las tablas de divisiones se crean correctamente
"""

import os
import sys

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import logging

from sqlmodel import select

from core.db import get_session, init_db
from modules.articulos.models import Articulo, Familia, Seccion, Subfamilia


def test_crear_tablas():
    """Prueba la creación de tablas en la base de datos"""
    logging.getLogger(__name__).info("=" * 60)
    logging.getLogger(__name__).info("TEST: Creación de tablas de divisiones")
    logging.getLogger(__name__).info("=" * 60)

    try:
        # Cambiar a base de datos de empresa (ajustar según sea necesario)
        # set_current_database('company_1')  # Descomentar para probar con empresa específica

        # Inicializar base de datos
        logging.getLogger(__name__).info("\n1. Inicializando base de datos...")
        init_db()
        logging.getLogger(__name__).info("   ✅ Base de datos inicializada")

        # Verificar que las tablas existen
        session = get_session()

        logging.getLogger(__name__).info("\n2. Verificando tablas...")

        # Intentar contar registros en cada tabla
        count_secciones = session.exec(select(Seccion)).count()
        logging.getLogger(__name__).info(
            f"   ✅ Tabla 'secciones' existe ({count_secciones} registros)"
        )

        count_familias = session.exec(select(Familia)).count()
        logging.getLogger(__name__).info(
            f"   ✅ Tabla 'familias' existe ({count_familias} registros)"
        )

        count_subfamilias = session.exec(select(Subfamilia)).count()
        logging.getLogger(__name__).info(
            f"   ✅ Tabla 'subfamilias' existe ({count_subfamilias} registros)"
        )

        count_articulos = session.exec(select(Articulo)).count()
        logging.getLogger(__name__).info(
            f"   ✅ Tabla 'articulos' existe ({count_articulos} registros)"
        )

        logging.getLogger(__name__).info(
            "\n3. Probando creación de datos de ejemplo..."
        )

        # Crear una sección de ejemplo
        seccion = Seccion(
            codigo="S001",
            seccion="Electrónica",
            comentario="Productos electrónicos",
        )

        # Verificar si ya existe
        seccion_existente = session.exec(
            select(Seccion).where(Seccion.codigo == "S001")
        ).first()
        if seccion_existente:
            logging.getLogger(__name__).info(
                "   ℹ️  Sección 'S001' ya existe, usando la existente"
            )
            seccion = seccion_existente
        else:
            session.add(seccion)
            session.commit()
            session.refresh(seccion)
            logging.getLogger(__name__).info(f"   ✅ Sección creada: {seccion}")

        # Crear una familia de ejemplo
        familia_existente = session.exec(
            select(Familia).where(Familia.codigo == "F001")
        ).first()
        if familia_existente:
            logging.getLogger(__name__).info("   ℹ️  Familia 'F001' ya existe")
        else:
            familia = Familia(
                codigo="F001",
                familia="Smartphones",
                id_seccion=seccion.id,
            )
            session.add(familia)
            session.commit()
            session.refresh(familia)
            logging.getLogger(__name__).info(f"   ✅ Familia creada: {familia}")

            # Crear una subfamilia de ejemplo
            subfamilia = Subfamilia(
                codigo="SF001",
                subfamilia="Android",
                id_familia=familia.id,
            )
            session.add(subfamilia)
            session.commit()
            session.refresh(subfamilia)
            logging.getLogger(__name__).info(f"   ✅ Subfamilia creada: {subfamilia}")

        logging.getLogger(__name__).info("\n" + "=" * 60)
        logging.getLogger(__name__).info("✅ TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
        logging.getLogger(__name__).info("=" * 60)

        session.close()
        return True

    except Exception:
        logging.getLogger(__name__).exception("❌ ERROR test_divisiones")
        return False


if __name__ == "__main__":
    exito = test_crear_tablas()
    sys.exit(0 if exito else 1)
