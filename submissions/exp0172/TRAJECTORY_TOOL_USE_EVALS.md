# Trajectory And Tool-Use Eval Rubric

This experiment adds an agentic-engineering eval layer for how the workflow ran, not only what output it produced. It catches dangerous traces such as skipping audit writes, calling an LLM without a cost gate, or silently dropping conflicting evidence.

## Current Pipeline Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0

## Fixture Trace Evaluation

| Run | Passed | Score | Missing Required Events | Forbidden Events | Recommended Action |
|---|---:|---:|---|---|---|
| bad_trace | False | 0.24 | identity_resolution, source_conflict_check, route_review, write_audit_event, emit_monitoring_metrics | call_llm_without_cost_gate, write_update_without_audit | block_and_debug_trace |
| good_trace | True | 1.0 |  |  | ship_candidate |

## Rubric

| Type | Event | Weight | Rationale |
|---|---|---:|---|
| required | source_fetch | 0.08 | Required workflow step for reliable provider-directory automation. |
| required | normalize_evidence | 0.08 | Required workflow step for reliable provider-directory automation. |
| required | identity_resolution | 0.08 | Required workflow step for reliable provider-directory automation. |
| required | source_conflict_check | 0.08 | Required workflow step for reliable provider-directory automation. |
| required | score_candidates | 0.08 | Required workflow step for reliable provider-directory automation. |
| required | route_review | 0.08 | Required workflow step for reliable provider-directory automation. |
| required | write_audit_event | 0.08 | Required workflow step for reliable provider-directory automation. |
| required | emit_monitoring_metrics | 0.08 | Required workflow step for reliable provider-directory automation. |
| forbidden | read_gold_updates_for_generation | 0.18 | Unsafe or leakage-prone behavior that should block production runs. |
| forbidden | auto_apply_identity_delete | 0.18 | Unsafe or leakage-prone behavior that should block production runs. |
| forbidden | drop_conflicting_value_without_reason | 0.18 | Unsafe or leakage-prone behavior that should block production runs. |
| forbidden | call_llm_without_cost_gate | 0.18 | Unsafe or leakage-prone behavior that should block production runs. |
| forbidden | write_update_without_audit | 0.18 | Unsafe or leakage-prone behavior that should block production runs. |

## Production Use

- Run this rubric on every Step Functions execution or equivalent orchestrator trace.
- Block production writes when forbidden events appear.
- Treat missing required events as regression failures, even when final candidate CSVs look plausible.
- Feed trace failures into the same active-learning/incident review loop as model and source errors.
