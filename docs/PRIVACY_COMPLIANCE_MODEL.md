# Privacy And Compliance Model

This model clarifies the data boundary for the provider-directory update pipeline. The system is designed for public provider/practice facts, not patient/member data, and production controls should enforce that boundary.

## Current Quality Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0

## Data Boundary

- Allowed entity types: provider, practice, source_evidence, review_disposition, audit_event
- Forbidden data classes: patient_name, member_id, claim_id, diagnosis, procedure, appointment, message_content, free_text_with_phi
- Production target: AWS with S3 immutable evidence/audit storage, Aurora/RDS workflow state, CloudWatch monitoring, IAM least privilege, and Secrets Manager.

## Controls

| Control ID | Domain | Control | Implementation | Evidence |
|---|---|---|---|---|
| pc_public_provider_data_only | data_minimization | Ingest only public provider/practice facts needed for directory accuracy. | Source connector registry excludes patient/member data and all parser schemas reject PHI-like fields. | SOURCE_CONNECTOR_REGISTRY.md |
| pc_no_patient_identifiers | schema | Candidate, evidence, review, and audit schemas contain provider/practice identifiers only. | Review disposition contract requires provider_id and reviewer_id, not patient/member identifiers. | review_disposition_contract.json |
| pc_least_privilege_roles | access_control | Agents use least-privilege AWS roles and cannot mutate directory data directly. | Source tools are read/append-only; scoring and review lanes are separated from write permissions. | AGENT_SECURITY_MATRIX.md |
| pc_secrets_manager | secrets | Source credentials and partner-feed secrets are not stored in prompts, docs, or code. | AWS Secrets Manager is the target production secrets boundary. | AWS_PRODUCTION_ARCHITECTURE.md |
| pc_immutable_audit | audit | Every update/review/rollback writes append-only audit evidence. | S3 audit bundles plus RDS audit event IDs; rollback never mutates prior audit events. | AUDIT_ROLLBACK_WORKFLOW.md |
| pc_retention_policy | retention | Raw source snapshots and audit bundles have explicit retention classes. | Hot normalized evidence retained for operational window; immutable audit retained for compliance window. | PRIVACY_COMPLIANCE_MODEL.md |
| pc_terms_and_rate_limits | source_compliance | Web sources require terms/robots approval and rate limits before crawling. | Terms allowlist required in evidence tool manifest for public web and third-party listings. | evidence_tool_manifest.json |
| pc_red_team_terms | safety_eval | Terms violations and audit gaps are red-team failure cases. | Failed critical red-team cases block production auto-apply or connector execution. | RED_TEAM_EVALS.md |

## Retention Policy

| Data Class | Suggested Retention | Rationale |
|---|---:|---|
| Raw public source snapshots | 90 days hot, archive after | Debug parser drift and source changes without indefinite crawl hoarding |
| Normalized evidence | 180 days | Supports review, active learning, and source freshness analysis |
| Review dispositions | 7 years or HealthLynked policy | Operational accountability and learning labels |
| Audit bundles | 7 years or HealthLynked policy | Compliance trail for applied changes and rollbacks |
| Secrets | Rotated per source policy | No secrets in prompts, docs, package, or logs |

## Enforcement Notes

- Any connector emitting forbidden data classes should fail schema validation and quarantine the payload.
- Human-review notes should use structured disposition reasons instead of open-ended PHI-bearing text.
- Directory mutation requires an audit event ID and reviewer/automation actor identity.
