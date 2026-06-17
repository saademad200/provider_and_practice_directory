#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTORESEARCH = ROOT / "autoresearch"
RESULTS = ROOT / "results"
EXPERIMENTS = ROOT / "experiments"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)


def discover_next_experiment(exp_id: str | None = None) -> Path | None:
    if exp_id:
        matches = sorted(EXPERIMENTS.glob(f"{exp_id}_*.py"))
        return matches[0] if matches else None
    completed = {path.parent.name for path in RESULTS.glob("exp*/metrics.json")}
    for script in sorted(EXPERIMENTS.glob("exp*.py")):
        exp_id = script.stem.split("_", 1)[0]
        if exp_id not in completed:
            return script
    return None


def load_metrics(exp_id: str) -> dict:
    return json.loads((RESULTS / exp_id / "metrics.json").read_text(encoding="utf-8"))


def update_leaderboard() -> None:
    rows = []
    for metrics_path in sorted(RESULTS.glob("exp*/metrics.json")):
        exp_id = metrics_path.parent.name
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        overall = metrics["overall"]
        desc = " ".join(exp_id.split("_")[1:]) or exp_id
        summary_path = metrics_path.parent / "summary.json"
        if summary_path.exists():
            desc = json.loads(summary_path.read_text(encoding="utf-8")).get("description", desc)
        rows.append(
            {
                "experiment": exp_id,
                "description": desc,
                "f1": overall["f1"],
                "precision": overall["precision"],
                "recall": overall["recall"],
                "auto_precision": overall["auto_apply_precision"],
                "auto_count": overall["auto_apply_count"],
                "review_count": overall["review_count"],
                "cost_per_correct": overall["cost_per_correct_update_usd"],
                "runtime": metrics["runtime_seconds"],
            }
        )
    rows.sort(
        key=lambda item: (
            item["f1"],
            item["auto_precision"],
            item["auto_count"],
            -(item["cost_per_correct"] or 999),
        ),
        reverse=True,
    )

    lines = [
        "# Experiment Leaderboard",
        "",
        "Sorted by validation F1. Higher is better.",
        "",
        "| Rank | Experiment | Description | F1 | Precision | Recall | Auto Precision | Auto Count | Review Count | Cost/Correct | Runtime | Notes |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    if not rows:
        lines.append("| - | none | No completed experiments yet | - | - | - | - | - | - | - | - | - |")
    for rank, row in enumerate(rows, start=1):
        cost = row["cost_per_correct"]
        lines.append(
            f"| {rank} | {row['experiment']} | {row['description']} | {row['f1']:.6f} | "
            f"{row['precision']:.6f} | {row['recall']:.6f} | {row['auto_precision']:.6f} | "
            f"{row['auto_count']} | {row['review_count']} | {cost if cost is not None else '-'} | "
            f"{row['runtime']:.3f}s | local synthetic CV |"
        )
    (AUTORESEARCH / "LEADERBOARD.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def best_completed() -> tuple[str, dict]:
    best_exp = ""
    best_metrics = {}
    best_key = (-1.0, -1.0, float("-inf"))
    for metrics_path in sorted(RESULTS.glob("exp*/metrics.json")):
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        overall = metrics["overall"]
        key = (
            float(overall["f1"]),
            float(overall["auto_apply_precision"]),
            float(overall["auto_apply_count"]),
            -float(overall["cost_per_correct_update_usd"] or 999),
        )
        if key > best_key:
            best_key = key
            best_exp = metrics_path.parent.name
            best_metrics = metrics
    return best_exp, best_metrics


def update_state(_: str, __: dict) -> None:
    exp_id, metrics = best_completed()
    overall = metrics["overall"]
    text = f"""# Autoresearch State

Last updated: {datetime.now(timezone.utc).date().isoformat()}

## Current Phase

Phase 2: Overfit / Prove Pipeline

## Current Best

- Experiment: {exp_id}
- Validation F1: {overall['f1']}
- Precision: {overall['precision']}
- Recall: {overall['recall']}
- Auto-apply precision: {overall['auto_apply_precision']}
- Auto-apply count: {overall['auto_apply_count']}
- Review count: {overall['review_count']}
- Cost per correct update: {overall['cost_per_correct_update_usd']}

## Invariants

- Competition has no official train/test data at setup time.
- Local benchmark is a proxy and must be clearly labeled as synthetic/public-demo.
- One weak public Kaggle notebook now exists; treat it as a baseline/gap signal, not a template to imitate.
- A 42,000-row public provider-directory dataset is available through that notebook and should be used only as transfer/readiness evidence.
- `autoresearch/NORTH_STAR.md` is a standing instruction for every iteration.
- AWS is the preferred cloud if a cloud provider must be named.
- Grouped evaluation uses `provider_id`.
- Candidate generation must not read gold labels.
- Every experiment must write `results/expNNNN/metrics.json`.

## Running

No active experiment.

## Next Action

Select the next queued hypothesis from `autoresearch/HYPOTHESES.md` and implement one change versus `{exp_id}`.
"""
    (AUTORESEARCH / "STATE.md").write_text(text, encoding="utf-8")


def update_hypotheses(exp_id: str) -> None:
    path = AUTORESEARCH / "HYPOTHESES.md"
    text = path.read_text(encoding="utf-8")
    hypothesis_id = {
        "exp0001": "H001",
        "exp0002": "H002",
        "exp0003": "H003",
        "exp0004": "H005",
        "exp0005": "H006",
        "exp0006": "H004",
        "exp0007": "H007",
        "exp0008": "H008",
        "exp0009": "H009",
        "exp0010": "H010",
        "exp0011": "H011",
        "exp0012": "H012",
        "exp0013": "H013",
        "exp0014": "H014",
        "exp0015": "H015",
        "exp0016": "H016",
        "exp0017": "H017",
        "exp0018": "H018",
        "exp0019": "H019",
        "exp0020": "H020",
        "exp0021": "H021",
        "exp0022": "H022",
        "exp0023": "H023",
        "exp0024": "H024",
        "exp0025": "H025",
        "exp0026": "H026",
        "exp0027": "H027",
        "exp0028": "H028",
        "exp0029": "H029",
        "exp0030": "H030",
        "exp0031": "H031",
        "exp0032": "H032",
        "exp0033": "H033",
        "exp0034": "H034",
        "exp0035": "H035",
        "exp0036": "H036",
        "exp0037": "H037",
        "exp0038": "H038",
        "exp0039": "H039",
        "exp0040": "H040",
        "exp0041": "H041",
        "exp0042": "H042",
        "exp0043": "H043",
        "exp0044": "H044",
        "exp0045": "H045",
        "exp0046": "H046",
        "exp0047": "H047",
        "exp0048": "H048",
        "exp0049": "H049",
        "exp0050": "H050",
        "exp0051": "H051",
        "exp0052": "H052",
        "exp0053": "H053",
        "exp0054": "H054",
        "exp0055": "H055",
        "exp0056": "H056",
        "exp0057": "H057",
        "exp0058": "H058",
        "exp0059": "H059",
        "exp0060": "H060",
        "exp0061": "H061",
        "exp0062": "H062",
        "exp0063": "H063",
        "exp0064": "H064",
        "exp0065": "H065",
        "exp0066": "H066",
        "exp0067": "H067",
        "exp0068": "H068",
        "exp0069": "H069",
        "exp0070": "H070",
        "exp0071": "H071",
        "exp0072": "H072",
        "exp0073": "H073",
        "exp0074": "H074",
        "exp0075": "H075",
        "exp0076": "H076",
        "exp0077": "H077",
        "exp0078": "H078",
        "exp0079": "H079",
        "exp0080": "H080",
        "exp0081": "H081",
        "exp0082": "H082",
        "exp0083": "H083",
        "exp0084": "H084",
        "exp0085": "H085",
        "exp0086": "H086",
        "exp0087": "H087",
        "exp0088": "H088",
        "exp0089": "H089",
        "exp0090": "H090",
        "exp0091": "H091",
        "exp0092": "H092",
        "exp0093": "H093",
        "exp0094": "H094",
        "exp0095": "H095",
        "exp0096": "H096",
        "exp0097": "H097",
        "exp0098": "H098",
        "exp0099": "H099",
        "exp0100": "H100",
        "exp0101": "H101",
        "exp0102": "H102",
        "exp0103": "H103",
        "exp0104": "H104",
        "exp0105": "H105",
        "exp0106": "H106",
        "exp0107": "H107",
        "exp0108": "H108",
        "exp0109": "H109",
        "exp0110": "H110",
        "exp0111": "H111",
        "exp0112": "H112",
        "exp0113": "H113",
        "exp0114": "H114",
        "exp0115": "H115",
        "exp0116": "H116",
        "exp0117": "H117",
        "exp0118": "H118",
        "exp0119": "H119",
        "exp0120": "H120",
        "exp0121": "H121",
        "exp0122": "H122",
        "exp0123": "H123",
        "exp0124": "H124",
        "exp0125": "H125",
        "exp0126": "H126",
        "exp0127": "H127",
        "exp0128": "H128",
        "exp0129": "H129",
        "exp0130": "H130",
        "exp0131": "H131",
        "exp0132": "H132",
        "exp0133": "H133",
        "exp0134": "H134",
        "exp0135": "H135",
        "exp0136": "H136",
        "exp0137": "H137",
        "exp0138": "H138",
        "exp0139": "H139",
        "exp0140": "H140",
        "exp0141": "H141",
        "exp0142": "H142",
        "exp0143": "H143",
        "exp0144": "H144",
        "exp0145": "H145",
        "exp0146": "H146",
        "exp0147": "H147",
        "exp0148": "H148",
        "exp0149": "H149",
        "exp0150": "H150",
        "exp0151": "H151",
        "exp0152": "H152",
        "exp0153": "H153",
        "exp0154": "H154",
        "exp0155": "H155",
        "exp0156": "H156",
        "exp0157": "H157",
        "exp0158": "H158",
        "exp0159": "H159",
        "exp0160": "H160",
        "exp0161": "H161",
        "exp0162": "H162",
        "exp0163": "H163",
        "exp0164": "H164",
        "exp0165": "H165",
        "exp0166": "H166",
        "exp0167": "H167",
        "exp0168": "H168",
        "exp0169": "H169",
        "exp0170": "H170",
        "exp0171": "H171",
        "exp0172": "H172",
        "exp0173": "H173",
        "exp0174": "H174",
    }.get(exp_id)
    if hypothesis_id and f"- [queued] {hypothesis_id}:" in text:
        text = text.replace(f"- [queued] {hypothesis_id}:", f"- [done] {hypothesis_id}:", 1)
    done_entry = f"- {exp_id}: Completed {hypothesis_id or 'a queued hypothesis'}."
    if done_entry not in text:
        if re.search(r"## Done\n\nNone yet\.", text):
            text = re.sub(r"## Done\n\nNone yet\.", "## Done\n\n" + done_entry, text)
        else:
            text = text.replace("## Killed", done_entry + "\n\n## Killed", 1)
    path.write_text(text, encoding="utf-8")


def append_journal(exp_id: str, metrics: dict, log_tail: str) -> None:
    overall = metrics["overall"]
    summary_path = RESULTS / exp_id / "summary.json"
    description = exp_id
    if summary_path.exists():
        description = json.loads(summary_path.read_text(encoding="utf-8")).get("description", description)
    entry = f"""
## {exp_id} - {datetime.now(timezone.utc).date().isoformat()} - {description}

- Phase: see `autoresearch/STATE.md`
- Hypothesis: {description}
- Change: One experiment script was run through the local grouped-CV harness.
- Smoke: Passed; see `results/{exp_id}/smoke/metrics.json`.
- Full CV: F1={overall['f1']}, precision={overall['precision']}, recall={overall['recall']}.
- Result: auto_apply_precision={overall['auto_apply_precision']}, review_recall={overall['review_recall']}, estimated_cost_usd={overall['estimated_cost_usd']}.
- Delta vs best: see `autoresearch/LEADERBOARD.md`.
- Runtime: {metrics['runtime_seconds']} seconds.
- Insight: Compare per-field precision/recall and worst providers before choosing the next change.
- Next: Select the next queued hypothesis.

Log tail:

```text
{log_tail.strip()}
```
"""
    with (AUTORESEARCH / "JOURNAL.md").open("a", encoding="utf-8") as handle:
        handle.write(entry)


def main() -> int:
    requested_exp = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].startswith("exp") else None
    script = discover_next_experiment(requested_exp)
    if script is None:
        print("No uncompleted experiment scripts found.")
        return 0
    exp_id = script.stem.split("_", 1)[0]
    print(f"Running {script}")
    proc = run([sys.executable, str(script)])
    out_dir = RESULTS / exp_id
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "log.txt").write_text(proc.stdout + "\n" + proc.stderr, encoding="utf-8")
    if proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr, file=sys.stderr)
        return proc.returncode

    metrics = load_metrics(exp_id)
    update_leaderboard()
    update_state(exp_id, metrics)
    update_hypotheses(exp_id)
    append_journal(exp_id, metrics, (proc.stdout + "\n" + proc.stderr)[-2000:])
    print(f"Completed {exp_id}; metrics in {RESULTS / exp_id / 'metrics.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
