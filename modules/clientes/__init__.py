"""
Módulo de Clientes - Migrado a SQL directo
"""

from .controller import ClientesController
from .repository_sql import ClienteRepository
from .view import ClientesView

__all__ = [
    "ClienteRepository",
    "ClientesController",
    "ClientesView",
]
