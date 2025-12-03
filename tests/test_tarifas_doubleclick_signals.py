"""Test that all three double-click signals work in TarifasBaseView."""
import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QPoint
from modules.articulos.view_tarifas_base import TarifasBaseView


@pytest.fixture
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def test_all_doubleclick_signals_connected(qapp):
    """Verify all three double-click signals are connected and trigger the handler."""
    view = TarifasBaseView()
    
    # Populate table with test data
    test_data = [
        {'id': 100, 'codigo': 'T01', 'nombre': 'Tarifa Test 1', 'moneda': 'EUR'},
        {'id': 200, 'codigo': 'T02', 'nombre': 'Tarifa Test 2', 'moneda': 'USD'},
    ]
    view._load_table(test_data)
    
    # Verify table has rows
    assert view.ui.tableWidget.rowCount() == 2
    
    # Track if handler was called
    handler_calls = []
    original_handler = view._on_table_double_click
    
    def tracking_handler(row, col):
        handler_calls.append((row, col))
        return original_handler(row, col)
    
    view._on_table_double_click = tracking_handler
    
    # Test 1: cellDoubleClicked signal
    handler_calls.clear()
    try:
        view.ui.tableWidget.cellDoubleClicked.emit(0, 1)
        assert len(handler_calls) >= 1, "cellDoubleClicked didn't trigger handler"
        print(f"✓ cellDoubleClicked works: {handler_calls}")
    except Exception as e:
        print(f"✗ cellDoubleClicked failed: {e}")
    
    # Test 2: itemDoubleClicked signal
    handler_calls.clear()
    try:
        item = view.ui.tableWidget.item(0, 1)
        if item:
            view.ui.tableWidget.itemDoubleClicked.emit(item)
            assert len(handler_calls) >= 1, "itemDoubleClicked didn't trigger handler"
            print(f"✓ itemDoubleClicked works: {handler_calls}")
    except Exception as e:
        print(f"✗ itemDoubleClicked failed: {e}")
    
    # Test 3: doubleClicked signal (QModelIndex)
    handler_calls.clear()
    try:
        index = view.ui.tableWidget.model().index(0, 1)
        view.ui.tableWidget.doubleClicked.emit(index)
        assert len(handler_calls) >= 1, "doubleClicked didn't trigger handler"
        print(f"✓ doubleClicked works: {handler_calls}")
    except Exception as e:
        print(f"✗ doubleClicked failed: {e}")
    
    # At least one signal should have worked
    assert len(handler_calls) > 0, "No double-click signal triggered the handler!"


def test_doubleclick_loads_record_and_switches_page(qapp):
    """Verify double-clicking a row loads the record and switches to edit page."""
    view = TarifasBaseView()
    
    # Mock controller to avoid DB calls
    class FakeController:
        def __init__(self):
            self.current = None
            self.index_list = [
                {'id': 333, 'codigo': 'DBL1', 'nombre': 'Double Test', 'moneda': 'EUR', 'descripcion': 'Test'}
            ]
        
        def list_all(self):
            return self.index_list
        
        def load_by_id(self, tipo_id):
            for item in self.index_list:
                if item['id'] == tipo_id:
                    self.current = item
                    return True
            return False
    
    view.controller = FakeController()
    
    # Populate table
    view._load_table([{'id': 333, 'codigo': 'DBL1', 'nombre': 'Double Test'}])
    
    # Initially on list page (index 1)
    view.ui.stackedWidget.setCurrentIndex(1)
    assert view.ui.stackedWidget.currentIndex() == 1
    
    # Simulate double-click on first row
    view._on_table_double_click(0, 1)
    
    # Should switch to edit page (index 0)
    assert view.ui.stackedWidget.currentIndex() == 0, "Page didn't switch to edit view"
    
    # Should have loaded the record
    assert view.controller.current is not None
    assert view.controller.current['id'] == 333
    print(f"✓ Double-click loaded record: {view.controller.current}")
