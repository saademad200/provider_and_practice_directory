from __future__ import annotations

from typing import Any

import pandas as pd


OWNER_TO_AGENT = {
    "source_ops": "source_retrieval_agent",
    "data_quality": "evidence_normalization_agent",
    "identity_ops": "identity_resolution_agent",
    "directory_ops": "evidence_scoring_agent",
    "compliance": "audit_and_rollback_agent",
    "ml_ops": "evaluation_agent",
}

OWNER_TO_AWS_RUNTIME = {
    "source_ops": "AWS Step Functions task with Lambda/ECS connector worker",
    "data_quality": "AWS Step Functions task with ECS parser worker",
    "identity_ops": "AWS Step Functions task with ECS matching worker",
    "directory_ops": "AWS Step Functions task with Lambda scorer and SQS review handoff",
    "compliance": "AWS Step Functions approval-gated task with DynamoDB audit ledger",
    "ml_ops": "AWS Batch/ECS eval job with S3 artifact outputs",
}

SKILL_SEQUENCE = [
    "checking-source-health",
    "normalizing-provider-evidence",
    "resolving-provider-identity",
    "routing-human-review",
    "auditing-and-rollback",
    "evaluating-provider-directory-pipeline",
]


def build_capability_profiles(skill_candidates: pd.DataFrame) -> list[dict[str, Any]]:
    profiles: list[dict[str, Any]] = []
    for row in skill_candidates.to_dict("records"):
        owner = row["owner"]
        profiles.append(
            {
                "agent": OWNER_TO_AGENT.get(owner, f"{owner}_agent"),
                "skill": row["skill_candidate"],
                "owner": owner,
                "authority_tier": row["authority_tier"],
                "aws_runtime": OWNER_TO_AWS_RUNTIME.get(owner, "AWS Step Functions task"),
                "inputs": inputs_for_skill(row["skill_candidate"]),
                "outputs": outputs_for_skill(row["skill_candidate"]),
                "allowed_actions": allowed_actions(row["authority_tier"]),
                "forbidden_actions": forbidden_actions(row["authority_tier"]),
                "required_eval": row["required_eval"],
                "deterministic_assets": row["deterministic_assets"],
                "human_gate": row["authority_tier"] == "action-allowed-after-approval",
            }
        )
    return profiles


def build_orchestration_dag(skill_candidates: pd.DataFrame) -> pd.DataFrame:
    known = set(skill_candidates["skill_candidate"])
    rows: list[dict[str, Any]] = []
    for idx, skill in enumerate(SKILL_SEQUENCE):
        if skill not in known:
            continue
        downstream = SKILL_SEQUENCE[idx + 1] if idx + 1 < len(SKILL_SEQUENCE) else "release_artifacts"
        rows.append(
            {
                "step": idx + 1,
                "skill": skill,
                "agent": OWNER_TO_AGENT.get(skill_candidates.loc[skill_candidates["skill_candidate"] == skill, "owner"].iloc[0]),
                "message_in": message_in(skill),
                "message_out": message_out(skill),
                "downstream": downstream,
                "aws_control_plane": "AWS Step Functions",
                "artifact_bus": "S3 versioned artifacts plus EventBridge status events",
                "blocking_gate": blocking_gate(skill),
            }
        )
    return pd.DataFrame(rows)


def inputs_for_skill(skill: str) -> list[str]:
    return {
        "checking-source-health": ["source_connector_registry", "connector_health_check_fixture", "freshness_summary"],
        "normalizing-provider-evidence": ["raw_source_snapshot", "specialty_alias_table", "address_normalization_rules"],
        "resolving-provider-identity": ["provider_record", "normalized_evidence_rows", "historical_directory_state"],
        "routing-human-review": ["candidate_updates", "field_risk_policy", "review_disposition_contract"],
        "auditing-and-rollback": ["applied_updates", "audit_events", "rollback_plan"],
        "evaluating-provider-directory-pipeline": ["candidate_updates", "oof_predictions", "red_team_results"],
    }.get(skill, ["package_artifacts"])


def outputs_for_skill(skill: str) -> list[str]:
    return {
        "checking-source-health": ["connector_health_status", "source_reliability_flags"],
        "normalizing-provider-evidence": ["normalized_evidence_rows", "parser_warnings"],
        "resolving-provider-identity": ["identity_match_decision", "duplicate_candidates", "movement_candidates"],
        "routing-human-review": ["auto_apply_updates", "review_queue", "review_reason_codes"],
        "auditing-and-rollback": ["audit_events", "rollback_plan", "post_apply_checks"],
        "evaluating-provider-directory-pipeline": ["cv_metrics", "skill_eval_results", "package_verification"],
    }.get(skill, ["updated_artifacts"])


def allowed_actions(authority_tier: str) -> list[str]:
    if authority_tier == "read-only":
        return ["read_package_artifacts", "emit_diagnostics"]
    if authority_tier == "draft-only":
        return ["read_package_artifacts", "write_candidate_artifacts", "route_to_review"]
    return ["read_package_artifacts", "draft_action_plan", "execute_only_after_human_approval"]


def forbidden_actions(authority_tier: str) -> list[str]:
    base = ["access_patient_data", "drop_audit_trail", "bypass_source_authority_policy"]
    if authority_tier == "read-only":
        return base + ["write_directory_record", "create_review_decision"]
    if authority_tier == "draft-only":
        return base + ["auto_apply_update", "mutate_production_directory"]
    return base + ["execute_without_approval", "delete_audit_records"]


def message_in(skill: str) -> str:
    return {
        "checking-source-health": "source_batch_requested",
        "normalizing-provider-evidence": "raw_snapshot_ready",
        "resolving-provider-identity": "normalized_evidence_ready",
        "routing-human-review": "candidate_updates_ready",
        "auditing-and-rollback": "approved_update_batch_ready",
        "evaluating-provider-directory-pipeline": "evaluation_artifacts_ready",
    }.get(skill, "artifact_ready")


def message_out(skill: str) -> str:
    return {
        "checking-source-health": "source_health_verified",
        "normalizing-provider-evidence": "normalized_evidence_ready",
        "resolving-provider-identity": "identity_resolution_ready",
        "routing-human-review": "review_or_auto_apply_batch_ready",
        "auditing-and-rollback": "audit_and_rollback_artifacts_ready",
        "evaluating-provider-directory-pipeline": "release_verification_ready",
    }.get(skill, "artifact_processed")


def blocking_gate(skill: str) -> str:
    if skill == "auditing-and-rollback":
        return "human approval plus rollback-plan precheck"
    if skill == "routing-human-review":
        return "no auto-apply for identity or high-risk fields"
    return "required eval passes"
