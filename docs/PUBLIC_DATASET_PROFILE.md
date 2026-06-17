# Public Dataset Profile

## Dataset

- Source: `chaitanyajamble/provider-directory`, attached to the currently visible public Kaggle notebook.
- Local file: `data/raw/kaggle_public_provider_directory/provider_directory_dataset.csv`
- License: CC0-1.0 via Kaggle dataset metadata
- Rows: 42000
- Columns: 37
- As-of date used for stale/expired checks: 2026-06-17

## Why This Matters

The official competition download still exposes only `NOTE.md`, but the public notebook now points to a substantial Kaggle-adjacent provider-directory dataset. Many NPIs appear synthetic or mock because they fail Luhn validation, so this is a transfer/readiness check rather than official truth. The Option C Hybrid package should still handle fields such as NPI, practice name, website, verification status, confidence score, change flags, and license expiry.

## Current Prototype Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0

## Highest-Volume Public Dataset Issues

| Issue | Rows | Rate |
|---|---:|---:|
| stale_verification_over_365d | 42000 | 1.0 |
| invalid_npi_luhn_or_format | 38144 | 0.90819 |
| expired_license | 25791 | 0.614071 |
| verification_needs_review | 25150 | 0.59881 |
| change_flag_high_risk | 10503 | 0.250071 |
| invalid_phone_format | 4170 | 0.099286 |
| invalid_website_format | 2560 | 0.060952 |
| invalid_zip_format | 2066 | 0.04919 |
| missing_address_line1 | 1276 | 0.030381 |
| invalid_email_format | 996 | 0.023714 |
| missing_practice_name | 0 | 0.0 |

## Triage Actions From Our Review-First Policy

| Action | Rows |
|---|---:|
| review_identity_or_status | 29863 |
| scheduled_verification | 6563 |
| urgent_review | 4958 |
| monitor_with_low_cost_refresh | 616 |

## Strategic Takeaways

- This dataset strongly supports our emphasis on stale verification, expired licenses, malformed contact data, and active/inactive review.
- NPI format alone is not enough; Luhn validation catches additional identity-quality risk.
- The public notebook scores rows, while our stronger path is to convert these signals into governed review/auto-refresh actions with audit and source evidence.
- Production should use this dataset shape as an adapter target for HealthLynked exports: preserve `provider_id`, `npi`, names, practice fields, website, status, confidence, and change flags.
