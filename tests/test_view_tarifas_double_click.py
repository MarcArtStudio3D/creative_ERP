import pytest
from PySide6.QtWidgets import QApplication, QTableWidgetItem

from modules.articulos.view_tarifas_base import TarifasBaseView


@pytest.fixture(scope="module", autouse=True)
def qapp():
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    yield app


def test_double_click_switches_to_edit(qapp):
    v = TarifasBaseView()

    # Prepare fake controller data and override controller methods
    sample = {
        "id": 123,
        "codigo": "T2",
        "nombre": "Tarifa general",
        "descripcion": "Demo",
    }

    # list_all returns a list with our sample (simulate cached list)
    v.controller.index_list = [sample]

    # load_by_id should set current and return True when asked for the sample id
    def fake_load_by_id(tipo_id):
        if int(tipo_id) == 123:
            v.controller.current = sample
            return True
        return False

    v.controller.load_by_id = fake_load_by_id

    # Populate table with one row having id in column 0
    v.ui.stackedWidget.setCurrentIndex(1)
    v.ui.tableWidget.setRowCount(1)
    v.ui.tableWidget.setItem(0, 0, QTableWidgetItem(str(sample["id"])))
    v.ui.tableWidget.setItem(0, 1, QTableWidgetItem(sample["codigo"]))
    v.ui.tableWidget.setItem(0, 2, QTableWidgetItem(sample["nombre"]))

    # simulate double click on the row
    v._on_table_double_click(0, 1)

    assert v.ui.stackedWidget.currentIndex() == 0
    assert v.controller.current and v.controller.current.get("id") == 123
    assert v.is_new is False
