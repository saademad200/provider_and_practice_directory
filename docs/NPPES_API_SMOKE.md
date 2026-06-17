# NPPES API Smoke Fixture

This experiment verifies that the prototype can call the official NPPES API, cache the response, and map it into evidence rows.

## Smoke Query

- API: `https://npiregistry.cms.hhs.gov/api/`
- Version: `2.1`
- NPI: `1679576722`
- Result count: 1
- Provider: DAVID WIEBE M.D.
- Taxonomies returned: 1
- Addresses returned: 2

## Parsed Evidence

| Field | Value |
|---|---|
| address | PO BOX 2168 KEARNEY NE 688482168 |
| phone | 308-865-2512 |
| address | 3500 CENTRAL AVE KEARNEY NE 688472944 |
| phone | 308-865-2512 |
| credential | M.D. |
| npi_status | A |
| specialty | Orthopaedic Surgery |

## Schema Mapping

| NPPES Field | Local Evidence Field | Use |
|---|---|---|
| `number` | `npi` | Provider identity anchor |
| `basic.first_name`, `basic.last_name`, `basic.credential` | provider name / credential evidence | Name normalization and display |
| `addresses[].address_purpose == LOCATION` | address and phone evidence | Practice-location verification |
| `taxonomies[].primary == true` | specialty evidence | Specialty normalization |
| `basic.status` | NPI status evidence | Identity validity / review routing |

## Current Pipeline Context

- F1: 0.93913
- Precision: 0.947368
- Recall: 0.931034
- Auto-apply precision: 1.0

## Production Notes

- Cache API responses in S3/DynamoDB with source timestamp and API version.
- Use NPPES for identity anchoring and specialty/address corroboration, not as sole proof of license validity.
- Combine targeted API lookups with monthly/weekly NPPES bulk files for scale.
