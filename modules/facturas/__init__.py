"""
Módulo de Facturas - Ejemplo de estructura modular.

Cada módulo sigue esta estructura:
- models.py: Modelos de datos
- repository.py: Acceso a base de datos
- views.py: Interfaces gráficas
- controller.py: Lógica de negocio
- __init__.py: Exportaciones públicas
"""

# Este archivo define qué expone el módulo al resto del sistema

from .models import Factura, LineaFactura, TipoFactura
from .repository import FacturaRepository
# from .controller import FacturaController
# from .views import FacturaView, FacturaListView

__all__ = [
    'Factura',
    'LineaFactura',
    'TipoFactura',
    'FacturaRepository',
    # 'FacturaController',
    # 'FacturaView',
    # 'FacturaListView',
]

# Metadatos del módulo
MODULE_INFO = {
    'id': 'facturas',
    'version': '1.0.0',
    'requires': ['clientes', 'articulos'],  # Dependencias
    'description': 'Gestión de facturas de venta'
}
