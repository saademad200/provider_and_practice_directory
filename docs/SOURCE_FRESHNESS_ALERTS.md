# Source Freshness Alerts

H039 adds label-free freshness metadata to every candidate update. It does not change scoring decisions yet; it makes stale evidence visible so future iterations can gate auto-apply or trigger re-crawls.

## Current Metrics

- F1: 0.93913
- Precision: 0.947368
- Recall: 0.931034
- Auto-apply precision: 1.0
- Auto-apply count: 20
- Review count: 37

## Freshness Status Counts

- Fresh: 2
- Partially stale: 24
- All stale: 31

## Freshness By Decision

| Decision | Freshness Status | Count |
|---|---|---:|
| auto_apply | all_stale | 9 |
| auto_apply | fresh | 2 |
| auto_apply | partially_stale | 9 |
| review | all_stale | 22 |
| review | partially_stale | 15 |

## Example Stale Candidates

| Provider | Field | Decision | Status | Max Age Days | Stale Sources | Sources |
|---|---|---|---|---:|---|---|
| P0001 | specialty | review | partially_stale | 76 | practice_website | health_system, practice_website |
| P0006 | phone | review | partially_stale | 55 | nppes | health_system, nppes, practice_website |
| P0016 | accepting_new_patients | review | partially_stale | 177 | health_system | health_system, nppes |
| P0031 | address | review | all_stale | 179 | health_system, nppes, practice_website | health_system, nppes, practice_website |
| P0036 | phone | review | all_stale | 152 | health_system, nppes, practice_website | health_system, nppes, practice_website |
| P0046 | accepting_new_patients | auto_apply | partially_stale | 96 | health_system | health_system, nppes, practice_website |
| P0046 | address | review | all_stale | 107 | health_system, nppes | health_system, nppes |
| P0046 | license_status | auto_apply | all_stale | 78 | state_license | state_license |
| P0051 | accepting_new_patients | auto_apply | all_stale | 176 | health_system, nppes, practice_website | health_system, nppes, practice_website |
| P0051 | address | review | all_stale | 148 | health_system, nppes | health_system, nppes |

## Production Use

- Before auto-apply, re-fetch any candidate with `all_stale` evidence.
- For `partially_stale` evidence, keep the candidate but lower source weight or route high-risk fields to review.
- Track stale-source rates by connector as an operational SLA.
- Use stale-source alerts to schedule AWS EventBridge refresh jobs for NPPES, state-board, practice website, and health-system connectors.
