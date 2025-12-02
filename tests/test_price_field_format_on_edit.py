#!/usr/bin/env python3
"""
Test UI behaviour: when user types '350.50' in txtPrecioVenta and finishes editing,
UI should display '350,50' immediately.
"""

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from modules.articulos.view import ArticulosView
from core.db import init_artstudio3d_db


def test_price_field_format_on_edit():
    app = QApplication.instance() or QApplication(sys.argv)

    # Ensure DB and UI models are in place
    init_artstudio3d_db()

    view = ArticulosView()

    # Ensure field exists
    assert hasattr(view.ui, 'txtPrecioVenta')

    # Simulate user entering '350.50' and leaving the field (editingFinished)
    view.ui.txtPrecioVenta.setText('350.50')
    # Trigger formatting handler directly
    view._format_price_field(view.ui.txtPrecioVenta)

    # The UI should show comma separator and 2 decimals
    val = view.ui.txtPrecioVenta.text()
    assert val == '350,50', f'Expected 350,50 but got {val}'


if __name__ == '__main__':
    test_price_field_format_on_edit()
    print('OK')
