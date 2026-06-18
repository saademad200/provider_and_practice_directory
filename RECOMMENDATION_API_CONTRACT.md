# Recommendation API Contract

## Why This Exists

The competition prompt asks for a structured recommendation that product and operations teams can inspect or apply. CSV files are useful for batch review, but HealthLynked also needs a product-facing contract.

This submission therefore includes:

- `scripts/export_recommendation_api_examples.py`
- `submissions/healthlynked_option_c_clean/prototype/recommendation_api_examples.json`
- `submissions/healthlynked_option_c_clean/prototype/recommendation_api_schema.json`

## Response Shape

```json
{
  "schema_version": "provider-directory-recommendation-v1",
  "pipeline_version": "best_cfg_full_peer_context_2026_06_17",
  "metrics_snapshot": {
    "f1": 0.948276,
    "precision": 0.948276,
    "recall": 0.948276,
    "auto_apply_precision": 1.0,
    "cost_per_correct_update_usd": 0.005836
  },
  "recommendations": [
    {
      "provider_id": "P0051",
      "provider_name": "Provider 051",
      "npi": "1999000051",
      "practice_id": "PR017",
      "change_detected": true,
      "changes": [
        {
          "field": "phone",
          "old_value": "555-252-5887",
          "new_value": "555-151-3887",
          "confidence_score": 0.99,
          "supporting_sources": ["health_system", "nppes", "practice_website"],
          "source_urls": ["https://example.org/health_system/P0051"],
          "freshness_status": "fresh",
          "review_reason_code": "auto_apply_criteria_met"
        }
      ],
      "overall_confidence": 0.99,
      "recommended_action": "auto_update",
      "reason": "All proposed changes satisfy high-confidence, low-risk auto-update rules.",
      "supporting_source_count": 3,
      "audit_required": true
    }
  ]
}
```

## Decision Semantics

| `recommended_action` | Meaning |
|---|---|
| `auto_update` | All proposed changes satisfy source, confidence, freshness, field-risk, and auto-apply thresholds. |
| `human_review` | At least one change is low-confidence, conflicting, high-risk, stale, identity-sensitive, or lacks enough independent source support. |
| `no_change` | Current record is confirmed or external evidence is insufficient to recommend a change. |

## Production Notes

- The JSON contract can be emitted by an AWS Lambda/ECS scoring task after evidence normalization.
- Each recommendation should be written to the audit ledger before mutation.
- `audit_required` is always true for any detected change.
- Identity-level actions such as merge, inactive suppression, or practice reassignment remain review-first.
