# Judge Comparison Matrix

## Purpose

This page gives judges a fast way to compare the submission against likely alternatives. The strongest entry should not merely sound advanced; it should reduce implementation risk, manual labor, source risk, cost, and post-award uncertainty.

## Competitive Comparison

| Submission Pattern | What It Usually Shows | Hidden Weakness | Why This Submission Is Stronger |
|---|---|---|---|
| Proposal-only architecture | Nice diagram and roadmap | No proof that matching, confidence, review routing, or audit records work end to end | Includes a runnable MVP, metrics, recommendation contract, dashboard, audit events, and self-contained smoke test |
| Notebook-only prototype | Code and sample outputs | Hard to see how it scales, handles source terms, or becomes production operations | Adds AWS architecture, source access policy, connector health model, lean-team operating model, failure playbook, shadow-mode pilot protocol, and 90-day acceptance gates |
| Broad scraper | Large amount of extracted data | Weak source authority, brittle parsers, high legal/robots risk, poor explainability | Uses field-level source law, polite crawling, cached official sources, conflict routing, and no weak-source auto-update |
| LLM-only agent demo | Impressive narrative and flexible extraction | Hallucination risk, cost uncertainty, poor determinism, weak auditability | Uses deterministic parsing first; LLM extraction is schema-bound, source-grounded, corroborated, and gated by cost/quality |
| Manual cleanup workflow | Human judgment and local accuracy | Expensive, slow, not repeatable, no continuous refresh | Prioritizes risky records, auto-applies only safe high-confidence changes, and reserves reviewers for ambiguous cases |
| Black-box enrichment vendor | Quick data enrichment | Opaque source lineage, recurring cost, hard-to-tune update policy | Produces transparent evidence, source weights, confidence reasons, audit trail, rollback plan, and source-ablation cost controls |

## Winning Edge By Criterion

| Criterion | What A Judge Can Inspect |
|---|---|
| Accuracy | `prototype/metrics.json`, `prototype/candidate_updates.csv`, confidence policy |
| Scalability | `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md`, `appendix/AWS_PRODUCTION_ARCHITECTURE.md`, synthetic benchmark |
| Cost Efficiency | `appendix/COST_MODEL.md`, `evidence/cost_model_per_1000.csv`, source-ablation logic |
| Practicality | `proposal/LEAN_TEAM_OPERATING_MODEL.md`, `proposal/IMPLEMENTATION_ACCEPTANCE_CRITERIA.md`, `proposal/SHADOW_MODE_PILOT_PROTOCOL.md` |
| Explainability | `prototype/RECOMMENDATION_API_CONTRACT.md`, `evidence/audit_events.jsonl` |
| Data Quality | normalization code in `src/data.py`, duplicate/movement/inactive appendices |
| Source Reliability | `proposal/SOURCE_ACCESS_COMPLIANCE_POLICY.md`, source connector matrix |
| Human Review Design | `dashboard/index.html`, review queue outputs, disposition loop |
| Audit Trail | audit events, rollback plan, recommendation examples |

## The Short Version

The submission wins because it is not one artifact. It is a complete operating system for directory quality: prototype, policy, production architecture, review workflow, source governance, cost controls, no-write pilot gates, and acceptance criteria that can survive the first consulting month.
