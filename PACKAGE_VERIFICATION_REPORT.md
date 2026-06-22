# Package Verification Report

Verification status: PASSED

Checks passed: 55 / 55

## Reproduced Metrics

| Metric | Value |
|---|---:|
| F1 | 0.948276 |
| Precision | 0.948276 |
| Recall | 0.948276 |
| Auto apply precision | 1.0 |
| Candidate updates | 58 |
| Gold updates | 58 |
| Auto apply rows | 3 |
| Human review rows | 55 |
| Evidence cost | $0.321 |
| Evidence cost per correct update | $0.005836 |

## Verification Scope

The verifier checks required files, CLI execution, metric alignment, sample recommendation shape, audit and rollback presence, image dimensions, stale reference removal, nested ZIP removal, and unit tests.

Detailed machine readable output is in `evidence/verification.json`.

## Clean Repository Check

The public GitHub repository was tested from a fresh clone:

```text
Repository: https://github.com/saademad200/provider_and_practice_directory
Tracked files: 85
Verifier: passed
Unit tests: 8 passed
```
