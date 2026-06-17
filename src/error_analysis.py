from __future__ import annotations

from typing import Any

import pandas as pd

from .data import normalize_value


FIELD_ACTIONS = {
    "address": "Add USPS/Google-free address canonicalization plus practice-site location history.",
    "phone": "Add stronger practice-location peer consensus and phone-line type checks.",
    "specialty": "Add taxonomy crosswalk plus provider-profile specialty history.",
    "accepting_new_patients": "Add payer/provider roster freshness checks and last-seen timestamps.",
    "license_status": "Add state-board status snapshots and explicit status transition rules.",
}


def residual_error_tables(candidates: pd.DataFrame, gold: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    pred = keyed_frame(candidates, "proposed_value")
    truth = keyed_frame(gold, "new_value")
    pred_keys = set(pred["key"]) if not pred.empty else set()
    truth_keys = set(truth["key"]) if not truth.empty else set()

    fp = pred[pred["key"].isin(pred_keys - truth_keys)].copy()
    fn = truth[truth["key"].isin(truth_keys - pred_keys)].copy()
    fp["error_type"] = "false_positive"
    fn["error_type"] = "false_negative"

    plan = acquisition_plan(fp, fn)
    return fp.drop(columns=["key"], errors="ignore"), fn.drop(columns=["key"], errors="ignore"), plan


def keyed_frame(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["key"])
    rows: list[dict[str, Any]] = []
    for row in df.to_dict("records"):
        field = str(row["field"])
        value = normalize_value(field, str(row[value_col]))
        rows.append(
            {
                **row,
                "normalized_value": value,
                "key": (str(row["provider_id"]), field, value),
            }
        )
    return pd.DataFrame(rows)


def acquisition_plan(fp: pd.DataFrame, fn: pd.DataFrame) -> pd.DataFrame:
    frames = []
    if not fp.empty:
        frames.append(fp.assign(error_type="false_positive"))
    if not fn.empty:
        frames.append(fn.assign(error_type="false_negative"))
    combined = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=["field", "error_type"])
    if combined.empty:
        return pd.DataFrame(columns=["field", "false_positives", "false_negatives", "priority", "recommended_action"])
    counts = combined.pivot_table(index="field", columns="error_type", values="provider_id", aggfunc="count", fill_value=0).reset_index()
    for col in ["false_positive", "false_negative"]:
        if col not in counts:
            counts[col] = 0
    counts["total_errors"] = counts["false_positive"] + counts["false_negative"]
    counts["priority"] = counts["total_errors"].rank(method="dense", ascending=False).astype(int)
    counts["recommended_action"] = counts["field"].map(FIELD_ACTIONS).fillna("Acquire more authoritative source evidence and add field-specific validators.")
    counts = counts.rename(columns={"false_positive": "false_positives", "false_negative": "false_negatives"})
    return counts.sort_values(["priority", "field"]).reset_index(drop=True)
