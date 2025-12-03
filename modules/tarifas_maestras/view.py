"""View adapter that exposes TarifasMaestrasView expected by the rest of the app.

It reuses the already implemented `TarifasBaseView` from `modules.articulos.view_tarifas_base` so
we don't duplicate logic.
"""
from PySide6.QtWidgets import QDialog

from modules.articulos.view_tarifas_base import TarifasBaseView


class TarifasMaestrasView(TarifasBaseView, QDialog):
    """Thin adapter so main_window can import modules.tarifas_maestras.view.TarifasMaestrasView.

    Inherits from TarifasBaseView (which is a QDialog already wired) — this class exists to match
    the expected import path and allow future customizations specific to tarifas_maestras.
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
