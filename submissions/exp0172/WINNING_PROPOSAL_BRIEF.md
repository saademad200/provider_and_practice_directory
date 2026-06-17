# Winning Proposal Brief

HealthLynked needs a repeatable provider-directory quality operating system, not a one-time cleanup.

This submission provides:

- a working MVP;
- an AWS production architecture;
- confidence scoring;
- source governance;
- human review routing;
- audit and rollback;
- duplicate, movement, inactive-provider, and practice-change diagnostics;
- a whitepaper-informed agentic harness with scoped agents, skills, evals, and approval gates.

## Why It Wins

| Criterion | Answer |
|---|---|
| Accuracy | F1 `0.948276`; auto-apply precision `1.0` |
| Scalability | AWS Step Functions, Lambda/ECS, S3, RDS/DynamoDB, CloudWatch |
| Cost Efficiency | deterministic public sources first, gated Bedrock fallback only when useful |
| Practicality | lean-team MVP to production roadmap |
| Explainability | old value, new value, confidence, sources, URLs, decision reason |
| Data Quality | normalization and field-risk logic across MVP fields |
| Source Reliability | authority tiers, conflict diagnostics, weak-source gates |
| Human Review | only uncertain, conflicting, identity-sensitive, or high-risk cases |
| Audit Trail | audit events, evidence hashes, rollback plan, timeline |

## Best Judge Path

1. `Provider_Directory_Update_Pipeline_End_to_End.ipynb`
2. `TECHNICAL_ARCHITECTURE_PROPOSAL.md`
3. `ARCHITECTURE_DIAGRAM.md`
4. `WORKING_PROTOTYPE.md`
5. `candidate_updates.csv`
6. `auto_apply_updates.csv`
7. `review_queue.csv`
8. `audit_events.jsonl`
