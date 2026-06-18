# Bonus Coverage Matrix

## Purpose

This page maps the competition bonus-point list to concrete artifacts in the curated package. It is intentionally short so a judge can confirm coverage quickly.

## Bonus Evidence

| Bonus Item | Coverage | Primary Evidence |
|---|---|---|
| Working prototype | Included | `prototype/WORKING_PROTOTYPE.md`, `scripts/run_best_pipeline.py`, `prototype/metrics.json` |
| Agent workflow diagram | Included | `proposal/ARCHITECTURE_DIAGRAM.md`, `proposal/ARCHITECTURE_DIAGRAM.mmd`, `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md` |
| Cost estimate per 1,000 records | Included | `appendix/COST_MODEL.md`, `evidence/cost_model_per_1000.csv` |
| Confidence scoring formula | Included | `proposal/CONFIDENCE_AND_DECISION_POLICY.md` |
| Sample human review dashboard | Included | `dashboard/index.html`, `appendix/DASHBOARD_SPEC.md` |
| Duplicate detection logic | Included | `appendix/DUPLICATE_MOVEMENT_DETECTION.md`, `evidence/duplicate_candidates.csv` |
| Address normalization strategy | Included | `src/data.py`, `proposal/CONFIDENCE_AND_DECISION_POLICY.md` |
| NPI validation | Included | `proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md`, `proposal/SOURCE_CONNECTOR_STATUS_MATRIX.md`, `proposal/OFFICIAL_SOURCE_REFERENCES.md` |
| Practice-location matching | Included | `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md`, `appendix/DUPLICATE_MOVEMENT_DETECTION.md` |
| Provider movement detection | Included | `appendix/DUPLICATE_MOVEMENT_DETECTION.md`, `evidence/provider_movement_candidates.csv` |
| Inactive/retired provider detection | Included | `appendix/INACTIVE_PROVIDER_DETECTION.md`, `evidence/inactive_provider_candidates.csv` |
| Change history and audit log | Included | `evidence/audit_events.jsonl`, `appendix/AUDIT_ROLLBACK_WORKFLOW.md` |
| Safe auto-update rules | Included | `proposal/CONFIDENCE_AND_DECISION_POLICY.md`, `prototype/auto_apply_updates.csv` |
| Clear implementation roadmap | Included | `proposal/IMPLEMENTATION_ROADMAP_90_DAYS.md`, `proposal/IMPLEMENTATION_ACCEPTANCE_CRITERIA.md` |

## Judge Takeaway

The submission does not treat bonus items as appendix decoration. Each bonus capability is connected to a runnable artifact, policy document, evidence file, or implementation gate.
