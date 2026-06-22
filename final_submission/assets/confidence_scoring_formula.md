# Confidence Scoring Formula

```text
confidence =
  source_authority_weight
  + source_agreement_weight
  + freshness_weight
  + field_stability_weight
  + identity_match_weight
  - conflict_penalty
  - stale_evidence_penalty
  - high_risk_field_penalty
```

Default field policy:

| Field | Risk | Auto-update policy |
|---|---|---|
| Phone | low/medium | allowed only with fresh corroborated evidence |
| Website | low/medium | allowed only with canonical URL validation and corroboration |
| Specialty | medium | allowed only with stable taxonomy/display mapping and corroboration |
| Address | high | review-first |
| Practice affiliation | high | review-first |
| Provider name | high | review-first |
| NPI | identity-critical | never auto-update |
| Active/inactive status | high | review-first |
| Duplicate merge | identity-critical | never auto-update |

Auto-update launch gates:

1. field is allowed for auto-update;
2. confidence exceeds field threshold;
3. at least two independent trusted sources support the value;
4. evidence is fresh for the field;
5. no high-risk identity flag is present;
6. audit and rollback records can be written before mutation.
