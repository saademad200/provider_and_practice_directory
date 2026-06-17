#!/usr/bin/env python3
from __future__ import annotations

import argparse
import compileall
import json
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_best_pipeline import BEST_CFG
from src.cv import run_cv


REQUIRED_DOCS = [
    "docs/ARCHITECTURE.md",
    "docs/JUDGING_NARRATIVE.md",
    "docs/FIELD_RISK_POLICY.md",
    "docs/SUBMISSION_CHECKLIST.md",
    "docs/RISK_REGISTER.md",
    "docs/BENCHMARK_DATASHEET.md",
]

REQUIRED_PACKAGE_FILES = [
    "README.md",
    "Provider_Directory_Update_Pipeline_End_to_End.ipynb",
    "PRESENTATION_NARRATIVE.md",
    "candidate_updates.csv",
    "auto_apply_updates.csv",
    "review_queue.csv",
    "config.json",
    "metrics.json",
    "cv_metrics.json",
    "source_ablation.csv",
    "web_extraction_benchmark.json",
    "nppes_parsed_evidence.json",
    "per_field.csv",
    "worst_providers.csv",
    "BENCHMARK_DATASHEET.md",
    "REVIEW_QUEUE_PRIORITIZATION.md",
    "CASE_STUDIES.md",
    "EXECUTIVE_SUMMARY.md",
    "EXTERNAL_SOURCE_STRATEGY.md",
    "MISSING_SOURCE_ROBUSTNESS.md",
    "SOURCE_FRESHNESS_ALERTS.md",
    "AWS_PRODUCTION_ARCHITECTURE.md",
    "ACTIVE_LEARNING_FEEDBACK.md",
    "DASHBOARD_SPEC.md",
    "DUPLICATE_MOVEMENT_DETECTION.md",
    "COST_MODEL.md",
    "MONITORING_ALERTS.md",
    "NPPES_API_SMOKE.md",
    "SPECIALTY_NORMALIZATION.md",
    "PRACTICE_AFFILIATION_REBRAND.md",
    "SOURCE_GOVERNANCE_CHECKLIST.md",
    "INACTIVE_PROVIDER_DETECTION.md",
    "LLM_FALLBACK_CONTRACT.md",
    "AUDIT_ROLLBACK_WORKFLOW.md",
    "SOURCE_CONFLICT_ADJUDICATION.md",
    "AGENTIC_WHITEPAPER_INSIGHTS.md",
    "AGENT_CARDS_AND_WORKFLOW_CONTRACTS.md",
    "TRAJECTORY_TOOL_USE_EVALS.md",
    "AGENT_SECURITY_MATRIX.md",
    "INCIDENT_RESPONSE_RUNBOOKS.md",
    "PRODUCTION_READINESS_SCORECARD.md",
    "SYNTHETIC_VOLUME_BENCHMARK.md",
    "SOURCE_CONNECTOR_REGISTRY.md",
    "REVIEW_DISPOSITION_AND_SLA.md",
    "RED_TEAM_EVALS.md",
    "AGENT_WORKFLOW_DIAGRAM.md",
    "AGENT_SKILLS_INSIGHTS.md",
    "PROVIDER_DIRECTORY_SKILLS_LIBRARY.md",
    "SKILL_LIBRARY_EVALS.md",
    "CAPABILITY_PROFILES_AND_ORCHESTRATION.md",
    "JUDGE_RUBRIC_SELF_EVAL.md",
    "SOURCE_PERTURBATION_STRESS_TESTS.md",
    "THRESHOLD_ROBUSTNESS_SWEEP.md",
    "RESIDUAL_ERROR_DATA_ACQUISITION.md",
    "FRESH_BUSINESS_LISTING_FALLBACK.md",
    "ONE_PAGE_JUDGE_GUIDE.md",
    "REPRODUCIBILITY.md",
    "MVP_FIELD_COVERAGE.md",
    "CORE_DOC_CONSISTENCY.md",
    "COMBINED_ABC_PIPELINE_COVERAGE.md",
    "TECHNICAL_ARCHITECTURE_PROPOSAL.md",
    "WORKING_PROTOTYPE.md",
    "ARCHITECTURE_DIAGRAM.md",
    "ARCHITECTURE_DIAGRAM.mmd",
    "COMPETITION_ALIGNMENT_REFRESH.md",
    "PUBLIC_DATASET_PROFILE.md",
    "PUBLIC_DATASET_TRIAGE_CLI.md",
    "KAGGLE_SUBMISSION_HANDOFF.md",
    "ARTIFACT_INDEX.md",
    "PRIVACY_COMPLIANCE_MODEL.md",
    "PACKAGE_INTEGRITY_MANIFEST.md",
    "NO_SECRETS_SCAN.md",
    "FINAL_RELEASE_NOTES.md",
    "MILESTONE_100_NORTH_STAR_AUDIT.md",
    "verification.json",
    "prioritized_review_queue.csv",
    "case_studies.json",
    "missing_source_robustness.csv",
    "freshness_summary.csv",
    "aws_service_map.json",
    "learning_actions.csv",
    "dashboard_data_contract.json",
    "dashboard_review_queue.csv",
    "duplicate_candidates.csv",
    "provider_movement_candidates.csv",
    "cost_model_per_1000.csv",
    "monitoring_alerts.json",
    "dashboard/index.html",
    "dashboard_v2/index.html",
    "nppes_api_evidence.csv",
    "specialty_normalization_fixture.csv",
    "practice_change_candidates.csv",
    "source_governance_checklist.json",
    "inactive_provider_candidates.csv",
    "bedrock_extraction_contract.json",
    "llm_fallback_fixture.csv",
    "audit_events.jsonl",
    "rollback_plan.csv",
    "provider_change_timeline.csv",
    "source_conflict_adjudication.csv",
    "agent_cards.json",
    "orchestrator_contract.json",
    "trajectory_trace_fixture.csv",
    "trajectory_eval_results.csv",
    "trajectory_eval_rubric.csv",
    "agent_security_matrix.csv",
    "incident_response_runbooks.csv",
    "production_readiness_scorecard.csv",
    "production_readiness_summary.json",
    "synthetic_volume_benchmark.csv",
    "aws_step_functions_throughput_plan.csv",
    "source_connector_registry.csv",
    "evidence_tool_manifest.json",
    "connector_health_check_fixture.csv",
    "review_disposition_contract.json",
    "review_sla_metrics.csv",
    "review_outcome_feedback_fixture.csv",
    "red_team_cases.csv",
    "red_team_eval_results.csv",
    "red_team_summary.json",
    "agent_workflow_diagram.mmd",
    "agent_workflow_nodes.csv",
    "agent_workflow_edges.csv",
    "artifact_index.csv",
    "privacy_controls.csv",
    "data_minimization_schema.json",
    "package_integrity_manifest.csv",
    "package_integrity_summary.json",
    "no_secrets_findings.csv",
    "no_secrets_summary.json",
    "milestone_100_north_star_audit.csv",
    "provider_directory_skill_candidates.csv",
    "provider_directory_skills_index.csv",
    "skill_eval_coverage.json",
    "skill_library_eval_results.csv",
    "skill_library_eval_summary.json",
    "agent_capability_profiles.json",
    "skill_orchestration_dag.csv",
    "judge_rubric_self_eval.csv",
    "judge_rubric_self_eval_summary.json",
    "source_perturbation_stress_tests.csv",
    "threshold_robustness_sweep.csv",
    "residual_false_positives.csv",
    "residual_false_negatives.csv",
    "data_acquisition_plan.csv",
    "fresh_business_listing_comparison.csv",
    "mvp_field_coverage.csv",
    "core_doc_stale_findings.csv",
    "competition_alignment_matrix.csv",
    "public_notebook_gap_analysis.csv",
    "public_notebook_summary.json",
    "public_dataset_profile_summary.json",
    "public_dataset_missingness.csv",
    "public_dataset_issue_counts.csv",
    "public_dataset_triage_action_counts.csv",
    "public_dataset_triage_top500.csv",
    "public_dataset_triage_cli_summary.json",
    "combined_abc_options.csv",
    "combined_abc_pipeline.csv",
    "combined_abc_capabilities.csv",
    "combined_abc_evaluation.csv",
    "combined_abc_bonus.csv",
    "combined_abc_mvp.csv",
    "provider_directory_skills/auditing_and_rollback/SKILL.md",
    "provider_directory_skills/auditing_and_rollback/evals/trigger_cases.json",
    "provider_directory_skills/auditing_and_rollback/references/authority_tier.md",
    "provider_directory_skills/checking_source_health/SKILL.md",
    "provider_directory_skills/checking_source_health/evals/trigger_cases.json",
    "provider_directory_skills/checking_source_health/references/authority_tier.md",
    "provider_directory_skills/evaluating_provider_directory_pipeline/SKILL.md",
    "provider_directory_skills/evaluating_provider_directory_pipeline/evals/trigger_cases.json",
    "provider_directory_skills/evaluating_provider_directory_pipeline/references/authority_tier.md",
    "provider_directory_skills/normalizing_provider_evidence/SKILL.md",
    "provider_directory_skills/normalizing_provider_evidence/evals/trigger_cases.json",
    "provider_directory_skills/normalizing_provider_evidence/references/authority_tier.md",
    "provider_directory_skills/resolving_provider_identity/SKILL.md",
    "provider_directory_skills/resolving_provider_identity/evals/trigger_cases.json",
    "provider_directory_skills/resolving_provider_identity/references/authority_tier.md",
    "provider_directory_skills/routing_human_review/SKILL.md",
    "provider_directory_skills/routing_human_review/evals/trigger_cases.json",
    "provider_directory_skills/routing_human_review/references/authority_tier.md",
]


def record(checks: list[dict[str, Any]], name: str, passed: bool, detail: str = "") -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


def compile_project(checks: list[dict[str, Any]]) -> None:
    targets = ["src", "scripts", "experiments"]
    ok = True
    for target in targets:
        ok = compileall.compile_dir(ROOT / target, quiet=1, force=True) and ok
    record(checks, "python_compile", ok, ", ".join(targets))


def run_smoke_cv(checks: list[dict[str, Any]]) -> dict:
    result = run_cv({**BEST_CFG, "seed": 42, "n_splits": 5, "smoke": True, "max_providers": 18})
    overall = result["overall"]
    passed = overall["predicted_updates"] > 0 and overall["f1"] >= 0.80
    detail = f"f1={overall['f1']}, predicted={overall['predicted_updates']}"
    record(checks, "smoke_cv", passed, detail)
    return result


def run_cli(checks: list[dict[str, Any]], out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [sys.executable, "scripts/run_best_pipeline.py", "--out-dir", str(out_dir)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    record(checks, "cli_exit", proc.returncode == 0, proc.stderr[-400:])
    metrics_path = out_dir / "metrics.json"
    if not metrics_path.exists():
        record(checks, "cli_metrics_exists", False, str(metrics_path))
        return {}
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    passed = metrics["f1"] >= 0.90 and metrics["auto_apply_precision"] >= 0.95
    detail = f"f1={metrics['f1']}, auto_precision={metrics['auto_apply_precision']}"
    record(checks, "cli_metrics_thresholds", passed, detail)
    for name in ["candidate_updates.csv", "auto_apply_updates.csv", "review_queue.csv", "config.json"]:
        record(checks, f"cli_output_{name}", (out_dir / name).exists(), str(out_dir / name))
    return metrics


def run_public_dataset_cli_smoke(checks: list[dict[str, Any]], out_dir: Path) -> None:
    dataset_path = ROOT / "data/raw/kaggle_public_provider_directory/provider_directory_dataset.csv"
    if not dataset_path.exists():
        record(checks, "public_dataset_cli_smoke", True, "skipped_missing_public_dataset")
        return
    cli_out = out_dir / "public_dataset_cli"
    proc = subprocess.run(
        [
            sys.executable,
            "scripts/run_public_dataset_triage.py",
            "--input",
            str(dataset_path),
            "--out-dir",
            str(cli_out),
            "--top-n",
            "25",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        record(checks, "public_dataset_cli_smoke", False, proc.stderr[-400:])
        return
    summary_path = cli_out / "public_dataset_profile_summary.json"
    top_path = cli_out / "public_dataset_triage_top25.csv"
    if not summary_path.exists():
        record(checks, "public_dataset_cli_smoke", False, "missing public_dataset_profile_summary.json")
        return
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    passed = summary.get("rows", 0) >= 1000 and top_path.exists()
    record(checks, "public_dataset_cli_smoke", passed, f"rows={summary.get('rows')}, top25={top_path.exists()}")


def validate_docs(checks: list[dict[str, Any]]) -> None:
    for doc in REQUIRED_DOCS:
        path = ROOT / doc
        record(checks, f"doc_{Path(doc).name}", path.exists() and path.stat().st_size > 0, doc)


def validate_notebook(checks: list[dict[str, Any]]) -> None:
    notebook_path = ROOT / "notebooks/Provider_Directory_Update_Pipeline_End_to_End.ipynb"
    if not notebook_path.exists():
        record(checks, "notebook_exists", False, str(notebook_path))
        return
    try:
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        record(checks, "notebook_json_valid", False, str(exc))
        return
    cells = notebook.get("cells", [])
    markdown_count = sum(1 for cell in cells if cell.get("cell_type") == "markdown")
    code_count = sum(1 for cell in cells if cell.get("cell_type") == "code")
    text = "\n".join("".join(cell.get("source", [])) for cell in cells)
    required_terms = [
        "Evaluation Criteria",
        "Bonus Point Coverage",
        "AWS Production Plan",
        "Whitepaper-Informed Design",
        "Technical Architecture Diagram",
        "Working Prototype",
    ]
    missing_terms = [term for term in required_terms if term not in text]
    record(checks, "notebook_json_valid", True, str(notebook_path))
    record(checks, "notebook_cell_count", markdown_count >= 10 and code_count >= 10, f"markdown={markdown_count}, code={code_count}")
    record(checks, "notebook_required_story_terms", not missing_terms, ", ".join(missing_terms))


def validate_package(checks: list[dict[str, Any]], package_path: Path) -> None:
    if not package_path.exists():
        record(checks, "package_exists", False, str(package_path))
        return
    record(checks, "package_exists", True, str(package_path))
    with zipfile.ZipFile(package_path) as archive:
        names = set(archive.namelist())
    top_level_dirs = {name.split("/", 1)[0] for name in names if "/" in name}
    prefix = next(iter(top_level_dirs)) if len(top_level_dirs) == 1 else package_path.stem.split("_", 1)[0]
    for filename in REQUIRED_PACKAGE_FILES:
        expected = f"{prefix}/{filename}"
        record(checks, f"package_{filename}", expected in names, expected)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify provider directory pipeline artifacts.")
    parser.add_argument("--out-dir", default="outputs/verify_pipeline", help="Directory for verification outputs.")
    parser.add_argument(
        "--package",
        default="submissions/exp0172_final_combined_abc_handoff_package.zip",
        help="Submission package zip to validate.",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    checks: list[dict[str, Any]] = []
    compile_project(checks)
    smoke = run_smoke_cv(checks)
    cli_metrics = run_cli(checks, out_dir / "cli")
    run_public_dataset_cli_smoke(checks, out_dir)
    validate_docs(checks)
    validate_notebook(checks)
    validate_package(checks, Path(args.package))

    report = {
        "passed": all(item["passed"] for item in checks),
        "checks": checks,
        "smoke_metrics": smoke["overall"],
        "cli_metrics": cli_metrics,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "verification.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
