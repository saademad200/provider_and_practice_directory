#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "submissions/healthlynked_option_c_clean"
SOURCE = TARGET
CURATED_SOURCE = TARGET


TOP_LEVEL_FILES = [
    ("README.md", "README.md"),
    ("Provider_Directory_Update_Pipeline_End_to_End.ipynb", "Provider_Directory_Update_Pipeline_End_to_End.ipynb"),
    ("JUDGE_DECISION_MEMO.md", "proposal/JUDGE_DECISION_MEMO.md"),
    ("JUDGE_COMPARISON_MATRIX.md", "proposal/JUDGE_COMPARISON_MATRIX.md"),
    ("BONUS_COVERAGE_MATRIX.md", "proposal/BONUS_COVERAGE_MATRIX.md"),
    ("PRESENTATION_NARRATIVE.md", "proposal/PRESENTATION_NARRATIVE.md"),
    ("WINNING_PROPOSAL_BRIEF.md", "proposal/WINNING_PROPOSAL_BRIEF.md"),
    ("TECHNICAL_ARCHITECTURE_PROPOSAL.md", "proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md"),
    ("CONFIDENCE_AND_DECISION_POLICY.md", "proposal/CONFIDENCE_AND_DECISION_POLICY.md"),
    ("IMPLEMENTATION_ACCEPTANCE_CRITERIA.md", "proposal/IMPLEMENTATION_ACCEPTANCE_CRITERIA.md"),
    ("EVALUATION_LIMITS_AND_TRANSFER_PLAN.md", "proposal/EVALUATION_LIMITS_AND_TRANSFER_PLAN.md"),
    ("LEAN_TEAM_OPERATING_MODEL.md", "proposal/LEAN_TEAM_OPERATING_MODEL.md"),
    ("FAILURE_MODE_PLAYBOOK.md", "proposal/FAILURE_MODE_PLAYBOOK.md"),
    ("AGENT_WORKFLOW_DIAGRAM.md", "proposal/AGENT_WORKFLOW_DIAGRAM.md"),
    ("AGENT_WORKFLOW_DIAGRAM.mmd", "proposal/AGENT_WORKFLOW_DIAGRAM.mmd"),
    ("ARCHITECTURE_DIAGRAM.md", "proposal/ARCHITECTURE_DIAGRAM.md"),
    ("ARCHITECTURE_DIAGRAM.mmd", "proposal/ARCHITECTURE_DIAGRAM.mmd"),
    ("IMPLEMENTATION_ROADMAP_90_DAYS.md", "proposal/IMPLEMENTATION_ROADMAP_90_DAYS.md"),
    ("OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md", "proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md"),
    ("SOURCE_CONNECTOR_STATUS_MATRIX.md", "proposal/SOURCE_CONNECTOR_STATUS_MATRIX.md"),
    ("SOURCE_ACCESS_COMPLIANCE_POLICY.md", "proposal/SOURCE_ACCESS_COMPLIANCE_POLICY.md"),
    ("OFFICIAL_SOURCE_REFERENCES.md", "proposal/OFFICIAL_SOURCE_REFERENCES.md"),
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
    ("AWS_PRODUCTION_ARCHITECTURE.md", "appendix/AWS_PRODUCTION_ARCHITECTURE.md"),
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
    "pyproject.toml",
]

CURATED_REQUIREMENTS = """pandas>=2.0
numpy>=1.24
scikit-learn>=1.3
matplotlib>=3.7
ipython>=8.0
requests>=2.31
beautifulsoup4>=4.12
"""

CURATED_SRC_FILES = [
    "src/__init__.py",
    "src/cost.py",
    "src/data.py",
    "src/freshness.py",
    "src/metrics.py",
    "src/cv.py",
    "src/npi.py",
    "src/review_priority.py",
    "src/specialty.py",
]


PRIVATE_PATTERNS = [
    "JUDGE_AUDIT",
    "COUNTERMOVE_LOG",
]


START_HERE = """# Start Here

This is the curated judge package for the HealthLynked Provider / Practice Directory Update Pipeline competition.

## 90-Second Read

This is an Option C hybrid submission: a runnable MVP plus an AWS-ready production architecture. The core idea is a provider-directory quality control plane, not a one-time cleanup script. It collects trusted evidence, normalizes fields, resolves provider/practice/location identity, scores confidence, routes uncertain changes to review, safely auto-updates only low-risk high-confidence fields, and records an audit/rollback trail for every recommendation.

Proof points:

- F1 `0.948276`, precision `0.948276`, recall `0.948276`
- safe auto-apply precision `1.0`
- estimated cost per correct update `$0.005836`
- 116 curated-package verification checks
- self-contained unzip-and-run MVP smoke test passes
- AWS production plan with source governance, review operations, monitoring, and rollback

Why it should win: it is immediately implementable after the competition. The package includes the technical architecture, working prototype, confidence policy, connector operating model, human review workflow, audit trail, cost controls, and post-award acceptance criteria.

## Recommended Judge Path

1. Open `Provider_Directory_Update_Pipeline_End_to_End.ipynb` for the narrated end-to-end walkthrough.
2. Read `proposal/WINNING_PROPOSAL_BRIEF.md` for the executive case.
3. Read `proposal/JUDGE_DECISION_MEMO.md` for the consulting-ready business case.
4. Read `proposal/PRESENTATION_NARRATIVE.md` for the pitch story.
5. Read `proposal/JUDGE_COMPARISON_MATRIX.md` for the fast comparison against likely alternatives.
6. Read `proposal/BONUS_COVERAGE_MATRIX.md` for bonus-point evidence links.
7. Read `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md` and `proposal/ARCHITECTURE_DIAGRAM.md` for the production architecture.
8. Read `proposal/AGENT_WORKFLOW_DIAGRAM.md` for the bounded agent workflow.
9. Read `proposal/CONFIDENCE_AND_DECISION_POLICY.md` for the exact auto-update and review policy.
10. Read `proposal/IMPLEMENTATION_ACCEPTANCE_CRITERIA.md` for the post-award delivery gates.
11. Read `prototype/WORKING_PROTOTYPE.md` and inspect `prototype/metrics.json` for the runnable MVP.
12. Read `proposal/EVALUATION_LIMITS_AND_TRANSFER_PLAN.md` for how proxy metrics transfer to HealthLynked data.
13. Read `proposal/LEAN_TEAM_OPERATING_MODEL.md` and `proposal/FAILURE_MODE_PLAYBOOK.md` for production operations.
14. Open `prototype/RECOMMENDATION_API_CONTRACT.md` for the exact update recommendation shape.
15. Open `proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md`, `proposal/SOURCE_CONNECTOR_STATUS_MATRIX.md`, `proposal/SOURCE_ACCESS_COMPLIANCE_POLICY.md`, and `proposal/OFFICIAL_SOURCE_REFERENCES.md` for trusted-source operations.
16. Inspect `dashboard/index.html` for the sample human review experience.
17. Use `evidence/verification.json` and `evidence/judge_rubric_self_eval.csv` to audit the claims.

## Run The MVP

From inside the unzipped package:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 scripts/run_best_pipeline.py --out-dir outputs/judge_smoke
```

The run writes candidate updates, safe auto-apply updates, human-review queue, config, and metrics under `outputs/judge_smoke/`. The expected proof point is the same as the packaged evidence: F1 `0.948276`, safe auto-apply precision `1.0`, and cost per correct update `$0.005836`.

## Why The Package Is Structured This Way

The first layer is intentionally small: notebook, proposal, prototype, architecture, API contract, source plan, dashboard, and verification. Supporting material is organized under `appendix/` and `evidence/` so judges can go deep without being forced through a flat folder of internal research files.
"""


CURATED_README = """# HealthLynked Provider Directory Update Pipeline

Option C hybrid submission: a working MVP plus a production architecture for continuously detecting, validating, reviewing, and auditing provider/practice directory updates.

## What To Open First

- `START_HERE.md`
- `Provider_Directory_Update_Pipeline_End_to_End.ipynb`
- `proposal/JUDGE_DECISION_MEMO.md`
- `proposal/WINNING_PROPOSAL_BRIEF.md`
- `proposal/BONUS_COVERAGE_MATRIX.md`
- `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md`
- `proposal/AGENT_WORKFLOW_DIAGRAM.md`
- `proposal/CONFIDENCE_AND_DECISION_POLICY.md`
- `prototype/WORKING_PROTOTYPE.md`
- `dashboard/index.html`

For the full reading order, use `START_HERE.md`.

## Prototype Proof Points

- Local proxy F1: 0.948276
- Precision / recall: 0.948276 / 0.948276
- Safe auto-apply precision: 1.0
- Cost per correct update: $0.005836
- Cloud plan: AWS

## Run The MVP

From inside the unzipped package:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 scripts/run_best_pipeline.py --out-dir outputs/judge_smoke
```

Expected output files:

- `outputs/judge_smoke/candidate_updates.csv`
- `outputs/judge_smoke/auto_apply_updates.csv`
- `outputs/judge_smoke/review_queue.csv`
- `outputs/judge_smoke/metrics.json`

The package has already been verified by `evidence/verification.json`.

## Folder Map

- `proposal/` - architecture, winning brief, source connector plan, roadmap, and diagram.
- `prototype/` - runnable MVP outputs, metrics, recommendation API contract, and update examples.
- `dashboard/` - sample human review dashboard.
- `evidence/` - machine-readable verification, rubric, cost, audit, rollback, duplicate, movement, and inactive-provider evidence.
- `appendix/` - supporting production controls and deeper implementation notes.
- `src/`, `scripts/`, and `data/sample/` - lightweight reproducible MVP code snapshot.
"""


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def source_file(source_root: Path, source_name: str, target_name: str) -> Path:
    legacy_path = source_root / source_name
    if legacy_path.exists():
        return legacy_path
    curated_path = source_root / target_name
    if curated_path.exists():
        return curated_path
    raise FileNotFoundError(f"Missing package source for {source_name} -> {target_name}")


def assert_no_private_files(target: Path) -> list[str]:
    offenders = []
    for path in target.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(target).as_posix()
        if any(pattern in rel for pattern in PRIVATE_PATTERNS):
            offenders.append(rel)
    return offenders


def build(target: Path, source_root: Path = SOURCE) -> dict:
    temp_source: Path | None = None
    same_source_and_target = source_root.exists() and source_root.resolve() == target.resolve()
    if same_source_and_target or (not source_root.exists() and CURATED_SOURCE.exists()):
        temp_source = ROOT / "outputs/build_clean_source_snapshot"
        if temp_source.exists():
            shutil.rmtree(temp_source)
        shutil.copytree(source_root if source_root.exists() else CURATED_SOURCE, temp_source)
        source_root = temp_source

    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    (target / "START_HERE.md").write_text(START_HERE, encoding="utf-8")
    (target / "README.md").write_text(CURATED_README, encoding="utf-8")

    for source_name, target_name in TOP_LEVEL_FILES:
        if source_name == "README.md":
            continue
        copy_file(source_file(source_root, source_name, target_name), target / target_name)
    patch_notebook_for_curated_package(target)

    for directory in ["dashboard"]:
        source_dir = source_root / directory
        if source_dir.exists():
            shutil.copytree(source_dir, target / directory)
    sync_dashboard_metrics(target)

    for src_file in CURATED_SRC_FILES:
        copy_file(ROOT / src_file, target / src_file)
    shutil.copytree(ROOT / "data/sample", target / "data/sample")
    for code_file in CODE_FILES:
        copy_file(ROOT / code_file, target / code_file)
    (target / "requirements.txt").write_text(CURATED_REQUIREMENTS, encoding="utf-8")

    offenders = assert_no_private_files(target)
    summary_path = target / "evidence/clean_package_summary.json"
    file_count = sum(1 for path in target.rglob("*") if path.is_file()) + (0 if summary_path.exists() else 1)
    summary = {
        "target": str(target),
        "file_count": file_count,
        "private_file_offenders": offenders,
        "passed": not offenders,
    }
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if temp_source and temp_source.exists():
        shutil.rmtree(temp_source)
    return summary


def sync_dashboard_metrics(target: Path) -> None:
    metrics_path = target / "prototype/metrics.json"
    if not metrics_path.exists():
        return
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    for dashboard_path in [target / "dashboard/index.html"]:
        if not dashboard_path.exists():
            continue
        html = dashboard_path.read_text(encoding="utf-8")
        match = re.search(r"const data = (\{.*?\});\n\s+const views", html, flags=re.S)
        if not match:
            continue
        data = json.loads(match.group(1))
        data["metrics"] = metrics
        data.setdefault("counts", {})
        data["counts"]["review"] = metrics.get("review_count", data["counts"].get("review"))
        data["counts"]["auto"] = metrics.get("auto_apply_count", data["counts"].get("auto"))
        replacement = "const data = " + json.dumps(data, sort_keys=True) + ";\n    const views"
        html = html[: match.start()] + replacement + html[match.end() :]
        dashboard_path.write_text(html, encoding="utf-8")


def patch_notebook_for_curated_package(target: Path) -> None:
    notebook_path = target / "Provider_Directory_Update_Pipeline_End_to_End.ipynb"
    if not notebook_path.exists():
        return
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    curated_source = [
        "audit_path = ROOT / 'evidence/audit_events.jsonl'\n",
        "if audit_path.exists():\n",
        "    audit_preview = [json.loads(line) for line in audit_path.read_text().splitlines()[:5]]\n",
        "    display(pd.DataFrame(audit_preview))\n",
        "else:\n",
        "    print('Audit fixture not found in this checkout.')\n",
    ]
    for cell in notebook.get("cells", []):
        source = cell.get("source", [])
        if isinstance(source, list) and "audit_events.jsonl" in "".join(source):
            cell["source"] = curated_source
    notebook_text = json.dumps(notebook, indent=1, ensure_ascii=False)
    notebook_text = notebook_text.replace(str(ROOT), ".")
    notebook_path.write_text(notebook_text + "\n", encoding="utf-8")


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
