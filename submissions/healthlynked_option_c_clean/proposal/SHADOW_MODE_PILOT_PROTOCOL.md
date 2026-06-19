# Shadow-Mode Pilot Protocol

## Purpose

The prototype proves the pipeline mechanics on a reproducible benchmark. The shadow-mode pilot proves the production truth on HealthLynked records before any write is allowed. This document is the day-one operating protocol for converting the Option C submission into a safe HealthLynked implementation.

## No-Write Pilot Law

During shadow mode, the system may read HealthLynked records, collect public evidence, produce recommendations, route cases to reviewers, and write audit artifacts. It may not mutate the production provider directory. Production writes begin only after HealthLynked approves the field-level launch decision for a specific field, source mix, confidence threshold, and rollback procedure.

## Pilot Cohorts

| Cohort | Size | Selection Logic | What It Proves |
|---|---:|---|---|
| Stale-risk sample | 1,000 records | Stratified by specialty, state, record age, source freshness, and practice type | Measures real update yield and evidence coverage |
| High-change-risk sample | 500 records | Records with old phone/address, weak website, missing practice match, or prior user complaint | Tests movement, inactive, and practice-location routing |
| Stable control sample | 500 records | Recently confirmed records across the same specialties and states | Estimates false-positive rate and over-triggering |
| Reviewer holdout | 10% of all reviewed cases | Randomly assigned after recommendation generation | Measures reviewer agreement and calibration drift |

If HealthLynked starts with a smaller operational sample, the same design still applies. Any field with too few reviewed examples remains review-only until the minimum evidence threshold is met.

## Daily Reviewer Disposition Loop

1. Ingest de-identified HealthLynked provider, practice, location, phone, specialty, website, NPI, and active-status fields.
2. Run only approved connectors from the source registry: NPPES, CMS/NPPES file snapshots, state boards where available, practice websites, health-system directories, and HealthLynked-provided internal signals.
3. Normalize names, addresses, phones, specialties, NPIs, practice names, websites, and affiliations with deterministic transforms before scoring.
4. Emit one recommendation event per proposed field change with evidence URLs, timestamps, source tier, confidence, reason code, policy version, and rollback key.
5. Route every case to a reviewer action in the dashboard: `accept`, `reject`, `edit`, `defer`, `recrawl`, or `suppress`.
6. Recompute precision, acceptance rate, source conflict rate, evidence coverage, cost, and reviewer time by field, source, state, specialty, and freshness band.
7. Update thresholds in shadow mode only. Threshold changes require a versioned policy note and a replay against the holdout set.
8. Publish a daily go/no-go report showing which fields are eligible for launch, which remain review-only, and which connectors are paused.

## Measurement Plan

| Metric | Required View | Why It Matters |
|---|---|---|
| Auto-update precision | Field, source tier, confidence band, specialty, state | Prevents incorrect writes |
| Reviewer acceptance rate | Field, reason code, source conflict class | Shows whether the system reduces manual work |
| Source URL and timestamp coverage | Field and connector | Confirms every recommendation is auditable |
| Evidence conflict rate | Field and source pair | Exposes source disagreement before writes |
| NPI validity and identity lock rate | Provider and practice-location pair | Prevents identity corruption |
| Movement and inactive-provider review yield | Field and reviewer disposition | Tests high-value directory cleanup without unsafe automation |
| Review time per case | Reason code and queue priority | Quantifies staffing and cost |
| Cost per 1,000 records | Evidence, AWS compute, LLM fallback, review labor | Keeps the operating model affordable |
| Rollback drill success | Auto-eligible field and audit event | Proves every write can be reversed |

## Go/No-Go Gates

| Gate | Launch Rule |
|---|---|
| Field-level auto-update precision | `>= 0.98` measured on accepted reviewer dispositions for that field and source mix |
| Audit coverage | `100%` of recommendations have source URL, source timestamp, evidence hash, policy version, and rollback key |
| Identity-critical changes | Provider identity, NPI, inactive status, practice affiliation, and high-risk address changes remain human-review-first |
| Source conflict handling | Conflicting authority-tier evidence cannot auto-update; it must route to review with conflict reason code |
| Minimum reviewed examples | A field cannot launch on fewer than 100 accepted/rejected reviewed examples unless HealthLynked explicitly narrows the scope |
| Holdout replay | Threshold changes must improve or preserve precision on the reviewer holdout set |
| Rollback drill | At least one non-production rollback drill must pass for each auto-eligible field family |
| Unexplained recommendation rate | `0%`; every recommendation must have a reviewer-readable reason |

## Error Budget And Stop Rules

- One critical identity error pauses all production-write planning until root cause analysis is complete.
- Any auto-eligible field below the agreed precision threshold remains review-only.
- A connector with stale terms, blocked access, schema drift, or abnormal conflict rate is quarantined until the source registry is updated.
- A policy version that improves recall but lowers precision below the gate is rejected for production launch.
- LLM extraction output is never write-authoritative without deterministic validation and source-backed audit.

## Field-Level Launch Decision

Each field receives one of four launch states:

| State | Meaning | Examples |
|---|---|---|
| `no_change_confirmed` | Evidence confirms the current record | Recent NPPES/practice-site agreement |
| `review_only` | Recommendation is useful but not safe to write automatically | Practice affiliation, inactive status, conflicting address |
| `auto_update_candidate` | Low-risk field meets precision, audit, and rollback gates | Phone or specialty under approved source mix |
| `blocked` | Source quality, sample size, or conflict rate is insufficient | State-board outage, weak website evidence |

The field-level decision is the unit of launch. HealthLynked does not need to approve the entire system at once; it can safely enable one proven low-risk field while keeping higher-risk fields in review.

## Calibration Outputs

The pilot produces these implementation artifacts:

- Calibrated confidence thresholds by field and source tier.
- Updated source authority table and connector admission decisions.
- Reviewer disposition export with reason-code distributions.
- Field-level launch matrix with eligible, review-only, and blocked states.
- Cost report per 1,000 records and per accepted update.
- Holdout replay report for the current policy version.
- Rollback drill record and audit-ledger sample.
- Production backlog for connectors, dashboard improvements, and edge cases.

## 90-Day Consulting Fit

| Period | Deliverable |
|---|---|
| Weeks 1-2 | Schema mapping, source registry, no-write AWS pilot environment, and first shadow run |
| Weeks 3-4 | Reviewer dashboard loop, disposition taxonomy, audit ledger, and baseline calibration report |
| Weeks 5-8 | Connector hardening, threshold calibration, holdout replay, cost monitoring, and review SLA dashboard |
| Weeks 9-12 | Limited production launch for approved low-risk fields, rollback drill, monitoring dashboard, and production handoff |

## Judge Takeaway

This protocol closes the gap between a strong prototype and a safe production launch. It gives HealthLynked a practical way to validate accuracy, source reliability, reviewer workload, cost, and rollback before production mutation, while still moving quickly enough for a lean engineering team.
