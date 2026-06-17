# Presentation Narrative

Provider directories decay continuously: providers move, practices rebrand, phone numbers change, NPIs deactivate, and public sources disagree. This submission treats that as an ongoing operations problem, not a one-time data cleanup task.

## Story

1. Start with risky or stale records instead of crawling everything.
2. Search trusted public sources with authority tiers and freshness rules.
3. Normalize names, addresses, phones, specialties, websites, affiliations, and status before comparison.
4. Match provider/practice/location identity with NPI anchors and movement/duplicate signals.
5. Score each update by source authority, agreement, freshness, field risk, and conflict penalties.
6. Auto-apply only high-confidence low-risk changes.
7. Route uncertain, conflicting, or identity-sensitive changes to human review.
8. Preserve an audit trail and rollback path for every recommendation.

## Whitepaper-Informed Design

The architecture applies agentic-engineering lessons from the provided whitepapers:

- Use a governed harness, not one opaque prompt.
- Split the system into scoped agents and skills.
- Keep deterministic normalization and validation in code.
- Gate LLM extraction to the rare pages where it adds value.
- Evaluate trigger behavior, tool paths, red-team cases, and package integrity.
- Package reusable skills with authority tiers and approval gates.

## Why It Wins

The package is both executable and implementable: a working MVP proves the loop, while the AWS architecture shows how HealthLynked can scale it into a continuous provider-directory quality operation.
