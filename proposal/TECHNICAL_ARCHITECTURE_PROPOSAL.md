# Technical Architecture Proposal

This package includes a detailed implementation plan for a repeatable, cost-efficient HealthLynked provider/practice directory update pipeline.

Open these files together:

- `proposal/ARCHITECTURE_DIAGRAM.md`
- `proposal/CONFIDENCE_AND_DECISION_POLICY.md`
- `proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md`
- `proposal/IMPLEMENTATION_ROADMAP_90_DAYS.md`
- `prototype/RECOMMENDATION_API_CONTRACT.md`
- `appendix/COST_MODEL.md`
- `appendix/CLOUD_AGNOSTIC_PRODUCTION_ARCHITECTURE.md`
- `appendix/AUDIT_ROLLBACK_WORKFLOW.md`

## Pipeline Summary

```text
HealthLynked directory
  -> risk scanner
  -> trusted source connectors
  -> evidence normalization
  -> provider/practice/location matching
  -> validation rules
  -> confidence scoring
  -> no change, safe auto-update, or human review
  -> audit log, rollback, and feedback loop
```

## Data Sources

- NPPES/NPI Registry for identity and taxonomy anchors.
- CMS PECOS / Medicare enrollment public data surfaces for enrollment and organization-affiliation cross-checks where legally accessible.
- NUCC provider taxonomy for specialty normalization and synonym mapping.
- State licensing boards for active/inactive and license status.
- CMS/public datasets for cross-checks.
- Practice websites and health-system directories for location, phone, roster, and affiliation evidence.
- Fresh business-listing fallback for phone/address only, age-gated and low weighted.
- LLM extraction fallback only for approved messy pages after deterministic parsing fails.

## AI Agents

- Risk Prioritization Agent
- Source Discovery Agent
- Evidence Extraction Agent
- Normalization Agent
- Identity Resolution Agent
- Confidence Scoring Agent
- Human Review Routing Agent
- Audit and Rollback Agent

Each agent has scoped permissions, source authority rules, and output contracts in the agent/workflow artifacts.

## Validation Logic

- NPI format and identity anchoring.
- Name, phone, address, specialty, website, affiliation, and status normalization.
- Production address normalization can use libpostal for parsing plus USPS/Smarty-style deliverability validation when HealthLynked approves terms and cost.
- Production phone normalization should use libphonenumber-style E.164 parsing, extension handling, and invalid-area-code rejection.
- Specialty normalization maps free text through NUCC/NPPES taxonomy codes before comparing display names.
- Duplicate detection.
- Provider movement detection.
- Practice-location matching.
- Inactive/retired provider detection.
- Source conflict adjudication.
- Field-risk policy for safe auto-update.

## Confidence And Decision Law

The production decision law is documented in `proposal/CONFIDENCE_AND_DECISION_POLICY.md`. In short:

- low-risk fields such as phone and website can be auto-updated only with high confidence, fresh evidence, and independent source agreement;
- medium-risk fields such as address and specialty require stricter source authority and conflict checks;
- high-risk or identity-sensitive changes such as provider name, NPI, affiliation moves, inactive status, merges, and suppressions are review-first;
- every change must be audit-ready before any mutation is allowed.

## Cost Controls

- Cache public data snapshots.
- Refresh risky/stale records first.
- Use deterministic parsing before LLM extraction.
- Gate LLM fallback by source, field, and failure mode.
- Track source cost and cost per correct update.
- Reduce manual review with explainable confidence thresholds.

## Update Workflow

| Decision | Behavior |
|---|---|
| No Change | Current record is confirmed or evidence is insufficient |
| Auto Update | High-confidence, low-risk, non-conflicting field update |
| Human Review | Low-confidence, conflicting, high-risk, or identity-sensitive update |

## Cloud-Agnostic Production Plan (AWS Reference Example)

The production plan is cloud-agnostic: EventBridge for schedules, Step Functions for orchestration, SQS for queueing, Lambda/ECS/Batch for workers, S3 for source snapshots, RDS/DynamoDB for state, CloudWatch for monitoring, and Bedrock only for bounded extraction fallback. See `appendix/CLOUD_AGNOSTIC_PRODUCTION_ARCHITECTURE.md`.

## IaC And Delivery Plan

The implementation should be promoted through dev, staging, and production environments with infrastructure as code. The recommended infrastructure-as-code path is Terraform, or AWS CDK when using AWS as the reference implementation, for evidence buckets, normalized evidence tables, workflows, workers, review queues, IAM roles, secret entries, and monitoring alarms. CI should run unit tests for normalization, NPI validation, confidence scoring, audit logging, and package verification before any workflow policy is promoted.
