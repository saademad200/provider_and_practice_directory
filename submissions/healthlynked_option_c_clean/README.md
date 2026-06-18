# HealthLynked Provider Directory Update Pipeline

Option C hybrid submission: a working MVP plus a production architecture for continuously detecting, validating, reviewing, and auditing provider/practice directory updates.

## What To Open First

- `START_HERE.md`
- `Provider_Directory_Update_Pipeline_End_to_End.ipynb`
- `proposal/ONE_PAGE_SCORECARD.md`
- `proposal/JUDGE_DECISION_MEMO.md`
- `proposal/WINNING_PROPOSAL_BRIEF.md`
- `proposal/BONUS_COVERAGE_MATRIX.md`
- `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md`
- `proposal/AGENT_WORKFLOW_DIAGRAM.md`
- `proposal/CONFIDENCE_AND_DECISION_POLICY.md`
- `prototype/WORKING_PROTOTYPE.md`
- `dashboard/index.html`

For the full reading order, use `START_HERE.md`.

## Prototype Proof Points

- Local proxy F1: 0.948276
- Precision / recall: 0.948276 / 0.948276
- Safe auto-apply precision: 1.0
- Cost per correct update: $0.005836
- Cloud plan: AWS

## Run The MVP

From inside the unzipped package:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 scripts/run_best_pipeline.py --out-dir outputs/judge_smoke
```

Expected output files:

- `outputs/judge_smoke/candidate_updates.csv`
- `outputs/judge_smoke/auto_apply_updates.csv`
- `outputs/judge_smoke/review_queue.csv`
- `outputs/judge_smoke/metrics.json`

The package has already been verified by `evidence/verification.json`.

## Folder Map

- `proposal/` - architecture, winning brief, source connector plan, roadmap, and diagram.
- `prototype/` - runnable MVP outputs, metrics, recommendation API contract, and update examples.
- `dashboard/` - sample human review dashboard.
- `evidence/` - machine-readable verification, rubric, source-health, cost, audit, rollback, duplicate, movement, and inactive-provider evidence.
- `appendix/` - supporting production controls and deeper implementation notes.
- `src/`, `scripts/`, and `data/sample/` - lightweight reproducible MVP code snapshot.
