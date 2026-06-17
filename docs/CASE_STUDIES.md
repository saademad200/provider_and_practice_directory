# Pipeline Case Studies

These examples come from the local synthetic benchmark and are meant to make the pipeline behavior inspectable. They are not official Kaggle labels.

## True Positives

| Provider | Field | Old | Proposed | Gold | Decision | Confidence | Sources | Notes |
|---|---|---|---|---|---|---:|---|---|
| P0003 | address | 632 Market St, Suite 5, FL | 121 pine boulevard suite 4 florida | 121 Pine Blvd, Suite 4, FL | review | 0.99 | health_system, nppes, practice_website | practice_peer_mismatch; high_field_risk, practice_peer_mismatch |
| P0004 | address | 639 Lake Dr, Suite 6, FL | 128 market street suite 5 florida | 128 Market St, Suite 5, FL | review | 0.99 | health_system, practice_website | insufficient_auto_sources; high_field_risk, source_gap |
| P0004 | phone | 555-205-5885 | 555-104-2148 | 555-104-2148 | review | 0.99 | health_system, practice_website | insufficient_auto_sources; source_gap |
| P0005 | phone | 555-206-5922 | 555-105-2185 | 555-105-2185 | review | 0.99 | health_system, nppes, practice_website | practice_peer_mismatch; practice_peer_mismatch |
| P0005 | specialty | cardiology | neurology | neurology | auto_apply | 0.99 | health_system, nppes, practice_website | auto_apply_criteria_met; auto_apply_criteria_met |

## False Positives

| Provider | Field | Old | Proposed | Gold | Decision | Confidence | Sources | Notes |
|---|---|---|---|---|---|---:|---|---|
| P0001 | specialty | cardiology | orthopedics |  | review | 0.99 | health_system, practice_website | insufficient_auto_sources; source_gap |
| P0010 | address | 681 Lake Dr, Suite 12, FL | 1213 pine boulevard suite 4 florida |  | review | 0.99 | health_system, practice_website | insufficient_auto_sources; high_field_risk, source_gap |
| P0013 | specialty | cardiology | orthopedics |  | review | 0.99 | nppes, practice_website | insufficient_auto_sources; source_gap |

## False Negatives

| Provider | Field | Old | Proposed | Gold | Decision | Confidence | Sources | Notes |
|---|---|---|---|---|---|---:|---|---|
| P0010 | address | 681 Lake Dr, Suite 12, FL |  | 170 Market St, Suite 11, FL | missed |  | business_listing | not_generated |
| P0012 | phone | 555-213-6181 |  | 555-112-2444 | missed |  | business_listing, nppes | not_generated |
| P0038 | license_status | inactive |  | active | missed |  |  | not_generated |
| P0049 | address | 954 Cedar Rd, Suite 3, FL |  | 443 Oak Ave, Suite 2, FL | missed |  | practice_website | not_generated |
