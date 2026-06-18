from __future__ import annotations

import re


NPI_RE = re.compile(r"^\d{10}$")


def luhn_check_digit(payload: str) -> int:
    total = 0
    for idx, char in enumerate(payload[::-1]):
        digit = int(char)
        if idx % 2 == 0:
            digit *= 2
            total += digit - 9 if digit > 9 else digit
        else:
            total += digit
    return (10 - total % 10) % 10


def valid_npi(npi: object) -> bool:
    text = str(npi)
    if not NPI_RE.match(text):
        return False
    return luhn_check_digit("80840" + text[:9]) == int(text[-1])


def synthetic_npi(sequence: int) -> str:
    prefix = f"199900{sequence:03d}"
    return prefix + str(luhn_check_digit("80840" + prefix))
