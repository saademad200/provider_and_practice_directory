# Production Readiness Scorecard

This scorecard maps the HealthLynked judging surface to concrete evidence, machine checks, remaining gaps, and next actions. Artifact presence checks now trace evidence across docs, scripts, packaged outputs, and latest result directories.

## Current Proxy Metrics

- F1: 0.93913
- Precision: 0.947368
- Recall: 0.931034
- Auto-apply precision: 1.0
- Cost per correct update: $0.005609

## Readiness Summary

- Criteria scored: 10
- Strong criteria: 10
- Readiness score: 50 / 50
- Readiness percent: 1.0
- Lowest scoring criteria: accuracy, agentic_harness, auditability

## Criterion Map

| Criterion | Status | Score | Artifact Presence | Judge Signal | Remaining Gap | Next Action |
|---|---|---:|---:|---|---|---|
| accuracy | strong | 5/5 | 5/5 | High precision/recall on a reproducible grouped proxy benchmark. | Proxy benchmark is synthetic because no official train/test data was provided. | Add any official/private fixtures immediately if HealthLynked releases them. |
| safe_auto_apply | strong | 5/5 | 4/4 | Separates detection from write eligibility with conservative review gates. | Real deployment still needs sampled post-apply QA and rollback rehearsals. | Attach sampled human QA outcomes to active-learning retraining loop. |
| source_reliability | strong | 5/5 | 4/4 | Uses source ablation, freshness checks, conflict handling, and public-source governance. | Need live connector health checks for every production source. | Add a connector registry with health-check policy and stale-source fallback rules. |
| data_quality | strong | 5/5 | 4/4 | Normalizes phone, address, specialty, practice affiliation, inactive status, and identity movement. | Need more geography-specific address edge cases for national rollout. | Expand address fixtures with USPS-like secondary unit and rural route cases. |
| human_review | strong | 5/5 | 4/4 | Ambiguous or high-risk items are ranked with reason codes, evidence URLs, and reviewer context. | Dashboard is static; production needs reviewer authentication and disposition capture. | Add dashboard contract for dispositions and SLA/workload metrics. |
| auditability | strong | 5/5 | 4/4 | Every candidate can be tied to evidence, timeline, audit event, rollback plan, and trajectory trace. | Production should enforce append-only audit storage and transactionally require event IDs. | Wire event schemas into the AWS architecture and incident runbooks. |
| cost_efficiency | strong | 5/5 | 4/4 | Cheap source-first design with explicit per-1,000 cost and gated LLM fallback. | Live web retrieval and review labor costs must be recalibrated with real volume. | Add AWS batch sizing, cache hit assumptions, and sensitivity analysis. |
| scalability | strong | 5/5 | 7/7 | Batch CLI, modular source connectors, AWS production map, monitoring alerts, and operational runbooks. | Cloud SLA still requires a real AWS load test with production connectors. | Run a shadow-mode AWS load test once HealthLynked connector credentials and source limits are available. |
| agentic_harness | strong | 5/5 | 4/4 | Specialized agent lanes have explicit contracts, permissions, trajectory evals, and security controls. | Need live tool invocation traces once connected to production sources. | Emit trace IDs and tool-call spans into every candidate row. |
| submission_clarity | strong | 5/5 | 4/4 | A judge can start from README, inspect metrics, open dashboards, and verify package integrity. | Latest scorecard must be packaged into the final zip. | Refresh final package after scorecard and dashboard readiness updates. |

## How To Use

- Treat any criterion below 5 as the next packaging or engineering opportunity.
- Keep this scorecard in the final zip so judges can trace each claim to a file.
- Update `scripts/verify_pipeline.py` whenever a scorecard artifact becomes mandatory.
