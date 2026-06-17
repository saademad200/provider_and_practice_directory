# Working Prototype

This package includes a lightweight MVP that demonstrates the pipeline using sample provider/practice data.

## Run

```bash
python3 scripts/run_best_pipeline.py --out-dir outputs/local_best
```

Verify the final package:

```bash
python3 scripts/verify_pipeline.py \
  --package submissions/latest_final_package.zip \
  --out-dir outputs/verify_latest
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

- `candidate_updates.csv`
- `auto_apply_updates.csv`
- `review_queue.csv`
- `metrics.json`
- `cv_metrics.json`
- `audit_events.jsonl`

## Current Metrics

- F1: `0.948276`
- Precision: `0.948276`
- Recall: `0.948276`
- Auto-apply precision: `1.0`
- Cost per correct update: `$0.005836`
