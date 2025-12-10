from . import models
from .controller import ArticuloController
from .divisiones_controller import DivisionesController
from .divisiones_repository import DivisionesRepository
from .divisiones_view import DivisionesView

# Forzar implementación Peewee
from .peewee_repository import ArticuloRepository

__all__ = [
    "ArticuloRepository",
    "ArticuloController",
    "DivisionesRepository",
    "DivisionesController",
    "DivisionesView",
    "models",
]
