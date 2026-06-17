# Review Queue Prioritization

Review priority is label-free and is computed before evaluation. It helps operators inspect the highest-risk updates first without changing candidate generation metrics.

## Score Inputs

- Field risk: address, license status, and patient acceptance are treated as higher patient-access risk.
- Confidence gap: candidates closer to the review threshold are prioritized.
- Source gap: candidates missing the auto-apply source-count requirement move up.
- Practice peer mismatch: phone and address values that disagree with practice peers move up.

## Current Review Queue

- High priority: 0
- Medium priority: 13
- Low priority: 24

## Top Review Items

| Provider | Field | Score | Band | Drivers | Review Reason |
|---|---|---:|---|---|---|
| P0031 | address | 0.556 | medium | high_field_risk, practice_peer_mismatch | practice_peer_mismatch |
| P0066 | address | 0.556 | medium | high_field_risk, practice_peer_mismatch | practice_peer_mismatch |
| P0050 | address | 0.556 | medium | high_field_risk, practice_peer_mismatch | practice_peer_mismatch |
| P0039 | address | 0.556 | medium | high_field_risk, practice_peer_mismatch | practice_peer_mismatch |
| P0003 | address | 0.556 | medium | high_field_risk, practice_peer_mismatch | practice_peer_mismatch |
| P0023 | address | 0.556 | medium | high_field_risk, practice_peer_mismatch | practice_peer_mismatch |
| P0017 | address | 0.556 | medium | high_field_risk, practice_peer_mismatch | practice_peer_mismatch |
| P0046 | address | 0.516 | medium | high_field_risk, source_gap | insufficient_auto_sources |
