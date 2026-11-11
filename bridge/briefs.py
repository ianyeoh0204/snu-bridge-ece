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

BRIEF = {
    "type": "object", "additionalProperties": False,
    "required": ["title_en", "summary", "applies_to", "dates", "steps", "translation"],
    "properties": {
        "title_en": {"type": "string"},
        "summary": {"type": "string", "description": "One or two formal sentences"},
        "applies_to": {"type": "string", "description": "Who must act, as the notice states it. Empty if not stated."},
        "dates": {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["what", "when", "original_ko"],
            "properties": {"what": {"type": "string"}, "when": {"type": "string"},
                           "original_ko": {"type": "string", "description": "The date text copied exactly from the notice"}}}},
        "steps": {"type": "array", "items": {"type": "string"}, "description": "Actions in order. Empty if none."},
        "translation": {"type": "string", "description": "Full English translation, paragraphs separated by blank lines"},
    },
}

SYSTEM = """You translate notices from a Korean university department's academic board for international \
students who cannot read Korean. Write formal, plain English, as an official university page would.

- Use only what the notice states. Never add outside knowledge, and never infer a date.
- `title_en`: short and formal, at most 14 words. Write "Fall 2026" for 2026학년도 2학기 and "Spring 2026" for 1학기.
- `dates`: every deadline, period or event with a calendar date in the notice, and nothing else. \
`original_ko` is the date text copied exactly as written in the notice. Do not list the date the notice was posted.
- `steps`: what the student must do, in order, with the place and method stated in the notice. When the notice \
describes separate cases (for example attending in person and attending online), begin every step of a case with \
the case name and a colon, worded identically each time; the site shows the name once as a heading.
- `applies_to`: who must act, exactly as the notice limits it. Keep every condition and exception.
- `translation`: the whole notice in English. Keep the structure and every condition. Keep course codes, \
form names and system menu paths, giving the Korean term in brackets where a student must recognise it on screen.
- Never include a person's name, email address or phone number. Refer to "the department office" and \
tell the reader the contact is in the original notice.
- If the notice refers to an image or attachment whose content is not in the text, say that it was not read."""

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"\b0\d{1,2}[-)\s]\d{3,4}-\d{4}\b|\b880-\d{4}\b")


def read(url: str) -> dict:
    """The notice text with contact details removed, plus what could not be read."""
    page = _fetch(url)
    start = page.rfind("조회수")
    end = page.find('class="rbtn', start)  # the row of buttons under the notice
    if start < 0 or end < 0:
        raise RuntimeError(f"Notice page layout changed, cannot find the body: {url}")
    region = page[start:end].rsplit("<", 1)[0]  # drop the tag the cut landed in
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", region, flags=re.S)
    text = re.sub(r"<br\s*/?>|</p>|</div>|</li>|</tr>|</h\d>", "\n", text)
    text = html.unescape(re.sub(r"<[^>]+>", "", re.sub(r"</t[dh]>", " | ", text)))
    text = re.sub(r"[ \t　]+", " ", re.sub(r"\n\s*\n+", "\n", text)).strip()
    text = re.sub(r"^조회수\s*\d+\s*", "", text)
    return {
        "text": PHONE.sub("[phone]", EMAIL.sub("[email]", text)),
        "images": len(re.findall(r'<img[^>]+src="(?!/_skin/)', region)),
        "attachments": [TITLED_NAME.sub(r"\1", html.unescape(a).strip()) for a in re.findall(r'md=down[^"]*">([^<]+)</a>', region)],
    }


# A person's name before a title in an attachment's file name, such as "(홍길동교수님)". Role words are not names.
TITLED_NAME = re.compile(r"(?<![가-힣])(?!지도|담당|심사|책임|주임|초빙|겸임|명예|연구|강의|석좌|전임|신임)[가-힣]{2,4}(교수|박사)(?=님|[^가-힣]|$)")


def _squash(value: str) -> str:
    return re.sub(r"\s+", "", value)


def update(department: str, limit: int = 0) -> list[str]:
    data = ROOT / "data" / department
    out = data / "briefs"
    out.mkdir(parents=True, exist_ok=True)
    log = []
    for notice in json.loads((data / "notices.json").read_text(encoding="utf-8")):
        if limit and len(log) >= limit:
            break
        target = out / f"{notice['id']}.json"
        source = read(notice["url"])
        time.sleep(1)
        digest = hashlib.sha256(source["text"].encode("utf-8")).hexdigest()[:16]
        if target.exists() and json.loads(target.read_text(encoding="utf-8"))["text_hash"] == digest:
            continue
        brief = llm.ask(SYSTEM, [llm.text(f"Title: {notice['title_ko']}\nPosted: {notice['date']}\n\n{source['text']}")],
                        BRIEF, max_tokens=16000, effort="medium")
        body = _squash(notice["title_ko"] + source["text"])  # a deadline is sometimes stated only in the title
        for date in brief["dates"]:
            date["verified"] = _squash(date["original_ko"]) in body
        brief.update(id=notice["id"], text_hash=digest, images=source["images"], attachments=source["attachments"],
                     model=llm.MODEL, written=datetime.date.today().isoformat(),
                     revised=target.exists())
        target.write_text(json.dumps(brief, ensure_ascii=False, indent=1), encoding="utf-8")
        unverified = sum(not d["verified"] for d in brief["dates"])
        log.append(f"{notice['id']} {len(brief['dates'])} dates, {unverified} not found in the text, {source['images']} images unread")
        print(log[-1], flush=True)
    return log
