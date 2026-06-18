# Production Monitoring And Alert Thresholds

This document defines the production control loop for the provider-directory pipeline. The goal is to catch source failures, unsafe automation, stale evidence, review backlog growth, and cost drift before they affect patients.

## Current Baseline Snapshot

- Candidate updates: 57
- Auto-apply count: 3
- Review count: 55
- Auto-apply precision proxy: 1.0
- All-stale candidate share: 0.5439
- Cost per correct update: $0.005609

## Alerts

| Metric | Threshold | Severity | Owner | Action |
|---|---|---|---|---|
| auto_apply_acceptance_rate | < 0.995 over rolling 7 days | critical | data_quality | Pause auto-apply for affected field/source, route to review, inspect recent accepted updates. |
| all_stale_candidate_share | > 0.25 of candidates | high | data_platform | Trigger AWS EventBridge recrawl/reingest jobs and lower auto-apply eligibility until freshness recovers. |
| source_coverage_rate | < 0.80 for any primary source | high | connectors | Check connector failures, API changes, robots/legal constraints, and retry queues. |
| review_backlog_age_p95_hours | > 72 hours | medium | operations | Increase reviewer allocation or tighten auto-apply expansion candidates with strong active-learning evidence. |
| cost_per_1000_records | > planned budget by 20% | medium | platform_finops | Inspect LLM call rate, manual review rate, failed recrawls, and low-value source usage. |
| false_positive_review_rate | > 0.10 by source/field | high | data_science | Downweight source-field pair or require additional corroboration in shadow mode. |

## CloudWatch Dashboard Sections

1. Source health: coverage, freshness, connector failures, retries, dead-letter queue depth.
2. Quality: auto-apply acceptance, review rejection rate, false positive clusters, field-level drift.
3. Operations: review backlog, p95 age, priority-band distribution, reviewer throughput.
4. Cost: cost per 1,000 records, LLM call rate, crawl retries, manual review estimate.
5. Audit: update volume, rollback count, evidence snapshot availability, policy version.

## AWS Implementation

- Emit pipeline events from Step Functions tasks to CloudWatch metrics.
- Store failed source tasks in SQS dead-letter queues.
- Write raw evidence snapshots to S3 with pipeline version and source timestamp.
- Use EventBridge rules to trigger recrawls when stale-source share breaches threshold.
- Store reviewer outcomes in Aurora/RDS and aggregate nightly for active learning.
