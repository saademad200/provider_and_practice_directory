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

Key proof points: 131 curated-package verification checks passed; local proxy F1 0.948276; precision/recall 0.948276/0.948276; auto-apply precision 1.0; cost per correct update $0.005836; includes source governance, confidence scoring, human review dashboard, duplicate/movement/inactive-provider detection, NPI validation, official-source connector plan, audit log, rollback plan, and AWS scaling roadmap.

Recommended first files: START_HERE.md, Provider_Directory_Update_Pipeline_End_to_End.ipynb, proposal/ONE_PAGE_SCORECARD.md, proposal/JUDGE_DECISION_MEMO.md, proposal/WINNING_PROPOSAL_BRIEF.md, proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md, proposal/CONFIDENCE_AND_DECISION_POLICY.md, proposal/IMPLEMENTATION_ACCEPTANCE_CRITERIA.md, prototype/WORKING_PROTOTYPE.md, prototype/RECOMMENDATION_API_CONTRACT.md, proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md, proposal/SOURCE_CONNECTOR_STATUS_MATRIX.md, dashboard/index.html, evidence/verification.json.
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
