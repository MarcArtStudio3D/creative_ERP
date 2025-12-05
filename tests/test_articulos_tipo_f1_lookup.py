from modules.articulos.view import ArticulosView
from modules.common.db_consulta_view import DBConsultaView


def test_f1_lookup_opens_dialog_and_sets_tipo(monkeypatch):
    v = ArticulosView()

    # Ensure we are in 'editing' mode
    if hasattr(v.ui, 'botGuardar'):
        v.ui.botGuardar.setEnabled(True)

    # Prepare fake result from DBConsultaView.select_from_data
    fake_selected = {'id': 123, 'codigo': 'T-TEST', 'descripcion': 'Tipo Test'}

    def fake_select_from_data(parent, data, headers, campos=None, titulo=None):
        return fake_selected, None

    monkeypatch.setattr(DBConsultaView, 'select_from_data', staticmethod(fake_select_from_data))

    # Ensure controller.current_article exists so set_tipo_from_lookup can write to it
    v.controller.current_article = {'id': 1}

    # Call the handler directly (simulates pressing F1)
    v._on_buscar_tipo_clicked()

    # Verify UI fields and controller were updated
    assert v.controller.current_article.get('id_tipo') == 123
    assert v.controller.current_article.get('codigo_tipo') == 'T-TEST'
    assert v.controller.current_article.get('descripcion_tipo') == 'Tipo Test'

    if hasattr(v.ui, 'txtCodigoTipo'):
        assert v.ui.txtCodigoTipo.text() == 'T-TEST'
    if hasattr(v.ui, 'txtDescripcionTipo'):
        assert v.ui.txtDescripcionTipo.text() == 'Tipo Test'
