# Missing-Source Robustness

This diagnostic answers a production question: if a source is unavailable, stale, legally inaccessible, rate-limited, or blocked, how does the pipeline degrade?

Baseline uses business listings disabled because source ablation showed they hurt quality and cost.

## Baseline

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply count: 3
- Review count: 55

## Source Drop Results

| Scenario | Disabled Sources | F1 | Precision | Recall | Auto Count | Review Count | Delta F1 | Interpretation |
|---|---|---:|---:|---:|---:|---:|---:|---|
| authoritative_only | business_listing, health_system, practice_website | 0.15873 | 1.0 | 0.086207 | 5 | 0 | -0.7804 | Registry/license-only fallback |
| drop_web_and_health | business_listing, health_system, practice_website | 0.15873 | 1.0 | 0.086207 | 5 | 0 | -0.7804 | Two rich web-style sources unavailable |
| web_only_no_registry | business_listing, nppes, state_license | 0.75 | 0.947368 | 0.62069 | 0 | 38 | -0.18913 | Web evidence without registry/license |
| drop_health_system | business_listing, health_system | 0.808081 | 0.97561 | 0.689655 | 5 | 36 | -0.131049 | Health-system source unavailable |
| drop_nppes | business_listing, nppes | 0.811881 | 0.953488 | 0.706897 | 5 | 38 | -0.127249 | Cheap registry unavailable |
| drop_practice_website | business_listing, practice_website | 0.851485 | 1.0 | 0.741379 | 5 | 38 | -0.087645 | Practice website unavailable |
| drop_state_license | business_listing, state_license | 0.890909 | 0.942308 | 0.844828 | 15 | 37 | -0.048221 | License source unavailable |

## Design Implications

- Source loss should reduce automation before it creates unsafe updates.
- License status is intentionally dependent on authoritative license evidence.
- Practice websites and health-system sources are high-value for phone/address updates and should get caching, retries, and freshness monitoring.
- NPPES should be treated as cheap baseline evidence, but not the only proof for high-risk fields.
- In production, missing-source scenarios should trigger coverage alerts and review-queue labeling.
