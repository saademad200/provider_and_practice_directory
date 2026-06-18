# Audit And Rollback Workflow

This experiment turns the audit trail into a concrete append-only event contract. Every candidate update gets an event id, evidence hash, before/after value, source list, policy version, and rollback status.

## Current Pipeline Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Audit events emitted: 57
- Rollback commands emitted: 20

## Event Contract

Required event fields:

- `schema_version`
- `event_id`
- `event_type`
- `created_at`
- `pipeline_version`
- `provider_id`
- `practice_id`
- `field`
- `old_value`
- `new_value`
- `decision`
- `confidence`
- `review_reason_code`
- `sources`
- `evidence_urls`
- `evidence_hash`
- `freshness_status`
- `rollback_status`

## Rollback Policy

- Only auto-applied updates produce executable rollback rows.
- Review-only candidates remain `not_applied_yet` until a reviewer accepts them.
- Rollback requires an approval identity and a typed rollback reason.
- Rollback writes a new audit event; it never mutates the original event.
- Evidence hashes let operators prove which source snapshot supported the original decision.

## AWS Storage Pattern

- Raw source snapshots and JSONL audit bundles: Amazon S3 with retention policy.
- Queryable event table: Aurora PostgreSQL or DynamoDB depending on product workflow needs.
- Reviewer actions: Step Functions task token or application-level event appended to the same audit stream.
