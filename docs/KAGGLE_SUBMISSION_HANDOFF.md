# Kaggle Submission Handoff

## Upload File

Upload `submissions/latest_final_package.zip`.

## Suggested Submission Title

Option C Hybrid Provider Directory Quality Control Plane

## Suggested Submission Description

This Option C hybrid submission combines a runnable provider/practice directory update MVP with an AWS-oriented production architecture. It includes source-governed candidate updates, deterministic normalization, provider/practice/location matching, confidence scoring, safe auto-apply thresholds, human review routing, audit/rollback artifacts, source access controls, bonus-capability evidence, and a 90-day implementation plan for the expected post-award consulting engagement.

Key proof points:

- Verified package checks: 150 curated-package checks
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
5. `proposal/PRESENTATION_NARRATIVE.md`
6. `proposal/BONUS_COVERAGE_MATRIX.md`
7. `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md`
8. `proposal/AGENT_WORKFLOW_DIAGRAM.md`
9. `proposal/CONFIDENCE_AND_DECISION_POLICY.md`
10. `proposal/IMPLEMENTATION_ACCEPTANCE_CRITERIA.md`
11. `proposal/SHADOW_MODE_PILOT_PROTOCOL.md`
12. `prototype/WORKING_PROTOTYPE.md`
13. `prototype/RECOMMENDATION_API_CONTRACT.md`
14. `proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md`
15. `proposal/SOURCE_CONNECTOR_STATUS_MATRIX.md`
16. `proposal/SOURCE_ACCESS_COMPLIANCE_POLICY.md`
17. `proposal/OFFICIAL_SOURCE_REFERENCES.md`
18. `dashboard/index.html`
19. `evidence/verification.json`

## Verify Before Upload

```bash
python3 scripts/verify_pipeline.py --package submissions/latest_final_package.zip --out-dir outputs/final_preupload_verify
```
