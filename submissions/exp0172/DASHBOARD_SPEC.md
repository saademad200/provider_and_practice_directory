# Human Review Dashboard Specification

This dashboard is the operational surface for uncertain provider-directory updates. It should let reviewers accept, reject, edit, defer, or request recrawl while preserving an audit trail.

## Dashboard Goals

- Show the highest-risk and most ambiguous updates first.
- Make evidence inspection fast: old value, proposed value, sources, URLs, freshness, and reason codes in one row.
- Capture reviewer outcomes that feed the active-learning loop.
- Separate safe auto-apply monitoring from manual review work.
- Keep cost visible: source usage, stale evidence, and review volume should be measurable.

## Current Queue Snapshot

- Candidate updates: 58
- Auto-apply queue: 20
- Manual review queue: 38
- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0

## Review Queue By Field

| Field | Review Items |
|---|---:|
| accepting_new_patients | 2 |
| address | 13 |
| phone | 18 |
| specialty | 5 |

## Top Review Items

| Provider | Field | Priority Score | Freshness | Reason | Sources |
|---|---|---:|---|---|---|
| P0031 | address | 0.556 | all_stale | practice_peer_mismatch | health_system, nppes, practice_website |
| P0066 | address | 0.556 | partially_stale | practice_peer_mismatch | health_system, nppes, practice_website |
| P0050 | address | 0.556 | partially_stale | practice_peer_mismatch | health_system, nppes, practice_website |
| P0051 | address | 0.556 | all_stale | practice_peer_mismatch | business_listing, health_system, nppes |
| P0039 | address | 0.556 | all_stale | practice_peer_mismatch | health_system, nppes, practice_website |
| P0003 | address | 0.556 | all_stale | practice_peer_mismatch | health_system, nppes, practice_website |
| P0023 | address | 0.556 | partially_stale | practice_peer_mismatch | health_system, nppes, practice_website |
| P0017 | address | 0.556 | all_stale | practice_peer_mismatch | health_system, nppes, practice_website |
| P0046 | address | 0.516 | all_stale | insufficient_auto_sources | health_system, nppes |

## Required Views

1. Review Queue: sortable table with priority, field, confidence, freshness, reason, and evidence.
2. Evidence Drawer: source snippets, URLs, source age, normalized value, and raw value.
3. Provider Timeline: current value, proposed changes, past accepted/rejected decisions, and audit log.
4. Source Health: coverage, stale-source rates, connector failures, and missing-source diagnostics.
5. Calibration: reviewer accept rates by source/field/freshness and recommended learning actions.
6. Auto-Apply Monitor: recently auto-applied updates with rollback/export controls.

## Data Contract

| Column | Type | Required | Purpose |
|---|---|---|---|
| provider_id | string | yes | Stable provider identifier. |
| practice_id | string | yes | Practice grouping for peer checks. |
| field | enum | yes | Changed field: phone, address, specialty, license_status, accepting_new_patients. |
| old_value | string | yes | Current HealthLynked value. |
| proposed_value | string | yes | Evidence-supported replacement value. |
| confidence | float | yes | Pipeline confidence score. |
| decision | enum | yes | auto_apply or review. |
| review_priority_score | float | yes | Sort order for manual review. |
| review_priority_band | enum | yes | low, medium, high. |
| review_reason_code | pipe-delimited string | yes | Why the item is auto-applied or reviewed. |
| sources | pipe-delimited string | yes | Supporting source names. |
| evidence_urls | pipe-delimited URL string | yes | Evidence drill-down links. |
| freshness_status | enum | yes | fresh, partially_stale, all_stale, missing. |
| stale_sources | pipe-delimited string | no | Sources exceeding freshness SLA. |
| practice_consensus_status | enum | yes | peer_match, peer_mismatch, no_peers, not_checked. |

## Reviewer Actions

| Action | Meaning | Learning Signal |
|---|---|---|
| Accept | Proposed value is correct and should update the directory | Positive label for sources, field, confidence, and freshness state |
| Reject | Proposed value is incorrect | Negative label for source/field/freshness calibration |
| Edit | Reviewer supplies a corrected value | Positive label for field need; negative/partial label for exact proposed value |
| Defer | Needs more evidence or outreach | Source coverage and freshness gap signal |
| Request recrawl | Evidence is stale or insufficient | Connector freshness/SLA signal |

## AWS Implementation Sketch

- Frontend: AWS Amplify or ECS/Fargate-hosted app.
- Review task queue: Amazon SQS.
- Candidate/review state: Aurora PostgreSQL or RDS PostgreSQL.
- Evidence files and audit bundles: Amazon S3.
- Source and review metrics: CloudWatch dashboards.
- Nightly learning aggregation: Step Functions plus Glue or Batch.
