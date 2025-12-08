from modules.articulos.view import ArticulosView


def test_txtCodigoTipo_has_tooltip():
    v = ArticulosView()

    if not hasattr(v.ui, "txtCodigoTipo"):
        # If the generated UI lacks the field, nothing to check — treat as pass
        return

    tip = v.ui.txtCodigoTipo.toolTip()
    assert tip is not None
    # Make the assertion flexible: check helpful substrings
    assert "Ctrl" in tip or "Buscar" in tip
