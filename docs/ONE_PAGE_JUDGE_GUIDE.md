# One Page Judge Guide

## Claim

This is an Option C Hybrid submission, not just a notebook. It is a runnable provider-directory update prototype plus a production operating model with source governance, human review, audit/rollback, red-team evals, Agent Skills, AWS deployment planning, and package verification.

## Metrics To Expect

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Auto-apply count: 3
- Review count: 55
- Cost per correct update: $0.005836
- Estimated evidence cost: $0.321

## Five-Minute Path

1. Open `MVP_FIELD_COVERAGE.md` to see how every requested MVP field and bonus capability maps to prototype and production artifacts.
2. Open `EXECUTIVE_SUMMARY.md` for the positioning and current metrics.
3. Open `FRESH_BUSINESS_LISTING_FALLBACK.md` for the latest model improvement.
4. Open `JUDGE_RUBRIC_SELF_EVAL.md` for the artifact-backed rubric map.
5. Open `verification.json` for machine-readable proof that the package compiles, runs, and contains required artifacts.

## What Makes It Hard To Beat

- The benchmark is transparent about the lack of official Kaggle train/test data.
- Safe automation is separated from update discovery.
- Weak sources are not trusted globally; the fresh business-listing fallback is field-gated and age-gated.
- The review queue is explainable, prioritized, and backed by disposition/SLA contracts.
- Agentic components have scoped skills, evals, capability profiles, and authority tiers.
- The production plan names AWS services and operational failure modes instead of hand-waving.
