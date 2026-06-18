# Artifact Index

| Artifact | Category | Purpose | Size Bytes |
|---|---|---|---:|
| KAGGLE_SUBMISSION_HANDOFF.md | start_here | Concise upload instructions, suggested title/description, and pre-upload verification command. | 1424 |
| README.md | start_here | Package entrypoint and recommended reading order. | 617 |
| COMBINED_ABC_PIPELINE_COVERAGE.md | judge_narrative | Combined Option A/B/C coverage map for desired pipeline, required capabilities, evaluation criteria, bonus points, and MVP fields. | 11197 |
| COMPETITION_ALIGNMENT_REFRESH.md | judge_narrative | Live competition-surface refresh, evaluation-criteria map, and public-notebook gap analysis. | 5143 |
| EXECUTIVE_SUMMARY.md | judge_narrative | High-level positioning, metrics, and rubric mapping. | 1491 |
| JUDGE_RUBRIC_SELF_EVAL.md | judge_narrative | Artifact-backed self-evaluation against qualitative competition judging criteria. | 1422 |
| MVP_FIELD_COVERAGE.md | judge_narrative | Option C hybrid submission map from MVP fields and bonus capabilities to prototype and production artifacts. | 6004 |
| ONE_PAGE_JUDGE_GUIDE.md | judge_narrative | Concise package walkthrough for judges: what to open, what it proves, and expected metrics. | 1585 |
| combined_abc_bonus.csv | judge_narrative | Machine-readable coverage map for bonus-point items. | 1344 |
| combined_abc_capabilities.csv | judge_narrative | Machine-readable coverage map for required system capabilities. | 1552 |
| combined_abc_evaluation.csv | judge_narrative | Machine-readable coverage map for evaluation criteria. | 1494 |
| combined_abc_mvp.csv | judge_narrative | Machine-readable coverage map for suggested MVP fields. | 987 |
| combined_abc_options.csv | judge_narrative | Machine-readable map showing Option A, Option B, and Option C are all included. | 1042 |
| combined_abc_pipeline.csv | judge_narrative | Machine-readable trace of the requested pipeline architecture to prototype and production artifacts. | 3670 |
| competition_alignment_matrix.csv | judge_narrative | Machine-readable map from competition criteria to package artifacts. | 3472 |
| judge_rubric_self_eval.csv | judge_narrative | Criterion-level rubric scores, weights, evidence links, and metric checks. | 2891 |
| judge_rubric_self_eval_summary.json | judge_narrative | Machine-readable summary of package rubric self-evaluation. | 238 |
| mvp_field_coverage.csv | judge_narrative | Machine-readable Option C hybrid MVP field and requirement coverage map. | 6400 |
| public_notebook_gap_analysis.csv | judge_narrative | Machine-readable comparison against the observed public Kaggle notebook. | 969 |
| public_notebook_summary.json | judge_narrative | Metadata and keyword summary for the observed public Kaggle notebook. | 717 |
| AGENT_WORKFLOW_DIAGRAM.md | workflow | Agentic workflow diagram with source-to-review-to-audit handoffs. | 3701 |
| agent_workflow_diagram.mmd | workflow | Mermaid source for the workflow diagram. | 1033 |
| PRODUCTION_READINESS_SCORECARD.md | readiness | Maps judging criteria to evidence, checks, gaps, and next actions. | 3874 |
| RED_TEAM_EVALS.md | safety | Forbidden-outcome red-team tests and regression policy. | 2127 |
| red_team_eval_results.csv | safety | Red-team case outcomes. | 2947 |
| PRIVACY_COMPLIANCE_MODEL.md | privacy_compliance | Public-provider-data boundary, minimization controls, retention, and audit/privacy posture. | 3726 |
| data_minimization_schema.json | privacy_compliance | Allowed entity/field schema and forbidden data classes. | 1432 |
| privacy_controls.csv | privacy_compliance | Machine-readable privacy and compliance controls. | 1888 |
| candidate_updates.csv | prototype_outputs | All proposed provider-directory updates with evidence and confidence. | 22529 |
| REVIEW_DISPOSITION_AND_SLA.md | human_review | Reviewer disposition schema, SLA metrics, and feedback loop. | 2295 |
| review_disposition_contract.json | human_review | Structured reviewer decision contract. | 2185 |
| review_queue.csv | human_review | Ambiguous or high-risk updates routed to manual review. | 15169 |
| FRESH_BUSINESS_LISTING_FALLBACK.md | source_reliability | Guarded business-listing fallback that improves phone/address recall without reducing auto-apply precision. | 1060 |
| SOURCE_CONNECTOR_REGISTRY.md | source_reliability | Connector authority, freshness, cost, fallback, and health contracts. | 3215 |
| SOURCE_PERTURBATION_STRESS_TESTS.md | source_reliability | Stress tests for missing, stale, cheap-only, and conservative source operating modes. | 690 |
| fresh_business_listing_comparison.csv | source_reliability | Legacy-vs-promoted comparison for guarded fresh business-listing fallback. | 637 |
| source_ablation.csv | source_reliability | Source value and cost diagnostic. | 341 |
| source_perturbation_stress_tests.csv | source_reliability | Scenario-level CV metrics under source perturbations and fallback modes. | 563 |
| aws_step_functions_throughput_plan.csv | scalability | AWS batch fan-out sizing scenarios. | 897 |
| synthetic_volume_benchmark.csv | scalability | 100x local throughput benchmark. | 438 |
| CORE_DOC_CONSISTENCY.md | verification | Stale-pattern scan proving core package docs match the current Option C package and metrics. | 264 |
| REPRODUCIBILITY.md | verification | Exact commands and expected outputs for rerunning the prototype, verifier, and package checks. | 1516 |
| core_doc_stale_findings.csv | verification | Machine-readable stale-pattern findings for core judge-facing docs. | 13 |
| verification.json | verification | Machine-readable package verification results. | 29500 |
| RESIDUAL_ERROR_DATA_ACQUISITION.md | metrics | Residual FP/FN analysis and targeted data-acquisition plan for remaining errors. | 510 |
| THRESHOLD_ROBUSTNESS_SWEEP.md | metrics | Local sweep showing threshold/configuration robustness around the current best pipeline. | 1178 |
| cv_metrics.json | metrics | Grouped-CV proxy benchmark metrics. | 8818 |
| data_acquisition_plan.csv | metrics | Field-level acquisition priorities derived from residual errors. | 354 |
| metrics.json | metrics | CLI/prototype metrics. | 509 |
| residual_false_negatives.csv | metrics | Remaining false-negative missed gold updates after normalized matching. | 362 |
| residual_false_positives.csv | metrics | Remaining false-positive proposed updates after normalized matching. | 1522 |
| threshold_robustness_sweep.csv | metrics | Nearby confidence, source-weight, and auto-apply threshold sweep results. | 1189 |
| dashboard/index.html | dashboard | Static operations dashboard prototype. | 16965 |
| dashboard/index.html | dashboard | Lifecycle, LLM, and rollback dashboard lanes. | 16965 |
| audit_events.jsonl | audit | Append-only audit trail sample. | 44305 |
| rollback_plan.csv | audit | Rollback plan for applied updates. | 3285 |
| PUBLIC_DATASET_PROFILE.md | data_profile | Profile and review-first triage transfer check for the visible 42k-row public provider-directory dataset. | 2345 |
| PUBLIC_DATASET_TRIAGE_CLI.md | data_profile | Commands and expected outputs for rerunning the public provider-directory dataset triage CLI. | 665 |
| public_dataset_issue_counts.csv | data_profile | Issue counts from validation checks on the public provider-directory dataset. | 424 |
| public_dataset_missingness.csv | data_profile | Field-level missingness profile for the public provider-directory dataset. | 860 |
| public_dataset_profile_summary.json | data_profile | Machine-readable summary of the public provider-directory dataset profile. | 2961 |
| public_dataset_triage_action_counts.csv | data_profile | Review-first action counts for public provider-directory dataset triage. | 137 |
| public_dataset_triage_cli_summary.json | data_profile | Machine-readable summary from the reusable public dataset triage CLI run. | 299 |
| public_dataset_triage_top500.csv | data_profile | Highest-risk public provider-directory rows under the review-first triage policy. | 122890 |
| AGENT_SKILLS_INSIGHTS.md | agentic_harness | Agent Skills Day 3 workflow-to-skill strategy, authority tiers, and eval coverage. | 3401 |
| CAPABILITY_PROFILES_AND_ORCHESTRATION.md | agentic_harness | AWS-oriented capability profiles and skill orchestration DAG for the agentic workflow. | 2573 |
| PROVIDER_DIRECTORY_SKILLS_LIBRARY.md | agentic_harness | Portable provider-directory Agent Skills library with trigger evals and authority tiers. | 1624 |
| SKILL_LIBRARY_EVALS.md | agentic_harness | Mechanical regression eval report for generated provider-directory skills. | 999 |
| agent_capability_profiles.json | agentic_harness | Capability profile manifest mapping skills to agents, permissions, AWS runtime, gates, inputs, and outputs. | 5675 |
| evidence_tool_manifest.json | agentic_harness | Evidence connector tool schemas and permissions. | 11371 |
| provider_directory_skill_candidates.csv | agentic_harness | Provider-directory workflow lanes mapped to skill candidates, owners, triggers, and evals. | 1667 |
| provider_directory_skills/auditing_and_rollback/SKILL.md | agentic_harness | Generated Agent Skill instructions for a specific provider-directory workflow lane. | 1087 |
| provider_directory_skills/auditing_and_rollback/evals/trigger_cases.json | agentic_harness | Positive and negative trigger eval cases for a generated Agent Skill. | 1322 |
| provider_directory_skills/auditing_and_rollback/references/authority_tier.md | agentic_harness | Authority and approval requirements for a generated Agent Skill. | 362 |
| provider_directory_skills/checking_source_health/SKILL.md | agentic_harness | Generated Agent Skill instructions for a specific provider-directory workflow lane. | 1144 |
| provider_directory_skills/checking_source_health/evals/trigger_cases.json | agentic_harness | Positive and negative trigger eval cases for a generated Agent Skill. | 1376 |
| provider_directory_skills/checking_source_health/references/authority_tier.md | agentic_harness | Authority and approval requirements for a generated Agent Skill. | 397 |
| provider_directory_skills/evaluating_provider_directory_pipeline/SKILL.md | agentic_harness | Generated Agent Skill instructions for a specific provider-directory workflow lane. | 1124 |
| provider_directory_skills/evaluating_provider_directory_pipeline/evals/trigger_cases.json | agentic_harness | Positive and negative trigger eval cases for a generated Agent Skill. | 1554 |
| provider_directory_skills/evaluating_provider_directory_pipeline/references/authority_tier.md | agentic_harness | Authority and approval requirements for a generated Agent Skill. | 391 |
| provider_directory_skills/normalizing_provider_evidence/SKILL.md | agentic_harness | Generated Agent Skill instructions for a specific provider-directory workflow lane. | 1083 |
| provider_directory_skills/normalizing_provider_evidence/evals/trigger_cases.json | agentic_harness | Positive and negative trigger eval cases for a generated Agent Skill. | 1418 |
| provider_directory_skills/normalizing_provider_evidence/references/authority_tier.md | agentic_harness | Authority and approval requirements for a generated Agent Skill. | 377 |
| provider_directory_skills/resolving_provider_identity/SKILL.md | agentic_harness | Generated Agent Skill instructions for a specific provider-directory workflow lane. | 1119 |
| provider_directory_skills/resolving_provider_identity/evals/trigger_cases.json | agentic_harness | Positive and negative trigger eval cases for a generated Agent Skill. | 1424 |
| provider_directory_skills/resolving_provider_identity/references/authority_tier.md | agentic_harness | Authority and approval requirements for a generated Agent Skill. | 383 |
| provider_directory_skills/routing_human_review/SKILL.md | agentic_harness | Generated Agent Skill instructions for a specific provider-directory workflow lane. | 1073 |
| provider_directory_skills/routing_human_review/evals/trigger_cases.json | agentic_harness | Positive and negative trigger eval cases for a generated Agent Skill. | 1308 |
| provider_directory_skills/routing_human_review/references/authority_tier.md | agentic_harness | Authority and approval requirements for a generated Agent Skill. | 369 |
| provider_directory_skills_index.csv | agentic_harness | Index of generated provider-directory skills, authority tiers, owners, and eval coverage. | 800 |
| skill_eval_coverage.json | agentic_harness | Eval coverage requirements for provider-directory skill candidates. | 456 |
| skill_library_eval_results.csv | agentic_harness | Per-skill regression check results for trigger coverage, authority tiers, tools, and context budget. | 6356 |
| skill_library_eval_summary.json | agentic_harness | Machine-readable pass/fail summary for the generated skill-library regression suite. | 137 |
| skill_orchestration_dag.csv | agentic_harness | AWS Step Functions-style skill orchestration DAG with message names and blocking gates. | 1501 |
| auto_apply_updates.csv | safe_automation | Subset eligible for low-risk auto-apply. | 7679 |
| ACTIVE_LEARNING_FEEDBACK.md | supporting_artifact | Supporting package artifact. | 2910 |
| AGENTIC_WHITEPAPER_INSIGHTS.md | supporting_artifact | Supporting package artifact. | 2282 |
| AGENT_CARDS_AND_WORKFLOW_CONTRACTS.md | supporting_artifact | Supporting package artifact. | 3362 |
| AGENT_SECURITY_MATRIX.md | supporting_artifact | Supporting package artifact. | 2774 |
| ARCHITECTURE.md | supporting_artifact | Supporting package artifact. | 2210 |
| ARTIFACT_INDEX.md | supporting_artifact | Supporting package artifact. | 16182 |
| AUDIT_ROLLBACK_WORKFLOW.md | supporting_artifact | Supporting package artifact. | 1456 |
| AWS_PRODUCTION_ARCHITECTURE.md | supporting_artifact | Supporting package artifact. | 4093 |
| BENCHMARK_DATASHEET.md | supporting_artifact | Supporting package artifact. | 4215 |
| CASE_STUDIES.md | supporting_artifact | Supporting package artifact. | 2475 |
| COST_MODEL.md | supporting_artifact | Supporting package artifact. | 1856 |
| DASHBOARD_SPEC.md | supporting_artifact | Supporting package artifact. | 4680 |
| DUPLICATE_MOVEMENT_DETECTION.md | supporting_artifact | Supporting package artifact. | 2504 |
| EXTERNAL_SOURCE_STRATEGY.md | supporting_artifact | Supporting package artifact. | 5254 |
| FIELD_RISK_POLICY.md | supporting_artifact | Supporting package artifact. | 886 |
| FINAL_RELEASE_NOTES.md | supporting_artifact | Supporting package artifact. | 1900 |
| INACTIVE_PROVIDER_DETECTION.md | supporting_artifact | Supporting package artifact. | 1991 |
| INCIDENT_RESPONSE_RUNBOOKS.md | supporting_artifact | Supporting package artifact. | 2117 |
| JUDGING_NARRATIVE.md | supporting_artifact | Supporting package artifact. | 1835 |
| LLM_FALLBACK_CONTRACT.md | supporting_artifact | Supporting package artifact. | 2035 |
| MILESTONE_100_NORTH_STAR_AUDIT.md | supporting_artifact | Supporting package artifact. | 1742 |
| MISSING_SOURCE_ROBUSTNESS.md | supporting_artifact | Supporting package artifact. | 2130 |
| MONITORING_ALERTS.md | supporting_artifact | Supporting package artifact. | 2498 |
| NO_SECRETS_SCAN.md | supporting_artifact | Supporting package artifact. | 170 |
| NPPES_API_SMOKE.md | supporting_artifact | Supporting package artifact. | 1556 |
| PACKAGE_INTEGRITY_MANIFEST.md | supporting_artifact | Supporting package artifact. | 140 |
| PRACTICE_AFFILIATION_REBRAND.md | supporting_artifact | Supporting package artifact. | 1415 |
| REVIEW_QUEUE_PRIORITIZATION.md | supporting_artifact | Supporting package artifact. | 1597 |
| RISK_REGISTER.md | supporting_artifact | Supporting package artifact. | 1051 |
| SOURCE_CONFLICT_ADJUDICATION.md | supporting_artifact | Supporting package artifact. | 3312 |
| SOURCE_FRESHNESS_ALERTS.md | supporting_artifact | Supporting package artifact. | 2365 |
| SOURCE_GOVERNANCE_CHECKLIST.md | supporting_artifact | Supporting package artifact. | 2065 |
| SPECIALTY_NORMALIZATION.md | supporting_artifact | Supporting package artifact. | 1458 |
| SUBMISSION_CHECKLIST.md | supporting_artifact | Supporting package artifact. | 1734 |
| SYNTHETIC_VOLUME_BENCHMARK.md | supporting_artifact | Supporting package artifact. | 934 |
