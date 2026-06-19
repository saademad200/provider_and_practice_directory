# Combined A/B/C Pipeline Coverage

## Claim

This submission intentionally combines all three allowed submission modes:

- **Option A:** Technical Architecture Proposal.
- **Option B:** Working Prototype.
- **Option C:** Hybrid Submission.

The package should be judged as a runnable MVP plus a production-scale architecture and operating model.

## Current Verified Metrics

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Auto-apply count: 3
- Review count: 55
- Prototype evidence-only cost per correct update: $0.005836

## Submission Mode Coverage

| Submission Mode | Status | Evidence |
|---|---|---|
| Option A: Technical Architecture Proposal | included | ARCHITECTURE.md; AWS_PRODUCTION_ARCHITECTURE.md; SOURCE_CONNECTOR_REGISTRY.md; CAPABILITY_PROFILES_AND_ORCHESTRATION.md; AGENT_WORKFLOW_DIAGRAM.md |
| Option B: Working Prototype | included | scripts/run_best_pipeline.py; candidate_updates.csv; auto_apply_updates.csv; review_queue.csv; metrics.json; verification.json |
| Option C: Hybrid Submission | included | MVP_FIELD_COVERAGE.md; COMPETITION_ALIGNMENT_REFRESH.md; PUBLIC_DATASET_PROFILE.md; PUBLIC_DATASET_TRIAGE_CLI.md; PRODUCTION_READINESS_SCORECARD.md |

## Desired Pipeline Trace

| Desired Pipeline Step | Prototype Implementation | Production Implementation | Artifacts |
|---|---|---|---|
| HealthLynked Provider / Practice Database | providers.csv-style fixture loaded by src.data.load_dataset() | RDS/DynamoDB operational store plus S3 snapshots and immutable evidence history | BENCHMARK_DATASHEET.md; AWS_PRODUCTION_ARCHITECTURE.md; data_minimization_schema.json |
| Find Outdated or Risky Records | Candidate generation flags field deltas, stale evidence, peer mismatches, inactive/license status, and review priority. | Scheduled risk scan driven by last_verified_date, source freshness, license expiry, public source drift, reviewer feedback, and monitoring alerts. | candidate_updates.csv; review_queue.csv; freshness_summary.csv; monitoring_alerts.json; PUBLIC_DATASET_PROFILE.md |
| Search Trusted Sources: NPI, CMS, state boards, practice websites | Evidence fixture and connector outputs model NPPES, state_license, practice_website, health_system, and guarded business_listing evidence. | Source Connector Registry with authority tiers, freshness SLAs, terms/governance checks, and optional Bedrock fallback only for messy official pages. | SOURCE_CONNECTOR_REGISTRY.md; nppes_api_evidence.csv; SOURCE_GOVERNANCE_CHECKLIST.md; LLM_FALLBACK_CONTRACT.md |
| Collect Updated Provider / Practice Data | Evidence rows keep provider_id, practice_id, source, field, proposed value, age, and URL. | Connector agents write raw evidence snapshots to S3 and normalized evidence rows to the operational evidence store. | candidate_updates.csv; evidence_tool_manifest.json; source_connector_registry.csv |
| Clean and Normalize Data | Normalizes phone, address, specialty, license status, accepting-new-patients, source freshness, and comparison keys. | Dedicated normalization lane for provider names, practice names, addresses, phones, specialties, affiliations, and source-specific field mappings. | SPECIALTY_NORMALIZATION.md; FIELD_RISK_POLICY.md; MVP_FIELD_COVERAGE.md; public_dataset_missingness.csv |
| Match Provider / Practice Records | Stable provider/practice IDs, NPI identity anchors, practice-peer checks, duplicate candidates, movement candidates, and practice-change candidates. | Identity-resolution agent combines NPI, names, addresses, phones, specialty, practice affiliation, and historical movement signals. | DUPLICATE_MOVEMENT_DETECTION.md; practice_change_candidates.csv; provider_movement_candidates.csv; NPPES_API_SMOKE.md |
| Assign Confidence Score | Weighted source agreement, recency decay, field thresholds, source-count gates, and freshness/peer review reasons. | Versioned scoring formula calibrated by source authority, field risk, source agreement, freshness, reviewer outcomes, and missing-source robustness. | candidate_updates.csv; THRESHOLD_ROBUSTNESS_SWEEP.md; source_perturbation_stress_tests.csv; calibration.csv |
| Decision: No Change / Auto Update / Human Review | No-change records emit no candidate; high-confidence low-risk updates go to auto_apply_updates.csv; uncertain/conflicting changes go to review_queue.csv. | Decision router applies safe auto-update rules, review-first identity policy, conflict rules, and reviewer disposition feedback. | auto_apply_updates.csv; review_queue.csv; REVIEW_DISPOSITION_AND_SLA.md; SOURCE_CONFLICT_ADJUDICATION.md |
| Save Audit Log + Update Provider Directory | Audit event fixture, provider change timeline, rollback plan, package integrity manifest, and before/after candidate rows. | Append-only audit events, evidence hashes, approval history, rollback workflow, and monitor/relearn loop after applied updates. | audit_events.jsonl; provider_change_timeline.csv; rollback_plan.csv; AUDIT_ROLLBACK_WORKFLOW.md; PACKAGE_INTEGRITY_MANIFEST.md |

## Required System Capabilities

| Required Capability | Status | Primary Artifacts |
|---|---|---|
| Identify outdated records | implemented | freshness_summary.csv; review_queue.csv; PUBLIC_DATASET_PROFILE.md |
| Search reliable public/legal sources | implemented plus production connectors | SOURCE_CONNECTOR_REGISTRY.md; SOURCE_GOVERNANCE_CHECKLIST.md |
| Compare HealthLynked data against external sources | implemented | candidate_updates.csv; source_conflict_adjudication.csv |
| Normalize names, practices, addresses, phones, specialties, affiliations | implemented/prototype plus production design | MVP_FIELD_COVERAGE.md; SPECIALTY_NORMALIZATION.md; FIELD_RISK_POLICY.md |
| Detect duplicates, inactive providers, moved providers, practice changes | implemented diagnostics and review queues | duplicate_candidates.csv; inactive_provider_candidates.csv; provider_movement_candidates.csv; practice_change_candidates.csv |
| Assign confidence to each proposed update | implemented | candidate_updates.csv; THRESHOLD_ROBUSTNESS_SWEEP.md |
| Automatically approve high-confidence updates | implemented | auto_apply_updates.csv; FIELD_RISK_POLICY.md |
| Send uncertain/conflicting records to human review | implemented | review_queue.csv; REVIEW_DISPOSITION_AND_SLA.md |
| Maintain audit trail of what/why/sources | implemented | audit_events.jsonl; provider_change_timeline.csv; PACKAGE_INTEGRITY_MANIFEST.md |
| Keep cost low | implemented and modeled | COST_MODEL.md; cost_model_per_1000.csv; LLM_FALLBACK_CONTRACT.md |
| Run continuously or periodically | production design | AWS_PRODUCTION_ARCHITECTURE.md; CAPABILITY_PROFILES_AND_ORCHESTRATION.md; MONITORING_ALERTS.md |

## Evaluation Criteria Coverage

| Criterion | Answer | Evidence |
|---|---|---|
| Accuracy | F1 0.948276, precision 0.948276, recall 0.948276, auto-apply precision 1.0 | metrics.json; cv_metrics.json; residual_false_positives.csv; residual_false_negatives.csv |
| Scalability | AWS batch/Step Functions plan and 100x synthetic throughput benchmark | SYNTHETIC_VOLUME_BENCHMARK.md; aws_step_functions_throughput_plan.csv |
| Cost Efficiency | Low-cost deterministic sources first; optional LLM fallback only when gated | COST_MODEL.md; LLM_FALLBACK_CONTRACT.md; source_ablation.csv |
| Practicality | Lean-team implementation with runnable CLI, docs, dashboard, review contracts, and package verifier | REPRODUCIBILITY.md; KAGGLE_SUBMISSION_HANDOFF.md; verification.json |
| Explainability | Every update includes old/new values, confidence, sources, URLs, freshness, review reason | candidate_updates.csv; REVIEW_QUEUE_PRIORITIZATION.md |
| Data Quality | Normalization and identity matching across names, addresses, phones, specialties, practices, status | SPECIALTY_NORMALIZATION.md; MVP_FIELD_COVERAGE.md |
| Source Reliability | Authority-tiered source registry, conflict adjudication, perturbation tests | SOURCE_CONNECTOR_REGISTRY.md; SOURCE_CONFLICT_ADJUDICATION.md |
| Human Review Design | Only ambiguous/high-risk/conflicting/identity-sensitive updates route to review | review_queue.csv; REVIEW_DISPOSITION_AND_SLA.md |
| Audit Trail | Append-only events, change timeline, rollback plan, manifest, no-secrets scan | audit_events.jsonl; provider_change_timeline.csv; rollback_plan.csv |

## Bonus Point Coverage

| Bonus Item | Status | Evidence |
|---|---|---|
| Working prototype | included | scripts/run_best_pipeline.py; candidate_updates.csv; verification.json |
| Agent workflow diagram | included | AGENT_WORKFLOW_DIAGRAM.md; agent_workflow_diagram.mmd |
| Cost estimate per 1,000 provider records | included | COST_MODEL.md; cost_model_per_1000.csv |
| Confidence scoring formula | included | candidate_updates.csv; THRESHOLD_ROBUSTNESS_SWEEP.md; FIELD_RISK_POLICY.md |
| Sample human review dashboard | included | dashboard/index.html |
| Duplicate detection logic | included | DUPLICATE_MOVEMENT_DETECTION.md; duplicate_candidates.csv |
| Address normalization strategy | included | FIELD_RISK_POLICY.md; BENCHMARK_DATASHEET.md |
| NPI validation | included | NPPES_API_SMOKE.md; public_dataset_issue_counts.csv |
| Practice-location matching | included | DUPLICATE_MOVEMENT_DETECTION.md; provider_movement_candidates.csv |
| Provider movement detection | included | provider_movement_candidates.csv; PRACTICE_AFFILIATION_REBRAND.md |
| Inactive/retired provider detection | included | INACTIVE_PROVIDER_DETECTION.md; inactive_provider_candidates.csv |
| Change history and audit log | included | provider_change_timeline.csv; audit_events.jsonl |
| Safe auto-update rules | included | FIELD_RISK_POLICY.md; auto_apply_updates.csv |
| Clear implementation roadmap | included | PRODUCTION_READINESS_SCORECARD.md; AWS_PRODUCTION_ARCHITECTURE.md |

## Suggested MVP Field Coverage

| MVP Field | Coverage | Evidence |
|---|---|---|
| Provider name | Identity/display anchor; review-first for mutation | MVP_FIELD_COVERAGE.md; DUPLICATE_MOVEMENT_DETECTION.md |
| NPI | Stable identity anchor and validation signal | NPPES_API_SMOKE.md; public_dataset_issue_counts.csv |
| Specialty | Prototype update field with normalization | SPECIALTY_NORMALIZATION.md; candidate_updates.csv |
| Practice name | Production design plus practice-change diagnostics | PRACTICE_AFFILIATION_REBRAND.md; practice_change_candidates.csv |
| Address | Prototype update field with normalization and guarded source policy | candidate_updates.csv; FIELD_RISK_POLICY.md |
| Phone number | Prototype update field with normalization and peer checks | candidate_updates.csv; FRESH_BUSINESS_LISTING_FALLBACK.md |
| Website | Evidence/source surface plus production update design | SOURCE_CONNECTOR_REGISTRY.md; PUBLIC_DATASET_PROFILE.md |
| Active/inactive status | License/status update field plus inactive detection | INACTIVE_PROVIDER_DETECTION.md; inactive_provider_candidates.csv |

## Continuous Pipeline Positioning

This is not framed as one-time manual cleanup. The production design uses scheduled refreshes, source health checks, event/audit logs, reviewer feedback, monitoring alerts, and threshold/source-policy updates so the pipeline can run continuously or periodically with bounded cost and review load.
