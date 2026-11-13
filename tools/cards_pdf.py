# -*- coding: utf-8 -*-
"""Shared by the departments whose graduate rules come as a PDF downloaded by a person (tools/cards_nuclear.py,
tools/cards_naval.py). The PDFs stay in sources/<DEPARTMENT>/ and are never uploaded; only short quoted lines are.

No second reader from another maker re-reads these cards. In its place `write` refuses to save unless, for every card:
  1. each Korean quote is found, word for word (spaces and line breaks aside), in the file the card cites;
  2. every number in the card's English title, key fact and rule lines appears in its Korean quotes.
The page shown for a card is the page of the PDF on which its first quote is found, so it is never typed by hand.
`why`, `when` and `trap` are not checked by code: keep them to what a quote says.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALL, DOCTORAL = ["masters", "phd", "integrated"], ["phd", "integrated"]


def pages(department, name):
    """The text of each page of sources/<department>/<file whose name contains `name`>."""
    import fitz

    found = [f for f in (ROOT / "sources" / department).glob("*.pdf") if name in f.name]
    if len(found) != 1:
        sys.exit(f"sources/{department}: expected one PDF whose name contains '{name}', found {len(found)}. Download it by hand (see the config).")
    return found[0].name, [page.get_text() for page in fitz.open(found[0])]


def card(id, programs, group, source, title, key, rule, quotes, why, when="", trap="", applies_from=""):
    return {"id": id, "programs": programs, "group": group, "title": title, "key": key, "rule": rule, "why": why, "when": when, "trap": trap,
            "applies_from": applies_from, "events": [], "source_file": source, "source_page": 0, "source_page_also": 0,
            "source_quote_ko": quotes[0], "quotes_ko": quotes, "check": "unchecked", "entry_years": [], "updates": []}


def numbers(text):
    return set(re.findall(r"\d+(?:\.\d+)?", text))


def write(department, cards, texts):
    """`texts` maps a card's source key to the list of page texts of that file."""
    plain = lambda text: re.sub(r"\s+", "", text)
    problems = []
    for c in cards:
        if c["source_file"] not in texts:
            problems.append(f"{c['id']}: unknown source '{c['source_file']}'")
            continue
        by_page = [plain(page) for page in texts[c["source_file"]]]
        whole = "".join(by_page)
        for quote in c["quotes_ko"]:
            if plain(quote) not in whole:
                problems.append(f"{c['id']}: a quote is not in '{c['source_file']}': {quote[:60]}")
        first = plain(c["quotes_ko"][0])
        on = next((i + 1 for i, page in enumerate(by_page) if first[:25] in page), 0)
        c["source_page"] = on
        missing = numbers(" ".join([c["title"], c["key"]] + c["rule"])) - numbers(" ".join(c["quotes_ko"]))
        if missing:
            problems.append(f"{c['id']}: numbers in the English that are in no quote: {sorted(missing)}")
        for field in ("why", "when", "trap"):
            extra = numbers(c[field]) - numbers(" ".join(c["quotes_ko"]))
            if extra:
                problems.append(f"{c['id']}: numbers in '{field}' that are in no quote: {sorted(extra)}")
    if len({c["id"] for c in cards}) != len(cards):
        problems.append("two cards share an id")
    if problems:
        sys.exit("Nothing was written.\n" + "\n".join(problems))
    target = ROOT / "data" / department / "cards.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(cards, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(cards)} cards written to {target.relative_to(ROOT)}:", {p: sum(p in c["programs"] for c in cards) for p in ALL})
    print("Every quote is in the file it cites, and every number in the English is in a quote.")
