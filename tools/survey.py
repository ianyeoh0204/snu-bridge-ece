# -*- coding: utf-8 -*-
"""Count Korean and English notices on the other engineering departments' public boards.

    .venv/bin/python tools/survey.py count        read the boards (list pages only) into out/survey/survey.json
    .venv/bin/python tools/survey.py check        second count, from each board's own row numbering
    .venv/bin/python tools/survey.py sample       open ten Korean-titled notices per department, measure their English
    .venv/bin/python tools/survey.py aggregate    write data/survey.json, the totals the About page shows

Rules kept: every host's robots.txt was read by hand first (Architecture disallows everything and is not read;
Materials Science disallows its paging links, so only its first page is read); one request per second; every page
fetched is kept in out/survey/cache so a count can be repeated without asking the site again. The full list of
posts stays in out/ (not published); only totals go into data/survey.json.
"""
import datetime
import hashlib
import html
import json
import pathlib
import random
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out" / "survey"
CACHE = OUT / "cache"
AGENT = "SNU-Bridge/0.1 (student project; one request per second)"
SINCE = "2024-01-01"      # how far back the boards are read
WINDOW = "2025-01-01"     # what is reported: two of the boards only begin in late 2024 or January 2025
UNTIL = "2026-10-31"      # the last day reported: a closed period (22 months), so no figure moves from day to day
TODAY = datetime.date(2026, 11, 12)  # the day of the count; a board that prints only a time means "today"
MONTH = {m: i + 1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
TAGS = re.compile(r"<[^>]+>")
HANGUL = re.compile(r"[가-힣]")


def in_english(title):
    """The title test used everywhere: Latin letters and no Korean."""
    return bool(re.search(r"[A-Za-z]{3}", title)) and not HANGUL.search(title)


def either(on_korean, on_english):
    """Notices with an English title on either board. One posted on both boards under the same title is one notice."""
    plain = lambda titles: {re.sub(r"\W+", "", t).lower() for t in titles}
    return len(on_korean) + len(on_english) - len(plain(on_korean) & plain(on_english))


def get(url):
    """A page, fetched once and kept on disk."""
    CACHE.mkdir(parents=True, exist_ok=True)
    file = CACHE / (hashlib.sha1(url.encode()).hexdigest()[:16] + ".html")
    if file.exists():
        return file.read_text(encoding="utf-8", errors="replace")
    safe = urllib.parse.quote(url, safe=":/?&=%#+,;@")
    with urllib.request.urlopen(urllib.request.Request(safe, headers={"User-Agent": AGENT}), timeout=40) as response:
        raw = response.read().decode("utf-8", "replace")
    time.sleep(1)
    file.write_text(raw, encoding="utf-8")
    return raw


def strip(page):
    return re.sub(r"<(script|style|svg)[^>]*>.*?</\1>", "", page, flags=re.S)


def iso(text):
    """The last date in a row, as YYYY-MM-DD. "" if the row shows none.
    Every board prints the posting date after the title, and a title can itself contain a date."""
    found = [(m.start(), f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}")
             for m in re.finditer(r"(20\d\d)[.\-/]\s?(\d{1,2})[.\-/]\s?(\d{1,2})(?!\d)", text)]
    found += [(m.start(), f"{m.group(3)}-{MONTH[m.group(1)]:02d}-{int(m.group(2)):02d}")
              for m in re.finditer(r"([A-Z][a-z]{2})\.? (\d{1,2}), (20\d\d)", text) if m.group(1) in MONTH]
    return max(found)[1] if found else ""


def row_number(row):
    """The running number a board prints in a row's first cell. None for a pinned row, which shows a label instead."""
    cell = re.search(r"<(?:td|span)[^>]*>\s*(?:<!--.*?-->)?\s*([^<]*?)\s*<", row, flags=re.S)
    return int(cell.group(1)) if cell and cell.group(1).strip().isdigit() else None


def rows_of(page, split, link):
    """Every list row that holds a post link: (id, row html, title)."""
    out = []
    for row in re.findall(split, strip(page), flags=re.S):
        m = re.search(link, row, flags=re.S)
        if m:
            title = re.sub(r"\s+", " ", html.unescape(TAGS.sub("", m.group(2)))).strip()
            out.append((m.group(1), row, title))
    return out


def walk(url, split, link, first=1, cap=260, today_as_time=False, empty_ok=False):
    """Read list pages until two pages in a row add no post inside the window. Pinned rows repeat and are kept once."""
    found, quiet, pages, per_page = {}, 0, 0, []
    for n in range(first, first + cap):
        rows = rows_of(get(url.format(n=n)), split, link)
        pages += 1
        per_page.append(len(rows))
        if not rows:
            if n == first and not empty_ok:
                raise RuntimeError(f"No rows could be read on the first page: {url}")
            break
        new = 0
        for pid, row, title in rows:
            date = iso(row)
            if not date and today_as_time and re.search(r">\s*\d{2}:\d{2}\s*<", row):
                date = TODAY.isoformat()
            if pid in found:
                continue
            if not date:
                raise RuntimeError(f"A row without a date on page {n} of {url}: {title[:60]}")
            if date >= SINCE:
                found[pid] = {"id": pid, "date": date, "title": title, "row_number": row_number(row)}
                new += 1
        quiet = 0 if new else quiet + 1
        if quiet == 2:
            break
    else:
        raise RuntimeError(f"Page cap reached without leaving the window: {url}")
    return {"posts": sorted(found.values(), key=lambda p: p["date"], reverse=True), "pages_read": pages,
            "rows_first_pages": per_page[:3]}


def walk_month_day(url, cap=260):
    """A board that prints only MM-DD. Unpinned rows run newest first, so the year falls by one each time the
    month jumps upward. A pinned row takes the year of the unpinned row with the nearest post number."""
    split, link = TR, GNU
    normal, pinned, year, last_month, seen = [], {}, TODAY.year, TODAY.month, set()
    pages = 0
    for n in range(1, cap):
        rows = rows_of(get(url.format(n=n)), split, link)
        pages += 1
        fresh = [r for r in rows if r[0] not in seen]
        if not fresh:
            break
        for pid, row, title in fresh:
            seen.add(pid)
            m = re.search(r">\s*(\d{2})-(\d{2})\s*<", row)
            if not m:
                if re.search(r">\s*\d{2}:\d{2}\s*<", row):
                    m = re.match(r"(\d\d)(\d\d)", TODAY.strftime("%m%d"))
                else:
                    raise RuntimeError(f"A row without a date on page {n} of {url}: {title[:60]}")
            month, day = int(m.group(1)), int(m.group(2))
            if "<strong" in row.split("</td>")[0]:  # the first cell says 공지 instead of a number
                pinned[pid] = (month, day, title)
                continue
            if month > last_month:
                year -= 1
            last_month = month
            normal.append({"id": pid, "date": f"{year}-{month:02d}-{day:02d}", "title": title, "row_number": row_number(row)})
        if normal and normal[-1]["date"] < "2023-10-01":
            break
    for pid, (month, day, title) in pinned.items():
        near = min(normal, key=lambda p: abs(int(p["id"]) - int(pid)))
        normal.append({"id": pid, "date": f"{near['date'][:4]}-{month:02d}-{day:02d}", "title": title, "pinned": True})
    posts = [p for p in normal if p["date"] >= SINCE]
    return {"posts": sorted(posts, key=lambda p: p["date"], reverse=True), "pages_read": pages}


def walk_dated_on_page(list_url, page_url):
    """A small board that prints only MM-DD: the full date is read from each notice page instead."""
    posts = []
    for pid, _, title in rows_of(get(list_url), TR, GNU):
        m = re.search(r"(\d{2})-(\d{2})-(\d{2})\s+\d{2}:\d{2}", TAGS.sub(" ", strip(get(page_url.format(id=pid)))))
        if not m:
            raise RuntimeError(f"No date on the notice page: {page_url.format(id=pid)}")
        posts.append({"id": pid, "date": f"20{m.group(1)}-{m.group(2)}-{m.group(3)}", "title": title})
    return {"posts": sorted(posts, key=lambda p: p["date"], reverse=True), "pages_read": 1}


TR, LI = r"<tr[^>]*>(.*?)</tr>", r"<li[^>]*>(.*?)</li>"
BBS = r'bbsidx=(\d+)[^"]*"[^>]*>(.*?)</a>'
GNU = r'wr_id=(\d+)[^"]*"[^>]*>(.*?)</a>'
KBOARD = r'uid=(\d+)"[^>]*>(.*?)</a>'
CBE = r'boardId=(\d+)[^"]*"[^>]*>(.*?)</a>'
CSE = r'/community/notice/(\d+)[^"]*"[^>]*>(.*?)</a>'

# The rule for every department: its notice boards are counted; boards it keeps apart for jobs, scholarships, news or
# seminars are not. Six of the other departments have a separate job board and three a separate scholarship board
# (seen in their menus on 12 November 2026); none of those is counted. So this site's own department is counted on its
# four notice boards, without its scholarship board (장학), its job board (취업ㆍ진로) and its seminar calendar (행사).
ECE_BOARDS = (("학사", "academics"), ("입시", "admissions"), ("대학생활", "campus-life"), ("기타", "etc"))
# Every tab of this department's Korean community menu, for the breakdown its own page shows (the developer browsed the
# site, saw English titles, and could not tell which tab a "0" referred to). The last two are not in the comparison.
ECE_TABS = (("학사", "Academic", "academics"), ("입시", "Admissions", "admissions"), ("대학생활", "Campus life", "campus-life"),
            ("기타", "Other", "etc"), ("장학", "Scholarships", "schoarships"), ("취업ㆍ진로", "Jobs and careers", "job-openings"))


# Where one notice of a given board opens, so every English-titled notice can be listed with its link and checked by anyone.
OPENS = {
    ("Energy Resources Engineering", "대학원 공지"): "https://ere.snu.ac.kr/bbs/board.php?bo_table=sub5_2&wr_id={id}",
    ("Chemical and Biological Engineering", "학부 공지"): "https://cbe.snu.ac.kr/cbe/bbs/BMSR00059/view.do?boardId={id}&menuNo=300053",
    ("Chemical and Biological Engineering", "대학원 공지"): "https://cbe.snu.ac.kr/cbe/bbs/BMSR00060/view.do?boardId={id}&menuNo=300054",
    **{("Electrical and Computer Engineering", name): f"https://ece.snu.ac.kr/community/{b}?md=v&bbsidx={{id}}"
       for name, b in (("학사", "academics"), ("입시", "admissions"), ("대학생활", "campus-life"), ("기타", "etc"))},
}


def listed(dept, boards):
    """Every notice on the department's Korean boards with an English title: date, title and link. Few enough to show them all.
    A speaker's name after a title such as "Prof." is replaced, as everywhere on the site."""
    sys.path.insert(0, str(ROOT))
    from bridge.notices import NAMED
    out = []
    for board in boards:
        opens = OPENS.get((dept, board["board"])) or DETAIL[dept][0]
        for post in board["posts"]:
            if WINDOW <= post["date"] <= UNTIL and in_english(post["title"]):
                out.append({"date": post["date"], "title": NAMED.sub(lambda m: m.group(1) + " [name]", post["title"]), "url": opens.format(id=post["id"])})
    return sorted({item["url"]: item for item in out}.values(), key=lambda item: item["date"], reverse=True)


def tabs():
    counted, out = {b for _, b in ECE_BOARDS}, []
    for name, name_en, b in ECE_TABS:
        posts = [p for p in walk(f"https://ece.snu.ac.kr/community/{b}?page={{n}}", TR, BBS, first=0)["posts"] if WINDOW <= p["date"] <= UNTIL]
        out.append({"name": name, "name_en": name_en, "url": f"https://ece.snu.ac.kr/community/{b}", "korean": len(posts),
                    "english_titled": sum(in_english(p["title"]) for p in posts), "counted": b in counted})
    return out
BOARDS = {
    "Electrical and Computer Engineering": {
        "ko": [(name, (lambda b=b: walk(f"https://ece.snu.ac.kr/community/{b}?page={{n}}", TR, BBS, first=0))) for name, b in ECE_BOARDS],
        "en": [("Notice", lambda: walk("https://ece.snu.ac.kr/en/community/notice?page={n}", TR, BBS, first=0))],
    },
    "Aerospace Engineering": {
        "ko": [("공지사항", lambda: walk("https://aerospace.snu.ac.kr/board/notice?page={n}", TR, BBS))],
        "en": [("International Students bulletin board", lambda: walk("https://aerospace.snu.ac.kr/en/board/notice?page={n}", TR, BBS))],
    },
    "Nuclear Engineering": {
        "ko": [("공지사항", lambda: walk("https://nucleng.snu.ac.kr/community/notice?page={n}", TR, BBS, first=0))],
        "en": [("Notice", lambda: walk("https://nucleng.snu.ac.kr/en/community/notice?page={n}", TR, BBS, first=0))],
    },
    "Naval Architecture and Ocean Engineering": {
        "ko": [("공지사항", lambda: walk("https://naoe.snu.ac.kr/news/notice?page={n}", TR, BBS, first=0))],
        "en": [],
    },
    "Computer Science and Engineering": {
        "ko": [("공지사항", lambda: walk("https://cse.snu.ac.kr/ko/community/notice?pageNum={n}", LI, CSE))],
        "en": [("Notice", lambda: walk("https://cse.snu.ac.kr/en/community/notice?pageNum={n}", LI, CSE))],
    },
    "Civil, Urban and Environmental Engineering": {
        "ko": [("공지사항", lambda: walk("https://cuee.snu.ac.kr/bbs/board.php?bo_table=sub5_1&lang=kor&page={n}", TR, GNU))],
        "en": [("Notice", lambda: walk("https://cuee.snu.ac.kr/bbs/board.php?bo_table=sub5_1&lang=eng&page={n}", TR, GNU))],
    },
    "Energy Resources Engineering": {
        "ko": [("공지사항", lambda: walk_month_day("https://ere.snu.ac.kr/bbs/board.php?bo_table=sub5_1&page={n}")),
               ("대학원 공지", lambda: walk_month_day("https://ere.snu.ac.kr/bbs/board.php?bo_table=sub5_2&page={n}"))],
        "en": [(name, (lambda b=b: walk_dated_on_page(f"https://ere.snu.ac.kr/bbs/board.php?bo_table={b}&page=1",
                                                        f"https://ere.snu.ac.kr/bbs/board.php?bo_table={b}&wr_id={{id}}")))
               for name, b in (("Undergrad Notice", "eng5_1"), ("Grad Notice", "eng5_2"))],
    },
    "Industrial Engineering": {
        "ko": [("공지사항", lambda: walk("https://ie.snu.ac.kr/notice/?pageid={n}&mod=list", LI, KBOARD, today_as_time=True))],
        "en": [("Notice", lambda: walk("https://ie.snu.ac.kr/en/department_news/?pageid={n}&mod=list", LI, KBOARD, today_as_time=True))],
    },
    "Mechanical Engineering": {
        "ko": [("공지사항", lambda: walk("https://me.snu.ac.kr/공통-공지사항/?pageid={n}&mod=list", LI, KBOARD, today_as_time=True))],
        "en": [("Announcement", lambda: walk("https://me.snu.ac.kr/en/announcements/?pageid={n}&mod=list", LI, KBOARD, today_as_time=True))],
    },
    "Chemical and Biological Engineering": {
        "ko": [(name, (lambda b=b, m=m: walk(f"https://cbe.snu.ac.kr/cbe/bbs/{b}/list.do?menuNo={m}&pageIndex={{n}}", TR, CBE)))
               for name, b, m in (("공지사항", "BMSR00058", "300052"), ("학부 공지", "BMSR00059", "300053"), ("대학원 공지", "BMSR00060", "300054"))],
        "en": [(name, (lambda b=b, m=m: walk(f"https://cbe.snu.ac.kr/cbeEng/bbs/{b}/list.do?menuNo={m}&pageIndex={{n}}", TR, CBE, empty_ok=True)))
               for name, b, m in (("Notices", "BMSR00058", "300052"), ("Undergraduate Notices", "BMSR00059", "300053"), ("Graduate Notices", "BMSR00060", "300054"))],
    },
}


# What each department offers in English, seen by hand on 12 November 2026.
#   separate    its own English board with its own posts
#   same_posts  the English menu lists the Korean board's posts (the same post numbers, Korean text)
#   none        no English site; the Korean site carries a browser translation button
THIS_SITE = "Electrical and Computer Engineering"
SIDE = {
    "Electrical and Computer Engineering": ("전기·정보공학부", "https://ece.snu.ac.kr", "separate"),
    "Aerospace Engineering": ("항공우주공학과", "https://aerospace.snu.ac.kr", "separate"),
    "Nuclear Engineering": ("원자핵공학과", "https://nucleng.snu.ac.kr", "separate"),
    "Naval Architecture and Ocean Engineering": ("조선해양공학과", "https://naoe.snu.ac.kr", "none"),
    "Computer Science and Engineering": ("컴퓨터공학부", "https://cse.snu.ac.kr", "same_posts"),
    "Civil, Urban and Environmental Engineering": ("건설환경도시공학부", "https://cuee.snu.ac.kr", "same_posts"),
    "Energy Resources Engineering": ("에너지자원공학과", "https://ere.snu.ac.kr", "separate"),
    "Industrial Engineering": ("산업공학과", "https://ie.snu.ac.kr", "separate"),
    "Mechanical Engineering": ("기계공학부", "https://me.snu.ac.kr", "separate"),
    "Chemical and Biological Engineering": ("화학생물공학부", "https://cbe.snu.ac.kr", "separate"),
}
NOT_COUNTED = [
    {"name": "Materials Science and Engineering", "name_ko": "재료공학부", "site": "https://mse.snu.ac.kr", "reason": "first_page_only"},
    {"name": "Architecture and Architectural Engineering", "name_ko": "건축학과", "site": "https://architecture.snu.ac.kr", "reason": "not_permitted"},
]
# Where one notice page lives, for the sample. A second address is the same notice under the English menu.
DETAIL = {
    "Aerospace Engineering": ["https://aerospace.snu.ac.kr/board/notice?bm=v&bbsidx={id}"],
    "Nuclear Engineering": ["https://nucleng.snu.ac.kr/community/notice?md=v&bbsidx={id}"],
    "Naval Architecture and Ocean Engineering": ["https://naoe.snu.ac.kr/news/notice?md=v&bbsidx={id}"],
    "Computer Science and Engineering": ["https://cse.snu.ac.kr/ko/community/notice/{id}", "https://cse.snu.ac.kr/en/community/notice/{id}"],
    "Civil, Urban and Environmental Engineering": ["https://cuee.snu.ac.kr/bbs/board.php?bo_table=sub5_1&wr_id={id}",
                                                   "https://cuee.snu.ac.kr/bbs/board.php?bo_table=sub5_1&wr_id={id}&lang=eng"],
    "Energy Resources Engineering": ["https://ere.snu.ac.kr/bbs/board.php?bo_table=sub5_1&wr_id={id}"],
    "Industrial Engineering": ["https://ie.snu.ac.kr/notice/?mod=document&uid={id}"],
    "Mechanical Engineering": ["https://me.snu.ac.kr/공통-공지사항/?mod=document&uid={id}"],
    "Chemical and Biological Engineering": ["https://cbe.snu.ac.kr/cbe/bbs/BMSR00058/view.do?boardId={id}&menuNo=300052"],
}
SEED = 20261112
# Departments whose row-number check (`check`) does not match inside the reported period; their totals are shown as "about".
# None for 1 January 2025 to 31 October 2026 (Chemical and Biological Engineering differed only in November 2026).
APPROXIMATE = set()


def count(only):
    out_file = OUT / "survey.json"
    out = json.loads(out_file.read_text(encoding="utf-8")) if out_file.exists() else {}
    for dept, sides in BOARDS.items():
        if only and not any(a.lower() in dept.lower() for a in only):
            continue
        out[dept] = {}
        for side in ("ko", "en"):
            out[dept][side] = []
            for name, run in sides[side]:
                try:
                    result = run()
                except Exception as error:  # one unreadable board must not hide the others, and must not pass as zero
                    result = {"error": str(error)}
                result["board"] = name
                out[dept][side].append(result)
                print(dept, side, name, len(result["posts"]) if "posts" in result else result["error"], flush=True)
        out_file.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


def english_in(page):
    """How much running English a page holds: stretches of eight or more English words."""
    text = html.unescape(TAGS.sub(" ", strip(page)))
    runs = re.findall(r"(?:\b[A-Za-z][a-z']+\b[ ,;:\-]+){7,}", text)
    return {"hangul": len(HANGUL.findall(text)), "runs": len(runs), "words": sum(len(r.split()) for r in runs)}


def sample():
    """Ten Korean-titled notices per department, chosen by a fixed seed. Does the page hold English the title hides?"""
    data, out = json.loads((OUT / "survey.json").read_text(encoding="utf-8")), {}
    for dept, urls in DETAIL.items():
        posts = [p for p in data[dept]["ko"][0]["posts"] if p["date"] >= WINDOW and HANGUL.search(p["title"])]
        rows = []
        for p in random.Random(SEED).sample(sorted(posts, key=lambda p: p["id"]), 10):
            row = {"id": p["id"], "date": p["date"], "page": english_in(get(urls[0].format(id=p["id"])))}
            if len(urls) > 1:
                row["english_menu"] = english_in(get(urls[1].format(id=p["id"])))
            rows.append(row)
        chrome = min(r["page"]["runs"] for r in rows)  # English the site prints on every page (menus, footer)
        for r in rows:
            r["english_passages"] = r["page"]["runs"] - chrome
        out[dept] = rows
        print(dept, "notices with an English passage:", sum(r["english_passages"] > 0 for r in rows), "of", len(rows),
              "| most English words in one:", max(r["page"]["words"] for r in rows), flush=True)
    (OUT / "sample.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


def last_post(dept):
    """The newest date on a department's English board, from the stored list or, if that is empty, its first page."""
    data = json.loads((OUT / "survey.json").read_text(encoding="utf-8"))
    dates = [p["date"] for b in data[dept]["en"] for p in b["posts"]]
    if not dates and dept == "Aerospace Engineering":
        dates = [iso(row) for _, row, _ in rows_of(get("https://aerospace.snu.ac.kr/en/board/notice?page=1"), TR, BBS)]
    return max(dates) if dates else None


def aggregate():
    data = json.loads((OUT / "survey.json").read_text(encoding="utf-8"))
    sampled = json.loads((OUT / "sample.json").read_text(encoding="utf-8"))
    departments = []
    for dept, (name_ko, site, side) in sorted(SIDE.items(), key=lambda item: item[0] == THIS_SITE):  # this site's department last
        boards = data[dept]
        for board in boards["ko"] + boards["en"]:
            if "error" in board:
                raise SystemExit(f"{dept} / {board['board']} could not be read: {board['error']}")
        once = lambda posts: list({p["id"]: p for p in posts if WINDOW <= p["date"] <= UNTIL}.values())  # a notice shown on two boards is one notice
        korean = once(p for b in boards["ko"] for p in b["posts"])
        english = once(p for b in boards["en"] for p in b["posts"]) if side == "separate" else []
        on_korean, on_english = [p["title"] for p in korean if in_english(p["title"])], [p["title"] for p in english if in_english(p["title"])]
        rows = [r for r in sampled.get(dept, []) if r["date"] <= UNTIL]
        departments.append({
            "name": dept, "name_ko": name_ko, "site": site, "korean_boards": [b["board"] for b in boards["ko"]], "this_site": dept == THIS_SITE,
            "korean": len(korean), "approximate": dept in APPROXIMATE, "english_side": side,
            "english_titled": len(on_korean),  # of the Korean board's notices, those with a title in English
            "english_posts": len(english) if side == "separate" else None,  # every post on its own English board
            "english_posts_titled": len(on_english) if side == "separate" else None,  # of those, titled in English
            "english_last_post": last_post(dept) if side == "separate" else None,
            "in_english": either(on_korean, on_english),  # a title in English on either board, each notice once
            # the board this site translates, on its own: the first Korean board listed for this site's department
            "translated_board": ({"name": boards["ko"][0]["board"], "korean": len(once(boards["ko"][0]["posts"])),
                                  "english_titled": sum(in_english(p["title"]) for p in once(boards["ko"][0]["posts"]))} if dept == THIS_SITE else None),
            "tabs": tabs() if dept == THIS_SITE else None,
            "english_titles": listed(dept, boards["ko"]),
            "sample": {"opened": len(rows), "with_english_passage": sum(r["english_passages"] > 0 for r in rows),
                       "english_menu_is_korean": all(r["english_menu"]["hangul"] > 100 for r in rows) if "english_menu" in rows[0] else None} if rows else None,
        })
    add = lambda key: sum(d[key] or 0 for d in departments)
    out = {"counted_on": TODAY.isoformat(), "since": WINDOW, "until": UNTIL,
           "departments": departments, "not_counted": NOT_COUNTED,
           "totals": {"korean": add("korean"), "in_english": add("in_english"), "english_titled": add("english_titled"),
                      "english_boards": sum(d["english_side"] == "separate" for d in departments),
                      "english_posts": add("english_posts"), "english_posts_titled": add("english_posts_titled"),
                      "sample_departments": sum(bool(d["sample"]) for d in departments),
                      "sample_opened": sum(d["sample"]["opened"] for d in departments if d["sample"]),
                      "sample_with_english_passage": sum(d["sample"]["with_english_passage"] for d in departments if d["sample"])}}
    (ROOT / "data" / "survey.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    for d in departments:
        print(f"{d['name'][:30]:30} Korean {d['korean']:5}  in English {d['in_english']:3}  (Korean board {d['english_titled']}, English board "
              f"{d['english_posts_titled']} of {d['english_posts']} posts, last post {d['english_last_post']}; {d['english_side']})")
    print(out["totals"])


def check():
    """A second count that shares nothing with the first: most boards number their unpinned rows 1..N, so the
    number on the newest row minus the number on the oldest row in the period, plus one, must equal the rows counted."""
    data = json.loads((OUT / "survey.json").read_text(encoding="utf-8"))
    for dept, sides in BOARDS.items():
        for name, run in sides["ko"]:
            board = next(b for b in data[dept]["ko"] if b["board"] == name)
            posts = [p for p in board["posts"] if WINDOW <= p["date"] <= UNTIL]
            window = {p["id"] for p in posts}
            numbers = {p["id"]: p["row_number"] for p in posts if p.get("row_number")}
            if not numbers:
                print(f"{dept} / {name}: {len(window)} counted; this board prints no row numbers")
                continue
            span = max(numbers.values()) - min(numbers.values()) + 1
            print(f"{dept} / {name}: {len(window)} counted = {len(numbers)} numbered + {len(window) - len(numbers)} pinned; "
                  f"row numbers span {span} -> {'match' if span == len(numbers) else 'differs by ' + str(span - len(numbers))}")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "count":
        count(sys.argv[2:])
    elif command == "check":
        check()
    elif command == "sample":
        sample()
    elif command == "aggregate":
        aggregate()
    else:
        sys.exit(__doc__)
