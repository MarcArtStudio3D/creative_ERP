from modules.articulos import models


def test_tarifa_tipo_model_defined():
    """A small smoke-test to ensure the TarifaTipo model exists and maps to the expected table name."""
    assert hasattr(
        models, "TarifaTipo"
    ), "TarifaTipo model should be defined in modules.articulos.models"
    cls = models.TarifaTipo
    assert getattr(cls, "__tablename__", None) == "tarifas_tipo"
