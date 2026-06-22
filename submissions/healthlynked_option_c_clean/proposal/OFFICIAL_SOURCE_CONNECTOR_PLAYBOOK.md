# Official Source Connector Playbook

## Purpose

This playbook shows how the MVP leaves synthetic fixtures and connects to real public or governed provider sources.

| Source | Official Surface | Use | Caveat |
|---|---|---|---|
| NPPES API | `https://npiregistry.cms.hhs.gov/api-page` | NPI identity lookup, taxonomy, metadata | NPI does not validate licensure |
| NPPES downloadable files | `https://download.cms.gov/nppes/NPI_Files.html` | Monthly/weekly batch refresh, deactivation files, practice locations, endpoints | Large files need batch ingestion |
| CMS data dissemination | `https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination` | FOIA-disclosable NPPES governance and file policy | Provider-reported data may lag |
| CMS PECOS / Medicare enrollment datasets | CMS public enrollment surfaces | Medicare enrollment and organization-affiliation cross-checks | Good signal for review and prioritization, not a sole source for write decisions |
| NUCC provider taxonomy | `https://nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40` | Specialty/taxonomy normalization and synonym mapping | Taxonomy defines classification, not licensure scope |
| FSMB/state boards | `https://www.fsmb.org/data-integration/` plus state-board sites | Licensure, sanctions, disciplinary status, inactive signals | Access terms vary |
| Practice websites | Practice roster, phone, address, accepting-new-patients | Strong for current location and roster | Must respect terms/robots |
| Health-system directories | Affiliation, specialty, location | Strong for group membership | May conflict with NPPES |
| Business listings | Fresh phone/address fallback only | Cheap recall source | Never authoritative for identity/status |

## Cloud Pattern (AWS Reference Example)

Cloud scheduler -> workflow service -> serverless/container/batch connectors -> object-store raw evidence -> relational/key-value normalized evidence (AWS EventBridge, Step Functions, Lambda/ECS/Batch, S3, RDS/DynamoDB as examples) -> confidence scoring -> recommendation JSON -> review/auto-update -> audit.

## Guardrails

- Do not use NPPES alone to prove licensure.
- Do not use business listings for identity, specialty, license, or inactive status.
- Do not treat PECOS/enrollment presence as a complete active-practice proof without field-specific corroboration.
- Do map specialties through NUCC/NPPES taxonomy before comparing display names.
- Preserve source URL, timestamp, parser version, and evidence hash.
- Route source conflicts to review unless field-specific authority rules resolve them.
