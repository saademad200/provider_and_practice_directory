from __future__ import annotations

import time
from typing import Any

import pandas as pd

from .data import build_candidate_updates, load_dataset
from .metrics import score_candidate_updates


def expand_dataset(scale_factor: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    providers, evidence, gold = load_dataset()
    provider_frames = []
    evidence_frames = []
    gold_frames = []
    for shard in range(scale_factor):
        provider_copy = providers.copy()
        evidence_copy = evidence.copy()
        gold_copy = gold.copy()
        provider_copy["provider_id"] = provider_copy["provider_id"].map(lambda value: f"S{shard:04d}_{value}")
        provider_copy["practice_id"] = provider_copy["practice_id"].map(lambda value: f"S{shard:04d}_{value}")
        provider_copy["npi"] = provider_copy["npi"].astype(str).map(lambda value: f"{shard % 10}{value[-9:]}")
        evidence_copy["provider_id"] = evidence_copy["provider_id"].map(lambda value: f"S{shard:04d}_{value}")
        evidence_copy["practice_id"] = evidence_copy["practice_id"].map(lambda value: f"S{shard:04d}_{value}")
        evidence_copy["url"] = evidence_copy["url"].astype(str).map(lambda value: f"{value}?scale_shard={shard}")
        gold_copy["provider_id"] = gold_copy["provider_id"].map(lambda value: f"S{shard:04d}_{value}")
        provider_frames.append(provider_copy)
        evidence_frames.append(evidence_copy)
        gold_frames.append(gold_copy)
    return (
        pd.concat(provider_frames, ignore_index=True),
        pd.concat(evidence_frames, ignore_index=True),
        pd.concat(gold_frames, ignore_index=True),
    )


def run_volume_benchmark(cfg: dict[str, Any], scale_factors: list[int] | None = None) -> pd.DataFrame:
    scale_factors = scale_factors or [1, 10, 50, 100]
    rows: list[dict[str, Any]] = []
    for scale_factor in scale_factors:
        providers, evidence, gold = expand_dataset(scale_factor)
        start = time.perf_counter()
        candidates = build_candidate_updates(providers, evidence, cfg)
        runtime_seconds = time.perf_counter() - start
        metrics = score_candidate_updates(candidates, gold)
        provider_count = int(len(providers))
        evidence_rows = int(len(evidence))
        throughput = provider_count / max(runtime_seconds, 1e-9)
        rows.append(
            {
                "scale_factor": scale_factor,
                "providers": provider_count,
                "evidence_rows": evidence_rows,
                "candidate_updates": int(len(candidates)),
                "runtime_seconds": round(runtime_seconds, 4),
                "providers_per_second": round(throughput, 2),
                "updates_per_1000_providers": round(len(candidates) / provider_count * 1000, 2),
                "f1": metrics["f1"],
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "auto_apply_precision": metrics["auto_apply_precision"],
            }
        )
    return pd.DataFrame(rows)


def step_functions_plan(benchmark: pd.DataFrame) -> pd.DataFrame:
    largest = benchmark.sort_values("providers").iloc[-1]
    provider_seconds = float(largest.runtime_seconds) / float(largest.providers)
    scenarios = [
        {"scenario": "daily_delta_refresh", "providers": 10_000, "batch_size": 500, "max_parallel_batches": 20},
        {"scenario": "regional_refresh", "providers": 100_000, "batch_size": 1000, "max_parallel_batches": 40},
        {"scenario": "national_backfill", "providers": 1_000_000, "batch_size": 2000, "max_parallel_batches": 80},
    ]
    rows: list[dict[str, Any]] = []
    for item in scenarios:
        batches = (item["providers"] + item["batch_size"] - 1) // item["batch_size"]
        sequential_seconds = item["providers"] * provider_seconds
        waves = (batches + item["max_parallel_batches"] - 1) // item["max_parallel_batches"]
        estimated_wall_seconds = waves * item["batch_size"] * provider_seconds
        rows.append(
            {
                **item,
                "batches": int(batches),
                "waves": int(waves),
                "estimated_sequential_minutes": round(sequential_seconds / 60, 2),
                "estimated_parallel_minutes": round(estimated_wall_seconds / 60, 2),
                "aws_orchestration": "EventBridge Scheduler -> Step Functions Map -> AWS Batch/Glue workers -> S3/RDS outputs",
                "control": "SQS dead-letter queue, CloudWatch alarms, idempotent S3 partition writes, audit event required before mutation",
            }
        )
    return pd.DataFrame(rows)
