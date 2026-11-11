"""Step 3 of the pipeline: a second reading of each page against its cards."""
from __future__ import annotations

import json

from . import cards, llm, sources

SYSTEM = """You are the second reader. You get one page of a Korean official document and the cards \
written from it. For each card decide:
- confirmed: the page states what the card says, numbers included, and the Korean quote is on the page.
- wrong: the page says something different. Name the difference in `problem`.
- not_on_page: the card's content is not on this page.
Then list in `missing` any rule on the page that a student must act on and no card covers.
Judge only against this page. Do not use outside knowledge."""


def run(department: str, all_cards: list[dict]) -> list[dict]:
    """Return the cards with `check` and `check_problem` filled in, plus a list of gaps."""
    by_page: dict[tuple, list[dict]] = {}
    for card in all_cards:
        by_page.setdefault((card["source_file"], card["source_page"]), []).append(card)
    gaps: list[dict] = []
    for unit in sources.load(department):
        key = (unit["file"], unit["page"])
        page_cards = by_page.pop(key, [])
        page = llm.image(unit["png"]) if "png" in unit else llm.text(unit["text"])
        answer = llm.ask(SYSTEM, [page, llm.text(json.dumps(page_cards, ensure_ascii=False))],
                         cards.PAGE_CHECK, max_tokens=8000)
        verdicts = {item["id"]: item for item in answer["cards"]}
        for card in page_cards:
            verdict = verdicts.get(card["id"], {"verdict": "unchecked", "problem": "second reader gave no verdict"})
            card["check"], card["check_problem"] = verdict["verdict"], verdict["problem"]
        gaps += [{"file": unit["file"], "page": unit["page"], "missing": text} for text in answer["missing"]]
    for orphan in (card for group in by_page.values() for card in group):
        orphan["check"], orphan["check_problem"] = "not_on_page", "source page is not among the files read"
    return gaps
