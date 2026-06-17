from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any

import pandas as pd

from .data import normalize_address, normalize_phone, normalize_text, normalize_value


def name_similarity(left: Any, right: Any) -> float:
    return SequenceMatcher(None, normalize_text(left), normalize_text(right)).ratio()


def potential_duplicate_pairs(providers: pd.DataFrame, min_score: float = 0.86) -> pd.DataFrame:
    rows = []
    records = providers.to_dict("records")
    for i, left in enumerate(records):
        for right in records[i + 1 :]:
            signals = []
            score = 0.0
            if str(left.get("npi", "")) and str(left.get("npi", "")) == str(right.get("npi", "")):
                signals.append("same_npi")
                score += 0.55
            if normalize_phone(left.get("phone", "")) == normalize_phone(right.get("phone", "")):
                signals.append("same_phone")
                score += 0.18
            if normalize_address(left.get("address", "")) == normalize_address(right.get("address", "")):
                signals.append("same_address")
                score += 0.18
            if normalize_value("specialty", left.get("specialty", "")) == normalize_value("specialty", right.get("specialty", "")):
                signals.append("same_specialty")
                score += 0.05
            similarity = name_similarity(left.get("provider_name", ""), right.get("provider_name", ""))
            if similarity >= 0.88:
                signals.append("similar_name")
                score += 0.18 * similarity
            score = min(score, 1.0)
            if score >= min_score:
                rows.append(
                    {
                        "left_provider_id": left.get("provider_id", ""),
                        "right_provider_id": right.get("provider_id", ""),
                        "duplicate_score": round(score, 4),
                        "name_similarity": round(similarity, 4),
                        "signals": "|".join(signals),
                        "recommended_action": "merge_review",
                    }
                )
    return pd.DataFrame(rows).sort_values("duplicate_score", ascending=False) if rows else pd.DataFrame(
        columns=[
            "left_provider_id",
            "right_provider_id",
            "duplicate_score",
            "name_similarity",
            "signals",
            "recommended_action",
        ]
    )


def provider_movement_signals(candidates: pd.DataFrame) -> pd.DataFrame:
    if candidates.empty:
        return pd.DataFrame(
            columns=[
                "provider_id",
                "practice_id",
                "field",
                "old_value",
                "proposed_value",
                "movement_score",
                "signals",
                "recommended_action",
            ]
        )
    movement_fields = candidates[candidates["field"].isin(["address", "phone"])].copy()
    if movement_fields.empty:
        return pd.DataFrame()
    rows = []
    for row in movement_fields.itertuples(index=False):
        item = row._asdict()
        signals = []
        score = 0.0
        if item.get("field") == "address":
            signals.append("address_changed")
            score += 0.45
        if item.get("field") == "phone":
            signals.append("phone_changed")
            score += 0.25
        if item.get("practice_consensus_status") == "peer_mismatch":
            signals.append("practice_peer_mismatch")
            score += 0.30
        if item.get("freshness_status") == "fresh":
            signals.append("fresh_evidence")
            score += 0.10
        if item.get("distinct_sources", 0) >= 3:
            signals.append("multi_source_support")
            score += 0.15
        rows.append(
            {
                "provider_id": item.get("provider_id", ""),
                "practice_id": item.get("practice_id", ""),
                "field": item.get("field", ""),
                "old_value": item.get("old_value", ""),
                "proposed_value": item.get("proposed_value", ""),
                "movement_score": round(min(score, 1.0), 4),
                "signals": "|".join(signals),
                "recommended_action": "movement_review" if score >= 0.65 else "field_update_review",
            }
        )
    return pd.DataFrame(rows).sort_values("movement_score", ascending=False)
