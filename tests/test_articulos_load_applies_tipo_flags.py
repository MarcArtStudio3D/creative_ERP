from modules.articulos.view import ArticulosView


def test_load_article_applies_tipo_flags(monkeypatch):
    v = ArticulosView()

    # Ensure UI elements are present
    if not hasattr(v.ui, 'txtcodigo_barras'):
        return

    # Make controller return a current article with id_tipo
    article = {'id': 42, 'id_tipo': 100, 'codigo': 'A1', 'descripcion_reducida': 'Art 1'}
    monkeypatch.setattr(v.controller, 'get_current_article', lambda: article)

    # Fake repository lookup for tipo
    fake_tipo = {'id': 100, 'codigo': 'T100', 'descripcion': 'Tipo 100', 'requiereEAN': True, 'proveedor': False}
    monkeypatch.setattr(v.controller.repository, 'get_articulo_tipo', lambda tid: fake_tipo if tid == 100 else None)

    # Call load
    v._load_form_from_article()

    # Expectations
    assert v.ui.txtcodigo_barras.isVisible() is True
    assert v.ui.label_3.isVisible() is True
    assert v.ui.txtcodigo_fabricante.isVisible() is False
    assert v.ui.label_4.isVisible() is False


def test_load_article_clears_flags_when_no_tipo(monkeypatch):
    v = ArticulosView()
    if not hasattr(v.ui, 'txtcodigo_barras'):
        return

    # Article with no tipo
    article = {'id': 43, 'codigo': 'A2'}
    monkeypatch.setattr(v.controller, 'get_current_article', lambda: article)
    v._load_form_from_article()

    assert v.ui.txtcodigo_barras.isVisible() is False
    assert v.ui.txtcodigo_fabricante.isVisible() is False
