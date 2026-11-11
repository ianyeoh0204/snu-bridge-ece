# -*- coding: utf-8 -*-
"""Write out/korean-review.md: every English and Korean pair the site shows, with a prompt for a Korean check.
Run from the project folder: .venv/bin/python tools/korean_review.py"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
pairs = list(json.loads((ROOT / "bridge/text.json").read_text(encoding="utf-8"))["pairs"].items())


def walk(value):  # labels in the hand-checked notes; the department's own notice titles are left out, they are not ours to edit
    if isinstance(value, dict):
        if "en" in value and "ko" in value and "title" not in value:
            pairs.append((value["en"], value["ko"]))
        for key, inner in value.items():
            if key != "title":
                walk(inner)
    elif isinstance(value, list):
        for inner in value:
            walk(inner)


for notes in sorted((ROOT / "sources").glob("*/evidence_notes.json")):
    walk(json.loads(notes.read_text(encoding="utf-8")))
lines = ["# Korean wording to check", "", "Paste everything below into ChatGPT, or give it to a Korean reader.", "", "```text",
         "You are a native Korean editor at a Korean university. Below is a table of English sentences and their Korean",
         "versions. On the website each Korean line is shown in small type under its English line (formal 합니다 style).",
         "For each row, check that the Korean (1) means exactly what the English says, nothing added or dropped,",
         "(2) reads naturally to Korean university staff, (3) uses the terms a Korean university uses",
         "(for example 학사 게시판, 논문제출자격시험, 이수규정, 석박사통합과정).",
         "Keep every {placeholder} exactly as it is. Do not change the English.",
         "Reply with a table of only the rows you would change: row number, your Korean, and one line saying why.",
         "Leave out rows that are fine. Finish with any term that is used inconsistently across rows.", "```", "",
         "| # | English | Korean |", "|---|---|---|"]
lines += [f"| {i} | {en.replace('|', '/')} | {ko.replace('|', '/')} |" for i, (en, ko) in enumerate(pairs, 1)]
(ROOT / "out").mkdir(exist_ok=True)
(ROOT / "out/korean-review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"{len(pairs)} pairs written to out/korean-review.md")
