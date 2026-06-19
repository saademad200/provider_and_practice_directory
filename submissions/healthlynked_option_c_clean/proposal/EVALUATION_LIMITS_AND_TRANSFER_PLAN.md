# Evaluation Limits And Transfer Plan

## Why This Exists

The competition does not provide an official labeled train/test split for provider-directory updates. The prototype therefore uses a controlled proxy benchmark to prove the mechanics of the pipeline: evidence normalization, candidate generation, confidence scoring, review routing, audit output, and safe auto-update behavior.

The proxy metrics should be read as a reproducible engineering signal, not as a claim that real HealthLynked production precision is already known.

## What The Current Metrics Prove

| Metric | Current Value | What It Proves |
|---|---:|---|
| F1 | `0.948276` | The pipeline can recover known synthetic/proxy updates while limiting false recommendations. |
| Precision | `0.948276` | The candidate-generation and matching logic is not simply over-producing changes. |
| Recall | `0.948276` | The evidence aggregation catches most expected changes in the proxy benchmark. |
| Auto-apply precision | `1.0` | The safe-write gate is stricter than the change-detection gate. |
| Prototype evidence-only cost per correct update | `$0.005836` | The deterministic-source-first design keeps evidence cost low in the prototype; production per-1,000 scenarios add AWS, LLM fallback, and review labor. |

## What The Current Metrics Do Not Prove

- They do not prove real HealthLynked production precision without shadow-mode validation.
- They do not prove every state-board connector behaves identically.
- They do not prove practice websites are always legally or technically accessible.
- They do not justify immediate production auto-update for identity-sensitive fields.
- They do not eliminate the need for reviewer calibration and source monitoring.

## Transfer Plan To HealthLynked Data

| Phase | Goal | Acceptance Signal |
|---|---|---|
| Shadow sample | Run on de-identified HealthLynked records without writing changes | Candidate/review/audit outputs generated successfully |
| Reviewer calibration | Compare recommendations against HealthLynked operations decisions | Precision, rejection reasons, and reviewer edits measured by field/source |
| Source calibration | Tune authority tiers and freshness windows from observed source quality | Source-specific accept/reject rates and conflict rates |
| Threshold calibration | Adjust auto-update thresholds by field risk | Safe low-risk fields exceed agreed precision threshold |
| Limited production | Enable auto-update only for approved low-risk fields | Audit coverage and rollback readiness remain 100% |

## Evaluation Design For Production

1. Sample records by field risk, source type, specialty, geography, and practice size.
2. Label reviewer decisions as accept, reject, edit, defer, recrawl, or suppress.
3. Track precision/recall by field, source, freshness, confidence band, and practice group.
4. Separate detection quality from write-eligibility quality.
5. Keep high-risk changes review-first until the evidence base proves otherwise.

## Judge Takeaway

The important point is not that proxy F1 alone wins the competition. The important point is that the submission has a measured, reproducible prototype and a responsible transfer plan for converting that prototype into a production HealthLynked workflow without pretending the benchmark is the live business.
