# Judge Decision Memo

## Recommendation

Select this Option C submission because it is not only an architecture proposal and not only a notebook demo. It is a practical operating model HealthLynked can start implementing immediately: source-governed evidence collection, deterministic normalization, conservative confidence scoring, human review for uncertain records, safe auto-update for low-risk changes, and an audit trail for every recommendation.

## Why This Is Different

Most provider-directory cleanup systems fail in one of three ways:

1. They scrape broadly but cannot explain why a record should change.
2. They produce impressive AI outputs but cannot control cost or prove source reliability.
3. They clean a sample once but do not become a repeatable update pipeline.

This design avoids those traps by separating evidence retrieval, normalization, identity resolution, confidence scoring, decision routing, human review, and audit. Each stage has a contract and can be tested independently.

## What HealthLynked Gets On Day One

- A runnable MVP with candidate updates, auto-apply updates, review queue, recommendation JSON, metrics, and audit events.
- An cloud-agnostic production architecture for periodic and continuous refresh, with portable service boundaries.
- A trusted-source connector plan for NPPES, CMS files, state boards/FSMB, practice websites, health-system directories, and carefully limited fallback sources.
- A confidence and decision policy that explains exactly when a change is auto-applied, reviewed, or rejected.
- A sample human review dashboard and review disposition loop.
- A no-write shadow-mode pilot protocol with cohort design, reviewer dispositions, holdout replay, field-level launch gates, and rollback drills.
- A 90-day roadmap suitable for the expected post-award consulting engagement.

## The Core Product Bet

The effective solution is not "use an LLM to search providers." it is a directory-quality control plane:

- Source authority decides what evidence is allowed to influence each field.
- Freshness and conflict rules prevent stale or weak evidence from silently changing records.
- Identity-sensitive changes are review-first.
- Low-risk, high-confidence field updates can be automated safely.
- Every recommendation is explainable, reversible, and measurable.

## Why It Can Scale

The architecture uses deterministic and cached sources first, then reserves LLM extraction for messy approved pages after cheaper parsers fail. Batch ingestion handles large public files, event orchestration handles periodic refresh, and review queues focus humans only where judgment is needed.

## Why It Is Cost-Aware

The current proxy run estimates prototype evidence-only cost per correct update at `$0.005836`. The production cost model separately includes per-1,000-record scenarios for cloud infrastructure (AWS reference), LLM fallback, and human-review labor. The production design keeps total cost low by:

- prioritizing stale/risky records before broad refresh;
- using NPPES/CMS/state-board snapshots where possible;
- caching raw evidence and parser outputs;
- deduplicating source requests across providers in the same practice;
- only calling LLM extraction when deterministic parsing is sparse or ambiguous.

## Monday-Morning Implementation Plan

1. Confirm HealthLynked schema, update-risk fields, and source terms.
2. Run the MVP on a de-identified HealthLynked sample in shadow mode.
3. Apply the shadow-mode pilot protocol: stale-risk sample, high-change-risk sample, stable control sample, and reviewer holdout.
4. Connect NPPES batch/API and one state-board/practice-site connector family.
5. Calibrate confidence thresholds against reviewer decisions and holdout replay.
6. Launch a dashboard queue for review-only recommendations.
7. Enable safe auto-update only for fields that pass the field-level launch gates.

## What Would Make This Unsafe

The system should not auto-apply:

- provider identity merges;
- inactive/retired status;
- specialty changes from weak sources;
- practice affiliation moves with conflicting evidence;
- address changes without strong source agreement;
- any field where evidence is stale, single-source, or authority-inappropriate.

Those cases go to human review with sources, confidence, reason codes, and rollback context.

## Judge Objection Handling

| Concern | Response |
| --- | --- |
| "The prototype uses proxy data, so why trust it?" | The metrics are intentionally framed as engineering proof, not production truth. The transfer plan requires HealthLynked shadow-mode calibration before production writes. |
| "This may be too complex for a lean team." | The MVP starts with deterministic connectors, cached evidence, conservative review routing, and only a small set of low-risk auto-update fields. Agents are bounded workers, not an uncontrolled autonomous system. |
| "LLM search could become expensive or unreliable." | LLM extraction is a fallback only after approved deterministic parsing fails, and outputs are schema-validated, source-grounded, confidence-scored, and review-only when uncertain. |
| "Bad auto-updates could damage trust." | Identity-sensitive and high-risk changes are review-first; auto-apply requires strong agreement, fresh evidence, allowed fields, audit events, and rollback records. |
| "How do we know it is ready for production?" | The shadow-mode protocol requires no-write pilot cohorts, reviewer dispositions, holdout replay, source quarantine, precision gates, and rollback drills before any field is enabled. |
| "Source conflicts are unavoidable." | Source authority, freshness, and field-specific reliability are explicit scoring inputs; conflicts lower confidence and route records to review with reason codes. |

## Decision

This submission is strongest when the goal is to hire a consultant team that can actually implement the pipeline after the competition. It gives judges a working prototype, production architecture, operating policy, and evidence trail in one coherent package.
