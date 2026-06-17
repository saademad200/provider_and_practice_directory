from __future__ import annotations

from typing import Any

import pandas as pd


def source_connector_registry() -> pd.DataFrame:
    rows: list[dict[str, Any]] = [
        {
            "connector_id": "nppes_npi_registry",
            "source_type": "official_api",
            "authority_rank": 1,
            "official_url": "https://npiregistry.cms.hhs.gov/api-page",
            "fields": "npi, provider_name, practice_address, mailing_address, taxonomy_specialty, enumeration_status",
            "auth_required": "no",
            "freshness_sla_days": 7,
            "cache_ttl_days": 7,
            "cost_tier": "free_public",
            "health_check": "GET sample NPI query, validate result_count and schema version",
            "fallback": "NPPES downloadable file or cached prior successful snapshot",
            "auto_apply_role": "identity and specialty support, never sole practice-affiliation authority",
        },
        {
            "connector_id": "cms_provider_data_catalog",
            "source_type": "official_dataset_api",
            "authority_rank": 2,
            "official_url": "https://data.cms.gov/provider-data/docs",
            "fields": "clinician_enrollment, organization, address, specialty, provider participation signals",
            "auth_required": "no",
            "freshness_sla_days": 30,
            "cache_ttl_days": 30,
            "cost_tier": "free_public",
            "health_check": "GET schema list and one dataset page, validate dataset modified timestamp",
            "fallback": "downloadable national file snapshot in S3",
            "auto_apply_role": "supporting evidence for organization/practice and Medicare-facing participation",
        },
        {
            "connector_id": "state_license_board",
            "source_type": "official_state_source",
            "authority_rank": 1,
            "official_url": "state-specific board URL configured per jurisdiction",
            "fields": "license_status, disciplinary_status, license_expiration, practice_state",
            "auth_required": "varies",
            "freshness_sla_days": 14,
            "cache_ttl_days": 14,
            "cost_tier": "free_or_low_cost",
            "health_check": "jurisdiction-specific search fixture plus schema/status vocabulary validation",
            "fallback": "last successful state snapshot; route stale license changes to review",
            "auto_apply_role": "highest authority for inactive/probation license status after identity match",
        },
        {
            "connector_id": "practice_website",
            "source_type": "public_web",
            "authority_rank": 3,
            "official_url": "practice or health-system owned public website",
            "fields": "phone, location_address, accepting_new_patients, specialty, provider_roster",
            "auth_required": "no",
            "freshness_sla_days": 21,
            "cache_ttl_days": 14,
            "cost_tier": "crawler_compute",
            "health_check": "robots/terms allowed, HTTP 200, parser fixture coverage, canonical domain match",
            "fallback": "health-system page or manual review if deterministic parser fails",
            "auto_apply_role": "strong for phone/address only with peer or second-source confirmation",
        },
        {
            "connector_id": "health_system_directory",
            "source_type": "public_web_or_partner_feed",
            "authority_rank": 2,
            "official_url": "health-system provider directory or partner feed endpoint",
            "fields": "practice_affiliation, location_address, phone, specialty, accepting_new_patients",
            "auth_required": "varies",
            "freshness_sla_days": 14,
            "cache_ttl_days": 14,
            "cost_tier": "crawler_or_partner_feed",
            "health_check": "feed timestamp, provider roster row count, parser drift and stale-page checks",
            "fallback": "practice website plus manual review for affiliation changes",
            "auto_apply_role": "strong for affiliation/roster when identity and location agree",
        },
        {
            "connector_id": "business_listing",
            "source_type": "third_party_listing",
            "authority_rank": 5,
            "official_url": "vendor-specific listing URL if terms permit",
            "fields": "phone, address, open/closed hints",
            "auth_required": "varies",
            "freshness_sla_days": 45,
            "cache_ttl_days": 30,
            "cost_tier": "paid_or_rate_limited",
            "health_check": "terms allowlist, duplicate listing rate, stale listing rate, cost threshold",
            "fallback": "disabled by default in current best config",
            "auto_apply_role": "review-only weak signal because ablation showed quality/cost risk",
        },
    ]
    return pd.DataFrame(rows)


def evidence_tool_manifest(registry: pd.DataFrame) -> dict[str, Any]:
    tools = []
    for row in registry.sort_values(["authority_rank", "connector_id"]).to_dict("records"):
        tools.append(
            {
                "name": row["connector_id"],
                "description": f"Fetch and normalize {row['fields']} from {row['source_type']}.",
                "input_schema": {
                    "type": "object",
                    "required": ["provider_id", "provider_name"],
                    "properties": {
                        "provider_id": {"type": "string"},
                        "npi": {"type": "string"},
                        "provider_name": {"type": "string"},
                        "practice_id": {"type": "string"},
                        "state": {"type": "string"},
                        "source_run_id": {"type": "string"},
                    },
                },
                "output_schema": {
                    "type": "object",
                    "required": ["connector_id", "retrieved_at", "evidence", "health_status"],
                    "properties": {
                        "connector_id": {"const": row["connector_id"]},
                        "retrieved_at": {"type": "string", "format": "date-time"},
                        "evidence": {"type": "array", "items": {"type": "object"}},
                        "health_status": {"enum": ["ok", "degraded", "failed", "stale"]},
                        "source_url": {"type": "string"},
                        "cache_key": {"type": "string"},
                    },
                },
                "freshness_sla_days": int(row["freshness_sla_days"]),
                "cache_ttl_days": int(row["cache_ttl_days"]),
                "authority_rank": int(row["authority_rank"]),
                "permissions": {
                    "default_mode": "read_or_append_only",
                    "may_mutate_directory": False,
                    "requires_terms_allowlist": row["source_type"] in {"public_web", "third_party_listing"},
                },
            }
        )
    return {
        "manifest_version": "2026-06-16",
        "contract": "provider-directory-evidence-tools",
        "cloud_target": "aws",
        "tools": tools,
    }


def connector_health_fixture(registry: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in registry.itertuples(index=False):
        rows.append(
            {
                "connector_id": row.connector_id,
                "expected_health_status": "ok" if row.connector_id != "business_listing" else "disabled",
                "freshness_sla_days": row.freshness_sla_days,
                "cache_ttl_days": row.cache_ttl_days,
                "required_actions_on_failure": "mark stale, block auto-apply if min-source policy fails, emit CloudWatch alert",
                "sample_check": row.health_check,
            }
        )
    return pd.DataFrame(rows)
