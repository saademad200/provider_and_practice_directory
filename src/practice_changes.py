from __future__ import annotations

from difflib import SequenceMatcher

import pandas as pd

from .data import normalize_address, normalize_phone, normalize_text


def practice_name_similarity(left: object, right: object) -> float:
    return SequenceMatcher(None, normalize_text(left), normalize_text(right)).ratio()


def practice_change_candidates(practice_records: pd.DataFrame) -> pd.DataFrame:
    rows = []
    records = practice_records.to_dict("records")
    for i, left in enumerate(records):
        for right in records[i + 1 :]:
            signals = []
            score = 0.0
            same_address = normalize_address(left.get("address", "")) == normalize_address(right.get("address", ""))
            same_phone = normalize_phone(left.get("phone", "")) == normalize_phone(right.get("phone", ""))
            name_sim = practice_name_similarity(left.get("practice_name", ""), right.get("practice_name", ""))
            if same_address:
                signals.append("same_address")
                score += 0.35
            if same_phone:
                signals.append("same_phone")
                score += 0.25
            if 0.55 <= name_sim < 0.92:
                signals.append("possible_rebrand")
                score += 0.25
            if str(left.get("npi", "")) and str(left.get("npi", "")) == str(right.get("npi", "")):
                signals.append("same_provider_npi")
                score += 0.30
            if str(left.get("practice_id", "")) != str(right.get("practice_id", "")) and same_address:
                signals.append("practice_affiliation_change")
                score += 0.20
            score = min(score, 1.0)
            if score >= 0.55:
                rows.append(
                    {
                        "left_practice_id": left.get("practice_id", ""),
                        "right_practice_id": right.get("practice_id", ""),
                        "left_practice_name": left.get("practice_name", ""),
                        "right_practice_name": right.get("practice_name", ""),
                        "provider_id": left.get("provider_id", ""),
                        "change_score": round(score, 4),
                        "name_similarity": round(name_sim, 4),
                        "signals": "|".join(signals),
                        "recommended_action": "practice_change_review",
                    }
                )
    return pd.DataFrame(rows).sort_values("change_score", ascending=False) if rows else pd.DataFrame(
        columns=[
            "left_practice_id",
            "right_practice_id",
            "left_practice_name",
            "right_practice_name",
            "provider_id",
            "change_score",
            "name_similarity",
            "signals",
            "recommended_action",
        ]
    )
