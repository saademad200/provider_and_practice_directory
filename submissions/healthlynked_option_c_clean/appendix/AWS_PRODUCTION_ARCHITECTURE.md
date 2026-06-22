# Cloud-Agnostic Production Architecture (AWS Reference Example)

This document maps the local provider-directory prototype to a cloud-agnostic production deployment. AWS services are named as a concrete reference implementation; the same roles can map to the organizer's preferred cloud services.

## Current Prototype Metrics

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Auto-apply count: 3
- Review count: 55

## Service Map

| Layer | Cloud capability | AWS reference example | Role |
|---|---|---|---|
| Scheduling | Managed scheduler | Amazon EventBridge Scheduler | Trigger recurring NPPES, CMS, state-board, website, and health-system refresh jobs. |
| Workflow orchestration | State-machine/workflow service | AWS Step Functions | Coordinate source fetch, normalization, matching, scoring, review routing, and audit export. |
| Batch/source ingestion | Managed ETL or batch workers | AWS Glue or AWS Batch | Process NPPES monthly files, weekly incrementals, and large CMS/website refresh batches. |
| Raw evidence lake | Object storage | Amazon S3 | Store immutable raw source snapshots, crawl output, parsed evidence, and audit bundles. |
| Metadata/catalog | Data catalog | AWS Glue Data Catalog | Catalog source snapshots, normalized evidence, and candidate-update tables. |
| Operational queues | Managed queue | Amazon SQS | Buffer provider refresh tasks, review tasks, retry work, and dead-letter failures. |
| Online lookup/cache | Key-value cache/store | Amazon DynamoDB | Cache provider evidence summaries, source freshness state, and NPI lookup results. |
| Relational workflow state | Relational database | Amazon RDS/PostgreSQL or Aurora PostgreSQL | Store candidate updates, review decisions, audit trail, and reviewer outcomes. |
| Optional LLM extraction | Governed foundation-model endpoint | Amazon Bedrock | Run constrained extraction only for messy web pages after deterministic parsers fail. |
| Human review UI | Hosted web app or container service | AWS Amplify or ECS/Fargate app | Serve the review dashboard and evidence drill-down workflow. |
| Monitoring | Logs, metrics, and alerting | Amazon CloudWatch | Track source coverage, freshness, cost, failures, review backlog, and auto-apply precision checks. |
| Secrets and access | Secrets manager and IAM | AWS Secrets Manager and IAM | Manage source credentials, least-privilege connector roles, and audit access boundaries. |

## Production Flow

1. EventBridge Scheduler triggers source-specific refresh plans.
2. Step Functions starts a provider batch and fans out source fetch tasks.
3. Glue or Batch ingests large public files such as NPPES monthly and weekly downloads.
4. Connector jobs write raw source snapshots and parsed evidence to S3.
5. Normalization jobs create canonical provider/practice/name/address/phone/specialty evidence tables.
6. Candidate scoring computes source agreement, confidence, freshness, and cost.
7. Safe auto-apply candidates pass field-specific gates, source-count checks, freshness checks, and practice-peer checks.
8. Ambiguous candidates go to SQS-backed human review with priority scores and reason codes.
9. Reviewer decisions update RDS/Aurora audit tables and become calibration data for the next tuning cycle.
10. CloudWatch dashboards and alerts track source freshness, connector failures, review backlog, cost, and quality.

## Deployment Phases

| Phase | Scope | Exit Criteria |
|---|---|---|
| 1. Shadow mode | Run against HealthLynked records, write recommendations only | Source coverage and reviewer precision are measurable |
| 2. Review assist | Prioritized review queue drives manual updates | Manual review time per accepted update drops materially |
| 3. Low-risk auto-apply | Enable auto-apply for fields with proven precision and fresh evidence | Auto-apply precision remains above policy threshold |
| 4. Source expansion | Add state-specific boards, CMS/PDC, health-system adapters | Missing-source alerts and source SLAs are monitored |
| 5. Continuous learning | Recalibrate thresholds and source weights from reviewer outcomes | Drift dashboards show stable precision/cost |

## Official AWS References

- AWS Step Functions: https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html
- Amazon EventBridge Scheduler: https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html
- AWS Glue: https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html
- Amazon Bedrock: https://docs.aws.amazon.com/bedrock/
