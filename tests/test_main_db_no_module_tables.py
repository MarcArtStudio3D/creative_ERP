from core.db import set_current_database, get_engine
from sqlalchemy import inspect


def test_main_db_has_no_module_tables():
    """Fails if any module-specific tables are present in `main`.

    This prevents accidental contamination of the global `main` DB with module tables.
    The list includes the most common module tables — extend if you add new module tables.
    """
    # Define module-specific tables we must not see in `main`
    forbidden = {
        'articulos', 'articulos_imagenes', 'articulos_ofertas', 'articulos_ofertas',
        'clientes', 'clientes_tipos', 'deudas_clientes', 'direcciones_alternativas',
        'familias', 'subfamilias', 'tarifas', 'kits', 'proveedores_frecuentes',
        'historial_clientes', 'estadisticas_clientes_mes', 'acum_articulos'
    }

    set_current_database('main')
    engine = get_engine()
    inspector = inspect(engine)

    existing = set(inspector.get_table_names())

    found = existing.intersection(forbidden)
    assert not found, (
        "The main database contains module tables which should NOT be there: "
        f"{sorted(found)}. Please remove them or fix the deployment/migration targets."
    )
