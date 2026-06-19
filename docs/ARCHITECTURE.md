# Provider Directory Update Pipeline Architecture

## Objective

Maintain provider and practice directory accuracy with a repeatable, cost-aware, auditable evidence pipeline.

## Submission Mode

This is an Option C Hybrid submission: the repository includes a runnable local prototype and a production architecture for HealthLynked-scale operation.

## Local Prototype Flow

1. Ingest current directory records.
2. Collect evidence from NPPES, state license sources, practice websites, health-system pages, and guarded business-listing fallback evidence.
3. Normalize phones, addresses, specialties, license status, and patient-acceptance values.
4. Resolve provider/practice identity using stable provider IDs, NPI-like identifiers, practice IDs, and normalized fields.
5. Generate candidate updates from weighted source agreement.
6. Route each update to auto-apply or review using field-specific confidence thresholds, source-count gates, freshness metadata, and practice-peer safety checks.
7. Emit audit logs with old value, proposed value, confidence, source list, evidence URLs, review reasons, priority drivers, and pipeline version.

## Current Best Local Proxy

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Auto-apply count: 3
- Review count: 55
- Prototype evidence-only cost per correct update: $0.005836
- Estimated evidence cost: $0.321

## AWS Production Target

The production version should use EventBridge Scheduler for recurring refreshes, Step Functions for orchestration, Glue or Batch for bulk source processing, S3 for immutable evidence snapshots, DynamoDB/RDS for operational state, SQS for review tasks, Bedrock only as an optional messy-page extraction fallback, and CloudWatch for freshness/cost/quality monitoring.

## Safety Design

- High-risk fields use stricter thresholds.
- Phone and address updates require multi-source evidence and practice-peer checks.
- Business-listing evidence is allowed only as a guarded fallback for phone/address, only when fresh, and at low source weight.
- Auto-apply requires stronger evidence than review routing.
- Human review receives stale, borderline, conflicting, peer-mismatched, and high-risk updates with citations.
