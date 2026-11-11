# -*- coding: utf-8 -*-
"""Check each undergraduate card against the document of every entry year it applies to:
the Korean quote and every course code in the card must appear in that year's text.
Run from the project folder: .venv/bin/python tools/check_quotes.py"""
import json
import re
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
squash = lambda s: re.sub(r"\s+", "", s)
config = json.loads((ROOT / "sources/ECE/config.json").read_text(encoding="utf-8"))
files = {f["entry_year"]: f["file"] for f in config["files"] if f.get("entry_year")}
text = {y: squash("".join(p.get_text() for p in fitz.open(ROOT / "sources/ECE" / name))) for y, name in files.items()}
cards = [c for c in json.loads((ROOT / "data/ECE/cards.json").read_text(encoding="utf-8")) if "undergraduate" in c["programs"]]
failures = 0
for c in cards:
    for year in c["entry_years"] or sorted(text):
        missing = [] if squash(c["source_quote_ko"]) in text[year] else ["quote"]
        words = " ".join(c["rule"] + [c["key"], c["trap"]])
        missing += [code for code in set(re.findall(r"\b(?:M\d{4}\.\d{6}|\d{3}\.\d{3}[A-Z]?)\b", words)) if code not in text[year]]
        if missing:
            failures += 1
            print(year, c["id"], "not found:", missing)
print(f"{len(cards)} undergraduate cards, {len(text)} entry years, {failures} failures")
sys.exit(1 if failures else 0)
