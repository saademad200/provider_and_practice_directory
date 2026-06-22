from __future__ import annotations

from typing import Any

import pandas as pd

from .data import FIELDS, normalize_value


SOURCE_AUTHORITY = {
    "state_license": 1.0,
    "nppes": 0.92,
    "health_system": 0.86,
    "practice_website": 0.82,
    "business_listing": 0.45,
}

FIELD_SOURCE_AUTHORITY = {
    "license_status": {"state_license": 1.0, "nppes": 0.6, "health_system": 0.5, "practice_website": 0.45, "business_listing": 0.2},
    "specialty": {"nppes": 1.0, "health_system": 0.86, "practice_website": 0.82, "business_listing": 0.35},
    "phone": {"practice_website": 0.95, "health_system": 0.9, "nppes": 0.75, "business_listing": 0.35},
    "address": {"practice_website": 0.95, "health_system": 0.9, "nppes": 0.75, "business_listing": 0.35},
    "accepting_new_patients": {"practice_website": 0.95, "health_system": 0.9, "nppes": 0.55, "business_listing": 0.25},
}

FIELD_AUTHORITY_SOURCE = {
    "license_status": "state_license",
    "specialty": "nppes",
    "phone": "practice_website",
    "address": "practice_website",
    "accepting_new_patients": "practice_website",
}


def authority_for(field: str, source: str) -> float:
    return FIELD_SOURCE_AUTHORITY.get(field, {}).get(source, SOURCE_AUTHORITY.get(source, 0.0))


def source_conflict_diagnostics(evidence: pd.DataFrame, min_sources: int = 2) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for (provider_id, field), group in evidence.groupby(["provider_id", "field"], dropna=False):
        if field not in FIELDS:
            continue
        values: dict[str, set[str]] = {}
        for row in group.to_dict("records"):
            value = normalize_value(str(field), row.get("value", ""))
            if not value:
                continue
            source = str(row.get("source", ""))
            values.setdefault(value, set()).add(source)
        if len(values) < 2:
            continue
        distinct_sources = len({source for sources in values.values() for source in sources})
        if distinct_sources < min_sources:
            continue

        ranked_values = sorted(
            values.items(),
            key=lambda item: (max(authority_for(str(field), source) for source in item[1]), len(item[1])),
            reverse=True,
        )
        winner, winner_sources = ranked_values[0]
        runner_up, runner_sources = ranked_values[1]
        winner_authority = max(authority_for(str(field), source) for source in winner_sources)
        runner_authority = max(authority_for(str(field), source) for source in runner_sources)
        authority_source = FIELD_AUTHORITY_SOURCE.get(str(field), "")
        if authority_source and authority_source in winner_sources and winner_authority > runner_authority:
            action = "authority_precedence_review"
        elif winner_authority == runner_authority:
            action = "tie_review"
        else:
            action = "multi_source_conflict_review"

        rows.append(
            {
                "provider_id": provider_id,
                "field": field,
                "candidate_value": winner,
                "candidate_sources": "|".join(sorted(winner_sources)),
                "competing_value": runner_up,
                "competing_sources": "|".join(sorted(runner_sources)),
                "distinct_values": len(values),
                "distinct_sources": distinct_sources,
                "winner_authority": round(winner_authority, 3),
                "runner_up_authority": round(runner_authority, 3),
                "field_authority_source": authority_source,
                "recommended_action": action,
                "all_values": " || ".join(
                    f"{value} <= {','.join(sorted(sources))}" for value, sources in sorted(values.items())
                ),
            }
        )
    if rows:
        return pd.DataFrame(rows).sort_values(
            ["winner_authority", "distinct_values", "distinct_sources"],
            ascending=[False, False, False],
        )
    return pd.DataFrame(
        columns=[
            "provider_id",
            "field",
            "candidate_value",
            "candidate_sources",
            "competing_value",
            "competing_sources",
            "distinct_values",
            "distinct_sources",
            "winner_authority",
            "runner_up_authority",
            "field_authority_source",
            "recommended_action",
            "all_values",
        ]
    )
