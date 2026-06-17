from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd


VALID_AUTHORITY_TIERS = {"read-only", "draft-only", "action-allowed-after-approval"}
SAFE_ALLOWED_TOOLS = {"Read", "Bash"}


def evaluate_skill_library(skills_dir: Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for skill_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
        rows.extend(evaluate_skill(skill_dir))
    frame = pd.DataFrame(rows)
    passed = bool(frame["passed"].all()) if not frame.empty else False
    summary = {
        "passed": passed,
        "skills": int(frame["skill"].nunique()) if not frame.empty else 0,
        "checks": int(len(frame)),
        "failed_checks": int((~frame["passed"]).sum()) if not frame.empty else 0,
        "positive_trigger_cases": int(frame.loc[frame["check"] == "positive_trigger_cases", "detail_value"].astype(int).sum()) if not frame.empty else 0,
        "negative_trigger_cases": int(frame.loc[frame["check"] == "negative_trigger_cases", "detail_value"].astype(int).sum()) if not frame.empty else 0,
    }
    return frame, summary


def evaluate_skill(skill_dir: Path) -> list[dict[str, Any]]:
    skill = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    evals_path = skill_dir / "evals" / "trigger_cases.json"
    authority_path = skill_dir / "references" / "authority_tier.md"
    text = skill_md.read_text(encoding="utf-8") if skill_md.exists() else ""
    cases = json.loads(evals_path.read_text(encoding="utf-8")) if evals_path.exists() else []
    authority_text = authority_path.read_text(encoding="utf-8") if authority_path.exists() else ""
    metadata = parse_frontmatter(text)
    positives = [case for case in cases if case.get("should_trigger") is True]
    negatives = [case for case in cases if case.get("should_trigger") is False]
    allowed_tools = set(parse_allowed_tools(metadata.get("allowed-tools", "")))
    authority_tier = metadata.get("metadata.authority_tier", "")
    markdown_word_count = len(re.findall(r"\b\w+\b", text))
    rows = [
        check(skill, "skill_markdown_exists", skill_md.exists() and len(text) > 500, len(text), "SKILL.md should be present and substantive."),
        check(skill, "frontmatter_name", metadata.get("name", "").replace("-", "_") == skill, metadata.get("name", ""), "Frontmatter name should match folder."),
        check(skill, "valid_authority_tier", authority_tier in VALID_AUTHORITY_TIERS, authority_tier, "Authority tier must be one of the approved tiers."),
        check(skill, "safe_allowed_tools", bool(allowed_tools) and allowed_tools <= SAFE_ALLOWED_TOOLS, ",".join(sorted(allowed_tools)), "Generated skeleton skills should only permit read/local script tools."),
        check(skill, "positive_trigger_cases", len(positives) == 3, len(positives), "Each skill needs exactly three positive trigger evals."),
        check(skill, "negative_trigger_cases", len(negatives) == 3, len(negatives), "Each skill needs exactly three negative trigger evals."),
        check(skill, "eval_case_skill_match", all(case.get("expected_skill", "").replace("-", "_") == skill for case in cases), len(cases), "Every trigger case should target this skill."),
        check(skill, "authority_reference_exists", authority_path.exists() and authority_tier in authority_text, len(authority_text), "Authority reference should exist and repeat the tier."),
        check(skill, "context_budget_hygiene", markdown_word_count <= 450, markdown_word_count, "SKILL.md should stay compact enough for progressive disclosure."),
    ]
    if authority_tier == "action-allowed-after-approval":
        rows.append(
            check(
                skill,
                "approval_language_present",
                "approval" in text.lower() and "approval" in authority_text.lower(),
                "approval",
                "Action-allowed skills must explicitly require approval.",
            )
        )
    return rows


def check(skill: str, name: str, passed: bool, detail_value: Any, note: str) -> dict[str, Any]:
    return {
        "skill": skill,
        "check": name,
        "passed": bool(passed),
        "detail_value": detail_value,
        "note": note,
    }


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    values: dict[str, str] = {}
    section_stack: list[str] = []
    for raw_line in parts[1].splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.strip() == "|":
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        value = value.strip()
        if indent == 0:
            section_stack = [key]
            values[key] = value
        elif section_stack:
            values[f"{section_stack[0]}.{key}"] = value
    return values


def parse_allowed_tools(value: str) -> list[str]:
    return [item.strip() for item in value.strip("[]").split(",") if item.strip()]
