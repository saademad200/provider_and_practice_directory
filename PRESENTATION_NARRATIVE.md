# Presentation Narrative

## Opening

Provider directories decay continuously. Providers move, practices rebrand, phone numbers change, rosters drift, NPIs deactivate, and public sources disagree. The winning system should not be a one-time cleanup script. It should be a repeatable operating system for evidence-backed directory updates.

This submission is built around that idea: a small runnable MVP that proves the update loop, plus an AWS production architecture that shows how HealthLynked can run the same loop continuously at scale.

## Story Arc

1. **Start with risk, not crawling everything.** The pipeline first identifies stale, incomplete, or conflicting records so cost is spent where it matters.
2. **Trust sources differently.** NPPES, state boards, CMS/public data, practice websites, health systems, and business listings are not treated as equal. Every source has authority, freshness, field scope, and fallback rules.
3. **Normalize before judging.** Phone numbers, addresses, specialties, statuses, names, and affiliations are normalized before comparison so the system avoids false changes caused by formatting noise.
4. **Match identity carefully.** NPI anchors the provider when available; name/address/phone/specialty/practice signals help detect duplicates, movement, practice changes, and inactive providers.
5. **Score confidence by field.** The system scores each proposed update with source agreement, freshness, authority, field risk, and conflict penalties.
6. **Separate discovery from mutation.** Finding a likely update is not the same as applying it. Low-risk high-confidence updates can be auto-applied; identity-sensitive, conflicting, or low-confidence changes go to human review.
7. **Make every update auditable.** Every recommendation keeps the old value, proposed value, sources, URLs, confidence logic, review reason, audit event, and rollback path.
8. **Use agents as a governed harness.** The whitepaper-guided design uses scoped agents, skills, contracts, evals, and AWS orchestration instead of one opaque agent prompt.

## Why It Wins

- It answers every evaluation criterion directly.
- It includes a working prototype and a production architecture.
- It is cost-aware by design, not as an afterthought.
- It treats human review as a precision tool, not a dumping ground.
- It is explainable enough for healthcare operations.
- It is deployable by a lean team on AWS.

## Judge Close

The deliverable is not just a proposal and not just a notebook. It is a practical blueprint for how HealthLynked can continuously improve provider data quality with safe automation, transparent evidence, and a production-ready review/audit workflow.
