# Winning Proposal Brief

## Core Thesis

HealthLynked does not need a one-time provider-directory cleanup. It needs a repeatable, governed directory-quality operating system.

This submission delivers that operating system in miniature:

- a working MVP that proposes, scores, routes, and audits provider/practice updates;
- an AWS production architecture for scaling the same loop to thousands or millions of records;
- a human-review design that keeps reviewers focused on genuinely uncertain or high-risk cases;
- a source-governance model that trusts NPPES, state boards, practice websites, health systems, and fallback sources differently;
- a whitepaper-informed agentic harness made of scoped agents, skills, evals, contracts, and audit controls.

## Why This Should Win

Most submissions can describe a pipeline. This one proves the operating loop and shows how to run it safely.

| Judge Concern | Winning Answer |
|---|---|
| Accuracy | The MVP reaches F1 `0.948276` while keeping auto-apply precision at `1.0`. |
| Scalability | AWS Step Functions, Lambda/ECS, S3, RDS/DynamoDB, CloudWatch, and Bedrock fallback are mapped to concrete workflow stages. |
| Cost Efficiency | The system spends first on deterministic public sources, then review, and only rarely gated LLM extraction. |
| Practicality | A lean team can ship the MVP path first, then add source hardening, review operations, and AWS scheduling. |
| Explainability | Every candidate includes old value, proposed value, confidence, source set, URL, decision, and review reason. |
| Data Quality | Normalization covers phone, address, specialty, status, source freshness, and matching keys, with production coverage for names/practices/websites/affiliations. |
| Source Reliability | Sources are authority-tiered by field, with conflict diagnostics and weak-source gates. |
| Human Review Design | The queue is intentionally narrow: low-confidence, conflicting, high-risk, or identity-sensitive cases. |
| Audit Trail | Audit events, rollback plans, evidence hashes, package manifest, and timelines are included. |

## Differentiator

The differentiator is not a clever prompt. It is the harness:

```text
approved sources
  -> normalized evidence
  -> identity matching
  -> field-risk policy
  -> confidence scoring
  -> safe auto-update or human review
  -> audit/rollback
  -> feedback into source and threshold policy
```

That harness is what HealthLynked can actually operate after the competition.

## Judge Demo Path

1. Open `notebooks/Provider_Directory_Update_Pipeline_End_to_End.ipynb`.
2. Skim the rendered metric cards and decision funnel.
3. Open `submissions/healthlynked_option_c_clean/proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md`.
4. Open `submissions/healthlynked_option_c_clean/proposal/ARCHITECTURE_DIAGRAM.md`.
5. Open `submissions/healthlynked_option_c_clean/prototype/WORKING_PROTOTYPE.md`.
6. Inspect `candidate_updates.csv`, `auto_apply_updates.csv`, `review_queue.csv`, and `audit_events.jsonl`.

## Closing Argument

The safest provider-directory automation is not automation everywhere. It is evidence-backed automation where confidence is high, human review where risk is real, and auditability everywhere.
