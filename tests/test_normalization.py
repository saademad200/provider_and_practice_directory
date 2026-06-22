from src.data import normalize_address, normalize_phone, normalize_value


def test_phone_normalization():
    assert normalize_phone("+1 (555) 123-4567") == "555-123-4567"


def test_address_normalization_suite_and_suffix():
    text = normalize_address("100 Main St., Ste 4, FL")
    assert "main street" in text
    assert "suite 4" in text
    assert "florida" in text


def test_specialty_normalization():
    assert normalize_value("specialty", "Cardiology") == "cardiology"
