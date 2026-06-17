from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests


@dataclass(frozen=True)
class NPPESConnector:
    cache_dir: Path = Path("data/cache/nppes")
    base_url: str = "https://npiregistry.cms.hhs.gov/api/"
    version: str = "2.1"

    def cache_path(self, npi: str) -> Path:
        return self.cache_dir / f"{npi}.json"

    def fetch(self, npi: str, use_cache: bool = True) -> dict[str, Any]:
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        path = self.cache_path(npi)
        if use_cache and path.exists():
            return json.loads(path.read_text(encoding="utf-8"))

        response = requests.get(
            self.base_url,
            params={"version": self.version, "number": npi},
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        return payload

    def parse_evidence(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        records = []
        for result in payload.get("results", []):
            npi = str(result.get("number", ""))
            basic = result.get("basic", {})
            for address in result.get("addresses", []):
                if address.get("address_purpose") not in {"LOCATION", "MAILING"}:
                    continue
                line1 = address.get("address_1", "")
                line2 = address.get("address_2", "")
                city = address.get("city", "")
                state = address.get("state", "")
                postal = address.get("postal_code", "")
                records.append(
                    {
                        "npi": npi,
                        "source": "nppes",
                        "field": "address",
                        "value": " ".join(part for part in [line1, line2, city, state, postal] if part),
                        "url": f"https://npiregistry.cms.hhs.gov/provider-view/{npi}",
                    }
                )
                if address.get("telephone_number"):
                    records.append(
                        {
                            "npi": npi,
                            "source": "nppes",
                            "field": "phone",
                            "value": address["telephone_number"],
                            "url": f"https://npiregistry.cms.hhs.gov/provider-view/{npi}",
                        }
                    )
            if basic.get("credential"):
                records.append(
                    {
                        "npi": npi,
                        "source": "nppes",
                        "field": "credential",
                        "value": basic["credential"],
                        "url": f"https://npiregistry.cms.hhs.gov/provider-view/{npi}",
                    }
                )
            if basic.get("status"):
                records.append(
                    {
                        "npi": npi,
                        "source": "nppes",
                        "field": "npi_status",
                        "value": basic["status"],
                        "url": f"https://npiregistry.cms.hhs.gov/provider-view/{npi}",
                    }
                )
            for date_field in ["deactivation_date", "reactivation_date"]:
                if basic.get(date_field):
                    records.append(
                        {
                            "npi": npi,
                            "source": "nppes",
                            "field": date_field,
                            "value": basic[date_field],
                            "url": f"https://npiregistry.cms.hhs.gov/provider-view/{npi}",
                        }
                    )
            for taxonomy in result.get("taxonomies", []):
                if taxonomy.get("primary") and taxonomy.get("desc"):
                    records.append(
                        {
                            "npi": npi,
                            "source": "nppes",
                            "field": "specialty",
                            "value": taxonomy["desc"],
                            "url": f"https://npiregistry.cms.hhs.gov/provider-view/{npi}",
                        }
                    )
        return records
