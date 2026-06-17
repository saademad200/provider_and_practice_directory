---
name: routing-human-review
description: |
  Use when the task involves review queue, SLA, disposition, reviewer feedback. Do NOT use for source crawling or model tuning.
version: 0.1.0
allowed-tools: [Read, Bash]
metadata:
  owner: directory_ops
  authority_tier: draft-only
---
# Routing Human Review

## When To Use

- review queue, SLA, disposition, reviewer feedback

## When Not To Use

- source crawling or model tuning

## Authority Tier

- `draft-only`
- See `references/authority_tier.md`.

## Workflow

1. Load only the deterministic assets needed for the request.
2. Use structured package artifacts instead of free-form memory.
3. Apply the required eval before trusting output: review disposition contract validation and SLA metrics.
4. Never exceed this skill's authority tier.

## Deterministic Assets

- review_disposition_contract.json, review_sla_metrics.csv

## Eval Coverage

- Positive and negative trigger cases live in `evals/trigger_cases.json`.
- Side-effecting or review-affecting workflows require trajectory/red-team coverage before action.
