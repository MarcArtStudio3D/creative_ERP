import xml.etree.ElementTree as ET
from pathlib import Path


def test_frmarticulos_ui_listwidget_properties():
    ui_path = Path('app/ui/Almacen/frmarticulos.ui')
    assert ui_path.exists(), 'UI file should exist'

    tree = ET.parse(ui_path)
    root = tree.getroot()

    # Find the QListWidget with name 'listWidget'
    list_widget = None
    for widget in root.iter('widget'):
        if widget.attrib.get('class') == 'QListWidget' and widget.attrib.get('name') == 'listWidget':
            list_widget = widget
            break

    assert list_widget is not None, 'listWidget widget present in UI'

    # Check some expected properties are present and set to palette-friendly values
    properties = {p.find('string').text if p.find('string') is not None else p.find('number').text if p.find('number') is not None else None: p for p in list_widget.findall('property')}

    # Icon size should be large enough to feel like a swatch (44x44)
    icon = list_widget.find("property[@name='iconSize']/size")
    assert icon is not None
    w = int(icon.find('width').text)
    h = int(icon.find('height').text)
    assert w == 44 and h == 44

    # Grid size should be generous so swatches appear clear (56x56)
    grid = list_widget.find("property[@name='gridSize']/size")
    assert grid is not None
    gw = int(grid.find('width').text)
    gh = int(grid.find('height').text)
    assert gw == 56 and gh == 56

    # Spacing property present and small
    spacing = list_widget.find("property[@name='spacing']")
    assert spacing is not None and int(spacing.find('number').text) >= 6


def test_generated_ui_file_reflects_palette():
    pyf = Path('modules/articulos/ui_frmarticulos.py')
    assert pyf.exists()
    content = pyf.read_text(encoding='utf8')

    assert 'setGridSize(QSize(56, 56))' in content
    assert 'setIconSize(QSize(44, 44))' in content
    assert 'setStyleSheet' in content
