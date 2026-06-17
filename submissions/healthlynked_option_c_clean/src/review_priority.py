from __future__ import annotations

from typing import Any


FIELD_RISK = {
    "address": 0.95,
    "license_status": 0.90,
    "accepting_new_patients": 0.85,
    "phone": 0.75,
    "specialty": 0.60,
}


def priority_band(score: float) -> str:
    if score >= 0.75:
        return "high"
    if score >= 0.50:
        return "medium"
    return "low"


def review_priority(
    *,
    field: str,
    confidence: float,
    review_reasons: list[str],
    threshold: float,
    auto_threshold: float,
    distinct_sources: int,
    min_auto_sources: int,
) -> dict[str, Any]:
    field_risk = FIELD_RISK.get(field, 0.50)
    confidence_window = max(auto_threshold - threshold, 1e-6)
    uncertainty = max(0.0, min(1.0, (auto_threshold - confidence) / confidence_window))
    source_gap = max(0, min_auto_sources - distinct_sources) / max(min_auto_sources, 1)
    peer_mismatch = 1.0 if "practice_peer_mismatch" in review_reasons else 0.0

    score = min(
        1.0,
        0.48 * field_risk
        + 0.24 * uncertainty
        + 0.18 * source_gap
        + 0.10 * peer_mismatch,
    )
    drivers = []
    if field_risk >= 0.85:
        drivers.append("high_field_risk")
    if uncertainty >= 0.50:
        drivers.append("near_threshold")
    if source_gap > 0:
        drivers.append("source_gap")
    if peer_mismatch:
        drivers.append("practice_peer_mismatch")
    if not drivers and review_reasons:
        drivers.append("standard_review")
    if not drivers:
        drivers.append("auto_apply_criteria_met")

    return {
        "review_priority_score": round(score, 4),
        "review_priority_band": priority_band(score),
        "review_priority_drivers": "|".join(drivers),
    }
