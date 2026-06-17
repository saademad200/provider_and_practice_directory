# Active-Learning Review Feedback

This experiment models the self-improving loop that should run after human review. The prototype uses synthetic gold labels to simulate reviewer decisions; production would use actual reviewer accept/reject/edit outcomes.

## Current Metrics

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Auto-apply count: 20
- Review count: 38

## Simulated Reviewer Outcomes

- Accepted candidate updates: 54
- Rejected candidate updates: 3

## Learning Actions

| Source | Field | Observations | Accept Rate | Auto-Apply Share | Recommended Action | Rationale |
|---|---|---:|---:|---:|---|---|
| practice_website | specialty | 9 | 0.7778 | 0.5556 | downweight_or_review_gate | review outcomes show elevated rejection rate |
| nppes | specialty | 7 | 0.8571 | 0.7143 | hold | enough precision for current role |
| health_system | specialty | 9 | 0.8889 | 0.5556 | hold | enough precision for current role |
| practice_website | address | 10 | 0.9 | 0.0 | hold | enough precision for current role |
| health_system | address | 12 | 0.9167 | 0.0 | hold | enough precision for current role |
| nppes | phone | 15 | 1.0 | 0.0 | consider_safe_auto_apply_expansion | high accept rate but many items still route to review |
| practice_website | phone | 14 | 1.0 | 0.0 | consider_safe_auto_apply_expansion | high accept rate but many items still route to review |
| health_system | phone | 13 | 1.0 | 0.0 | consider_safe_auto_apply_expansion | high accept rate but many items still route to review |
| health_system | accepting_new_patients | 12 | 1.0 | 0.8333 | hold | enough precision for current role |
| nppes | accepting_new_patients | 11 | 1.0 | 0.9091 | hold | enough precision for current role |
| nppes | address | 11 | 1.0 | 0.0 | consider_safe_auto_apply_expansion | high accept rate but many items still route to review |
| practice_website | accepting_new_patients | 11 | 1.0 | 0.9091 | hold | enough precision for current role |
| state_license | license_status | 5 | 1.0 | 1.0 | hold | enough precision for current role |

## Production Loop

1. Store every human review decision in RDS/Aurora with reviewer, timestamp, field, sources, freshness, and final disposition.
2. Nightly AWS Step Functions job aggregates accept/reject/edit outcomes by source, field, freshness status, and review reason.
3. Candidate source weights and field thresholds are updated only through a controlled calibration job.
4. New thresholds run in shadow mode before changing auto-apply behavior.
5. CloudWatch alarms fire if auto-apply acceptance, source freshness, or review backlog drifts outside policy.

## Why Judges Should Care

This turns the system from a static rules demo into a learning operation. Human review is no longer just a cost; it becomes the labeled signal that improves source reliability, review routing, and auto-apply safety over time.
