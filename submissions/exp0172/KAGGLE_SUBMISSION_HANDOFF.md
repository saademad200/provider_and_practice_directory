# Kaggle Submission Handoff

## Upload File

Upload `submissions/latest_final_package.zip`.

## Suggested Submission Title

Combined Option A/B/C Provider Directory Update Pipeline

## Suggested Submission Description

This submission intentionally combines all three allowed paths: Option A technical architecture, Option B working prototype, and Option C hybrid production scale plan. It includes a runnable provider/practice directory update MVP, an AWS-oriented production operating model, source-governed candidate updates, confidence scoring, safe auto-apply thresholds, human review routing, audit/rollback artifacts, source reliability controls, public-notebook gap analysis, and a 42,000-row Kaggle-adjacent provider-directory transfer check with a reusable CLI.

Key proof points:

- Verified package checks: 213
- Local proxy F1: 0.948276
- Precision/recall: 0.948276 / 0.948276
- Auto-apply precision: 1.0
- Public dataset CLI smoke: 42,000 Kaggle-adjacent rows processed
- Cloud target: AWS

Recommended first files for judges:

1. `Provider_Directory_Update_Pipeline_End_to_End.ipynb`
2. `WINNING_PROPOSAL_BRIEF.md`
3. `ADVERSARIAL_JUDGE_AUDIT.md`
4. `RECOMMENDATION_API_CONTRACT.md`
5. `ONE_PAGE_JUDGE_GUIDE.md`
6. `TECHNICAL_ARCHITECTURE_PROPOSAL.md`
7. `WORKING_PROTOTYPE.md`
8. `ARCHITECTURE_DIAGRAM.md`
9. `IMPLEMENTATION_ROADMAP_90_DAYS.md`
10. `verification.json`

## Verify Before Upload

```bash
python3 scripts/verify_pipeline.py --package submissions/latest_final_package.zip --out-dir outputs/final_preupload_verify
```
