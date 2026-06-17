# Failure Mode Playbook

## Purpose

Provider-directory automation is only trustworthy if failure modes are known before launch. This playbook describes common failures, detection signals, and safe responses.

| Failure Mode | Detection Signal | Immediate Response | Long-Term Fix |
|---|---|---|---|
| Source layout changes | Parser empty rate spikes or extracted fields disappear | Disable affected connector writes; route to review with stale-source flag | Update parser fixture and connector tests |
| Source becomes stale | Evidence age exceeds field policy | Penalize confidence; prevent auto-update | Adjust refresh cadence or replace source |
| Source conflict | Strong sources disagree on field value | Route to human review | Calibrate source authority and conflict rules |
| Business listing drift | Business listing disagrees with practice/health-system source | Ignore for identity/status/specialty; review phone/address if useful | Lower source weight or require fresher listing |
| LLM hallucinated extraction | Output lacks source grounding or violates schema | Reject output and route to review | Tighten extraction schema and validation |
| Duplicate provider confusion | Same NPI/name appears across practices/locations ambiguously | Stop auto-update; create identity-resolution review task | Improve provider-practice-location matching |
| Inactive status false positive | Inactive signal from one weak/stale source | Review-first; no suppression | Require license/state-board authority agreement |
| Review backlog spike | Queue exceeds SLA or priority threshold | Pause low-value recrawls; prioritize high-impact fields | Improve source filters and auto-apply thresholds |
| Cost spike | Cost per accepted update rises | Disable expensive fallback paths | Re-run source ablation and caching review |
| Bad auto-update | Reviewer or monitoring flags applied change | Roll back from audit event; quarantine similar changes | Add rule or threshold guardrail |

## Safe Defaults

- Any unknown failure mode routes to human review.
- Any identity-level change is review-first.
- Any stale or conflicting evidence blocks auto-update.
- Any LLM-derived value must be grounded, schema-valid, and corroborated.
- Any applied update must have rollback eligibility.

## Incident Workflow

1. Detect through CloudWatch/source metrics, reviewer feedback, or audit anomaly.
2. Stop affected auto-update path.
3. Preserve source payload, normalized evidence, recommendation, and audit event.
4. Identify affected providers and candidate fields.
5. Roll back applied changes if needed.
6. Add regression test or verifier check.
7. Re-enable only after shadow-mode validation passes.

## Judge Takeaway

This system is intentionally conservative. It is designed to fail closed, route uncertainty to review, and keep enough evidence to explain and reverse every applied change.
