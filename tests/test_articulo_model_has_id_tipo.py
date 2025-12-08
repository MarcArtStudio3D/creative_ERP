from modules.articulos import models


def test_articulo_model_has_id_tipo():
    assert hasattr(
        models.Articulo, "id_tipo"
    ), "El modelo Articulo debe tener el atributo id_tipo"
