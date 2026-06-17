# External Source Strategy And Freshness Plan

This plan is based on official CMS/HHS documentation checked on 2026-06-16. It explains how the prototype should scale from synthetic evidence into a legally accessible production evidence pipeline.

## Current Prototype Anchor

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Review count: 38

## Source Plan

| Source | Role | Freshness | Pipeline Use | Risk / Guardrail | Reference |
|---|---|---|---|---|---|
| NPPES NPI Registry API | Low-cost point lookup for NPI, provider name, taxonomy, mailing/practice addresses, and organization records. | Daily query path for targeted lookups. | Use for identity anchoring, NPI validation, baseline address/name/specialty evidence, and lightweight refreshes. | NPI issuance does not prove license/credential validity, so never use NPPES alone for license status. | https://npiregistry.cms.hhs.gov/api-page |
| NPPES monthly V2 downloadable files | Bulk refresh of FOIA-disclosable NPPES provider data. | Monthly full replacement plus weekly incrementals. | Maintain a local searchable NPI cache; ingest practice-location, other-name, endpoint, and deactivation references. | Large files require batch ingestion and schema/version monitoring. | https://download.cms.gov/nppes/NPI_Files.html |
| NPPES deactivation data | Detect deactivated NPIs and avoid stale identities. | Monthly deactivation file and weekly incremental updates. | Route deactivated/reactivated NPI evidence to high-priority review unless corroborated by authoritative status sources. | CMS warns deactivated NPI records should not be used in standard transactions. | https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination |
| CMS Provider Data Catalog / Medicare Care Compare | Doctors, clinicians, groups, practice locations, affiliations, and public profile context. | CMS states general profile information such as addresses and phones is updated monthly. | Cross-check group affiliations, locations, demographic fields, and Medicare-facing profile data. | Some profile changes may take months to propagate from PECOS; do not treat as the sole real-time source. | https://www.cms.gov/medicare/quality/physician-compare-initiative/about-data |
| Practice websites and health-system pages | Fastest public signal for moves, phone changes, location closures, rebrands, accepting-patient status, and direct patient-facing contact info. | Crawl with per-domain cache TTL and change detection. | High-value evidence for phone/address/status updates; use deterministic extraction first and LLM fallback only for messy pages. | Scraping constraints, duplicate locations, marketing pages, and stale pages require robots/legal review and citations. | Practice or health-system public websites |
| State licensing boards | Authoritative license status, discipline, inactive/retired signals, and credential confirmation. | State-dependent; monitor source-specific update cadence. | Primary authority for license_status and safety review routing. | Fragmented schemas, different access terms, and state-specific identifiers require adapters. | State-specific licensing board portals |

## Freshness SLAs

| Evidence Tier | Examples | Suggested SLA | Action When Stale |
|---|---|---:|---|
| Authoritative identity | NPPES full file, NPPES API, NPPES deactivation | Daily API for targeted records; weekly incremental; monthly full replacement | Keep old value but lower confidence; mark stale_source in review reason |
| Authoritative license | State board/license source | State-specific, target weekly to monthly | Never auto-apply license changes without fresh authority |
| Public profile | CMS Provider Data Catalog / Medicare Care Compare | Monthly | Use as corroborating evidence, not sole high-risk proof |
| Patient-facing web | Practice websites, health-system profile pages | Weekly for high-risk/stale records, monthly otherwise | Re-crawl before auto-apply if cached page is stale |
| Low-reliability aggregators | Business listings | Disabled by default | Use only as weak discovery hints, not scoring evidence |

## Why This Is Stronger Than Generic Agent Search

- It separates authoritative identity, license authority, public profile, patient-facing web, and low-reliability aggregator evidence.
- It gives each source a freshness SLA and a failure mode.
- It uses official bulk files for scale and APIs/crawlers for targeted changes.
- It routes stale, conflicting, or missing evidence to review instead of forcing unsafe updates.
- It creates a path to active learning: human review outcomes can recalibrate source weights and freshness thresholds.

## Official References

- NPPES API: https://npiregistry.cms.hhs.gov/api-page
- NPPES downloadable files: https://download.cms.gov/nppes/NPI_Files.html
- CMS NPPES data dissemination: https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination
- CMS Provider Data Catalog: https://data.cms.gov/provider-data/
- CMS Provider Data Catalog API docs: https://data.cms.gov/provider-data/docs
- CMS Doctors and Clinicians data background: https://www.cms.gov/medicare/quality/physician-compare-initiative/about-data
