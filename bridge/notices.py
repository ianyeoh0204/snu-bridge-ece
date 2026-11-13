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
LINK = re.compile(r'<a[^>]+bbsidx=(\d+)[^"]*"[^>]*>\s*<span[^>]*>(.*?)</span>\s*</a>', re.S)
CELL = re.compile(r'<td class="text-center hidden-sm-down[^"]*">([^<]*)</td>')
CATEGORY = re.compile(r'class="bbs-category">\s*\[?([^<\]]*)\]?\s*<')  # some departments print "[학부]" above the title instead
DATE = re.compile(r"(\d{4})[.-](\d{2})[.-](\d{2})")
# A speaker's name in a seminar title. The original notice keeps it; this site does not copy personal names.
NAMED = re.compile(r"\b(Prof\.|Professor|Dr\.)\s*[A-Z][\w'-]+(?:[ -][A-Z][\w'-]+){0,3}")


def _fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", "replace")


def _rows(page: str) -> list[dict]:
    found = []
    for row in ROW.findall(page):
        link = LINK.search(row)
        date = link and DATE.search(row[:link.start()] + row[link.end():])  # a title can contain a date of its own
        if not (link and date):
            continue
        cells = [html.unescape(c).strip() for c in CELL.findall(row)]
        category = CATEGORY.search(row)
        title = html.unescape(re.sub(r"<[^>]+>", "", link.group(2))).strip()
        found.append({
            "id": int(link.group(1)),
            "title_ko": NAMED.sub(r"\1 [name]", title),
            "date": "-".join(date.groups()),
            "audience_ko": next((c for c in cells if c and not c.isdigit()), category.group(1).strip() if category else ""),
            "pinned": 'class="noti"' in row,
        })
    return found


def update(department: str) -> tuple[list[dict], list[str]]:
    """Fetch list pages back to the configured date. Returns all notices and a list of what changed."""
    config = json.loads((ROOT / "sources" / department / "config.json").read_text(encoding="utf-8"))["board"]
    store = ROOT / "data" / department / "notices.json"
    known = {n["id"]: n for n in json.loads(store.read_text(encoding="utf-8"))} if store.exists() else {}
    today, changes = datetime.date.today().isoformat(), []
    first = config.get("first_page", 0)  # some departments number their list pages from 1
    for page in range(first, first + 40):
        rows = _rows(_fetch(f"{config['list_url']}?page={page}"))
        if page == first and not rows:  # a maintenance page or a changed layout must never pass as "nothing new"
            raise RuntimeError(f"No notices could be read on the first list page of {department}. Nothing was changed.")
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
        if not rows or (dated and max(dated) < config["since"]):  # a page of pinned notices only is not the end
            break
        time.sleep(config.get("pause", 1))  # seconds between requests; a slow site gets more (see the config)
    notices = sorted(known.values(), key=lambda n: (n["date"], n["id"]), reverse=True)
    store.write_text(json.dumps(notices, ensure_ascii=False, indent=1), encoding="utf-8")
    return notices, changes
