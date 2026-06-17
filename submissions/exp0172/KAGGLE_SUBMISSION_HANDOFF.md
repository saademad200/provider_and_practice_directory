# Kaggle Submission Handoff

## Upload File

Upload `submissions/latest_final_package.zip`.

## Suggested Submission Title

Combined Option A/B/C Provider Directory Update Pipeline

## Suggested Submission Description

This submission intentionally combines all three allowed paths: Option A technical architecture, Option B working prototype, and Option C hybrid production scale plan. It includes a runnable provider/practice directory update MVP, an AWS-oriented production operating model, source-governed candidate updates, confidence scoring, safe auto-apply thresholds, human review routing, audit/rollback artifacts, source reliability controls, public-notebook gap analysis, and a 42,000-row Kaggle-adjacent provider-directory transfer check with a reusable CLI.

Key proof points:

- Verified package checks: 191
- Local proxy F1: 0.948276
- Precision/recall: 0.948276 / 0.948276
- Auto-apply precision: 1.0
- Public dataset CLI smoke: 42,000 Kaggle-adjacent rows processed
- Cloud target: AWS

Recommended first files for judges:

1. `Provider_Directory_Update_Pipeline_End_to_End.ipynb`
2. `ONE_PAGE_JUDGE_GUIDE.md`
3. `TECHNICAL_ARCHITECTURE_PROPOSAL.md`
4. `WORKING_PROTOTYPE.md`
5. `ARCHITECTURE_DIAGRAM.md`
6. `COMBINED_ABC_PIPELINE_COVERAGE.md`
7. `verification.json`

## Verify Before Upload

```bash
python3 scripts/verify_pipeline.py --package submissions/latest_final_package.zip --out-dir outputs/final_preupload_verify
```
