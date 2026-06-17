# Kaggle Submission Instructions

Submit:

```text
submissions/latest_final_package.zip
```

Suggested title:

```text
Option C Hybrid: Auditable AI Provider Directory Update Pipeline
```

Suggested description:

```text
This is an Option C hybrid submission: a runnable provider/practice directory update MVP plus an AWS-ready production architecture. It detects outdated or risky records, searches trusted public sources, normalizes provider/practice fields, matches records, assigns confidence, separates safe auto-updates from human review, and maintains evidence-backed audit and rollback trails.

Key proof points: 191 verification checks passed; local proxy F1 0.948276; precision/recall 0.948276/0.948276; auto-apply precision 1.0; cost per correct update $0.005836; includes source governance, confidence scoring, human review dashboard, duplicate/movement/inactive-provider detection, NPI validation, audit log, rollback plan, and AWS scaling roadmap.

Recommended first files: ONE_PAGE_JUDGE_GUIDE.md, COMBINED_ABC_PIPELINE_COVERAGE.md, EXECUTIVE_SUMMARY.md, KAGGLE_SUBMISSION_HANDOFF.md, ARTIFACT_INDEX.md.
```

Pre-upload verification:

```bash
python3 scripts/verify_pipeline.py \
  --package submissions/latest_final_package.zip \
  --out-dir outputs/final_preupload_verify
```

Expected result:

```text
"passed": true
```
