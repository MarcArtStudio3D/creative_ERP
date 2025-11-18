from modules.clientes.view_full import ClientesViewFull


def test_is_valid_dni_valid_and_invalid():
    # '00000000T' -> T maps to 0 => valid
    assert ClientesViewFull._is_valid_dni(None, '00000000T') is True
    # Change last letter, must be invalid
    assert ClientesViewFull._is_valid_dni(None, '00000000A') is False


def test_is_valid_iban_valid_and_invalid():
    # Sample Spanish IBAN: ES9121000418450200051332 (valid)
    assert ClientesViewFull._is_valid_iban(None, 'ES91 2100 0418 4502 0005 1332') is True
    # Simple invalid (wrong checksum)
    assert ClientesViewFull._is_valid_iban(None, 'ES00 0000 0000 0000 0000 0000') is False
