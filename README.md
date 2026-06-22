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

See `FINAL_UPLOAD.md` for the current artifact SHA-256, verification command, and judge smoke-test command.

Start here:

1. `START_HERE.md`
2. `Provider_Directory_Update_Pipeline_End_to_End.ipynb`
3. `proposal/ONE_PAGE_SCORECARD.md`
4. `proposal/JUDGE_DECISION_MEMO.md`
5. `proposal/PRESENTATION_NARRATIVE.md`
6. `proposal/BONUS_COVERAGE_MATRIX.md`
7. `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md`
8. `proposal/AGENT_WORKFLOW_DIAGRAM.md`
9. `proposal/CONFIDENCE_AND_DECISION_POLICY.md`
10. `proposal/SHADOW_MODE_PILOT_PROTOCOL.md`
11. `prototype/WORKING_PROTOTYPE.md`
12. `prototype/RECOMMENDATION_API_CONTRACT.md`
13. `proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md`
14. `proposal/SOURCE_ACCESS_COMPLIANCE_POLICY.md`
15. `proposal/OFFICIAL_SOURCE_REFERENCES.md`
16. `dashboard/index.html`
17. `evidence/verification.json`

Current verified package:

- Submission mode: Option C Hybrid, with Option A and Option B coverage included
- Package: `submissions/latest_final_package.zip`
- Verification checks passed: 131 curated-package checks
- Local proxy F1: `0.948276`
- Precision / recall: `0.948276` / `0.948276`
- Auto-apply precision: `1.0`
- Prototype evidence-only cost per correct update: `$0.005836`
- Cloud reference: cloud-agnostic; AWS examples included

## Files To Show Judges

Show only the curated package path above. The intended first impression is small and deliberate:

1. `START_HERE.md`
2. `Provider_Directory_Update_Pipeline_End_to_End.ipynb`
3. `proposal/ONE_PAGE_SCORECARD.md`
4. `proposal/JUDGE_DECISION_MEMO.md`
5. `proposal/PRESENTATION_NARRATIVE.md`
6. `proposal/BONUS_COVERAGE_MATRIX.md`
7. `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md`
8. `proposal/AGENT_WORKFLOW_DIAGRAM.md`
9. `proposal/CONFIDENCE_AND_DECISION_POLICY.md`
10. `proposal/SHADOW_MODE_PILOT_PROTOCOL.md`
11. `prototype/WORKING_PROTOTYPE.md`
12. `prototype/RECOMMENDATION_API_CONTRACT.md`
13. `proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md`
14. `proposal/SOURCE_ACCESS_COMPLIANCE_POLICY.md`
15. `proposal/OFFICIAL_SOURCE_REFERENCES.md`
16. `dashboard/index.html`
17. `evidence/verification.json`

Everything else in the upload is supporting evidence under `appendix/`, `evidence/`, `src/`, or `scripts/`.

## What Is Included

- `src/` - minimal reusable MVP modules for loading, scoring, normalization, NPI validation, and review routing.
- `scripts/` - reproducible CLI entrypoints for the best pipeline, recommendation examples, package build, and package verification.
- `submissions/healthlynked_option_c_clean/prototype/RECOMMENDATION_API_CONTRACT.md` - product-facing JSON recommendation shape matching the competition examples.
- `submissions/healthlynked_option_c_clean/proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md` - real-source ingestion plan for NPPES, CMS files, PECOS, NUCC taxonomy, state boards, practice websites, and fallback sources.
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

## Production Positioning

The architecture is intentionally practical for a lean engineering team:

- deterministic source connectors before LLM fallback
- authority-tiered source reliability
- NPI and public-source validation
- field-level normalization for names, addresses, phone numbers, specialties, practice affiliations, websites, and status
- safe auto-update rules separated from update discovery
- review-first routing for identity-sensitive, conflicting, or high-risk changes
- append-only audit trail, package manifest, rollback workflow, and privacy controls
- cloud-portable scaling through object storage, managed compute, workflow orchestration, relational/key-value storage, monitoring, gated foundation-model fallback, and review queues; AWS services are used as reference examples where concrete names help.

## GitHub Notes

This repository is structured for a private GitHub handoff. It intentionally excludes `.env`, raw Kaggle zip downloads, Python caches, historical result directories, old intermediate submission zips, and reference PDFs.

The root repository is intentionally small. Internal research logs, adversarial review notes, raw Kaggle downloads, and generated caches are kept out of the judge-facing surface.
