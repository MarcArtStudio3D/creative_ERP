#!/usr/bin/env python3
"""
Test que comprueba que al pulsar buscar subfamilia sin familia seleccionada
se muestra un mensaje informativo (hint).
"""

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from core.ui_helpers import show_info
from modules.articulos.view import ArticulosView
from modules.articulos.controller import ArticuloController
from core.db import set_current_database


def test_subfamily_hint_shown(monkeypatch):
    set_current_database('artstudio3d')
    app = QApplication.instance() or QApplication(sys.argv)

    view = ArticulosView()
    controller = ArticuloController()

    # Cargamos un artículo sin familia
    controller.load_by_id(controller.repository.get_all(limit=1)[0]['id'])
    # Forzamos que no tenga familia
    if controller.current_article:
        controller.current_article['id_familia'] = None

    view.controller = controller

    # Interceptar QMessageBox.information para capturar la llamada
    called = {'msg': None}

    def fake_info(parent, title, text):
        called['msg'] = text

    monkeypatch.setattr('core.ui_helpers.show_info', fake_info)

    # Llamamos al método que maneja el clic
    view._on_buscar_subfamilia_clicked()

    assert called['msg'] == 'Antes de buscar subfamilias, seleccione primero una familia.'
    print('✅ Mensaje informativo mostrado correctamente cuando no hay familia seleccionada')


if __name__ == '__main__':
    test_subfamily_hint_shown(__import__('pytest').monkeypatch)
