# Lean Team Operating Model

## Purpose

HealthLynked asked for a practical solution a lean engineering team can implement. This operating model shows who does what during the first production rollout without assuming a large platform organization.

## Minimum Team

| Role | Ownership | Weekly Commitment During Pilot |
|---|---|---:|
| Data/ML engineer | Pipeline logic, normalization, confidence scoring, evaluation, threshold calibration | 3-5 days |
| Backend engineer | AWS orchestration, source connector jobs, data contracts, audit writes, API handoff | 3-5 days |
| Ops/product owner | Review policy, field-risk approvals, reviewer workflow, acceptance criteria | 1-2 days |
| Directory reviewer lead | Ground-truth decisions, disposition labels, escalation patterns | 1-2 days |
| Security/compliance reviewer | Source terms, IAM/secrets, audit/privacy checks | 0.5-1 day |

## Weekly Rhythm

| Day | Activity | Output |
|---|---|---|
| Monday | Review source health, backlog, cost, and previous-week reviewer outcomes | Updated priorities |
| Tuesday-Wednesday | Connector and scoring improvements | Shadow-run candidate set |
| Thursday | Reviewer calibration and threshold review | Field/source accept-rate report |
| Friday | Release decision for next shadow or limited-production run | Go/no-go record |

## Decision Rights

| Decision | Owner | Required Evidence |
|---|---|---|
| Add new source connector | Backend engineer + security/compliance reviewer | Terms review, source authority tier, health checks |
| Change confidence threshold | Data/ML engineer + ops/product owner | Reviewer accept/reject metrics by field/source |
| Enable auto-update for a field | Ops/product owner | Precision threshold met, audit/rollback proven |
| Suppress inactive provider | Ops/product owner + reviewer lead | Approved inactive-provider policy and authority evidence |
| Roll back applied update | Reviewer lead or directory ops lead | Audit event and rollback record |

## Production Cadence

- Daily: risky-record refresh, connector health, review queue generation.
- Weekly: NPPES incremental ingest, reviewer calibration, source quality review.
- Monthly: NPPES/CMS snapshot ingest, cost review, threshold review, rollback drill.
- Quarterly: source policy review, security/IAM review, sampling strategy refresh.

## Escalation Rules

Escalate to human review when:

- source conflict involves an authority-tier mismatch;
- provider movement affects multiple locations or practices;
- inactive/suppression is suggested;
- reviewer rejection rate for a source exceeds threshold;
- connector parsing changes cause unusual candidate volume;
- cost or review backlog exceeds operating target.

## Why This Matters

The proposal is designed to be run by a small team because the pipeline does not depend on a large manual cleanup effort. Automation handles repeatable evidence collection and low-risk updates; humans handle policy, ambiguous identity, source conflict, and calibration.
