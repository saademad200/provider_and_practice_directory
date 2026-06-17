from __future__ import annotations

from typing import Any


DEFAULT_SOURCE_SLA_DAYS = {
    "nppes": 30,
    "state_license": 45,
    "practice_website": 30,
    "health_system": 30,
    "business_listing": 14,
}


def freshness_metadata(
    evidence_items: list[tuple[str, float]],
    source_slas_days: dict[str, Any] | None = None,
) -> dict[str, Any]:
    slas = {**DEFAULT_SOURCE_SLA_DAYS, **(source_slas_days or {})}
    if not evidence_items:
        return {
            "max_evidence_age_days": None,
            "source_age_days": "",
            "freshness_status": "missing",
            "stale_sources": "",
            "freshness_alert": "no_supporting_evidence",
        }

    source_ages: dict[str, float] = {}
    for source, age in evidence_items:
        source_ages[source] = min(float(age), source_ages.get(source, float("inf")))

    stale_sources = []
    for source, age in source_ages.items():
        if age > float(slas.get(source, 30)):
            stale_sources.append(source)

    if not stale_sources:
        status = "fresh"
        alert = "fresh_supporting_evidence"
    elif len(stale_sources) == len(source_ages):
        status = "all_stale"
        alert = "all_supporting_sources_stale"
    else:
        status = "partially_stale"
        alert = "some_supporting_sources_stale"

    return {
        "max_evidence_age_days": int(max(source_ages.values())),
        "source_age_days": "|".join(f"{source}:{int(age)}" for source, age in sorted(source_ages.items())),
        "freshness_status": status,
        "stale_sources": "|".join(sorted(stale_sources)),
        "freshness_alert": alert,
    }
