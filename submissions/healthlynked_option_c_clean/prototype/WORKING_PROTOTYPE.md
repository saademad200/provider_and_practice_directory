# Working Prototype

This package includes a lightweight MVP that demonstrates the pipeline using sample provider/practice data.

## Run

```bash
python3 scripts/run_best_pipeline.py --out-dir outputs/local_best
```

## Demonstrated Capabilities

- Load sample provider/practice data.
- Load external evidence rows.
- Normalize field values.
- Generate candidate updates.
- Assign confidence scores.
- Split safe auto-updates from human review.
- Emit audit-ready outputs.
- Score the result against proxy labels.

## Sample Inputs

- `data/sample/providers.csv`
- `data/sample/evidence.csv`
- `data/sample/gold_updates.csv`

## Primary Outputs

- `prototype/candidate_updates.csv`
- `prototype/auto_apply_updates.csv`
- `prototype/review_queue.csv`
- `prototype/metrics.json`
- `evidence/audit_events.jsonl`
- `evidence/rollback_plan.csv`

## Current Metrics

- F1: `0.948276`
- Precision: `0.948276`
- Recall: `0.948276`
- Auto-apply precision: `1.0`
- Cost per correct update: `$0.005836`

## Deterministic Reproduction Check

The MVP is deterministic on the packaged sample data. A fresh run of `python3 scripts/run_best_pipeline.py --out-dir outputs/local_best` should reproduce the packaged metrics:

| Metric | Expected value |
|---|---:|
| F1 | `0.948276` |
| Precision | `0.948276` |
| Recall | `0.948276` |
| Predicted updates | `58` |
| Human-review rows | `55` |
| Safe auto-apply rows | `3` |
| Safe auto-apply precision | `1.0` |
