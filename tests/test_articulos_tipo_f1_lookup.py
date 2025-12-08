from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent

from modules.articulos.view import ArticulosView
from modules.common.db_consulta_view import DBConsultaView


def test_f1_lookup_opens_dialog_and_sets_tipo(monkeypatch):
    v = ArticulosView()

    # Ensure we are in 'editing' mode
    if hasattr(v.ui, "botGuardar"):
        v.ui.botGuardar.setEnabled(True)

    # Prepare fake result from DBConsultaView.select_from_data
    fake_selected = {
        "id": 123,
        "codigo": "T-TEST",
        "descripcion": "Tipo Test",
        "requiereEAN": True,
        "proveedor": True,
    }

    def fake_select_from_data(parent, data, headers, campos=None, titulo=None):
        return fake_selected, None

    monkeypatch.setattr(
        DBConsultaView, "select_from_data", staticmethod(fake_select_from_data)
    )

    # Ensure controller.current_article exists so set_tipo_from_lookup can write to it
    v.controller.current_article = {"id": 1}

    # Call the handler directly (simulates pressing F1)
    v._on_buscar_tipo_clicked()

    # Verify UI fields and controller were updated
    assert v.controller.current_article.get("id_tipo") == 123
    assert v.controller.current_article.get("codigo_tipo") == "T-TEST"
    assert v.controller.current_article.get("descripcion_tipo") == "Tipo Test"

    if hasattr(v.ui, "txtCodigoTipo"):
        assert v.ui.txtCodigoTipo.text() == "T-TEST"
    if hasattr(v.ui, "txtDescripcionTipo"):
        assert v.ui.txtDescripcionTipo.text() == "Tipo Test"

    # visibility based on flags
    if hasattr(v.ui, "txtcodigo_barras"):
        assert v.ui.txtcodigo_barras.isVisible() is True
    if hasattr(v.ui, "txtcodigo_fabricante"):
        assert v.ui.txtcodigo_fabricante.isVisible() is True


def test_eventfilter_captures_f1(monkeypatch):
    v = ArticulosView()
    if not hasattr(v.ui, "txtCodigoTipo"):
        return

    # Ensure editing enabled
    if hasattr(v.ui, "botGuardar"):
        v.ui.botGuardar.setEnabled(True)

    v.controller.current_article = {"id": 1}

    fake_selected = {
        "id": 321,
        "codigo": "T-KEY",
        "descripcion": "Tipo Key",
        "requiereEAN": False,
        "proveedor": False,
    }

    def fake_select(parent, data, headers, campos=None, titulo=None):
        return fake_selected, None

    monkeypatch.setattr(DBConsultaView, "select_from_data", staticmethod(fake_select))

    # Simulate Ctrl+F key press on the widget
    key_event = QKeyEvent(QEvent.KeyPress, Qt.Key_F, Qt.ControlModifier)
    handled = v.eventFilter(v.ui.txtCodigoTipo, key_event)

    assert handled is True
    assert v.controller.current_article.get("id_tipo") == 321
    assert v.ui.txtCodigoTipo.text() == "T-KEY"
    # visibility should reflect flags
    if hasattr(v.ui, "txtcodigo_barras"):
        assert v.ui.txtcodigo_barras.isVisible() is False
    if hasattr(v.ui, "txtcodigo_fabricante"):
        assert v.ui.txtcodigo_fabricante.isVisible() is False
