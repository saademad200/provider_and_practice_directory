from __future__ import annotations

SPECIALTY_ALIASES = {
    "family practice": "family medicine",
    "general practice": "family medicine",
    "primary care": "family medicine",
    "internal medicine": "family medicine",
    "cardiovascular disease": "cardiology",
    "interventional cardiology": "cardiology",
    "pediatric medicine": "pediatrics",
    "paediatrics": "pediatrics",
    "orthopaedic surgery": "orthopedics",
    "orthopedic surgery": "orthopedics",
    "orthopaedics": "orthopedics",
    "dermatologic surgery": "dermatology",
    "neurological surgery": "neurology",
    "clinical neurophysiology": "neurology",
}


def _normalize_text(value: object) -> str:
    return " ".join(str(value).lower().replace(",", " ").replace(".", " ").split())


def normalize_specialty(value: object) -> str:
    text = _normalize_text(value)
    return SPECIALTY_ALIASES.get(text, text)
