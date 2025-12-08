from modules.articulos.view import ArticulosView


class _DummyWidget:
    def __init__(self, enabled=False):
        self._enabled = enabled

    def setEnabled(self, v: bool):
        self._enabled = bool(v)

    def isEnabled(self):
        return self._enabled

    def setVisible(self, v: bool):
        self._visible = bool(v)


def test_promo_dates_respect_edit_mode():
    """Los campos de fecha solo deben ser editables si el checkbox está marcado y estamos en modo edición."""

    # Build a fake view that holds only the UI attributes we need
    class FakeView:
        def __init__(self):
            self.ui = type("u", (), {})()
            self.ui.txtOferta_Fecha_ini = _DummyWidget(False)
            self.ui.txtOferta_Fecha_fin = _DummyWidget(False)
            self.ui.botGuardar = _DummyWidget(False)  # locked by default
            self.ui.lbl_en_promocion = _DummyWidget(False)

    view = FakeView()

    # Bind the original method to our fake instance
    handler = ArticulosView._on_articulo_promocionado_changed.__get__(view, FakeView)

    # Initially locked -> even if checkbox checked, date fields remain disabled
    handler(True)
    assert not view.ui.txtOferta_Fecha_ini.isEnabled()
    assert not view.ui.txtOferta_Fecha_fin.isEnabled()

    # Now enable edit mode (botGuardar enabled) and check again
    view.ui.botGuardar.setEnabled(True)
    handler(True)
    assert view.ui.txtOferta_Fecha_ini.isEnabled()
    assert view.ui.txtOferta_Fecha_fin.isEnabled()

    # Uncheck while in edit mode -> dates disabled again
    handler(False)
    assert not view.ui.txtOferta_Fecha_ini.isEnabled()
    assert not view.ui.txtOferta_Fecha_fin.isEnabled()
