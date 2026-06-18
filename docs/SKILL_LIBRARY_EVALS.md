# Skill Library Regression Evals

This artifact turns the Agent Skills whitepaper guidance into mechanical checks for the generated provider-directory skills library.

## Result

- Passed: True
- Skills checked: 6
- Checks: 55
- Failed checks: 0
- Positive trigger cases: 18
- Negative trigger cases: 18

## Current Prototype Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0

## Checks

- Skill file exists and is substantive.
- Frontmatter name matches the folder.
- Authority tier is one of the approved tiers.
- Allowed tools remain local/read-only for generated skeleton skills.
- Each skill has exactly three positive and three negative trigger cases.
- Trigger cases target the same skill.
- Authority reference exists and repeats the tier.
- Skill body stays compact enough for progressive disclosure.
- Action-allowed skills explicitly require approval.

## Failures

| Skill | Check | Passed | Note |
|---|---|---|---|
| none | none | passed | |
