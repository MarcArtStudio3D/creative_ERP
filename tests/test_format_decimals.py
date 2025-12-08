#!/usr/bin/env python3
"""
Unit tests for decimal formatting helper in ArticulosView.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.articulos.view import format_decimal_value


def test_format_decimal_value_basic():
    assert format_decimal_value(12.34567, 2) == "12,35"
    assert format_decimal_value(12.3, 3) == "12,300"
    assert format_decimal_value("9.876", 1) == "9,9"
    assert format_decimal_value("not-a-number", 2) == "not-a-number"


def test_parse_decimal_input():
    from core.utils import parse_decimal_input

    assert parse_decimal_input("350,50") == 350.5
    assert parse_decimal_input("1.234,56") == 1234.56
    assert parse_decimal_input("1,234.56") == 1234.56
    assert parse_decimal_input("1234") == 1234.0
    try:
        parse_decimal_input("abc")
        assert False, "should raise"
    except ValueError:
        pass


if __name__ == "__main__":
    test_format_decimal_value_basic()
    print("format decimal tests OK")
