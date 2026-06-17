# Field Risk Policy

| Field | Risk | Candidate Gate | Auto-Apply Gate | Review Policy |
|---|---|---|---|---|
| phone | Medium | 2 sources | 4 sources + 0.96 confidence | Review if fewer than 4 sources or practice peers disagree |
| address | High | 2 sources | 4 sources + 0.97 confidence | Review if fewer than 4 sources or practice peers disagree |
| specialty | Medium | 2 sources | 4 sources + 0.97 confidence | Review if fewer than 4 sources |
| accepting_new_patients | High | 2 sources | 4 sources + 0.98 confidence | Review if fewer than 4 sources |
| license_status | High | 1 authoritative source | 1 state/license source + 0.90 confidence | Review if source is stale or missing |

Business listings are treated as low-reliability supporting evidence and downweighted to 0.35.
NPPES, state license records, health-system pages, and practice websites remain primary sources.
