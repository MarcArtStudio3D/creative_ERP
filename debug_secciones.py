#!/usr/bin/env python3
"""
Test para verificar los datos de secciones que recibimos
"""

import os
import sys

sys.path.insert(0, os.path.abspath("."))

import logging

from core.db import set_current_database
from modules.articulos.controller import ArticuloController


def debug_secciones_data():
    """Debug de datos de secciones"""

    # Configurar base de datos
    set_current_database("artstudio3d")
    logging.getLogger(__name__).info("✅ Base de datos configurada a: artstudio3d")

    # Crear controller
    controller = ArticuloController()

    # Obtener datos
    secciones_data = controller.get_secciones_data()

    logging.getLogger(__name__).info(f"Number of sections found: {len(secciones_data)}")
    logging.getLogger(__name__).info("Section data:")

    for i, seccion in enumerate(secciones_data):
        logging.getLogger(__name__).info(f"  [{i}] {seccion}")
        logging.getLogger(__name__).debug(
            f"      id: {seccion.get('id')} (tipo: {type(seccion.get('id'))})"
        )
        logging.getLogger(__name__).debug(
            f"      codigo: {seccion.get('codigo')} (tipo: {type(seccion.get('codigo'))})"
        )
        logging.getLogger(__name__).debug(
            f"      seccion: {seccion.get('seccion')} (tipo: {type(seccion.get('seccion'))})"
        )


if __name__ == "__main__":
    debug_secciones_data()
