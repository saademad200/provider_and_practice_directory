from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from .npi import valid_npi


AS_OF_DATE = datetime(2026, 6, 17, tzinfo=timezone.utc)
PHONE_RE = re.compile(r"^\(\d{3}\)\s\d{3}-\d{4}$")
EMAIL_RE = re.compile(r"^[\w.\-]+@[\w\-]+\.\w{2,}$")
URL_RE = re.compile(r"^https?://[\w\-\.]+\.\w{2,}")
ZIP_RE = re.compile(r"^\d{5}(-\d{4})?$")


def parse_date(value: str) -> datetime | None:
    try:
        if not value or value == "nan":
            return None
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def load_public_dataset(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, low_memory=False).fillna("")


def profile_dataset(df: pd.DataFrame, dataset_path: Path, as_of_date: datetime = AS_OF_DATE) -> tuple[dict[str, Any], pd.DataFrame, pd.DataFrame]:
    row_count = len(df)
    missing_df = pd.DataFrame(
        [
            {
                "field": col,
                "blank_rows": int((df[col].astype(str).str.strip() == "").sum()),
                "blank_rate": round(int((df[col].astype(str).str.strip() == "").sum()) / row_count, 6),
            }
            for col in df.columns
        ]
    ).sort_values(["blank_rate", "field"], ascending=[False, True])
    issue_masks = {
        "invalid_npi_luhn_or_format": ~df["npi"].map(valid_npi),
        "invalid_phone_format": ~df["phone"].astype(str).map(lambda value: bool(PHONE_RE.match(value))),
        "invalid_email_format": ~df["email"].astype(str).map(lambda value: bool(EMAIL_RE.match(value)) or value == ""),
        "invalid_website_format": ~df["website"].astype(str).map(lambda value: bool(URL_RE.match(value)) or value == ""),
        "invalid_zip_format": ~df["zip_code"].astype(str).map(lambda value: bool(ZIP_RE.match(value))),
        "missing_address_line1": df["address_line1"].astype(str).str.strip() == "",
        "missing_practice_name": df["practice_name"].astype(str).str.strip() == "",
        "expired_license": df["license_expiry_date"].map(parse_date).map(lambda dt: dt is not None and dt < as_of_date),
        "stale_verification_over_365d": df["last_verified_date"].map(parse_date).map(lambda dt: dt is None or (as_of_date - dt).days > 365),
        "change_flag_high_risk": df["change_flag"].isin(["Retired", "Left Practice"]),
        "verification_needs_review": df["verification_status"].isin(["Needs Review", "Unverified", "Stale"]),
    }
    issue_df = pd.DataFrame(
        [
            {"issue": issue, "affected_rows": int(mask.sum()), "affected_rate": round(int(mask.sum()) / row_count, 6)}
            for issue, mask in issue_masks.items()
        ]
    ).sort_values(["affected_rows", "issue"], ascending=[False, True])
    summary = {
        "dataset": str(dataset_path),
        "rows": row_count,
        "columns": len(df.columns),
        "as_of_date": as_of_date.date().isoformat(),
        "change_flag_counts": df["change_flag"].replace("", "blank").value_counts().to_dict(),
        "verification_status_counts": df["verification_status"].value_counts().to_dict(),
        "data_source_counts": df["data_source"].value_counts().to_dict(),
        "top_missing_fields": missing_df.head(10).to_dict(orient="records"),
        "top_issues": issue_df.head(10).to_dict(orient="records"),
    }
    return summary, missing_df.reset_index(drop=True), issue_df.reset_index(drop=True)


def triage_dataset(df: pd.DataFrame, as_of_date: datetime = AS_OF_DATE) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for item in df.itertuples(index=False):
        row = item._asdict()
        issues: list[str] = []
        risk = 0.0
        if not valid_npi(row.get("npi", "")):
            issues.append("invalid_npi")
            risk += 0.18
        if not PHONE_RE.match(row.get("phone", "")):
            issues.append("invalid_phone")
            risk += 0.12
        if row.get("address_line1", "").strip() == "":
            issues.append("missing_address")
            risk += 0.12
        license_dt = parse_date(row.get("license_expiry_date", ""))
        if license_dt is None:
            issues.append("missing_license_expiry")
            risk += 0.08
        elif license_dt < as_of_date:
            issues.append("expired_license")
            risk += 0.2
        verified_dt = parse_date(row.get("last_verified_date", ""))
        if verified_dt is None or (as_of_date - verified_dt).days > 365:
            issues.append("stale_verification")
            risk += 0.2 if verified_dt is None else min(0.2, (as_of_date - verified_dt).days / 3650)
        if row.get("verification_status") in {"Needs Review", "Unverified", "Stale"}:
            issues.append("verification_status_risk")
            risk += 0.1
        if row.get("change_flag") in {"Retired", "Left Practice"}:
            issues.append("identity_or_active_status_change")
            risk += 0.22
        elif row.get("change_flag") and row.get("change_flag") != "No Change":
            issues.append("field_change_flag")
            risk += 0.1
        try:
            confidence = float(row.get("confidence_score", ""))
        except ValueError:
            confidence = 0.0
        risk += max(0.0, 0.65 - confidence) * 0.18
        risk = min(1.0, round(risk, 6))
        if "identity_or_active_status_change" in issues or "expired_license" in issues:
            action = "review_identity_or_status"
        elif risk >= 0.55:
            action = "urgent_review"
        elif risk >= 0.35:
            action = "scheduled_verification"
        elif issues:
            action = "monitor_with_low_cost_refresh"
        else:
            action = "monitor"
        rows.append(
            {
                "provider_id": row.get("provider_id", ""),
                "npi": row.get("npi", ""),
                "provider_name": " ".join(part for part in [row.get("first_name", ""), row.get("last_name", "")] if part),
                "practice_name": row.get("practice_name", ""),
                "state": row.get("state", ""),
                "specialty_primary": row.get("specialty_primary", ""),
                "verification_status": row.get("verification_status", ""),
                "change_flag": row.get("change_flag", "") or "blank",
                "confidence_score": confidence,
                "triage_risk_score": risk,
                "recommended_action": action,
                "issue_flags": "|".join(issues) if issues else "none",
            }
        )
    return pd.DataFrame(rows).sort_values(["triage_risk_score", "provider_id"], ascending=[False, True]).reset_index(drop=True)


def write_public_dataset_outputs(dataset_path: Path, out_dir: Path, top_n: int = 500) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    df = load_public_dataset(dataset_path)
    summary, missing_df, issue_df = profile_dataset(df, dataset_path)
    triage = triage_dataset(df)
    missing_df.to_csv(out_dir / "public_dataset_missingness.csv", index=False)
    issue_df.to_csv(out_dir / "public_dataset_issue_counts.csv", index=False)
    triage.head(top_n).to_csv(out_dir / f"public_dataset_triage_top{top_n}.csv", index=False)
    triage["recommended_action"].value_counts().rename_axis("recommended_action").reset_index(name="rows").to_csv(
        out_dir / "public_dataset_triage_action_counts.csv", index=False
    )
    (out_dir / "public_dataset_profile_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
