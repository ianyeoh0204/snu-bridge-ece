# -*- coding: utf-8 -*-
"""A sheet for a Korean-speaking reader: ten notices as this site shows them in English, each beside its Korean original.

    .venv/bin/python tools/reader_sheet.py      writes out/review/notices-for-a-korean-reader.md (not published)

The proposal promised briefs "reviewed by the applicant with a Korean-speaking labmate". So far they are checked by
code (each quoted date is found in the notice) and, up to 13 Nov 2026, by a second AI reader
(data/<DEPARTMENT>/notice_reading.json). This sheet is for the human
reading. It takes the ten notices with the most dates still ahead, because a wrong date there can still do harm.
When the reader has finished, record the result by hand in sources/ECE/reader_notes.json; nothing reads that file yet.
"""
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = json.loads((ROOT / "sources/ECE/config.json").read_text(encoding="utf-8"))["site"]

if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(ROOT))
    from bridge import deadlines

    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date()
    notices = json.loads((ROOT / "data/ECE/notices.json").read_text(encoding="utf-8"))
    scored = []
    for n in notices:
        file = ROOT / "data/ECE/briefs" / f"{n['id']}.json"
        if not file.exists():
            continue
        brief = json.loads(file.read_text(encoding="utf-8"))
        ahead = sum(1 for d in brief["dates"] if (e := deadlines.read(d["original_ko"], d["when"], n["date"])) and e["day"] >= today)
        scored.append((ahead, n, brief))
    chosen = sorted(scored, key=lambda item: (-item[0], item[1]["date"]))[:10]
    out = ["# Ten notices for a Korean-speaking reader", "",
           f"Prepared {today.isoformat()}. For each notice: open the Korean original, read the English beside it, and mark each line.",
           "Mark **OK**, **Wrong** (say what) or **Missing** (say what the Korean has that the English does not). About 5 minutes a notice.", ""]
    for i, (ahead, n, b) in enumerate(chosen, 1):
        out += [f"## {i}. {b['title_en']}", "", f"- Korean title: {n['title_ko']}", f"- Korean original: {n['url']}", f"- On the site: {SITE}#notice-{n['id']}",
                f"- Posted {n['date']}; {ahead} dates still ahead", "", f"**Who must act.** {b.get('applies_to', '')}", "", "- [ ] OK   - [ ] Wrong / Missing: ", "",
                "**Summary.** " + b["summary"], "", "- [ ] OK   - [ ] Wrong / Missing: ", "", "| What | When (English) | Korean in the notice | OK? |", "|---|---|---|---|"]
        out += [f"| {d['what']} | {d['when']} | {d['original_ko']} | |" for d in b["dates"]]
        out += ["", "**Conditions and exceptions.**"] + [f"- [ ] {c}" for c in b.get("conditions", [])] + ["", "**Steps.**"] + [f"- [ ] {s}" for s in b.get("steps", [])]
        out += ["", "Anything in the Korean notice that a student needs and that is not above: ", "", "---", ""]
    target = ROOT / "out" / "review" / "notices-for-a-korean-reader.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(out), encoding="utf-8")
    print(f"{target.relative_to(ROOT)}: {len(chosen)} notices, {sum(len(b['dates']) for _, _, b in chosen)} dates;", ", ".join(str(n["id"]) for _, n, _ in chosen))
