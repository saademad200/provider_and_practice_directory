# 90-Day Implementation Roadmap

## Days 0-15

- Map HealthLynked provider/practice schema.
- Configure AWS account boundary, IAM, S3 evidence storage, Secrets Manager.
- Run MVP on de-identified sample records.
- Approve source registry and field-risk policy.

## Days 16-35

- Harden NPPES, state-board, practice website, health-system, and CMS/public connectors.
- Implement address, phone, specialty, provider name, practice name, website, affiliation, and status normalization.
- Build duplicate, movement, practice-location, inactive-provider, and source-conflict queues.

## Days 36-60

- Deploy review dashboard.
- Capture reviewer dispositions and SLA metrics.
- Store append-only audit events and rollback plans.
- Calibrate confidence thresholds against reviewer outcomes.

## Days 61-90

- Deploy AWS EventBridge and Step Functions orchestration.
- Run connector/scoring workers on Lambda/ECS or AWS Batch.
- Gate Amazon Bedrock extraction to messy approved pages only.
- Run shadow-mode pilot, then limited safe auto-apply for low-risk fields.

## Success Metrics

- Auto-apply precision `>= 0.98`
- `100%` evidence traceability
- `100%` applied-update audit coverage
- Review workload reduced by routing only risky/uncertain cases
- Cost tracked per 1,000 provider records
