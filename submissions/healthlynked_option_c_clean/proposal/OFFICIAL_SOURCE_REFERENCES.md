# Official Source References

## Purpose

This note records the public authority sources that shaped the connector strategy. It is included so judges can distinguish source-grounded design choices from generic scraping assumptions.

## Reference Map

| Reference | What It Supports In This Submission | How The Pipeline Uses It |
|---|---|---|
| NPPES NPI Registry API: https://npiregistry.cms.hhs.gov/api-page | Official targeted lookup for NPI/provider facts | Used for targeted NPI verification, provider identity facts, taxonomy, and source-backed evidence records |
| CMS NPPES Data Dissemination: https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination | Monthly full replacement and weekly incremental files; no-charge downloadable data | Used for low-cost batch refresh, deactivation checks, and stale/risky record prioritization |
| CMS NPI Files: https://download.cms.gov/nppes/NPI_Files.html | Current downloadable file names, update dates, and supplemental reference files. Checked June 18, 2026: CMS listed the June 08, 2026 monthly V.2 file plus June 2026 weekly incremental files. | Used by the production connector to pin file versions and preserve source lineage |
| CMS NPPES downloadable-file readme: https://www.cms.gov/regulations-and-guidance/administrative-simplification/nationalprovidentstand/downloads/data_dissemination_file-readme.pdf | NPPES data-field interpretation and public dissemination scope | Used to map raw NPPES fields to normalized directory fields without guessing |
| FSMB Data Integration: https://www.fsmb.org/data-integration/ | Primary-source verified licensure/discipline data availability | Used as the preferred paid/contracted authority path for license/status enrichment when HealthLynked approves cost and terms |
| FSMB Physician Data Center files: https://www.fsmb.org/PDC/pdc-data-files/ | High-volume licensure and disciplinary data option | Used in the production roadmap as a scalable alternative to one-off state-board scraping |
| FSMB Physician Data Center FAQ: https://www.fsmb.org/PDC/pdc-faq/ | Source lineage from state boards and regulatory entities | Used to justify higher authority weight for licensure/status evidence than business listings |

## Design Implications

- NPPES is excellent for NPI identity, taxonomy, and public provider facts, but the pipeline does not treat an NPI record as proof of licensure.
- Monthly and weekly CMS files are the default scale path because they are cheaper and more stable than repeated web searches.
- The production connector should persist the exact CMS file label/date, not just the generic source name, so every recommendation can be traced to a specific monthly or weekly NPPES release.
- State boards and FSMB-style sources are the higher-authority path for active/inactive, licensure, and disciplinary status.
- Practice and health-system websites are strong for current affiliation, location, phone, and scheduling-page evidence.
- Business listings are fallback discovery evidence, not final authority for sensitive updates.
- Every connector records source URL/file, retrieval timestamp, source version, parser version, and evidence hash.

## Judge Takeaway

The system is designed around public and legally accessible authority sources first, with paid or LLM-assisted paths treated as gated fallbacks. That keeps the proposal practical, auditable, and cost-controlled.
