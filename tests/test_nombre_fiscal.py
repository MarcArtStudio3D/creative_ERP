from modules.clientes.view_full import format_nombre_fiscal


def test_format_nombre_fiscal_all_parts():
    assert format_nombre_fiscal('Garcia', 'Lopez', 'Juan') == 'GARCIA LOPEZ JUAN'


def test_format_nombre_fiscal_missing_second_surname():
    assert format_nombre_fiscal('Garcia', '', 'Juan') == 'GARCIA JUAN'


def test_format_nombre_fiscal_only_name():
    assert format_nombre_fiscal('', '', 'Juan') == 'JUAN'


def test_format_nombre_fiscal_empty_all():
    assert format_nombre_fiscal('', '', '') == ''
