# Cost Model Per 1,000 Records

This model separates evidence retrieval cost from reviewer labor. In production, reviewer labor is expected to dominate cost, so the main optimization is reducing unnecessary review through source caching, field risk gates, and shadow mode calibration.

## Evidence retrieval scenarios

| Scenario | Public bulk data | Targeted public pages | LLM fallback | Estimated evidence cost per 1,000 records |
|---|---:|---:|---:|---:|
| Cached steady state | High | Low | Near zero | $3 to $8 |
| Normal refresh | Medium | Medium | Low | $8 to $25 |
| High risk campaign | Medium | High | Bounded | $25 to $75 |

## Manual review scenarios

| Scenario | Review rate | Minutes per case | Reviewer cost assumption | Estimated labor per 1,000 records |
|---|---:|---:|---:|---:|
| Mature policy | 5 percent | 2 | $25 per hour | $41.67 |
| Early pilot | 15 percent | 3 | $25 per hour | $187.50 |
| High risk refresh | 30 percent | 4 | $25 per hour | $500.00 |

## MVP evidence cost

The included synthetic benchmark run produced 58 candidate updates with total evidence cost `$0.321` and cost per correct update `$0.005836`. This is a prototype evidence only metric. It excludes production labor, cloud monitoring, source access agreements, and dashboard operations.
