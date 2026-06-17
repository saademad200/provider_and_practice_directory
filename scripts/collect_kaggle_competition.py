#!/usr/bin/env python3
"""Collect a local Kaggle competition research bundle.

This script intentionally saves raw API/page responses alongside a concise
summary so the final analysis can be checked against source material.
"""

from __future__ import annotations

import csv
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kaggle import api
from kagglesdk.competitions.types import competition_api_service as comp_types
from kagglesdk.search.types import search_api_service as search_types


SLUG = "provider-practice-directory-update-pipeline"
TITLE = "Provider & Practice Directory Update Pipeline"
OUT_DIR = Path("provider-practice-directory-update-pipeline_kaggle_bundle")


def as_jsonable(obj: Any) -> Any:
    if obj is None:
        return None
    if isinstance(obj, list):
        return [as_jsonable(item) for item in obj]
    if isinstance(obj, dict):
        return {key: as_jsonable(value) for key, value in obj.items()}
    if hasattr(obj, "to_json"):
        return json.loads(obj.to_json())
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    return obj


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(as_jsonable(data), indent=2, sort_keys=True), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def get_competition(client: Any) -> Any:
    request = comp_types.ApiGetCompetitionRequest()
    request.competition_name = SLUG
    return client.competitions.competition_api_client.get_competition(request)


def get_files_summary(client: Any) -> Any:
    request = comp_types.ApiGetCompetitionDataFilesSummaryRequest()
    request.competition_name = SLUG
    return client.competitions.competition_api_client.get_competition_data_files_summary(request)


def list_data_files(client: Any) -> Any:
    request = comp_types.ApiListDataFilesRequest()
    request.competition_name = SLUG
    request.page_size = 100
    return client.competitions.competition_api_client.list_data_files(request)


def list_data_tree(client: Any) -> Any:
    request = comp_types.ApiListDataTreeFilesRequest()
    request.competition_name = SLUG
    request.page_size = 100
    return client.competitions.competition_api_client.list_data_tree_files(request)


def get_leaderboard(client: Any) -> Any:
    request = comp_types.ApiGetLeaderboardRequest()
    request.competition_name = SLUG
    request.page_size = 100
    return client.competitions.competition_api_client.get_leaderboard(request)


def list_submissions(client: Any) -> Any:
    request = comp_types.ApiListSubmissionsRequest()
    request.competition_name = SLUG
    request.page_size = 100
    return client.competitions.competition_api_client.list_submissions(request)


def search_entities(client: Any, query: str, document_types: list[Any], source_type: Any | None = None) -> Any:
    request = search_types.ListEntitiesRequest()
    request.page_size = 50
    request.canonical_order_by = search_types.ListSearchContentOrderBy.LIST_SEARCH_CONTENT_ORDER_BY_DATE_UPDATED
    filters = search_types.ListEntitiesFilters()
    filters.query = query
    filters.document_types = document_types
    if source_type is not None:
        discussion_filters = search_types.ApiSearchDiscussionsFilters()
        discussion_filters.source_type = source_type
        filters.discussion_filters = discussion_filters
    request.filters = filters
    return client.search.search_api_client.list_entities(request)


def collect_pages() -> dict[str, dict[str, Any]]:
    import requests

    pages = {}
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 Kaggle competition research collector",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    sections = ["overview", "data", "code", "discussion", "leaderboard", "rules"]
    for section in sections:
        url = f"https://www.kaggle.com/competitions/{SLUG}/{section}"
        response = session.get(url, headers=headers, timeout=30)
        html = response.text
        write_text(OUT_DIR / "raw" / "pages" / f"{section}.html", html)
        title_match = re.search(r"<title>(.*?)</title>", html, flags=re.I | re.S)
        pages[section] = {
            "url": url,
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type"),
            "bytes": len(response.content),
            "title": re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else None,
            "has_next_data": "__NEXT_DATA__" in html,
            "has_competition_slug": SLUG in html,
        }
    return pages


def extract_download() -> list[dict[str, Any]]:
    data_dir = OUT_DIR / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    api.competition_download_files(SLUG, path=str(data_dir), force=True, quiet=True)
    zip_path = data_dir / f"{SLUG}.zip"
    files = []
    if zip_path.exists():
        with zipfile.ZipFile(zip_path) as archive:
            for item in archive.infolist():
                files.append({"name": item.filename, "size": item.file_size, "modified": item.date_time})
            archive.extractall(data_dir)
    return files


def csv_from_records(path: Path, records: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({field: record.get(field, "") for field in fields})


def summarize_search_docs(data: dict[str, Any]) -> list[dict[str, Any]]:
    records = []
    for document in data.get("documents") or []:
        owner = document.get("ownerUser") or {}
        records.append(
            {
                "documentType": document.get("documentType"),
                "title": document.get("title"),
                "slug": document.get("slug"),
                "owner": owner.get("userName") or owner.get("displayName"),
                "votes": document.get("votes"),
                "createTime": document.get("createTime"),
                "updateTime": document.get("updateTime"),
                "isPrivate": document.get("isPrivate"),
            }
        )
    return records


def make_report(bundle: dict[str, Any], downloaded_files: list[dict[str, Any]]) -> None:
    competition = bundle["competition"]
    data_files = (bundle["data_files"] or {}).get("files") or []
    kernels_by_sort = bundle["kernels_by_sort"]
    leaderboard = bundle.get("leaderboard") or {}
    submissions = bundle.get("submissions") or {}
    discussion_search = bundle["search"].get("discussion_competition_source_title") or {}
    exact_search = bundle["search"].get("exact_title_all_docs") or {}
    discussion_docs = discussion_search.get("documents") or []
    exact_search_docs = exact_search.get("documents") or []

    unique_notebooks = {}
    for notebooks in kernels_by_sort.values():
        if not isinstance(notebooks, list):
            continue
        for notebook in notebooks or []:
            ref = notebook.get("ref") or notebook.get("id") or notebook.get("title")
            unique_notebooks[ref] = notebook

    lines = [
        f"# {competition.get('title', TITLE)}",
        "",
        f"Collected: {bundle['collected_at_utc']}",
        f"Source: https://www.kaggle.com/competitions/{SLUG}",
        "",
        "## Competition Facts",
        "",
        f"- ID: {competition.get('id')}",
        f"- Host: {competition.get('hostName')}",
        f"- Category: {competition.get('category')}",
        f"- Reward: {competition.get('reward')}",
        f"- Created: {competition.get('dateCreated')}",
        f"- Enabled: {competition.get('enabledDate')}",
        f"- Deadline: {competition.get('deadline')}",
        f"- Team count: {competition.get('teamCount')}",
        f"- User has entered: {competition.get('userHasEntered')}",
        f"- Max daily submissions: {competition.get('maxDailySubmissions')}",
        f"- Max team size: {competition.get('maxTeamSize')}",
        "",
        "## Description",
        "",
        competition.get("description") or "",
        "",
        "## Data",
        "",
        f"- Kaggle data-file API returned {len(data_files)} file(s).",
        f"- Downloaded archive contains {len(downloaded_files)} file(s).",
    ]

    for item in downloaded_files:
        lines.append(f"- {item['name']} ({item['size']} bytes)")

    note_path = OUT_DIR / "data" / "NOTE.md"
    if note_path.exists():
        lines.extend(["", "### NOTE.md", "", "```text", note_path.read_text(encoding="utf-8").strip(), "```"])

    lines.extend(
        [
            "",
            "## Notebooks",
            "",
            f"- Competition-scoped kernels returned {len(unique_notebooks)} unique notebook(s) across {len(kernels_by_sort)} sort modes.",
        ]
    )
    if unique_notebooks:
        for notebook in unique_notebooks.values():
            lines.append(f"- {notebook.get('ref')}: {notebook.get('title')} by {notebook.get('author')} ({notebook.get('totalVotes')} votes)")
    else:
        lines.append("- No competition-scoped notebooks were found.")

    lines.extend(
        [
            "",
            "## Discussions",
            "",
            f"- Competition-source discussion search returned {len(discussion_docs)} document(s) for the exact title query.",
            "- The installed Kaggle CLI/SDK does not expose a direct competition discussion-list endpoint, so raw discussion search responses are saved for audit.",
        ]
    )

    if discussion_docs:
        for doc in discussion_docs[:20]:
            lines.append(f"- {doc.get('documentType')}: {doc.get('title')} ({doc.get('slug')})")
    else:
        lines.append("- No directly related discussion topics/comments were found via Kaggle search.")

    lines.extend(
        [
            "",
            "## Leaderboard And Submissions",
            "",
            f"- Leaderboard entries returned: {len(leaderboard.get('submissions') or leaderboard.get('entries') or [])}",
            f"- Current account submissions returned: {len(submissions.get('submissions') or [])}",
            "",
            "## Page Fetches",
            "",
        ]
    )
    for section, info in bundle["pages"].items():
        lines.append(f"- {section}: HTTP {info['status_code']}, {info['bytes']} bytes, slug_in_html={info['has_competition_slug']}")

    lines.extend(
        [
            "",
            "## Search Caveat",
            "",
            f"Exact-title global search returned {len(exact_search_docs)} document(s), but Kaggle global search can return broad/unrelated hits.",
            "Use competition-scoped API results as the authoritative source for notebooks and files.",
        ]
    )

    write_text(OUT_DIR / "README.md", "\n".join(lines).rstrip() + "\n")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    downloaded_files = extract_download()

    with api.build_kaggle_client() as client:
        competition = as_jsonable(get_competition(client))
        competitions_list = as_jsonable(api.competitions_list(search=SLUG, page_size=20))
        files_summary = as_jsonable(get_files_summary(client))
        data_files = as_jsonable(list_data_files(client))
        data_tree = as_jsonable(list_data_tree(client))
        leaderboard = as_jsonable(get_leaderboard(client))
        submissions = as_jsonable(list_submissions(client))

        kernels_by_sort = {}
        for sort_by in [None, "voteCount", "dateCreated", "hotness", "commentCount", "recentlyUpdated"]:
            label = sort_by or "default"
            try:
                kernels_by_sort[label] = as_jsonable(
                    api.kernels_list(competition=SLUG, sort_by=sort_by, page_size=100)
                )
            except Exception as exc:
                kernels_by_sort[label] = {"error": f"{type(exc).__name__}: {exc}"}

        doc_all = [
            search_types.DocumentType.COMPETITION,
            search_types.DocumentType.KERNEL,
            search_types.DocumentType.TOPIC,
            search_types.DocumentType.COMMENT,
            search_types.DocumentType.DATASET,
            search_types.DocumentType.MODEL,
        ]
        search_payloads = {
            "exact_slug_all_docs": as_jsonable(search_entities(client, SLUG, doc_all)),
            "exact_title_all_docs": as_jsonable(search_entities(client, TITLE, doc_all)),
            "discussion_competition_source_title": as_jsonable(
                search_entities(
                    client,
                    TITLE,
                    [search_types.DocumentType.TOPIC, search_types.DocumentType.COMMENT],
                    search_types.SearchDiscussionsSourceType.SEARCH_DISCUSSIONS_SOURCE_TYPE_COMPETITION,
                )
            ),
            "discussion_competition_source_slug": as_jsonable(
                search_entities(
                    client,
                    SLUG,
                    [search_types.DocumentType.TOPIC, search_types.DocumentType.COMMENT],
                    search_types.SearchDiscussionsSourceType.SEARCH_DISCUSSIONS_SOURCE_TYPE_COMPETITION,
                )
            ),
        }

    pages = collect_pages()

    bundle = {
        "slug": SLUG,
        "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        "competition": competition,
        "competitions_list_search": competitions_list,
        "files_summary": files_summary,
        "data_files": data_files,
        "data_tree": data_tree,
        "downloaded_files": downloaded_files,
        "leaderboard": leaderboard,
        "submissions": submissions,
        "kernels_by_sort": kernels_by_sort,
        "search": search_payloads,
        "pages": pages,
    }

    write_json(OUT_DIR / "raw" / "sdk" / "competition.json", competition)
    write_json(OUT_DIR / "raw" / "sdk" / "competitions_list_search.json", competitions_list)
    write_json(OUT_DIR / "raw" / "sdk" / "files_summary.json", files_summary)
    write_json(OUT_DIR / "raw" / "sdk" / "data_files.json", data_files)
    write_json(OUT_DIR / "raw" / "sdk" / "data_tree.json", data_tree)
    write_json(OUT_DIR / "raw" / "sdk" / "leaderboard.json", leaderboard)
    write_json(OUT_DIR / "raw" / "sdk" / "submissions.json", submissions)
    write_json(OUT_DIR / "raw" / "sdk" / "kernels_by_sort.json", kernels_by_sort)
    write_json(OUT_DIR / "raw" / "sdk" / "search.json", search_payloads)
    write_json(OUT_DIR / "raw" / "pages" / "page_fetch_summary.json", pages)
    write_json(OUT_DIR / "competition_bundle.json", bundle)

    all_search_records = []
    for name, payload in search_payloads.items():
        for record in summarize_search_docs(payload):
            record["search"] = name
            all_search_records.append(record)
    csv_from_records(
        OUT_DIR / "search_results.csv",
        all_search_records,
        ["search", "documentType", "title", "slug", "owner", "votes", "createTime", "updateTime", "isPrivate"],
    )

    make_report(bundle, downloaded_files)
    print(f"Wrote Kaggle research bundle to {OUT_DIR.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
