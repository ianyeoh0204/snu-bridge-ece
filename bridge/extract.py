"""Step 2 of the pipeline: official pages in, cards out.

Every request sees all pages, so a rule on one page can be read with a note on another.
Each request writes cards for a few pages only, and progress is saved after each one,
so a failure costs one small request, not the whole run.
"""
from __future__ import annotations

import json
from pathlib import Path

from . import cards, llm, sources

BATCH = 5  # pages written per request

SYSTEM = """You turn a Korean university department's official documents into short requirement cards \
for international students who cannot read Korean.

Write one card per rule a student must act on to finish their degree. Rules for each card:
- Use only what the pages state. Never add outside knowledge. Copy every number exactly.
- Keep each condition and exception the source gives. Never drop one because it looks rare.
- One rule that differs by program becomes one card per program. A rule shared by all programs is one card.
- `rule` is 1 to 5 short lines in plain English. No paragraphs.
- `group` says what the rule unlocks: start_early for things with limited windows or prerequisites \
that take a semester; before_exam for qualification-exam eligibility; finish_coursework for credit and \
course rules; for_degree for thesis, papers and defense; every_semester for recurring duties.
- `why` is one line naming what the rule unlocks or blocks.
- `trap` is the easy mistake, only if the source states it.
- `source_quote_ko` is the Korean line copied exactly from the page, and `source_file` and `source_page` \
are the labels given before that page.
- Skip personal names, phone numbers and email addresses. Skip pages that only list people."""


def run(department: str, state_file: Path) -> list[dict]:
    units = sources.load(department)
    pages: list[dict] = []
    for unit in units:
        pages.append(llm.text(f"File: {unit['file']} | Page: {unit['page']} | {unit['name']}"))
        pages.append(llm.image(unit["png"]) if "png" in unit else llm.text(unit["text"]))
    pages[-1]["cache_control"] = {"type": "ephemeral"}  # later requests reuse the pages at a fraction of the price

    state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {"done": [], "cards": []}
    for start in range(0, len(units), BATCH):
        if start in state["done"]:
            continue
        wanted = "; ".join(f"{u['file']} page {u['page']}" for u in units[start:start + BATCH])
        ask = llm.text(f"Write cards only for rules stated on these pages: {wanted}. "
                       "Use the other pages as context. Return an empty list if these pages hold no rule.")
        state["cards"] += llm.ask(SYSTEM, pages + [ask], cards.CARD_LIST)["cards"]
        state["done"].append(start)
        state_file.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"pages {start + 1}-{min(start + BATCH, len(units))} of {len(units)} done, {len(state['cards'])} cards so far")
    return state["cards"]
