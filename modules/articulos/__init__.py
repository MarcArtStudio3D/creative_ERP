"""
Módulo de Artículos - Migrado a SQL directo
"""

from .controller import ArticuloController
from .divisiones_controller import DivisionesController
from .divisiones_repository import DivisionesRepository
from .divisiones_view import DivisionesView
from .repository_sql import ArticuloRepository

__all__ = [
    "ArticuloRepository",
    "ArticuloController",
    "DivisionesRepository",
    "DivisionesController",
    "DivisionesView",
]
