# Implementation Acceptance Criteria

## Purpose

If HealthLynked selects this proposal, the next three months should begin with measurable delivery criteria. This document turns the submission into a consulting-ready implementation contract: what must be built, how it will be accepted, and what is not allowed to go live until it is proven safe.

## First 30 Days: Shadow-Mode MVP On HealthLynked Data

| Workstream | Acceptance Criteria | Evidence |
|---|---|---|
| Schema mapping | Provider, practice, location, phone, specialty, website, NPI, and active-status fields mapped from HealthLynked into the pipeline schema | Data mapping table approved by HealthLynked |
| Source registry | NPPES, CMS/NPPES files, at least one state-board pattern, practice websites, and health-system directories configured with authority tiers | Source registry and connector health report |
| Shadow run | Pipeline runs on de-identified sample records without mutating production | Candidate updates, review queue, audit events |
| Review calibration | Operations reviewers accept/reject/edit recommendations in dashboard workflow | Reviewer disposition export |
| Safety gate | No auto-update enabled until measured precision and audit coverage meet thresholds | Precision report and audit coverage report |

## Days 31-60: Production Workflow Pilot

| Workstream | Acceptance Criteria | Evidence |
|---|---|---|
| Connector hardening | Retry, timeout, cache, freshness, and source-term controls implemented | Connector run logs and failure dashboard |
| Decision policy | Confidence formula and auto-update thresholds calibrated from reviewer dispositions | Calibration report |
| Review operations | Review queue includes priority, reason codes, field risk, evidence links, and SLA tracking | Dashboard and SLA metrics |
| Audit/rollback | Every recommendation has evidence hash, source URLs, timestamps, policy version, and rollback eligibility | Audit ledger sample |
| AWS deployment | EventBridge/Step Functions/Lambda-or-ECS/S3/RDS-or-DynamoDB path deployed in non-production | Architecture deployment notes |

## Days 61-90: Limited Production Launch

| Workstream | Acceptance Criteria | Evidence |
|---|---|---|
| Safe auto-update | Enabled only for approved low-risk fields after agreed precision threshold is met | Auto-update precision report |
| Human review | High-risk identity, affiliation, inactive, conflicting, and stale-source cases remain review-first | Review routing report |
| Monitoring | Source freshness, connector failures, review backlog, cost, and quality monitored | CloudWatch dashboard/export |
| Cost controls | Cost per 1,000 records and cost per correct update reported | Cost model refresh |
| Rollback drill | A sample auto-applied update is reversed from audit data in a non-production drill | Rollback drill record |

## Go/No-Go Thresholds

| Gate | Threshold |
|---|---:|
| Auto-update precision for approved low-risk fields | `>= 0.98` before production mutation |
| Audit coverage for recommended changes | `100%` |
| Source URL/timestamp coverage | `100%` for all recommended changes |
| Human-review routing for identity-critical changes | `100%` |
| Rollback eligibility for auto-applied changes | `100%` |
| Unexplained recommendation rate | `0%` |

## Explicit Non-Goals For Initial Launch

- Do not auto-merge provider identities.
- Do not auto-change NPI.
- Do not auto-suppress inactive providers without HealthLynked-approved policy.
- Do not use business listings as identity, specialty, license, or inactive-status authority.
- Do not allow LLM extraction to write directly without deterministic validation and audit.

## Consulting Success Definition

The implementation is successful when HealthLynked can run the pipeline repeatedly, inspect every recommendation, understand why each update was proposed, review only genuinely uncertain cases, safely auto-update low-risk fields, and roll back any applied change from the audit trail.
