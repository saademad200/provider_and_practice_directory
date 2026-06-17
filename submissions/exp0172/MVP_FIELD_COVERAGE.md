# Option C Hybrid MVP Field Coverage

## Submission Choice

This package is explicitly an **Option C: Hybrid Submission**. It includes a runnable prototype and a production architecture/operating model. The prototype proves candidate generation, confidence scoring, safe auto-apply, review routing, audit-style outputs, and verifier-backed reproducibility. The architecture extends that prototype into an AWS-oriented pipeline for scheduled evidence refresh, source governance, review operations, rollback, monitoring, and cost control.

## Current Verified Prototype Metrics

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Auto-apply count: 20
- Review count: 38
- Cost per correct update: $0.005836

## Why Hybrid Is The Right Fit

The competition has no official train/test data in the downloadable archive, so a pure notebook would be fragile and a pure architecture deck would be too hand-wavy. The hybrid package makes the core loop executable while giving judges the production controls they asked for: reliable public/legal sources, normalization, confidence, safe automation, human review, audit trail, duplicate/movement detection, inactive detection, cost model, and AWS deployment path.

## MVP And Requirement Coverage

| Field Or Requirement | Status | Prototype Evidence | Production Evidence | Decision Policy |
|---|---|---|---|---|
| Hybrid architecture plus working prototype | implemented | scripts/run_best_pipeline.py; candidate_updates.csv; auto_apply_updates.csv; review_queue.csv; verification.json | ARCHITECTURE.md; AWS_PRODUCTION_ARCHITECTURE.md; AGENT_WORKFLOW_DIAGRAM.md; PRODUCTION_READINESS_SCORECARD.md | Working prototype proposes updates; production plan covers orchestration, audit, rollback, monitoring, and human review. |
| provider name | implemented as identity/display anchor; review-gated for updates | providers.provider_name; normalization and identity matching docs; case studies | DUPLICATE_MOVEMENT_DETECTION.md; PRACTICE_AFFILIATION_REBRAND.md; SOURCE_CONFLICT_ADJUDICATION.md | Name changes are identity-risking and should route to review unless backed by authoritative NPI/state-board evidence. |
| NPI | implemented as stable identity anchor | providers.npi; nppes_api_evidence.csv; nppes_parsed_evidence.json | NPPES_API_SMOKE.md; SOURCE_CONNECTOR_REGISTRY.md; SOURCE_GOVERNANCE_CHECKLIST.md | NPI is not auto-mutated; it anchors evidence joins, duplicate checks, and suspicious identity review. |
| specialty | implemented | evidence.field=specialty; candidate_updates.csv; SPECIALTY_NORMALIZATION.md; specialty_normalization_fixture.csv | SOURCE_CONNECTOR_REGISTRY.md; JUDGE_RUBRIC_SELF_EVAL.md | Requires field-specific confidence and multi-source support before auto-apply. |
| practice name | partially implemented; production-ready design | providers.practice_id; practice_change_candidates.csv; source_conflict_adjudication.csv | PRACTICE_AFFILIATION_REBRAND.md; DUPLICATE_MOVEMENT_DETECTION.md | Practice-name changes are reviewed with rebrand, merge, and location-move context before update. |
| address | implemented | evidence.field=address; candidate_updates.csv; auto_apply_updates.csv; review_queue.csv | FIELD_RISK_POLICY.md; FRESH_BUSINESS_LISTING_FALLBACK.md; DUPLICATE_MOVEMENT_DETECTION.md | Address updates need strong confidence, freshness, and practice-peer safety checks for auto-apply. |
| phone | implemented | evidence.field=phone; candidate_updates.csv; auto_apply_updates.csv; review_queue.csv | FIELD_RISK_POLICY.md; FRESH_BUSINESS_LISTING_FALLBACK.md; SOURCE_PERTURBATION_STRESS_TESTS.md | Phone updates require field-specific thresholds, source-count gates, and practice-peer checks. |
| website | implemented as evidence/source surface; production update design | evidence.url; web_extraction_benchmark.json; source_connector_registry.csv | EXTERNAL_SOURCE_STRATEGY.md; LLM_FALLBACK_CONTRACT.md; SOURCE_CONNECTOR_REGISTRY.md | Website evidence can support field updates; website URL changes should route to review unless domain ownership is clear. |
| active/inactive | implemented through license_status and inactive detection | evidence.field=license_status; inactive_provider_candidates.csv; candidate_updates.csv | INACTIVE_PROVIDER_DETECTION.md; SOURCE_CONFLICT_ADJUDICATION.md; AUDIT_ROLLBACK_WORKFLOW.md | Inactive signals can be auto-applied only when authoritative and low-conflict; otherwise review. |
| duplicate detection | implemented as candidate diagnostic | duplicate_candidates.csv | DUPLICATE_MOVEMENT_DETECTION.md; PROVIDER_DIRECTORY_SKILLS_LIBRARY.md | Duplicates are review-routed because merges are irreversible/high-risk. |
| practice-location movement detection | implemented as candidate diagnostic | provider_movement_candidates.csv; practice_change_candidates.csv | DUPLICATE_MOVEMENT_DETECTION.md; PRACTICE_AFFILIATION_REBRAND.md | Movement is review-routed unless the old and new location evidence is fresh, consistent, and authoritative. |
| confidence, audit, human review | implemented | confidence column; review_queue.csv; audit_events.jsonl; rollback_plan.csv | REVIEW_DISPOSITION_AND_SLA.md; AUDIT_ROLLBACK_WORKFLOW.md; THRESHOLD_ROBUSTNESS_SWEEP.md | High confidence can auto-apply only under stricter field-specific thresholds; uncertain/conflicting changes route to review. |

## Intentional Guardrails

- Identity-risk fields such as provider name, NPI, practice name, duplicate merge, and movement are treated as review-first rather than blindly auto-updated.
- Official practice websites, NPPES, state boards, and health-system pages outrank generic business listings.
- Business-listing evidence is intentionally field-gated to phone/address and age-gated to 60 days.
- Website pages can be evidence; website URL mutation requires ownership/canonicalization checks before any production auto-update.
- AWS is the target cloud for orchestration, evidence storage, optional Bedrock extraction, monitoring, and review workflow integration.
