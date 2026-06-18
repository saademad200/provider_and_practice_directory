# Agent Cards And Workflow Contracts

This experiment applies the local agentic-engineering whitepaper lessons to the provider-directory pipeline. The production solution is framed as a bounded multi-agent harness, not one monolithic agent prompt.

## Current Pipeline Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Agent cards emitted: 8

## Orchestrator Contract

- Name: `provider_directory_orchestrator`
- Style: bounded multi-agent workflow
- State store: Aurora PostgreSQL for workflow state, S3 for immutable evidence/audit bundles
- Message bus: Amazon SQS for review and connector work queues

## Global Invariants

- No gold labels or reviewer dispositions are available during candidate generation.
- No identity-level delete or inactive-provider update is auto-applied.
- Every source-derived value preserves source URL, retrieved timestamp, parser version, and evidence hash.
- Every applied update has an audit event and rollback command.
- LLM fallback outputs are review-routed unless corroborated by stronger deterministic sources.

## Agent Cards

| Agent | Purpose | Tools | Handoff |
|---|---|---|---|
| source_retrieval_agent | Fetch public evidence snapshots from approved provider-directory sources. | nppes_connector, state_license_connector, practice_website_fetcher, cms_provider_data_connector | evidence_normalization_agent |
| evidence_normalization_agent | Normalize phone, address, specialty, license, NPI status, and patient-acceptance evidence. | deterministic_parser, specialty_alias_table, address_normalizer, bedrock_fallback_contract | identity_resolution_agent, source_conflict_agent |
| identity_resolution_agent | Resolve providers, practices, locations, affiliations, duplicates, and movement candidates. | npi_matcher, address_matcher, practice_change_detector, duplicate_detector | evidence_scoring_agent |
| source_conflict_agent | Adjudicate competing source values using field-specific source authority. | source_conflict_diagnostics, field_authority_policy | evidence_scoring_agent, human_review_agent |
| evidence_scoring_agent | Score candidate updates for confidence, cost, freshness, source reliability, and auto-apply eligibility. | confidence_scorer, freshness_sla_checker, cost_model, review_priority_model | human_review_agent, audit_rollback_agent |
| human_review_agent | Prepare reviewer worklists and capture accept, reject, edit, defer, recrawl, and rollback decisions. | dashboard, review_priority_queue, case_study_generator | active_learning_agent, audit_rollback_agent |
| audit_rollback_agent | Emit immutable audit events, provider timelines, and rollback commands for applied updates. | audit_event_writer, rollback_plan_generator, s3_archive_writer | monitoring_agent |
| monitoring_agent | Watch connector freshness, false positives, review backlog, cost drift, and audit completeness. | monitoring_alert_rules, source_freshness_sla, cost_per_1000_model | source_retrieval_agent, human_review_agent |

## Why This Helps The Submission

The judge can inspect a realistic division of labor: retrieval, normalization, identity resolution, conflict adjudication, scoring, review, audit/rollback, and monitoring. This turns the proposal from a clever script into a governed AI operations system with clear tool permissions and handoff boundaries.
