# Inactive And Retired Provider Detection

This experiment adds a lifecycle layer for providers who are inactive, deactivated, retired, deceased, or attached to a closed practice. It is intentionally conservative: identity-level changes go to review, while downstream product actions can suppress scheduling or highlight stale directory entries.

## Current Pipeline Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0

## Fixture Candidates

| Provider | Name | Confidence | Sources | Recommended Action | Review Reasons |
|---|---|---:|---|---|---|
| P0002 | Provider 002 | 0.82 | nppes, state_license | suppress_from_auto_scheduling_and_review | identity_level_change, current_directory_lists_active |
| P0008 | Provider 008 | 0.48 | health_system, practice_website | inactive_status_review | identity_level_change, missing_license_authority_confirmation, current_directory_lists_active |
| P0010 | Provider 010 | 0.36 | nppes | inactive_status_review | identity_level_change, single_source_inactive_signal, missing_license_authority_confirmation, current_directory_lists_active |

## Signal Policy

- Treat NPPES `A` as active and `D` or deactivation dates as inactive evidence.
- Use state-license status as the highest-authority inactive signal.
- Use practice website and health-system text for retirement or closed-practice evidence.
- Require human review for all identity-level inactive status changes.
- Allow a safer intermediate action, `suppress_from_auto_scheduling_and_review`, when at least two sources agree and one is license authority.
- Never delete a provider record from source evidence alone; write an audit event and preserve historical affiliation/change context.

## Why This Helps

Inactive and retired-provider detection is a category judges can inspect directly. It protects patients from stale directory entries while avoiding the dangerous shortcut of automatically deleting or inactivating providers from one source.
