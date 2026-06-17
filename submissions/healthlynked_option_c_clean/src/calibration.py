from __future__ import annotations

import pandas as pd

from .data import normalize_value


def candidate_correctness(candidates: pd.DataFrame, gold: pd.DataFrame) -> pd.DataFrame:
    if candidates.empty:
        return candidates.assign(is_correct=pd.Series(dtype=bool))
    truth = {
        (str(row.provider_id), str(row.field), normalize_value(str(row.field), row.new_value))
        for row in gold.itertuples(index=False)
    }
    out = candidates.copy()
    out["is_correct"] = [
        (str(row.provider_id), str(row.field), normalize_value(str(row.field), row.proposed_value)) in truth
        for row in out.itertuples(index=False)
    ]
    return out


def calibration_table(candidates: pd.DataFrame, gold: pd.DataFrame) -> pd.DataFrame:
    scored = candidate_correctness(candidates, gold)
    if scored.empty:
        return pd.DataFrame(columns=["field", "decision", "confidence_bin", "count", "accuracy", "avg_confidence"])
    bins = [0.0, 0.75, 0.85, 0.90, 0.95, 0.98, 1.0]
    labels = ["<=0.75", "0.75-0.85", "0.85-0.90", "0.90-0.95", "0.95-0.98", "0.98-1.00"]
    scored["confidence_bin"] = pd.cut(scored["confidence"], bins=bins, labels=labels, include_lowest=True)
    rows = []
    for keys, group in scored.groupby(["field", "decision", "confidence_bin"], observed=True):
        field, decision, confidence_bin = keys
        rows.append(
            {
                "field": field,
                "decision": decision,
                "confidence_bin": str(confidence_bin),
                "count": int(len(group)),
                "accuracy": round(float(group["is_correct"].mean()), 6),
                "avg_confidence": round(float(group["confidence"].mean()), 6),
            }
        )
    return pd.DataFrame(rows).sort_values(["field", "decision", "confidence_bin"])

