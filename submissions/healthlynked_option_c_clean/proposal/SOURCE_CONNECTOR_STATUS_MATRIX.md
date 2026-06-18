# Source Connector Status Matrix

## Purpose

This matrix shows how the production system keeps source usage reliable, legal, cost-aware, and explainable. It gives judges a concrete operating plan for connector cadence, fallback behavior, and field-level authority.

| Source | Primary Fields | Authority Tier | Refresh Cadence | Failure Fallback | Auto-Update Eligibility |
|---|---|---:|---|---|---|
| NPPES API | NPI identity, taxonomy, mailing/practice metadata | A | Daily for risky records; on demand for review | NPPES monthly/weekly files | Identity anchor only; not sufficient alone for licensure/current phone |
| NPPES monthly file | NPI identity, taxonomy, deactivation, practice location, endpoints | A | Monthly full snapshot | Weekly incremental file | Batch anchor and deactivation evidence; status review-first |
| NPPES weekly incremental | Recently changed NPI records | A | Weekly | Monthly file plus API lookup | Same as NPPES monthly |
| CMS public files | Cross-checks and supplemental provider data | A/B | Monthly or dataset-specific | Cached prior snapshot with stale flag | Only when field authority is approved |
| State boards / FSMB-style feeds | License status, sanctions, inactive/retired signals | A | Weekly to monthly, state-dependent | Manual review and last-known status with stale flag | Review-first unless HealthLynked approves a narrow suppression workflow |
| Practice websites | Phone, address, website, roster, accepting-new-patients, affiliation | B | 30-60 days for risky/stale records | Health-system directory or recrawl request | Low-risk phone/website; address only with strong agreement |
| Health-system directories | Affiliation, specialty, location, roster | B | 30-60 days | Practice website or manual review | Review-first for affiliation and movement |
| Business listings | Phone/address recall only | C | 30 days when used | Ignore if stale or conflicting | Never for identity/status/specialty; low-weight support only |
| LLM extraction over approved pages | Structured extraction from messy permitted pages | D | On demand after parser failure | Human review | Never standalone; output must be grounded and validated |

## Connector Health Signals

| Signal | Why It Matters | Action |
|---|---|---|
| HTTP failure rate | Detects broken source access or blocking | Backoff, retry, alert, route affected records to stale-source review |
| Parser empty rate | Detects layout drift | Run deterministic parser tests, then gated LLM fallback for approved pages |
| Stale evidence rate | Prevents old pages from changing records | Penalize confidence and route to review |
| Source conflict rate | Detects authority disagreements | Trigger conflict adjudication and source-specific quality review |
| Cost per accepted update | Keeps paid extraction/manual review controlled | Disable low-value source paths or change refresh cadence |
| Reviewer rejection rate by source | Learns which sources are unreliable in practice | Lower source weight or require stronger corroboration |

## Field-Level Source Law

| Field | Preferred Sources | Weak/Fallback Sources | Auto-Update Policy |
|---|---|---|---|
| NPI | NPPES API/file | none | Never auto-change |
| Provider name | NPPES plus practice/health-system corroboration | none | Formatting-only normalization; otherwise review |
| Specialty | NPPES taxonomy plus health-system/practice corroboration | business listings not allowed | Auto only for configured low-risk specialty corrections with strong independent agreement; otherwise review |
| Practice name | Practice website, health-system directory, HealthLynked history | business listings low-weight | Review if affiliation/rebrand ambiguity exists |
| Address | Practice website, health-system directory, NPPES practice location | fresh business listing as support only | Auto only with strong agreement and no conflict |
| Phone | Practice website, health-system directory, NPPES/business listing support | fresh business listing | Auto allowed when low-risk and independently supported |
| Website | Practice website, health-system directory | business listing support only | Auto allowed with strong confidence |
| Active/inactive status | State board/FSMB-style feed, NPPES deactivation, HealthLynked policy | business listings not allowed | Review-first |

## AWS Implementation Notes

- Store raw source responses in S3 with source, timestamp, connector version, and hash.
- Store normalized evidence in RDS or DynamoDB keyed by provider, NPI, practice, location, field, and source.
- Use EventBridge for scheduled refresh and Step Functions for connector orchestration.
- Use Lambda/ECS for lightweight connectors and AWS Batch for large NPPES/CMS file ingestion.
- Use CloudWatch metrics for connector health, staleness, conflict rate, cost, and review backlog.
