# Source Freshness Alerts

The prototype attaches source-age metadata to every candidate update and uses that metadata as an auto-apply safety gate. A record can only auto-apply when it passes confidence, source agreement, field-risk, and freshness checks together.

## Safe Auto-Apply Freshness Gate

Auto-apply is intentionally narrow in this MVP:

- Allowed fields: `phone` and `specialty` by default.
- Allowed freshness: `fresh` or `partially_stale`, never `all_stale`.
- Required support: high confidence, enough independent trusted sources, and no high-risk review driver.
- High-risk fields such as address, license status, accepting-new-patients, activity status, and affiliations are review-first unless the production owner explicitly widens the safe-field list.

This keeps the automated path conservative while still demonstrating how a repeatable pipeline can reduce manual work without accepting unsupported changes.

## Current Metrics

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Auto-apply count: 3
- Review count: 55

## Freshness Status Counts

- Fresh: 2
- Partially stale: 25
- All stale: 31

## Freshness By Decision

| Decision | Freshness Status | Count |
|---|---|---:|
| auto_apply | partially_stale | 3 |
| review | all_stale | 31 |
| review | fresh | 2 |
| review | partially_stale | 22 |

## Safe Auto-Apply Examples

| Provider | Field | Decision | Status | Max Age Days | Stale Sources | Sources |
|---|---|---|---|---:|---|---|
| P0005 | specialty | auto_apply | partially_stale | 170 | health_system, practice_website | health_system, nppes, practice_website |
| P0022 | specialty | auto_apply | partially_stale | 146 | nppes, practice_website | health_system, nppes, practice_website |
| P0025 | specialty | auto_apply | partially_stale | 108 | health_system, nppes | health_system, nppes, practice_website |

## Review-Routed Stale Examples

| Provider | Field | Decision | Status | Max Age Days | Stale Sources | Sources | Review Reason |
|---|---|---|---|---:|---|---|---|
| P0004 | address | review | all_stale | 141 | health_system, practice_website | health_system, practice_website | insufficient_auto_sources, field_not_safe_for_auto_apply, stale_or_missing_supporting_evidence |
| P0010 | address | review | all_stale | 126 | health_system, practice_website | health_system, practice_website | insufficient_auto_sources, field_not_safe_for_auto_apply, stale_or_missing_supporting_evidence |
| P0046 | address | review | all_stale | 107 | health_system, nppes | health_system, nppes | insufficient_auto_sources, field_not_safe_for_auto_apply, stale_or_missing_supporting_evidence |
| P0048 | address | review | all_stale | 171 | nppes, practice_website | nppes, practice_website | insufficient_auto_sources, field_not_safe_for_auto_apply, stale_or_missing_supporting_evidence |
| P0063 | address | review | all_stale | 132 | health_system, nppes | health_system, nppes | insufficient_auto_sources, field_not_safe_for_auto_apply, stale_or_missing_supporting_evidence |
| P0027 | accepting_new_patients | review | all_stale | 116 | health_system, practice_website | health_system, practice_website | insufficient_auto_sources, field_not_safe_for_auto_apply, stale_or_missing_supporting_evidence |
| P0003 | address | review | all_stale | 156 | health_system, nppes, practice_website | health_system, nppes, practice_website | field_not_safe_for_auto_apply, stale_or_missing_supporting_evidence |
| P0017 | address | review | all_stale | 120 | health_system, nppes, practice_website | health_system, nppes, practice_website | field_not_safe_for_auto_apply, stale_or_missing_supporting_evidence |
| P0031 | address | review | all_stale | 179 | health_system, nppes, practice_website | health_system, nppes, practice_website | field_not_safe_for_auto_apply, stale_or_missing_supporting_evidence |
| P0039 | address | review | all_stale | 136 | health_system, nppes, practice_website | health_system, nppes, practice_website | field_not_safe_for_auto_apply, stale_or_missing_supporting_evidence |

## Production Use

- Re-fetch any candidate with `all_stale` evidence before a human approves it.
- Permit `partially_stale` auto-apply only for configured low/medium-risk fields with a fresh corroborating source.
- Route high-risk fields to review even when the confidence score is high.
- Track stale-source rates by connector as an operational SLA.
- Use stale-source alerts to schedule AWS EventBridge refresh jobs for NPPES, state-board, practice website, and health-system connectors.
