from __future__ import annotations

from typing import Any

import pandas as pd


SOURCE_COST_USD = {
    "nppes": 0.0001,
    "state_license": 0.0015,
    "practice_website": 0.0040,
    "health_system": 0.0025,
    "business_listing": 0.0030,
    "llm_extraction": 0.0200,
}


def estimate_candidate_cost(candidates: pd.DataFrame, source_costs: dict[str, float] | None = None) -> dict[str, Any]:
    source_costs = {**SOURCE_COST_USD, **(source_costs or {})}
    breakdown = {source: 0.0 for source in source_costs}
    if candidates.empty or "sources" not in candidates:
        return {"total": 0.0, "breakdown": breakdown}

    for sources in candidates["sources"].fillna(""):
        for source in {item for item in str(sources).split("|") if item}:
            breakdown[source] = breakdown.get(source, 0.0) + source_costs.get(source, 0.0050)
    total = sum(breakdown.values())
    return {
        "total": round(total, 6),
        "breakdown": {key: round(value, 6) for key, value in sorted(breakdown.items()) if value},
    }

