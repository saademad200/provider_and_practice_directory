# Synthetic Benchmark Datasheet

## Status

This benchmark is a local proxy for the Kaggle Provider & Practice Directory Update Pipeline hackathon. It is not official Kaggle train/test data; the downloaded competition archive contained no labeled dataset. The purpose is to make pipeline changes measurable and reproducible while building an auditable submission artifact.

## Version

- Benchmark version: `2026-06-16-v2`
- Generation seed: `42`
- Providers: 72
- Practices: 24
- Evidence rows: 1224
- Gold update rows: 58

## Intended Use

- Validate candidate-update generation for provider directory maintenance.
- Compare one-change experiments with grouped CV by `provider_id`.
- Stress source agreement, normalization, stale records, missing evidence, and noisy sources.
- Demonstrate a review/auto-apply workflow with citations and audit fields.

## Not Intended For

- Claiming public leaderboard performance.
- Training a production model without real payer, provider, NPPES, licensing, and website data.
- Measuring demographic, geographic, specialty, or accessibility fairness.
- Auto-updating live healthcare directories without human governance and source contracts.

## Data Construction

The generator creates canonical provider records, injects stale values into selected fields, then emits source evidence from NPPES-like records, state licensing, practice websites, health-system pages, and business listings. Evidence includes noise, missing values, stale current values, retrieved-age metadata, and URLs. Gold labels are the injected corrections and are only used by metric code.

## Fields

Candidate updates cover:

- `phone`
- `address`
- `specialty`
- `license_status`
- `accepting_new_patients`

Gold changes by field:

| Field | Gold Updates |
|---|---:|
| phone | 18 |
| address | 14 |
| specialty | 8 |
| license_status | 6 |
| accepting_new_patients | 12 |

Evidence rows by source:

| Source | Rows |
|---|---:|
| business_listing | 288 |
| health_system | 288 |
| nppes | 288 |
| practice_website | 288 |
| state_license | 72 |

## Current Best Proxy Metrics

Grouped validation uses `GroupKFold(provider_id)` with five folds. Candidate generation does not read gold labels.

- Experiment: current safe auto-apply configuration in `scripts/run_best_pipeline.py`
- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Auto-apply count: 3
- Review count: 55
- Cost per correct update: $0.005836

Per-field metrics:

| Field | F1 | Precision | Recall | Auto Count | Auto Precision |
|---|---:|---:|---:|---:|---:|
| accepting_new_patients | 1.0 | 1.0 | 1.0 | 0 | 0.0 |
| address | 0.888889 | 0.923077 | 0.857143 | 0 | 0.0 |
| license_status | 0.909091 | 1.0 | 0.833333 | 0 | 0.0 |
| phone | 1.0 | 1.0 | 1.0 | 0 | 0.0 |
| specialty | 0.888889 | 0.8 | 1.0 | 3 | 1.0 |

## Leakage Controls

- Gold updates are generated after current values are made stale and are not read by `build_candidate_updates`.
- Evaluation folds are grouped by provider ID.
- Source evidence is treated as timestamped facts with source names, values, ages, and URLs.
- Business listings are not trusted globally; the current best uses them only as a fresh, field-gated phone/address fallback at low source weight.
- Final demos should be kept separate from future tuning examples.

## Known Limitations

- Synthetic evidence is cleaner and smaller than real public/provider web data.
- Provider identity is simplified with stable `provider_id`, `practice_id`, and NPI-like IDs.
- No real geographic, payer-network, language-access, taxonomy, or appointment-availability variation is modeled.
- Practice peer checks can differ between grouped CV and full-corpus CLI runs because more peers are visible in the full corpus.
- Costs are proxy estimates, not vendor invoices.

## Governance Notes

The pipeline is designed for conservative healthcare-directory maintenance: high-confidence updates can be auto-applied only with strong evidence, while ambiguous or peer-inconsistent updates route to review with source URLs and reason codes. Real deployment should add source freshness SLAs, appeal/audit workflow, monitoring by field and geography, and periodic human quality review.
