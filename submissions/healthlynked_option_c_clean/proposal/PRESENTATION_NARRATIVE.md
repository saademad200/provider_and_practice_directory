# Presentation Narrative

## Opening

Provider directories decay every day. Providers move, practices rebrand, phone numbers drift, websites disagree, NPIs deactivate, and weak sources can confidently repeat old information. The winning system should not be a one-time cleanup. It should be a repeatable quality-control plane that keeps HealthLynked's directory trustworthy while controlling cost, risk, and manual labor.

## Three-Minute Talk Track

1. **The problem is continuous decay.** A static cleanup creates a short-lived improvement, but the directory starts aging again the next morning.
2. **The answer is evidence discipline.** The pipeline starts with risky or stale records, searches trusted sources, and records the exact evidence behind each suggested change.
3. **Authority matters by field.** NPPES can anchor NPI identity and taxonomy, state-board/FSMB-style sources are stronger for licensure and inactive status, and practice or health-system websites are stronger for current affiliations and locations.
4. **Normalization happens before judgment.** Names, addresses, phones, specialties, websites, practice names, and status are standardized before comparison so the system does not confuse formatting drift with real change.
5. **Matching is provider-practice-location aware.** NPI anchors identity, but movement, duplicate, affiliation, and practice-location signals prevent careless merges.
6. **Confidence is policy, not vibes.** Scores combine source authority, agreement, freshness, field risk, conflict penalties, historical stability, and normalization quality.
7. **Automation is intentionally conservative.** Low-risk, high-confidence changes can be auto-applied; identity-sensitive, conflicting, stale, or inactive-status changes go to human review.
8. **Every decision is auditable.** The recommendation explains old value, new value, sources, confidence, action, reason code, and rollback path.
9. **The MVP proves the loop.** It runs end to end with candidate updates, safe auto-apply outputs, review queue, audit events, dashboard, metrics, and recommendation JSON.
10. **The launch path is no-write first.** HealthLynked can run a shadow-mode pilot with stale-risk, high-change-risk, stable-control, and reviewer-holdout cohorts before any production mutation.
11. **The production design is cloud-portable, with AWS as a reference path.** Batch and event jobs, cached source payloads, review queues, monitoring, and field-level launch gates turn the prototype into an implementation plan for the post-award consulting period.

## Whitepaper-Informed Design

The architecture applies agentic-engineering lessons from the provided whitepapers:

- Use a governed harness, not one opaque prompt.
- Split the system into scoped agents and skills.
- Keep deterministic normalization and validation in code.
- Gate LLM extraction to the rare pages where it adds value.
- Evaluate trigger behavior, tool paths, red-team cases, source perturbations, and package integrity.
- Package reusable skills with authority tiers and approval gates.

## Closing Ask

Choose this submission if HealthLynked wants a team that can begin implementation immediately. The package is executable enough to prove the mechanics and structured enough to become a production system: source governance, normalization, identity resolution, confidence scoring, no-write shadow-mode validation, human review, safe auto-update, audit, rollback, cost controls, and a 90-day roadmap.
