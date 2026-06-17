# Capability Profiles And Skill Orchestration

This artifact translates the generated Agent Skills library into deployable capability profiles and a Step Functions-style orchestration DAG. The cloud target is AWS.

## Current Quality Context

- F1: 0.93913
- Precision: 0.947368
- Recall: 0.931034
- Auto-apply precision: 1.0

## Capability Profiles

| Agent | Skill | Authority Tier | AWS Runtime | Human Gate |
|---|---|---|---|---|
| source_retrieval_agent | checking-source-health | read-only | AWS Step Functions task with Lambda/ECS connector worker | False |
| evidence_normalization_agent | normalizing-provider-evidence | draft-only | AWS Step Functions task with ECS parser worker | False |
| identity_resolution_agent | resolving-provider-identity | draft-only | AWS Step Functions task with ECS matching worker | False |
| evidence_scoring_agent | routing-human-review | draft-only | AWS Step Functions task with Lambda scorer and SQS review handoff | False |
| audit_and_rollback_agent | auditing-and-rollback | action-allowed-after-approval | AWS Step Functions approval-gated task with DynamoDB audit ledger | True |
| evaluation_agent | evaluating-provider-directory-pipeline | read-only | AWS Batch/ECS eval job with S3 artifact outputs | False |

## Orchestration DAG

| Step | Skill | Message In | Message Out | Downstream | Blocking Gate |
|---:|---|---|---|---|---|
| 1 | checking-source-health | source_batch_requested | source_health_verified | normalizing-provider-evidence | required eval passes |
| 2 | normalizing-provider-evidence | raw_snapshot_ready | normalized_evidence_ready | resolving-provider-identity | required eval passes |
| 3 | resolving-provider-identity | normalized_evidence_ready | identity_resolution_ready | routing-human-review | required eval passes |
| 4 | routing-human-review | candidate_updates_ready | review_or_auto_apply_batch_ready | auditing-and-rollback | no auto-apply for identity or high-risk fields |
| 5 | auditing-and-rollback | approved_update_batch_ready | audit_and_rollback_artifacts_ready | evaluating-provider-directory-pipeline | human approval plus rollback-plan precheck |
| 6 | evaluating-provider-directory-pipeline | evaluation_artifacts_ready | release_verification_ready | release_artifacts | required eval passes |

## Operating Principle

The workflow treats S3 versioned artifacts as the file message bus and EventBridge events as status signals. Step Functions owns ordering and retries; each skill owns procedural know-how, authority boundaries, deterministic assets, and required evals.
