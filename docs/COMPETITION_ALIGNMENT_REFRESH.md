# Competition Alignment Refresh

## Live Kaggle Surface

- Checked via Kaggle API/CLI on 2026-06-17.
- Competition files available through the API: `NOTE.md` only.
- Leaderboard results: none returned by the CLI.
- Public notebooks: one observed, `chaitanyajamble/provider-and-practice-directory`, title `Provider and Practice directory`, 0 votes at pull time.
- Public notebook local copy: `data/raw/kaggle_kernels/chaitanyajamble_provider-and-practice-directory/`.

## Strategic Read

The visible public notebook is a useful baseline, but it is mostly a directory-health scoring notebook. It does not appear to solve the harder HealthLynked production problem: finding public/legal evidence, normalizing source observations, producing citation-backed field updates, separating auto-apply from human review, and maintaining audit/rollback controls. Our best path remains Option C Hybrid.

## Current Verified Metrics

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Review count: 55
- Latest package: `submissions/latest_final_package.zip`

## Evaluation Criteria Coverage

| Criterion | Our Answer | Primary Artifacts |
|---|---|---|
| Option C Hybrid submission | Runnable prototype plus production architecture and operating model. | README.md; MVP_FIELD_COVERAGE.md; ARCHITECTURE.md; AWS_PRODUCTION_ARCHITECTURE.md; verification.json |
| Accuracy | Validated local proxy with F1 0.948276, precision 0.948276, recall 0.948276, and auto-apply precision 1.0. | metrics.json; cv_metrics.json; THRESHOLD_ROBUSTNESS_SWEEP.md; RESIDUAL_ERROR_DATA_ACQUISITION.md |
| Scalability | Batchable AWS design with Step Functions orchestration and synthetic 100x throughput plan. | SYNTHETIC_VOLUME_BENCHMARK.md; aws_step_functions_throughput_plan.csv; CAPABILITY_PROFILES_AND_ORCHESTRATION.md |
| Cost efficiency | Cheap deterministic/public-source evidence first; optional Bedrock extraction only for messy pages. | COST_MODEL.md; cost_model_per_1000.csv; LLM_FALLBACK_CONTRACT.md; source_ablation.csv |
| Practicality | Emits candidate updates, auto-apply queue, review queue, audit events, rollback plan, and dashboard data. | candidate_updates.csv; auto_apply_updates.csv; review_queue.csv; audit_events.jsonl; dashboard/index.html |
| Explainability | Every proposed update carries before/after values, confidence, source list, URLs, freshness, and review reasons. | candidate_updates.csv; REVIEW_QUEUE_PRIORITIZATION.md; SOURCE_CONFLICT_ADJUDICATION.md |
| Data quality | Normalization for phone, address, specialty, license status, patient acceptance, source freshness, and duplicate/movement signals. | SPECIALTY_NORMALIZATION.md; DUPLICATE_MOVEMENT_DETECTION.md; FIELD_RISK_POLICY.md; BENCHMARK_DATASHEET.md |
| Source reliability | Authority-tiered connector registry and guarded business-listing fallback only for fresh phone/address evidence. | SOURCE_CONNECTOR_REGISTRY.md; SOURCE_PERTURBATION_STRESS_TESTS.md; FRESH_BUSINESS_LISTING_FALLBACK.md |
| Human review design | Uncertain, stale, conflicting, identity-risking, and peer-mismatched updates route to prioritized review with disposition contracts. | review_queue.csv; REVIEW_DISPOSITION_AND_SLA.md; review_disposition_contract.json |
| Audit trail | Append-only event fixture, rollback plan, change timeline, package manifest, and no-secrets scan. | audit_events.jsonl; rollback_plan.csv; provider_change_timeline.csv; PACKAGE_INTEGRITY_MANIFEST.md; NO_SECRETS_SCAN.md |
| Bonus coverage | Dashboard, duplicate detection, NPI validation, inactive detection, movement/rebrand detection, confidence formula, and roadmap. | MVP_FIELD_COVERAGE.md; dashboard/index.html; NPPES_API_SMOKE.md; INACTIVE_PROVIDER_DETECTION.md; PRACTICE_AFFILIATION_REBRAND.md |

## Public Notebook Gap Analysis

Notebook summary: Baseline notebook scores internal directory health using structural, semantic, temporal, duplicate-risk, and change-velocity signals, then writes a priority-sorted submission CSV.

| Observed Strength | Observed Gap | Our Response |
|---|---|---|
| Has a runnable tabular scoring baseline with structural, temporal, duplicate-risk, and action-priority features. | No external evidence collection or citation-backed update candidate workflow. | Candidate updates preserve sources, URLs, freshness, old/new values, confidence, review reasons, and decisions. |
| Uses duplicate-risk signals via TF-IDF blocking. | Duplicate handling is a score, not a governed merge/review workflow. | Duplicate and movement candidates are review-routed with rollback and audit artifacts. |
| Creates a submission CSV from an attached dataset. | No production architecture, AWS path, source governance, cost model, or human-review SLA. | Option C package includes AWS architecture, cost model, source connector registry, review SLA, and verifier. |

## Implication For Next Iterations

- Keep the final submission framed as Option C Hybrid.
- Do not chase the public notebook's internal-health-score framing as the primary solution.
- Continue strengthening source-governed updates, review operations, auditability, AWS deployment, and field-level coverage.
