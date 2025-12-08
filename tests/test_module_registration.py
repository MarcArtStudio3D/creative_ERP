from core.module_manager import AVAILABLE_MODULES, ModuleCategory, ModuleManager


def test_tarifas_maestras_registered():
    assert "tarifas_maestras" in AVAILABLE_MODULES
    mod = AVAILABLE_MODULES["tarifas_maestras"]
    assert mod.category == ModuleCategory.ALMACEN
    # ModuleManager should find it
    mm = ModuleManager()
    assert mm.get_module("tarifas_maestras") is mod
