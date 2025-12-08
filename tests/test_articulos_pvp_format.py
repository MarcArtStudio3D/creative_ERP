#!/usr/bin/env python3
"""
Test para asegurar que la tabla de artículos muestra PVP con coma y el número de decimales correcto.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.articulos.view import ArticlesTableModel


def test_articles_table_pvp_format():
    model = ArticlesTableModel()
    # If precio_venta is missing, this must be considered a fatal error (we require the column)
    article = {
        "codigo": "TST001",
        "descripcion_reducida": "Test",
        "stock_real": 5,
        "coste": 10.0,
        "margen": 25,
    }
    try:
        model.set_articles([article])
        assert False, "Expected RuntimeError because precio_venta key is missing"
    except RuntimeError as e:
        assert "precio_venta" in str(e)

    # If precio_venta field exists, it should be used as-is
    article2 = {
        "codigo": "TST002",
        "descripcion_reducida": "Test2",
        "stock_real": 3,
        "precio_venta": 99.95,
    }
    model.set_articles([article2])
    idx2 = model.index(0, 3)
    val2 = model.data(idx2, 0x0)
    assert "99,95" in val2

    # If precio_venta exists but is explicitly None, this should be considered invalid
    article3 = {
        "codigo": "TST003",
        "descripcion_reducida": "Test3",
        "stock_real": 1,
        "precio_venta": None,
    }
    try:
        model.set_articles([article3])
        assert False, "Expected RuntimeError because precio_venta is None"
    except RuntimeError:
        pass


if __name__ == "__main__":
    test_articles_table_pvp_format()
    print("OK")
