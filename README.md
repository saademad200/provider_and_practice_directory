# HealthLynked Provider Directory Update Pipeline

Option C hybrid submission: a working MVP plus a cloud-agnostic production architecture for continuously detecting, validating, reviewing, and auditing provider and practice directory updates.

## What To Open First

1. `START_HERE.md`
2. `KAGGLE_SUBMISSION_TEXT.md`
3. `HealthLynked_Provider_Directory_Update_Pipeline.ipynb`
4. `assets/architecture_diagram.png`
5. `assets/agent_workflow_diagram.png`
6. `assets/human_review_dashboard_mock.png`
7. `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md`
8. `prototype/RECOMMENDATION_API_CONTRACT.md`
9. `evidence/verification.json`
10. `ADVERSARIAL_REVIEW_LOG.md`

## Prototype Proof Points

| Metric | Value |
|---|---:|
| Local proxy F1 | 0.948276 |
| Precision | 0.948276 |
| Recall | 0.948276 |
| Safe auto apply precision | 1.0 |
| Candidate updates | 58 |
| Safe auto apply updates | 3 |
| Human review items | 55 |
| Prototype evidence only cost per correct update | $0.005836 |

## Run The MVP

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 scripts/run_best_pipeline.py --out-dir outputs/judge_smoke
python3 scripts/verify_pipeline.py
```

Expected output files:

```text
outputs/judge_smoke/candidate_updates.csv
outputs/judge_smoke/auto_apply_updates.csv
outputs/judge_smoke/review_queue.csv
outputs/judge_smoke/metrics.json
```

## Folder Map

| Folder | Purpose |
|---|---|
| `assets/` | Diagrams, source matrix, confidence formula, cost model, samples |
| `proposal/` | Main technical architecture, judge memo, source plan, roadmap |
| `prototype/` | MVP outputs, metrics, recommendation contract |
| `dashboard/` | Sample human review dashboard |
| `evidence/` | Verification, audit, rollback, rubric, cost and source health evidence |
| `appendix/` | Deeper production controls |
| `src/`, `scripts/`, `data/sample/`, `tests/` | Reproducible MVP code and checks |
