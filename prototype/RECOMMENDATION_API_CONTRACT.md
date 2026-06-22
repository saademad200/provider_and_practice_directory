# Recommendation API Contract

## Why This Exists

The competition prompt asks for a structured recommendation that product and operations teams can inspect or apply. CSV files are useful for batch review, but HealthLynked also needs a product-facing contract.

This submission therefore includes:

- `prototype/recommendation_api_examples.json`
- `prototype/recommendation_api_schema.json`
- examples generated from the same pipeline outputs used by the MVP

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
      "provider_id": "P0022",
      "provider_name": "Provider 022",
      "npi": "1999000221",
      "practice_id": "PR007",
      "change_detected": true,
      "changes": [
        {
          "field": "specialty",
          "old_value": "family medicine",
          "new_value": "orthopedics",
          "confidence_score": 0.99,
          "supporting_sources": ["health_system", "nppes", "practice_website"],
          "source_urls": [
            "https://example.org/health_system/P0022",
            "https://example.org/nppes/P0022",
            "https://example.org/practice_website/P0022"
          ],
          "source_observations": [
            {
              "source": "health_system",
              "url": "https://example.org/health_system/P0022",
              "authority_tier": "B",
              "age_days": 6
            },
            {
              "source": "nppes",
              "url": "https://example.org/nppes/P0022",
              "authority_tier": "A",
              "age_days": 102
            },
            {
              "source": "practice_website",
              "url": "https://example.org/practice_website/P0022",
              "authority_tier": "B",
              "age_days": 146
            }
          ],
          "freshness_status": "partially_stale",
          "field_decision": "auto_apply",
          "field_risk": "medium",
          "launch_state": "auto_update_candidate",
          "policy_version": "safe_auto_policy_2026_06_19",
          "review_reason_code": "auto_apply_criteria_met",
          "review_priority_score": 0.288,
          "audit_event_type": "candidate_update_created",
          "evidence_hash": "0d3cc158258a9672",
          "rollback_eligible": true
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

`field_decision` records the field-level route from the scoring engine. A recommendation is only `auto_update` when every changed field is `auto_apply`; mixed records are sent to `human_review` with the field-level reasons preserved.

## Field-Level Production Metadata

| Field | Meaning |
|---|---|
| `source_observations` | Per-source URL, authority tier, and evidence age used for the recommendation. |
| `field_risk` | Field risk bucket used by the auto-update policy: low, medium, high, or critical. |
| `launch_state` | Shadow-mode launch state: `auto_update_candidate`, `review_only`, `blocked`, or `no_change_confirmed`. |
| `policy_version` | Versioned decision policy that produced the field route. |
| `evidence_hash` | Stable evidence fingerprint used to join recommendation, audit event, and rollback record. |
| `rollback_eligible` | Whether the update can be automatically reversed from the audit payload after approval. |

## Demo Source URLs

The prototype uses synthetic `example.org` source URLs because the sample benchmark is synthetic and contains no real provider records. In production, these fields are populated with the exact NPPES/API/file reference, state-board page, practice website URL, health-system roster URL, retrieval timestamp, and parser version used for the recommendation.

## Production Notes

- The JSON contract can be emitted by a cloud scoring task (AWS Lambda/ECS as one reference) after evidence normalization.
- Each recommendation should be written to the audit ledger before mutation.
- `audit_required` is always true for any detected change.
- Identity-level actions such as merge, inactive suppression, or practice reassignment remain review-first.
