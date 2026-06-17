# Source Connector Registry And Evidence Tool Manifest

This experiment turns source strategy into an inspectable contract. Each connector has authority rank, fields covered, freshness SLA, cache policy, cost posture, health check, fallback, and auto-apply role. The JSON manifest follows the same spirit as agent tool contracts: agents discover what each source can do and what it is forbidden to do.

## Current Quality Context

- F1: 0.93913
- Precision: 0.947368
- Recall: 0.931034
- Auto-apply precision: 1.0

## Connector Registry

| Connector | Source Type | Authority Rank | Freshness SLA Days | Cost Tier | Auto-Apply Role |
|---|---|---:|---:|---|---|
| nppes_npi_registry | official_api | 1 | 7 | free_public | identity and specialty support, never sole practice-affiliation authority |
| cms_provider_data_catalog | official_dataset_api | 2 | 30 | free_public | supporting evidence for organization/practice and Medicare-facing participation |
| state_license_board | official_state_source | 1 | 14 | free_or_low_cost | highest authority for inactive/probation license status after identity match |
| practice_website | public_web | 3 | 21 | crawler_compute | strong for phone/address only with peer or second-source confirmation |
| health_system_directory | public_web_or_partner_feed | 2 | 14 | crawler_or_partner_feed | strong for affiliation/roster when identity and location agree |
| business_listing | third_party_listing | 5 | 45 | paid_or_rate_limited | review-only weak signal because ablation showed quality/cost risk |

## Health-Check Fixture

| Connector | Expected Status | Freshness SLA Days | Required Failure Action |
|---|---|---:|---|
| nppes_npi_registry | ok | 7 | mark stale, block auto-apply if min-source policy fails, emit CloudWatch alert |
| cms_provider_data_catalog | ok | 30 | mark stale, block auto-apply if min-source policy fails, emit CloudWatch alert |
| state_license_board | ok | 14 | mark stale, block auto-apply if min-source policy fails, emit CloudWatch alert |
| practice_website | ok | 21 | mark stale, block auto-apply if min-source policy fails, emit CloudWatch alert |
| health_system_directory | ok | 14 | mark stale, block auto-apply if min-source policy fails, emit CloudWatch alert |
| business_listing | disabled | 45 | mark stale, block auto-apply if min-source policy fails, emit CloudWatch alert |

## Official Source References

- NPPES NPI Registry API: https://npiregistry.cms.hhs.gov/api-page
- CMS Provider Data Catalog API docs: https://data.cms.gov/provider-data/docs
- CMS Data API docs: https://data.cms.gov/api-docs

## Production Rules

- Every source tool is read-only or append-only; no connector can mutate the directory.
- Authority rank is field-specific context, not blanket truth. State boards outrank all sources for license status; practice and health-system pages are stronger for current location/roster.
- Business listings remain disabled in the current best config and review-only if reintroduced.
- Freshness failures must mark evidence stale, block unsafe auto-apply routes, and emit monitoring events.
- Health-check outputs should be written to S3 and CloudWatch before each Step Functions batch proceeds to scoring.
