# Start Here

This is the curated judge package for the HealthLynked Provider / Practice Directory Update Pipeline competition.

## 90-Second Read

This is an Option C hybrid submission: a runnable MVP plus an AWS-ready production architecture. The core idea is a provider-directory quality control plane, not a one-time cleanup script. It collects trusted evidence, normalizes fields, resolves provider/practice/location identity, scores confidence, routes uncertain changes to review, safely auto-updates only low-risk high-confidence fields, and records an audit/rollback trail for every recommendation.

Proof points:

- F1 `0.948276`, precision `0.948276`, recall `0.948276`
- safe auto-apply precision `1.0`
- estimated cost per correct update `$0.005836`
- 103 curated-package verification checks
- self-contained unzip-and-run MVP smoke test passes
- AWS production plan with source governance, review operations, monitoring, and rollback

Why it should win: it is immediately implementable after the competition. The package includes the technical architecture, working prototype, confidence policy, connector operating model, human review workflow, audit trail, cost controls, and post-award acceptance criteria.

## Recommended Judge Path

1. Open `Provider_Directory_Update_Pipeline_End_to_End.ipynb` for the narrated end-to-end walkthrough.
2. Read `proposal/WINNING_PROPOSAL_BRIEF.md` for the executive case.
3. Read `proposal/JUDGE_DECISION_MEMO.md` for the consulting-ready business case.
4. Read `proposal/PRESENTATION_NARRATIVE.md` for the pitch story.
5. Read `proposal/JUDGE_COMPARISON_MATRIX.md` for the fast comparison against likely alternatives.
6. Read `proposal/BONUS_COVERAGE_MATRIX.md` for bonus-point evidence links.
7. Read `proposal/TECHNICAL_ARCHITECTURE_PROPOSAL.md` and `proposal/ARCHITECTURE_DIAGRAM.md` for the production architecture.
8. Read `proposal/CONFIDENCE_AND_DECISION_POLICY.md` for the exact auto-update and review policy.
9. Read `proposal/IMPLEMENTATION_ACCEPTANCE_CRITERIA.md` for the post-award delivery gates.
10. Read `prototype/WORKING_PROTOTYPE.md` and inspect `prototype/metrics.json` for the runnable MVP.
11. Read `proposal/EVALUATION_LIMITS_AND_TRANSFER_PLAN.md` for how proxy metrics transfer to HealthLynked data.
12. Read `proposal/LEAN_TEAM_OPERATING_MODEL.md` and `proposal/FAILURE_MODE_PLAYBOOK.md` for production operations.
13. Open `prototype/RECOMMENDATION_API_CONTRACT.md` for the exact update recommendation shape.
14. Open `proposal/OFFICIAL_SOURCE_CONNECTOR_PLAYBOOK.md`, `proposal/SOURCE_CONNECTOR_STATUS_MATRIX.md`, `proposal/SOURCE_ACCESS_COMPLIANCE_POLICY.md`, and `proposal/OFFICIAL_SOURCE_REFERENCES.md` for trusted-source operations.
15. Inspect `dashboard/index.html` for the sample human review experience.
16. Use `evidence/verification.json` and `evidence/judge_rubric_self_eval.csv` to audit the claims.

## Run The MVP

From inside the unzipped package:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 scripts/run_best_pipeline.py --out-dir outputs/judge_smoke
```

The run writes candidate updates, safe auto-apply updates, human-review queue, config, and metrics under `outputs/judge_smoke/`. The expected proof point is the same as the packaged evidence: F1 `0.948276`, safe auto-apply precision `1.0`, and cost per correct update `$0.005836`.

## Why The Package Is Structured This Way

The first layer is intentionally small: notebook, proposal, prototype, architecture, API contract, source plan, dashboard, and verification. Supporting material is organized under `appendix/` and `evidence/` so judges can go deep without being forced through a flat folder of internal research files.
