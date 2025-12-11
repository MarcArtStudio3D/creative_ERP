"""
Módulo de Clientes
"""

from . import models
from .controller import ClientesController
from .repository_sql import ClienteRepository  # Usando SQL directo (sin ORM)
from .view import ClientesView

__all__ = [
    "ClienteRepository",
    "ClientesController",
    "ClientesView",
    "models",
]
