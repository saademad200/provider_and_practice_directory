from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import pandas as pd

from .data import build_candidate_updates, load_dataset, provider_splits
from .metrics import per_field_breakdown, score_candidate_updates, worst_provider_breakdown


def run_cv(cfg: dict[str, Any]) -> dict[str, Any]:
    start = time.time()
    providers, evidence, gold = load_dataset()
    seed = int(cfg.get("seed", 42))
    n_splits = int(cfg.get("n_splits", 5))
    smoke = bool(cfg.get("smoke", False))
    max_providers = cfg.get("max_providers")
    full_directory_peer_context = bool(cfg.get("full_directory_peer_context", False))

    if smoke:
        max_providers = max_providers or 18
    if max_providers:
        keep = providers["provider_id"].head(int(max_providers))
        providers = providers[providers["provider_id"].isin(keep)].reset_index(drop=True)
        evidence = evidence[evidence["provider_id"].isin(keep)].reset_index(drop=True)
        gold = gold[gold["provider_id"].isin(keep)].reset_index(drop=True)

    fold_rows = []
    all_candidates = []
    for fold, (_, val_idx) in enumerate(provider_splits(providers, n_splits=n_splits), start=1):
        val_providers = providers.iloc[val_idx].reset_index(drop=True)
        val_ids = set(val_providers["provider_id"])
        val_evidence = evidence[evidence["provider_id"].isin(val_ids)].reset_index(drop=True)
        val_gold = gold[gold["provider_id"].isin(val_ids)].reset_index(drop=True)
        provider_context = providers if full_directory_peer_context else val_providers
        candidates = build_candidate_updates(provider_context, val_evidence, cfg)
        if not candidates.empty:
            candidates["fold"] = fold
        metrics = score_candidate_updates(candidates, val_gold)
        fold_rows.append({"fold": fold, **metrics})
        all_candidates.append(candidates)

    candidates_all = pd.concat(all_candidates, ignore_index=True) if all_candidates else pd.DataFrame()
    overall = score_candidate_updates(candidates_all, gold)
    field_breakdown = per_field_breakdown(candidates_all, gold)
    worst = worst_provider_breakdown(candidates_all, gold)
    runtime = time.time() - start
    return {
        "config": {**cfg, "seed": seed},
        "overall": overall,
        "folds": fold_rows,
        "per_field": field_breakdown.to_dict(orient="records"),
        "worst_providers": worst.to_dict(orient="records"),
        "runtime_seconds": round(runtime, 3),
        "candidate_updates": candidates_all,
    }


def save_cv_result(result: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    candidates = result.pop("candidate_updates")
    metrics_path = out_dir / "metrics.json"
    metrics_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    if not candidates.empty:
        for column in candidates.select_dtypes(include=["object"]).columns:
            candidates[column] = candidates[column].astype(str)
        candidates.to_parquet(out_dir / "candidate_updates.parquet", index=False)
        candidates.to_csv(out_dir / "candidate_updates.csv", index=False)
    else:
        pd.DataFrame().to_csv(out_dir / "candidate_updates.csv", index=False)
