# Review Disposition Contract And SLA Metrics

This experiment turns the static review dashboard into a production handoff. Reviewers do not just inspect rows; their decisions become validated disposition records, audit events, source feedback, and active-learning labels.

## Current Quality Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Review queue size: 37

## Disposition Contract

- Contract version: 2026-06-16
- Required fields: candidate_id, provider_id, field, reviewer_id, review_action, reviewed_at, disposition_reason, audit_event_id
- Allowed review actions: accept, reject, edit, defer, request_recrawl
- Audit rule: accept, reject, edit, defer, and recrawl decisions must produce append-only audit events.

## SLA And Workload Metrics

| Priority Band | Items | SLA Hours | Estimated Reviewer Hours | Risk Policy |
|---|---:|---:|---:|---|
| medium | 13 | 24 | 0.542 | standard_queue_review |
| low | 24 | 72 | 0.6 | standard_queue_review |

## Feedback Fixture

| Candidate ID | Provider | Field | Action | Source Feedback | SLA Status |
|---|---|---|---|---|---|
| review_fixture_000 | P0031 | address | accept | source_correct | within_sla |
| review_fixture_001 | P0066 | address | reject | source_wrong | within_sla |
| review_fixture_002 | P0050 | address | edit | source_correct | within_sla |
| review_fixture_003 | P0039 | address | defer | source_insufficient | within_sla |
| review_fixture_004 | P0003 | address | request_recrawl | source_stale | within_sla |
| review_fixture_005 | P0023 | address | accept | source_correct | within_sla |
| review_fixture_006 | P0017 | address | reject | source_wrong | within_sla |
| review_fixture_007 | P0046 | address | edit | source_correct | within_sla |

## AWS Production Handoff

- Authentication: AWS Cognito or workforce identity provider supplies `reviewer_id`.
- Queue state: SQS review tasks backed by Aurora/RDS candidate and disposition tables.
- Audit: every disposition writes an immutable S3 audit bundle plus RDS audit event ID.
- Learning: nightly Step Functions job aggregates reviewer outcomes by source, field, freshness, and confidence band.
- SLA monitoring: CloudWatch tracks high-priority breaches, backlog age, recrawl requests, and reviewer throughput.
