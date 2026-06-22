# Confidence Scoring Formula

The confidence score is decomposed so a reviewer can understand why a recommendation exists.

```text
confidence = source_authority_weight
           + source_agreement_weight
           + freshness_weight
           + identity_match_weight
           + field_stability_weight
           - conflict_penalty
           - stale_evidence_penalty
           - high_risk_field_penalty
```

## Required explanations per recommendation

| Term | Reviewer meaning |
|---|---|
| Source authority | How trustworthy each source is for the specific field |
| Source agreement | Whether independent sources agree on the same value |
| Freshness | Whether the evidence is inside the field level source SLA |
| Identity match | NPI, provider name, specialty, practice and location consistency |
| Field stability | Lower risk for display fields, higher risk for identity or affiliation fields |
| Conflict penalty | Deduction when trusted sources disagree |
| Stale evidence penalty | Deduction when supporting sources are old |
| High risk field penalty | Deduction or hard review gate for address, NPI, status, merge and movement |

## Decision thresholds

| Band | Action |
|---|---|
| 0.96 and above | Possible auto update only for low risk fields with enough trusted sources |
| 0.74 to 0.95 | Human review |
| Below 0.74 | Reject or recrawl unless risk policy sends to review |
| Any identity, NPI, inactive, movement, affiliation, or duplicate merge signal | Human review regardless of score |
