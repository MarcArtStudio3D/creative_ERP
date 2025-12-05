from modules.articulos.repository import ArticuloRepository


def test_repository_exposes_articulo_tipo_methods():
    repo = ArticuloRepository()
    for name in ("get_articulo_tipos", "get_articulo_tipo", "get_articulo_tipo_por_codigo"):
        assert hasattr(repo, name), f"ArticuloRepository debe exponer {name}"
