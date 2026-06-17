# Reproducibility

All commands assume the repository root as the working directory.

## Expected Current Metrics

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Auto-apply count: 20
- Review count: 38
- Candidate updates: 58

## Run The Prototype

```bash
python3 scripts/run_best_pipeline.py --out-dir outputs/reproduce_best
```

Expected files:

- `outputs/reproduce_best/candidate_updates.csv`
- `outputs/reproduce_best/auto_apply_updates.csv`
- `outputs/reproduce_best/review_queue.csv`
- `outputs/reproduce_best/metrics.json`
- `outputs/reproduce_best/config.json`

## Verify The Package

```bash
python3 scripts/verify_pipeline.py --package submissions/exp0172_final_combined_abc_handoff_package.zip --out-dir outputs/reproduce_verify
```

Expected result:

- `outputs/reproduce_verify/verification.json`
- `passed: true`
- 89 curated-package checks
- F1 at or above 0.90
- Auto-apply precision at or above 0.95

## Inspect The Package

```bash
unzip -l submissions/exp0172_final_combined_abc_handoff_package.zip | head -80
```

Open these first:

1. `MVP_FIELD_COVERAGE.md`
2. `ONE_PAGE_JUDGE_GUIDE.md`
3. `EXECUTIVE_SUMMARY.md`
4. `FRESH_BUSINESS_LISTING_FALLBACK.md`
5. `verification.json`

## Data Note

The Kaggle competition archive did not include official train/test files. The local benchmark is a transparent synthetic/public-demo proxy and the package includes datasheets, leakage controls, source-stress tests, and residual-error analysis to make that limitation explicit.
