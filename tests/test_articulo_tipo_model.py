from modules.articulos import models


def test_articulo_tipo_model_defined():
    """Smoke-test: el modelo ArticuloTipo está definido en modules.articulos.models"""
    assert hasattr(
        models, "ArticuloTipo"
    ), "ArticuloTipo debe estar definido en modules.articulos.models"
