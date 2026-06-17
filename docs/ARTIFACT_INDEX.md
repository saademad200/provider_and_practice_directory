# Artifact Index

This index helps judges navigate the submitted package without guessing which file supports which rubric category.

## Current Quality Context

- F1: 0.93913
- Precision: 0.947368
- Recall: 0.931034
- Auto-apply precision: 1.0

## Category Counts

| Category | Files |
|---|---:|
| agentic_harness | 1 |
| audit | 2 |
| dashboard | 2 |
| human_review | 3 |
| judge_narrative | 1 |
| metrics | 2 |
| prototype_outputs | 1 |
| readiness | 1 |
| safe_automation | 1 |
| safety | 2 |
| scalability | 2 |
| source_reliability | 2 |
| start_here | 1 |
| supporting_artifact | 78 |
| verification | 1 |
| workflow | 2 |

## Priority Artifacts

| Artifact | Category | Purpose | Size Bytes |
|---|---|---|---:|
| README.md | start_here | Package entrypoint and recommended reading order. | 794 |
| EXECUTIVE_SUMMARY.md | judge_narrative | High-level positioning, metrics, and rubric mapping. | 3892 |
| AGENT_WORKFLOW_DIAGRAM.md | workflow | Agentic workflow diagram with source-to-review-to-audit handoffs. | 3700 |
| agent_workflow_diagram.mmd | workflow | Mermaid source for the workflow diagram. | 1033 |
| PRODUCTION_READINESS_SCORECARD.md | readiness | Maps judging criteria to evidence, checks, gaps, and next actions. | 3873 |
| RED_TEAM_EVALS.md | safety | Forbidden-outcome red-team tests and regression policy. | 2126 |
| red_team_eval_results.csv | safety | Red-team case outcomes. | 2947 |
| candidate_updates.csv | prototype_outputs | All proposed provider-directory updates with evidence and confidence. | 21699 |
| REVIEW_DISPOSITION_AND_SLA.md | human_review | Reviewer disposition schema, SLA metrics, and feedback loop. | 2294 |
| review_disposition_contract.json | human_review | Structured reviewer decision contract. | 2185 |
| review_queue.csv | human_review | Ambiguous or high-risk updates routed to manual review. | 14339 |
| SOURCE_CONNECTOR_REGISTRY.md | source_reliability | Connector authority, freshness, cost, fallback, and health contracts. | 3214 |
| source_ablation.csv | source_reliability | Source value and cost diagnostic. | 341 |
| aws_step_functions_throughput_plan.csv | scalability | AWS batch fan-out sizing scenarios. | 897 |
| synthetic_volume_benchmark.csv | scalability | 100x local throughput benchmark. | 435 |
| verification.json | verification | Machine-readable package verification results. | 15828 |
| cv_metrics.json | metrics | Grouped-CV proxy benchmark metrics. | 8322 |
| metrics.json | metrics | CLI/prototype metrics. | 478 |
| dashboard/index.html | dashboard | Static operations dashboard prototype. | 16965 |
| dashboard_v2/index.html | dashboard | Lifecycle, LLM, and rollback dashboard lanes. | 16965 |
| audit_events.jsonl | audit | Append-only audit trail sample. | 44305 |
| rollback_plan.csv | audit | Rollback plan for applied updates. | 3285 |
| evidence_tool_manifest.json | agentic_harness | Evidence connector tool schemas and permissions. | 11371 |
| auto_apply_updates.csv | safe_automation | Subset eligible for low-risk auto-apply. | 7679 |
| ACTIVE_LEARNING_FEEDBACK.md | supporting_artifact | Supporting package artifact. | 2909 |
| AGENTIC_WHITEPAPER_INSIGHTS.md | supporting_artifact | Supporting package artifact. | 2282 |
| AGENT_CARDS_AND_WORKFLOW_CONTRACTS.md | supporting_artifact | Supporting package artifact. | 3361 |
| AGENT_SECURITY_MATRIX.md | supporting_artifact | Supporting package artifact. | 2773 |
| ARCHITECTURE.md | supporting_artifact | Supporting package artifact. | 1875 |
| AUDIT_ROLLBACK_WORKFLOW.md | supporting_artifact | Supporting package artifact. | 1455 |
| AWS_PRODUCTION_ARCHITECTURE.md | supporting_artifact | Supporting package artifact. | 4092 |
| BENCHMARK_DATASHEET.md | supporting_artifact | Supporting package artifact. | 4170 |
| CASE_STUDIES.md | supporting_artifact | Supporting package artifact. | 2475 |
| COST_MODEL.md | supporting_artifact | Supporting package artifact. | 1856 |
| DASHBOARD_SPEC.md | supporting_artifact | Supporting package artifact. | 4679 |

## Inspection Guidance

- Start with `README.md` and `EXECUTIVE_SUMMARY.md`.
- Then inspect workflow, readiness, red-team, source registry, and human-review handoff docs.
- Use `verification.json` to confirm machine checks and `candidate_updates.csv` to inspect the runnable prototype output.
