from __future__ import annotations

from typing import Any

import pandas as pd

from .data import normalize_value


def keyed(df: pd.DataFrame, value_col: str) -> set[tuple[str, str, str]]:
    if df.empty:
        return set()
    return {
        (str(row.provider_id), str(row.field), normalize_value(str(row.field), getattr(row, value_col)))
        for row in df.itertuples(index=False)
    }


def simulated_review_feedback(candidates: pd.DataFrame, gold: pd.DataFrame) -> pd.DataFrame:
    truth = keyed(gold, "new_value")
    rows: list[dict[str, Any]] = []
    for row in candidates.itertuples(index=False):
        item = row._asdict()
        field = str(item["field"])
        candidate_key = (
            str(item["provider_id"]),
            field,
            normalize_value(field, item["proposed_value"]),
        )
        reviewer_decision = "accepted" if candidate_key in truth else "rejected"
        rows.append(
            {
                **item,
                "reviewer_decision": reviewer_decision,
                "reviewer_correct": reviewer_decision == "accepted",
            }
        )
    return pd.DataFrame(rows)


def source_feedback_summary(feedback: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in feedback.itertuples(index=False):
        item = row._asdict()
        for source in str(item.get("sources", "")).split("|"):
            if source:
                rows.append(
                    {
                        "source": source,
                        "field": item["field"],
                        "reviewer_correct": bool(item["reviewer_correct"]),
                        "decision": item["decision"],
                        "freshness_status": item.get("freshness_status", ""),
                    }
                )
    exploded = pd.DataFrame(rows)
    if exploded.empty:
        return pd.DataFrame(columns=["source", "field", "observations", "accept_rate", "auto_apply_share"])
    grouped = (
        exploded.groupby(["source", "field"])
        .agg(
            observations=("reviewer_correct", "size"),
            accept_rate=("reviewer_correct", "mean"),
            auto_apply_share=("decision", lambda values: (values == "auto_apply").mean()),
        )
        .reset_index()
    )
    grouped["accept_rate"] = grouped["accept_rate"].round(4)
    grouped["auto_apply_share"] = grouped["auto_apply_share"].round(4)
    return grouped.sort_values(["accept_rate", "observations"], ascending=[True, False])


def learning_actions(source_summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in source_summary.itertuples(index=False):
        action = "hold"
        rationale = "enough precision for current role"
        if row.observations >= 3 and row.accept_rate < 0.80:
            action = "downweight_or_review_gate"
            rationale = "review outcomes show elevated rejection rate"
        elif row.observations >= 3 and row.accept_rate >= 0.95 and row.auto_apply_share < 0.50:
            action = "consider_safe_auto_apply_expansion"
            rationale = "high accept rate but many items still route to review"
        rows.append(
            {
                "source": row.source,
                "field": row.field,
                "observations": int(row.observations),
                "accept_rate": float(row.accept_rate),
                "auto_apply_share": float(row.auto_apply_share),
                "recommended_action": action,
                "rationale": rationale,
            }
        )
    return pd.DataFrame(rows)
