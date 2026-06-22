# Agent Workflow Diagram

This diagram shows the controlled agent workflow behind the provider/practice update pipeline. The design is deliberately not a single opaque agent. Each lane has a narrow job, deterministic validation, bounded tool access, and a traceable handoff into review or audit.

## Mermaid Diagram

```mermaid
flowchart LR
    schedule[Cloud Scheduler (AWS EventBridge reference)] --> registry[Source Connector Registry]
    registry --> retrieval[Source Retrieval Agents]
    retrieval --> normalize[Evidence Normalization Agent]
    normalize --> identity[Provider / Practice Identity Agent]
    identity --> conflict[Source Conflict Resolver]
    conflict --> score[Confidence Scoring Agent]
    score --> shadow[Shadow-Mode Calibration Agent]
    shadow --> safety[Safety And Policy Gates]
    safety --> route{Decision Router}
    route -->|safe low-risk update| audit[Audit And Rollback Agent]
    route -->|ambiguous or high-risk| review[Human Review Workbench]
    review --> audit
    audit --> monitor[Monitoring And Learning Loop]
    monitor --> registry

    classDef agent fill:#e8f1f8,stroke:#1e6b9e,color:#16202a
    classDef human fill:#fff4df,stroke:#9a6b1d,color:#16202a
    classDef safetyClass fill:#fbe7e7,stroke:#a33a3a,color:#16202a
    class registry,retrieval,normalize,identity,conflict,score,shadow,audit,monitor agent
    class review human
    class safety safetyClass
```

## Render-Free Diagram

```text
Cloud scheduler (AWS EventBridge reference)
  -> source connector registry
  -> source retrieval agents
  -> evidence normalization agent
  -> provider / practice identity agent
  -> source conflict resolver
  -> confidence scoring agent
  -> shadow-mode calibration agent
  -> safety and policy gates
  -> decision router
       -> safe low-risk update: audit and rollback agent
       -> ambiguous or high-risk: human review workbench
  -> monitoring and learning loop
```

Every agent has a narrow contract, field-level evidence, and a policy gate before any directory mutation.

## Agent Responsibilities

| Agent | Responsibility | Guardrail | Package Evidence |
|---|---|---|---|
| Source Connector Registry | Chooses approved sources by authority, cost, freshness, and field coverage | No source is used without access policy and health checks | `evidence/source_connector_registry.csv` |
| Source Retrieval Agents | Pull NPPES, CMS/state board, practice-site, health-system, and fallback listing evidence | Paid or LLM extraction is gated behind deterministic failure reasons | `proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md`, `proposal/SOURCE_ACCESS_COMPLIANCE_POLICY.md` |
| Evidence Normalization Agent | Normalizes names, phones, addresses, specialties, and practice aliases | Raw and normalized values stay side by side for audit | `src/data.py`, `src/specialty.py`, `prototype/candidate_updates.csv` |
| Provider / Practice Identity Agent | Matches provider, NPI, practice, and location candidates | Identity-level changes never bypass review | `appendix/DUPLICATE_MOVEMENT_DETECTION.md`, `evidence/provider_movement_candidates.csv` |
| Source Conflict Resolver | Compares authority, freshness, consensus, and field risk | Conflicts lower confidence and create reviewer-visible reason codes | `appendix/SOURCE_CONFLICT_ADJUDICATION.md`, `proposal/CONFIDENCE_AND_DECISION_POLICY.md` |
| Confidence Scoring Agent | Produces update confidence, review priority, and action recommendation | Scores are decomposed into explainable factors | `prototype/RECOMMENDATION_API_CONTRACT.md`, `prototype/recommendation_api_examples.json` |
| Shadow-Mode Calibration Agent | Converts reviewer dispositions into field-level launch states and threshold changes | No production write threshold changes without holdout replay and launch-gate evidence | `proposal/SHADOW_MODE_PILOT_PROTOCOL.md`, `dashboard/index.html` |
| Safety And Policy Gates | Blocks stale, high-risk, identity-level, or weakly supported auto-updates | Auto-apply is allowed only for configured low-risk fields | `prototype/auto_apply_updates.csv`, `evidence/verification.json` |
| Human Review Workbench | Presents only uncertain, conflicting, or high-risk records | Reviewer decisions create training and audit feedback | `dashboard/index.html`, `prototype/review_queue.csv` |
| Audit And Rollback Agent | Writes event records, evidence hashes, and rollback rows | Every mutation has evidence and restore path | `evidence/audit_events.jsonl`, `evidence/rollback_plan.csv` |
| Monitoring And Learning Loop | Tracks connector health, cost drift, reviewer outcomes, and threshold drift | Learning changes are promoted only after offline validation | `appendix/PRODUCTION_READINESS_SCORECARD.md`, `evidence/production_readiness_summary.json` |

## Why This Wins

- It turns agentic AI into an auditable workflow, not an uncontrolled scraper.
- It answers the competition's practical concern: a lean team can run this because each agent has a small contract and clear failure mode.
- It protects HealthLynked from the highest-risk mistakes: identity merges, stale source overreach, and silent high-risk updates.
- It keeps cost low by using deterministic extraction and official/public sources first, with LLM fallback only when a page is approved but messy.
