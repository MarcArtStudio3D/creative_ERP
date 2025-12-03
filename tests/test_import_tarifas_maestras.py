def test_import_tarifas_maestras_view():
    # Ensure the application can import the view the main window expects
    from modules.tarifas_maestras.view import TarifasMaestrasView

    assert callable(TarifasMaestrasView)
