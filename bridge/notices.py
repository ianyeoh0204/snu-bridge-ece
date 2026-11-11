"""Step 4 of the pipeline: read the department board's list pages and keep a record of every notice.

Only list pages are read here. robots.txt disallows /webdata, so images and attachments are never fetched.
"""
from __future__ import annotations

import datetime
import html
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENT = "SNU-Bridge/0.1 (student project; one request per second)"
ROW = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
LINK = re.compile(r'bbsidx=(\d+)"[^>]*>\s*<span[^>]*>(.*?)</span>', re.S)
CELL = re.compile(r'<td class="text-center hidden-sm-down[^"]*">([^<]*)</td>')
DATE = re.compile(r"(\d{4})\.(\d{2})\.(\d{2})\.")


def _fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", "replace")


def _rows(page: str) -> list[dict]:
    found = []
    for row in ROW.findall(page):
        link, date = LINK.search(row), DATE.search(row)
        if not (link and date):
            continue
        cells = [html.unescape(c).strip() for c in CELL.findall(row)]
        found.append({
            "id": int(link.group(1)),
            "title_ko": html.unescape(re.sub(r"<[^>]+>", "", link.group(2))).strip(),
            "date": "-".join(date.groups()),
            "audience_ko": next((c for c in cells if c and not c.isdigit()), ""),
            "pinned": 'class="noti"' in row,
        })
    return found


def update(department: str) -> tuple[list[dict], list[str]]:
    """Fetch list pages back to the configured date. Returns all notices and a list of what changed."""
    config = json.loads((ROOT / "sources" / department / "config.json").read_text(encoding="utf-8"))["board"]
    store = ROOT / "data" / department / "notices.json"
    known = {n["id"]: n for n in json.loads(store.read_text(encoding="utf-8"))} if store.exists() else {}
    today, changes = datetime.date.today().isoformat(), []
    for page in range(40):
        rows = _rows(_fetch(f"{config['list_url']}?page={page}"))
        for row in rows:
            if row["date"] < config["since"]:
                continue
            old = known.get(row["id"])
            if old is None:
                known[row["id"]] = dict(row, url=config["detail_url"].format(id=row["id"]), first_seen=today, title_history=[])
                changes.append(f"new {row['id']} {row['title_ko']}")
            elif old["title_ko"] != row["title_ko"]:
                old["title_history"].append({"until": today, "title_ko": old["title_ko"]})
                old.update(title_ko=row["title_ko"], pinned=row["pinned"])
                changes.append(f"retitled {row['id']} {row['title_ko']}")
        dated = [r["date"] for r in rows if not r["pinned"]]
        if not dated or max(dated) < config["since"]:
            break
        time.sleep(1)
    notices = sorted(known.values(), key=lambda n: (n["date"], n["id"]), reverse=True)
    store.write_text(json.dumps(notices, ensure_ascii=False, indent=1), encoding="utf-8")
    return notices, changes
