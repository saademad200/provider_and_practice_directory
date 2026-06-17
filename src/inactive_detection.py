from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .data import normalize_text


INACTIVE_STATUS = {
    "d",
    "deactivated",
    "deactivation",
    "inactive",
    "expired",
    "retired",
    "surrendered",
    "revoked",
    "closed",
    "not active",
    "ceased practice",
}

ACTIVE_STATUS = {
    "a",
    "active",
    "reactivated",
    "current",
    "in good standing",
    "probation",
}

RETIREMENT_PHRASES = [
    "retired",
    "no longer practicing",
    "has left the practice",
    "practice closed",
    "office closed",
    "deceased",
    "not seeing patients",
    "ceased practice",
]


@dataclass(frozen=True)
class StatusSignal:
    source: str
    field: str
    value: str
    weight: float
    evidence_type: str


def normalize_status(value: object) -> str:
    text = normalize_text(value)
    if text in ACTIVE_STATUS:
        return "active"
    if text in INACTIVE_STATUS:
        return "inactive"
    if any(phrase in text for phrase in RETIREMENT_PHRASES):
        return "inactive"
    return text


def _signal_from_row(row: dict) -> StatusSignal | None:
    source = str(row.get("source", ""))
    field = str(row.get("field", ""))
    raw_value = str(row.get("value", ""))
    if source == "nppes" and field == "deactivation_date" and raw_value.strip():
        return StatusSignal(source, field, raw_value, 0.36, "nppes_status")
    value = normalize_status(raw_value)
    if value != "inactive":
        return None

    if source == "state_license" and field in {"license_status", "provider_status"}:
        return StatusSignal(source, field, raw_value, 0.46, "license_authority")
    if source == "nppes" and field in {"npi_status", "deactivation_date"}:
        return StatusSignal(source, field, raw_value, 0.36, "nppes_status")
    if source in {"practice_website", "health_system"} and field in {"provider_status", "profile_text"}:
        return StatusSignal(source, field, raw_value, 0.24, "owned_web_text")
    return None


def inactive_provider_candidates(providers: pd.DataFrame, evidence: pd.DataFrame) -> pd.DataFrame:
    rows = []
    current_by_provider = providers.set_index("provider_id").to_dict("index")
    for provider_id, group in evidence.groupby("provider_id", dropna=False):
        if provider_id not in current_by_provider:
            continue
        signals = [signal for signal in (_signal_from_row(row) for row in group.to_dict("records")) if signal]
        if not signals:
            continue

        support = min(sum(signal.weight for signal in signals), 0.99)
        distinct_sources = len({signal.source for signal in signals})
        evidence_types = sorted({signal.evidence_type for signal in signals})
        current_license = normalize_status(current_by_provider[provider_id].get("license_status", ""))
        review_reasons = ["identity_level_change"]
        if distinct_sources < 2:
            review_reasons.append("single_source_inactive_signal")
        if "license_authority" not in evidence_types:
            review_reasons.append("missing_license_authority_confirmation")
        if current_license == "active":
            review_reasons.append("current_directory_lists_active")

        if distinct_sources >= 2 and "license_authority" in evidence_types:
            recommended_action = "suppress_from_auto_scheduling_and_review"
        else:
            recommended_action = "inactive_status_review"

        rows.append(
            {
                "provider_id": provider_id,
                "npi": current_by_provider[provider_id].get("npi", ""),
                "provider_name": current_by_provider[provider_id].get("provider_name", ""),
                "current_license_status": current_by_provider[provider_id].get("license_status", ""),
                "candidate_status": "inactive",
                "confidence": round(support, 4),
                "distinct_sources": distinct_sources,
                "evidence_types": "|".join(evidence_types),
                "sources": "|".join(sorted({signal.source for signal in signals})),
                "evidence_values": "|".join(f"{signal.source}:{signal.field}={signal.value}" for signal in signals),
                "decision": "review",
                "review_reason_code": "|".join(review_reasons),
                "recommended_action": recommended_action,
            }
        )
    if rows:
        return pd.DataFrame(rows).sort_values(["confidence", "distinct_sources"], ascending=False)
    return pd.DataFrame(
        columns=[
            "provider_id",
            "npi",
            "provider_name",
            "current_license_status",
            "candidate_status",
            "confidence",
            "distinct_sources",
            "evidence_types",
            "sources",
            "evidence_values",
            "decision",
            "review_reason_code",
            "recommended_action",
        ]
    )
