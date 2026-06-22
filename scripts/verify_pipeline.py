#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "START_HERE.md",
    "README.md",
    "KAGGLE_SUBMISSION_TEXT.md",
    "FINAL_UPLOAD_INSTRUCTIONS.md",
    "HealthLynked_Provider_Directory_Update_Pipeline.ipynb",
    "assets/architecture_diagram.png",
    "assets/agent_workflow_diagram.png",
    "assets/human_review_dashboard_mock.png",
    "assets/source_governance_matrix.md",
    "assets/confidence_scoring_formula.md",
    "assets/cost_model_per_1000_records.md",
    "assets/launch_gates_matrix.md",
    "assets/sample_recommendations.json",
    "assets/sample_human_review_queue.json",
    "assets/sample_audit_and_rollback.json",
    "prototype/metrics.json",
    "dashboard/index.html",
    "proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md",
    "proposal/CONFIDENCE_AND_DECISION_POLICY.md",
    "proposal/IMPLEMENTATION_ROADMAP_90_DAYS.md",
    "appendix/CLOUD_AGNOSTIC_PRODUCTION_ARCHITECTURE.md",
]

FORBIDDEN_PATTERNS = [
    "submissions/latest_final_package.zip",
    "latest_final_package.zip",
    "verify_no_hype",
    "can be added later",
    "TODO",
    "TBD",
]


def add(checks: list[dict], name: str, passed: bool, detail: str = "") -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


def read_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def is_generated_or_hidden(path: Path) -> bool:
    parts = set(path.relative_to(ROOT).parts)
    return bool(parts & {"outputs", "results", ".git", ".pytest_cache", "__pycache__"})


def main() -> int:
    checks: list[dict] = []

    for rel in REQUIRED_FILES:
        add(checks, f"required_file_{rel}", (ROOT / rel).exists(), rel)

    # Run pipeline and compare metrics.
    out_dir = ROOT / "outputs" / "verify_final"
    out_dir.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [sys.executable, "scripts/run_best_pipeline.py", "--out-dir", str(out_dir)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=90,
    )
    add(checks, "cli_exit", proc.returncode == 0, proc.stderr[-1000:])
    metrics = json.loads((out_dir / "metrics.json").read_text())
    expected = {
        "f1": 0.948276,
        "precision": 0.948276,
        "recall": 0.948276,
        "auto_apply_precision": 1.0,
        "auto_apply_count": 3,
        "review_count": 55,
        "predicted_updates": 58,
        "gold_updates": 58,
    }
    for key, value in expected.items():
        add(checks, f"metric_{key}", metrics.get(key) == value, f"actual={metrics.get(key)} expected={value}")

    # Sample assets align with metrics.
    recs = read_json("assets/sample_recommendations.json")
    add(checks, "sample_metrics_align", recs["metrics_snapshot"]["f1"] == metrics["f1"], "sample_recommendations")
    add(checks, "sample_has_auto_and_review", any(r["recommended_action"] == "auto_update" for r in recs["recommendations"]) and any(r["recommended_action"] == "human_review" for r in recs["recommendations"]), "recommendation mix")
    for rec in recs["recommendations"]:
        for change in rec["changes"]:
            add(checks, "recommendation_change_has_sources", bool(change.get("supporting_sources")), rec["provider_id"])
            add(checks, "recommendation_change_has_audit_hash", bool(change.get("evidence_hash")), rec["provider_id"])

    audit = read_json("assets/sample_audit_and_rollback.json")
    add(checks, "audit_has_rollback", "rollback_plan" in audit and "audit_event" in audit, "audit sample")

    # Image dimensions.
    for rel in ["assets/architecture_diagram.png", "assets/agent_workflow_diagram.png", "assets/human_review_dashboard_mock.png"]:
        im = Image.open(ROOT / rel)
        add(checks, f"image_size_{rel}", im.width >= 1500 and im.height >= 900, f"{im.width}x{im.height}")

    # No nested zip dependency.
    zips = [p for p in ROOT.rglob("*.zip") if not is_generated_or_hidden(p)]
    add(checks, "no_nested_zip_files", len(zips) == 0, ", ".join(str(p.relative_to(ROOT)) for p in zips))

    # Forbidden stale references.
    bad_hits = []
    for path in ROOT.rglob("*"):
        if is_generated_or_hidden(path):
            continue
        if path.relative_to(ROOT).as_posix() == "evidence/verification.json":
            continue
        if path.is_file() and path.name != "verify_pipeline.py" and path.suffix.lower() in {".md", ".txt", ".json", ".csv", ".py"}:
            txt = path.read_text(encoding="utf-8", errors="ignore")
            for pat in FORBIDDEN_PATTERNS:
                if pat in txt and path.name != "PACKAGE_VERIFICATION_REPORT.md":
                    bad_hits.append(f"{path.relative_to(ROOT)}::{pat}")
    add(checks, "no_stale_or_placeholder_refs", not bad_hits, " | ".join(bad_hits[:20]))

    # Pytest.
    proc_test = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)
    add(checks, "pytest", proc_test.returncode == 0, (proc_test.stdout + proc_test.stderr)[-2000:])

    passed = all(c["passed"] for c in checks)
    report = {"passed": passed, "checks": checks, "metrics": metrics}
    evidence_dir = ROOT / "evidence"
    evidence_dir.mkdir(exist_ok=True)
    (evidence_dir / "verification.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"passed": passed, "checks": len(checks), "metrics": metrics}, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
