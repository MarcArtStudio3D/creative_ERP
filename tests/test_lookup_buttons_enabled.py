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

    # Modo edición -> desbloqueado.
    # Observación: las familias dependen de la sección — por tanto el botón de buscar familia
    # no debe activarse hasta que haya una sección seleccionada en el artículo.
    view._lock_fields(False)
    assert view.ui.botBuscarSeccion.isEnabled()
    # No hay sección asignada por defecto -> familia no habilitada
    assert not view.ui.botBuscarFamilia.isEnabled()
    assert not view.ui.botBuscarSubfamilia.isEnabled()

    # Simular que el artículo actual obtiene una sección via lookup -> ahora la búsqueda de familia debe activarse
    # Necesitamos asignar un current_article en el controller para que set_seccion_from_lookup funcione
    # controller.current_article must be truthy for set_seccion_from_lookup to accept it
    view.controller.current_article = {'id': -1}
    view.controller.set_seccion_from_lookup(1, 'S1', 'GENERAL')
    # Actualizar la vista desde el modelo
    view._load_form_from_article()
    assert view.ui.botBuscarFamilia.isEnabled()

    print('✅ lookup buttons enabled/disabled behavior OK')

if __name__ == '__main__':
    test_lookup_buttons_enabled()
