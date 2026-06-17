from __future__ import annotations

from typing import Any

import pandas as pd


REQUIRED_TRACE_EVENTS = [
    "source_fetch",
    "normalize_evidence",
    "identity_resolution",
    "source_conflict_check",
    "score_candidates",
    "route_review",
    "write_audit_event",
    "emit_monitoring_metrics",
]

FORBIDDEN_TRACE_EVENTS = [
    "read_gold_updates_for_generation",
    "auto_apply_identity_delete",
    "drop_conflicting_value_without_reason",
    "call_llm_without_cost_gate",
    "write_update_without_audit",
]


def sample_trace_fixture() -> list[dict[str, Any]]:
    return [
        {"run_id": "good_trace", "event": "source_fetch", "agent": "source_retrieval_agent", "status": "ok"},
        {"run_id": "good_trace", "event": "normalize_evidence", "agent": "evidence_normalization_agent", "status": "ok"},
        {"run_id": "good_trace", "event": "identity_resolution", "agent": "identity_resolution_agent", "status": "ok"},
        {"run_id": "good_trace", "event": "source_conflict_check", "agent": "source_conflict_agent", "status": "ok"},
        {"run_id": "good_trace", "event": "score_candidates", "agent": "evidence_scoring_agent", "status": "ok"},
        {"run_id": "good_trace", "event": "route_review", "agent": "human_review_agent", "status": "ok"},
        {"run_id": "good_trace", "event": "write_audit_event", "agent": "audit_rollback_agent", "status": "ok"},
        {"run_id": "good_trace", "event": "emit_monitoring_metrics", "agent": "monitoring_agent", "status": "ok"},
        {"run_id": "bad_trace", "event": "source_fetch", "agent": "source_retrieval_agent", "status": "ok"},
        {"run_id": "bad_trace", "event": "normalize_evidence", "agent": "evidence_normalization_agent", "status": "ok"},
        {"run_id": "bad_trace", "event": "call_llm_without_cost_gate", "agent": "evidence_normalization_agent", "status": "fail"},
        {"run_id": "bad_trace", "event": "score_candidates", "agent": "evidence_scoring_agent", "status": "ok"},
        {"run_id": "bad_trace", "event": "write_update_without_audit", "agent": "evidence_scoring_agent", "status": "fail"},
    ]


def evaluate_trace_events(events: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    df = pd.DataFrame(events)
    for run_id, group in df.groupby("run_id", dropna=False):
        observed = set(group["event"].astype(str))
        missing = [event for event in REQUIRED_TRACE_EVENTS if event not in observed]
        forbidden = [event for event in FORBIDDEN_TRACE_EVENTS if event in observed]
        passed = not missing and not forbidden
        score = max(0.0, 1.0 - 0.08 * len(missing) - 0.18 * len(forbidden))
        rows.append(
            {
                "run_id": run_id,
                "passed": passed,
                "trajectory_score": round(score, 4),
                "missing_required_events": "|".join(missing),
                "forbidden_events": "|".join(forbidden),
                "event_count": int(len(group)),
                "recommended_action": "ship_candidate" if passed else "block_and_debug_trace",
            }
        )
    return pd.DataFrame(rows).sort_values(["passed", "trajectory_score"], ascending=[True, True])


def rubric_rows() -> pd.DataFrame:
    rows = []
    for event in REQUIRED_TRACE_EVENTS:
        rows.append(
            {
                "rubric_type": "required",
                "event": event,
                "weight": 0.08,
                "rationale": "Required workflow step for reliable provider-directory automation.",
            }
        )
    for event in FORBIDDEN_TRACE_EVENTS:
        rows.append(
            {
                "rubric_type": "forbidden",
                "event": event,
                "weight": 0.18,
                "rationale": "Unsafe or leakage-prone behavior that should block production runs.",
            }
        )
    return pd.DataFrame(rows)
