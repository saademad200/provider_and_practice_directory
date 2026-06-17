# Executive Submission Summary

## Positioning

This is an Option C Hybrid submission: a runnable provider-directory update prototype plus a production implementation plan for HealthLynked. It detects public provider/practice changes, separates safe automation from review, and preserves evidence, source reliability, audit, rollback, and human-review controls.

## Current Verified Package

- Package: `submissions/latest_final_package.zip`
- Source package: `submissions/exp0136_final_hybrid_mvp_package.zip`
- Verification: `verification.json` inside the package.
- Verification checks passed: 168
- Production readiness score: 50 / 50.
- Red-team evals passed: 7 / 7.
- Rubric self-eval: 100 / 100.

## Current Verified Proxy

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Auto-apply count: 20
- Review count: 38
- Cost per correct update: $0.005836
- Estimated evidence cost: $0.321

## Latest Metric Improvement

The promoted fresh business-listing fallback uses `business_listing` only for `phone` and `address`, only when evidence is at most 60 days old, and at low source weight. It raises F1 from 0.93913 to 0.948276 while keeping auto-apply precision at 1.0.

## What To Inspect First

1. `MVP_FIELD_COVERAGE.md`
2. `ONE_PAGE_JUDGE_GUIDE.md`
3. `REPRODUCIBILITY.md`
4. `FRESH_BUSINESS_LISTING_FALLBACK.md`
5. `JUDGE_RUBRIC_SELF_EVAL.md`
6. `PRODUCTION_READINESS_SCORECARD.md`
7. `AGENT_WORKFLOW_DIAGRAM.md`
8. `verification.json`
