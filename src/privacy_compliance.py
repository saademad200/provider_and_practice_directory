from __future__ import annotations

from typing import Any

import pandas as pd


def privacy_controls() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "control_id": "pc_public_provider_data_only",
                "domain": "data_minimization",
                "control": "Ingest only public provider/practice facts needed for directory accuracy.",
                "implementation": "Source connector registry excludes patient/member data and all parser schemas reject PHI-like fields.",
                "evidence_artifact": "SOURCE_CONNECTOR_REGISTRY.md",
            },
            {
                "control_id": "pc_no_patient_identifiers",
                "domain": "schema",
                "control": "Candidate, evidence, review, and audit schemas contain provider/practice identifiers only.",
                "implementation": "Review disposition contract requires provider_id and reviewer_id, not patient/member identifiers.",
                "evidence_artifact": "review_disposition_contract.json",
            },
            {
                "control_id": "pc_least_privilege_roles",
                "domain": "access_control",
                "control": "Agents use least-privilege AWS roles and cannot mutate directory data directly.",
                "implementation": "Source tools are read/append-only; scoring and review lanes are separated from write permissions.",
                "evidence_artifact": "AGENT_SECURITY_MATRIX.md",
            },
            {
                "control_id": "pc_secrets_manager",
                "domain": "secrets",
                "control": "Source credentials and partner-feed secrets are not stored in prompts, docs, or code.",
                "implementation": "AWS Secrets Manager is the target production secrets boundary.",
                "evidence_artifact": "AWS_PRODUCTION_ARCHITECTURE.md",
            },
            {
                "control_id": "pc_immutable_audit",
                "domain": "audit",
                "control": "Every update/review/rollback writes append-only audit evidence.",
                "implementation": "S3 audit bundles plus RDS audit event IDs; rollback never mutates prior audit events.",
                "evidence_artifact": "AUDIT_ROLLBACK_WORKFLOW.md",
            },
            {
                "control_id": "pc_retention_policy",
                "domain": "retention",
                "control": "Raw source snapshots and audit bundles have explicit retention classes.",
                "implementation": "Hot normalized evidence retained for operational window; immutable audit retained for compliance window.",
                "evidence_artifact": "PRIVACY_COMPLIANCE_MODEL.md",
            },
            {
                "control_id": "pc_terms_and_rate_limits",
                "domain": "source_compliance",
                "control": "Web sources require terms/robots approval and rate limits before crawling.",
                "implementation": "Terms allowlist required in evidence tool manifest for public web and third-party listings.",
                "evidence_artifact": "evidence_tool_manifest.json",
            },
            {
                "control_id": "pc_red_team_terms",
                "domain": "safety_eval",
                "control": "Terms violations and audit gaps are red-team failure cases.",
                "implementation": "Failed critical red-team cases block production auto-apply or connector execution.",
                "evidence_artifact": "RED_TEAM_EVALS.md",
            },
        ]
    )


def data_minimization_schema() -> dict[str, Any]:
    return {
        "schema_version": "2026-06-16",
        "allowed_entity_types": ["provider", "practice", "source_evidence", "review_disposition", "audit_event"],
        "forbidden_data_classes": [
            "patient_name",
            "member_id",
            "claim_id",
            "diagnosis",
            "procedure",
            "appointment",
            "message_content",
            "free_text_with_phi",
        ],
        "allowed_fields": {
            "provider": ["provider_id", "npi", "provider_name", "specialty", "license_status"],
            "practice": ["practice_id", "practice_name", "address", "phone", "accepting_new_patients"],
            "source_evidence": ["connector_id", "source_url", "retrieved_at", "field", "value", "freshness_status"],
            "review_disposition": ["candidate_id", "provider_id", "reviewer_id", "review_action", "disposition_reason", "audit_event_id"],
            "audit_event": ["audit_event_id", "candidate_id", "old_value", "new_value", "source_hash", "created_at"],
        },
        "production_storage": {
            "raw_public_evidence": "S3 immutable source snapshots",
            "normalized_evidence": "S3/Aurora operational tables",
            "review_state": "Aurora/RDS with reviewer identity",
            "audit_bundles": "S3 object lock or equivalent immutable retention",
            "secrets": "AWS Secrets Manager",
        },
    }
