#!/usr/bin/env python3
from __future__ import annotations

import argparse
import compileall
import csv
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_best_pipeline import BEST_CFG
from src.cv import run_cv
from src.npi import valid_npi


REQUIRED_DOCS = [
    "README.md",
    "SUBMISSION.md",
    "FINAL_UPLOAD.md",
]

REQUIRED_PACKAGE_FILES: list[str] = []

CURATED_PACKAGE_FILES = [
    "README.md",
    "START_HERE.md",
    "Provider_Directory_Update_Pipeline_End_to_End.ipynb",
    "proposal/ONE_PAGE_SCORECARD.md",
    "proposal/JUDGE_DECISION_MEMO.md",
    "proposal/BONUS_COVERAGE_MATRIX.md",
    "proposal/PRESENTATION_NARRATIVE.md",
    "proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md",
    "proposal/CONFIDENCE_AND_DECISION_POLICY.md",
    "proposal/SHADOW_MODE_PILOT_PROTOCOL.md",
    "proposal/AGENT_WORKFLOW_DIAGRAM.md",
    "proposal/AGENT_WORKFLOW_DIAGRAM.mmd",
    "proposal/ARCHITECTURE_DIAGRAM.md",
    "proposal/ARCHITECTURE_DIAGRAM.mmd",
    "proposal/IMPLEMENTATION_ROADMAP_90_DAYS.md",
    "proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md",
    "proposal/SOURCE_ACCESS_COMPLIANCE_POLICY.md",
    "proposal/OFFICIAL_SOURCE_REFERENCES.md",
    "prototype/WORKING_PROTOTYPE.md",
    "prototype/RECOMMENDATION_API_CONTRACT.md",
    "prototype/metrics.json",
    "prototype/candidate_updates.csv",
    "prototype/auto_apply_updates.csv",
    "prototype/review_queue.csv",
    "prototype/recommendation_api_examples.json",
    "prototype/recommendation_api_schema.json",
    "dashboard/index.html",
    "evidence/verification.json",
    "evidence/judge_rubric_self_eval.csv",
    "evidence/cost_model_per_1000.csv",
    "evidence/source_connector_registry.csv",
    "evidence/source_reference_health.csv",
    "evidence/audit_events.jsonl",
    "evidence/rollback_plan.csv",
    "appendix/COST_MODEL.md",
    "appendix/AWS_PRODUCTION_ARCHITECTURE.md",
    "appendix/DUPLICATE_MOVEMENT_DETECTION.md",
    "appendix/INACTIVE_PROVIDER_DETECTION.md",
    "appendix/AUDIT_ROLLBACK_WORKFLOW.md",
    "src/data.py",
    "src/entity_resolution.py",
    "src/inactive_detection.py",
    "src/metrics.py",
    "src/cv.py",
    "src/npi.py",
    "src/source_conflicts.py",
    "scripts/run_best_pipeline.py",
    "data/sample/providers.csv",
    "data/sample/evidence.csv",
    "data/sample/gold_updates.csv",
    "requirements.txt",
]

PRIVATE_PACKAGE_PATTERNS = ["JUDGE_AUDIT", "COUNTERMOVE_LOG"]
SECRET_NAME_PATTERNS = [".env", "kaggle.json", "credentials", "secrets"]
SECRET_TEXT_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)aws_secret_access_key"),
    re.compile(r"(?i)kaggle_key"),
    re.compile(r"(?i)kaggle_username"),
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
]
SAFE_AUTO_APPLY_FIELDS = {"phone", "specialty"}
UNSAFE_AUTO_APPLY_DRIVER_PATTERN = re.compile(r"high_field_risk|practice_peer_mismatch|source_gap")


def record(checks: list[dict[str, Any]], name: str, passed: bool, detail: str = "") -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def auto_apply_policy_violations(rows: list[dict[str, str]]) -> list[str]:
    violations: list[str] = []
    for index, row in enumerate(rows, start=2):
        field = row.get("field", "")
        freshness_status = row.get("freshness_status", "")
        drivers = row.get("review_priority_drivers", "")
        reason = row.get("review_reason_code", "")
        if field not in SAFE_AUTO_APPLY_FIELDS:
            violations.append(f"row {index}: unsafe field {field}")
        if freshness_status == "all_stale":
            violations.append(f"row {index}: all_stale evidence")
        if UNSAFE_AUTO_APPLY_DRIVER_PATTERN.search(drivers):
            violations.append(f"row {index}: unsafe driver {drivers}")
        if reason != "auto_apply_criteria_met":
            violations.append(f"row {index}: review reason {reason}")
    return violations


def cost_model_markdown_rows(text: str) -> dict[str, dict[str, float]]:
    rows: dict[str, dict[str, float]] = {}
    columns = [
        "evidence_usd",
        "aws_compute_storage_monitoring_usd",
        "llm_extraction_usd",
        "manual_review_usd",
        "manual_review_items",
        "total_usd",
    ]
    for line in text.splitlines():
        if not line.startswith("| ") or "---" in line or "Scenario" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 7:
            continue
        scenario = cells[0]
        try:
            values = [float(cell) for cell in cells[1:]]
        except ValueError:
            continue
        rows[scenario] = dict(zip(columns, values))
    return rows


def compile_project(checks: list[dict[str, Any]]) -> None:
    targets = ["src", "scripts"]
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
    auto_path = out_dir / "auto_apply_updates.csv"
    if auto_path.exists():
        rows = list(csv.DictReader(auto_path.read_text(encoding="utf-8").splitlines()))
        violations = auto_apply_policy_violations(rows)
        record(
            checks,
            "cli_safe_auto_apply_policy",
            not violations,
            f"rows={len(rows)}, violations={'; '.join(violations[:5])}",
        )
    return metrics


def validate_sample_npis(checks: list[dict[str, Any]]) -> None:
    providers_path = ROOT / "data/sample/providers.csv"
    if not providers_path.exists():
        record(checks, "sample_npi_validity", False, str(providers_path))
        return
    providers = pd.read_csv(providers_path, dtype=str)
    invalid = providers.loc[~providers["npi"].map(valid_npi), "npi"].head(5).tolist()
    record(checks, "sample_npi_validity", not invalid, "; ".join(invalid))


def run_public_dataset_cli_smoke(checks: list[dict[str, Any]], out_dir: Path) -> None:
    dataset_path = ROOT / "data/raw/kaggle_public_provider_directory/provider_directory_dataset.csv"
    if not dataset_path.exists():
        record(checks, "public_dataset_cli_smoke", True, "skipped_missing_public_dataset")
        return
    cli_path = ROOT / "scripts/run_public_dataset_triage.py"
    if not cli_path.exists():
        record(checks, "public_dataset_cli_smoke", True, "skipped_missing_public_dataset_cli")
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
    notebook_path = ROOT / "submissions/healthlynked_option_c_clean/Provider_Directory_Update_Pipeline_End_to_End.ipynb"
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
        "Bonus capabilities",
        "Cloud-Agnostic Production Plan",
        "Whitepaper-Informed Design",
        "Technical Architecture Diagram",
        "Working Prototype",
    ]
    missing_terms = [term for term in required_terms if term not in text]
    record(checks, "notebook_json_valid", True, display_path(notebook_path))
    record(checks, "notebook_cell_count", markdown_count >= 10 and code_count >= 10, f"markdown={markdown_count}, code={code_count}")
    record(checks, "notebook_required_story_terms", not missing_terms, ", ".join(missing_terms))


def validate_recommendation_contract(checks: list[dict[str, Any]]) -> None:
    examples_path = ROOT / "submissions/healthlynked_option_c_clean/prototype/recommendation_api_examples.json"
    schema_path = ROOT / "submissions/healthlynked_option_c_clean/prototype/recommendation_api_schema.json"
    if not examples_path.exists():
        record(checks, "recommendation_examples_exist", False, display_path(examples_path))
        return
    if not schema_path.exists():
        record(checks, "recommendation_schema_exist", False, display_path(schema_path))
        return
    try:
        examples = json.loads(examples_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        record(checks, "recommendation_json_valid", False, str(exc))
        return
    recommendations = examples.get("recommendations", [])
    required_keys = {"provider_id", "npi", "change_detected", "changes", "overall_confidence", "recommended_action", "reason"}
    valid_shape = bool(recommendations) and all(required_keys.issubset(item) for item in recommendations)
    has_sources = all(
        all("supporting_sources" in change and change["supporting_sources"] for change in item.get("changes", []))
        for item in recommendations
    )
    has_field_decisions = all(
        all(
            change.get("field_decision") in {"auto_apply", "review"}
            and change.get("launch_state") in {"auto_update_candidate", "review_only", "blocked", "no_change_confirmed"}
            and change.get("policy_version")
            and change.get("evidence_hash")
            and isinstance(change.get("rollback_eligible"), bool)
            and all(obs.get("authority_tier") in {"A", "B", "C", "D"} for obs in change.get("source_observations", []))
            for change in item.get("changes", [])
        )
        for item in recommendations
    )
    has_human_review = any(item.get("recommended_action") == "human_review" for item in recommendations)
    invalid_npis = [str(item.get("npi", "")) for item in recommendations if not valid_npi(item.get("npi", ""))]
    has_schema_title = schema.get("title") == "ProviderDirectoryRecommendationBatch"
    record(checks, "recommendation_examples_exist", True, display_path(examples_path))
    record(checks, "recommendation_json_valid", True, display_path(examples_path))
    record(checks, "recommendation_contract_shape", valid_shape, f"recommendations={len(recommendations)}")
    record(checks, "recommendation_contract_sources", has_sources, "supporting_sources required per change")
    record(
        checks,
        "recommendation_contract_field_decisions",
        has_field_decisions,
        "field_decision, launch_state, policy_version, evidence_hash, rollback, source authority required per change",
    )
    record(checks, "recommendation_contract_human_review", has_human_review, "at least one human_review example")
    record(checks, "recommendation_contract_valid_npis", not invalid_npis, "; ".join(invalid_npis[:5]))
    record(checks, "recommendation_schema_title", has_schema_title, schema.get("title", ""))


def validate_package(checks: list[dict[str, Any]], package_path: Path) -> None:
    if not package_path.exists():
        record(checks, "package_exists", False, package_path.name)
        return
    record(checks, "package_exists", True, package_path.name)
    with zipfile.ZipFile(package_path) as archive:
        names = set(archive.namelist())
    top_level_dirs = {name.split("/", 1)[0] for name in names if "/" in name}
    prefix = next(iter(top_level_dirs)) if len(top_level_dirs) == 1 else package_path.stem.split("_", 1)[0]
    curated_mode = f"{prefix}/START_HERE.md" in names
    required_files = CURATED_PACKAGE_FILES if curated_mode else REQUIRED_PACKAGE_FILES
    record(checks, "package_curated_layout", curated_mode, "START_HERE.md present")
    for filename in required_files:
        expected = f"{prefix}/{filename}"
        record(checks, f"package_{filename}", expected in names, expected)
    private_hits = sorted(name for name in names if any(pattern in name for pattern in PRIVATE_PACKAGE_PATTERNS))
    record(checks, "package_no_private_research_artifacts", not private_hits, "; ".join(private_hits[:10]))
    secret_name_hits = sorted(name for name in names if any(pattern in name.lower() for pattern in SECRET_NAME_PATTERNS))
    secret_text_hits: list[str] = []
    with zipfile.ZipFile(package_path) as archive:
        for name in sorted(names):
            if name.endswith("/"):
                continue
            try:
                text = archive.read(name).decode("utf-8")
            except (UnicodeDecodeError, KeyError):
                continue
            if any(pattern.search(text) for pattern in SECRET_TEXT_PATTERNS):
                secret_text_hits.append(name)
    secret_hits = secret_name_hits + secret_text_hits
    record(checks, "package_no_secret_like_artifacts", not secret_hits, "; ".join(secret_hits[:10]))
    if curated_mode:
        validate_curated_package_text(checks, package_path, prefix)


def validate_curated_package_text(checks: list[dict[str, Any]], package_path: Path, prefix: str) -> None:
    selected_docs = [
        "START_HERE.md",
        "proposal/ONE_PAGE_SCORECARD.md",
        "proposal/JUDGE_DECISION_MEMO.md",
        "proposal/BONUS_COVERAGE_MATRIX.md",
        "proposal/PRESENTATION_NARRATIVE.md",
        "proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md",
        "proposal/SHADOW_MODE_PILOT_PROTOCOL.md",
        "proposal/AGENT_WORKFLOW_DIAGRAM.md",
        "proposal/ARCHITECTURE_DIAGRAM.md",
        "proposal/CONFIDENCE_AND_DECISION_POLICY.md",
        "proposal/SOURCE_ACCESS_COMPLIANCE_POLICY.md",
        "proposal/OFFICIAL_SOURCE_REFERENCES.md",
        "prototype/WORKING_PROTOTYPE.md",
        "prototype/RECOMMENDATION_API_CONTRACT.md",
    ]
    forbidden = ["COMBINED_ABC_PIPELINE_COVERAGE.md", "ONE_PAGE_JUDGE_GUIDE.md", "scripts/verify_pipeline.py"]
    required_terms = {
        "START_HERE.md": ["90-Second Read", "Five-Minute Judge Path", "self-contained unzip-and-run MVP smoke test passes"],
        "proposal/ONE_PAGE_SCORECARD.md": [
            "Competition Criteria",
            "Bonus Coverage",
            "evidence-only cost per correct update",
            "The Judge Decision In One Sentence",
        ],
        "proposal/JUDGE_DECISION_MEMO.md": [
            "Monday-Morning Implementation Plan",
            "What Would Make This Unsafe",
            "Judge Objection Handling",
        ],
        "proposal/BONUS_COVERAGE_MATRIX.md": ["Bonus Evidence", "Confidence scoring formula"],
        "proposal/PRESENTATION_NARRATIVE.md": ["Three-Minute Talk Track", "Closing Ask"],
        "proposal/CONFIDENCE_AND_DECISION_POLICY.md": ["Confidence Formula", "Auto-Update Rules", "Human Review Rules"],
        "proposal/AGENT_WORKFLOW_DIAGRAM.md": ["Agent Responsibilities", "Safety And Policy Gates", "Render-Free Diagram", "safetyClass"],
        "proposal/ARCHITECTURE_DIAGRAM.md": ["Render-Free Diagram", "LLM extraction is a gated fallback"],
        "proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md": ["Confidence And Decision Law", "Cloud-Agnostic Production Plan"],
        "prototype/WORKING_PROTOTYPE.md": ["Deterministic Reproduction Check"],
        "prototype/RECOMMENDATION_API_CONTRACT.md": ["recommended_action", "audit_required"],
        "proposal/SHADOW_MODE_PILOT_PROTOCOL.md": [
            "Shadow-Mode Pilot Protocol",
            "No-Write Pilot Law",
            "Daily Reviewer Disposition Loop",
            "Go/No-Go Gates",
            "Field-Level Launch Decision",
        ],
        "proposal/SOURCE_ACCESS_COMPLIANCE_POLICY.md": ["Source Access Law", "Connector Admission Checklist"],
        "proposal/OFFICIAL_SOURCE_REFERENCES.md": ["Reference Map", "Design Implications", "Current Verification Snapshot"],
    }
    with zipfile.ZipFile(package_path) as archive:
        legacy_hits: list[str] = []
        for doc in selected_docs:
            name = f"{prefix}/{doc}"
            try:
                text = archive.read(name).decode("utf-8")
            except KeyError:
                continue
            for pattern in forbidden:
                if pattern in text:
                    legacy_hits.append(f"{doc}:{pattern}")
            for term in required_terms.get(doc, []):
                record(checks, f"package_text_{doc}_{term}", term in text, term)
        try:
            metrics = json.loads(archive.read(f"{prefix}/prototype/metrics.json").decode("utf-8"))
            dashboard = archive.read(f"{prefix}/dashboard/index.html").decode("utf-8")
            match = re.search(r"const data = (\{.*?\});\n\s+const views", dashboard, flags=re.S)
            dashboard_metrics = json.loads(match.group(1))["metrics"] if match else {}
            metric_keys = ["f1", "precision", "recall", "auto_apply_precision", "cost_per_correct_update_usd"]
            consistent = all(dashboard_metrics.get(key) == metrics.get(key) for key in metric_keys)
            detail = ", ".join(f"{key}={dashboard_metrics.get(key)}" for key in metric_keys)
            record(checks, "package_dashboard_metrics_match_prototype", consistent, detail)
            has_reviewer_actions = all(term in dashboard for term in ["data-review-action=\"accept\"", "data-review-action=\"reject\"", "data-review-action=\"recrawl\""])
            record(checks, "package_dashboard_reviewer_actions", has_reviewer_actions, "accept/reject/recrawl controls")
            has_review_sources = all(
                term in dashboard
                for term in [
                    "<th>sources</th>",
                    "<th>evidence_urls</th>",
                    "https://example.org/",
                    "Synthetic benchmark data",
                    "Launch Gates",
                    "auto_update_candidate",
                ]
            )
            record(
                checks,
                "package_dashboard_review_sources",
                has_review_sources,
                "review table includes source, URL, prototype provenance, and launch gates",
            )
        except (KeyError, json.JSONDecodeError, TypeError, AttributeError) as exc:
            record(checks, "package_dashboard_metrics_match_prototype", False, str(exc))
        try:
            auto_text = archive.read(f"{prefix}/prototype/auto_apply_updates.csv").decode("utf-8")
            auto_rows = list(csv.DictReader(auto_text.splitlines()))
            violations = auto_apply_policy_violations(auto_rows)
            record(
                checks,
                "package_safe_auto_apply_policy",
                not violations,
                f"rows={len(auto_rows)}, violations={'; '.join(violations[:5])}",
            )
        except KeyError as exc:
            record(checks, "package_safe_auto_apply_policy", False, str(exc))
        try:
            providers_text = archive.read(f"{prefix}/data/sample/providers.csv").decode("utf-8")
            providers = list(csv.DictReader(providers_text.splitlines()))
            invalid = [row.get("npi", "") for row in providers if not valid_npi(row.get("npi", ""))]
            record(checks, "package_sample_npi_validity", not invalid, "; ".join(invalid[:5]))
        except KeyError as exc:
            record(checks, "package_sample_npi_validity", False, str(exc))
        try:
            metrics = json.loads(archive.read(f"{prefix}/prototype/metrics.json").decode("utf-8"))
            review_rows = list(csv.DictReader(archive.read(f"{prefix}/prototype/review_queue.csv").decode("utf-8").splitlines()))
            field_counts: dict[str, int] = {}
            for row in review_rows:
                field_counts[row.get("field", "")] = field_counts.get(row.get("field", ""), 0) + 1
            expected_terms = [
                "candidate",
                "auto",
                "human review",
            ]
            dashboard_text = archive.read(f"{prefix}/dashboard/index.html").decode("utf-8").lower()
            missing = [term for term in expected_terms if term not in dashboard_text]
            has_all_fields = all(field.lower() in dashboard_text for field in field_counts)
            record(checks, "package_dashboard_matches_outputs", not missing and has_all_fields, "; ".join(missing[:8]))
        except (KeyError, json.JSONDecodeError) as exc:
            record(checks, "package_dashboard_matches_outputs", False, str(exc))
        try:
            cost_md = archive.read(f"{prefix}/appendix/COST_MODEL.md").decode("utf-8")
            cost_csv = archive.read(f"{prefix}/evidence/cost_model_per_1000.csv").decode("utf-8")
            md_rows = cost_model_markdown_rows(cost_md)
            csv_rows = {row["scenario"]: row for row in csv.DictReader(cost_csv.splitlines())}
            mismatches = []
            for scenario, csv_row in csv_rows.items():
                md_row = md_rows.get(scenario)
                if not md_row:
                    mismatches.append(f"{scenario}: missing markdown row")
                    continue
                for csv_key, md_key in [
                    ("evidence_usd", "evidence_usd"),
                    ("aws_compute_storage_monitoring_usd", "aws_compute_storage_monitoring_usd"),
                    ("llm_extraction_usd", "llm_extraction_usd"),
                    ("manual_review_usd", "manual_review_usd"),
                    ("manual_review_items", "manual_review_items"),
                    ("total_usd", "total_usd"),
                ]:
                    if round(float(csv_row[csv_key]), 2) != round(float(md_row[md_key]), 2):
                        mismatches.append(f"{scenario}:{csv_key}")
            record(
                checks,
                "package_cost_model_markdown_matches_csv",
                not mismatches,
                "; ".join(mismatches[:8]),
            )
            total_mismatches = []
            cost_components = [
                "evidence_usd",
                "aws_compute_storage_monitoring_usd",
                "llm_extraction_usd",
                "manual_review_usd",
            ]
            for scenario, csv_row in csv_rows.items():
                expected_total = sum(float(csv_row[key]) for key in cost_components)
                reported_total = float(csv_row["total_usd"])
                if round(expected_total, 2) != round(reported_total, 2):
                    total_mismatches.append(
                        f"{scenario}: expected {expected_total:.2f} got {reported_total:.2f}"
                    )
            record(
                checks,
                "package_cost_model_totals_add_up",
                not total_mismatches,
                "; ".join(total_mismatches[:8]),
            )
            metric_boundary = (
                "evidence acquisition cost per true-positive recommendation" in cost_md
                and "does not include human labor" in cost_md
                and "manual-review labor" in cost_md
            )
            record(checks, "package_cost_model_metric_boundary", metric_boundary, "prototype evidence cost vs review labor")
        except (KeyError, ValueError) as exc:
            record(checks, "package_cost_model_markdown_matches_csv", False, str(exc))
        try:
            notebook_text = archive.read(f"{prefix}/Provider_Directory_Update_Pipeline_End_to_End.ipynb").decode("utf-8")
            notebook_portable = (
                "submissions/" not in notebook_text
                and "evidence/audit_events.jsonl" in notebook_text
                and "Production Handoff" in notebook_text
                and notebook_text.count("audit_path = ROOT / 'evidence/audit_events.jsonl'") == 1
            )
            record(checks, "package_notebook_uses_curated_paths", notebook_portable, "evidence/audit_events.jsonl + Production Handoff")
        except KeyError as exc:
            record(checks, "package_notebook_uses_curated_paths", False, str(exc))
        try:
            verification = json.loads(archive.read(f"{prefix}/evidence/verification.json").decode("utf-8"))
            rubric = archive.read(f"{prefix}/evidence/judge_rubric_self_eval.csv").decode("utf-8")
            expected = f"{len(verification.get('checks', []))} curated-package checks passed={verification.get('passed')}"
            record(checks, "package_rubric_verification_claim_matches", expected in rubric, expected)
        except (KeyError, json.JSONDecodeError) as exc:
            record(checks, "package_rubric_verification_claim_matches", False, str(exc))
    record(checks, "package_no_legacy_doc_references", not legacy_hits, "; ".join(legacy_hits[:10]))


def run_package_self_contained_smoke(checks: list[dict[str, Any]], package_path: Path, out_dir: Path) -> None:
    if not package_path.exists():
        record(checks, "package_self_contained_smoke", False, str(package_path))
        return
    extract_dir = out_dir / "package_self_contained"
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(package_path) as archive:
        archive.extractall(extract_dir)
    package_roots = [path for path in extract_dir.iterdir() if path.is_dir()]
    if len(package_roots) != 1:
        record(checks, "package_self_contained_smoke", False, f"roots={len(package_roots)}")
        return
    package_root = package_roots[0]
    proc = subprocess.run(
        [sys.executable, "scripts/run_best_pipeline.py", "--out-dir", "outputs/package_smoke"],
        cwd=package_root,
        text=True,
        capture_output=True,
        check=False,
    )
    metrics_path = package_root / "outputs/package_smoke/metrics.json"
    if proc.returncode != 0 or not metrics_path.exists():
        record(checks, "package_self_contained_smoke", False, (proc.stderr or proc.stdout)[-500:])
        return
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    passed = metrics.get("f1", 0) >= 0.90 and metrics.get("auto_apply_precision", 0) >= 0.95
    detail = f"f1={metrics.get('f1')}, auto_precision={metrics.get('auto_apply_precision')}"
    record(checks, "package_self_contained_smoke", passed, detail)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify provider directory pipeline artifacts.")
    parser.add_argument("--out-dir", default="outputs/verify_pipeline", help="Directory for verification outputs.")
    parser.add_argument(
        "--package",
        default="submissions/latest_final_package.zip",
        help="Submission package zip to validate.",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    checks: list[dict[str, Any]] = []
    compile_project(checks)
    smoke = run_smoke_cv(checks)
    cli_metrics = run_cli(checks, out_dir / "cli")
    run_public_dataset_cli_smoke(checks, out_dir)
    validate_sample_npis(checks)
    validate_docs(checks)
    validate_notebook(checks)
    validate_recommendation_contract(checks)
    validate_package(checks, Path(args.package))
    run_package_self_contained_smoke(checks, Path(args.package), out_dir)

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
