# Official Source Connector Playbook

## Why This Matters

A judge may ask whether this proposal knows how to leave the synthetic benchmark and connect to real provider data sources. This playbook answers that question directly.

## Source Plan

| Source | Official Surface | Primary Use | Refresh Strategy | Caveat |
|---|---|---|---|---|
| NPPES API | `https://npiregistry.cms.hhs.gov/api-page` | NPI identity lookup, taxonomy/specialty, provider/practice metadata | Live lookup for risky records and reviewer drill-down | NPI issuance does not validate licensure |
| NPPES downloadable files | `https://download.cms.gov/nppes/NPI_Files.html` | Large-scale monthly/weekly batch refresh, practice locations, endpoints, deactivation file | Monthly full replacement plus weekly increments in S3 | Large files require batch ingestion |
| CMS data dissemination page | `https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination` | Governance context for FOIA-disclosable NPPES fields and deactivation files | Use as source-policy reference | NPPES data is provider-reported and may lag reality |
| FSMB / state licensing | `https://www.fsmb.org/data-integration/` and state board sites | License status, sanctions, disciplinary data, inactive/retired signals | Paid/API/MFT where available, state-board connectors otherwise | Access terms vary; do not treat as free universal API |
| Practice websites | Provider roster, phone, address, accepting-new-patients, location pages | Risk-triggered crawl and deterministic extraction | Respect robots/terms; snapshot evidence |
| Health-system directories | Provider affiliation, roster, locations, specialty labels | Risk-triggered crawl, health-system connector templates | Stronger for affiliation than NPI |
| Business listings | Phone/address fallback | Only fresh, field-gated, low-weight fallback | Never authoritative for identity or inactive status |

## AWS Ingestion Pattern

1. EventBridge schedules source refreshes.
2. Step Functions selects connector jobs by risk tier and source SLA.
3. Lambda handles light API lookups.
4. ECS/Fargate or AWS Batch handles large downloadable files and crawlers.
5. Raw snapshots land in versioned S3 partitions.
6. Normalized evidence lands in RDS/DynamoDB.
7. Scoring tasks emit recommendation JSON, review queue rows, and audit events.

## Production Guardrails

- Never use NPPES alone to assert licensure.
- Never use business listings for identity, specialty, license, or inactive status.
- Require source URL, retrieval timestamp, parser version, and evidence hash.
- Route source conflicts to review unless field-specific authority rules resolve them.
- Calibrate source weights against HealthLynked reviewer outcomes.

## First Three Connectors To Build

1. **NPPES API plus downloadable files:** identity, taxonomy, deactivation, and practice location baseline.
2. **Practice website connector:** highest practical value for phone, address, roster, and accepting-new-patients.
3. **State license/FSMB lane:** active/inactive and disciplinary/source-of-truth status signals.

## References

- NPPES API: https://npiregistry.cms.hhs.gov/api-page
- NPPES files: https://download.cms.gov/nppes/NPI_Files.html
- CMS data dissemination: https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination
- FSMB data integration: https://www.fsmb.org/data-integration/
