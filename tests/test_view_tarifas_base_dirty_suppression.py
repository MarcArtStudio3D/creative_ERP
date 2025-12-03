
import pytest
from PySide6.QtWidgets import QApplication

from modules.articulos.view_tarifas_base import TarifasBaseView


@pytest.fixture(scope="module", autouse=True)
def qapp():
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    yield app


def test_fill_form_does_not_mark_search_dirty():
    v = TarifasBaseView()

    # Simulate user previously having marked fields dirty
    v._search_dirty = True

    v._fill_form({'codigo': 'C1', 'nombre': 'Name', 'moneda': 'EUR', 'descripcion': 'desc'})

    # After programmatic fill, the search must be considered clean
    assert v._search_dirty is False


def test_load_table_does_not_mark_search_dirty():
    v = TarifasBaseView()
    v._search_dirty = True

    # Ensure table load clears dirty flag, we rely on controller.list_all being safe to call
    v._load_table([])
    assert v._search_dirty is False
