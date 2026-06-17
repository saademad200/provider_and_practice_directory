from __future__ import annotations

from pathlib import Path

import pandas as pd


def save_diagnostics(per_field: pd.DataFrame, worst_providers: pd.DataFrame, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    per_field.to_csv(out_dir / "per_field.csv", index=False)
    worst_providers.to_csv(out_dir / "worst_providers.csv", index=False)

    try:
        import matplotlib.pyplot as plt
    except Exception:
        return

    if not per_field.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(per_field["field"], per_field["f1"])
        ax.set_ylim(0, 1)
        ax.set_ylabel("F1")
        ax.set_title("Per-field F1")
        ax.tick_params(axis="x", rotation=30)
        fig.tight_layout()
        fig.savefig(out_dir / "per_field_f1.png", dpi=160)
        plt.close(fig)

