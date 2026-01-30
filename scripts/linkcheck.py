#!/usr/bin/env python3
"""Concurrent link checker for awesomelist JSON files.

Outputs reports/broken_links.json with structure:
{
  "total_checked": int,
  "broken_count": int,
  "broken": [ {"file": str, "name": str, "url": str, "status": int, "error": str } ]
}
"""

import json
import concurrent.futures
import urllib.request
import urllib.error
import urllib.parse
import ssl
from pathlib import Path
import sys

# Import from src.core (Phase 3 migration)
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.core.config import Config
from src.core.logger import Logger

logger = Logger()

# Use Config for all settings
TIMEOUT = Config.LINK_CHECK_TIMEOUT
MAX_WORKERS = Config.MAX_WORKERS
DATA_DIR = Config.DATA_DIR
REPORTS_DIR = Config.REPORTS_DIR
SOFT_FAIL_DOMAINS = Config.SOFT_FAIL_DOMAINS

ensure_dirs = Config.ensure_report_dirs


def iter_links():
    """Iterate over all URLs in awesomelist JSON files."""
    files = [
        ("github_projects.json", "project", lambda d: d.get("categories", []), lambda c: c.get("projects", []), "name"),
        ("latest_projects.json", "latest", lambda d: [d.get("spatial_intelligence", []), d.get("world_models", [])], lambda s: s, "name"),
        ("conferences.json", "conference", lambda d: d.get("conferences", [])),
        ("journals.json", "journal", lambda d: d.get("international", []) + d.get("chinese", [])),
        ("datasets.json", "dataset", lambda d: d.get("datasets", [])),
        ("media_channels.json", "media", lambda d: d.get("wechat_publications", []) + d.get("newsletters", [])),
        ("papers.json", "paper", lambda d: d.get("papers", [])),
    ]

    for file_info in files:
        if len(file_info) == 5:
            # Nested structure (github_projects, latest_projects)
            filename, kind, root_fn, list_fn, name_field = file_info
            path = DATA_DIR / filename
            if not path.exists():
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue

            roots = root_fn(data)
            if isinstance(roots, list) and roots and not isinstance(roots[0], dict):
                # for latest_projects where roots is [list1, list2]
                for sub in roots:
                    for item in list_fn(sub):
                        url = item.get("url")
                        name = item.get(name_field, "")
                        if isinstance(url, str) and url.startswith(("http://", "https://")):
                            yield filename, kind, name, url
            else:
                for root in roots:
                    for item in list_fn(root):
                        url = item.get("url")
                        name = item.get(name_field, "")
                        if isinstance(url, str) and url.startswith(("http://", "https://")):
                            yield filename, kind, name, url
        else:
            # Flat structure (conferences, journals, datasets, media_channels, papers)
            filename, kind, items_fn = file_info
            path = DATA_DIR / filename
            if not path.exists():
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue

            items = items_fn(data)
            name_field = "title" if kind == "paper" else "name"
            for item in items:
                url = item.get("url")
                name = item.get(name_field, "")
                if isinstance(url, str) and url.startswith(("http://", "https://")):
                    yield filename, kind, name, url


def check_url(url: str):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
            status = getattr(resp, "status", 200)
            return status, None
    except urllib.error.HTTPError as e:
        return e.code, str(e)
    except Exception as e:
        # try GET fallback for servers not supporting HEAD
        req = urllib.request.Request(url, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
                status = getattr(resp, "status", 200)
                return status, None
        except Exception as e2:
            return -1, str(e2)


def domain_from_url(url: str):
    try:
        return urllib.parse.urlparse(url).netloc
    except Exception:
        return ""


def main():
    ensure_dirs()
    broken = []
    total = 0

    items = list(iter_links())
    total = len(items)

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futs = {ex.submit(check_url, url): (filename, kind, name, url) for (filename, kind, name, url) in items}
        for fut in concurrent.futures.as_completed(futs):
            filename, kind, name, url = futs[fut]
            status, err = fut.result()
            dom = domain_from_url(url)
            if status >= 400 or status == -1:
                if dom in SOFT_FAIL_DOMAINS:
                    # soft fail, ignore
                    continue
                broken.append({
                    "file": filename,
                    "kind": kind,
                    "name": name,
                    "url": url,
                    "status": status,
                    "error": err,
                })

    report = {
        "total_checked": total,
        "broken_count": len(broken),
        "broken": broken,
    }
    (REPORTS_DIR / "broken_links.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"summary": {"total": total, "broken": len(broken)}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
