# Technical Architecture Proposal

This package includes a detailed implementation plan for a repeatable, cost-efficient HealthLynked provider/practice directory update pipeline.

Open these files together:

- `ARCHITECTURE_DIAGRAM.md`
- `COMBINED_ABC_PIPELINE_COVERAGE.md`
- `ARCHITECTURE.md`
- `AWS_PRODUCTION_ARCHITECTURE.md`
- `SOURCE_CONNECTOR_REGISTRY.md`
- `FIELD_RISK_POLICY.md`
- `COST_MODEL.md`
- `AUDIT_ROLLBACK_WORKFLOW.md`
- `REVIEW_DISPOSITION_AND_SLA.md`

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
- Duplicate detection.
- Provider movement detection.
- Practice-location matching.
- Inactive/retired provider detection.
- Source conflict adjudication.
- Field-risk policy for safe auto-update.

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

## AWS Production Plan

The production plan uses EventBridge, Step Functions, Lambda/ECS, S3, RDS/DynamoDB, CloudWatch, and gated Bedrock fallback. See `AWS_PRODUCTION_ARCHITECTURE.md`.
