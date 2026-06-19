# 90-Day Implementation Roadmap

## Days 0-15

- Map HealthLynked provider/practice schema.
- Configure AWS account boundary, IAM, S3 evidence storage, Secrets Manager.
- Run MVP on de-identified sample records in no-write shadow mode.
- Approve source registry and field-risk policy.
- Establish reviewer disposition labels and the initial field-level launch matrix.

## Days 16-35

- Harden NPPES, state-board, practice website, health-system, and CMS/public connectors.
- Implement address, phone, specialty, provider name, practice name, website, affiliation, and status normalization.
- Build duplicate, movement, practice-location, inactive-provider, and source-conflict queues.

## Days 36-60

- Deploy review dashboard.
- Capture reviewer dispositions and SLA metrics.
- Store append-only audit events and rollback plans.
- Calibrate confidence thresholds against reviewer outcomes and holdout replay.
- Quarantine weak connectors and keep insufficient-sample fields review-only.

## Days 61-90

- Deploy AWS EventBridge and Step Functions orchestration.
- Run connector/scoring workers on Lambda/ECS or AWS Batch.
- Gate Amazon Bedrock extraction to messy approved pages only.
- Graduate approved low-risk fields from shadow mode into limited safe auto-apply.
- Keep identity, NPI, inactive-status, affiliation, and source-conflict changes human-review-first.

## Success Metrics

- Auto-apply precision `>= 0.98`
- `100%` evidence traceability
- `100%` applied-update audit coverage
- Review workload reduced by routing only risky/uncertain cases
- Cost tracked per 1,000 provider records
