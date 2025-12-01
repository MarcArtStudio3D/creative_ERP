#!/usr/bin/env python3
"""
Verifica que los botones de lookup para sección, familia y subfamilia se habilitan en modo edición
"""

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from modules.articulos.view import ArticulosView


def test_lookup_buttons_enabled():
    app = QApplication.instance() or QApplication(sys.argv)
    view = ArticulosView()

    # En modo lectura por defecto, los botones deben estar desactivados
    view._lock_fields(True)
    assert not view.ui.botBuscarSeccion.isEnabled()
    assert not view.ui.botBuscarFamilia.isEnabled()
    assert not view.ui.botBuscarSubfamilia.isEnabled()

    # Modo edición -> desbloqueado (la subfamilia queda deshabilitada por defecto si no hay familia seleccionada)
    view._lock_fields(False)
    assert view.ui.botBuscarSeccion.isEnabled()
    assert view.ui.botBuscarFamilia.isEnabled()
    assert not view.ui.botBuscarSubfamilia.isEnabled()

    print('✅ lookup buttons enabled/disabled behavior OK')

if __name__ == '__main__':
    test_lookup_buttons_enabled()
