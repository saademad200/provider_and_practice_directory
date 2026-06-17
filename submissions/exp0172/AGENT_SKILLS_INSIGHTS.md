# Agent Skills Day 3 Insights

The Day 3 whitepaper reframes reusable agent work as small, owned, testable skills with progressive disclosure. For this competition, that means the provider-directory system should not become one huge prompt or one opaque agent. Its durable advantage should be a versioned library of provider-directory procedural units.

## Current Quality Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0

## Applied Insights

- Skills are procedural memory: repeatable HealthLynked workflows should become small, versioned units.
- Progressive disclosure avoids context rot: bulky source rules, schemas, and examples should live in references/assets or deterministic scripts.
- The skill description is the router: every skill-like lane needs trigger and anti-trigger tests.
- Eval coverage is broader than output quality: test trigger behavior, tool trajectory, regression against the library, and token budget under co-loaded conditions.
- Use read/draft/act tiers: provider-directory mutation and rollback must stay action-allowed only after explicit approval gates.
- Shift intelligence left: deterministic normalization, scans, hashing, verification, and cost calculations belong in scripts, not long LLM instructions.

## Provider-Directory Skill Candidates

| Skill Candidate | Owner | Authority Tier | Trigger | Anti-Trigger | Required Eval |
|---|---|---|---|---|---|
| checking-source-health | source_ops | read-only | source freshness, connector health, terms allowlist, source outage | candidate scoring or directory mutation | positive/negative trigger tests, connector fixture, no-secrets scan |
| normalizing-provider-evidence | data_quality | draft-only | normalize phone/address/specialty/license evidence | apply directory update | golden normalization fixtures and trajectory evals |
| resolving-provider-identity | identity_ops | draft-only | duplicate provider, NPI match, practice movement, rebrand | identity merge without reviewer approval | red-team wrong-provider merge, NPI mismatch fixture |
| routing-human-review | directory_ops | draft-only | review queue, SLA, disposition, reviewer feedback | source crawling or model tuning | review disposition contract validation and SLA metrics |
| auditing-and-rollback | compliance | action-allowed-after-approval | audit event, rollback plan, false positive auto-apply | new candidate generation | audit-gap red-team eval, rollback fixture, approval gate |
| evaluating-provider-directory-pipeline | ml_ops | read-only | CV metrics, red-team eval, readiness score, verifier check | manual review disposition | grouped CV, trajectory eval, red-team eval, package verifier |

## Eval Coverage Requirements

- 3 positive and 3 negative trigger cases per skill candidate
- trajectory eval for tool sequence where side effects matter
- regression check against existing package verifier
- token-budget check by keeping bulky context in references/assets
- human approval before any action-allowed workflow

## Packaging Implication

The final package should keep shipping workflow contracts, deterministic scripts, eval fixtures, and artifact manifests. If this becomes a real HealthLynked internal platform, the next step is a `provider-directory-skills/` library with one folder per candidate above, each with a `SKILL.md`, scripts, references, assets, and eval cases.
