from __future__ import annotations

from typing import Any

import pandas as pd


def provider_directory_skill_candidates() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "skill_candidate": "checking-source-health",
                "owner": "source_ops",
                "authority_tier": "read-only",
                "trigger": "source freshness, connector health, terms allowlist, source outage",
                "anti_trigger": "candidate scoring or directory mutation",
                "required_eval": "positive/negative trigger tests, connector fixture, no-secrets scan",
                "deterministic_assets": "source_connector_registry.csv, connector_health_check_fixture.csv",
            },
            {
                "skill_candidate": "normalizing-provider-evidence",
                "owner": "data_quality",
                "authority_tier": "draft-only",
                "trigger": "normalize phone/address/specialty/license evidence",
                "anti_trigger": "apply directory update",
                "required_eval": "golden normalization fixtures and trajectory evals",
                "deterministic_assets": "specialty_normalization_fixture.csv, bedrock_extraction_contract.json",
            },
            {
                "skill_candidate": "resolving-provider-identity",
                "owner": "identity_ops",
                "authority_tier": "draft-only",
                "trigger": "duplicate provider, NPI match, practice movement, rebrand",
                "anti_trigger": "identity merge without reviewer approval",
                "required_eval": "red-team wrong-provider merge, NPI mismatch fixture",
                "deterministic_assets": "duplicate_candidates.csv, provider_movement_candidates.csv",
            },
            {
                "skill_candidate": "routing-human-review",
                "owner": "directory_ops",
                "authority_tier": "draft-only",
                "trigger": "review queue, SLA, disposition, reviewer feedback",
                "anti_trigger": "source crawling or model tuning",
                "required_eval": "review disposition contract validation and SLA metrics",
                "deterministic_assets": "review_disposition_contract.json, review_sla_metrics.csv",
            },
            {
                "skill_candidate": "auditing-and-rollback",
                "owner": "compliance",
                "authority_tier": "action-allowed-after-approval",
                "trigger": "audit event, rollback plan, false positive auto-apply",
                "anti_trigger": "new candidate generation",
                "required_eval": "audit-gap red-team eval, rollback fixture, approval gate",
                "deterministic_assets": "audit_events.jsonl, rollback_plan.csv",
            },
            {
                "skill_candidate": "evaluating-provider-directory-pipeline",
                "owner": "ml_ops",
                "authority_tier": "read-only",
                "trigger": "CV metrics, red-team eval, readiness score, verifier check",
                "anti_trigger": "manual review disposition",
                "required_eval": "grouped CV, trajectory eval, red-team eval, package verifier",
                "deterministic_assets": "metrics.json, trajectory_eval_results.csv, red_team_eval_results.csv",
            },
        ]
    )


def skill_eval_coverage(candidates: pd.DataFrame) -> dict[str, Any]:
    return {
        "skill_candidates": int(len(candidates)),
        "read_only": int((candidates["authority_tier"] == "read-only").sum()),
        "draft_only": int((candidates["authority_tier"] == "draft-only").sum()),
        "action_allowed_after_approval": int((candidates["authority_tier"] == "action-allowed-after-approval").sum()),
        "coverage_requirements": [
            "3 positive and 3 negative trigger cases per skill candidate",
            "trajectory eval for tool sequence where side effects matter",
            "regression check against existing package verifier",
            "token-budget check by keeping bulky context in references/assets",
            "human approval before any action-allowed workflow",
        ],
    }
