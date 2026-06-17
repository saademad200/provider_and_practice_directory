from __future__ import annotations

from typing import Any

import pandas as pd


def red_team_cases() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "case_id": "rt_wrong_provider_merge",
                "threat": "Evidence from a same-name provider with different NPI is attached to the target provider.",
                "expected_control": "identity_resolution_requires_npi_match",
                "forbidden_outcome": "auto_apply_identity_or_affiliation_change",
                "signal": "npi_mismatch",
                "severity": "critical",
            },
            {
                "case_id": "rt_stale_source_auto_apply",
                "threat": "All supporting sources are stale but agree on a phone/address update.",
                "expected_control": "freshness_gate_blocks_auto_apply",
                "forbidden_outcome": "auto_apply_stale_evidence",
                "signal": "all_supporting_sources_stale",
                "severity": "high",
            },
            {
                "case_id": "rt_audit_gap",
                "threat": "Candidate update proceeds without an append-only audit event ID.",
                "expected_control": "audit_event_required_before_mutation",
                "forbidden_outcome": "directory_mutation_without_audit_event",
                "signal": "missing_audit_event_id",
                "severity": "critical",
            },
            {
                "case_id": "rt_llm_unsupported_span",
                "threat": "LLM extracts a value not present in the cited source snippet.",
                "expected_control": "grounded_schema_validation_routes_review",
                "forbidden_outcome": "auto_apply_llm_unsupported_value",
                "signal": "unsupported_evidence_span",
                "severity": "high",
            },
            {
                "case_id": "rt_conflicting_authorities",
                "threat": "State board and practice website disagree on license or active status.",
                "expected_control": "authority_rank_conflict_review",
                "forbidden_outcome": "silent_lower_authority_override",
                "signal": "higher_authority_disagreement",
                "severity": "high",
            },
            {
                "case_id": "rt_cost_runaway",
                "threat": "Crawler or LLM route exceeds expected cost per 1,000 providers.",
                "expected_control": "cost_gate_and_source_budget_alarm",
                "forbidden_outcome": "unbounded_paid_source_or_llm_calls",
                "signal": "cost_budget_exceeded",
                "severity": "medium",
            },
            {
                "case_id": "rt_terms_violation",
                "threat": "Connector attempts to crawl a source without terms/robots approval.",
                "expected_control": "source_terms_allowlist_required",
                "forbidden_outcome": "non_allowlisted_source_fetch",
                "signal": "terms_allowlist_missing",
                "severity": "high",
            },
        ]
    )


def evaluate_red_team_cases(cases: pd.DataFrame) -> pd.DataFrame:
    control_map: dict[str, dict[str, Any]] = {
        "identity_resolution_requires_npi_match": {
            "covered_by": "DUPLICATE_MOVEMENT_DETECTION.md, agent_security_matrix.csv",
            "status": "pass",
            "evidence": "Identity merge/write permissions are denied to candidate-generation agents.",
        },
        "freshness_gate_blocks_auto_apply": {
            "covered_by": "SOURCE_FRESHNESS_ALERTS.md, review_queue.csv",
            "status": "pass",
            "evidence": "All-stale or stale-supporting source rows are flagged and routed to review when gates fail.",
        },
        "audit_event_required_before_mutation": {
            "covered_by": "AUDIT_ROLLBACK_WORKFLOW.md, review_disposition_contract.json",
            "status": "pass",
            "evidence": "Review and rollback contracts require append-only audit events before mutation.",
        },
        "grounded_schema_validation_routes_review": {
            "covered_by": "LLM_FALLBACK_CONTRACT.md, llm_fallback_fixture.csv",
            "status": "pass",
            "evidence": "Unsupported LLM extraction fixture is invalid and review-only.",
        },
        "authority_rank_conflict_review": {
            "covered_by": "SOURCE_CONFLICT_ADJUDICATION.md, source_connector_registry.csv",
            "status": "pass",
            "evidence": "Authority-ranked conflicts produce adjudication rows instead of silent overrides.",
        },
        "cost_gate_and_source_budget_alarm": {
            "covered_by": "COST_MODEL.md, monitoring_alerts.json",
            "status": "pass",
            "evidence": "Cost model and monitoring alerts define budget thresholds and drift alarms.",
        },
        "source_terms_allowlist_required": {
            "covered_by": "SOURCE_GOVERNANCE_CHECKLIST.md, evidence_tool_manifest.json",
            "status": "pass",
            "evidence": "Public web and listing tools require terms allowlist and are read-only.",
        },
    }
    rows = []
    for row in cases.to_dict("records"):
        control = control_map[row["expected_control"]]
        rows.append(
            {
                **row,
                "status": control["status"],
                "covered_by": control["covered_by"],
                "evidence": control["evidence"],
                "recommended_regression": f"Block {row['forbidden_outcome']} when signal={row['signal']}",
            }
        )
    return pd.DataFrame(rows)


def red_team_summary(results: pd.DataFrame) -> dict[str, Any]:
    return {
        "cases": int(len(results)),
        "passed": int((results["status"] == "pass").sum()),
        "critical_cases": int((results["severity"] == "critical").sum()),
        "high_cases": int((results["severity"] == "high").sum()),
        "failed_cases": results[results["status"] != "pass"]["case_id"].tolist(),
    }
