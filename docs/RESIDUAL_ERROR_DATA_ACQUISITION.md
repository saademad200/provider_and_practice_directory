# Residual Error And Data Acquisition Plan

This artifact explains what remains after the current best pipeline. Threshold sweeps did not improve F1, so the next gains should come from new evidence, extraction quality, or identity resolution.

## Current Metrics

- F1: 0.93913
- Precision: 0.947368
- Recall: 0.931034
- False positives: 3
- False negatives: 4

## Acquisition Priorities

| Field | False Positives | False Negatives | Priority | Recommended Action |
|---|---:|---:|---:|---|
| address | 1 | 2 | 1 | Add USPS/Google-free address canonicalization plus practice-site location history. |
| specialty | 2 | 0 | 2 | Add taxonomy crosswalk plus provider-profile specialty history. |
| license_status | 0 | 1 | 3 | Add state-board status snapshots and explicit status transition rules. |
| phone | 0 | 1 | 3 | Add stronger practice-location peer consensus and phone-line type checks. |

## False Positives

| Provider | Field | Value | Decision | Sources | Review Reason |
|---|---|---|---|---|---|
| P0001 | specialty | orthopedics | review | health_system|practice_website | insufficient_auto_sources |
| P0010 | address | 1213 pine boulevard suite 4 florida | review | health_system|practice_website | insufficient_auto_sources |
| P0013 | specialty | orthopedics | review | nppes|practice_website | insufficient_auto_sources |

## False Negatives

| Provider | Field | Value | Decision | Sources | Review Reason |
|---|---|---|---|---|---|
| P0010 | address | 170 Market St, Suite 11, FL | missed |  | not_proposed |
| P0012 | phone | 555-112-2444 | missed |  | not_proposed |
| P0038 | license_status | active | missed |  | not_proposed |
| P0049 | address | 443 Oak Ave, Suite 2, FL | missed |  | not_proposed |
