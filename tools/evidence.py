# -*- coding: utf-8 -*-
"""Count what the "Why and how" page claims, from the department's own public pages.

Reads the list pages of the Korean academic board and of the English notice board back to 1 January 2024
(one request per second, list pages only) and writes data/ECE/evidence.json: posts and views per year on each
board, the most-read Korean notices of the current year, and every English post of the period. Run by hand when the numbers should be refreshed:
    .venv/bin/python tools/evidence.py
"""
import datetime
import html
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from bridge.notices import _fetch, _rows  # noqa: E402

SINCE = "2024-01-01"
KOREAN = "https://ece.snu.ac.kr/community/academics"
ENGLISH = "https://ece.snu.ac.kr/en/community/notice"
MONTH = {m: i + 1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
VIEWS = re.compile(r"<td[^>]*>\s*(\d+)\s*</td>")  # the last all-digit cell of a row is its view count


def korean() -> list[dict]:
    found = {}
    for page in range(200):
        raw = _fetch(f"{KOREAN}?page={page}")
        time.sleep(1)
        rows = _rows(raw)
        views = {}
        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", raw, flags=re.S):
            link, count = re.search(r"bbsidx=(\d+)", row), VIEWS.findall(row)
            if link and count:
                views[int(link.group(1))] = int(count[-1])
        for row in rows:
            if row["date"] >= SINCE:
                found[row["id"]] = {"id": row["id"], "date": row["date"], "title_ko": row["title_ko"],
                                    "audience_ko": row["audience_ko"], "views": views.get(row["id"], 0)}
        dated = [r["date"] for r in rows if not r["pinned"]]
        if not dated:  # a maintenance page or a changed layout must never pass as the end of the board
            raise RuntimeError(f"No notices could be read on page {page} of the Korean board. Nothing was written.")
        if max(dated) < SINCE:
            break
    return sorted(found.values(), key=lambda n: (n["date"], n["id"]), reverse=True)


def english() -> list[dict]:
    found = {}
    for page in range(100):
        raw = _fetch(f"{ENGLISH}?page={page}")
        time.sleep(1)
        dates = []
        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", raw, flags=re.S):
            link = re.search(r'bbsidx=(\d+)"[^>]*>(.*?)</a>', row, flags=re.S)
            date = re.search(r"([A-Z][a-z]{2}) (\d{1,2}), (\d{4})", row)
            hit = re.search(r"Hit\s*(\d+)", row)
            if not (link and date):
                continue
            iso = f"{date.group(3)}-{MONTH[date.group(1)]:02d}-{int(date.group(2)):02d}"
            dates.append(iso)
            if iso >= SINCE:
                title = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", link.group(2)))).strip()
                found[int(link.group(1))] = {"id": int(link.group(1)), "date": iso, "title": title, "views": int(hit.group(1)) if hit else 0}
        if not dates:
            raise RuntimeError(f"No posts could be read on page {page} of the English board. Nothing was written.")
        if max(dates) < SINCE:
            break
    return sorted(found.values(), key=lambda n: (n["date"], n["id"]), reverse=True)


def by_year(posts: list[dict]) -> dict:
    out = {}
    for post in posts:
        year = out.setdefault(post["date"][:4], {"posts": 0, "views": 0})
        year["posts"] += 1
        year["views"] += post["views"]
    return dict(sorted(out.items()))


if __name__ == "__main__":
    ko, en = korean(), english()
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().isoformat()
    this_year = today[:4]
    result = {
        "counted_on": today, "since": SINCE, "korean_board": KOREAN, "english_board": ENGLISH,
        "korean_by_year": by_year(ko), "english_by_year": by_year(en),
        "most_read_korean": sorted((n for n in ko if n["date"][:4] == this_year), key=lambda n: -n["views"])[:10],
        "english_posts": en,  # every post of the period, so any later start date can be compared
    }
    target = ROOT / "data" / "ECE" / "evidence.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(ko)} Korean and {len(en)} English posts since {SINCE}; written to {target.relative_to(ROOT)}")
    print(json.dumps({"korean": result["korean_by_year"], "english": result["english_by_year"]}, indent=1))
