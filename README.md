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

Upload this curated judge package to Kaggle:

```text
submissions/latest_final_package.zip
```

Start here:

1. `START_HERE.md`
2. `Provider_Directory_Update_Pipeline_End_to_End.ipynb`
3. `proposal/JUDGE_DECISION_MEMO.md`
4. `proposal/WINNING_PROPOSAL_BRIEF.md`
5. `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md`
6. `proposal/CONFIDENCE_AND_DECISION_POLICY.md`
7. `proposal/IMPLEMENTATION_ACCEPTANCE_CRITERIA.md`
8. `prototype/WORKING_PROTOTYPE.md`
9. `prototype/RECOMMENDATION_API_CONTRACT.md`
10. `proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md`
11. `proposal/SOURCE_CONNECTOR_STATUS_MATRIX.md`
12. `dashboard/index.html`
13. `evidence/verification.json`

Current verified package:

- Submission mode: Option C Hybrid, with Option A and Option B coverage included
- Package: `submissions/latest_final_package.zip`
- Verification checks passed: 89 curated-package checks
- Local proxy F1: `0.948276`
- Precision / recall: `0.948276` / `0.948276`
- Auto-apply precision: `1.0`
- Cost per correct update: `$0.005836`
- Cloud target: AWS

## Files To Show Judges

Show only the curated package path above. The intended first impression is small and deliberate:

1. `START_HERE.md`
2. `Provider_Directory_Update_Pipeline_End_to_End.ipynb`
3. `proposal/JUDGE_DECISION_MEMO.md`
4. `proposal/WINNING_PROPOSAL_BRIEF.md`
5. `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md`
6. `proposal/CONFIDENCE_AND_DECISION_POLICY.md`
7. `proposal/IMPLEMENTATION_ACCEPTANCE_CRITERIA.md`
8. `prototype/WORKING_PROTOTYPE.md`
9. `prototype/RECOMMENDATION_API_CONTRACT.md`
10. `proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md`
11. `proposal/SOURCE_CONNECTOR_STATUS_MATRIX.md`
12. `dashboard/index.html`
13. `evidence/verification.json`

Everything else in the upload is supporting evidence under `appendix/`, `evidence/`, `src/`, or `scripts/`.

## What Is Included

- `src/` - reusable pipeline modules for candidate generation, scoring, source reliability, review routing, audit, privacy, red-team checks, and production readiness.
- `scripts/` - reproducible CLI entrypoints for the best pipeline, public dataset triage, Kaggle metadata collection, and package verification.
- `docs/` - supporting research and architecture documents.
- `architecture/` - judge-facing architecture proposal, implementation map, and diagram source.
- `prototype/` - judge-facing MVP runbook and prototype artifact map.
- `notebooks/` - polished end-to-end notebook with narrative, MVP execution, metrics, diagrams, and bonus coverage.
- `RECOMMENDATION_API_CONTRACT.md` - product-facing JSON recommendation shape matching the competition examples.
- `OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md` - real-source ingestion plan for NPPES, CMS files, FSMB/state boards, practice websites, and fallback sources.
- `experiments/` - append-only experiment scripts used to evolve the solution.
- `data/sample/` - synthetic provider/evidence/gold-update benchmark used when official train/test labels are unavailable.
- `submissions/healthlynked_option_c_clean/` - curated judge-facing handoff package.
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
