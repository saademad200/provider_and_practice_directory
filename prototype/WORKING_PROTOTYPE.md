# Working Prototype

## Claim

The repository includes a lightweight MVP that demonstrates the core pipeline on sample provider/practice data. It generates candidate updates, confidence scores, safe auto-apply rows, human-review rows, metrics, and audit-ready outputs.

## What The MVP Demonstrates

- Loads sample provider/practice records.
- Loads external evidence rows from simulated trusted sources.
- Normalizes addresses, phones, specialties, status, and comparison keys.
- Builds candidate field updates.
- Scores update confidence.
- Routes safe updates to auto-apply.
- Routes uncertain or conflicting updates to human review.
- Produces metrics and evidence-backed CSV/JSON outputs.
- Verifies the final Kaggle package.

## Sample Data

| File | Purpose |
|---|---|
| `data/sample/providers.csv` | Current directory records |
| `data/sample/evidence.csv` | External source evidence |
| `data/sample/gold_updates.csv` | Proxy labels for local evaluation |
| `data/sample/benchmark_meta.json` | Benchmark metadata |

## Run Commands

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the MVP:

```bash
python3 scripts/run_best_pipeline.py --out-dir outputs/local_best
```

Verify the final package:

```bash
python3 scripts/verify_pipeline.py \
  --package submissions/latest_final_package.zip \
  --out-dir outputs/verify_latest
```

## Expected MVP Outputs

| Output | Purpose |
|---|---|
| `candidate_updates.csv` | All proposed field updates with confidence and evidence |
| `auto_apply_updates.csv` | Safe high-confidence updates |
| `review_queue.csv` | Human review queue |
| `metrics.json` | Precision, recall, F1, cost, auto-apply precision |
| `config.json` | Reproducible scoring and routing configuration |

## Current Verified Metrics

- F1: `0.948276`
- Precision: `0.948276`
- Recall: `0.948276`
- Auto-apply precision: `1.0`
- Auto-apply count: `20`
- Review count: `38`
- Cost per correct update: `$0.005836`

## Prototype Entry Points

- `scripts/run_best_pipeline.py`
- `scripts/verify_pipeline.py`
- `src/data.py`
- `src/metrics.py`
- `src/cv.py`
- `src/entity_resolution.py`
- `src/source_registry.py`
- `src/review_priority.py`
- `submissions/exp0172/candidate_updates.csv`
- `submissions/exp0172/auto_apply_updates.csv`
- `submissions/exp0172/review_queue.csv`
