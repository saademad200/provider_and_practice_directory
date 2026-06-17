from __future__ import annotations

import re
from typing import Any

from bs4 import BeautifulSoup

from .data import normalize_address, normalize_phone, normalize_text


SPECIALTIES = [
    "family medicine",
    "cardiology",
    "dermatology",
    "pediatrics",
    "orthopedics",
    "neurology",
]


PHONE_RE = re.compile(r"(?:\+?1[\s.-]?)?\(?([2-9]\d{2})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})")
ADDRESS_RE = re.compile(
    r"\b(\d{2,6}\s+[A-Za-z0-9 .'-]+?\s+(?:St|Street|Ave|Avenue|Rd|Road|Blvd|Boulevard|Dr|Drive)\.?"
    r"(?:,\s*(?:Suite|Ste|Unit|#)\s*\w+)?(?:,\s*(?:FL|Florida))?)\b",
    flags=re.I,
)


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return " ".join(soup.get_text(" ").split())


def extract_provider_page(html: str) -> dict[str, Any]:
    text = html_to_text(html)
    text_norm = normalize_text(text)

    phones = set()
    for match in PHONE_RE.finditer(text):
        context = text[max(0, match.start() - 24) : match.start()].lower()
        if "fax" in context:
            continue
        phones.add(normalize_phone("".join(match.groups())))
    phones = sorted(phones)
    addresses = sorted({normalize_address(match.group(1)) for match in ADDRESS_RE.finditer(text)})
    specialties = sorted({specialty for specialty in SPECIALTIES if specialty in text_norm})

    accepting_new_patients = None
    if any(phrase in text_norm for phrase in ["accepting new patients", "welcoming new patients"]):
        accepting_new_patients = "true"
    if any(phrase in text_norm for phrase in ["not accepting new patients", "closed to new patients"]):
        accepting_new_patients = "false"
    if any(phrase in text_norm for phrase in ["new patient appointments unavailable", "not taking new patients"]):
        accepting_new_patients = "false"

    return {
        "phones": phones,
        "addresses": addresses,
        "specialties": specialties,
        "accepting_new_patients": accepting_new_patients,
        "text_length": len(text),
    }


def score_extraction(predictions: list[dict[str, Any]], gold: list[dict[str, Any]]) -> dict[str, Any]:
    fields = ["phones", "addresses", "specialties", "accepting_new_patients"]
    rows = []
    for field in fields:
        tp = fp = fn = 0
        for pred, truth in zip(predictions, gold):
            if field == "accepting_new_patients":
                pred_set = {pred.get(field)} if pred.get(field) is not None else set()
                truth_set = {truth.get(field)} if truth.get(field) is not None else set()
            else:
                pred_set = set(pred.get(field, []))
                truth_set = set(truth.get(field, []))
            tp += len(pred_set & truth_set)
            fp += len(pred_set - truth_set)
            fn += len(truth_set - pred_set)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        rows.append(
            {
                "field": field,
                "tp": tp,
                "fp": fp,
                "fn": fn,
                "precision": round(precision, 6),
                "recall": round(recall, 6),
                "f1": round(f1, 6),
            }
        )
    macro_f1 = sum(row["f1"] for row in rows) / len(rows)
    return {"macro_f1": round(macro_f1, 6), "fields": rows}
