# Public Source Governance Checklist

This checklist is operational due diligence, not legal advice. It helps a lean engineering team avoid building a provider-directory pipeline that is technically impressive but risky to run.

## Current Pipeline Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0

## Checklist

| Area | Requirement |
|---|---|
| source_terms | Confirm API terms, robots.txt, usage policies, and redistribution limits before crawling or storing data. |
| rate_limits | Set connector-specific rate limits, retries, and backoff to avoid abusive access patterns. |
| raw_snapshot_retention | Define how long raw source HTML/API payloads stay in S3 and who can access them. |
| pii_scope | Classify provider directory data and avoid collecting patient data or unrelated PII. |
| auditability | Store source URL, retrieved timestamp, parser version, confidence formula version, and reviewer disposition. |
| license_authority | Use state/license sources for license status; do not infer license validity from NPPES alone. |
| llm_controls | Send only necessary public text snippets to Bedrock or any model endpoint; log prompt/version/output. |
| human_review | Require review for stale, conflicting, high-risk, peer-mismatched, or identity-level changes. |
| appeals_rollbacks | Support rollback and correction workflow for contested updates. |
| monitoring | Monitor source freshness, connector failures, false positives, review backlog, and cost drift. |

## Deployment Gate

Before production write access is enabled:

1. Legal/product owner approves each source class.
2. AWS IAM and S3 retention policies are reviewed.
3. Review queue and rollback workflow are tested.
4. Auto-apply is launched in shadow mode first.
5. Monitoring alerts are wired to owners.

## Why This Helps The Submission

HealthLynked asked for a repeatable pipeline, not a one-off scraper. Governance, source access, auditability, and rollback design are what make the prototype credible as a system they could actually operate.
