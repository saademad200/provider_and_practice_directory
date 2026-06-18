# Kaggle Submission Handoff

## Upload File

Upload `submissions/latest_final_package.zip`.

## Suggested Submission Title

Option C Hybrid Provider Directory Quality Control Plane

## Suggested Submission Description

This Option C hybrid submission combines a runnable provider/practice directory update MVP with an AWS-oriented production architecture. It includes source-governed candidate updates, deterministic normalization, provider/practice/location matching, confidence scoring, safe auto-apply thresholds, human review routing, audit/rollback artifacts, source access controls, bonus-capability evidence, and a 90-day implementation plan for the expected post-award consulting engagement.

Key proof points:

- Verified package checks: 101 curated-package checks
- Local proxy F1: 0.948276
- Precision/recall: 0.948276 / 0.948276
- Auto-apply precision: 1.0
- Bonus coverage matrix: included
- Manual unzip-and-run smoke: passed
- Cloud target: AWS

Recommended first files for judges:

1. `START_HERE.md`
2. `Provider_Directory_Update_Pipeline_End_to_End.ipynb`
3. `proposal/WINNING_PROPOSAL_BRIEF.md`
4. `proposal/JUDGE_DECISION_MEMO.md`
5. `proposal/BONUS_COVERAGE_MATRIX.md`
6. `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md`
7. `proposal/CONFIDENCE_AND_DECISION_POLICY.md`
8. `prototype/WORKING_PROTOTYPE.md`
9. `prototype/RECOMMENDATION_API_CONTRACT.md`
10. `proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md`
11. `dashboard/index.html`
12. `evidence/verification.json`

## Verify Before Upload

```bash
python3 scripts/verify_pipeline.py --package submissions/latest_final_package.zip --out-dir outputs/final_preupload_verify
```
