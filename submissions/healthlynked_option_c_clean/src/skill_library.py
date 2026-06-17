from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def skill_slug(name: str) -> str:
    return name.replace("-", "_")


def write_skill_library(candidates: pd.DataFrame, out_dir: Path) -> pd.DataFrame:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for row in candidates.to_dict("records"):
        slug = skill_slug(row["skill_candidate"])
        skill_dir = out_dir / slug
        (skill_dir / "evals").mkdir(parents=True, exist_ok=True)
        (skill_dir / "references").mkdir(parents=True, exist_ok=True)
        (skill_dir / "scripts").mkdir(parents=True, exist_ok=True)
        skill_md = skill_markdown(row)
        (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
        eval_cases = trigger_eval_cases(row)
        (skill_dir / "evals" / "trigger_cases.json").write_text(json.dumps(eval_cases, indent=2), encoding="utf-8")
        (skill_dir / "references" / "authority_tier.md").write_text(authority_reference(row), encoding="utf-8")
        rows.append(
            {
                "skill_candidate": row["skill_candidate"],
                "skill_dir": skill_dir.as_posix(),
                "authority_tier": row["authority_tier"],
                "eval_cases": len(eval_cases),
                "owner": row["owner"],
            }
        )
    return pd.DataFrame(rows)


def skill_markdown(row: dict[str, Any]) -> str:
    title = row["skill_candidate"].replace("-", " ").title()
    description = (
        f"Use when the task involves {row['trigger']}. "
        f"Do NOT use for {row['anti_trigger']}."
    )
    return f"""---
name: {row['skill_candidate']}
description: |
  {description}
version: 0.1.0
allowed-tools: [Read, Bash]
metadata:
  owner: {row['owner']}
  authority_tier: {row['authority_tier']}
---
# {title}

## When To Use

- {row['trigger']}

## When Not To Use

- {row['anti_trigger']}

## Authority Tier

- `{row['authority_tier']}`
- See `references/authority_tier.md`.

## Workflow

1. Load only the deterministic assets needed for the request.
2. Use structured package artifacts instead of free-form memory.
3. Apply the required eval before trusting output: {row['required_eval']}.
4. Never exceed this skill's authority tier.

## Deterministic Assets

- {row['deterministic_assets']}

## Eval Coverage

- Positive and negative trigger cases live in `evals/trigger_cases.json`.
- Side-effecting or review-affecting workflows require trajectory/red-team coverage before action.
"""


def trigger_eval_cases(row: dict[str, Any]) -> list[dict[str, Any]]:
    skill = row["skill_candidate"]
    trigger = row["trigger"]
    anti = row["anti_trigger"]
    positives = [
        f"Check {trigger} for this provider directory batch.",
        f"I need help with {trigger} before review routing.",
        f"Run the {skill} workflow for the latest package artifacts.",
    ]
    negatives = [
        f"Do {anti} instead.",
        "Summarize the executive summary in plain English.",
        "Package the current submission zip without changing workflow logic.",
    ]
    cases = []
    for idx, text in enumerate(positives, start=1):
        cases.append({"case_id": f"{skill}_positive_{idx}", "input": text, "expected_skill": skill, "should_trigger": True})
    for idx, text in enumerate(negatives, start=1):
        cases.append({"case_id": f"{skill}_negative_{idx}", "input": text, "expected_skill": skill, "should_trigger": False})
    return cases


def authority_reference(row: dict[str, Any]) -> str:
    return f"""# Authority Tier

- Skill: `{row['skill_candidate']}`
- Owner: `{row['owner']}`
- Authority tier: `{row['authority_tier']}`

## Required Eval

{row['required_eval']}

## Deterministic Assets

{row['deterministic_assets']}

## Rule

The skill must not perform work described by its anti-trigger: {row['anti_trigger']}.
"""
