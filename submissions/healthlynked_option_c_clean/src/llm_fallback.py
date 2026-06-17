from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from .data import normalize_address, normalize_phone, normalize_value
from .web_extract import extract_provider_page


BEDROCK_EXTRACTION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["provider_name", "fields", "confidence", "evidence_spans", "warnings"],
    "properties": {
        "provider_name": {"type": ["string", "null"]},
        "fields": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "phone": {"type": ["string", "null"]},
                "address": {"type": ["string", "null"]},
                "specialty": {"type": ["string", "null"]},
                "accepting_new_patients": {"type": ["boolean", "null"]},
                "provider_status": {"type": ["string", "null"]},
            },
        },
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "evidence_spans": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["field", "text"],
                "properties": {
                    "field": {"type": "string"},
                    "text": {"type": "string"},
                },
            },
        },
        "warnings": {"type": "array", "items": {"type": "string"}},
    },
}


@dataclass(frozen=True)
class LLMGateDecision:
    should_call: bool
    reasons: tuple[str, ...]
    deterministic_fields_found: int
    estimated_input_tokens: int
    estimated_cost_usd: float


def estimate_tokens(text: str) -> int:
    return max(1, len(text.split()) * 4 // 3)


def should_call_llm(html: str, max_cost_usd: float = 0.002) -> LLMGateDecision:
    deterministic = extract_provider_page(html)
    found = 0
    found += bool(deterministic.get("phones"))
    found += bool(deterministic.get("addresses"))
    found += bool(deterministic.get("specialties"))
    found += deterministic.get("accepting_new_patients") is not None
    text_length = int(deterministic.get("text_length", 0))
    tokens = estimate_tokens("x " * max(1, text_length // 5))
    estimated_cost = round(tokens * 0.0000008 + 450 * 0.0000024, 6)

    reasons: list[str] = []
    if found < 2:
        reasons.append("deterministic_extraction_sparse")
    if text_length > 3500:
        reasons.append("long_or_complex_page")
    if "location" in html.lower() and not deterministic.get("addresses"):
        reasons.append("location_hint_without_address")
    if "provider" in html.lower() and not deterministic.get("specialties"):
        reasons.append("provider_hint_without_specialty")
    if estimated_cost > max_cost_usd:
        reasons.append("cost_gate_exceeded")

    should_call = bool(reasons) and "cost_gate_exceeded" not in reasons
    return LLMGateDecision(
        should_call=should_call,
        reasons=tuple(reasons),
        deterministic_fields_found=found,
        estimated_input_tokens=tokens,
        estimated_cost_usd=estimated_cost,
    )


def validate_llm_extraction(payload: dict[str, Any], source_text: str) -> dict[str, Any]:
    fields = payload.get("fields", {}) if isinstance(payload, dict) else {}
    normalized: dict[str, str] = {}
    errors: list[str] = []
    warnings = list(payload.get("warnings", [])) if isinstance(payload.get("warnings", []), list) else []
    source_norm = source_text.lower()

    for field, value in fields.items():
        if value in {None, ""}:
            continue
        if field == "phone":
            normalized[field] = normalize_phone(value)
        elif field == "address":
            normalized[field] = normalize_address(value)
        elif field in {"specialty", "provider_status"}:
            normalized[field] = normalize_value(field if field == "specialty" else "license_status", value)
        elif field == "accepting_new_patients":
            normalized[field] = "true" if bool(value) else "false"
        else:
            errors.append(f"unknown_field:{field}")

    for span in payload.get("evidence_spans", []):
        text = str(span.get("text", "")).strip()
        if text and text.lower() not in source_norm:
            errors.append(f"unsupported_evidence_span:{span.get('field', '')}")

    confidence = float(payload.get("confidence", 0.0) or 0.0)
    if confidence < 0.60:
        warnings.append("llm_low_confidence_review_only")
    if errors:
        warnings.append("schema_or_grounding_error_review_only")

    return {
        "normalized_fields": normalized,
        "confidence": round(max(0.0, min(confidence, 1.0)), 4),
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "route": "review",
    }


def bedrock_request_contract() -> dict[str, Any]:
    return {
        "runtime": "bedrock-runtime",
        "api": "Converse",
        "response_format": "json_schema",
        "schema": BEDROCK_EXTRACTION_SCHEMA,
        "temperature": 0,
        "max_output_tokens": 450,
        "system": (
            "Extract only provider-directory facts directly supported by the page text. "
            "Return null for missing fields. Include short evidence spans copied from the page."
        ),
    }


def schema_as_json() -> str:
    return json.dumps(BEDROCK_EXTRACTION_SCHEMA, indent=2, sort_keys=True)
