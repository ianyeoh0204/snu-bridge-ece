"""A calendar file of the deadlines in a department's notices, for students to subscribe to.

No model is asked for a date here. Each date is read by plain code from the Korean text the notice itself printed
(already confirmed word for word in the notice), and it is kept only if all of this holds:
  1. the Korean names a weekday, and the date really falls on that weekday. Without a printed year, the year is the
     notice's own or the next, and the date lies no more than 300 days after the notice;
  2. the English line shown on the site names the same day and month, and no other year;
  3. the Korean holds one date, or two dates that form a period (then the event is the last day). A date followed by
     the end of a period that could not be read is left out, so an opening day never passes as a deadline.
A time is kept only if the English shows the same time, and never guessed: "5시" without 오전 or 오후 gives a day, no time.
Everything else (relative dates such as "one week before", dates without a weekday) stays on the notice page only.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEOUL = datetime.timezone(datetime.timedelta(hours=9))
WEEKDAY = "월화수목금토일"  # Monday is 0, as in datetime.weekday()
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
# "2026. 12. 21.(월)", "12월 21일(월)", "12/21(월)", "10.1(목)"; the year is optional
DATE = re.compile(r"(?:(20\d{2})\s*[.년]\s*)?(\d{1,2})\s*[.월/]\s*(\d{1,2})\s*[.일]?\s*\(\s*([월화수목금토일])\s*\)")
TIME = re.compile(r"^\s*(오전|오후)?\s*(\d{1,2})\s*(?::|시)\s*(\d{2})?")
RANGE = r"[~∼～–\-]"
BETWEEN = re.compile(RANGE + "|부터")
# after a date: a range mark and then something shaped like another date, such as "~ 8. 31" or "~ 20.(금)"
ANOTHER_DATE = re.compile(RANGE + r"\s*(?:20\d{2}\s*[.년]\s*)?\d{1,2}\s*(?:[.월/]\s*\d{1,2}|[.일]?\s*\()")
FAR = datetime.timedelta(days=300)


def _day(match: re.Match, after: datetime.date) -> datetime.date | None:
    """The date a match names, if it falls on the weekday printed beside it.
    `after` is the day the notice was posted, or the first day of the period this date closes."""
    years = [int(match.group(1))] if match.group(1) else [after.year, after.year + 1]
    for year in years:
        try:
            day = datetime.date(year, int(match.group(2)), int(match.group(3)))
        except ValueError:
            continue
        if day.weekday() == WEEKDAY.index(match.group(4)) and (match.group(1) or day - after <= FAR):
            return day
    return None


def _time(text: str) -> tuple[tuple[int, int] | None, str]:
    """The time a text starts with, and the text after it. None if there is no time or the hour could mean two things."""
    match = TIME.match(text)
    if not match:
        return None, text
    half, hour, minute = match.group(1), int(match.group(2)), int(match.group(3) or 0)
    if half == "오후" and hour < 12:
        hour += 12
    elif half == "오전" and hour == 12:
        hour = 0
    elif not half and hour < 8:
        return None, text  # "5시" is five in the afternoon far more often than five in the morning: do not guess
    return ((hour, minute) if hour < 24 and minute < 60 else None), text[match.end():]


def _says(when_en: str, hour: int, minute: int) -> bool:
    """Whether the English line shows this time, in 24-hour or 12-hour form."""
    text = re.sub(r"(?<=\d)\s*([ap])\.?m\b\.?", r"\1m", when_en.lower())  # "5:00 p.m." becomes "5:00pm"
    twelve, half = (hour % 12) or 12, "am" if hour < 12 else "pm"
    forms = [rf"{hour:02d}:{minute:02d}(?!\d|[ap]m)", rf"{hour}:{minute:02d}(?!\d|[ap]m)", rf"{twelve}:{minute:02d}{half}"]
    forms += [rf"{twelve}{half}"] if minute == 0 else []
    return any(re.search(r"(?<![\d:])" + form, text) for form in forms) or (hour == 12 and minute == 0 and "noon" in text)


def read(original_ko: str, when_en: str, posted: str) -> dict | None:
    """One event from one date line, or None if any check fails."""
    found = list(DATE.finditer(original_ko))
    if not found or len(found) > 2:
        return None
    last = found[-1]
    before, after = original_ko[:found[0].start()], original_ko[last.end():]
    if len(found) == 2:
        if not BETWEEN.search(original_ko[found[0].end():found[1].start()]):
            return None
        period = True
    else:
        if ANOTHER_DATE.search(after):
            return None  # the first day of a period whose last day could not be read
        period = bool(re.search(r"\d.*" + RANGE + r"\s*$", before))  # "8. 13. ~ 8. 31.(월)": only the last day carries a weekday
    posted_on = datetime.date.fromisoformat(posted)
    first = _day(found[0], posted_on)
    day = _day(last, first) if (first and len(found) == 2) else first if len(found) == 1 else None
    if not day or day < first:
        return None
    years = {int(year) for year in re.findall(r"\b20\d{2}\b", when_en)}
    if not (re.search(rf"\b{day.day}\b", when_en) and MONTHS[day.month - 1][:3] in when_en) or (years and day.year not in years):
        return None  # the English shown on the site must name the same day and month, and no other year
    time, rest = _time(after)
    if time and not _says(when_en, *time):
        time = None  # the English does not show the same time: keep the day, drop the time
    until = period or "까지" in after[:12] or bool(re.search(RANGE + r"\s*$", before))
    end = None
    if time and until and re.match(r"\s*" + RANGE, rest):
        time = None  # "~ 11. 20.(금) 09:00~18:00": daily hours, not a closing time. Keep the day only.
    if time and not until and re.match(r"\s*" + RANGE, rest):  # "10:00 ~ 16:00" on one day
        end = _time(re.sub(r"^\s*" + RANGE, "", rest))[0]
        if not (end and end > time and _says(when_en, *end)):
            end = None
    return {"day": day, "time": time, "end": end, "period": period, "until": until}


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def _fold(line: str) -> str:
    """Lines of at most 75 bytes, continued with a space, as the format requires."""
    raw, out = line.encode("utf-8"), []
    while len(raw) > 75:
        cut = 75
        while cut and (raw[cut] & 0xC0) == 0x80:  # never split a character
            cut -= 1
        out.append(raw[:cut])
        raw = b" " + raw[cut:]
    out.append(raw)
    return "\r\n".join(part.decode("utf-8") for part in out)


def build(department: str, short: str, site: str) -> tuple[str, dict]:
    """The calendar text and a count of what went in and what was left out."""
    data = ROOT / "data" / department
    notices = json.loads((data / "notices.json").read_text(encoding="utf-8"))
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//SNU Bridge//Deadlines//EN", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
             f"X-WR-CALNAME:{_escape(short + ' deadlines (SNU Bridge)')}", "X-WR-TIMEZONE:Asia/Seoul",
             _fold("X-WR-CALDESC:" + _escape("Dates from the department's notices, translated by AI. Not official. Check the original notice."))]
    count = {"dates": 0, "events": 0, "notices": 0}
    for notice in notices:
        file = data / "briefs" / f"{notice['id']}.json"
        if not file.exists():
            continue
        brief, used = json.loads(file.read_text(encoding="utf-8")), 0
        if brief.get("stale"):
            continue  # the notice changed after this English was written: its dates wait for the new translation
        stamp = brief["written"].replace("-", "") + "T000000Z"  # unchanged between builds unless the notice is translated again
        for date in brief["dates"]:
            count["dates"] += 1
            event = date["verified"] and read(date["original_ko"], date["when"], notice["date"])
            if not event:
                continue
            # the line was written to sit under its notice's title; in a calendar it stands alone, so the title follows it
            day, title = event["day"], ("Last day: " if event["period"] else "") + date["what"] + " · " + brief["title_en"]
            uid = f"{department}-{notice['id']}-{day:%Y%m%d}-{hashlib.sha256((date['original_ko'] + date['what']).encode('utf-8')).hexdigest()[:8]}@snu-bridge"
            if event["time"]:
                at = datetime.datetime(day.year, day.month, day.day, *event["time"], tzinfo=SEOUL).astimezone(datetime.timezone.utc)
                if event["until"]:  # a closing time: a half-hour block that ends at it
                    start, end = at - datetime.timedelta(minutes=30), at
                elif event["end"]:
                    length = datetime.timedelta(hours=event["end"][0] - event["time"][0], minutes=event["end"][1] - event["time"][1])
                    start, end = at, at + length
                else:
                    start, end = at, at + datetime.timedelta(hours=1)
                when = [f"DTSTART:{start:%Y%m%dT%H%M%SZ}", f"DTEND:{end:%Y%m%dT%H%M%SZ}"]
            else:
                when = [f"DTSTART;VALUE=DATE:{day:%Y%m%d}", f"DTEND;VALUE=DATE:{day + datetime.timedelta(days=1):%Y%m%d}"]
            about = "\n".join([brief["title_en"], date["when"], "Korean original: " + date["original_ko"],
                               "Translated by AI. Check the original notice before acting.", f"{site}#notice-{notice['id']}"])
            lines += ["BEGIN:VEVENT", f"UID:{uid}", f"DTSTAMP:{stamp}", *when, _fold("SUMMARY:" + _escape(f"{short}: {title}")),
                      _fold("DESCRIPTION:" + _escape(about)), _fold("URL:" + notice["url"]),
                      "BEGIN:VALARM", "ACTION:DISPLAY", _fold("DESCRIPTION:" + _escape(f"{short}: {title}")),
                      "TRIGGER:" + ("-P1D" if event["time"] else "-PT15H"), "END:VALARM", "END:VEVENT"]
            count["events"] += 1
            used += 1
        count["notices"] += bool(used)
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n", count
