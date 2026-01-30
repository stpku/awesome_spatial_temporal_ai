#!/usr/bin/env python3
"""Generate repository metrics and badge endpoint JSONs.

Outputs:
- reports/summary.json
- reports/summary.md
- reports/badges/entries.json
- reports/badges/broken_rate.json
- reports/badges/stale.json
- reports/badges/updated.json
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

# Import from src.core (Phase 3 migration)
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.core.config import Config
from src.core.io import load_json, save_json
from src.core.logger import Logger

logger = Logger()

# Use Config for paths
DATA_DIR = Config.DATA_DIR
REPORTS_DIR = Config.REPORTS_DIR
BADGES_DIR = Config.BADGES_DIR

ensure_dirs = Config.ensure_report_dirs  # Reuse Config method


# Backward compatibility: keep load_json signature
def load_json_compat(path: Path):
    return load_json(path)


def count_projects(data):
    total = 0
    if not data:
        return 0
    for cat in data.get("categories", []):
        total += len(cat.get("projects", []))
    return total


def count_latest(data):
    if not data:
        return 0
    return len(data.get("spatial_intelligence", [])) + len(data.get("world_models", []))


def count_conferences(data):
    if not data:
        return 0
    return len(data.get("conferences", []))


def count_journals(data):
    if not data:
        return 0
    return len(data.get("international", [])) + len(data.get("chinese", []))


def count_datasets(data):
    if not data:
        return 0
    return len(data.get("datasets", []))


def count_media(data):
    if not data:
        return 0
    return len(data.get("wechat_publications", [])) + len(data.get("newsletters", []))


def count_papers(data):
    if not data:
        return 0
    return len(data.get("papers", []))


def parse_date(s: str):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except Exception:
        return None


def compute_stale_and_latest(projects_data):
    stale_count = 0
    latest_date = None
    cutoff = datetime.utcnow() - timedelta(days=90)

    if projects_data:
        for cat in projects_data.get("categories", []):
            for proj in cat.get("projects", []):
                d = parse_date(proj.get("last_updated", ""))
                if d:
                    if latest_date is None or d > latest_date:
                        latest_date = d
                    if d < cutoff:
                        stale_count += 1

    return stale_count, latest_date or datetime.utcnow()


def read_broken_links():
    data = load_json_compat(REPORTS_DIR / "broken_links.json")
    if not data:
        return 0, 0
    total = int(data.get("total_checked", 0))
    broken = int(data.get("broken_count", 0))
    return total, broken


def write_summary(summary):
    (REPORTS_DIR / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # human-readable markdown
    lines = [
        "# Repository Metrics Summary",
        "",
        f"Last Update: {summary['updated_at']}",
        "",
        "## Totals",
        f"- Entries: {summary['totals']['entries']}",
        f"- Projects: {summary['totals']['projects']}",
        f"- Latest Projects: {summary['totals']['latest']}",
        f"- Papers: {summary['totals']['papers']}",
        f"- Datasets: {summary['totals']['datasets']}",
        f"- Conferences: {summary['totals']['conferences']}",
        f"- Journals: {summary['totals']['journals']}",
        f"- Media: {summary['totals']['media']}",
        "",
        "## Quality",
        f"- Broken-link rate: {summary['quality']['broken_rate']:.2%}",
        f"- Broken-link count: {summary['quality']['broken_count']}",
        f"- Stale count (last_updated > 90 days): {summary['quality']['stale_count']}",
    ]
    (REPORTS_DIR / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def badge_json(label: str, message: str, color: str = "blue"):
    return {
        "schemaVersion": 1,
        "label": label,
        "message": message,
        "color": color,
    }


def write_badges(summary):
    # entries
    entries = str(summary["totals"]["entries"])
    (BADGES_DIR / "entries.json").write_text(
        json.dumps(badge_json("entries", entries, "blue")), encoding="utf-8"
    )

    # broken rate
    rate = summary["quality"]["broken_rate"]
    if rate < 0.02:
        color = "green"
    elif rate < 0.05:
        color = "yellow"
    else:
        color = "red"
    (BADGES_DIR / "broken_rate.json").write_text(
        json.dumps(badge_json("broken links", f"{rate:.1%}", color)),
        encoding="utf-8",
    )

    # stale count
    stale = str(summary["quality"]["stale_count"])
    color = "orange" if summary["quality"]["stale_count"] > 0 else "green"
    (BADGES_DIR / "stale.json").write_text(
        json.dumps(badge_json("stale", stale, color)), encoding="utf-8"
    )

    # last update
    (BADGES_DIR / "updated.json").write_text(
        json.dumps(badge_json("last update", summary["updated_at"], "informational")),
        encoding="utf-8",
    )


def main():
    ensure_dirs()

    projects = load_json_compat(DATA_DIR / "github_projects.json")
    latest = load_json_compat(DATA_DIR / "latest_projects.json")
    conferences = load_json_compat(DATA_DIR / "conferences.json")
    journals = load_json_compat(DATA_DIR / "journals.json")
    datasets = load_json_compat(DATA_DIR / "datasets.json")
    media = load_json_compat(DATA_DIR / "media_channels.json")
    papers = load_json_compat(DATA_DIR / "papers.json")

    totals = {
        "projects": count_projects(projects),
        "latest": count_latest(latest),
        "conferences": count_conferences(conferences),
        "journals": count_journals(journals),
        "datasets": count_datasets(datasets),
        "media": count_media(media),
        "papers": count_papers(papers),
    }
    totals["entries"] = sum(totals.values())

    stale_count, latest_date = compute_stale_and_latest(projects)

    total_links, broken_links = read_broken_links()
    broken_rate = (broken_links / total_links) if total_links else 0.0

    updated_at = (latest_date).strftime("%Y-%m-%d")

    summary = {
        "schemaVersion": 1,
        "updated_at": updated_at,
        "totals": totals,
        "quality": {
            "broken_rate": broken_rate,
            "broken_count": broken_links,
            "stale_count": stale_count,
        },
    }

    write_summary(summary)
    write_badges(summary)

    print("Metrics generated:")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
