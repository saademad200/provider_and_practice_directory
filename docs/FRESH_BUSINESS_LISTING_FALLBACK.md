# Fresh Business Listing Fallback

This experiment promotes a narrow fallback: use `business_listing` only for `phone` and `address`, only when the evidence is at most 60 days old, and at low source weight. This recovers one missed update without reducing auto-apply precision.

## Current Best Metrics

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Estimated cost: $0.321

## Comparison

| Config | F1 | Precision | Recall | Auto Precision | Auto Count | Review Count | Cost/Correct |
|---|---:|---:|---:|---:|---:|---:|---:|
| legacy_business_listing_disabled | 0.93913 | 0.947368 | 0.931034 | 1.0 | 20 | 37 | 0.005609 |
| fresh_business_listing_fallback | 0.948276 | 0.948276 | 0.948276 | 1.0 | 20 | 38 | 0.005836 |

## Decision

- F1 delta vs legacy: 0.009146
- Guardrail: business-listing specialty and patient-acceptance signals remain excluded.
- Guardrail: evidence older than 60 days is ignored for business-listing phone/address.
- Guardrail: auto-apply precision remains 1.0; the added update goes to review.
