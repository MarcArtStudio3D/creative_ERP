import pytest
from PySide6.QtWidgets import QApplication, QTableWidgetItem
from PySide6.QtCore import QModelIndex
from modules.articulos.view_tarifas_base import TarifasBaseView


@pytest.fixture(scope='module', autouse=True)
def qapp():
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    yield app


def test_emit_doubleclicked_signal_triggers_handler(qapp):
    v = TarifasBaseView()

    sample = {'id': 222, 'codigo': 'T3', 'nombre': 'Tarifa prueba', 'descripcion': 'Demo'}
    v.controller.index_list = [sample]

    def fake_load_by_id(tipo_id):
        if int(tipo_id) == 222:
            v.controller.current = sample
            return True
        return False

    v.controller.load_by_id = fake_load_by_id

    v.ui.stackedWidget.setCurrentIndex(1)
    v.ui.tableWidget.setRowCount(1)
    v.ui.tableWidget.setItem(0, 0, QTableWidgetItem(str(sample['id'])))
    v.ui.tableWidget.setItem(0, 1, QTableWidgetItem(sample['codigo']))
    v.ui.tableWidget.setItem(0, 2, QTableWidgetItem(sample['nombre']))

    # Emit the QModelIndex-based doubleClicked signal
    idx = v.ui.tableWidget.model().index(0, 1)
    v.ui.tableWidget.doubleClicked.emit(idx)

    assert v.ui.stackedWidget.currentIndex() == 0
    assert v.controller.current and v.controller.current.get('id') == 222
*** End Patch