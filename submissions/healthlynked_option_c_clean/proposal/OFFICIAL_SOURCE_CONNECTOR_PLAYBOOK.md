# Official Source Connector Playbook

## Purpose

This playbook shows how the MVP leaves synthetic fixtures and connects to real public or governed provider sources.

| Source | Official Surface | Use | Caveat |
|---|---|---|---|
| NPPES API | `https://npiregistry.cms.hhs.gov/api-page` | NPI identity lookup, taxonomy, metadata | NPI does not validate licensure |
| NPPES downloadable files | `https://download.cms.gov/nppes/NPI_Files.html` | Monthly/weekly batch refresh, deactivation files, practice locations, endpoints | Large files need batch ingestion |
| CMS data dissemination | `https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination` | FOIA-disclosable NPPES governance and file policy | Provider-reported data may lag |
| FSMB/state boards | `https://www.fsmb.org/data-integration/` plus state-board sites | Licensure, sanctions, disciplinary status, inactive signals | Access terms vary |
| Practice websites | Practice roster, phone, address, accepting-new-patients | Strong for current location and roster | Must respect terms/robots |
| Health-system directories | Affiliation, specialty, location | Strong for group membership | May conflict with NPPES |
| Business listings | Fresh phone/address fallback only | Cheap recall source | Never authoritative for identity/status |

## AWS Pattern

EventBridge schedule -> Step Functions workflow -> Lambda/ECS/AWS Batch connectors -> S3 raw evidence -> RDS/DynamoDB normalized evidence -> confidence scoring -> recommendation JSON -> review/auto-update -> audit.

## Guardrails

- Do not use NPPES alone to prove licensure.
- Do not use business listings for identity, specialty, license, or inactive status.
- Preserve source URL, timestamp, parser version, and evidence hash.
- Route source conflicts to review unless field-specific authority rules resolve them.
