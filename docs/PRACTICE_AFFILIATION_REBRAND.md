# Practice Affiliation And Rebrand Detection

This experiment adds signals for provider group changes, practice rebrands, and affiliation moves. It uses an augmented fixture because the core benchmark intentionally keeps practice identities simple.

## Current Pipeline Context

- F1: 0.93913
- Precision: 0.947368
- Recall: 0.931034
- Auto-apply precision: 1.0

## Practice Change Candidates

| Left Practice | Right Practice | Left Name | Right Name | Score | Signals |
|---|---|---|---|---:|---|
| PR000 | PR_REBRAND | HealthLynked Practice PR000 | HealthLynked Medical Group | 1.0 | same_address, same_phone, possible_rebrand, same_provider_npi, practice_affiliation_change |
| PR000 | PR_NEW_AFFIL | HealthLynked Practice PR000 | Coastal Ortho Partners | 0.85 | same_address, same_provider_npi, practice_affiliation_change |
| PR_REBRAND | PR_NEW_AFFIL | HealthLynked Medical Group | Coastal Ortho Partners | 0.85 | same_address, same_provider_npi, practice_affiliation_change |

## Production Design

- Detect rebrands when practice name changes but address/phone/location remains stable.
- Detect affiliation moves when provider NPI appears under a new practice identity or location.
- Never auto-merge practices from fuzzy names alone.
- Route high-score candidates to review with source URLs and historical directory values.
- Feed accepted/rejected practice-change reviews into the active-learning loop.
