# Cost Model Per 1,000 Provider Records

This is a parameterized operating-cost model, not a live AWS bill. Cloud and LLM prices change, so the model keeps assumptions explicit and easy to replace.

## Current Prototype Inputs

- Estimated source evidence cost: $0.321 for 58 proposed updates
- Cost per correct update: $0.005836
- Review count: 55
- Auto-apply count: 3

## Default Assumptions

- `records_per_1000`: 1000
- `source_evidence_cost_per_record`: 0.00446
- `aws_batch_etl_per_1000`: 0.15
- `aws_storage_monitoring_per_1000`: 0.05
- `llm_extraction_call_cost`: 0.01
- `llm_extraction_rate`: 0.08
- `manual_review_minutes`: 1.5
- `manual_review_hourly_cost`: 30.0
- `manual_review_rate`: 0.37

## Scenario Estimates

| Scenario | Evidence | AWS Compute/Storage/Monitoring | LLM Extraction | Manual Review | Review Items | Total / 1,000 |
|---|---:|---:|---:|---:|---:|---:|
| base_case | 4.46 | 0.2 | 0.8 | 277.5 | 370.0 | 282.96 |
| llm_heavy | 4.46 | 0.2 | 2.5 | 277.5 | 370.0 | 284.66 |
| review_heavy | 4.46 | 0.2 | 0.8 | 450.0 | 600.0 | 455.46 |
| mature_auto_apply | 4.46 | 0.2 | 0.5 | 135.0 | 180.0 | 139.96 |

The proxy benchmark is intentionally enriched for risky/outdated records, so its raw review queue rate is not used as the production base-case rate. The `manual_review_rate` assumption is a planning target that HealthLynked can recalibrate from reviewer disposition data during shadow mode.

## Cost-Control Levers

- Disable low-value sources by measured ablation, as done with business listings.
- Use deterministic extraction first; call Bedrock only for pages that fail parsers or have high-value stale fields.
- Re-fetch stale evidence before review to avoid wasting reviewer time.
- Use active learning to expand auto-apply only where reviewer accept rates are strong.
- Batch large public files through AWS Glue/Batch and reserve API/crawler work for changed or high-risk records.

## Why This Matters

HealthLynked asked for a repeatable, cost-efficient pipeline. This model lets judges see how manual review dominates cost and why source quality, freshness, and safe auto-apply are the real economic levers.
