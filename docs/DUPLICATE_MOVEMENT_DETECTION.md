# Duplicate And Provider Movement Detection

This module adds two bonus-criterion capabilities: duplicate-provider detection and provider-movement review signals.

## Current Pipeline Context

- F1: 0.93913
- Precision: 0.947368
- Recall: 0.931034
- Auto-apply precision: 1.0

## Duplicate Detection

Duplicate scoring combines same NPI, same phone, same normalized address, same specialty, and similar provider name. Exact NPI matches dominate the score because NPI is the strongest identity anchor.

| Left Provider | Right Provider | Score | Signals | Recommended Action |
|---|---|---:|---|---|
| P0000 | P_DUP_0000 | 0.96 | same_npi, same_phone, same_address, same_specialty | merge_review |

## Provider Movement Detection

Movement scoring uses address/phone update candidates, practice-peer mismatch, freshness, and multi-source support. It does not auto-merge or auto-move records; it routes likely moves to review with evidence.

| Provider | Field | Score | Signals | Recommended Action |
|---|---|---:|---|---|
| P0031 | address | 0.9 | address_changed, practice_peer_mismatch, multi_source_support | movement_review |
| P0066 | address | 0.9 | address_changed, practice_peer_mismatch, multi_source_support | movement_review |
| P0050 | address | 0.9 | address_changed, practice_peer_mismatch, multi_source_support | movement_review |
| P0003 | address | 0.9 | address_changed, practice_peer_mismatch, multi_source_support | movement_review |
| P0023 | address | 0.9 | address_changed, practice_peer_mismatch, multi_source_support | movement_review |
| P0039 | address | 0.9 | address_changed, practice_peer_mismatch, multi_source_support | movement_review |
| P0017 | address | 0.9 | address_changed, practice_peer_mismatch, multi_source_support | movement_review |
| P0061 | phone | 0.7 | phone_changed, practice_peer_mismatch, multi_source_support | movement_review |
| P0067 | phone | 0.7 | phone_changed, practice_peer_mismatch, multi_source_support | movement_review |
| P0037 | phone | 0.7 | phone_changed, practice_peer_mismatch, multi_source_support | movement_review |

## Production Design

- Duplicate candidates should be reviewed before auto-applying identity-level merges.
- Provider movement should require fresh patient-facing or authoritative source evidence.
- AWS Step Functions can run duplicate and movement scans after each evidence refresh.
- Reviewer outcomes should feed the active-learning loop, especially for name-similarity and practice-affiliation thresholds.
