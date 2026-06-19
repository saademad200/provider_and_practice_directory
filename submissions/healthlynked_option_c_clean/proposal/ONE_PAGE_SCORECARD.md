# One-Page Judge Scorecard

This package is designed to win as an Option C hybrid: a runnable prototype plus a production architecture that a lean HealthLynked team can implement on AWS after the award.

## Competition Criteria

| Criterion | What the submission proves | Primary evidence |
| --- | --- | --- |
| Accuracy | Field-level recommendations reach F1 `0.948276`; safe auto-apply precision is `1.0`; unsafe identity-sensitive changes route to review. | `prototype/metrics.json`, `evidence/verification.json`, `proposal/CONFIDENCE_AND_DECISION_POLICY.md` |
| Scalability | The production plan separates cheap deterministic source checks from bounded LLM fallback and scales with AWS Step Functions, S3, ECS/Lambda, queues, and RDS/DynamoDB. | `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md`, `appendix/AWS_PRODUCTION_ARCHITECTURE.md` |
| Cost Efficiency | The prototype estimates `$0.005836` evidence-only cost per correct update and includes per-1,000-record scenarios with AWS, LLM, and manual-review labor. | `appendix/COST_MODEL.md`, `evidence/cost_model_per_1000.csv` |
| Practicality | The roadmap defines 30/60/90 day delivery, lean-team roles, no-write pilot gates, rollback, and source connector operations. | `proposal/IMPLEMENTATION_ROADMAP_90_DAYS.md`, `proposal/LEAN_TEAM_OPERATING_MODEL.md`, `proposal/IMPLEMENTATION_ACCEPTANCE_CRITERIA.md`, `proposal/SHADOW_MODE_PILOT_PROTOCOL.md` |
| Explainability | Every recommendation includes changed field, old/new value, confidence, source support, disagreement reason, and recommended action. | `prototype/RECOMMENDATION_API_CONTRACT.md`, `prototype/recommendation_api_examples.json` |
| Data Quality | The MVP normalizes provider names, specialties, phones, addresses, websites, practice names, status, NPIs, and affiliations. | `src/`, `prototype/WORKING_PROTOTYPE.md`, `appendix/DUPLICATE_MOVEMENT_DETECTION.md` |
| Source Reliability | Sources are authority-tiered; official sources dominate, stale/conflicting sources are penalized, and legally accessible connectors are governed. | `proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md`, `proposal/SOURCE_ACCESS_COMPLIANCE_POLICY.md`, `proposal/OFFICIAL_SOURCE_REFERENCES.md` |
| Human Review Design | Review is reserved for conflicting, high-risk, identity-sensitive, or low-confidence updates; the dashboard includes accept/reject/recrawl actions. | `dashboard/index.html`, `appendix/DASHBOARD_SPEC.md`, `prototype/review_queue.csv` |
| Audit Trail | Candidate updates, auto-apply decisions, human-review rows, rollback records, and audit JSONL events are packaged and reproducible. | `evidence/audit_events.jsonl`, `evidence/rollback_plan.csv`, `appendix/AUDIT_ROLLBACK_WORKFLOW.md` |

## Bonus Coverage

| Bonus item | Included evidence |
| --- | --- |
| Working prototype | `scripts/run_best_pipeline.py`, `prototype/WORKING_PROTOTYPE.md`, `prototype/metrics.json` |
| Agent workflow diagram | `proposal/AGENT_WORKFLOW_DIAGRAM.md`, `proposal/AGENT_WORKFLOW_DIAGRAM.mmd` |
| Cost estimate per 1,000 records | `appendix/COST_MODEL.md`, `evidence/cost_model_per_1000.csv` |
| Confidence scoring formula | `proposal/CONFIDENCE_AND_DECISION_POLICY.md` |
| Sample human review dashboard | `dashboard/index.html` |
| Duplicate detection logic | `appendix/DUPLICATE_MOVEMENT_DETECTION.md`, `evidence/duplicate_candidates.csv` |
| Address normalization strategy | `prototype/WORKING_PROTOTYPE.md`, `src/data.py` |
| NPI validation | `src/npi.py`, `data/sample/providers.csv`, `evidence/verification.json` |
| Practice-location matching | `appendix/DUPLICATE_MOVEMENT_DETECTION.md`, `evidence/provider_movement_candidates.csv` |
| Provider movement detection | `appendix/DUPLICATE_MOVEMENT_DETECTION.md`, `evidence/provider_movement_candidates.csv` |
| Inactive/retired provider detection | `appendix/INACTIVE_PROVIDER_DETECTION.md`, `evidence/inactive_provider_candidates.csv` |
| Change history and audit log | `evidence/audit_events.jsonl`, `appendix/AUDIT_ROLLBACK_WORKFLOW.md` |
| Safe auto-update rules | `proposal/CONFIDENCE_AND_DECISION_POLICY.md`, `prototype/auto_apply_updates.csv` |
| Clear implementation roadmap | `proposal/IMPLEMENTATION_ROADMAP_90_DAYS.md`, `proposal/IMPLEMENTATION_ACCEPTANCE_CRITERIA.md`, `proposal/SHADOW_MODE_PILOT_PROTOCOL.md` |

## The Judge Decision In One Sentence

Choose this submission because it does not merely describe AI agents; it packages a verified control plane for directory quality: deterministic evidence first, bounded agents where useful, source reliability law, conservative auto-update rules, human review only where it matters, and a clean AWS path from MVP to production.
