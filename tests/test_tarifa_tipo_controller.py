from modules.articulos.tarifa_tipo_controller import TarifaTipoController


def test_tarifa_tipo_controller_methods_exist():
    ctrl = TarifaTipoController()
    for name in ("list_all", "load_by_id", "create", "update", "delete", "next", "prev"):
        assert hasattr(ctrl, name), f"TarifaTipoController should have method {name}"
        assert callable(getattr(ctrl, name))
