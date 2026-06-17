from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


ARTIFACT_PURPOSES: dict[str, tuple[str, str]] = {
    "README.md": ("start_here", "Package entrypoint and recommended reading order."),
    "EXECUTIVE_SUMMARY.md": ("judge_narrative", "High-level positioning, metrics, and rubric mapping."),
    "PRODUCTION_READINESS_SCORECARD.md": ("readiness", "Maps judging criteria to evidence, checks, gaps, and next actions."),
    "AGENT_WORKFLOW_DIAGRAM.md": ("workflow", "Agentic workflow diagram with source-to-review-to-audit handoffs."),
    "AGENT_SKILLS_INSIGHTS.md": ("agentic_harness", "Agent Skills Day 3 workflow-to-skill strategy, authority tiers, and eval coverage."),
    "PROVIDER_DIRECTORY_SKILLS_LIBRARY.md": ("agentic_harness", "Portable provider-directory Agent Skills library with trigger evals and authority tiers."),
    "SKILL_LIBRARY_EVALS.md": ("agentic_harness", "Mechanical regression eval report for generated provider-directory skills."),
    "CAPABILITY_PROFILES_AND_ORCHESTRATION.md": ("agentic_harness", "AWS-oriented capability profiles and skill orchestration DAG for the agentic workflow."),
    "JUDGE_RUBRIC_SELF_EVAL.md": ("judge_narrative", "Artifact-backed self-evaluation against qualitative competition judging criteria."),
    "SOURCE_PERTURBATION_STRESS_TESTS.md": ("source_reliability", "Stress tests for missing, stale, cheap-only, and conservative source operating modes."),
    "THRESHOLD_ROBUSTNESS_SWEEP.md": ("metrics", "Local sweep showing threshold/configuration robustness around the current best pipeline."),
    "RESIDUAL_ERROR_DATA_ACQUISITION.md": ("metrics", "Residual FP/FN analysis and targeted data-acquisition plan for remaining errors."),
    "FRESH_BUSINESS_LISTING_FALLBACK.md": ("source_reliability", "Guarded business-listing fallback that improves phone/address recall without reducing auto-apply precision."),
    "ONE_PAGE_JUDGE_GUIDE.md": ("judge_narrative", "Concise package walkthrough for judges: what to open, what it proves, and expected metrics."),
    "REPRODUCIBILITY.md": ("verification", "Exact commands and expected outputs for rerunning the prototype, verifier, and package checks."),
    "MVP_FIELD_COVERAGE.md": ("judge_narrative", "Option C hybrid submission map from MVP fields and bonus capabilities to prototype and production artifacts."),
    "CORE_DOC_CONSISTENCY.md": ("verification", "Stale-pattern scan proving core package docs match the current Option C package and metrics."),
    "COMPETITION_ALIGNMENT_REFRESH.md": ("judge_narrative", "Live competition-surface refresh, evaluation-criteria map, and public-notebook gap analysis."),
    "COMBINED_ABC_PIPELINE_COVERAGE.md": ("judge_narrative", "Combined Option A/B/C coverage map for desired pipeline, required capabilities, evaluation criteria, bonus points, and MVP fields."),
    "PUBLIC_DATASET_PROFILE.md": ("data_profile", "Profile and review-first triage transfer check for the visible 42k-row public provider-directory dataset."),
    "PUBLIC_DATASET_TRIAGE_CLI.md": ("data_profile", "Commands and expected outputs for rerunning the public provider-directory dataset triage CLI."),
    "KAGGLE_SUBMISSION_HANDOFF.md": ("start_here", "Concise upload instructions, suggested title/description, and pre-upload verification command."),
    "RED_TEAM_EVALS.md": ("safety", "Forbidden-outcome red-team tests and regression policy."),
    "PRIVACY_COMPLIANCE_MODEL.md": ("privacy_compliance", "Public-provider-data boundary, minimization controls, retention, and audit/privacy posture."),
    "SOURCE_CONNECTOR_REGISTRY.md": ("source_reliability", "Connector authority, freshness, cost, fallback, and health contracts."),
    "REVIEW_DISPOSITION_AND_SLA.md": ("human_review", "Reviewer disposition schema, SLA metrics, and feedback loop."),
    "candidate_updates.csv": ("prototype_outputs", "All proposed provider-directory updates with evidence and confidence."),
    "auto_apply_updates.csv": ("safe_automation", "Subset eligible for low-risk auto-apply."),
    "review_queue.csv": ("human_review", "Ambiguous or high-risk updates routed to manual review."),
    "verification.json": ("verification", "Machine-readable package verification results."),
    "metrics.json": ("metrics", "CLI/prototype metrics."),
    "cv_metrics.json": ("metrics", "Grouped-CV proxy benchmark metrics."),
    "source_ablation.csv": ("source_reliability", "Source value and cost diagnostic."),
    "synthetic_volume_benchmark.csv": ("scalability", "100x local throughput benchmark."),
    "aws_step_functions_throughput_plan.csv": ("scalability", "AWS batch fan-out sizing scenarios."),
    "red_team_eval_results.csv": ("safety", "Red-team case outcomes."),
    "agent_workflow_diagram.mmd": ("workflow", "Mermaid source for the workflow diagram."),
    "evidence_tool_manifest.json": ("agentic_harness", "Evidence connector tool schemas and permissions."),
    "provider_directory_skill_candidates.csv": ("agentic_harness", "Provider-directory workflow lanes mapped to skill candidates, owners, triggers, and evals."),
    "provider_directory_skills_index.csv": ("agentic_harness", "Index of generated provider-directory skills, authority tiers, owners, and eval coverage."),
    "skill_eval_coverage.json": ("agentic_harness", "Eval coverage requirements for provider-directory skill candidates."),
    "skill_library_eval_results.csv": ("agentic_harness", "Per-skill regression check results for trigger coverage, authority tiers, tools, and context budget."),
    "skill_library_eval_summary.json": ("agentic_harness", "Machine-readable pass/fail summary for the generated skill-library regression suite."),
    "agent_capability_profiles.json": ("agentic_harness", "Capability profile manifest mapping skills to agents, permissions, AWS runtime, gates, inputs, and outputs."),
    "skill_orchestration_dag.csv": ("agentic_harness", "AWS Step Functions-style skill orchestration DAG with message names and blocking gates."),
    "judge_rubric_self_eval.csv": ("judge_narrative", "Criterion-level rubric scores, weights, evidence links, and metric checks."),
    "judge_rubric_self_eval_summary.json": ("judge_narrative", "Machine-readable summary of package rubric self-evaluation."),
    "source_perturbation_stress_tests.csv": ("source_reliability", "Scenario-level CV metrics under source perturbations and fallback modes."),
    "threshold_robustness_sweep.csv": ("metrics", "Nearby confidence, source-weight, and auto-apply threshold sweep results."),
    "residual_false_positives.csv": ("metrics", "Remaining false-positive proposed updates after normalized matching."),
    "residual_false_negatives.csv": ("metrics", "Remaining false-negative missed gold updates after normalized matching."),
    "data_acquisition_plan.csv": ("metrics", "Field-level acquisition priorities derived from residual errors."),
    "fresh_business_listing_comparison.csv": ("source_reliability", "Legacy-vs-promoted comparison for guarded fresh business-listing fallback."),
    "mvp_field_coverage.csv": ("judge_narrative", "Machine-readable Option C hybrid MVP field and requirement coverage map."),
    "core_doc_stale_findings.csv": ("verification", "Machine-readable stale-pattern findings for core judge-facing docs."),
    "competition_alignment_matrix.csv": ("judge_narrative", "Machine-readable map from competition criteria to package artifacts."),
    "public_notebook_gap_analysis.csv": ("judge_narrative", "Machine-readable comparison against the observed public Kaggle notebook."),
    "public_notebook_summary.json": ("judge_narrative", "Metadata and keyword summary for the observed public Kaggle notebook."),
    "public_dataset_profile_summary.json": ("data_profile", "Machine-readable summary of the public provider-directory dataset profile."),
    "public_dataset_missingness.csv": ("data_profile", "Field-level missingness profile for the public provider-directory dataset."),
    "public_dataset_issue_counts.csv": ("data_profile", "Issue counts from validation checks on the public provider-directory dataset."),
    "public_dataset_triage_action_counts.csv": ("data_profile", "Review-first action counts for public provider-directory dataset triage."),
    "public_dataset_triage_top500.csv": ("data_profile", "Highest-risk public provider-directory rows under the review-first triage policy."),
    "public_dataset_triage_cli_summary.json": ("data_profile", "Machine-readable summary from the reusable public dataset triage CLI run."),
    "combined_abc_options.csv": ("judge_narrative", "Machine-readable map showing Option A, Option B, and Option C are all included."),
    "combined_abc_pipeline.csv": ("judge_narrative", "Machine-readable trace of the requested pipeline architecture to prototype and production artifacts."),
    "combined_abc_capabilities.csv": ("judge_narrative", "Machine-readable coverage map for required system capabilities."),
    "combined_abc_evaluation.csv": ("judge_narrative", "Machine-readable coverage map for evaluation criteria."),
    "combined_abc_bonus.csv": ("judge_narrative", "Machine-readable coverage map for bonus-point items."),
    "combined_abc_mvp.csv": ("judge_narrative", "Machine-readable coverage map for suggested MVP fields."),
    "SKILL.md": ("agentic_harness", "Generated Agent Skill instructions for a specific provider-directory workflow lane."),
    "trigger_cases.json": ("agentic_harness", "Positive and negative trigger eval cases for a generated Agent Skill."),
    "authority_tier.md": ("agentic_harness", "Authority and approval requirements for a generated Agent Skill."),
    "review_disposition_contract.json": ("human_review", "Structured reviewer decision contract."),
    "privacy_controls.csv": ("privacy_compliance", "Machine-readable privacy and compliance controls."),
    "data_minimization_schema.json": ("privacy_compliance", "Allowed entity/field schema and forbidden data classes."),
    "audit_events.jsonl": ("audit", "Append-only audit trail sample."),
    "rollback_plan.csv": ("audit", "Rollback plan for applied updates."),
    "dashboard/index.html": ("dashboard", "Static operations dashboard prototype."),
    "dashboard_v2/index.html": ("dashboard", "Lifecycle, LLM, and rollback dashboard lanes."),
}


def build_artifact_index(package_dir: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for path in sorted(package_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(package_dir).as_posix()
        name = path.name if "/" not in rel else rel
        category, purpose = ARTIFACT_PURPOSES.get(name, ARTIFACT_PURPOSES.get(path.name, ("supporting_artifact", "Supporting package artifact.")))
        rows.append(
            {
                "artifact": rel,
                "category": category,
                "purpose": purpose,
                "size_bytes": path.stat().st_size,
                "inspection_priority": inspection_priority(category),
            }
        )
    return pd.DataFrame(rows).sort_values(["inspection_priority", "category", "artifact"]).reset_index(drop=True)


def inspection_priority(category: str) -> int:
    order = {
        "start_here": 1,
        "judge_narrative": 2,
        "workflow": 3,
        "readiness": 4,
        "safety": 5,
        "privacy_compliance": 6,
        "prototype_outputs": 7,
        "human_review": 8,
        "source_reliability": 9,
        "scalability": 10,
        "verification": 11,
        "metrics": 12,
        "dashboard": 13,
        "audit": 14,
        "data_profile": 15,
        "agentic_harness": 16,
    }
    return order.get(category, 50)
