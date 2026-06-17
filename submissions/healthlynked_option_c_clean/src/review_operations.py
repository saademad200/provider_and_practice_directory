from __future__ import annotations

from typing import Any

import pandas as pd


def review_disposition_contract() -> dict[str, Any]:
    return {
        "contract_version": "2026-06-16",
        "name": "provider_directory_review_disposition",
        "required_fields": [
            "candidate_id",
            "provider_id",
            "field",
            "reviewer_id",
            "review_action",
            "reviewed_at",
            "disposition_reason",
            "audit_event_id",
        ],
        "properties": {
            "candidate_id": {"type": "string", "description": "Stable hash or UUID for the candidate update row."},
            "provider_id": {"type": "string"},
            "practice_id": {"type": "string"},
            "field": {"enum": ["phone", "address", "specialty", "license_status", "accepting_new_patients"]},
            "old_value": {"type": "string"},
            "proposed_value": {"type": "string"},
            "reviewer_value": {"type": "string", "description": "Required when review_action is edit."},
            "reviewer_id": {"type": "string", "description": "Authenticated reviewer identity, not a free-text name."},
            "review_action": {"enum": ["accept", "reject", "edit", "defer", "request_recrawl"]},
            "reviewed_at": {"type": "string", "format": "date-time"},
            "disposition_reason": {"type": "string"},
            "source_feedback": {"enum": ["source_correct", "source_wrong", "source_stale", "source_insufficient", "not_applicable"]},
            "audit_event_id": {"type": "string"},
            "source_run_id": {"type": "string"},
            "sla_status": {"enum": ["within_sla", "breached", "paused_waiting_on_source"]},
        },
        "validation_rules": [
            "reviewer_id must come from authenticated AWS Cognito or workforce identity provider context",
            "edit requires reviewer_value and disposition_reason",
            "request_recrawl requires at least one stale or insufficient source reason",
            "accept/reject/edit must write an append-only audit event before downstream mutation",
            "identity-level or inactive-provider decisions require elevated reviewer role",
        ],
    }


def review_sla_metrics(review_queue: pd.DataFrame) -> pd.DataFrame:
    if review_queue.empty:
        return pd.DataFrame(columns=["priority_band", "items", "sla_hours", "estimated_reviewer_hours", "risk_policy"])
    sla_hours = {"high": 8, "medium": 24, "low": 72}
    minutes_per_item = {"high": 4.0, "medium": 2.5, "low": 1.5}
    rows = []
    for band, group in review_queue.groupby("review_priority_band", dropna=False):
        band_key = str(band).lower()
        items = int(len(group))
        rows.append(
            {
                "priority_band": band_key,
                "items": items,
                "sla_hours": sla_hours.get(band_key, 72),
                "estimated_reviewer_hours": round(items * minutes_per_item.get(band_key, 2.0) / 60, 3),
                "risk_policy": "same_day_patient_access_review" if band_key == "high" else "standard_queue_review",
            }
        )
    return pd.DataFrame(rows).sort_values(["sla_hours", "priority_band"]).reset_index(drop=True)


def review_feedback_fixture(review_queue: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    rows = []
    for index, row in review_queue.head(limit).reset_index(drop=True).iterrows():
        action = ["accept", "reject", "edit", "defer", "request_recrawl"][index % 5]
        rows.append(
            {
                "candidate_id": f"review_fixture_{index:03d}",
                "provider_id": row.get("provider_id", ""),
                "practice_id": row.get("practice_id", ""),
                "field": row.get("field", ""),
                "old_value": row.get("old_value", ""),
                "proposed_value": row.get("proposed_value", ""),
                "reviewer_value": row.get("proposed_value", "") if action == "edit" else "",
                "reviewer_id": f"reviewer_{1 + index % 3}",
                "review_action": action,
                "reviewed_at": "2026-06-16T12:00:00Z",
                "disposition_reason": _reason_for_action(action, row),
                "source_feedback": _source_feedback_for_action(action),
                "audit_event_id": f"audit_fixture_{index:03d}",
                "source_run_id": "synthetic_review_fixture",
                "sla_status": "within_sla",
            }
        )
    return pd.DataFrame(rows)


def _reason_for_action(action: str, row: pd.Series) -> str:
    if action == "accept":
        return "evidence_supports_update"
    if action == "reject":
        return "source_conflict_or_wrong_provider"
    if action == "edit":
        return "value_correct_after_minor_normalization"
    if action == "request_recrawl":
        return "stale_or_insufficient_evidence"
    return f"needs_additional_confirmation:{row.get('review_reason_code', '')}"


def _source_feedback_for_action(action: str) -> str:
    return {
        "accept": "source_correct",
        "reject": "source_wrong",
        "edit": "source_correct",
        "defer": "source_insufficient",
        "request_recrawl": "source_stale",
    }[action]
