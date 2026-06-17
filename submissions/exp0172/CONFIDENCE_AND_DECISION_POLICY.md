# Confidence And Decision Policy

## Purpose

This policy defines how the pipeline turns external evidence into one of three actions:

- `no_change`
- `auto_update`
- `human_review`

It is intentionally conservative. The goal is not to maximize the number of automated changes; the goal is to maximize correct updates while reducing human review to the cases that actually require judgment.

## Source Authority Tiers

| Tier | Source Type | Allowed Uses | Not Allowed |
|---|---|---|---|
| A | NPPES, CMS files, state boards, FSMB-style licensing feeds | NPI identity, taxonomy, licensure/status signals, deactivation signals | NPPES alone cannot prove active licensure or current office phone |
| B | Practice websites, health-system directories | Current location, phone, roster, affiliation, website, accepting-new-patients evidence | Cannot override license/status authority alone |
| C | Fresh business listings | Phone/address recall fallback only | Identity, license, specialty, inactive status, or practice affiliation decisions |
| D | LLM extraction over approved pages | Structured extraction from messy but permitted pages | Never a standalone authority source |

## Field Risk Levels

| Field | Risk | Default Routing |
|---|---:|---|
| phone | low | auto-update allowed with strong source agreement |
| website | low | auto-update allowed with strong source agreement |
| address | medium | auto-update only with strong practice/health-system agreement and no conflict |
| specialty | medium | review unless authority/source agreement is strong |
| practice name | high | review-first if rebrand or affiliation ambiguity exists |
| practice affiliation | high | review-first |
| provider name | high | review-first unless formatting-only normalization |
| NPI | identity-critical | never auto-change; identity anchor |
| active/inactive status | identity-critical | review-first unless HealthLynked explicitly approves a suppression workflow |

## Confidence Formula

For a candidate field update:

```text
confidence =
  0.32 * source_authority_score
+ 0.22 * independent_source_agreement
+ 0.16 * freshness_score
+ 0.12 * identity_match_score
+ 0.10 * field_consistency_score
+ 0.08 * historical_stability_score
- conflict_penalty
- field_risk_penalty
```

Component meanings:

| Component | Meaning |
|---|---|
| `source_authority_score` | Whether the source is permitted to support this field. |
| `independent_source_agreement` | Agreement across independent sources, not duplicate mirrors. |
| `freshness_score` | Recency of evidence and connector health. |
| `identity_match_score` | NPI/name/practice/location match strength. |
| `field_consistency_score` | Normalized phone/address/specialty/practice value consistency. |
| `historical_stability_score` | Whether the change matches known movement or practice history. |
| `conflict_penalty` | Penalty for contradictory sources or stale authoritative data. |
| `field_risk_penalty` | Penalty for high-risk or identity-sensitive fields. |

## Auto-Update Rules

Auto-update is allowed only when all conditions pass:

1. `confidence >= 0.97`
2. field risk is `low`, or `medium` with stricter source agreement;
3. at least two independent supporting sources exist;
4. no stronger source conflicts with the proposed value;
5. evidence is fresh enough for the field;
6. the change is not identity-level;
7. audit event and rollback record can be created before mutation.

## Human Review Rules

Route to human review when any condition is true:

- confidence is below threshold;
- sources conflict;
- source authority is inappropriate for the field;
- source freshness is weak;
- the field is identity-critical;
- provider movement or practice affiliation is detected;
- inactive/retired status is suggested;
- the candidate would merge, split, suppress, or reassign a provider record.

## No-Change Rules

Return `no_change` when:

- current HealthLynked value is confirmed by stronger or fresher evidence;
- external evidence is too weak to recommend a change;
- evidence refers to a different provider/practice/location entity;
- the proposed value is only a formatting difference already handled by normalization.

## Reviewer Explanation Contract

Every recommendation shown to a reviewer must include:

- old value;
- proposed value;
- normalized comparison;
- field risk;
- confidence score and component reasons;
- supporting sources and URLs;
- source timestamps/freshness;
- conflict summary;
- recommended action;
- audit hash and rollback eligibility.

## Production Calibration

Initial thresholds should be calibrated in shadow mode against HealthLynked reviewer decisions. Auto-update should remain disabled for any field until measured precision exceeds the agreed safety threshold over a representative sample.
