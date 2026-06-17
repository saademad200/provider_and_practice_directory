---
name: normalizing-provider-evidence
description: |
  Use when the task involves normalize phone/address/specialty/license evidence. Do NOT use for apply directory update.
version: 0.1.0
allowed-tools: [Read, Bash]
metadata:
  owner: data_quality
  authority_tier: draft-only
---
# Normalizing Provider Evidence

## When To Use

- normalize phone/address/specialty/license evidence

## When Not To Use

- apply directory update

## Authority Tier

- `draft-only`
- See `references/authority_tier.md`.

## Workflow

1. Load only the deterministic assets needed for the request.
2. Use structured package artifacts instead of free-form memory.
3. Apply the required eval before trusting output: golden normalization fixtures and trajectory evals.
4. Never exceed this skill's authority tier.

## Deterministic Assets

- specialty_normalization_fixture.csv, bedrock_extraction_contract.json

## Eval Coverage

- Positive and negative trigger cases live in `evals/trigger_cases.json`.
- Side-effecting or review-affecting workflows require trajectory/red-team coverage before action.
