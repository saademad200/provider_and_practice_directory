# Start Here

This is the flattened judge package for the HealthLynked Provider and Practice Directory Update Pipeline competition.

## 90 Second Read

This is an Option C hybrid submission: a runnable MVP plus a cloud-agnostic production architecture for continuous provider directory quality. The system collects trusted evidence, normalizes fields, resolves provider, practice, and location identity, scores confidence, routes uncertain changes to review, safely auto updates only low risk high confidence fields, and records an audit plus rollback trail for every recommendation.

Proof points:

| Proof point | Value |
|---|---:|
| Field level F1 | 0.948276 |
| Precision | 0.948276 |
| Recall | 0.948276 |
| Safe auto apply precision | 1.0 |
| Candidate updates | 58 |
| Safe auto apply rows | 3 |
| Human review rows | 55 |
| Prototype evidence only cost per correct update | $0.005836 |
| Verification checks | 55 passed |

## Five Minute Judge Path

1. Read `KAGGLE_SUBMISSION_TEXT.md`.
2. Open `HealthLynked_Provider_Directory_Update_Pipeline.ipynb`.
3. Inspect `assets/architecture_diagram.png`.
4. Inspect `assets/agent_workflow_diagram.png`.
5. Inspect `assets/human_review_dashboard_mock.png`.
6. Review `prototype/metrics.json` and `assets/sample_recommendations.json`.
7. Check `evidence/verification.json`.

## Run The MVP

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 scripts/run_best_pipeline.py --out-dir outputs/judge_smoke
python3 scripts/verify_pipeline.py
```

Expected metrics:

```json
{
  "f1": 0.948276,
  "precision": 0.948276,
  "recall": 0.948276,
  "auto_apply_precision": 1.0,
  "predicted_updates": 58,
  "gold_updates": 58,
  "auto_apply_count": 3,
  "review_count": 55
}
```

## Submission Path

Use `KAGGLE_SUBMISSION_TEXT.md` as the main Kaggle writeup. Attach or link `HealthLynked_Provider_Directory_Update_Pipeline.ipynb` as the runnable code artifact. Include the GitHub repository as supporting reproducibility evidence: `https://github.com/saademad200/provider_and_practice_directory`. Link the public Google Drive reproducibility folder as a mirror of this final package.
