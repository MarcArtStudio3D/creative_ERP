from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication

from modules.articulos.view import ArticulosView
from modules.common.db_consulta_view import DBConsultaView


def ensure_qapp():
    app = QApplication.instance()
    if app is None:
        QApplication([])


def test_f1_does_not_call_lookup_twice(monkeypatch):
    ensure_qapp()
    v = ArticulosView()

    if not hasattr(v.ui, "txtCodigoTipo"):
        return

    # Enable editing state
    if hasattr(v.ui, "botGuardar"):
        v.ui.botGuardar.setEnabled(True)

    v.controller.current_article = {"id": 1}

    calls = []

    def fake_select(parent, data, headers, campos=None, titulo=None):
        # record that the select dialog was called
        calls.append((parent, len(data)))
        return ({"id": 888, "codigo": "T-ONE", "descripcion": "Tipo One"}, None)

    monkeypatch.setattr(DBConsultaView, "select_from_data", staticmethod(fake_select))

    # Simulate a ShortcutOverride / eventFilter first
    ev = QKeyEvent(QEvent.ShortcutOverride, Qt.Key_F, Qt.ControlModifier)
    v.ui.txtCodigoTipo.setFocus()
    v.eventFilter(v.ui.txtCodigoTipo, ev)

    # Simulate the subsequent KeyPress event that often follows (and can arrive after a modal dialog)
    ev2 = QKeyEvent(QEvent.KeyPress, Qt.Key_F, Qt.ControlModifier)
    v.eventFilter(v.ui.txtCodigoTipo, ev2)

    # only one call should have been made
    assert len(calls) == 1
    assert v.controller.current_article.get("id_tipo") == 888
    assert v.ui.txtCodigoTipo.text() == "T-ONE"
