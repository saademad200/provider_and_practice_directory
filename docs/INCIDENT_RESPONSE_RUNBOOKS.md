# Production Incident Response Runbooks

This experiment adds operational runbooks for the failures HealthLynked would care about after launch: false positive auto-updates, source outages, LLM grounding failures, audit gaps, and identity merge errors.

## Current Pipeline Context

- F1: 0.93913
- Precision: 0.947368
- Recall: 0.931034
- Auto-apply precision: 1.0
- Runbooks emitted: 5

## Runbook Matrix

| Incident | Severity | Owner | First Response | Containment | Recovery |
|---|---|---|---:|---|---|
| false_positive_auto_apply | high | directory_ops_lead | 30 min | pause auto-apply for affected field/source pair; enqueue rollback plan rows | execute approved rollback, append rollback audit event, notify downstream consumers |
| source_connector_outage | medium | source_retrieval_owner | 60 min | disable affected source in scoring or mark as stale; block auto-apply if min-source policy fails | restore connector, backfill missed snapshots, rerun missing-source robustness check |
| llm_grounding_failure | high | ml_platform_owner | 30 min | disable Bedrock fallback for affected parser route; route all derived rows to review | patch schema/prompt, regenerate affected evidence, require reviewer confirmation |
| audit_gap_detected | critical | compliance_owner | 15 min | stop production writes; freeze affected workflow run; preserve raw logs | reconstruct missing append-only event from immutable evidence bundle; document exception |
| identity_merge_error | critical | identity_resolution_owner | 30 min | block identity-level auto-merge class; move related candidates to manual review | split identity, restore prior practice affiliation, append corrective audit event |

## Operating Policy

- Critical audit or identity incidents stop production writes.
- False positive auto-apply incidents pause the affected field/source route, not the entire pipeline unless scope is unknown.
- Every rollback writes a new audit event and never mutates the original event.
- Every incident produces at least one regression artifact: case study, trajectory eval, connector health check, or parser fixture.
