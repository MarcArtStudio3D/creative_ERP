from modules.articulos.controller import ArticuloController


def test_controller_exposes_tipo_methods():
    c = ArticuloController()
    assert hasattr(c, 'get_tipos_data')
    assert hasattr(c, 'get_tipo_by_codigo')
    assert hasattr(c, 'set_tipo_from_lookup')

    # Ensure set_tipo_from_lookup stores values on current_article
    c.current_article = {'id': 1}
    ok = c.set_tipo_from_lookup(10, 'X1', 'Tipo X1')
    assert ok
    assert c.current_article.get('id_tipo') == 10
    assert c.current_article.get('codigo_tipo') == 'X1'
    assert c.current_article.get('descripcion_tipo') == 'Tipo X1'
