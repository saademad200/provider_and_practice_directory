from src.npi import synthetic_npi, valid_npi


def test_synthetic_npis_validate():
    for i in range(25):
        assert valid_npi(synthetic_npi(i))


def test_invalid_npi_fails():
    assert not valid_npi("1999999995")
    assert not valid_npi("12345")
    assert not valid_npi("abcdefghij")
