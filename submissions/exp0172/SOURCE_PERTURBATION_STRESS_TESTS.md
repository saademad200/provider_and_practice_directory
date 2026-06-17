# Source Perturbation Stress Tests

Post-fallback refresh using the promoted fresh business-listing configuration.

- Baseline F1: 0.948276
- Baseline auto-apply precision: 1.0

| Scenario | F1 | F1 Delta | Auto Precision | Review Count | Cost/Correct |
|---|---:|---:|---:|---:|---:|
| baseline_fresh_business | 0.948276 | 0.0 | 1.0 | 38 | 0.005836 |
| no_practice_website | 0.884615 | -0.063661 | 1.0 | 41 | 0.002709 |
| no_health_system | 0.843137 | -0.105139 | 1.0 | 39 | 0.004033 |
| no_business_listing | 0.93913 | -0.009146 | 1.0 | 37 | 0.005609 |
| public_registry_only | 0.15873 | -0.789546 | 1.0 | 0 | 0.0015 |
| stale_source_penalty | 0.93913 | -0.009146 | 1.0 | 37 | 0.005896 |
