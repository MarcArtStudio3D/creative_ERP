"""Módulo de integración para 'tarifas_maestras'.

Este paquete actúa como punto de entrada para la vista que usa la UI 'Tarifas maestras'
y reexporta la vista principal para que se pueda importar desde
`modules.tarifas_maestras.view.TarifasMaestrasView`.
"""

from .view import TarifasMaestrasView

__all__ = ["TarifasMaestrasView"]
