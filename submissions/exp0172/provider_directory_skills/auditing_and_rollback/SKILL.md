---
name: auditing-and-rollback
description: |
  Use when the task involves audit event, rollback plan, false positive auto-apply. Do NOT use for new candidate generation.
version: 0.1.0
allowed-tools: [Read, Bash]
metadata:
  owner: compliance
  authority_tier: action-allowed-after-approval
---
# Auditing And Rollback

## When To Use

- audit event, rollback plan, false positive auto-apply

## When Not To Use

- new candidate generation

## Authority Tier

- `action-allowed-after-approval`
- See `references/authority_tier.md`.

## Workflow

1. Load only the deterministic assets needed for the request.
2. Use structured package artifacts instead of free-form memory.
3. Apply the required eval before trusting output: audit-gap red-team eval, rollback fixture, approval gate.
4. Never exceed this skill's authority tier.

## Deterministic Assets

- audit_events.jsonl, rollback_plan.csv

## Eval Coverage

- Positive and negative trigger cases live in `evals/trigger_cases.json`.
- Side-effecting or review-affecting workflows require trajectory/red-team coverage before action.
