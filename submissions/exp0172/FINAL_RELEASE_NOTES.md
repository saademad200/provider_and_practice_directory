# Final Release Notes

## Current Final Package

- Package: `submissions/latest_final_package.zip`
- Source package: `submissions/exp0172_final_combined_abc_handoff_package.zip`
- Submission mode: Option A + Option B + Option C combined.
- Verification: see `verification.json`.
- Verification checks: 98 curated-package checks.
- Public dataset CLI smoke: passes on 42,000 Kaggle-adjacent rows when the downloaded public dataset is present.
- Self no-secrets scan: see `NO_SECRETS_SCAN.md`.
- Production readiness score: 50 / 50.
- Red-team evals: 7 / 7 passed.
- Judge-rubric self-eval: 100 / 100.

## Current Metrics

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Auto-apply count: 20
- Review count: 38
- Cost per correct update: $0.005836
- Estimated evidence cost: $0.321
- Package checks passed: 98 curated-package checks

## Major Additions

| Area | Release Content |
|---|---|
| Combined A/B/C | Technical architecture, working prototype, and hybrid production scale plan in one package |
| Desired Pipeline | HealthLynked DB -> risk scan -> trusted sources -> normalize -> match -> confidence -> decision -> audit/update |
| Public Data Transfer | 42,000-row Kaggle-adjacent provider-directory profile, triage queue, and reusable CLI |
| Metric Lift | Fresh, field-gated business-listing fallback for phone/address recall |
| Robustness | Source perturbation, threshold robustness, residual analysis, verifier smoke checks, zip integrity |
| Agentic Harness | Agent Skills library, skill evals, capability profiles, AWS orchestration DAG |
| Safety | Red-team evals, source conflict adjudication, audit rollback, no-secrets scan |

## Final Submission Advice

Submit `submissions/latest_final_package.zip`. Lead with `COMBINED_ABC_PIPELINE_COVERAGE.md`, `KAGGLE_SUBMISSION_HANDOFF.md`, `COMPETITION_ALIGNMENT_REFRESH.md`, `PUBLIC_DATASET_PROFILE.md`, `MVP_FIELD_COVERAGE.md`, and `verification.json`.
