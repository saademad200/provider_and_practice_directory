#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data import build_candidate_updates, load_dataset
from src.metrics import score_candidate_updates


BEST_CFG = {
    "confidence_threshold": 0.74,
    "auto_apply_threshold": 0.94,
    "recency_half_life_days": 120.0,
    "practice_consensus_review_fields": ["phone", "address"],
    "disabled_sources": [],
    "source_field_allowlist": {
        "business_listing": ["phone", "address"],
    },
    "source_max_age_days_by_source_field": {
        "business_listing": {
            "phone": 60,
            "address": 60,
        },
    },
    "min_distinct_sources": 1,
    "min_distinct_sources_by_field": {
        "phone": 2,
        "address": 2,
        "specialty": 2,
        "accepting_new_patients": 2,
        "license_status": 1,
    },
    "min_auto_sources": 1,
    "min_auto_sources_by_field": {
        "phone": 3,
        "address": 3,
        "specialty": 3,
        "accepting_new_patients": 3,
        "license_status": 1,
    },
    "field_confidence_thresholds": {
        "phone": 0.78,
        "address": 0.80,
        "specialty": 0.82,
        "accepting_new_patients": 0.82,
        "license_status": 0.72,
    },
    "field_auto_apply_thresholds": {
        "phone": 0.96,
        "address": 0.97,
        "specialty": 0.97,
        "accepting_new_patients": 0.98,
        "license_status": 0.90,
    },
    "source_weights": {
        "business_listing": 0.10,
        "practice_website": 0.65,
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the best provider-directory update pipeline.")
    parser.add_argument("--out-dir", default="outputs/best_pipeline", help="Directory for pipeline outputs.")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    providers, evidence, gold = load_dataset()
    candidates = build_candidate_updates(providers, evidence, BEST_CFG)
    metrics = score_candidate_updates(candidates, gold)
    review_queue = candidates[candidates["decision"] == "review"].copy()
    if "review_priority_score" in review_queue.columns:
        review_queue = review_queue.sort_values(["review_priority_score", "confidence"], ascending=[False, True])

    candidates.to_csv(out_dir / "candidate_updates.csv", index=False)
    candidates[candidates["decision"] == "auto_apply"].to_csv(out_dir / "auto_apply_updates.csv", index=False)
    review_queue.to_csv(out_dir / "review_queue.csv", index=False)
    review_queue.to_csv(out_dir / "prioritized_review_queue.csv", index=False)
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    (out_dir / "config.json").write_text(json.dumps(BEST_CFG, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"out_dir": str(out_dir), "metrics": metrics}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
