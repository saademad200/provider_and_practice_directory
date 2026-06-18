from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold

from .freshness import freshness_metadata
from .npi import synthetic_npi
from .review_priority import review_priority
from .specialty import normalize_specialty


FIELDS = ["phone", "address", "specialty", "license_status", "accepting_new_patients"]
BENCHMARK_VERSION = "2026-06-18-v3-valid-npi"

SOURCE_WEIGHTS = {
    "nppes": 0.92,
    "state_license": 0.96,
    "practice_website": 0.82,
    "health_system": 0.86,
    "business_listing": 0.64,
}


@dataclass(frozen=True)
class DatasetPaths:
    base_dir: Path = Path("data/sample")

    @property
    def providers(self) -> Path:
        return self.base_dir / "providers.csv"

    @property
    def evidence(self) -> Path:
        return self.base_dir / "evidence.csv"

    @property
    def gold_updates(self) -> Path:
        return self.base_dir / "gold_updates.csv"

    @property
    def meta(self) -> Path:
        return self.base_dir / "benchmark_meta.json"


def normalize_phone(value: Any) -> str:
    digits = "".join(ch for ch in str(value) if ch.isdigit())
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    return str(value).strip()


def normalize_text(value: Any) -> str:
    return " ".join(str(value).lower().replace(",", " ").replace(".", " ").split())


def normalize_address(value: Any) -> str:
    text = normalize_text(value)
    aliases = {
        "st": "street",
        "ave": "avenue",
        "rd": "road",
        "blvd": "boulevard",
        "dr": "drive",
        "ste": "suite",
        "unit": "suite",
        "#": "suite",
        "fl": "florida",
    }
    tokens = []
    for token in text.split():
        if token.startswith("#") and token[1:].isalnum():
            tokens.extend(["suite", token[1:]])
            continue
        tokens.append(aliases.get(token, token))
    compact = []
    for token in tokens:
        if compact and compact[-1] == token == "suite":
            continue
        compact.append(token)
    return " ".join(compact)


def normalize_value(field: str, value: Any) -> str:
    if pd.isna(value):
        return ""
    if field == "phone":
        return normalize_phone(value)
    if field == "address":
        return normalize_address(value)
    if field == "accepting_new_patients":
        text = normalize_text(value)
        if text in {"yes", "true", "1", "accepting"}:
            return "true"
        if text in {"no", "false", "0", "not accepting"}:
            return "false"
    if field == "specialty":
        return normalize_specialty(value)
    return normalize_text(value)


def _phone(i: int) -> str:
    return f"555-{100 + (i % 800):03d}-{2000 + (i * 37) % 7000:04d}"


def _address(i: int) -> str:
    streets = ["Main St", "Oak Ave", "Cedar Rd", "Pine Blvd", "Market St", "Lake Dr"]
    return f"{100 + i * 7} {streets[i % len(streets)]}, Suite {1 + i % 12}, FL"


def _wrong_value(field: str, i: int, specialties: list[str], current_value: str) -> str:
    if field == "phone":
        return _phone(i + 211)
    if field == "address":
        return _address(i + 149)
    if field == "specialty":
        return specialties[(i + 3) % len(specialties)]
    if field == "accepting_new_patients":
        return "false" if normalize_value(field, current_value) == "true" else "true"
    return current_value


def ensure_sample_data(paths: DatasetPaths | None = None, n_providers: int = 72, seed: int = 42) -> DatasetPaths:
    paths = paths or DatasetPaths()
    paths.base_dir.mkdir(parents=True, exist_ok=True)
    if (
        paths.providers.exists()
        and paths.evidence.exists()
        and paths.gold_updates.exists()
        and paths.meta.exists()
        and BENCHMARK_VERSION in paths.meta.read_text(encoding="utf-8")
    ):
        return paths

    rng = np.random.default_rng(seed)
    specialties = ["family medicine", "cardiology", "dermatology", "pediatrics", "orthopedics", "neurology"]
    providers = []
    evidence = []
    gold = []

    stale_plan = {
        "phone": set(rng.choice(n_providers, size=18, replace=False).tolist()),
        "address": set(rng.choice(n_providers, size=14, replace=False).tolist()),
        "specialty": set(rng.choice(n_providers, size=8, replace=False).tolist()),
        "license_status": set(rng.choice(n_providers, size=6, replace=False).tolist()),
        "accepting_new_patients": set(rng.choice(n_providers, size=12, replace=False).tolist()),
    }

    for i in range(n_providers):
        provider_id = f"P{i:04d}"
        practice_id = f"PR{i // 3:03d}"
        true_values = {
            "phone": _phone(i),
            "address": _address(i),
            "specialty": specialties[i % len(specialties)],
            "license_status": "active" if i % 17 else "probation",
            "accepting_new_patients": "true" if i % 4 else "false",
        }
        current_values = dict(true_values)
        for field, stale_ids in stale_plan.items():
            if i in stale_ids:
                if field == "phone":
                    current_values[field] = _phone(i + 101)
                elif field == "address":
                    current_values[field] = _address(i + 73)
                elif field == "specialty":
                    current_values[field] = specialties[(i + 2) % len(specialties)]
                elif field == "license_status":
                    current_values[field] = "inactive" if true_values[field] == "active" else "active"
                elif field == "accepting_new_patients":
                    current_values[field] = "false" if true_values[field] == "true" else "true"
                gold.append(
                    {
                        "provider_id": provider_id,
                        "field": field,
                        "old_value": current_values[field],
                        "new_value": true_values[field],
                    }
                )

        providers.append(
            {
                "provider_id": provider_id,
                "practice_id": practice_id,
                "npi": synthetic_npi(i),
                "provider_name": f"Provider {i:03d}",
                **current_values,
            }
        )

        for source in ["nppes", "practice_website", "health_system", "business_listing"]:
            for field in ["phone", "address", "specialty", "accepting_new_patients"]:
                value = true_values[field]
                noise_rate = {
                    "nppes": 0.03,
                    "practice_website": 0.08,
                    "health_system": 0.06,
                    "business_listing": 0.22,
                }[source]
                stale_noise_bonus = 0.04 if i in stale_plan[field] else 0.0
                if rng.random() < 0.08:
                    value = current_values[field]
                if rng.random() < noise_rate + stale_noise_bonus:
                    value = _wrong_value(field, i, specialties, current_values[field])
                if rng.random() < 0.06:
                    value = ""
                evidence.append(
                    {
                        "provider_id": provider_id,
                        "practice_id": practice_id,
                        "source": source,
                        "field": field,
                        "value": value,
                        "retrieved_days_ago": int(rng.integers(2, 180)),
                        "url": f"https://example.org/{source}/{provider_id}",
                    }
                )

        evidence.append(
            {
                "provider_id": provider_id,
                "practice_id": practice_id,
                "source": "state_license",
                "field": "license_status",
                "value": true_values["license_status"] if rng.random() > 0.08 else current_values["license_status"],
                "retrieved_days_ago": int(rng.integers(1, 90)),
                "url": f"https://example.org/license/{provider_id}",
            }
        )

    pd.DataFrame(providers).to_csv(paths.providers, index=False)
    pd.DataFrame(evidence).to_csv(paths.evidence, index=False)
    pd.DataFrame(gold).to_csv(paths.gold_updates, index=False)
    paths.meta.write_text(
        f'{{"benchmark_version": "{BENCHMARK_VERSION}", "n_providers": {n_providers}, "seed": {seed}}}\n',
        encoding="utf-8",
    )
    return paths


def load_dataset(paths: DatasetPaths | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    paths = ensure_sample_data(paths)
    return (
        pd.read_csv(paths.providers),
        pd.read_csv(paths.evidence),
        pd.read_csv(paths.gold_updates),
    )


def provider_splits(providers: pd.DataFrame, n_splits: int = 5) -> list[tuple[np.ndarray, np.ndarray]]:
    groups = providers["provider_id"].to_numpy()
    indices = np.arange(len(providers))
    if providers["provider_id"].nunique() < n_splits:
        n_splits = max(2, providers["provider_id"].nunique())
    return list(GroupKFold(n_splits=n_splits).split(indices, groups=groups))


def build_candidate_updates(
    providers: pd.DataFrame,
    evidence: pd.DataFrame,
    cfg: dict[str, Any],
) -> pd.DataFrame:
    default_threshold = float(cfg.get("confidence_threshold", 0.72))
    default_auto_threshold = float(cfg.get("auto_apply_threshold", 0.90))
    field_thresholds = cfg.get("field_confidence_thresholds", {})
    field_auto_thresholds = cfg.get("field_auto_apply_thresholds", {})
    min_sources_by_field = cfg.get("min_distinct_sources_by_field", {})
    default_min_sources = int(cfg.get("min_distinct_sources", 1))
    min_auto_sources_by_field = cfg.get("min_auto_sources_by_field", {})
    default_min_auto_sources = int(cfg.get("min_auto_sources", 1))
    recency_half_life = float(cfg.get("recency_half_life_days", 120.0))
    source_weights = {**SOURCE_WEIGHTS, **cfg.get("source_weights", {})}
    conflict_weight_scale = float(cfg.get("conflict_weight_scale", 0.15))
    practice_consensus_fields = set(cfg.get("practice_consensus_review_fields", []))
    safe_auto_apply_fields = set(cfg.get("safe_auto_apply_fields", ["phone", "specialty"]))
    auto_apply_freshness_statuses = set(
        cfg.get("auto_apply_freshness_statuses", ["fresh", "partially_stale"])
    )
    disabled_sources = set(cfg.get("disabled_sources", []))
    source_slas_days = cfg.get("source_slas_days", {})
    source_field_allowlist = {
        source: set(fields)
        for source, fields in cfg.get("source_field_allowlist", {}).items()
    }
    source_max_age_days_by_source_field = cfg.get("source_max_age_days_by_source_field", {})

    current_lookup = providers.set_index("provider_id").to_dict("index")
    records = []
    for (provider_id, field), group in evidence.groupby(["provider_id", "field"], dropna=False):
        if field not in FIELDS or provider_id not in current_lookup:
            continue
        current_value = normalize_value(field, current_lookup[provider_id].get(field, ""))
        votes: dict[str, float] = {}
        sources: dict[str, list[str]] = {}
        urls: dict[str, list[str]] = {}
        ages: dict[str, list[tuple[str, float]]] = {}
        for row in group.to_dict("records"):
            value = normalize_value(field, row.get("value", ""))
            if not value or value == current_value:
                continue
            source = row.get("source", "")
            if source in disabled_sources:
                continue
            age = float(row.get("retrieved_days_ago", 999))
            if source in source_field_allowlist and field not in source_field_allowlist[source]:
                continue
            max_age_by_field = source_max_age_days_by_source_field.get(source, {})
            if field in max_age_by_field and age > float(max_age_by_field[field]):
                continue
            recency = 0.5 ** (age / recency_half_life)
            weight = float(source_weights.get(source, 0.50)) * recency
            votes[value] = votes.get(value, 0.0) + weight
            sources.setdefault(value, []).append(source)
            urls.setdefault(value, []).append(row.get("url", ""))
            ages.setdefault(value, []).append((source, age))

        if not votes:
            continue

        proposed_value, support = max(votes.items(), key=lambda item: item[1])
        distinct_sources = len(set(sources[proposed_value]))
        min_sources = int(min_sources_by_field.get(field, default_min_sources))
        if distinct_sources < min_sources:
            continue
        conflicting_support = sum(value for key, value in votes.items() if key != proposed_value)
        total_support = support + conflict_weight_scale * conflicting_support
        confidence = support / max(total_support, 1e-9)
        confidence = min(confidence, 0.99)
        if distinct_sources >= 2:
            confidence = min(confidence + 0.06, 0.99)
        threshold = float(field_thresholds.get(field, default_threshold))
        auto_threshold = float(field_auto_thresholds.get(field, default_auto_threshold))
        if confidence < threshold:
            continue

        min_auto_sources = int(min_auto_sources_by_field.get(field, default_min_auto_sources))
        freshness = freshness_metadata(ages.get(proposed_value, []), source_slas_days)
        review_reasons = []
        if confidence < auto_threshold:
            review_reasons.append("confidence_below_auto_threshold")
        if distinct_sources < min_auto_sources:
            review_reasons.append("insufficient_auto_sources")
        if field not in safe_auto_apply_fields:
            review_reasons.append("field_not_safe_for_auto_apply")
        if freshness["freshness_status"] not in auto_apply_freshness_statuses:
            review_reasons.append("stale_or_missing_supporting_evidence")
        decision = "auto_apply" if not review_reasons else "review"
        practice_consensus_status = "not_checked"
        if decision == "auto_apply" and field in practice_consensus_fields:
            same_practice = providers[providers["practice_id"] == current_lookup[provider_id].get("practice_id", "")]
            peer_values = {
                normalize_value(field, row.get(field, ""))
                for row in same_practice.to_dict("records")
                if row.get("provider_id") != provider_id
            }
            if peer_values and proposed_value not in peer_values:
                decision = "review"
                practice_consensus_status = "peer_mismatch"
                review_reasons.append("practice_peer_mismatch")
            elif peer_values:
                practice_consensus_status = "peer_match"
            else:
                practice_consensus_status = "no_peers"
        priority = review_priority(
            field=field,
            confidence=confidence,
            review_reasons=review_reasons,
            threshold=threshold,
            auto_threshold=auto_threshold,
            distinct_sources=distinct_sources,
            min_auto_sources=min_auto_sources,
        )
        if decision == "auto_apply" and "high_field_risk" in priority["review_priority_drivers"]:
            decision = "review"
            review_reasons.append("high_field_risk")
            priority = review_priority(
                field=field,
                confidence=confidence,
                review_reasons=review_reasons,
                threshold=threshold,
                auto_threshold=auto_threshold,
                distinct_sources=distinct_sources,
                min_auto_sources=min_auto_sources,
            )
        review_reason_code = "|".join(review_reasons) if review_reasons else "auto_apply_criteria_met"
        records.append(
            {
                "provider_id": provider_id,
                "practice_id": current_lookup[provider_id].get("practice_id", ""),
                "field": field,
                "old_value": current_lookup[provider_id].get(field, ""),
                "proposed_value": proposed_value,
                "confidence": round(confidence, 4),
                "support": round(support, 4),
                "distinct_sources": distinct_sources,
                "practice_consensus_status": practice_consensus_status,
                "review_reason_code": review_reason_code,
                "sources": "|".join(sorted(set(sources[proposed_value]))),
                "evidence_urls": "|".join(sorted(set(urls[proposed_value]))),
                **freshness,
                "decision": decision,
                **priority,
            }
        )
    return pd.DataFrame(records)
