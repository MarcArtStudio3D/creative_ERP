from modules.articulos.view import ArticulosView


def test_codigo_tipo_entered_sets_visibility(monkeypatch):
    v = ArticulosView()

    if not hasattr(v.ui, 'txtCodigoTipo'):
        return

    # Enable editing
    if hasattr(v.ui, 'botGuardar'):
        v.ui.botGuardar.setEnabled(True)

    # Prepare a tipo record with flags
    fake_tipo = {'id': 999, 'codigo': 'T-CODE', 'descripcion': 'Tipo X', 'requiereEAN': True, 'proveedor': True}

    # Replace controller method
    monkeypatch.setattr(v.controller, 'get_tipo_by_codigo', lambda c: fake_tipo)

    # Put code into the textbox
    v.ui.txtCodigoTipo.setText('T-CODE')

    # Call handler
    v._on_codigo_tipo_entered()

    # Check that UI fields reflect tipo flags
    if hasattr(v.ui, 'txtcodigo_barras'):
        assert v.ui.txtcodigo_barras.isVisible() is True
    if hasattr(v.ui, 'txtcodigo_fabricante'):
        assert v.ui.txtcodigo_fabricante.isVisible() is True

    # Also check controller flags were stored
    assert v.controller.current_article.get('tipo_requiereEAN') is True
    assert v.controller.current_article.get('tipo_proveedor') is True


def test_codigo_tipo_empty_hides_flags():
    v = ArticulosView()
    if not hasattr(v.ui, 'txtCodigoTipo'):
        return

    if hasattr(v.ui, 'botGuardar'):
        v.ui.botGuardar.setEnabled(True)

    v.ui.txtCodigoTipo.setText('')

    v._on_codigo_tipo_entered()

    # Verify things hidden
    if hasattr(v.ui, 'txtcodigo_barras'):
        assert v.ui.txtcodigo_barras.isVisible() is False
    if hasattr(v.ui, 'txtcodigo_fabricante'):
        assert v.ui.txtcodigo_fabricante.isVisible() is False
*** End Patch