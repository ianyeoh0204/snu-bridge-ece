"""Step 5 of the pipeline: cards in, one static page out. No server, no framework."""
from __future__ import annotations

import datetime
import json
import re
from pathlib import Path

from .cards import GROUPS

ROOT = Path(__file__).resolve().parent.parent
SEOUL = datetime.timezone(datetime.timedelta(hours=9))  # the published date is the date in Seoul, wherever this runs
PROGRAM_LABELS = {"undergraduate": "Undergraduate", "masters": "Master's", "phd": "PhD", "integrated": "Integrated MS-PhD"}
HIDDEN = {"wrong", "not_on_page"}  # a card the second reader rejected is never published


AUDIENCE = {"학부": "Undergraduate", "대학원": "Graduate", "학부&대학원": "All students"}


def _notices(department: str, card_ids: set) -> list[dict]:
    """Notices with their English title and the cards their title is tied to."""
    data, folder = ROOT / "data" / department, ROOT / "sources" / department
    if not (data / "notices.json").exists():
        return []
    titles = json.loads((data / "notice_titles_en.json").read_text(encoding="utf-8")) if (data / "notice_titles_en.json").exists() else {}
    links = json.loads((folder / "notice_links.json").read_text(encoding="utf-8")) if (folder / "notice_links.json").exists() else []
    out = []
    for n in json.loads((data / "notices.json").read_text(encoding="utf-8")):
        tied = next((rule["cards"] for rule in links if re.search(rule["pattern"], n["title_ko"])), [])
        brief_file = data / "briefs" / f"{n['id']}.json"
        brief = json.loads(brief_file.read_text(encoding="utf-8")) if brief_file.exists() else None
        out.append({"id": n["id"], "date": n["date"], "url": n["url"], "title_ko": n["title_ko"], "brief": brief,
                    "title_en": titles.get(str(n["id"])) or (brief or {}).get("title_en", ""),  # a reviewed title wins
                    "audience": AUDIENCE.get(n["audience_ko"], n["audience_ko"]),
                    "edited": bool(n.get("title_history")), "cards": [c for c in tied if c in card_ids]})
    return out


def build() -> Path:
    departments = {}
    for config_file in sorted((ROOT / "sources").glob("*/config.json")):
        name = config_file.parent.name
        cards_file = ROOT / "data" / name / "cards.json"
        if not cards_file.exists():
            continue
        config = json.loads(config_file.read_text(encoding="utf-8"))
        cards = [c for c in json.loads(cards_file.read_text(encoding="utf-8")) if c.get("check") not in HIDDEN]
        notices = _notices(name, {c["id"] for c in cards})
        departments[name] = {
            "name": config["department"], "programs": config["programs"],
            "default_program": config.get("default_program", config["programs"][0]),
            "headline_cards": config.get("headline_cards", {}),
            "assistant": config.get("assistant"),  # where to read attachments and images this site did not translate  # the one fact shown on each program's homepage tile
            "sources": {f["file"]: {k: f[k] for k in ("name", "url", "series", "entry_year") if k in f} for f in config["files"]},
            "cards": cards, "notices": notices, "board": config.get("board", {}),
        }
    data = {"departments": departments, "groups": GROUPS, "program_labels": PROGRAM_LABELS,
            "built": datetime.datetime.now(SEOUL).date().isoformat()}
    site = ROOT / "site"
    site.mkdir(exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    template = (Path(__file__).parent / "site_template.html").read_text(encoding="utf-8")
    (site / "index.html").write_text(template.replace("__DATA__", payload), encoding="utf-8")
    (site / "cards.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return site / "index.html"
