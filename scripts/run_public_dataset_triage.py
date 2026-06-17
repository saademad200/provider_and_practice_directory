#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.public_dataset_triage import write_public_dataset_outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Profile and triage the public Kaggle provider-directory dataset.")
    parser.add_argument(
        "--input",
        default="data/raw/kaggle_public_provider_directory/provider_directory_dataset.csv",
        help="Path to provider_directory_dataset.csv.",
    )
    parser.add_argument("--out-dir", default="outputs/public_dataset_triage", help="Output directory.")
    parser.add_argument("--top-n", type=int, default=500, help="Number of highest-risk rows to save.")
    args = parser.parse_args()

    summary = write_public_dataset_outputs(Path(args.input), Path(args.out_dir), top_n=args.top_n)
    print(json.dumps({"out_dir": args.out_dir, "rows": summary["rows"], "columns": summary["columns"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
