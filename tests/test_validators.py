from modules.clientes.view import ClientesView


def test_dni_validation():
    # Valid DNI
    assert ClientesView._is_valid_dni(None, '00000000T') is True
    # Invalid DNI
    assert ClientesView._is_valid_dni(None, '00000000A') is False


def test_iban_validation():
    # Valid IBAN
    assert ClientesView._is_valid_iban(None, 'ES91 2100 0418 4502 0005 1332') is True
    # Invalid IBAN
    assert ClientesView._is_valid_iban(None, 'ES00 0000 0000 0000 0000 0000') is False
