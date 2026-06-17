# Authority Tier

- Skill: `checking-source-health`
- Owner: `source_ops`
- Authority tier: `read-only`

## Required Eval

positive/negative trigger tests, connector fixture, no-secrets scan

## Deterministic Assets

source_connector_registry.csv, connector_health_check_fixture.csv

## Rule

The skill must not perform work described by its anti-trigger: candidate scoring or directory mutation.
