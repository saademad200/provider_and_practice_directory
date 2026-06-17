from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


RUBRIC = [
    {
        "criterion": "accuracy",
        "weight": 16,
        "evidence": ["cv_metrics.json", "per_field.csv", "worst_providers.csv", "BENCHMARK_DATASHEET.md"],
        "metric_checks": {"f1": 0.93, "auto_apply_precision": 0.99},
        "why_it_matters": "Judges need evidence that proposed updates are correct and risky updates are not auto-applied.",
    },
    {
        "criterion": "scalability",
        "weight": 10,
        "evidence": ["SYNTHETIC_VOLUME_BENCHMARK.md", "synthetic_volume_benchmark.csv", "aws_step_functions_throughput_plan.csv"],
        "metric_checks": {},
        "why_it_matters": "The pipeline must scale beyond a notebook into an operational batch/update system.",
    },
    {
        "criterion": "cost_efficiency",
        "weight": 8,
        "evidence": ["COST_MODEL.md", "cost_model_per_1000.csv", "source_ablation.csv"],
        "metric_checks": {"cost_per_correct_update_usd": 0.01},
        "why_it_matters": "Provider-directory updates need affordable evidence retrieval and model fallback.",
    },
    {
        "criterion": "practicality",
        "weight": 10,
        "evidence": ["README.md", "ARCHITECTURE.md", "AWS_PRODUCTION_ARCHITECTURE.md", "CAPABILITY_PROFILES_AND_ORCHESTRATION.md"],
        "metric_checks": {},
        "why_it_matters": "The proposal should be deployable by a real HealthLynked engineering team.",
    },
    {
        "criterion": "explainability",
        "weight": 8,
        "evidence": ["candidate_updates.csv", "CASE_STUDIES.md", "source_conflict_adjudication.csv"],
        "metric_checks": {},
        "why_it_matters": "Every update should carry source, confidence, reason, and reviewer-readable context.",
    },
    {
        "criterion": "data_quality",
        "weight": 8,
        "evidence": ["SPECIALTY_NORMALIZATION.md", "DUPLICATE_MOVEMENT_DETECTION.md", "INACTIVE_PROVIDER_DETECTION.md"],
        "metric_checks": {},
        "why_it_matters": "Directory quality failures include duplicates, stale locations, specialty drift, and inactive providers.",
    },
    {
        "criterion": "source_reliability",
        "weight": 8,
        "evidence": ["SOURCE_CONNECTOR_REGISTRY.md", "source_connector_registry.csv", "SOURCE_FRESHNESS_ALERTS.md"],
        "metric_checks": {},
        "why_it_matters": "Conflicting sources need authority tiers, freshness checks, connector health, and fallback paths.",
    },
    {
        "criterion": "human_review",
        "weight": 8,
        "evidence": ["REVIEW_DISPOSITION_AND_SLA.md", "review_queue.csv", "review_disposition_contract.json"],
        "metric_checks": {"review_count": 30, "auto_apply_precision": 0.99},
        "why_it_matters": "Ambiguous or high-risk updates must be routed to reviewers, not silently applied.",
    },
    {
        "criterion": "audit_and_rollback",
        "weight": 8,
        "evidence": ["AUDIT_ROLLBACK_WORKFLOW.md", "audit_events.jsonl", "rollback_plan.csv", "PACKAGE_INTEGRITY_MANIFEST.md"],
        "metric_checks": {},
        "why_it_matters": "A production update pipeline needs traceability, rollback, and artifact integrity.",
    },
    {
        "criterion": "privacy_security",
        "weight": 6,
        "evidence": ["PRIVACY_COMPLIANCE_MODEL.md", "NO_SECRETS_SCAN.md", "agent_security_matrix.csv"],
        "metric_checks": {},
        "why_it_matters": "The system should stay within public-provider-data boundaries and avoid credential leakage.",
    },
    {
        "criterion": "agentic_innovation",
        "weight": 6,
        "evidence": ["AGENT_SKILLS_INSIGHTS.md", "PROVIDER_DIRECTORY_SKILLS_LIBRARY.md", "SKILL_LIBRARY_EVALS.md"],
        "metric_checks": {},
        "why_it_matters": "Agentic structure matters only when paired with scoped skills, evals, and explicit authority.",
    },
    {
        "criterion": "operational_verifiability",
        "weight": 4,
        "evidence": ["verification.json", "ARTIFACT_INDEX.md", "artifact_index.csv"],
        "metric_checks": {},
        "why_it_matters": "Judges should be able to inspect and trust the package quickly.",
    },
]


def evaluate_package(package_dir: Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    metrics = load_metrics(package_dir)
    rows: list[dict[str, Any]] = []
    for item in RUBRIC:
        present = [name for name in item["evidence"] if (package_dir / name).exists()]
        missing = [name for name in item["evidence"] if not (package_dir / name).exists()]
        evidence_score = len(present) / len(item["evidence"])
        metric_score, metric_detail = metric_check_score(metrics, item["metric_checks"])
        raw_score = round(5.0 * min(evidence_score, metric_score), 2)
        weighted = round(raw_score / 5.0 * item["weight"], 2)
        rows.append(
            {
                "criterion": item["criterion"],
                "weight": item["weight"],
                "score_0_to_5": raw_score,
                "weighted_score": weighted,
                "evidence_present": ";".join(present),
                "evidence_missing": ";".join(missing),
                "metric_detail": metric_detail,
                "why_it_matters": item["why_it_matters"],
            }
        )
    frame = pd.DataFrame(rows)
    summary = {
        "total_weight": int(frame["weight"].sum()),
        "weighted_score": round(float(frame["weighted_score"].sum()), 2),
        "score_percent": round(float(frame["weighted_score"].sum() / frame["weight"].sum() * 100), 2),
        "criteria": int(len(frame)),
        "criteria_at_full_score": int((frame["score_0_to_5"] == 5.0).sum()),
        "lowest_criteria": frame.sort_values(["score_0_to_5", "weight"]).head(3)["criterion"].tolist(),
    }
    return frame, summary


def load_metrics(package_dir: Path) -> dict[str, float]:
    for name in ["cv_metrics.json", "metrics.json"]:
        path = package_dir / name
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            if "overall" in data:
                data = data["overall"]
            return data
    return {}


def metric_check_score(metrics: dict[str, Any], checks: dict[str, float]) -> tuple[float, str]:
    if not checks:
        return 1.0, "no numeric threshold"
    passed = 0
    details = []
    for key, threshold in checks.items():
        value = float(metrics.get(key, 0.0))
        ok = value >= threshold if key != "cost_per_correct_update_usd" else 0 < value <= threshold
        passed += int(ok)
        details.append(f"{key}={value} threshold={threshold} passed={ok}")
    return passed / len(checks), "; ".join(details)
