from __future__ import annotations

from typing import Any

import pandas as pd

from .data import normalize_value
from .cost import estimate_candidate_cost


def _keyed_updates(df: pd.DataFrame, value_col: str) -> set[tuple[str, str, str]]:
    if df.empty:
        return set()
    return {
        (str(row.provider_id), str(row.field), normalize_value(str(row.field), getattr(row, value_col)))
        for row in df.itertuples(index=False)
    }


def score_candidate_updates(candidates: pd.DataFrame, gold: pd.DataFrame) -> dict[str, Any]:
    pred = _keyed_updates(candidates, "proposed_value")
    truth = _keyed_updates(gold, "new_value")
    tp = len(pred & truth)
    fp = len(pred - truth)
    fn = len(truth - pred)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    auto = candidates[candidates.get("decision", "") == "auto_apply"] if not candidates.empty else candidates
    auto_pred = _keyed_updates(auto, "proposed_value")
    auto_tp = len(auto_pred & truth)
    auto_fp = len(auto_pred - truth)
    auto_precision = auto_tp / (auto_tp + auto_fp) if auto_tp + auto_fp else 0.0

    review = candidates[candidates.get("decision", "") == "review"] if not candidates.empty else candidates
    review_pred = _keyed_updates(review, "proposed_value")
    review_recall = len(review_pred & truth) / len(truth) if truth else 0.0

    cost = estimate_candidate_cost(candidates)
    estimated_cost = float(cost["total"])
    cost_per_correct = estimated_cost / tp if tp else None

    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "f1": round(f1, 6),
        "auto_apply_count": int(len(auto)),
        "auto_apply_precision": round(auto_precision, 6),
        "review_count": int(len(review)),
        "review_recall": round(review_recall, 6),
        "estimated_cost_usd": round(estimated_cost, 6),
        "cost_per_correct_update_usd": round(cost_per_correct, 6) if cost_per_correct is not None else None,
        "source_cost_breakdown_usd": cost["breakdown"],
        "predicted_updates": int(len(candidates)),
        "gold_updates": int(len(gold)),
    }


def per_field_breakdown(candidates: pd.DataFrame, gold: pd.DataFrame) -> pd.DataFrame:
    fields = sorted(set(candidates.get("field", pd.Series(dtype=str))).union(set(gold.get("field", pd.Series(dtype=str)))))
    rows = []
    for field in fields:
        rows.append(
            {
                "field": field,
                **score_candidate_updates(
                    candidates[candidates["field"] == field] if not candidates.empty else candidates,
                    gold[gold["field"] == field] if not gold.empty else gold,
                ),
            }
        )
    return pd.DataFrame(rows)


def worst_provider_breakdown(candidates: pd.DataFrame, gold: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    pred = _keyed_updates(candidates, "proposed_value")
    truth = _keyed_updates(gold, "new_value")
    provider_ids = sorted({item[0] for item in pred | truth})
    rows = []
    for provider_id in provider_ids:
        p_pred = {item for item in pred if item[0] == provider_id}
        p_truth = {item for item in truth if item[0] == provider_id}
        rows.append(
            {
                "provider_id": provider_id,
                "tp": len(p_pred & p_truth),
                "fp": len(p_pred - p_truth),
                "fn": len(p_truth - p_pred),
            }
        )
    if not rows:
        return pd.DataFrame(columns=["provider_id", "tp", "fp", "fn", "error"])
    out = pd.DataFrame(rows)
    out["error"] = out["fp"] + out["fn"]
    return out.sort_values(["error", "fn", "fp"], ascending=False).head(limit)
