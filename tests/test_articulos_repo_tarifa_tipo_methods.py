from modules.articulos.repository import ArticuloRepository


def test_repository_exposes_tarifa_tipo_methods():
    repo = ArticuloRepository()
    for name in ("get_tarifa_tipos", "get_tarifa_tipo", "create_tarifa_tipo", "update_tarifa_tipo", "delete_tarifa_tipo"):
        assert hasattr(repo, name), f"ArticuloRepository should expose {name}"
        assert callable(getattr(repo, name)), f"{name} should be callable"
