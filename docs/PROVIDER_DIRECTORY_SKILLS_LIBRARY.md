# Provider Directory Skills Library

This experiment turns the Day 3 Agent Skills strategy into a concrete, portable skills-library skeleton. Each repeated workflow has its own folder, `SKILL.md`, authority-tier reference, and six trigger eval cases.

## Current Quality Context

- F1: 0.93913
- Precision: 0.947368
- Recall: 0.931034
- Auto-apply precision: 1.0

## Skill Folders

| Skill | Owner | Authority Tier | Eval Cases | Folder |
|---|---|---|---:|---|
| checking-source-health | source_ops | read-only | 6 | results/exp0104/provider_directory_skills/checking_source_health |
| normalizing-provider-evidence | data_quality | draft-only | 6 | results/exp0104/provider_directory_skills/normalizing_provider_evidence |
| resolving-provider-identity | identity_ops | draft-only | 6 | results/exp0104/provider_directory_skills/resolving_provider_identity |
| routing-human-review | directory_ops | draft-only | 6 | results/exp0104/provider_directory_skills/routing_human_review |
| auditing-and-rollback | compliance | action-allowed-after-approval | 6 | results/exp0104/provider_directory_skills/auditing_and_rollback |
| evaluating-provider-directory-pipeline | ml_ops | read-only | 6 | results/exp0104/provider_directory_skills/evaluating_provider_directory_pipeline |

## Governance

- Every skill has three positive and three negative trigger evals.
- Action-allowed workflows remain approval-gated.
- Deterministic assets are referenced explicitly rather than copied into long prompts.
- This library is a skeleton for a future HealthLynked internal skills package; it is not required to run the local prototype.
