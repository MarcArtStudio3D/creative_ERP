from modules.articulos.view import ArticulosView


def test_save_form_includes_id_tipo_when_present():
    v = ArticulosView()

    # Simulate that controller has loaded an article and it contains id_tipo
    v.controller.current_article = {"id": 123, "id_tipo": 77}

    # Make sure required fields exist so _save_form_to_article doesn't error
    if hasattr(v.ui, "txtcodigo"):
        v.ui.txtcodigo.setText("X001")
    if hasattr(v.ui, "txtdescripcionResumida"):
        v.ui.txtdescripcionResumida.setText("Nombre de prueba")

    payload = v._save_form_to_article()
    assert "id_tipo" in payload and payload["id_tipo"] == 77
