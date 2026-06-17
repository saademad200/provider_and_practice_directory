# AWS Production Architecture

This document maps the local provider-directory prototype to an AWS production deployment. It uses AWS only where naming a cloud is helpful; the code remains local and portable.

## Current Prototype Metrics

- F1: 0.93913
- Precision: 0.947368
- Recall: 0.931034
- Auto-apply precision: 1.0
- Auto-apply count: 20
- Review count: 37

## Service Map

| Layer | AWS Service | Role |
|---|---|---|
| Scheduling | Amazon EventBridge Scheduler | Trigger recurring NPPES, CMS, state-board, website, and health-system refresh jobs. |
| Workflow orchestration | AWS Step Functions | Coordinate source fetch, normalization, matching, scoring, review routing, and audit export. |
| Batch/source ingestion | AWS Glue or AWS Batch | Process NPPES monthly files, weekly incrementals, and large CMS/website refresh batches. |
| Raw evidence lake | Amazon S3 | Store immutable raw source snapshots, crawl output, parsed evidence, and audit bundles. |
| Metadata/catalog | AWS Glue Data Catalog | Catalog source snapshots, normalized evidence, and candidate-update tables. |
| Operational queues | Amazon SQS | Buffer provider refresh tasks, review tasks, retry work, and dead-letter failures. |
| Online lookup/cache | Amazon DynamoDB | Cache provider evidence summaries, source freshness state, and NPI lookup results. |
| Relational workflow state | Amazon RDS/PostgreSQL or Aurora PostgreSQL | Store candidate updates, review decisions, audit trail, and reviewer outcomes. |
| Optional LLM extraction | Amazon Bedrock | Run constrained extraction only for messy web pages after deterministic parsers fail. |
| Human review UI | AWS Amplify or ECS/Fargate app | Serve the review dashboard and evidence drill-down workflow. |
| Monitoring | Amazon CloudWatch | Track source coverage, freshness, cost, failures, review backlog, and auto-apply precision checks. |
| Secrets and access | AWS Secrets Manager and IAM | Manage source credentials, least-privilege connector roles, and audit access boundaries. |

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
