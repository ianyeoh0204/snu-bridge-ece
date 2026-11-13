"""Read each notice's text and write an English brief with a full translation.

A brief is rewritten only when the notice text changes, so an edited notice is caught by its hash.
Every Korean date the model quotes is checked against the notice text in plain code.
"""
from __future__ import annotations

import datetime
import hashlib
import html
import json
import re
import time
from pathlib import Path

from . import llm
from .notices import ROOT, _fetch

PROMPT_VERSION = 2  # raise this when SYSTEM or BRIEF changes; every notice is then translated again
BRIEF = {
    "type": "object", "additionalProperties": False,
    "required": ["title_en", "summary", "applies_to", "dates", "conditions", "steps", "translation"],
    "properties": {
        "title_en": {"type": "string"},
        "summary": {"type": "string", "description": "Two or three formal sentences: who must act, what they must do, by when and where"},
        "applies_to": {"type": "string", "description": "Who must act, with every limit the notice states. Empty if not stated."},
        "dates": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["what", "when", "original_ko"],
            "properties": {"what": {"type": "string"}, "when": {"type": "string"},
                           "original_ko": {"type": "string", "description": "The date text copied exactly from the notice"}}}},
        "conditions": {"type": "array", "items": {"type": "string"},
                       "description": "Conditions, exceptions, exclusions, prohibitions and consequences. Empty if none."},
        "steps": {"type": "array", "items": {"type": "string"}, "description": "Actions in order. Empty if none."},
        "translation": {"type": "string", "description": "Full English translation, paragraphs separated by blank lines"},
    },
}

# Version 2 follows an audit (tools/audit.py) in which a second reader found no wrong dates in ten notices but found
# that every short summary left out something a student could need: who exactly, a condition, a further date.
SYSTEM = """You translate notices from a Korean university department's academic board for international \
students who cannot read Korean. Many will read only the short parts (summary, who must act, dates, conditions, \
steps) and never open the full translation, so the short parts must be complete enough to act on safely. \
Write formal, plain English, as an official university page would.

- Use only what the notice states. Never add outside knowledge, never infer a date, and never narrow or widen who \
a rule applies to.
- `title_en`: short and formal, at most 14 words. Write "Fall 2026" for 2026학년도 2학기 and "Spring 2026" for 1학기.
- `summary`: two or three sentences. Who must act, what they must do, by when and where.
- `applies_to`: exactly who must act: program, year of admission, registered semester, nationality or any other \
limit in the notice, and whether it is mandatory. Keep every condition.
- `dates`: every date, time, period or deadline a student could need to act on or plan around: when something \
happens, opens, closes or is due. Include times of day, entry cut-off times, fee periods, result and submission \
deadlines, and periods stated loosely (such as "in November"). In `what`, say what it is for and, if it is only for \
some students, for whom. `original_ko` is the date text copied exactly as written in the notice. Do not list the \
date the notice was posted, or dates that only tell when a rule was made.
- `conditions`: one short sentence for every condition, exception, exclusion, prohibition and consequence that \
changes what a student should do or what happens if they do not: who is exempt, what is not accepted, what is not \
allowed, what happens when a deadline is missed, what else must already be completed.
- `steps`: what the student must do, in order. Each step says where (building and room number whenever the notice \
gives them anywhere), how (the form, website or menu path) and what to bring or submit. If the notice tells \
students to read another notice or an attachment first, that is a step. When the notice describes separate cases \
(for example attending in person and attending online), begin every step of a case with the case name and a \
colon, worded identically each time; the site shows the name once as a heading.
- `translation`: the whole notice in English. Keep the structure and every condition. Keep course codes, \
form names and system menu paths, giving the Korean term in brackets where a student must recognise it on screen.
- Keep distinct words distinct: 날인 is a seal (stamp) and 서명 is a signature; 청강 is auditing and 수강신청 is \
course registration; 신규교육 is the initial training for those who have not yet completed it, not training for \
new employees; 석박통합과정 is the integrated master's-doctoral program. 필수 means must.
- Never include a person's name, email address or phone number. Refer to "the department office" and \
tell the reader the contact is in the original notice.
- If the notice refers to an image or attachment whose content is not in the text, say that it was not read."""

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"\b0\d{1,2}[-)\s]\d{3,4}-\d{4}\b|\b880-\d{4}\b")
# The page prints a download counter beside each attachment. It rises all day, so it must not count as a change to the notice.
COUNTER = re.compile(r",\s*download:\s*\d+")
SEOUL = datetime.timezone(datetime.timedelta(hours=9))


def read(url: str) -> dict:
    """The notice text with contact details removed, plus what could not be read."""
    page = _fetch(url)
    start = page.rfind("조회수")
    end = page.find('class="rbtn', start)  # the row of buttons under the notice
    if end < 0:
        end = page.find('class="function"', start)  # the same row on Nuclear Engineering's pages
    if start < 0 or end < 0:
        raise RuntimeError(f"Notice page layout changed, cannot find the body: {url}")
    region = page[start:end].rsplit("<", 1)[0]  # drop the tag the cut landed in
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", region, flags=re.S)
    text = re.sub(r"<br\s*/?>|</p>|</div>|</li>|</tr>|</h\d>", "\n", text)
    text = html.unescape(re.sub(r"<[^>]+>", "", re.sub(r"</t[dh]>", " | ", text)))
    text = re.sub(r"[ \t　]+", " ", re.sub(r"\n\s*\n+", "\n", text)).strip()
    text = COUNTER.sub("", re.sub(r"^조회수\s*\d+\s*", "", text))
    return {
        "text": PHONE.sub("[phone]", EMAIL.sub("[email]", text)),
        "images": len(re.findall(r'<img[^>]+src="(?!/_skin/)', region)),
        "attachments": [TITLED_NAME.sub(r"\1", html.unescape(a).strip()) for a in re.findall(r'(?:md|bm)=down[^"]*">([^<]+)</a>', region)],
    }


# A person's name before a title in an attachment's file name, such as "(홍길동교수님)". Role words are not names.
TITLED_NAME = re.compile(r"(?<![가-힣])(?!지도|담당|심사|책임|주임|초빙|겸임|명예|연구|강의|석좌|전임|신임)[가-힣]{2,4}(교수|박사)(?=님|[^가-힣]|$)")


def _squash(value: str) -> str:
    return re.sub(r"\s+", "", value)


def _translate(notice: dict, target: Path) -> str:
    """Write the brief for one notice if it is new or its text changed. Returns a log line, or "" if nothing was needed."""
    source = read(notice["url"])
    time.sleep(1)
    digest = hashlib.sha256(source["text"].encode("utf-8")).hexdigest()[:16]
    old = json.loads(target.read_text(encoding="utf-8")) if target.exists() else None
    if old and old["text_hash"] == digest and old.get("prompt") == PROMPT_VERSION:
        return ""
    changed = bool(old) and old["text_hash"] != digest  # the notice itself was edited, not just our instructions
    brief = llm.ask(SYSTEM, [llm.text(f"Title: {notice['title_ko']}\nPosted: {notice['date']}\n\n{source['text']}")],
                    BRIEF, max_tokens=32000, effort="medium")
    body = _squash(notice["title_ko"] + source["text"])  # a deadline is sometimes stated only in the title
    for date in brief["dates"]:
        date["verified"] = _squash(date["original_ko"]) in body
    brief.update(id=notice["id"], text_hash=digest, images=source["images"], attachments=source["attachments"],
                 model=llm.MODEL, written=datetime.datetime.now(SEOUL).date().isoformat(), prompt=PROMPT_VERSION,
                 revised=changed or bool(old and old.get("revised")))
    target.write_text(json.dumps(brief, ensure_ascii=False, indent=1), encoding="utf-8")
    unverified = sum(not d["verified"] for d in brief["dates"])
    return f"{notice['id']} {len(brief['dates'])} dates, {unverified} not found in the text, {source['images']} images unread"


def update(department: str, limit: int = 0, only: set | None = None) -> tuple[list[str], list[str], int]:
    """Translate what is new or changed. Returns (written, failed, checked). One bad notice never stops the rest."""
    data = ROOT / "data" / department
    out = data / "briefs"
    out.mkdir(parents=True, exist_ok=True)
    written, failed, checked = [], [], 0
    for notice in json.loads((data / "notices.json").read_text(encoding="utf-8")):
        if limit and len(written) >= limit:
            break
        if only and notice["id"] not in only:
            continue
        try:
            line = _translate(notice, out / f"{notice['id']}.json")
        except Exception as error:  # network trouble, a changed page layout, or a notice too long for the model
            failed.append(f"{notice['id']} not translated ({type(error).__name__}: {error})")
            print(failed[-1], flush=True)
            continue
        checked += 1
        if line:
            written.append(line)
            print(line, flush=True)
    return written, failed, checked
