from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import QEvent, Qt
from modules.articulos.view import ArticulosView
from modules.common.db_consulta_view import DBConsultaView


def ensure_qapp():
    app = QApplication.instance()
    if app is None:
        QApplication([])


def test_shortcutoverride_f1_is_handled(monkeypatch):
    ensure_qapp()
    v = ArticulosView()

    if not hasattr(v.ui, 'txtCodigoTipo'):
        return

    # Ensure editing enabled
    if hasattr(v.ui, 'botGuardar'):
        v.ui.botGuardar.setEnabled(True)

    v.controller.current_article = {'id': 1}

    fake_selected = {'id': 777, 'codigo': 'T-OVR', 'descripcion': 'Tipo Override'}

    def fake_select(parent, data, headers, campos=None, titulo=None):
        return fake_selected, None

    monkeypatch.setattr(DBConsultaView, 'select_from_data', staticmethod(fake_select))

    # Ensure the widget is focused so ShortcutOverride will point to it
    v.ui.txtCodigoTipo.setFocus()

    # Simulate ShortcutOverride event (what Qt sends when a shortcut might be handled)
    ev = QKeyEvent(QEvent.ShortcutOverride, Qt.Key_F, Qt.ControlModifier)

    handled = v.eventFilter(v.ui.txtCodigoTipo, ev)

    assert handled is True
    assert v.controller.current_article.get('id_tipo') == 777
    assert v.ui.txtCodigoTipo.text() == 'T-OVR'
