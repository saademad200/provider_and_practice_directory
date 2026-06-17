# Technical Architecture Proposal

## Executive Claim

This proposal describes a repeatable, cost-efficient AI pipeline for HealthLynked's provider and practice directory. It combines deterministic public-source validation, field normalization, identity resolution, confidence scoring, safe automation, human review, and auditable update history.

The design is production-oriented but lean: deterministic connectors and rules do most of the work, while LLM/agent steps are gated to extraction and conflict explanation cases where they add value.

## Target Outcomes

- Identify records likely to be outdated or risky.
- Search public and legally accessible sources.
- Normalize provider names, practice names, addresses, phones, specialties, websites, and active/inactive status.
- Match provider and practice records using NPI, source agreement, addresses, phones, specialty, and affiliation history.
- Assign field-level confidence scores.
- Auto-apply only high-confidence, low-risk updates.
- Route uncertain, conflicting, or identity-sensitive changes to human review.
- Preserve an audit trail of sources, evidence, decisions, and rollback metadata.
- Keep cost low by avoiding unnecessary paid APIs, unnecessary LLM calls, and unnecessary manual review.

## Data Sources

| Source | Role | Trust Tier | Cost Control |
|---|---|---:|---|
| NPPES/NPI Registry | Identity anchor, provider taxonomy, public profile fields | 1 | Cached API pulls and batch refresh |
| State licensing boards | Active/inactive signal and license status | 1 | Scheduled refresh by state and specialty |
| CMS/public datasets | Cross-checks and provider/practice context | 1-2 | Batch snapshots in S3 |
| Practice websites | Phone, address, practice name, provider roster | 2 | Crawl only risky/stale records |
| Health system directories | Affiliation and location evidence | 2 | Connector health checks and incremental refresh |
| Business listings | Phone/address fallback only when fresh | 3 | Field-gated, age-gated, low weight |
| LLM extraction | Messy page extraction and explanation | gated | Only after deterministic parsing fails |

## Pipeline

1. **Risk scanner**
   Scores records by stale verification date, source drift, missing fields, provider movement signals, conflicting evidence, and directory-critical fields.

2. **Source connector layer**
   Fetches evidence from NPPES, state boards, CMS/public datasets, practice websites, health-system pages, and guarded fallback sources.

3. **Evidence normalization**
   Converts raw evidence into canonical field/value rows with source, URL, timestamp, extraction method, and field type.

4. **Entity resolution**
   Matches providers and practices using NPI anchors first, then normalized names, addresses, phones, specialties, affiliations, and historical movement patterns.

5. **Validation logic**
   Applies NPI validation, phone/address normalization, specialty mapping, inactive-provider detection, duplicate detection, practice-location matching, and source conflict rules.

6. **Confidence scoring**
   Combines source authority, source agreement, field risk, evidence freshness, extraction confidence, identity stability, and conflict penalties.

7. **Decision routing**
   Sends each candidate to one of three outcomes:

   | Outcome | Rule |
   |---|---|
   | No change | External evidence agrees with current record or evidence is insufficient |
   | Auto update | High confidence, low field risk, no material conflict, stable identity |
   | Human review | Conflict, identity sensitivity, low confidence, high-risk field, or movement ambiguity |

8. **Audit and feedback**
   Stores immutable evidence snapshots, decision reasons, reviewer dispositions, update events, rollback plan, and source-policy feedback.

## AI Agents

| Agent | Responsibility | Guardrail |
|---|---|---|
| Risk Prioritization Agent | Selects records worth refreshing | Cannot modify records |
| Source Discovery Agent | Chooses approved connectors and source order | Uses source registry only |
| Evidence Extraction Agent | Parses pages and structures evidence | LLM fallback only when gated |
| Normalization Agent | Canonicalizes names, addresses, phones, specialties | Deterministic validators first |
| Identity Resolution Agent | Links provider/practice/location records | Review-first for identity changes |
| Confidence Agent | Computes field-level confidence and reasons | Versioned scoring formula |
| Review Routing Agent | Builds prioritized review queue | No auto-approval for blocked classes |
| Audit Agent | Writes evidence, decision, and rollback events | Append-only audit model |

## Confidence Formula

```text
confidence =
  source_authority_score
  + source_agreement_bonus
  + freshness_bonus
  + identity_anchor_bonus
  + extraction_quality_bonus
  - field_risk_penalty
  - conflict_penalty
  - stale_source_penalty
```

The prototype implements this as field-level scoring with source weights, recency gates, source-count thresholds, conflict penalties, and safe auto-apply thresholds.

## Cost Controls

- Use cached public data snapshots before live lookups.
- Refresh risky/stale records first instead of crawling every record.
- Prefer deterministic parsing over LLM extraction.
- Use LLM extraction only for approved messy official/practice pages.
- Downweight and gate low-authority business listings.
- Auto-apply only safe low-risk changes; reserve human review for high-value uncertainty.
- Track cost per source, per candidate, and per correct update.

## AWS Production Deployment

| Layer | AWS Services |
|---|---|
| Scheduling | EventBridge |
| Orchestration | Step Functions |
| Connector execution | Lambda for small connectors, ECS/Fargate for crawlers |
| Evidence storage | S3 raw snapshots, RDS/DynamoDB normalized evidence |
| Scoring and routing | ECS/Lambda batch jobs |
| LLM fallback | Amazon Bedrock behind policy gates |
| Review queue | RDS/DynamoDB plus lightweight web dashboard |
| Monitoring | CloudWatch, structured logs, source health alerts |
| Audit | S3 immutable evidence, append-only audit table |

## Implementation Roadmap

| Phase | Deliverable |
|---|---|
| 0-2 weeks | Load HealthLynked export, run sample MVP, configure source registry |
| 3-5 weeks | NPPES/state/practice connector hardening, confidence calibration |
| 6-8 weeks | Human review dashboard, audit/rollback workflow, reviewer feedback |
| 9-12 weeks | AWS deployment, monitoring, source health checks, production rollout |

## Primary Artifacts

- `ARCHITECTURE_DIAGRAM.md`
- `ARCHITECTURE_DIAGRAM.mmd`
- `WORKING_PROTOTYPE.md`
- `COMBINED_ABC_PIPELINE_COVERAGE.md`
- `AWS_PRODUCTION_ARCHITECTURE.md`
- `SOURCE_CONNECTOR_REGISTRY.md`
- `FIELD_RISK_POLICY.md`
- `COST_MODEL.md`
- `AUDIT_ROLLBACK_WORKFLOW.md`
- `REVIEW_DISPOSITION_AND_SLA.md`
