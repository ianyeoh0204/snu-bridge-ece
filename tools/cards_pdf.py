# -*- coding: utf-8 -*-
"""Shared by the departments whose graduate rules come as a PDF downloaded by a person (tools/cards_nuclear.py,
tools/cards_naval.py). The PDFs stay in sources/<DEPARTMENT>/ and are never uploaded; only short quoted lines are.

A model from another maker re-read these cards on 13 Nov 2026 (data/<DEPARTMENT>/audit.json). Before that reading,
`write` refuses to save unless, for every card:
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


def card(id, programs, group, source, title, key, rule, quotes, why, when="", trap="", applies_from="", entry_years=()):
    """`entry_years`: the years of admission a card applies to, for rules that differ by year (undergraduate).
    When each year has its own document, name them "<source>-<year>" in the texts given to `verify`: the card's quotes
    must then be found in the document of EVERY year it applies to, and the site cites the student's own year's file."""
    return {"id": id, "programs": programs, "group": group, "title": title, "key": key, "rule": rule, "why": why, "when": when, "trap": trap,
            "applies_from": applies_from, "events": [], "source_file": source, "source_page": 0, "source_page_also": 0,
            "source_quote_ko": quotes[0], "quotes_ko": quotes, "entry_years": sorted(entry_years), "updates": []}


def numbers(text):
    return set(re.findall(r"\d+(?:\.\d+)?", text))


def verify(cards, texts):
    """Check every card against its source; fill in the page; stop with the list of problems if there are any.
    `texts` maps a source key to the list of page texts of that file."""
    plain = lambda text: re.sub(r"\s+", "", text)
    problems = []
    for c in cards:
        yearly = [f"{c['source_file']}-{year}" for year in c["entry_years"]] if f"{c['source_file']}-{(c['entry_years'] or [0])[-1]}" in texts else []
        keys = yearly or [c["source_file"]]
        if any(key not in texts for key in keys):
            problems.append(f"{c['id']}: no source text for {[k for k in keys if k not in texts]}")
            continue
        for key in keys:
            whole = plain("".join(texts[key]))
            for quote in c["quotes_ko"]:
                if plain(quote) not in whole:
                    problems.append(f"{c['id']}: a quote is not in '{key}': {quote[:60]}")
        if yearly:
            c["source_file"], c["source_page"] = yearly[-1], 0  # the newest year's file; the site swaps in the reader's own year
        else:
            first = plain(c["quotes_ko"][0])
            c["source_page"] = next((i + 1 for i, page in enumerate(texts[keys[0]]) if first[:25] in plain(page)), 0)
        missing = numbers(" ".join([c["title"], c["key"]] + c["rule"])) - numbers(" ".join(c["quotes_ko"]))
        if missing:
            problems.append(f"{c['id']}: numbers in the English that are in no quote: {sorted(missing)}")
        for field in ("why", "when", "trap"):
            extra = numbers(c[field]) - numbers(" ".join(c["quotes_ko"]))
            if extra:
                problems.append(f"{c['id']}: numbers in '{field}' that are in no quote: {sorted(extra)}")
        if "undergraduate" in c["programs"] and not c["entry_years"]:
            problems.append(f"{c['id']}: an undergraduate card must say which years of admission it applies to (entry_years)")
    if len({c["id"] for c in cards}) != len(cards):
        problems.append("two cards share an id")
    if problems:
        sys.exit("Nothing was written.\n" + "\n".join(problems))
    return cards


def write(department, cards, texts=None):
    """Save a department's cards. With `texts`, check them first; without, they were checked already by `verify`."""
    if texts is not None:
        verify(cards, texts)
    target = ROOT / "data" / department / "cards.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(cards, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    programs = ["undergraduate"] + ALL
    print(f"{len(cards)} cards written to {target.relative_to(ROOT)}:", {p: sum(p in c["programs"] for c in cards) for p in programs if any(p in c["programs"] for c in cards)})
    print("Every quote is in the file it cites, and every number in the English is in a quote.")
