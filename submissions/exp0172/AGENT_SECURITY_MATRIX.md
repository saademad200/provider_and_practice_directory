# Agent Security And Least-Privilege Matrix

This experiment adds a security review artifact for the multi-agent production design. Each agent lane has a scoped AWS role, allowed/denied actions, data scope, review gate, risk, and compensating control.

## Current Pipeline Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Agent roles reviewed: 8

## Security Matrix

| Agent | AWS Role | Data Scope | Review Gate | Risk | Control |
|---|---|---|---|---|---|
| source_retrieval_agent | ProviderSourceReadRole | public provider source snapshots only | source_terms_approved | source terms violation or over-crawling | rate limits, robots/terms checklist, connector allowlist |
| evidence_normalization_agent | EvidenceNormalizeRole | public snippets and parser output | llm_cost_and_grounding_gate | unsupported LLM extraction or patient-data leakage | schema validation, evidence-span grounding, PHI redaction, Bedrock cost gate |
| identity_resolution_agent | IdentityCandidateRole | provider/practice identity features | identity_level_review_required | incorrect provider merge or affiliation move | NPI match requirement, duplicate/movement review queue, no auto-merge |
| source_conflict_agent | SourceConflictRole | normalized public evidence | equal_authority_or_conflict_review | silently discarding contradictory source values | field-specific authority matrix and conflict artifact |
| evidence_scoring_agent | CandidateScoringRole | evidence-derived features only | auto_apply_threshold_policy | unsafe auto-update or leakage | threshold policy, grouped CV, trajectory eval forbidden events |
| human_review_agent | DirectoryReviewerRole | review queue, evidence URLs, audit context | named_reviewer_identity | unattributed reviewer changes | reviewer identity, required disposition reason, immutable audit append |
| audit_rollback_agent | AuditRollbackRole | candidate, review, rollback event metadata | rollback_approval_required | audit tampering or unauthorized rollback | append-only events, evidence hashes, approval identity |
| monitoring_agent | DirectoryMonitoringRole | aggregate operational metrics | alert_owner_configured | silent connector/source drift | freshness, false-positive, review backlog, and cost-drift alerts |

## Production Principles

- Default source and connector agents to read-only or append-only permissions.
- Separate candidate generation from directory write permissions.
- Block identity deletes, inactive-provider writes, and rollbacks without named review/approval.
- Keep raw evidence and audit bundles immutable in S3.
- Log every tool invocation and run trajectory evals before production writes.
- Store credentials in AWS Secrets Manager, never prompts, docs, or scripts.
