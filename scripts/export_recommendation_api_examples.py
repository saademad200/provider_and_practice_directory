#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_best_pipeline import BEST_CFG
from src.data import build_candidate_updates, load_dataset
from src.metrics import score_candidate_updates


def _split_pipe(value: Any) -> list[str]:
    text = str(value or "")
    if not text or text == "nan":
        return []
    return [item for item in text.split("|") if item]


def recommendation_records(limit: int = 8) -> list[dict[str, Any]]:
    providers, evidence, gold = load_dataset()
    candidates = build_candidate_updates(providers, evidence, BEST_CFG)
    metrics = score_candidate_updates(candidates, gold)
    provider_lookup = providers.set_index("provider_id").to_dict("index")

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in candidates.to_dict("records"):
        grouped[str(row["provider_id"])].append(row)

    ranked_provider_ids = sorted(
        grouped,
        key=lambda provider_id: (
            max(item.get("decision") == "auto_apply" for item in grouped[provider_id]),
            len(grouped[provider_id]),
            max(float(item.get("confidence", 0.0)) for item in grouped[provider_id]),
        ),
        reverse=True,
    )

    recommendations: list[dict[str, Any]] = []
    for provider_id in ranked_provider_ids[:limit]:
        current = provider_lookup.get(provider_id, {})
        changes = []
        decisions = []
        confidences = []
        reason_parts = []
        source_set = set()
        for item in sorted(grouped[provider_id], key=lambda record: str(record["field"])):
            sources = _split_pipe(item.get("sources"))
            urls = _split_pipe(item.get("evidence_urls"))
            confidence = round(float(item.get("confidence", 0.0)), 4)
            confidences.append(confidence)
            decisions.append(str(item.get("decision", "review")))
            source_set.update(sources)
            reason = str(item.get("review_reason_code", ""))
            if reason and reason != "auto_apply_criteria_met":
                reason_parts.append(reason)
            changes.append(
                {
                    "field": item["field"],
                    "old_value": item["old_value"],
                    "new_value": item["proposed_value"],
                    "confidence_score": confidence,
                    "supporting_sources": sources,
                    "source_urls": urls,
                    "freshness_status": item.get("freshness_status", ""),
                    "field_decision": item.get("decision", ""),
                    "review_reason_code": item.get("review_reason_code", ""),
                }
            )

        recommended_action = "auto_update" if decisions and all(decision == "auto_apply" for decision in decisions) else "human_review"
        if recommended_action == "auto_update":
            reason = "All proposed changes satisfy high-confidence, low-risk auto-update rules."
        else:
            unique_reasons = sorted({part for part in reason_parts if part})
            if unique_reasons:
                reason = (
                    "Manual verification recommended because "
                    + ", ".join(unique_reasons[:4]).replace("_", " ")
                    + "."
                )
            else:
                reason = "Manual verification recommended because this provider has mixed auto-apply and review-routed field updates."
        recommendations.append(
            {
                "provider_id": provider_id,
                "provider_name": current.get("provider_name", ""),
                "npi": str(current.get("npi", "")),
                "practice_id": current.get("practice_id", ""),
                "change_detected": bool(changes),
                "changes": changes,
                "overall_confidence": round(sum(confidences) / len(confidences), 4) if confidences else 0.0,
                "recommended_action": recommended_action,
                "reason": reason,
                "supporting_source_count": len(source_set),
                "audit_required": True,
            }
        )

    return [
        {
            "schema_version": "provider-directory-recommendation-v1",
            "pipeline_version": "best_cfg_full_peer_context_2026_06_17",
            "metrics_snapshot": {
                "f1": metrics["f1"],
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "auto_apply_precision": metrics["auto_apply_precision"],
                "cost_per_correct_update_usd": metrics["cost_per_correct_update_usd"],
            },
            "recommendations": recommendations,
        }
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Export product-facing recommendation API examples.")
    parser.add_argument("--out", default="outputs/recommendation_api_examples.json")
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = recommendation_records(limit=args.limit)[0]
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"out": str(out_path), "recommendations": len(payload["recommendations"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
