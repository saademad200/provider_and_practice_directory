---
name: evaluating-provider-directory-pipeline
description: |
  Use when the task involves CV metrics, red-team eval, readiness score, verifier check. Do NOT use for manual review disposition.
version: 0.1.0
allowed-tools: [Read, Bash]
metadata:
  owner: ml_ops
  authority_tier: read-only
---
# Evaluating Provider Directory Pipeline

## When To Use

- CV metrics, red-team eval, readiness score, verifier check

## When Not To Use

- manual review disposition

## Authority Tier

- `read-only`
- See `references/authority_tier.md`.

## Workflow

1. Load only the deterministic assets needed for the request.
2. Use structured package artifacts instead of free-form memory.
3. Apply the required eval before trusting output: grouped CV, trajectory eval, red-team eval, package verifier.
4. Never exceed this skill's authority tier.

## Deterministic Assets

- metrics.json, trajectory_eval_results.csv, red_team_eval_results.csv

## Eval Coverage

- Positive and negative trigger cases live in `evals/trigger_cases.json`.
- Side-effecting or review-affecting workflows require trajectory/red-team coverage before action.
