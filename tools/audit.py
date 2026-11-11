# -*- coding: utf-8 -*-
"""Audit of requirement cards by a second reader that did not write them.

    .venv/bin/python tools/audit.py prepare     # writes out/audit/: one image and one question file per page
    (a different AI model reads each page and answers; see README "Audit")
    .venv/bin/python tools/audit.py collect     # reads the answers into data/ECE/audit.json

Selection rule, fixed before any result was seen: every card whose source is one of PAGES of the graduate handbook.
Two cards with a deliberately wrong number are mixed in, to learn whether the reader really reads the page.
"""
import copy
import json
import re
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out" / "audit"
PAGES = [8, 9, 10, 12, 20]
HANDBOOK = "학사안내서"
DECOYS = {  # id shown to the reader -> (card it copies, text to change, changed text)
    "check-a": ("credits-total", "24", "30"),
    "check-b": ("thesis-deadline", "4 years", "5 years"),
}
SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["transcription", "cards", "missing"],
    "properties": {
        "transcription": {"type": "string", "description": "The Korean text of the page, copied exactly, line by line"},
        "cards": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["id", "quote_on_page", "key", "lines", "why", "caution"],
            "properties": {
                "id": {"type": "string"},
                "quote_on_page": {"type": "boolean"},
                "key": {"$ref": "#/$defs/judgement"},
                "lines": {"type": "array", "items": {"$ref": "#/$defs/judgement"}},
                "why": {"$ref": "#/$defs/judgement"},
                "caution": {"$ref": "#/$defs/judgement"},
            }}},
        "missing": {"type": "array", "items": {"type": "string"}},
    },
    "$defs": {"judgement": {
        "type": "object", "additionalProperties": False, "required": ["text", "verdict", "korean", "note"],
        "properties": {
            "text": {"type": "string", "description": "The English statement being judged, copied from the card"},
            "verdict": {"type": "string", "enum": ["supported", "contradicted", "not_stated", "empty"]},
            "korean": {"type": "string", "description": "The Korean line on the page that decides it, or empty"},
            "note": {"type": "string", "description": "One sentence, only when not supported"},
        }}},
}
PROMPT = """You are an independent second reader. Do not edit any file and do not use the network.

Attached is one page image from a Korean university department's graduate handbook. The file {questions} in the \
current folder holds requirement cards that someone else wrote in English from this page.

Work in this order.
1. Transcribe the Korean text of the page exactly, line by line, including tables and numbers.
2. For each card, using only this page:
   - quote_on_page: is the card's `source_quote_ko` on the page, character for character apart from spacing?
   - key: is the short key fact right?
   - lines: judge every entry of `rule` separately.
   - why and caution: judge the `why` and `trap` text. If a field is empty, use verdict "empty".
   Verdicts: "supported" (the page says this, numbers included), "contradicted" (the page says something different), \
"not_stated" (the page does not say this; it may be an inference or come from another page).
   Give the deciding Korean line. Be strict about every number, unit, limit and condition.
3. missing: any rule on this page that a student must act on and that no card covers.

Judge against the page only. Do not assume a card is right because it looks plausible."""


def cards() -> list[dict]:
    return json.loads((ROOT / "data/ECE/cards.json").read_text(encoding="utf-8"))


def prepare() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    config = json.loads((ROOT / "sources/ECE/config.json").read_text(encoding="utf-8"))
    handbook = next(f["file"] for f in config["files"] if HANDBOOK in f["file"])
    chosen = [c for c in cards() if c["source_file"] == handbook and c["source_page"] in PAGES]
    by_id = {c["id"]: c for c in chosen}
    for fake, (real, old, new) in DECOYS.items():
        text = json.dumps(by_id[real], ensure_ascii=False)
        assert old in text, (real, old)
        decoy = json.loads(text.replace(old, new))
        decoy["id"] = fake
        chosen.append(decoy)
    (OUT / "schema.json").write_text(json.dumps(SCHEMA, ensure_ascii=False, indent=1), encoding="utf-8")
    with fitz.open(ROOT / "sources/ECE" / handbook) as doc:
        for page in PAGES:
            doc[page - 1].get_pixmap(dpi=170).save(OUT / f"page-{page}.png")
            asked = [{k: c[k] for k in ("id", "title", "key", "rule", "why", "trap", "when", "source_quote_ko")} for c in chosen if c["source_page"] == page]
            (OUT / f"page-{page}.json").write_text(json.dumps(asked, ensure_ascii=False, indent=1), encoding="utf-8")
            (OUT / f"page-{page}.prompt.txt").write_text(PROMPT.format(questions=f"page-{page}.json"), encoding="utf-8")
            print(f"page {page}: {len(asked)} cards")
    print(f"{len(chosen) - len(DECOYS)} cards and {len(DECOYS)} decoys in {OUT.relative_to(ROOT)}")


def prepare_pass(number: int = 2) -> None:
    """After corrections: the changed cards again. Pass 2 also adds page 11, which an audited card turned out to continue from.
    `out/audit/cards.before[-passN].json` is the card file as it was before that pass's corrections."""
    snapshot, extra_page, decoy_of = {2: ("cards.before.json", 11, ("registration-count-phd", "12", "14", "check-c")),
                                      3: ("cards.before-pass3.json", 0, ("credits-total-phd", "36", "42", "check-d")),
                                      4: ("cards.before-pass4.json", 0, ("credits-ece-phd", "12", "15", "check-e"))}[number]
    before = {c["id"]: c for c in json.loads((OUT / snapshot).read_text(encoding="utf-8"))}
    config = json.loads((ROOT / "sources/ECE/config.json").read_text(encoding="utf-8"))
    handbook = next(f["file"] for f in config["files"] if HANDBOOK in f["file"])
    fields = ("id", "title", "key", "rule", "why", "trap", "when", "applies_from", "source_quote_ko")
    chosen = [c for c in cards() if c["source_file"] == handbook and c["source_page"] in PAGES + [11] and (
        any(before[c["id"]].get(k) != c.get(k) for k in fields) or c["source_page"] == extra_page)]
    decoy = json.loads(json.dumps(next(c for c in cards() if c["id"] == decoy_of[0]), ensure_ascii=False).replace(decoy_of[1], decoy_of[2]))
    decoy["id"] = decoy_of[3]
    chosen.append(decoy)
    pages = sorted({p for c in chosen for p in (c["source_page"], c.get("source_page_also") or c["source_page"])})
    with fitz.open(ROOT / "sources/ECE" / handbook) as doc:
        for page in pages:
            doc[page - 1].get_pixmap(dpi=170).save(OUT / f"page-{page}.png")
            asked = []
            for c in chosen:
                if page in (c["source_page"], c.get("source_page_also")):
                    item = {k: c[k] for k in fields}
                    if c.get("source_page_also"):
                        item["note_for_reader"] = "This rule runs over a page break. Judge only what this page shows and use not_stated for the rest."
                    asked.append(item)
            (OUT / f"pass{number}-page-{page}.json").write_text(json.dumps(asked, ensure_ascii=False, indent=1), encoding="utf-8")
            (OUT / f"pass{number}-page-{page}.prompt.txt").write_text(PROMPT.format(questions=f"pass{number}-page-{page}.json"), encoding="utf-8")
            print(f"pass {number}, page {page}: {[c['id'] for c in asked]}")


REST_DECOYS = {"check-f": ("ug-degree-total", "130", "140"), "check-g": ("credits-ece-integrated", "21", "24"),
               "check-h": ("leave-of-absence", "4 semesters", "6 semesters")}
TEXT_PROMPT = PROMPT.replace("Attached is one page image from a Korean university department's graduate handbook.",
                             "The file {source} in the current folder is the text of an official Korean department document.").replace(
    "1. Transcribe the Korean text of the page exactly, line by line, including tables and numbers.",
    "1. Copy into `transcription` the Korean lines of that file that the cards below depend on.")


def prepare_rest(prefix: str = "rest", snapshot: str = "") -> None:
    """Every card not audited yet, grouped by the page it cites. A PDF page becomes an image; a spreadsheet is given as text.
    With a snapshot (the card file before a round of corrections), only the cards changed since then are asked again."""
    sys.path.insert(0, str(ROOT))
    from bridge import sources
    done = set(json.loads((ROOT / "data/ECE/audit.json").read_text(encoding="utf-8"))["cards"])
    fields = ("id", "title", "key", "rule", "why", "trap", "when", "applies_from", "source_quote_ko")
    todo = [c for c in cards() if c["id"] not in done]
    decoys = REST_DECOYS
    if snapshot:
        before = {c["id"]: c for c in json.loads((OUT / snapshot).read_text(encoding="utf-8"))}
        todo = [c for c in cards() if any(before[c["id"]].get(k) != c.get(k) for k in fields + ("source_page_also",))]
        decoys = {"check-i": ("ug-category-change", "one week", "two weeks")}
    by_id = {c["id"]: c for c in todo}
    for fake, (real, old, new) in decoys.items():
        text = json.dumps(by_id[real], ensure_ascii=False)
        assert old in text, (real, old)
        decoy = json.loads(text.replace(old, new))
        decoy["id"] = fake
        todo.append(decoy)
    groups = {}
    for c in todo:
        groups.setdefault((c["source_file"], c["source_page"]), []).append(c)
        if c.get("source_page_also"):
            groups.setdefault((c["source_file"], c["source_page_also"]), []).append(c)
    index = []
    for number, ((file, page), group) in enumerate(sorted(groups.items()), 1):
        path = ROOT / "sources/ECE" / file
        asked = [{k: c.get(k, "") for k in fields} for c in group]
        (OUT / f"{prefix}-page-{number}.json").write_text(json.dumps(asked, ensure_ascii=False, indent=1), encoding="utf-8")
        if path.suffix.lower() == ".pdf":
            with fitz.open(path) as doc:
                doc[page - 1].get_pixmap(dpi=170).save(OUT / f"{prefix}-{number}.png")
            (OUT / f"{prefix}-page-{number}.prompt.txt").write_text(PROMPT.format(questions=f"{prefix}-page-{number}.json").replace(
                "graduate handbook", "official document"), encoding="utf-8")
            kind = "image"
        else:
            (OUT / f"{prefix}-{number}.txt").write_text(sources._xlsx_text(path), encoding="utf-8")
            (OUT / f"{prefix}-page-{number}.prompt.txt").write_text(TEXT_PROMPT.format(questions=f"{prefix}-page-{number}.json", source=f"{prefix}-{number}.txt"), encoding="utf-8")
            kind = "text"
        index.append({"number": number, "file": file, "page": page, "kind": kind, "cards": [c["id"] for c in group]})
        print(f"{number:2d} {kind:5s} p{page:<3} {len(group):2d} cards  {file[:34]}")
    (OUT / f"{prefix}-index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(todo) - len(decoys)} cards and {len(decoys)} decoys in {len(index)} packets")


def collect() -> None:
    """Read every answer in out/audit into data/ECE/audit.json. For each card the latest pass it appeared in counts;
    a rule that runs over a page break is supported if either page supports it."""
    import collections
    import datetime
    norm = lambda t: re.sub(r"[－–‐―-]", "-", re.sub(r"\s+", "", t))
    latest, first, decoys, uncovered, quotes = {}, {}, {}, 0, collections.defaultdict(bool)
    for number, prefix in ((1, ""), (2, "pass2-"), (3, "pass3-"), (4, "pass4-"), (5, "rest-"), (6, "rest2-")):
        seen = collections.defaultdict(list)
        for answer_file in sorted(OUT.glob(f"{prefix}answer-*.json")):
            page = answer_file.stem.split("-")[-1]
            asked = {c["id"]: c for c in json.loads((OUT / f"{prefix}page-{page}.json").read_text(encoding="utf-8"))}
            answer = json.loads(answer_file.read_text(encoding="utf-8"))
            text = norm(answer["transcription"])
            if number == 1:
                uncovered += len(answer["missing"])
            for card in answer["cards"]:
                seen[card["id"]].append(card)
                if card["id"] in asked:
                    quotes[card["id"]] |= norm(asked[card["id"]]["source_quote_ko"]) in text
        for card_id, answers in seen.items():
            def best(items):
                verdicts = [i["verdict"] for i in items]
                return ("contradicted" if "contradicted" in verdicts else "supported" if "supported" in verdicts
                        else "empty" if set(verdicts) == {"empty"} else "not_stated")
            lines = collections.defaultdict(list)
            for one in answers:
                for line in one["lines"]:
                    lines[line["text"]].append(line)
            result = {"pass": number, "key": best([a["key"] for a in answers]), "lines": {t: best(v) for t, v in lines.items()},
                      "why": best([a["why"] for a in answers]), "caution": best([a["caution"] for a in answers])}
            result["agrees"] = result["key"] == "supported" and all(v == "supported" for v in result["lines"].values())
            if card_id.startswith("check-"):
                decoys[card_id] = "caught" if result["key"] == "contradicted" or "contradicted" in result["lines"].values() else "MISSED"
                continue
            first.setdefault(card_id, result)
            latest[card_id] = result
    settled = json.loads((ROOT / "sources/ECE/audit_notes.json").read_text(encoding="utf-8"))["settled"]
    for card_id in latest:
        latest[card_id]["quote_found"] = quotes[card_id]
        latest[card_id]["status"] = "reader_agrees" if latest[card_id]["agrees"] else "settled_by_author" if card_id in settled else "open"
        latest[card_id]["reason"] = "" if latest[card_id]["agrees"] else settled.get(card_id, "")
    notices, notices_after = {}, {}
    for answer_file in sorted(OUT.glob("notice-answer-*.json")) + sorted(OUT.glob("notice2-answer-*.json")):
        number = answer_file.stem.split("-")[-1]
        answer = json.loads(answer_file.read_text(encoding="utf-8"))
        kinds = collections.Counter(f["kind"] for f in answer["findings"] if f["severity"] == "could_mislead")
        second = answer_file.name.startswith("notice2-")
        if number == "check":
            decoys["notice2" if second else "notice"] = "caught" if any(f["kind"] == "wrong_date" for f in answer["findings"]) else "MISSED"
            continue
        (notices_after if second else notices)[number] = {"overall": answer["overall"], "could_mislead": dict(kinds),
                           "minor": sum(f["severity"] == "minor" for f in answer["findings"]),
                           "wrong_dates": sum(f["kind"] == "wrong_date" for f in answer["findings"])}
    result = {
        "audited_on": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date().isoformat(),
        "reader": "A second AI model from a different maker (OpenAI, through the Codex command-line tool), which did not write the cards",
        "selection": f"Every card whose source is page {', '.join(map(str, PAGES))} of the graduate handbook, fixed before any result was seen; "
                     "page 11 was added because an audited rule continues from it.",
        "decoys": decoys, "rules_on_these_pages_without_a_card": uncovered,
        "cards_first_reading": {"agree": sum(r["agrees"] for r in first.values()), "of": len(first),
                                "contradicted": sum("contradicted" in [r["key"], *r["lines"].values()] for r in first.values())},
        "cards": latest, "notices": notices, "notices_after": notices_after,
    }
    (ROOT / "data/ECE/audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    status = collections.Counter(r["status"] for r in latest.values())
    print(f"cards: {len(latest)} audited; first reading {result['cards_first_reading']}; now {dict(status)}; decoys {decoys}")
    for card_id, r in latest.items():
        if r["status"] == "open":
            print("  still open:", card_id, r["key"], [t[:60] for t, v in r["lines"].items() if v != "supported"])
    print("why/caution not stated on the page:", sum(r["why"] == "not_stated" for r in latest.values()), "/", sum(r["caution"] == "not_stated" for r in latest.values()))
    print("notices:", {n: (v["overall"], sum(v["could_mislead"].values())) for n, v in notices.items()})


NOTICES = [57932, 58072, 57938, 58022, 58076, 58067, 57941, 57942, 57986, 58191]  # notices where a missed date has a cost
NOTICE_DECOY = (58022, "17 September", "24 September")  # one brief is also sent with a wrong date, under another name
NOTICE_SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["dates_in_notice", "findings", "overall"],
    "properties": {
        "dates_in_notice": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["korean", "meaning"],
            "properties": {"korean": {"type": "string"}, "meaning": {"type": "string"}}}},
        "findings": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["kind", "severity", "korean", "english", "note"],
            "properties": {
                "kind": {"type": "string", "enum": ["missing_date", "wrong_date", "wrong_meaning_of_date", "wrong_audience", "missing_step",
                                                    "wrong_step", "dropped_condition", "added_content", "other"]},
                "severity": {"type": "string", "enum": ["could_mislead", "minor"]},
                "korean": {"type": "string"}, "english": {"type": "string"}, "note": {"type": "string"}}}},
        "overall": {"type": "string", "enum": ["accurate", "minor_issues", "could_mislead"]},
    },
}
NOTICE_PROMPT = """You are an independent second reader. Do not edit any file and do not use the network.

In the current folder, {korean} is the text of a Korean university department notice, and {english} is an English \
summary that an AI wrote from it for international students who cannot read Korean (title, summary, who must act, dates, conditions, steps; some of these may be absent).

Work in this order.
1. From the Korean only, before opening the English file: list every date, time, period and deadline in the notice, \
copying the Korean exactly, and say what each one is for.
2. Then compare with the English file and report findings:
   - a date in the Korean that the English leaves out, when a student could need it;
   - a date that is wrong, or whose meaning is wrong (a deadline shown as an event, a period for one group shown as for all);
   - who must act: any group the English adds, drops or changes;
   - a required action that is missing or wrong, including where and how to submit;
   - a condition, exception or consequence in the Korean that the English drops;
   - anything the English states that the Korean does not.
   Mark each finding "could_mislead" (a student could act wrongly or miss something) or "minor".
3. overall: "accurate", "minor_issues" or "could_mislead".

The notice text had email addresses and phone numbers removed on purpose; do not report those. Images and attachments \
were not available to the writer, and the English may say so; do not report that either. Be strict about every date."""


def prepare_notices(prefix: str = "notice") -> None:
    """prefix "notice" is the first reading; "notice2" is the reading after the translation instructions were tightened."""
    import hashlib
    import time
    sys.path.insert(0, str(ROOT))
    from bridge import briefs
    OUT.mkdir(parents=True, exist_ok=True)
    notices = {n["id"]: n for n in json.loads((ROOT / "data/ECE/notices.json").read_text(encoding="utf-8"))}
    (OUT / "notice-schema.json").write_text(json.dumps(NOTICE_SCHEMA, ensure_ascii=False, indent=1), encoding="utf-8")
    for number in NOTICES:
        brief = json.loads((ROOT / f"data/ECE/briefs/{number}.json").read_text(encoding="utf-8"))
        source = briefs.read(notices[number]["url"])
        time.sleep(1)
        same = hashlib.sha256(source["text"].encode("utf-8")).hexdigest()[:16] == brief["text_hash"]
        (OUT / f"{prefix}-{number}.ko.txt").write_text(f"제목: {notices[number]['title_ko']}\n게시일: {notices[number]['date']}\n\n{source['text']}\n", encoding="utf-8")
        shown = {"title": brief["title_en"], "summary": brief["summary"], "steps": brief["steps"],
                 "dates": [{"what": d["what"], "when": d["when"], "korean_quoted": d["original_ko"]} for d in brief["dates"]]}
        if prefix != "notice":  # these two parts are shown on the page from the second reading on
            shown.update(who_must_act=brief["applies_to"], conditions_and_exceptions=brief.get("conditions", []))
        (OUT / f"{prefix}-{number}.en.json").write_text(json.dumps(shown, ensure_ascii=False, indent=1), encoding="utf-8")
        (OUT / f"{prefix}-{number}.prompt.txt").write_text(NOTICE_PROMPT.format(korean=f"{prefix}-{number}.ko.txt", english=f"{prefix}-{number}.en.json"), encoding="utf-8")
        print(f"{number}: {len(source['text'])} characters, {len(brief['dates'])} dates, unchanged since translation: {same}")
        if number == NOTICE_DECOY[0]:
            text = json.dumps(shown, ensure_ascii=False, indent=1)
            assert NOTICE_DECOY[1] in text, "decoy date not found"
            (OUT / f"{prefix}-check.ko.txt").write_text((OUT / f"{prefix}-{number}.ko.txt").read_text(encoding="utf-8"), encoding="utf-8")
            (OUT / f"{prefix}-check.en.json").write_text(text.replace(NOTICE_DECOY[1], NOTICE_DECOY[2]), encoding="utf-8")
            (OUT / f"{prefix}-check.prompt.txt").write_text(NOTICE_PROMPT.format(korean=f"{prefix}-check.ko.txt", english=f"{prefix}-check.en.json"), encoding="utf-8")


if __name__ == "__main__":
    {"prepare": prepare, "prepare-notices": lambda: prepare_notices(*sys.argv[2:3]), "prepare-pass": lambda: prepare_pass(int(sys.argv[2])), "collect": collect, "prepare-rest": lambda: prepare_rest(*sys.argv[2:4])}[sys.argv[1]]()
