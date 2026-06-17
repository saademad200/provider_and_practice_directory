from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import pandas as pd


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_package_manifest(package_dir: Path) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for path in sorted(package_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(package_dir).as_posix()
        rows.append(
            {
                "artifact": rel,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return pd.DataFrame(rows)


def manifest_summary(manifest: pd.DataFrame) -> dict[str, Any]:
    return {
        "artifacts": int(len(manifest)),
        "total_size_bytes": int(manifest["size_bytes"].sum()),
        "manifest_sha256": hashlib.sha256(
            "\n".join(manifest.sort_values("artifact")["sha256"].tolist()).encode("utf-8")
        ).hexdigest(),
    }
