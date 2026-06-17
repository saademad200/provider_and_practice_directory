# 90-Day Implementation Roadmap

## Goal

Move from the submitted MVP to a production pilot that HealthLynked can run on AWS with real provider/practice records, source connectors, review operations, and audit controls.

## Days 0-15: Foundation

| Workstream | Deliverable |
|---|---|
| Data contract | HealthLynked provider/practice export schema, field mapping, and data-quality baseline |
| Source registry | Approved NPPES, state board, CMS/public, practice website, and health-system source list |
| MVP adaptation | Run current pipeline against a de-identified sample export |
| Security | AWS account boundary, IAM roles, Secrets Manager, S3 evidence bucket, no-secrets checks |
| Review policy | Auto-apply blocked fields, review disposition contract, reviewer SLA |

## Days 16-35: Connector And Normalization Hardening

| Workstream | Deliverable |
|---|---|
| NPPES | Batch/API connector with NPI validation and taxonomy mapping |
| State licensing | State-board connector pattern for priority states |
| Practice websites | Deterministic crawler/parser with source health checks |
| Normalization | Address, phone, specialty, practice name, provider name, website canonicalization |
| Identity | Duplicate, movement, practice-location, inactive-provider review queues |

## Days 36-60: Review And Audit Pilot

| Workstream | Deliverable |
|---|---|
| Dashboard | Human review queue with evidence, confidence, reason codes, and disposition actions |
| Audit | Append-only audit events, evidence hashes, before/after values, rollback plan |
| Monitoring | CloudWatch alarms for source freshness, review backlog, cost drift, and conflict spikes |
| Calibration | Threshold tuning against reviewer outcomes |
| Governance | Source conflict policy and field-risk policy approval |

## Days 61-90: AWS Production Pilot

| Workstream | Deliverable |
|---|---|
| Orchestration | EventBridge schedule plus Step Functions workflow |
| Compute | Lambda/ECS connector workers and scoring tasks |
| Storage | S3 evidence snapshots, RDS/DynamoDB workflow/evidence tables |
| LLM fallback | Amazon Bedrock extraction only behind source and field gates |
| Launch | Shadow-mode pilot, reviewer feedback loop, auto-apply limited to low-risk fields |

## Success Metrics

- Auto-apply precision: `>= 0.98`
- Review queue reduction: `>= 60%` vs review-all workflow
- Evidence traceability: `100%` of proposed updates have source URL and confidence reason
- Audit coverage: `100%` of applied updates have event ID and rollback plan
- Cost visibility: source, LLM, compute, and review cost tracked per 1,000 records

## Pilot Exit Criteria

The system is ready to expand when:

- source freshness alerts are stable;
- reviewers accept the majority of high-priority review candidates;
- false-positive auto-updates remain below agreed threshold;
- rollback drill succeeds;
- HealthLynked approves the field-risk policy for broader scheduled operation.
