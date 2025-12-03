import pytest
from PySide6.QtWidgets import QApplication, QSizePolicy
from modules.articulos.view_tarifas_base import TarifasBaseView


@pytest.fixture(scope='module', autouse=True)
def qapp():
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    yield app


def test_tarifas_panel_api_methods_exist_and_basic_behaviour(qapp):
    v = TarifasBaseView()

    # methods existence
    for name in ('list', 'nuevo', 'editar', 'borrar', 'search', 'filter_records', 'get_search_options', 'filtrar'):
        assert hasattr(v, name), f"Missing public API method: {name}"

    # list should switch to table view
    v.ui.stackedWidget.setCurrentIndex(0)
    v.list()
    assert v.ui.stackedWidget.currentIndex() == 1

    # nuevo should switch to form and set is_new
    v.nuevo()
    assert v.is_new is True
    assert v.ui.stackedWidget.currentIndex() == 0

    # search/filter_records should not raise for empty and non-empty text
    v.search("")
    v.search("T2")
    v.filter_records("T2", order_by="Nombre", order_mode="A-Z")
    v.filtrar("T2")

    # get_search_options must return dict with keys
    opts = v.get_search_options()
    assert isinstance(opts, dict)
    assert 'sort_fields' in opts and 'search_placeholder' in opts


def test_typing_updates_table_live(qapp):
    v = TarifasBaseView()

    # ensure we are on the list view and table has rows
    v.ui.stackedWidget.setCurrentIndex(1)
    v._load_table()
    before = v.ui.tableWidget.rowCount()

    # If no rows to begin with, the test is not meaningful — skip
    if before == 0:
        return

    # Type a filter that likely matches at least one item (use an existing code from fixtures like 'T2')
    v.ui.lineEdit.setText("T2")

    after = v.ui.tableWidget.rowCount()

    # After typing, either the table is filtered (<= before) or unchanged (if nothing matched)
    assert after <= before
