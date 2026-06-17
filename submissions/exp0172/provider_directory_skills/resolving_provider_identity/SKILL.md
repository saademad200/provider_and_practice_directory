---
name: resolving-provider-identity
description: |
  Use when the task involves duplicate provider, NPI match, practice movement, rebrand. Do NOT use for identity merge without reviewer approval.
version: 0.1.0
allowed-tools: [Read, Bash]
metadata:
  owner: identity_ops
  authority_tier: draft-only
---
# Resolving Provider Identity

## When To Use

- duplicate provider, NPI match, practice movement, rebrand

## When Not To Use

- identity merge without reviewer approval

## Authority Tier

- `draft-only`
- See `references/authority_tier.md`.

## Workflow

1. Load only the deterministic assets needed for the request.
2. Use structured package artifacts instead of free-form memory.
3. Apply the required eval before trusting output: red-team wrong-provider merge, NPI mismatch fixture.
4. Never exceed this skill's authority tier.

## Deterministic Assets

- duplicate_candidates.csv, provider_movement_candidates.csv

## Eval Coverage

- Positive and negative trigger cases live in `evals/trigger_cases.json`.
- Side-effecting or review-affecting workflows require trajectory/red-team coverage before action.
