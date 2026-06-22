# HealthLynked Provider & Practice Directory Update Pipeline

## Option C Hybrid Submission

This submission proposes and demonstrates a repeatable provider/practice directory quality pipeline. It is not a one-time cleanup. It is a governed operating loop that continuously finds stale records, searches trusted sources, normalizes evidence, scores confidence, separates safe updates from human review, and records an audit trail before any directory mutation.

The package is intentionally submitted as two judge-facing artifacts:

- `HealthLynked_Provider_Directory_Option_C_Writeup.md`
- `HealthLynked_Provider_Directory_Update_Pipeline.ipynb`

The GitHub repository can be used as optional reproducibility evidence for the runnable prototype, sample data, dashboard, audit events, and verification checks.

## Executive Summary

HealthLynked's provider directory should be maintained by a quality control plane, not by manual search or an opaque scraper. The proposed system combines deterministic public-source checks, bounded AI agents, conservative auto-update rules, and reviewer-visible evidence.

The MVP demonstrates the core loop on sample provider/practice data:

| Metric | MVP Result |
|---|---:|
| Field-level F1 | `0.948276` |
| Precision | `0.948276` |
| Recall | `0.948276` |
| Safe auto-apply precision | `1.0` |
| Candidate updates found | `58` |
| Safe auto-apply updates | `3` |
| Human-review items | `55` |
| Prototype evidence-only cost per correct update | `$0.005836` |

The key design choice is separation of discovery from mutation. The system may discover many candidate changes, but it auto-updates only low-risk fields with fresh, corroborated evidence. Identity-sensitive, conflicting, stale, or low-confidence changes go to human review.

## Desired Pipeline Architecture

```text
HealthLynked Provider / Practice Database
  ↓
Find Outdated or Risky Records
  ↓
Search Trusted Sources
NPI, CMS, state boards, practice websites
  ↓
Collect Updated Provider / Practice Data
  ↓
Clean and Normalize Data
Names, addresses, phones, specialties
  ↓
Match Provider / Practice Records
  ↓
Assign Confidence Score
  ↓
Decision
No Change | Auto Update | Human Review
Record confirmed as accurate | High-confidence update | Low-confidence or conflicting data
  ↓
Save Audit Log + Update Provider Directory
```

## How The Pipeline Works

### 1. Find Outdated Or Risky Records

The system prioritizes records likely to be stale or risky:

- old `last_verified_at` timestamps;
- missing or malformed NPI, phone, website, address, or specialty;
- provider/practice records with conflicting internal fields;
- providers with multiple practice locations;
- specialties or affiliations that commonly drift;
- providers previously flagged by reviewers or patient/user feedback;
- practice locations with signs of closure, rebrand, acquisition, or relocation.

This avoids spending source/API/reviewer budget on already-fresh low-risk records.

### 2. Search Trusted Sources

The source strategy is authority-tiered:

| Tier | Source Type | Use |
|---|---|---|
| A | NPPES / NPI Registry, CMS public enrollment surfaces, state licensing boards | identity, NPI, specialty taxonomy, license/activity status |
| B | practice websites, health-system directories | phone, address, roster, affiliation, website, accepting status |
| C | reputable business listings | fallback for phone/address only, low weight |
| D | untrusted or unsupported pages | never used for auto-update |

Source access is legally conservative. The system uses public or contractually approved sources, respects terms of use, records source URLs and retrieval timestamps, and keeps raw evidence snapshots for audit.

### 3. Collect And Normalize Evidence

Every source observation is normalized before comparison:

- provider names: case, punctuation, suffixes, initials, credentials;
- practice names: aliases, DBA names, health-system branding;
- phones: E.164-style normalization, extensions, invalid patterns;
- addresses: street suffixes, suites, city/state/ZIP, deliverability-ready canonical form;
- specialties: NUCC/NPPES-style taxonomy mapping and synonym handling;
- websites: canonical domain, protocol normalization, tracking-parameter removal;
- active/inactive status: source-specific status mapped into a common lifecycle vocabulary.

Raw and normalized values are retained side by side so reviewers can see exactly what changed.

### 4. Match Provider / Practice Records

Matching is not a naive string join. The pipeline resolves:

- provider identity anchored by NPI where available;
- provider name similarity with specialty and location checks;
- practice-location matching across phone, address, website, and roster;
- duplicate provider records;
- provider movement between practices or locations;
- inactive or retired providers.

High-risk identity actions, including merges, NPI changes, suppressions, and provider movement, are review-first.

### 5. Assign Confidence Score

The confidence score is decomposed so it can be explained to a reviewer:

```text
confidence =
  source_authority_weight
  + source_agreement_weight
  + freshness_weight
  + field_stability_weight
  + identity_match_weight
  - conflict_penalty
  - stale_evidence_penalty
  - high_risk_field_penalty
```

The MVP exposes confidence, review priority, source set, evidence URLs, reason codes, freshness status, and recommended action for each candidate update.

### 6. Decision Policy

| Decision | Meaning | Example |
|---|---|---|
| No Change | Existing record is confirmed or evidence is insufficient | NPPES and practice website agree with current phone |
| Auto Update | Low-risk field, high confidence, fresh corroborated evidence, audit-ready | phone or specialty with independent trusted-source agreement |
| Human Review | Low confidence, stale evidence, conflict, identity risk, or practice movement | address move, inactive status, affiliation change, NPI/name conflict |

Safe auto-update rules are deliberately narrow. In the MVP, auto-apply precision is `1.0`; uncertain cases are routed to review instead of silently changed.

### 7. Audit Log And Update

Every recommendation carries:

- provider ID and NPI;
- changed field;
- current value and proposed value;
- confidence score;
- source observations and source URLs;
- reason code;
- decision;
- evidence hash;
- rollback eligibility;
- reviewer/auditor trace.

This makes each update explainable and reversible.

## AI Agent Design

The proposed agent workflow is bounded and auditable:

1. Risk Prioritization Agent selects records to refresh.
2. Source Discovery Agent chooses allowed sources by authority, cost, and field.
3. Evidence Extraction Agent retrieves or parses evidence.
4. Normalization Agent canonicalizes names, addresses, phones, specialties, websites, and statuses.
5. Identity Resolution Agent matches provider, NPI, practice, and location.
6. Confidence Scoring Agent creates score, action, and explanation.
7. Human Review Routing Agent queues uncertain or risky updates.
8. Audit And Rollback Agent writes evidence hashes, events, and rollback rows.

LLM extraction is not the default path. It is a gated fallback for approved messy pages after deterministic parsing fails.

## Cost Controls

The design keeps cost low by:

- refreshing risky/stale records before fresh records;
- caching public source snapshots;
- preferring bulk public files over per-record API calls;
- using deterministic extraction before LLM fallback;
- limiting LLM calls to approved pages and fields;
- deduplicating provider/practice/location evidence before scoring;
- routing only uncertain or high-risk cases to humans.

### Example Cost Per 1,000 Records

| Scenario | Evidence | Cloud compute/storage/monitoring | LLM fallback | Manual review | Total |
|---|---:|---:|---:|---:|---:|
| Conservative MVP-like run | low | low | near-zero | moderate | low operating cost |
| Production steady state | cached public data + targeted refresh | modest | bounded | reduced by confidence gates | scalable |
| High-risk refresh campaign | higher source retrieval | modest | bounded | higher review queue | temporary spike |

Cloud services are intentionally described generically. If a concrete reference is useful, AWS can be used as an example implementation: object storage similar to S3, workflow orchestration similar to Step Functions, queueing similar to SQS, serverless/container workers similar to Lambda/ECS/Batch, monitoring similar to CloudWatch, and governed foundation-model fallback similar to Bedrock.

## Human Review Dashboard

The MVP includes a sample dashboard concept showing:

- headline quality metrics;
- review queue rows with old/new value, confidence, reason, sources, and evidence URLs;
- accept, reject, and recrawl actions;
- launch gates for auto-update eligibility;
- inactive-provider candidates;
- rollback and audit evidence.

The dashboard is designed to reduce reviewer work, not create a second manual cleanup project.

## MVP Scope Covered

The prototype covers the suggested MVP fields:

- provider name;
- NPI;
- specialty;
- practice name;
- address;
- phone number;
- website;
- active/inactive status.

It also demonstrates bonus areas:

- confidence scoring formula;
- duplicate detection logic;
- address normalization strategy;
- NPI validation;
- practice-location matching;
- provider movement detection;
- inactive/retired provider detection;
- audit log;
- rollback plan;
- safe auto-update rules;
- human review queue;
- implementation roadmap;
- cloud-agnostic scaling plan with AWS as an example only.

## Production Roadmap

### First 30 Days

- Map HealthLynked production schema to the recommendation contract.
- Run no-write shadow mode on a representative sample.
- Validate NPI, phone, address, specialty, practice, and website normalization.
- Measure source coverage and reviewer agreement.
- Calibrate confidence thresholds.

### Days 31-60

- Add official/bulk source connectors.
- Deploy review workflow and reviewer disposition capture.
- Add connector health checks and source freshness monitoring.
- Produce daily audit bundles and rollback plans.
- Tune thresholds using reviewer decisions.

### Days 61-90

- Enable low-risk auto-update only for fields that pass launch gates.
- Keep identity-level changes review-first.
- Expand state-board and health-system coverage.
- Add production monitoring for cost, freshness, precision, review backlog, and drift.
- Prepare staged rollout with field-level kill switches.

## Implementation Value

This approach is practical rather than speculative. It gives HealthLynked:

- a clear architecture;
- a working prototype;
- a conservative confidence policy;
- trusted-source governance;
- human review only where needed;
- audit and rollback from day one;
- a scalable path a lean engineering team can implement during the post-award consulting period.

The core implementation principle is simple: provider directory quality is not solved by scraping more pages. It is solved by a repeatable evidence-and-decision system that knows when to trust, when to abstain, when to ask a human, and how to prove every change afterward.
