# Package Integrity Manifest

This manifest records artifact sizes and SHA-256 hashes for the submitted package directory. It gives judges and maintainers a simple way to confirm that key files did not change after verification.

## Current Quality Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0

## Manifest Summary

- Artifacts: 107
- Total size bytes: 412100
- Manifest digest: `2491be0be163ec03f8aa6be10665a70b98c937abf55679385e94cbce2b6ea568`

## Key Artifacts

| Artifact | Size Bytes | SHA-256 |
|---|---:|---|
| ARTIFACT_INDEX.md | 5238 | d73eb1140389ede92a855fbb78231f4bf5cbe8f06cbc56e44aea247f03f08d42 |
| EXECUTIVE_SUMMARY.md | 3892 | bb765dced79942a8a6d0e690618f282cc69a9e6f98914625a4faef8830d3e473 |
| PRODUCTION_READINESS_SCORECARD.md | 3873 | 79c250931a17209065dbcc868b55c2cbb54fe146d4f102e18bcd73a735ed4c49 |
| README.md | 650 | 46bdfda33df285da30023afdf94ac21d3088b3e21088218a1f5688aa3c995b7f |
| RED_TEAM_EVALS.md | 2126 | 4bae6e61b080b5236850ac71299f8a7e620f12056d4a893a189bc678c9755a2b |
| candidate_updates.csv | 21699 | 3f40850a09074c75986633dc13e9f53efb3dfc3bf0733c0e4a16dadad47e0d38 |
| verification.json | 16487 | 1dde52b886d9ecb61b8f69db2bae872851eecc07f05d8bccd3a2d32dd381b84e |

## Verification Notes

- The package verifier checks required artifact presence and runnable pipeline health.
- This manifest checks artifact identity and supports reproducibility across handoffs.
- Regenerate after any package content change; do not reuse stale hashes.
