from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

import pandas as pd


AUDIT_SCHEMA_VERSION = "provider-directory-audit-v1"


def audit_scalar(value: object) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return ""
    if pd.isna(value):
        return ""
    return str(value)


def stable_hash(value: object) -> str:
    text = json.dumps(value, sort_keys=True, default=str)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def audit_events_from_candidates(
    candidates: pd.DataFrame,
    run_id: str,
    pipeline_version: str,
    created_at: str | None = None,
) -> list[dict[str, Any]]:
    timestamp = created_at or datetime.now(timezone.utc).isoformat()
    events: list[dict[str, Any]] = []
    for idx, row in enumerate(candidates.to_dict("records"), start=1):
        evidence = {
            "sources": str(row.get("sources", "")).split("|") if row.get("sources") else [],
            "urls": str(row.get("evidence_urls", "")).split("|") if row.get("evidence_urls") else [],
            "source_age_days": str(row.get("source_age_days", "")),
            "freshness_status": row.get("freshness_status", ""),
        }
        event_body = {
            "run_id": run_id,
            "provider_id": row.get("provider_id", ""),
            "practice_id": row.get("practice_id", ""),
            "field": row.get("field", ""),
            "old_value": audit_scalar(row.get("old_value", "")),
            "new_value": audit_scalar(row.get("proposed_value", "")),
            "decision": row.get("decision", ""),
            "confidence": row.get("confidence", ""),
            "evidence_hash": stable_hash(evidence),
        }
        events.append(
            {
                "schema_version": AUDIT_SCHEMA_VERSION,
                "event_id": f"{run_id}-{idx:05d}-{stable_hash(event_body)}",
                "event_type": "candidate_update_created",
                "created_at": timestamp,
                "pipeline_version": pipeline_version,
                "provider_id": event_body["provider_id"],
                "practice_id": event_body["practice_id"],
                "field": event_body["field"],
                "old_value": event_body["old_value"],
                "new_value": event_body["new_value"],
                "decision": event_body["decision"],
                "confidence": event_body["confidence"],
                "review_reason_code": row.get("review_reason_code", ""),
                "review_priority_score": row.get("review_priority_score", ""),
                "sources": evidence["sources"],
                "evidence_urls": evidence["urls"],
                "evidence_hash": event_body["evidence_hash"],
                "freshness_status": evidence["freshness_status"],
                "rollback_status": "eligible" if row.get("decision") == "auto_apply" else "not_applied_yet",
            }
        )
    return events


def rollback_plan_from_events(events: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for event in events:
        if event.get("decision") != "auto_apply":
            continue
        rows.append(
            {
                "rollback_id": f"rollback-{event['event_id']}",
                "event_id": event["event_id"],
                "provider_id": event.get("provider_id", ""),
                "practice_id": event.get("practice_id", ""),
                "field": event.get("field", ""),
                "current_value_to_replace": event.get("new_value", ""),
                "restore_value": event.get("old_value", ""),
                "required_approval": "directory_ops_lead",
                "rollback_reason_required": True,
                "evidence_hash": event.get("evidence_hash", ""),
            }
        )
    return pd.DataFrame(rows)


def provider_timeline(events: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for event in events:
        rows.append(
            {
                "provider_id": event.get("provider_id", ""),
                "created_at": event.get("created_at", ""),
                "event_type": event.get("event_type", ""),
                "field": event.get("field", ""),
                "old_value": event.get("old_value", ""),
                "new_value": event.get("new_value", ""),
                "decision": event.get("decision", ""),
                "event_id": event.get("event_id", ""),
            }
        )
    return pd.DataFrame(rows).sort_values(["provider_id", "created_at", "field"]) if rows else pd.DataFrame()


def write_jsonl(path, records: list[dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
