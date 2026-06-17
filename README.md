# Provider Practice Directory Update Pipeline

Option C hybrid submission for the Kaggle **Provider & Practice Directory Update Pipeline** competition: a working MVP plus a production-grade architecture for continuously finding, validating, scoring, reviewing, and auditing provider/practice directory updates.

The submission target is HealthLynked's requested operating model:

```text
Provider/practice directory
  -> outdated/risky record detection
  -> trusted public source search
  -> normalization and entity matching
  -> confidence scoring
  -> no-change, safe auto-update, or human review
  -> audit log, rollback, and directory update
```

## Judge Path

Upload this file to Kaggle:

```text
submissions/latest_final_package.zip
```

Start here:

1. `notebooks/Provider_Directory_Update_Pipeline_End_to_End.ipynb`
2. `WINNING_PROPOSAL_BRIEF.md`
3. `submissions/exp0172/ONE_PAGE_JUDGE_GUIDE.md`
4. `submissions/exp0172/TECHNICAL_ARCHITECTURE_PROPOSAL.md`
5. `submissions/exp0172/WORKING_PROTOTYPE.md`
6. `submissions/exp0172/ARCHITECTURE_DIAGRAM.md`
7. `IMPLEMENTATION_ROADMAP_90_DAYS.md`
8. `submissions/exp0172/COMBINED_ABC_PIPELINE_COVERAGE.md`
9. `submissions/exp0172/KAGGLE_SUBMISSION_HANDOFF.md`

Current verified package:

- Submission mode: Option C Hybrid, with Option A and Option B coverage included
- Package: `submissions/latest_final_package.zip`
- Verification checks passed: 191
- Local proxy F1: `0.948276`
- Precision / recall: `0.948276` / `0.948276`
- Auto-apply precision: `1.0`
- Cost per correct update: `$0.005836`
- Cloud target: AWS

## What Is Included

- `src/` - reusable pipeline modules for candidate generation, scoring, source reliability, review routing, audit, privacy, red-team checks, and production readiness.
- `scripts/` - reproducible CLI entrypoints for the best pipeline, public dataset triage, Kaggle metadata collection, and package verification.
- `docs/` - working research and architecture documents.
- `architecture/` - judge-facing architecture proposal, implementation map, and diagram source.
- `prototype/` - judge-facing MVP runbook and prototype artifact map.
- `notebooks/` - polished end-to-end notebook with narrative, MVP execution, metrics, diagrams, and bonus coverage.
- `autoresearch/` - self-improvement loop state, playbook, hypotheses, journal, and leaderboard.
- `experiments/` - append-only experiment scripts used to evolve the solution.
- `data/sample/` - synthetic provider/evidence/gold-update benchmark used when official train/test labels are unavailable.
- `submissions/exp0172/` - final judge-facing handoff package.
- `submissions/latest_final_package.zip` - upload-ready Kaggle package.

## Run The Prototype

Create an environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the current best MVP pipeline:

```bash
python3 scripts/run_best_pipeline.py --out-dir outputs/local_best
```

Verify the upload package:

```bash
python3 scripts/verify_pipeline.py \
  --package submissions/latest_final_package.zip \
  --out-dir outputs/verify_latest
```

Optional public-provider-directory triage smoke:

```bash
python3 scripts/run_public_dataset_triage.py \
  --input data/raw/kaggle_public_provider_directory/provider_directory_dataset.csv \
  --out-dir outputs/public_dataset_triage \
  --top-n 100
```

## Production Positioning

The architecture is intentionally practical for a lean engineering team:

- deterministic source connectors before LLM fallback
- authority-tiered source reliability
- NPI and public-source validation
- field-level normalization for names, addresses, phone numbers, specialties, practice affiliations, websites, and status
- safe auto-update rules separated from update discovery
- review-first routing for identity-sensitive, conflicting, or high-risk changes
- append-only audit trail, package manifest, rollback workflow, and privacy controls
- AWS-oriented scaling through S3, Lambda/ECS, Step Functions, RDS/DynamoDB, EventBridge, CloudWatch, Bedrock fallback, and human-review queues

## GitHub Notes

This repository is structured for a private GitHub handoff. It intentionally excludes `.env`, raw Kaggle zip downloads, Python caches, historical result directories, old intermediate submission zips, and reference PDFs.

See `GITHUB_REPO_HANDOFF.md` for push commands and repository settings.
