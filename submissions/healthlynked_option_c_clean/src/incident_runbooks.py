from __future__ import annotations

import pandas as pd


def incident_runbooks() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "incident": "false_positive_auto_apply",
                "trigger": "reviewer appeal, rollback request, or post-update audit sampling finds incorrect applied value",
                "severity": "high",
                "owner": "directory_ops_lead",
                "first_response_minutes": 30,
                "containment": "pause auto-apply for affected field/source pair; enqueue rollback plan rows",
                "diagnosis": "inspect audit event, evidence_hash, source_conflict row, trajectory eval, and source freshness",
                "recovery": "execute approved rollback, append rollback audit event, notify downstream consumers",
                "prevention": "raise field threshold or source min-count; add case to regression/case-study suite",
            },
            {
                "incident": "source_connector_outage",
                "trigger": "connector failure rate or freshness SLA breach exceeds monitoring threshold",
                "severity": "medium",
                "owner": "source_retrieval_owner",
                "first_response_minutes": 60,
                "containment": "disable affected source in scoring or mark as stale; block auto-apply if min-source policy fails",
                "diagnosis": "check HTTP status, rate limits, source terms, auth secret, and recent parser changes",
                "recovery": "restore connector, backfill missed snapshots, rerun missing-source robustness check",
                "prevention": "add retry/backoff, source health alert, and alternate source path",
            },
            {
                "incident": "llm_grounding_failure",
                "trigger": "trajectory eval or validation finds unsupported evidence span or LLM call without cost gate",
                "severity": "high",
                "owner": "ml_platform_owner",
                "first_response_minutes": 30,
                "containment": "disable Bedrock fallback for affected parser route; route all derived rows to review",
                "diagnosis": "inspect prompt version, schema version, source snippet, validation errors, and cost gate",
                "recovery": "patch schema/prompt, regenerate affected evidence, require reviewer confirmation",
                "prevention": "add fixture to LLM fallback benchmark and forbidden trajectory event tests",
            },
            {
                "incident": "audit_gap_detected",
                "trigger": "candidate update, auto-apply row, or reviewer disposition has no matching audit event",
                "severity": "critical",
                "owner": "compliance_owner",
                "first_response_minutes": 15,
                "containment": "stop production writes; freeze affected workflow run; preserve raw logs",
                "diagnosis": "join candidate IDs against audit_events.jsonl and Step Functions trace IDs",
                "recovery": "reconstruct missing append-only event from immutable evidence bundle; document exception",
                "prevention": "make write path transactionally require audit event ID before directory mutation",
            },
            {
                "incident": "identity_merge_error",
                "trigger": "duplicate/provider movement review identifies wrong NPI or practice affiliation",
                "severity": "critical",
                "owner": "identity_resolution_owner",
                "first_response_minutes": 30,
                "containment": "block identity-level auto-merge class; move related candidates to manual review",
                "diagnosis": "compare NPI, address, practice history, phone, specialty, and reviewer notes",
                "recovery": "split identity, restore prior practice affiliation, append corrective audit event",
                "prevention": "tighten NPI requirement, add negative fixture, and require two-authority confirmation",
            },
        ]
    )
