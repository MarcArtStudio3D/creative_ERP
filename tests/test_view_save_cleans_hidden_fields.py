from modules.articulos.view import ArticulosView


def test_save_cleans_hidden_fields_when_tipo_false(monkeypatch):
    v = ArticulosView()

    # Ensure UI fields are present
    if not hasattr(v.ui, 'txtcodigo_barras'):
        return

    # Set UI values
    v.ui.txtcodigo_barras.setText('EAN123')
    v.ui.txtcodigo_fabricante.setText('FAB456')

    # current article has tipo flags false
    v.controller.current_article = {'id': 1, 'id_tipo': 10, 'tipo_requiereEAN': False, 'tipo_proveedor': False}

    payload = v._save_form_to_article()

    assert 'codigo_barras' not in payload
    assert 'codigo_fabricante' not in payload


def test_save_keeps_fields_when_tipo_true(monkeypatch):
    v = ArticulosView()

    if not hasattr(v.ui, 'txtcodigo_barras'):
        return

    v.ui.txtcodigo_barras.setText('EAN999')
    v.ui.txtcodigo_fabricante.setText('FAB999')

    v.controller.current_article = {'id': 1, 'id_tipo': 10, 'tipo_requiereEAN': True, 'tipo_proveedor': True}

    payload = v._save_form_to_article()

    assert 'codigo_barras' in payload and payload['codigo_barras'] == 'EAN999'
    assert 'codigo_fabricante' in payload and payload['codigo_fabricante'] == 'FAB999'
