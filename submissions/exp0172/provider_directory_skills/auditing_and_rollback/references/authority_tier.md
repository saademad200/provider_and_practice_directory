# Authority Tier

- Skill: `auditing-and-rollback`
- Owner: `compliance`
- Authority tier: `action-allowed-after-approval`

## Required Eval

audit-gap red-team eval, rollback fixture, approval gate

## Deterministic Assets

audit_events.jsonl, rollback_plan.csv

## Rule

The skill must not perform work described by its anti-trigger: new candidate generation.
