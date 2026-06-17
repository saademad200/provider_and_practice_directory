from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pandas as pd


SECRET_PATTERNS = {
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "aws_secret_assignment": re.compile(r"(?i)(aws_secret_access_key|secret_access_key)\s*[:=]\s*[A-Za-z0-9/+=]{20,}"),
    "generic_api_key_assignment": re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{24,}"),
    "private_key_block": re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
}


TEXT_SUFFIXES = {".py", ".md", ".json", ".csv", ".txt", ".yaml", ".yml", ".html", ".mmd", ".jsonl"}


def scan_paths(paths: list[Path]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for root in paths:
        if not root.exists():
            continue
        files = [root] if root.is_file() else [path for path in root.rglob("*") if path.is_file()]
        for path in files:
            if path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for name, pattern in SECRET_PATTERNS.items():
                matches = list(pattern.finditer(text))
                if matches:
                    rows.append(
                        {
                            "path": path.as_posix(),
                            "pattern": name,
                            "matches": len(matches),
                            "action": "block_release_and_rotate_if_real",
                        }
                    )
    return pd.DataFrame(rows, columns=["path", "pattern", "matches", "action"])


def scan_summary(findings: pd.DataFrame, scanned_roots: list[Path]) -> dict[str, Any]:
    return {
        "scanned_roots": [path.as_posix() for path in scanned_roots],
        "finding_count": int(len(findings)),
        "passed": bool(findings.empty),
    }
