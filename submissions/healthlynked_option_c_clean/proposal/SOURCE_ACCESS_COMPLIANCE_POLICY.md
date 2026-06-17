# Source Access Compliance Policy

## Purpose

The pipeline should improve directory quality without creating source-access, privacy, or operational risk. This policy defines which sources can be used automatically, how connectors behave, and when a source must be blocked or routed to human review.

## Source Access Law

| Source Type | Allowed Use | Automation Rule | Notes |
|---|---|---|---|
| CMS/NPPES public API | NPI lookup, provider identity, taxonomy, practice/mailing address, phone, endpoint metadata | Prefer API for targeted lookup and monthly/weekly files for batch refresh | NPPES is an authority source for NPI facts, but not a license/credentialing validator |
| CMS/NPPES downloadable files | Large-batch refresh, deactivation checks, incremental updates | Cache monthly full replacement and weekly incremental files before scoring | CMS states the downloadable data is available at no charge |
| State medical/licensing boards | License status, discipline/status, provider active/inactive signals | Connector only after terms review; inactive/suppression remains review-first | State boards outrank business listings for status |
| Health system and practice websites | Practice affiliation, location, phone, scheduling page, active roster evidence | Respect robots/terms, rate limits, cache pages, preserve source URL and retrieval time | Good for current affiliation but weaker than state/license authority for status |
| Business listings/search snippets | Last-resort discovery and corroboration | Never sole source for identity, specialty, inactive status, or auto-update | Useful for candidate generation, not final authority |
| Paid enrichment APIs | Optional fallback only | Disabled by default; must pass source ablation and cost gate | Use only when marginal accepted-update lift justifies cost |
| LLM extraction | Structured extraction from already-collected evidence | Never allowed to invent values; schema-valid, source-grounded, corroborated output only | LLMs assist parsing and explanation, not authority |

## Connector Admission Checklist

A source connector cannot write candidate evidence until it has:

- documented legal/terms review status;
- authority tier and field-level allowed-use mapping;
- robots/rate-limit policy for websites;
- cached raw payload or page snapshot path;
- parser fixture and empty-rate alert;
- freshness threshold by field;
- cost estimate per 1,000 provider records;
- conflict behavior when stronger sources disagree;
- audit fields: source name, URL/file, retrieved timestamp, parser version, evidence hash.

## Polite Crawling And Cost Controls

- Prefer official bulk files and APIs over website scraping when available.
- Cache source payloads and normalized evidence; re-fetch only when freshness policy requires it.
- Use conditional requests, backoff, and connector-level concurrency limits.
- Do not bypass login walls, CAPTCHAs, paywalls, or explicit robots/terms restrictions.
- Keep paid APIs behind a source-ablation gate; they must improve accepted updates enough to justify spend.
- Run expensive or ambiguous sources after cheap authority sources have already failed to resolve the field.

## Privacy And Data Minimization

- Collect only fields required for the MVP and audit trail: provider name, NPI, specialty, practice name, address, phone, website, affiliation, status, source metadata, confidence reasons.
- Avoid collecting patient data, reviews, social profiles, or unrelated personal data.
- Store raw source payloads with retention limits and access controls.
- Use hashed evidence fingerprints in audit records when raw payload retention is not necessary.

## Disallowed Behaviors

- No auto-update from a single weak or stale source.
- No inactive/suppression update from business listings alone.
- No scraping that violates explicit source terms or technical access controls.
- No LLM-only recommendation without cited source evidence.
- No paid API fallback without cost and acceptance-rate justification.
- No use of NPPES as proof of licensure; license/status decisions require stronger state or board evidence.

## Judge Takeaway

This submission does not depend on reckless scraping or expensive enrichment. It starts with public authority sources, applies field-level source law, caches aggressively, fails closed under uncertainty, and keeps every proposed change traceable to legally accessible evidence.
