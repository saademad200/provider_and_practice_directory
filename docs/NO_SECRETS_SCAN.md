# No-Secrets Scan

This scan supports the privacy/compliance claim that source credentials and secrets are not stored in prompts, docs, package artifacts, or source code.

## Current Quality Context

- F1: 0.93913
- Precision: 0.947368
- Recall: 0.931034
- Auto-apply precision: 1.0

## Scan Summary

- Passed: True
- Findings: 0
- Scanned roots: src, scripts, experiments, docs, submissions/exp0094

## Findings

| Path | Pattern | Matches | Action |
|---|---|---:|---|
| none | none | 0 | none |

## Production Rule

- Any real secret finding blocks release.
- Store source credentials in AWS Secrets Manager and inject at runtime through least-privilege roles.
- Keep package artifacts free of source credentials, API keys, private keys, and long-lived tokens.
