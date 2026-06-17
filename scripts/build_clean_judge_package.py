#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "submissions/exp0172"
TARGET = ROOT / "submissions/healthlynked_option_c_clean"


TOP_LEVEL_FILES = [
    ("README.md", "README.md"),
    ("Provider_Directory_Update_Pipeline_End_to_End.ipynb", "Provider_Directory_Update_Pipeline_End_to_End.ipynb"),
    ("WINNING_PROPOSAL_BRIEF.md", "proposal/WINNING_PROPOSAL_BRIEF.md"),
    ("TECHNICAL_ARCHITECTURE_PROPOSAL.md", "proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md"),
    ("ARCHITECTURE_DIAGRAM.md", "proposal/ARCHITECTURE_DIAGRAM.md"),
    ("ARCHITECTURE_DIAGRAM.mmd", "proposal/ARCHITECTURE_DIAGRAM.mmd"),
    ("IMPLEMENTATION_ROADMAP_90_DAYS.md", "proposal/IMPLEMENTATION_ROADMAP_90_DAYS.md"),
    ("OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md", "proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md"),
    ("WORKING_PROTOTYPE.md", "prototype/WORKING_PROTOTYPE.md"),
    ("RECOMMENDATION_API_CONTRACT.md", "prototype/RECOMMENDATION_API_CONTRACT.md"),
    ("metrics.json", "prototype/metrics.json"),
    ("candidate_updates.csv", "prototype/candidate_updates.csv"),
    ("auto_apply_updates.csv", "prototype/auto_apply_updates.csv"),
    ("review_queue.csv", "prototype/review_queue.csv"),
    ("recommendation_api_examples.json", "prototype/recommendation_api_examples.json"),
    ("recommendation_api_schema.json", "prototype/recommendation_api_schema.json"),
    ("cost_model_per_1000.csv", "evidence/cost_model_per_1000.csv"),
    ("source_connector_registry.csv", "evidence/source_connector_registry.csv"),
    ("duplicate_candidates.csv", "evidence/duplicate_candidates.csv"),
    ("provider_movement_candidates.csv", "evidence/provider_movement_candidates.csv"),
    ("inactive_provider_candidates.csv", "evidence/inactive_provider_candidates.csv"),
    ("audit_events.jsonl", "evidence/audit_events.jsonl"),
    ("rollback_plan.csv", "evidence/rollback_plan.csv"),
    ("production_readiness_summary.json", "evidence/production_readiness_summary.json"),
    ("judge_rubric_self_eval.csv", "evidence/judge_rubric_self_eval.csv"),
    ("verification.json", "evidence/verification.json"),
    ("COST_MODEL.md", "appendix/COST_MODEL.md"),
    ("DASHBOARD_SPEC.md", "appendix/DASHBOARD_SPEC.md"),
    ("DUPLICATE_MOVEMENT_DETECTION.md", "appendix/DUPLICATE_MOVEMENT_DETECTION.md"),
    ("INACTIVE_PROVIDER_DETECTION.md", "appendix/INACTIVE_PROVIDER_DETECTION.md"),
    ("AUDIT_ROLLBACK_WORKFLOW.md", "appendix/AUDIT_ROLLBACK_WORKFLOW.md"),
    ("SOURCE_CONFLICT_ADJUDICATION.md", "appendix/SOURCE_CONFLICT_ADJUDICATION.md"),
    ("SOURCE_GOVERNANCE_CHECKLIST.md", "appendix/SOURCE_GOVERNANCE_CHECKLIST.md"),
    ("SYNTHETIC_VOLUME_BENCHMARK.md", "appendix/SYNTHETIC_VOLUME_BENCHMARK.md"),
    ("PRODUCTION_READINESS_SCORECARD.md", "appendix/PRODUCTION_READINESS_SCORECARD.md"),
    ("PRIVACY_COMPLIANCE_MODEL.md", "appendix/PRIVACY_COMPLIANCE_MODEL.md"),
]


CODE_FILES = [
    "scripts/run_best_pipeline.py",
    "scripts/verify_pipeline.py",
    "requirements.txt",
    "pyproject.toml",
]


PRIVATE_PATTERNS = [
    "JUDGE_AUDIT",
    "COUNTERMOVE_LOG",
    "MILESTONE_100_NORTH_STAR_AUDIT",
]


START_HERE = """# Start Here

This is the curated judge package for the HealthLynked Provider / Practice Directory Update Pipeline competition.

## Recommended Judge Path

1. Open `Provider_Directory_Update_Pipeline_End_to_End.ipynb` for the narrated end-to-end walkthrough.
2. Read `proposal/WINNING_PROPOSAL_BRIEF.md` for the executive case.
3. Read `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md` and `proposal/ARCHITECTURE_DIAGRAM.md` for the production architecture.
4. Read `prototype/WORKING_PROTOTYPE.md` and inspect `prototype/metrics.json` for the runnable MVP.
5. Open `prototype/RECOMMENDATION_API_CONTRACT.md` for the exact update recommendation shape.
6. Open `proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md` for the trusted-source ingestion plan.
7. Inspect `dashboard/index.html` for the sample human review experience.
8. Use `evidence/verification.json` and `evidence/judge_rubric_self_eval.csv` to audit the claims.

## Why The Package Is Structured This Way

The first layer is intentionally small: notebook, proposal, prototype, architecture, API contract, source plan, dashboard, and verification. Supporting material is organized under `appendix/` and `evidence/` so judges can go deep without being forced through a flat folder of internal research files.
"""


CURATED_README = """# HealthLynked Provider Directory Update Pipeline

Option C hybrid submission: a working MVP plus a production architecture for continuously detecting, validating, reviewing, and auditing provider/practice directory updates.

## What To Open First

- `START_HERE.md`
- `Provider_Directory_Update_Pipeline_End_to_End.ipynb`
- `proposal/WINNING_PROPOSAL_BRIEF.md`
- `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md`
- `prototype/WORKING_PROTOTYPE.md`
- `dashboard/index.html`

## Prototype Proof Points

- Local proxy F1: 0.948276
- Precision / recall: 0.948276 / 0.948276
- Safe auto-apply precision: 1.0
- Cost per correct update: $0.005836
- Cloud plan: AWS

## Folder Map

- `proposal/` - architecture, winning brief, source connector plan, roadmap, and diagram.
- `prototype/` - runnable MVP outputs, metrics, recommendation API contract, and update examples.
- `dashboard/` - sample human review dashboard.
- `evidence/` - machine-readable verification, rubric, cost, audit, rollback, duplicate, movement, and inactive-provider evidence.
- `appendix/` - supporting production controls and deeper implementation notes.
- `src/` and `scripts/` - lightweight reproducible code snapshot.
"""


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def assert_no_private_files(target: Path) -> list[str]:
    offenders = []
    for path in target.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(target).as_posix()
        if any(pattern in rel for pattern in PRIVATE_PATTERNS):
            offenders.append(rel)
    return offenders


def build(target: Path) -> dict:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    (target / "START_HERE.md").write_text(START_HERE, encoding="utf-8")
    (target / "README.md").write_text(CURATED_README, encoding="utf-8")

    for source_name, target_name in TOP_LEVEL_FILES:
        if source_name == "README.md":
            continue
        copy_file(SOURCE / source_name, target / target_name)

    for directory in ["dashboard", "dashboard_v2"]:
        source_dir = SOURCE / directory
        if source_dir.exists():
            shutil.copytree(source_dir, target / directory)

    shutil.copytree(ROOT / "src", target / "src", ignore=shutil.ignore_patterns("__pycache__"))
    for code_file in CODE_FILES:
        copy_file(ROOT / code_file, target / code_file)

    offenders = assert_no_private_files(target)
    file_count = sum(1 for path in target.rglob("*") if path.is_file())
    summary = {
        "target": str(target),
        "file_count": file_count,
        "private_file_offenders": offenders,
        "passed": not offenders,
    }
    (target / "evidence/clean_package_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def zip_dir(target: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(target.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(target.parent))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the curated judge-facing package.")
    parser.add_argument("--target", default=str(TARGET))
    parser.add_argument("--zip", default=str(ROOT / "submissions/latest_final_package.zip"))
    args = parser.parse_args()

    target = Path(args.target)
    summary = build(target)
    zip_path = Path(args.zip)
    zip_dir(target, zip_path)
    companion = zip_path.with_name("healthlynked_option_c_clean.zip")
    if companion != zip_path:
        shutil.copy2(zip_path, companion)
    print(json.dumps({**summary, "zip": str(zip_path)}, indent=2, sort_keys=True))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
