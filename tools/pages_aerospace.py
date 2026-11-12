"""Aerospace Engineering's graduate rules, read from the department's own web pages into plain text, one file per
page and per entry-year tab. Each page carries two rule sets: `tab-2020` (entrants up to 2020) and `tab-2021` (entrants
from 2021). They are separated by the page's own element ids, read with a real HTML parser: cutting the text at the
first mention of an id put both sets in one file, and the tab captions in the page text are in a misleading order.

    .venv/bin/python tools/pages_aerospace.py      writes out/aerospace/<page>.<tab>.txt (not published)
"""
import html.parser
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import survey  # noqa: E402  (its `get` keeps one copy of each page and waits a second between requests)

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://aerospace.snu.ac.kr/"
PAGES = {"completion": "graduate/completion/graduate", "qualifying": "graduate/completion/qualifying-examination",
         "committee": "graduate/completion/committee", "thesis": "graduate/completion/examination-thesis"}
VOID = {"br", "img", "hr", "input", "meta", "link", "col", "area", "base", "source", "wbr"}
BREAKS = {"br", "p", "li", "tr", "div", "h1", "h2", "h3", "h4", "h5", "dt", "dd", "table"}


class Pane(html.parser.HTMLParser):
    """The text inside the element with one id, however deeply other elements are nested in it."""

    def __init__(self, wanted):
        super().__init__(convert_charrefs=True)
        self.wanted, self.depth, self.parts, self.skip = wanted, 0, [], 0

    def handle_starttag(self, tag, attrs):
        if self.depth:
            if tag in ("script", "style"):
                self.skip += 1
            if tag in BREAKS:
                self.parts.append("\n")
            if tag not in VOID:
                self.depth += 1
        elif dict(attrs).get("id") == self.wanted:
            self.depth = 1

    def handle_endtag(self, tag):
        if self.depth and tag not in VOID:
            if tag in ("script", "style") and self.skip:
                self.skip -= 1
            if tag in BREAKS:
                self.parts.append("\n")
            self.depth -= 1

    def handle_data(self, data):
        if self.depth and not self.skip:
            self.parts.append(data)


def pane(page, tab):
    reader = Pane(tab)
    reader.feed(survey.get(SITE + PAGES[page]))
    lines = (re.sub(r"[ \t\xa0]+", " ", line).strip() for line in "".join(reader.parts).split("\n"))
    return [line for line in lines if line]


if __name__ == "__main__":
    out = ROOT / "out" / "aerospace"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.txt"):
        old.unlink()
    for page in PAGES:
        for tab in ("tab-2020", "tab-2021"):
            lines = pane(page, tab)
            if not lines:
                sys.exit(f"{page} / {tab}: nothing was read. The page may have changed.")
            (out / f"{page}.{tab}.txt").write_text("\n".join(lines), encoding="utf-8")
            print(f"{page:11} {tab}: {len(lines):3} lines, {sum(map(len, lines)):5} characters | {lines[0][:40]}")
