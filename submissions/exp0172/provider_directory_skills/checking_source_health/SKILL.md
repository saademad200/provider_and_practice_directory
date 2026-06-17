---
name: checking-source-health
description: |
  Use when the task involves source freshness, connector health, terms allowlist, source outage. Do NOT use for candidate scoring or directory mutation.
version: 0.1.0
allowed-tools: [Read, Bash]
metadata:
  owner: source_ops
  authority_tier: read-only
---
# Checking Source Health

## When To Use

- source freshness, connector health, terms allowlist, source outage

## When Not To Use

- candidate scoring or directory mutation

## Authority Tier

- `read-only`
- See `references/authority_tier.md`.

## Workflow

1. Load only the deterministic assets needed for the request.
2. Use structured package artifacts instead of free-form memory.
3. Apply the required eval before trusting output: positive/negative trigger tests, connector fixture, no-secrets scan.
4. Never exceed this skill's authority tier.

## Deterministic Assets

- source_connector_registry.csv, connector_health_check_fixture.csv

## Eval Coverage

- Positive and negative trigger cases live in `evals/trigger_cases.json`.
- Side-effecting or review-affecting workflows require trajectory/red-team coverage before action.
