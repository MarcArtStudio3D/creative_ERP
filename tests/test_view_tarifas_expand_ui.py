import pytest
from PySide6.QtWidgets import QApplication, QSizePolicy

from modules.articulos.view_tarifas_base import TarifasBaseView


@pytest.fixture(scope='module', autouse=True)
def qapp():
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    yield app


def test_tarifas_form_and_table_expandable():
    v = TarifasBaseView()

    # form container should be expanding
    assert hasattr(v.ui, 'gridLayoutWidget')
    policy = v.ui.gridLayoutWidget.sizePolicy()
    assert policy.horizontalPolicy() in (QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
    assert policy.verticalPolicy() in (QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

    # description should expand vertically
    assert hasattr(v.ui, 'plainTextEdit')
    p = v.ui.plainTextEdit.sizePolicy()
    assert p.verticalPolicy() in (QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

    # table should be expandable
    assert hasattr(v.ui, 'tableWidget')
    tpol = v.ui.tableWidget.sizePolicy()
    assert tpol.horizontalPolicy() in (QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
    assert tpol.verticalPolicy() in (QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

    # stackedWidget should have been added to a layout with expanding policy
    assert hasattr(v.ui, 'stackedWidget')
    sp = v.ui.stackedWidget.sizePolicy()
    assert sp.horizontalPolicy() in (QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
    assert sp.verticalPolicy() in (QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

    # The view itself should be expanding
    vp = v.sizePolicy()
    assert vp.horizontalPolicy() in (QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
    assert vp.verticalPolicy() in (QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

    # Verify pages have proper layouts
    assert v.ui.page.layout() is not None, "Page 1 should have a layout"
    assert v.ui.page_2.layout() is not None, "Page 2 should have a layout"
