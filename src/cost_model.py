from __future__ import annotations

from typing import Any


DEFAULT_COST_ASSUMPTIONS = {
    "records_per_1000": 1000,
    "source_evidence_cost_per_record": 0.00531,
    "aws_batch_etl_per_1000": 0.15,
    "aws_storage_monitoring_per_1000": 0.05,
    "llm_extraction_call_cost": 0.01,
    "llm_extraction_rate": 0.08,
    "manual_review_minutes": 1.5,
    "manual_review_hourly_cost": 30.0,
    "manual_review_rate": 0.37,
}


def estimate_cost_per_1000(overrides: dict[str, Any] | None = None) -> dict[str, float]:
    cfg = {**DEFAULT_COST_ASSUMPTIONS, **(overrides or {})}
    records = float(cfg["records_per_1000"])
    evidence = records * float(cfg["source_evidence_cost_per_record"])
    aws_compute = float(cfg["aws_batch_etl_per_1000"]) + float(cfg["aws_storage_monitoring_per_1000"])
    llm = records * float(cfg["llm_extraction_rate"]) * float(cfg["llm_extraction_call_cost"])
    manual_reviews = records * float(cfg["manual_review_rate"])
    manual = manual_reviews * float(cfg["manual_review_minutes"]) / 60.0 * float(cfg["manual_review_hourly_cost"])
    total = evidence + aws_compute + llm + manual
    return {
        "evidence_usd": round(evidence, 4),
        "aws_compute_storage_monitoring_usd": round(aws_compute, 4),
        "llm_extraction_usd": round(llm, 4),
        "manual_review_usd": round(manual, 4),
        "total_usd": round(total, 4),
        "manual_review_items": round(manual_reviews, 2),
    }
