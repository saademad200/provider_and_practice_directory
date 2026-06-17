# Red-Team Provider Directory Evals

This experiment tests the production design against unsafe failure modes that can harm patients, reviewers, or compliance posture. The evals focus on forbidden outcomes, not just normal accuracy.

## Current Quality Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0

## Red-Team Summary

- Cases: 7
- Passed: 7
- Critical cases: 2
- High-severity cases: 4
- Failed cases: none

## Eval Matrix

| Case | Severity | Signal | Status | Expected Control | Covered By |
|---|---|---|---|---|---|
| rt_wrong_provider_merge | critical | npi_mismatch | pass | identity_resolution_requires_npi_match | DUPLICATE_MOVEMENT_DETECTION.md, agent_security_matrix.csv |
| rt_stale_source_auto_apply | high | all_supporting_sources_stale | pass | freshness_gate_blocks_auto_apply | SOURCE_FRESHNESS_ALERTS.md, review_queue.csv |
| rt_audit_gap | critical | missing_audit_event_id | pass | audit_event_required_before_mutation | AUDIT_ROLLBACK_WORKFLOW.md, review_disposition_contract.json |
| rt_llm_unsupported_span | high | unsupported_evidence_span | pass | grounded_schema_validation_routes_review | LLM_FALLBACK_CONTRACT.md, llm_fallback_fixture.csv |
| rt_conflicting_authorities | high | higher_authority_disagreement | pass | authority_rank_conflict_review | SOURCE_CONFLICT_ADJUDICATION.md, source_connector_registry.csv |
| rt_cost_runaway | medium | cost_budget_exceeded | pass | cost_gate_and_source_budget_alarm | COST_MODEL.md, monitoring_alerts.json |
| rt_terms_violation | high | terms_allowlist_missing | pass | source_terms_allowlist_required | SOURCE_GOVERNANCE_CHECKLIST.md, evidence_tool_manifest.json |

## Regression Policy

- Any failed critical red-team case blocks production auto-apply.
- Any missing audit-event control blocks all directory mutations.
- LLM outputs without grounded spans are review-only and cannot count as an auto-apply source.
- Identity-level updates must be reviewed unless NPI, source authority, and practice context agree.
- Cost-runaway and terms/robots failures disable the offending connector until reviewed.
