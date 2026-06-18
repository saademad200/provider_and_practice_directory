# Source Conflict Adjudication

This experiment makes source disagreement explicit. Instead of hiding conflicts inside an aggregate confidence score, it emits a review artifact that shows the candidate value, competing value, source authority, and recommended adjudication action.

## Current Pipeline Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Conflict rows emitted: 93

## Top Conflict Rows

| Provider | Field | Candidate Value | Candidate Sources | Competing Value | Competing Sources | Recommended Action |
|---|---|---|---|---|---|---|
| P0001 | specialty | cardiology | nppes | orthopedics | business_listing, health_system, practice_website | authority_precedence_review |
| P0004 | specialty | orthopedics | health_system, nppes, practice_website | cardiology | business_listing | authority_precedence_review |
| P0006 | specialty | family medicine | business_listing, health_system, nppes | pediatrics | practice_website | authority_precedence_review |
| P0012 | specialty | family medicine | health_system, nppes, practice_website | pediatrics | business_listing | authority_precedence_review |
| P0023 | specialty | cardiology | business_listing, nppes | neurology | health_system, practice_website | authority_precedence_review |
| P0025 | specialty | cardiology | health_system, nppes, practice_website | orthopedics | business_listing | authority_precedence_review |
| P0026 | specialty | dermatology | health_system, nppes, practice_website | neurology | business_listing | authority_precedence_review |
| P0032 | specialty | dermatology | health_system, nppes, practice_website | neurology | business_listing | authority_precedence_review |
| P0035 | specialty | neurology | health_system, nppes, practice_website | dermatology | business_listing | authority_precedence_review |
| P0043 | specialty | cardiology | health_system, nppes, practice_website | orthopedics | business_listing | authority_precedence_review |
| P0047 | specialty | neurology | health_system, nppes, practice_website | dermatology | business_listing | authority_precedence_review |
| P0050 | specialty | neurology | nppes | dermatology | business_listing, health_system, practice_website | authority_precedence_review |
| P0051 | specialty | pediatrics | health_system, nppes, practice_website | family medicine | business_listing | authority_precedence_review |
| P0052 | specialty | orthopedics | health_system, nppes, practice_website | cardiology | business_listing | authority_precedence_review |
| P0053 | specialty | neurology | health_system, nppes, practice_website | dermatology | business_listing | authority_precedence_review |

## Adjudication Policy

- State-license sources are authoritative for license status.
- NPPES is authoritative for NPI status and a strong source for specialty taxonomy.
- Practice websites and health-system pages are strong for current contact/location and patient-acceptance status.
- Business listings are never authority sources; they can only add low-weight hints or review context.
- If authority sources disagree or the top two values have equal authority, route to human review.
- Conflict rows are ideal dashboard and active-learning feedback inputs because reviewer decisions identify systematic source failure modes.
