# Judging Narrative

This competition provides no official train/test data, so the solution is framed as an applied AI pipeline rather than a leaderboard model. The submission is Option C Hybrid: a runnable prototype plus a production-grade implementation plan.

## Why This Can Win

- It solves the actual operational problem: keeping provider and practice records fresh continuously, not performing one-time cleanup.
- It separates evidence gathering, candidate generation, confidence scoring, auto-apply safety, human review, and audit logging.
- It is cost-aware: cheap public sources are preferred, guarded business-listing fallback is used only for fresh phone/address evidence, and expensive extraction can be gated.
- It is auditable: every proposed update carries sources, URLs, confidence, before/after values, review reasons, and priority drivers.
- It is safe: auto-apply is conservative, practice-peer mismatches route to review, and high-risk review items are prioritized.
- It is honest: the synthetic benchmark is documented with limitations, leakage controls, and concrete failure cases.

## Current Verified Local Proxy

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Auto-apply count: 3
- Review count: 55
- Cost per correct update: $0.005836
- Estimated evidence cost: $0.321

## What To Emphasize In Submission

- No official dataset was provided; the project supplies its own reproducible validation harness.
- The output is not just predictions; it is an operational update workflow.
- Healthcare directory changes require citation, source reliability, auditability, and review controls.
- The pipeline starts deterministic and uses optional AI extraction only where messy web text needs it.
- The final package includes verification evidence and judge-friendly examples.
