from __future__ import annotations

from typing import Any

import pandas as pd


def least_privilege_matrix() -> pd.DataFrame:
    rows: list[dict[str, Any]] = [
        {
            "agent": "source_retrieval_agent",
            "aws_role": "ProviderSourceReadRole",
            "allowed_actions": "s3:PutObject raw-evidence/*|secretsmanager:GetSecretValue approved-connectors|logs:PutLogEvents",
            "denied_actions": "rds:UpdateTable|s3:DeleteObject|bedrock:InvokeModel",
            "data_scope": "public provider source snapshots only",
            "review_gate": "source_terms_approved",
            "risk": "source terms violation or over-crawling",
            "control": "rate limits, robots/terms checklist, connector allowlist",
        },
        {
            "agent": "evidence_normalization_agent",
            "aws_role": "EvidenceNormalizeRole",
            "allowed_actions": "s3:GetObject raw-evidence/*|s3:PutObject normalized-evidence/*|bedrock:InvokeModel gated-fallback",
            "denied_actions": "rds:UpdateDirectory|s3:DeleteObject",
            "data_scope": "public snippets and parser output",
            "review_gate": "llm_cost_and_grounding_gate",
            "risk": "unsupported LLM extraction or patient-data leakage",
            "control": "schema validation, evidence-span grounding, PHI redaction, Bedrock cost gate",
        },
        {
            "agent": "identity_resolution_agent",
            "aws_role": "IdentityCandidateRole",
            "allowed_actions": "rds:ReadDirectory|rds:WriteIdentityCandidates",
            "denied_actions": "rds:MergeProviderIdentity|rds:DeleteProvider",
            "data_scope": "provider/practice identity features",
            "review_gate": "identity_level_review_required",
            "risk": "incorrect provider merge or affiliation move",
            "control": "NPI match requirement, duplicate/movement review queue, no auto-merge",
        },
        {
            "agent": "source_conflict_agent",
            "aws_role": "SourceConflictRole",
            "allowed_actions": "rds:ReadEvidence|s3:PutObject conflict-artifacts/*",
            "denied_actions": "rds:ApplyDirectoryUpdate",
            "data_scope": "normalized public evidence",
            "review_gate": "equal_authority_or_conflict_review",
            "risk": "silently discarding contradictory source values",
            "control": "field-specific authority matrix and conflict artifact",
        },
        {
            "agent": "evidence_scoring_agent",
            "aws_role": "CandidateScoringRole",
            "allowed_actions": "rds:WriteCandidateUpdates|s3:PutObject metrics/*",
            "denied_actions": "rds:ApplyIdentityDelete|rds:ReadGoldLabels",
            "data_scope": "evidence-derived features only",
            "review_gate": "auto_apply_threshold_policy",
            "risk": "unsafe auto-update or leakage",
            "control": "threshold policy, grouped CV, trajectory eval forbidden events",
        },
        {
            "agent": "human_review_agent",
            "aws_role": "DirectoryReviewerRole",
            "allowed_actions": "rds:ReadReviewQueue|rds:WriteReviewDisposition|s3:GetObject evidence-bundles/*",
            "denied_actions": "s3:DeleteObject audit/*|rds:BypassReview",
            "data_scope": "review queue, evidence URLs, audit context",
            "review_gate": "named_reviewer_identity",
            "risk": "unattributed reviewer changes",
            "control": "reviewer identity, required disposition reason, immutable audit append",
        },
        {
            "agent": "audit_rollback_agent",
            "aws_role": "AuditRollbackRole",
            "allowed_actions": "s3:PutObject audit/*|rds:WriteAuditEvent|rds:WriteRollbackPlan",
            "denied_actions": "s3:DeleteObject audit/*|rds:MutatePriorAuditEvent",
            "data_scope": "candidate, review, rollback event metadata",
            "review_gate": "rollback_approval_required",
            "risk": "audit tampering or unauthorized rollback",
            "control": "append-only events, evidence hashes, approval identity",
        },
        {
            "agent": "monitoring_agent",
            "aws_role": "DirectoryMonitoringRole",
            "allowed_actions": "cloudwatch:PutMetricData|sns:Publish owned-alert-topics|rds:ReadOperationalMetrics",
            "denied_actions": "rds:ApplyDirectoryUpdate|secretsmanager:GetSecretValue",
            "data_scope": "aggregate operational metrics",
            "review_gate": "alert_owner_configured",
            "risk": "silent connector/source drift",
            "control": "freshness, false-positive, review backlog, and cost-drift alerts",
        },
    ]
    return pd.DataFrame(rows)
