# -*- coding: utf-8 -*-
"""The competition poster, drawn from the site's own data so its figures cannot drift from the site.

    .venv/bin/pip install segno            (QR code; needed for this script only)
    .venv/bin/python tools/poster.py       writes out/poster/poster.html, poster.pdf, poster.png and korean-review.md

Six panels, evidence first (the developer's choice of three drafts): why now, the gap, what it does, how it works,
checked, try it. The gap panel is the tall one and Checked is one short row, at the developer's request.
Board counts cover one closed period (tools/survey.py and tools/evidence.py share it); live counts carry "as of".
The lab logo and the university emblem are read from out/poster/ (lab-logo.png, snu-logo.png), like the author's name,
and each is left out if its file is missing. The emblem is for the poster only: the site must not look official.

Size: 1445 mm wide by 1400 mm high, one page, as the competition asks. The PDF is printed by Google Chrome and then
measured. Everything is text and shapes (no screenshots), so the file stays small enough to email.
The author's name is read from out/poster/author.txt (one line; that folder is not published), never from this file.
Korean lines already on the site come from bridge/text.json; lines written only for the poster are in POSTER_KO below
and are listed in korean-review.md for a Korean reader before the poster is sent.
"""
import datetime
import glob
import html
import json
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from bridge import deadlines  # noqa: E402
OUT = ROOT / "out" / "poster"
SITE = "https://ianyeoh0204.github.io/snubridge/"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
WIDTH_MM, HEIGHT_MM = 1445, 1400
SEOUL = datetime.timezone(datetime.timedelta(hours=9))

# Korean written for the poster only. Not yet read by a Korean speaker.
POSTER_KO = {
    "The 2nd SNU Generative AI Competition": "제2회 서울대학교 생성형 AI 경진대회",
    "One department's graduation requirements and notices, in English, each with its source. Updated daily from the department's own notices.":
        "한 학과의 졸업 요건과 공지를 출처와 함께 영어로 제공합니다. 학과 공지를 바탕으로 매일 갱신됩니다.",
    "Scan to open the site": "QR 코드로 사이트 열기",
    "The university set two directions this year.": "올해 대학은 두 가지 방향을 밝혔습니다.",
    "Internationalisation: the base of all the university's work, not an added project.": "국제화: “대학의 부가적인 사업이 아니라 모든 일의 기반”",
    "AI Native Campus: {n} action plans in education, research, administration and governance.": "AI Native Campus: 교육·연구·행정·거버넌스 분야 실행계획 {n}개",
    "QS rank, 2026 and 2027 editions ({n} in 2025)": "QS 순위, 2026·2027년판 (2025년판 {n}위)",
    "rank for share of international students, 2026 edition": "외국인 학생 비율 지표 순위, 2026년판",
    "international students in Korea, 2026": "2026년 국내 외국인 유학생",
    "Our reading, not the university's: a student who cannot read the department's notices is left out of both.":
        "대학의 입장이 아닌 저희의 해석입니다. 학과 공지를 읽지 못하는 학생은 두 방향 모두에서 소외됩니다.",
    "Sources: President's New Year address; SNU press releases; SNU Alumni Association newspaper; Korea University News; The Korea Herald. Links on the site.":
        "출처: 총장 신년사, 서울대학교 보도자료, 서울대학교총동창신문, 한국대학신문, 코리아헤럴드. 링크는 사이트에 있습니다.",
    "The gap": "격차",
    "The board this site translates, {name}'s academic board: {n} of {m} titles in English.":
        "본 사이트가 번역하는 {name} 학사 게시판: {m}건 가운데 영어 제목 {n}건",
    "–: no English board of its own. Job, scholarship and seminar boards are not counted for any department.":
        "–: 별도 영어 게시판 없음. 취업·장학·세미나 게시판은 어느 학과에서도 집계하지 않았습니다.",
    "A sample of {m} Korean-titled notices was opened: {n} held a line of English, none an English version.":
        "한국어 제목의 공지 {m}건을 표본으로 열어 보았습니다. {n}건에 영어로 된 줄이 있었고, 영어본이 있는 공지는 없었습니다.",
    "{year}: a new undergraduate division for international students, about {n} new students expected.":
        "{year}년: 외국인 대상 학부 신설, 신입생 약 {n}명 예상",
    "Our reading: the notices these students must follow are posted in Korean. AI in administration, an aim of the AI Native Campus, can close that gap.":
        "저희의 해석: 이 학생들이 따라야 할 공지는 한국어로 게시됩니다. AI Native Campus가 지향하는 행정 분야의 AI 활용으로 이 격차를 줄일 수 있습니다.",
    "Sources: News1, 27 April 2026; President's New Year address; SNU Alumni Association newspaper. Links on the site.":
        "출처: 뉴스1(2026년 4월 27일), 총장 신년사, 서울대학교총동창신문. 링크는 사이트에 있습니다.",
    "new notices read and translated": "새 공지를 읽고 번역",
    "Board counts: {from} to {to}. Site figures as of {date}.": "게시판 집계 기간: {from} ~ {to}. 사이트 수치 기준일: {date}.",
    "Korean board": "한국어 게시판",
    "English title": "영어 제목",
    "Korean notices on {n} engineering departments' boards since {date}": "{date} 이후 공과대학 {n}개 학과 게시판의 한국어 공지",
    "have a title in English": "제목이 영어인 공지",
    "This department's academic board since {date}": "{date} 이후 본 학과 학사 게시판",
    "Korean notices": "한국어 공지",
    "posts on the English board": "영문 게시판 게시물",
    "Counted from the public boards. Titles only; method and limits are on the site.": "공개 게시판을 집계했습니다. 제목만 확인했으며, 방법과 한계는 사이트에 있습니다.",
    "What it does": "하는 일",
    "{n} requirements for four programs. Each cites its file, page and Korean line.": "네 개 과정의 요건 {n}개. 항목마다 파일, 쪽, 한국어 원문을 밝힙니다.",
    "{n} notices in English: who must act, dates, conditions, steps, and the full translation.": "영어로 제공하는 공지 {n}건: 조치 대상, 날짜, 조건, 절차, 전문 번역",
    "Source": "출처",
    "page {n}": "{n}쪽",
    "An AI model writes the English. Plain code checks every quoted date against the notice.": "AI 모델이 영어로 옮기고, 인용된 모든 날짜를 코드가 공지 원문과 대조합니다.",
    "A second AI model, from another maker, re-read every requirement against its page.": "개발사가 다른 두 번째 AI 모델이 모든 요건을 해당 쪽과 대조해 다시 읽었습니다.",
    "The site is rebuilt and published. No one's computer is needed.": "사이트를 다시 만들어 게시합니다. 누구의 컴퓨터도 필요하지 않습니다.",
    "Re-read": "재판독",
    "every day": "매일",
    "a notice": "공지 1건당",
    "Claude translates. An OpenAI model, through ChatGPT Edu, re-reads.": "번역은 Claude가, 재판독은 ChatGPT Edu를 통한 OpenAI 모델이 맡습니다.",
    "Checked": "검증",
    "requirements re-read by a second reader": "2차 판독자가 다시 읽은 요건",
    "deliberately wrong entries caught": "일부러 넣은 오류 적발",
    "dates found word for word in the notice": "공지 원문에서 그대로 확인된 날짜",
    "points that could mislead, in ten notices, after the instructions were tightened": "지침을 강화한 뒤, 공지 10건에서 오해를 부를 수 있는 지점",
    "Try it": "직접 해 보기",
    "Choose your program. See what to finish before graduation, and the page each item comes from.": "과정을 고르면 졸업 전에 마쳐야 할 항목과 각 항목의 출처 쪽을 볼 수 있습니다.",
    "Open a notice. Compare its dates with the Korean beside them, then open the original.": "공지를 열어 날짜를 옆의 한국어와 비교하고, 원문을 열어 보세요.",
    "Add the deadlines to your calendar: {n} dated events, each checked against the weekday the notice prints.":
        "마감일을 내 캘린더에 추가해 보세요. 날짜가 있는 일정 {n}건이며, 각각 공지에 적힌 요일과 대조했습니다.",
    "Switch to {name}: another department's notices, added in one day as a pilot.": "{name}(으)로 바꿔 보세요. 하루 만에 시범으로 추가한 다른 학과의 공지입니다.",
    "Where it extends": "확장 방향",
    "Notices: one small reader for each kind of board software. The eleven department sites read use six kinds.": "공지: 게시판 소프트웨어 종류마다 간단한 읽기 프로그램 하나가 필요합니다. 읽어 본 11개 학과 사이트는 여섯 종류를 씁니다.",
    "Requirements: written by hand from each department's documents, then re-read.": "요건: 학과의 공식 문서를 바탕으로 직접 작성한 뒤 다시 읽습니다.",
    "What it does not do": "하지 않는 일",
    "For images and attachments, use ChatGPT Edu. The site does not read them. It does not replace the department office. Translations are made by AI and can be wrong.":
        "이미지와 첨부파일은 ChatGPT Edu를 이용하세요. 본 사이트는 이를 읽지 않습니다. 학과 사무실을 대신하지 않습니다. 번역은 AI가 한 것이며 틀릴 수 있습니다.",
    "requirements to graduate, in {d} departments. Each cites its file, page and Korean line.":
        "{d}개 학과의 졸업 요건입니다. 요건마다 파일, 쪽, 한국어 원문을 밝힙니다.",
    "department notices in English, in {d} departments. Each gives who must act, the dates, the conditions, the steps and the full translation.":
        "{d}개 학과의 공지를 영어로 제공합니다. 공지마다 조치 대상, 날짜, 조건, 절차, 전문 번역을 보여 줍니다.",
    "dates from ECE's notices, ready for your calendar, past ones included. Each matches the weekday the notice prints.":
        "전기·정보공학부 공지의 날짜로, 지난 일정을 포함하며 캘린더에 추가할 수 있습니다. 모두 공지에 적힌 요일과 일치합니다.",
    "Add the notices' dates to your calendar.": "공지의 날짜를 내 캘린더에 추가해 보세요.",
    "Departments post their notices in Korean.": "학과 공지는 한국어로 게시됩니다.",
    "SNU Bridge shows each notice in English.": "SNU Bridge는 각 공지를 영어로 보여 줍니다.",
    "Each graduation requirement shows its source.": "졸업 요건마다 출처를 보여 줍니다.",
    "It runs by itself, once a day.": "하루 한 번, 스스로 실행됩니다.",
    "A second AI and plain code check the first.": "두 번째 AI와 코드가 첫 번째 AI를 검증합니다.",
    "What it does not do yet, and what comes next.": "아직 하지 않는 일과 다음 단계",
    "Notices and graduation requirements of {d} engineering departments, in English, for international students. New notices are translated daily, and every item links to its Korean source.":
        "공과대학 {d}개 학과의 공지와 졸업 요건을 외국인 학생을 위해 영어로 제공합니다. 새 공지는 매일 번역하며, 항목마다 한국어 원문으로 연결됩니다.",
    "The academic board of Electrical and Computer Engineering, {date}.": "전기·정보공학부 학사 게시판, {date}.",
    "{n} notices in English so far, from {d} departments. Each date sits beside its Korean, and each notice links to the original.":
        "지금까지 {d}개 학과의 공지 {n}건을 영어로 제공합니다. 날짜마다 한국어 원문을 함께 보여 주고, 공지마다 원문으로 연결합니다.",
    "ECE's dates can also be added to a calendar.": "전기·정보공학부의 날짜는 캘린더에도 추가할 수 있습니다.",
    "{n} requirements to graduate, in {d} departments, by program and year of entry. Each cites its file, page and Korean line.":
        "{d}개 학과의 졸업 요건 {n}개를 과정과 입학 연도별로 제공합니다. 요건마다 파일, 쪽, 한국어 원문을 밝힙니다.",
    "For images and attachments, use ChatGPT Edu. The site does not read them.": "이미지와 첨부파일은 ChatGPT Edu를 이용하세요. 본 사이트는 이를 읽지 않습니다.",
    "It does not replace the department office. Translations are made by AI and can be wrong.": "학과 사무실을 대신하지 않습니다. 번역은 AI가 한 것이며 틀릴 수 있습니다.",
    "Separate job, scholarship, news and seminar boards are not counted.": "따로 둔 취업·장학·뉴스·세미나 게시판은 집계하지 않았습니다.",
}


# Lines rewritten on 12 Nov 2026 after an outside review (an OpenAI model through Codex, read-only) found no wrong number
# but a dozen lines that made a narrow check look like a broader claim. Not yet read by a Korean speaker.
POSTER_KO.update({
    "A department's graduation requirements and notices, in English, each with its source. New notices are translated daily.":
        "학과의 졸업 요건과 공지를 출처와 함께 영어로 제공합니다. 새 공지는 매일 번역됩니다.",
    "Master's program": "석사과정",
    "of them, English title": "이 중 영어 제목",
    "of them have a title in English": "이 가운데 제목이 영어인 공지",
    "A title counts as English when it has no Korean in it. All {n} are listed on the site, each with its link.":
        "제목에 한글이 없으면 영어 제목으로 셌습니다. {n}건 전체를 링크와 함께 사이트에 실었습니다.",
    "QS 2026 rank for share of international students, as reported by the SNU Alumni Association newspaper":
        "QS 2026년판 외국인 학생 비율 지표 순위 (서울대학교총동창신문 보도)",
    "{n} requirement cards for four ECE programs (undergraduate: {a} to {b} entrants). Each cites its file, page and Korean line.":
        "전기·정보공학부 네 개 과정의 요건 카드 {n}개 (학부: {a}~{b}학번). 카드마다 파일, 쪽, 한국어 원문을 밝힙니다.",
    "{n} ECE academic notices since {date}, in English: who must act, dates, conditions, steps, and the full translation.":
        "{date} 이후 전기·정보공학부 학사 공지 {n}건을 영어로 제공: 조치 대상, 날짜, 조건, 절차, 전문 번역",
    "Requirements, separately": "요건은 별도로",
    "An AI model wrote them once from the official documents, and a second AI model from another maker re-read them once.":
        "AI 모델이 공식 문서를 바탕으로 한 번 작성했고, 개발사가 다른 두 번째 AI 모델이 한 번 다시 읽었습니다.",
    "scheduled check for new notices": "매일 예약된 새 공지 확인",
    "departments read by one automatic job": "하나의 자동 작업이 읽는 학과 수",
    "Claude writes the English. An OpenAI model, from a different maker, re-read every requirement card against the Korean.":
        "영어는 Claude가 작성합니다. 개발사가 다른 OpenAI 모델이 모든 요건 카드를 한국어 원문과 대조해 다시 읽었습니다.",
    "Checks performed": "수행한 확인",
    "requirements, {d} departments, agreed by the second AI reader; {n} settled by the author":
        "{d}개 학과 요건 중 2차 AI 판독자가 동의. {n}개는 작성자가 판단",
    "planted errors caught, in the ECE readings": "전기·정보공학부 판독에서 적발한 일부러 넣은 오류",
    "quoted dates, {d} departments, found word for word in the Korean notice (the quote, not the translation)":
        "{d}개 학과, 한국어 공지에서 그대로 확인된 인용 날짜 (번역이 아닌 인용문 확인)",
    "In ten notices re-read after the instructions were tightened, {n} doubtful points remained.":
        "지침을 강화한 뒤 다시 읽은 공지 10건에서 의심스러운 지점 {n}곳이 남았습니다.",
    "Choose your program and year of entry. See the requirements covered, and the page each comes from.":
        "과정과 입학 연도를 고르면 다루는 요건과 각 요건의 출처 쪽을 볼 수 있습니다.",
    "Add the notices' dates to your calendar. It holds {n} events, past ones included, and each matches the weekday the notice prints.":
        "공지의 날짜를 내 캘린더에 추가해 보세요. 지난 일정을 포함해 {n}건이며, 모두 공지에 적힌 요일과 일치합니다.",
    "Switch department. {names} are here too, with {n} requirements written from their own rules.":
        "학과를 바꿔 보세요. {names}도 있으며, 각 학과의 자체 규정을 바탕으로 요건 {n}개를 작성했습니다.",
    "Notices need a small reader for each kind of board software. Translation and publishing are reused.":
        "공지에는 게시판 소프트웨어 종류마다 간단한 읽기 프로그램이 필요합니다. 번역과 게시는 그대로 다시 씁니다.",
    "Requirements: written from each department's own documents, then re-read.": "요건: 각 학과의 공식 문서를 바탕으로 작성한 뒤 다시 읽습니다.",
})


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


TEXT = load("bridge/text.json")["pairs"]
used_new, missing = [], []


def fill(text, values):
    for key, value in (values or {}).items():
        text = text.replace("{" + key + "}", str(value))
    return text


def bi(english, values=None, korean_values=None, tag="span"):
    """An English line with its Korean beneath. Korean comes from the site where the sentence exists there.
    A line with no Korean yet is drawn in English only and listed, so a draft can be judged before it is translated."""
    korean = TEXT.get(english) or POSTER_KO.get(english)
    if english not in TEXT and english in POSTER_KO and english not in used_new:
        used_new.append(english)
    if not korean:
        if english not in missing:
            missing.append(english)
        return f'<{tag}>{html.escape(fill(english, values))}</{tag}>'
    ko_values = dict(values or {}, **(korean_values or {}))
    return f'<{tag}>{html.escape(fill(english, values))}<small class="ko" lang="ko">{html.escape(fill(korean, ko_values))}</small></{tag}>'


def num(n):
    return f"{n:,}"


def day(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B')} {d.year}", f"{d.year}년 {d.month}월 {d.day}일"


def bar(title, crit):
    return f'<div class="bar">{bi(title)}<em>{html.escape(crit)}</em></div>'


def fig(big, caption, small=""):
    return f'<div class="fig"><b>{big}{f"<i>{small}</i>" if small else ""}</b><p>{caption}</p></div>'


# Three layouts. The developer compared them on 14 Nov 2026 and chose "equal": the judges read Korean, so every Korean
# line is the size of the English above it, and a lower blue band pays for the room. `python tools/poster.py` draws it
# as out/poster/poster.*. The other two are kept to compare (`python tools/poster.py first` or `balanced`, written to
# out/poster/poster-<name>.*): "first" is the tall band with small Korean, "balanced" has Korean at 85% of the English.
LOWER_BAND = """
.band { height: 196mm; padding: 22mm 44mm 0; grid-template-columns: 1fr auto; }
.band h1 { margin: 3mm 0 8mm -1mm; font-size: 96mm; }
.band .tag { max-width: none; font-size: 15mm; }
.band aside { display: grid; grid-template-columns: 270mm 150mm; grid-template-rows: auto auto 1fr; gap: 4mm 8mm; text-align: right; }
.band aside svg { grid-column: 2; grid-row: 1 / span 3; width: 150mm; height: 150mm; }
.band aside p { grid-column: 1; }
.grid { height: 1092mm; }
.foot { height: 98mm; }
.foot .logo { height: 80mm; }
.col.mid .panel:first-child { flex: 4.6 1 0; }
.drow { grid-template-columns: 200mm minmax(0, 1fr) 62mm; font-size: 11.6mm; }
.drow:not(.own):not(.head) { padding: 2.4mm 0; }
.drow .dbar b, .drow u { font-size: 12.4mm; }
.drow.head, .drow.head u, .drow.head .ko { font-size: 9.6mm !important; }
.bar .ko { display: inline; margin-left: 5mm; }
"""
CHOSEN = "equal"
LAYOUTS = {
    "first": "",
    "equal": LOWER_BAND + """
.ko, .drow .dn small, .mock td small, .mock .kotitle { font-size: 1em !important; line-height: 1.24; }
.col:first-child .panel:first-child { flex: 1.11 1 0; }
.steps li { padding: 3.6mm 0; }
.foot { grid-template-columns: 1.6fr 1.15fr auto auto; }
""",
    "product": "",  # filled in below: the chosen layout plus its own rules
    "talk": "",
    "balanced": LOWER_BAND + """
.ko, .mock .kotitle { font-size: max(.85em, 9.2mm) !important; line-height: 1.26; }
.drow .dn small, .mock td small, .drow.head .ko, .band aside .ko { font-size: max(.85em, 8.6mm) !important; }
""",
}


# "product" (to compare, 14 Nov 2026): the developer found the requirements, the notices and the calendar hard to find
# on the poster, and the missing English notices overstated. Here "What it does" is the tall panel, on the right, with
# one large number and one example for each of the three, and "The gap" is an ordinary panel. The top row reads
# Why now, The gap, What it does; the bottom row How it works, Try it, Checks performed.
LAYOUTS["product"] = LAYOUTS["equal"] + """
.col.mid .panel:first-child { flex: 1.85 1 0; }
.col:last-child .panel:first-child { flex: 4.6 1 0; }
.col:last-child .panel:first-child .body { gap: 6mm; }
.does .figs.rows .fig { grid-template-columns: 138mm minmax(0, 1fr); padding: 4mm 6mm; }
.does .figs.rows .fig b { font-size: 54mm; }
.does .figs.rows .fig p { font-size: 12.6mm; line-height: 1.2; }
.does .mock h4 { font-size: 16mm; }
.does .mock .key { font-size: 14.5mm; }
.does .mock .src, .does .mock .meta, .does .mock .kotitle { font-size: 11mm; }
.does .mock table { font-size: 11.4mm; }
.small-gap .heropair b { font-size: 48mm; }
.small-gap .drow { grid-template-columns: 190mm minmax(0, 1fr) 50mm; font-size: 10.6mm; }
.small-gap .drow:not(.own):not(.head) { padding: 1.7mm 0; }
.small-gap .drow.own { padding: 1.6mm 3mm; }
.small-gap .stand { font-size: 12.4mm; padding: 4mm 6mm; }
"""


# "talk" (to compare, 14 Nov 2026): the developer said the poster looked nice but did not help to explain the project,
# and a reader with no history agreed: there was no picture of the site on it. Here each panel is headed by a sentence
# the presenter says and holds one thing to point at: the department's Korean board, the same notice in English, a
# requirement with its source (three real screenshots from tools/poster_shots.py), the daily flow, the checks, the limits.
LAYOUTS["talk"] = LAYOUTS["equal"] + """
.bar { font-size: 15.5mm; }
.bar .ko { display: block; margin: 1.5mm 0 0; font-size: 12.5mm !important; }
.col .panel, .col.mid .panel:first-child, .col:first-child .panel:first-child { flex: 0 0 auto; }
.col .panel:last-child { flex: 1 1 0; }
.body { justify-content: flex-start; gap: 7mm; }
.shot { overflow: hidden; border: .6mm solid #000; }
.shot img { display: block; width: 100%; }
.shot.board { aspect-ratio: 662 / 384; }
.shot.notice { aspect-ratio: 600 / 782; }
.shot.card { aspect-ratio: 600 / 600; }
.shot.board img { width: 166.2%; margin: -94.6% 0 0 -41.2%; }
.cap2 { font-size: 13.4mm; line-height: 1.24; }
.where { font-size: 9.6mm; color: #444; margin-top: -4mm; }
.heropair b { font-size: 50mm; }
.flow { list-style: none; }
.flow li { position: relative; margin-bottom: 13mm; padding: 5mm 7mm 6mm; border: .7mm solid #000; }
.flow li:last-child { margin-bottom: 0; border-style: dashed; }
.flow li:nth-child(-n+2)::after { content: ""; position: absolute; left: 50%; bottom: -11.5mm; margin-left: -8mm; border: 8mm solid transparent; border-top: 9mm solid #002c84; border-bottom: 0; }
.foot { grid-template-columns: 1fr auto auto; }
.foot div:first-child { display: none; }
.foot div:nth-child(2) { text-align: left; }
.checks .figs.rows .fig { grid-template-columns: 150mm minmax(0, 1fr); padding: 4mm 6mm; }
.checks .figs.rows .fig b { font-size: 44mm; }
.checks .figs.rows .fig p { font-size: 12.8mm; line-height: 1.22; }
.limits li { padding: 6mm 0; font-size: 14mm; line-height: 1.24; }
.flow h4 { font-size: 17mm; }
.flow p { font-size: 13mm; }
.flow li b { font-size: 36mm; }
.checks .stand { font-size: 14mm; }
"""


def build(variant=CHOSEN):
    import segno

    used_new.clear(), missing.clear()
    ece, aero = load("sources/ECE/config.json"), load("sources/AEROSPACE/config.json")
    cards, audit = load("data/ECE/cards.json"), load("data/ECE/audit.json")
    notices = load("data/ECE/notices.json")
    survey, context = load("data/survey.json"), load("sources/context.json")
    briefs = [json.loads(pathlib.Path(f).read_text(encoding="utf-8")) for f in glob.glob(str(ROOT / "data/ECE/briefs/*.json"))]
    dates = [d for b in briefs for d in b["dates"]]
    all_dates = [d for f in glob.glob(str(ROOT / "data/*/briefs/*.json")) for d in json.loads(pathlib.Path(f).read_text(encoding="utf-8"))["dates"]]
    reread = sum(1 for c in audit["cards"].values() if c["status"] != "open")
    caught = sum(1 for v in audit["decoys"].values() if v == "caught")
    mislead = lambda group: sum(sum(n["could_mislead"].values()) for n in audit.get(group, {}).values())
    f, totals = context["figures"], survey["totals"]
    today = datetime.datetime.now(SEOUL).date().isoformat()
    calendar = deadlines.build("ECE", ece["short"], ece["site"])[1]  # the same count the site shows
    # the other departments that have requirement cards, as the site lists them
    others = [dict(load(f"sources/{f.parent.name}/config.json"), cards=len(load(f"data/{f.parent.name}/cards.json")))
              for f in sorted((ROOT / "data").glob("*/cards.json")) if f.parent.name != "ECE"]
    author = (OUT / "author.txt").read_text(encoding="utf-8").strip() if (OUT / "author.txt").exists() else ""
    since, until = day(survey["since"]), day(survey["until"])
    period = bi("{from} to {to}", {"from": since[0], "to": until[0]}, {"from": since[1], "to": until[1]})

    # One real requirement and one real notice, redrawn as the site shows them. The requirement is one whose every number
    # can be seen in the Korean line quoted beside it, so the example shows what it claims to show.
    digits = lambda text: set(re.findall(r"\d+(?:\.\d+)?", text))
    shown = [c for c in cards if "masters" in c["programs"] and digits(c["key"]) and digits(c["key"]) <= digits(c["source_quote_ko"])]
    card = next((c for c in shown if c["id"] == ece["headline_cards"]["masters"]), shown[0])
    source = next(s for s in ece["files"] if s["file"] == card["source_file"])
    newest = next(b for n in notices for b in briefs if b["id"] == n["id"] and len(b["dates"]) >= 2)
    notice = next(n for n in notices if n["id"] == newest["id"])
    rows = sorted((d for d in newest["dates"] if d["verified"]), key=lambda d: len(d["what"]))[:2]
    qr = segno.make(SITE, error="m").svg_inline(omitsize=True, border=2, dark="#000", light="#fff")

    program = bi("Master's program")
    requirement = (f'<div class="mock"><p class="meta">{program}</p><h4>{html.escape(card["title"])}</h4><p class="key">{html.escape(card["key"])}</p>'
                   f'<p class="src">{bi("Source")}: {html.escape(source["name"])}, {fill("page {n}", {"n": card["source_page"]})} · <span lang="ko">{html.escape(card["source_quote_ko"])}</span></p></div>')
    date_rows = "".join(f'<tr><td>{html.escape(d["what"])}</td><td>{html.escape(d["when"])}<small lang="ko">{html.escape(d["original_ko"])}</small></td></tr>' for d in rows)
    translated = (f'<div class="mock"><p class="meta">{notice["date"]}</p><h4>{html.escape(newest["title_en"])}</h4><p class="kotitle" lang="ko">{html.escape(notice["title_ko"])}</p>'
                  f'<table>{date_rows}</table><p class="src">{bi("Original notice")} →</p></div>')

    # The departments, largest first, this site's own marked. One period. Each column is one plain count: notices on the
    # Korean boards, how many of those have an English title, and posts on the department's own English board.
    # (An earlier draft added the two boards into one "English" figure; a reviewer showed it read as a share of the first.)
    most = max(d["korean"] for d in survey["departments"])
    def drow(d):
        mark = mark_ko = ""  # the developer: no "(this site)" after the department's name; the row is highlighted instead
        # the English side is one number in every row: posts on the department's separate English board. A department
        # without one counts 0 (Computer Science and Civil show the Korean board's own notices under their English menu,
        # checked live for Computer Science on 13 Nov 2026; Naval has no English site). The site says which these are.
        board = num(d["english_posts"] or 0)
        return (f'<div class="drow {"own" if d["this_site"] else ""}"><span class="dn">{html.escape(d["name"] + mark)}<small lang="ko">{html.escape(d["name_ko"] + mark_ko)}</small></span>'
                f'<span class="dbar"><i style="width:{74 * d["korean"] / most:.1f}%"></i><b>{num(d["korean"])}</b></span><u>{board}</u></div>')
    chart = ('<div class="chart"><div class="drow head"><span></span>' + bi("Korean board") + bi("Separate English board posts", tag="u") + "</div>"
             + "".join(drow(d) for d in sorted(survey["departments"], key=lambda d: -d["korean"])) + "</div>")
    heropair = (f'<div class="heropair"><div><b>{num(totals["korean"])}</b><p>' + bi("notices on the Korean boards of {n} engineering departments", {"n": len(survey["departments"])}) + "</p></div>"
                f'<div><b class="blue">{num(totals["english_titled"])}</b><p>{bi("of them have a title in English")}</p></div></div>')
    silent = min((d for d in survey["departments"] if d["english_side"] == "separate" and not d["english_posts"]), key=lambda d: d["english_last_post"])
    korean_only = max((d for d in survey["departments"] if d["english_posts"] and not d["english_posts_titled"]), key=lambda d: d["english_posts"])
    english_boards = bi("The {k} separate English boards had {n} posts in the same period, {m} with an English title.",
                        {"k": totals["english_boards"], "n": totals["english_posts"], "m": totals["english_posts_titled"]})
    last = datetime.date.fromisoformat(silent["english_last_post"])
    boards_line = bi("{a}'s English board last had a post in {month} {year}. {b}'s has {n} posts, all with Korean titles.",
                     {"a": silent["name"], "month": last.strftime("%B"), "year": last.year, "b": korean_only["name"], "n": korean_only["english_posts"]},
                     {"a": silent["name_ko"], "month": last.month, "b": korean_only["name_ko"]})
    legend = bi("Separate job, scholarship, news and seminar boards are not counted.")
    counted = f'<p class="note">{legend}</p><p class="note">' + bi("A title counts as English when it has no Korean in it. All {n} are listed on the site, each with its link.", {"n": totals["english_titled"]}) + "</p>"

    funded = bi("In 2026 the university put {won} billion won into {n} colleges and schools to recruit international students and help them settle.",
                {"won": f["college_fund_billion_won"], "n": f["colleges_funded"]}, {"won": 10 * f["college_fund_billion_won"]})  # 1 billion won is 10억 원
    division = bi("A new undergraduate division for international students is planned for September {year}, with about {n} entrants expected.",
                  {"year": f["new_division_year"], "n": f["new_division_students"]})
    reading = bi("This is our reading. The notices these students must follow are posted in Korean, and AI in administration, an aim of the AI Native Campus, can put them into English.")
    why_figs = '<div class="figs rows">' + fig(num(f["qs_student_ratio_rank"]), bi("QS 2026 rank for share of international students, as reported by the SNU Alumni Association newspaper")) + "</div>"
    why = ('<div class="body">' + f'<p class="lead">{bi("SNU is working to bring in more international students.")}</p>'
           + f'<ul class="rule"><li>{funded}</li><li>{division}</li><li>' + bi("In his 2026 address the President said internationalisation must be the base of all the university's work.") + "</li></ul>"
           + why_figs + f'<p class="stand">{reading}</p>'
           + '<p class="note">' + bi("Sources: News1, 27 April 2026; President's New Year address; SNU Alumni Association newspaper. Links on the site.") + "</p></div>")

    gap = f'<div class="body"><p class="period">{period}</p>{heropair}{chart}<p class="stand">{english_boards}</p><p class="cap">{boards_line}</p><div>{counted}</div></div>'

    years = sorted({y for c in cards for y in (c.get("entry_years") or [])})
    covered = day(ece["board"]["since"])
    line_req = bi("{n} requirement cards for four ECE programs (undergraduate: {a} to {b} entrants). Each cites its file, page and Korean line.",
                  {"n": len(cards), "a": years[0], "b": years[-1]})
    line_notices = bi("{n} ECE academic notices since {date}, in English: who must act, dates, conditions, steps, and the full translation.",
                      {"n": len(notices), "date": covered[0]}, {"date": covered[1]})
    does = f'<div class="body"><p>{line_req}</p>{requirement}<p>{line_notices}</p>{translated}</div>'

    step = lambda n, title, text: f'<li><b>{n}</b><h4>{bi(title)}</h4><p>{text}</p></li>'
    steps = ('<ol class="steps">' + step(1, "Collect", bi("Once a day a scheduled job reads the department's Korean board."))
             + step(2, "Translate", bi("An AI model writes the English. Plain code checks every quoted date against the notice."))
             + step(3, "Publish", bi("GitHub rebuilds and publishes the site, without the developer's laptop."))
             + step("+", "Requirements, separately", bi("An AI model wrote them once from the official documents, and a second AI model from another maker re-read them once.")) + "</ol>")
    # the point of this panel is that the flow runs by itself, so the second figure is how much it covers, not what it costs
    daily, cost = fig(html.escape("Daily"), bi("scheduled check for new notices")), fig(len(others) + 1, bi("departments read by one automatic job"))
    who = f'<p class="stand">{bi("Claude writes the English. An OpenAI model, from a different maker, re-read every requirement card against the Korean.")}</p>'
    how = f'<div class="body">{steps}<div class="figs two">{daily}{cost}</div>{who}</div>'

    # every department's cards and its second reading (data/<DEPARTMENT>/audit.json)
    audits = [json.loads(f.read_text(encoding="utf-8"))["cards"] for f in sorted((ROOT / "data").glob("*/audit.json"))]
    all_cards = sum(len(load(f"data/{f.parent.name}/cards.json")) for f in (ROOT / "data").glob("*/cards.json"))
    agreed = sum(1 for a in audits for c in a.values() if c["status"] == "reader_agrees")
    settled = sum(1 for a in audits for c in a.values() if c["status"] == "settled_by_author")
    if agreed + settled != all_cards:
        sys.exit(f"{all_cards} cards but {agreed + settled} have a second reading on record.")
    checks = [fig(agreed, bi("requirements, {d} departments, agreed by the second AI reader; {n} settled by the author", {"n": settled, "d": len(audits)}), f"of {all_cards}"),
              fig(caught, bi("planted errors caught, in the ECE readings"), f"of {len(audit['decoys'])}"),
              fig(num(sum(d["verified"] for d in all_dates)), bi("quoted dates, {d} departments, found word for word in the Korean notice (the quote, not the translation)", {"d": len(audits)}), f"of {num(len(all_dates))}")]
    checked = f'<div class="body"><div class="figs three even">{"".join(checks)}</div></div>'

    tries = [bi("Choose your program and year of entry. See the requirements covered, and the page each comes from."),
             bi("Open a notice. Compare its dates with the Korean beside them, then open the original."),
             bi("Add the notices' dates to your calendar. It holds {n} events, past ones included, and each matches the weekday the notice prints.", {"n": calendar["events"]}),
             bi("Switch department. {names} are here too, with {n} requirements written from their own rules.",
                {"names": " and ".join([", ".join(o["short"] for o in others[:-1]), others[-1]["short"]]) + " Engineering", "n": sum(o["cards"] for o in others)},
                {"names": ", ".join(o["department_ko"] for o in others)})]
    try_list = '<ol class="try">' + "".join(f'<li><b>{i}</b><p>{t}</p></li>' for i, t in enumerate(tries, 1)) + "</ol>"
    extends = (f'<h5>{bi("Where it extends")}</h5>'
               + f'<p class="small">{bi("Notices need a small reader for each kind of board software. Translation and publishing are reused.")}</p>')
    try_it = f'<div class="body">{try_list}{extends}</div>'

    if variant == "product":
        # the example requirement: the master's headline card, with the rule line whose every number is in its Korean quote
        head = next(c for c in cards if c["id"] == ece["headline_cards"]["masters"])
        line = next(r for r in head["rule"] if digits(r) and digits(r) <= digits(head["source_quote_ko"]))
        head_source = next(x for x in ece["files"] if x["file"] == head["source_file"])
        example = (f'<div class="mock"><p class="meta">{program}</p><h4>{html.escape(head["title"])}</h4><p class="key">{html.escape(line)}</p>'
                   f'<p class="src">{bi("Source")}: {html.escape(head_source["name"])}, {fill("page {n}", {"n": head["source_page"]})} · <span lang="ko">{html.escape(head["source_quote_ko"])}</span></p></div>')
        translated_all = sum(1 for d in sorted((ROOT / "data").glob("*/notices.json")) for n in json.loads(d.read_text(encoding="utf-8"))
                             if (d.parent / "briefs" / f"{n['id']}.json").exists())
        row = lambda big, caption: f'<div class="figs rows">{fig(num(big), caption)}</div>'
        does = ('<div class="body does">'
                + row(all_cards, bi("requirements to graduate, in {d} departments. Each cites its file, page and Korean line.", {"d": len(audits)})) + example
                + row(translated_all, bi("department notices in English, in {d} departments. Each gives who must act, the dates, the conditions, the steps and the full translation.", {"d": len(audits)})) + translated
                + row(calendar["events"], bi("dates from ECE's notices, ready for your calendar, past ones included. Each matches the weekday the notice prints."))
                + f"<div>{extends}</div></div>")
        gap = (f'<div class="body small-gap"><p class="period">{period}</p>{heropair}{chart}<p class="stand">{english_boards}</p><p class="note">'
               + bi("A title counts as English when it has no Korean in it. All {n} are listed on the site, each with its link.", {"n": totals["english_titled"]}) + "</p></div>")
        tries[2] = bi("Add the notices' dates to your calendar.")
        try_list = '<ol class="try">' + "".join(f'<li><b>{i}</b><p>{t}</p></li>' for i, t in enumerate(tries, 1)) + "</ol>"
        try_it = f'<div class="body">{try_list}</div>'
    tagline = bi("A department's graduation requirements and notices, in English, each with its source. New notices are translated daily.")
    foot_left = f'<b>{bi("What it does not do")}</b>' + bi("For images and attachments, use ChatGPT Edu. The site does not read them. It does not replace the department office. Translations are made by AI and can be wrong.")
    if variant == "talk":
        shots = OUT / "shots"
        if not all((shots / f"{name}.png").exists() for name in ("board", "notice", "card")):
            sys.exit("The screenshots are missing: run tools/poster_shots.py first.")
        shot = lambda name: f'<div class="shot {name}"><img src="shots/{name}.png" alt=""></div>'
        translated_all = sum(1 for d in sorted((ROOT / "data").glob("*/notices.json")) for n in json.loads(d.read_text(encoding="utf-8"))
                             if (d.parent / "briefs" / f"{n['id']}.json").exists())
        taken = day(datetime.date.fromtimestamp((shots / "board.png").stat().st_mtime).isoformat())
        tagline = bi("Notices and graduation requirements of {d} engineering departments, in English, for international students. New notices are translated daily, and every item links to its Korean source.", {"d": len(audits)})
        p1 = ('<div class="body">' + shot("board") + f'<p class="where">{bi("The academic board of Electrical and Computer Engineering, {date}.", {"date": taken[0]}, {"date": taken[1]})}</p>'
              + heropair + f'<p class="where">{period}</p>'
              + f'<p class="cap2">{bi("SNU is working to bring in more international students.")}</p><p class="cap2">{funded}</p></div>')
        p2 = ('<div class="body">' + shot("notice")
              + f'<p class="cap2">{bi("{n} notices in English so far, from {d} departments. Each date sits beside its Korean, and each notice links to the original.", {"n": translated_all, "d": len(audits)})}</p>'
              + '<p class="cap2">' + bi("ECE's dates can also be added to a calendar.") + "</p></div>")
        p3 = ('<div class="body">' + shot("card")
              + f'<p class="cap2">{bi("{n} requirements to graduate, in {d} departments, by program and year of entry. Each cites its file, page and Korean line.", {"n": all_cards, "d": len(audits)})}</p></div>')
        p4 = '<div class="body">' + steps.replace('<ol class="steps">', '<ol class="steps flow">') + "</div>"
        p5 = ('<div class="body checks"><div class="figs rows">' + "".join(checks) + f"</div>{who}</div>")
        p6 = ('<div class="body"><ul class="rule limits">'
              + f'<li>{bi("For images and attachments, use ChatGPT Edu. The site does not read them.")}</li>'
              + f'<li>{bi("It does not replace the department office. Translations are made by AI and can be wrong.")}</li>'
              + f'<li>{bi("Notices need a small reader for each kind of board software. Translation and publishing are reused.")}</li></ul></div>')
        foot_left = ""
    columns = [[bar("Departments post their notices in Korean.", "1") + p1, bar("It runs by itself, once a day.", "4") + p4],
               [bar("SNU Bridge shows each notice in English.", "2") + p2, bar("What it does not do yet, and what comes next.", "5") + p6],
               [bar("Each graduation requirement shows its source.", "3") + p3, bar("A second AI and plain code check the first.", "6") + p5]] if variant == "talk" else [[bar("Why now", "1") + why, bar("How it works", "4") + how],
               [bar("The gap", "2") + gap, bar("Try it", "5") + try_it],
               [bar("What it does", "3") + does, bar("Checks performed", "6") + checked]] if variant == "product" else [[bar("Why now", "1") + why, bar("How it works", "4") + how],
               [bar("The gap", "2") + gap, bar("Checks performed", "5") + checked],
               [bar("What it does", "3") + does, bar("Try it", "6") + try_it]]
    grid = "".join(f'<div class="col{" mid" if i == 1 else ""}">' + "".join(f'<section class="panel">{p}</section>' for p in column) + "</div>"
                   for i, column in enumerate(columns))
    # both marks are read from out/poster/ (not published) and left out if the file is missing
    logo = "".join(f'<img class="logo" src="{name}" alt="">' for name in ("snu-logo.png", "lab-logo.png") if (OUT / name).exists())

    stamp = day(today)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>SNU Bridge poster</title>
<style>
@page {{ size: {WIDTH_MM}mm {HEIGHT_MM}mm; margin: 0; }}
* {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
html, body {{ margin: 0; width: {WIDTH_MM}mm; height: {HEIGHT_MM}mm; overflow: hidden; }}
body {{ font: 400 12.6mm/1.26 "Helvetica Neue", Helvetica, "Apple SD Gothic Neo", Arial, sans-serif; color: #000; background: #fff; }}
p, h1, h4, h5, ul, ol {{ margin: 0; padding: 0; }}
.ko {{ display: block; margin-top: 1.2mm; font-size: 9.2mm; font-weight: 400; line-height: 1.32; letter-spacing: 0; color: #555; text-transform: none; }}
.blue {{ color: #002c84; }}
.band {{ height: 300mm; padding: 34mm 44mm 0; display: grid; grid-template-columns: 1fr 230mm; gap: 50mm; background: #002c84; color: #fff; }}
.band .ko, .bar .ko, .stand .ko {{ color: inherit; opacity: .8; }}
.band .eyebrow {{ font-size: 13mm; font-weight: 500; }}
.band .eyebrow .ko {{ display: inline; margin-left: 5mm; font-size: 10mm; }}
.band h1 {{ margin: 6mm 0 12mm -1mm; font-size: 138mm; font-weight: 700; line-height: .9; letter-spacing: -.045em; }}
.band .tag {{ max-width: 1010mm; font-size: 17.5mm; line-height: 1.22; }}
.band .tag .ko {{ font-size: 11.5mm; margin-top: 3mm; }}
.band aside {{ display: flex; flex-direction: column; gap: 5mm; font-size: 9.5mm; line-height: 1.25; }}
.band aside svg {{ display: block; width: 168mm; height: 168mm; background: #fff; }}
.band aside .ko {{ font-size: 8.6mm; }}
.who {{ position: absolute; left: 44mm; top: 34mm; }}
.grid {{ height: 1000mm; padding: 28mm 44mm 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); grid-template-rows: repeat(2, minmax(0, 1fr)); gap: 24mm 26mm; }}
.panel {{ display: flex; flex-direction: column; min-height: 0; border-bottom: 1.2mm solid #000; }}
.bar {{ display: flex; justify-content: space-between; align-items: flex-start; padding: 6mm 9mm 7mm; background: #000; color: #fff; font-size: 17mm; font-weight: 700; line-height: 1.1; }}
.bar em {{ font-style: normal; font-weight: 400; opacity: .7; }}
.body {{ flex: 1; min-height: 0; padding: 10mm 10mm 9mm; display: flex; flex-direction: column; justify-content: space-between; gap: 6mm; border-left: .5mm solid #000; border-right: .5mm solid #000; }}
.lead {{ font-size: 16mm; font-weight: 700; line-height: 1.15; }}
.rule {{ list-style: none; border-top: .5mm solid #000; }}
.rule li {{ padding: 4.5mm 0; border-bottom: .3mm solid #bbb; }}
.figs {{ display: grid; gap: 0; border-left: .5mm solid #000; }}
.figs.three {{ grid-template-columns: minmax(0, .8fr) minmax(0, .9fr) minmax(0, 1.4fr); }}
.figs.two {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
.figs.two:not(.tall) .fig b {{ font-size: 46mm; }}
.fig {{ padding: 4mm 6mm 5mm; border-right: .5mm solid #000; border-top: .5mm solid #000; border-bottom: .5mm solid #000; }}
.figs.tall .fig:nth-child(n+3) {{ border-top: 0; }}
.fig b {{ display: block; font-size: 45mm; font-weight: 700; line-height: 1; letter-spacing: -.035em; color: #002c84; white-space: nowrap; }}
.figs.tall {{ flex: 1; grid-auto-rows: 1fr; }}
.figs.tall .fig {{ display: flex; flex-direction: column; justify-content: center; }}
.figs.tall .fig b {{ font-size: 76mm; }}
.figs.tall .fig p {{ font-size: 11.5mm; }}
.fig b i {{ margin-left: 3mm; font-style: normal; font-size: .3em; font-weight: 400; letter-spacing: 0; color: #000; }}
.fig p {{ margin-top: 3mm; font-size: 10.4mm; line-height: 1.22; }}
.stand {{ padding: 6mm 8mm; background: #002c84; color: #fff; font-size: 13.4mm; font-weight: 700; line-height: 1.2; }}
.stand .ko {{ font-weight: 400; }}
.note {{ font-size: 9.2mm; line-height: 1.3; color: #333; }}
.hero b {{ display: block; font-size: 150mm; font-weight: 700; line-height: .88; letter-spacing: -.045em; color: #002c84; }}
.hero b i {{ margin-left: 5mm; font-style: normal; font-size: .26em; font-weight: 400; letter-spacing: 0; color: #000; }}
.track {{ height: 15mm; background: #000; }}
.track i {{ display: block; height: 100%; min-width: 1.4mm; background: #6f9bff; outline: .6mm solid #fff; }}
.cap {{ margin-top: -3mm; font-weight: 700; }}
.sub {{ margin-top: 3mm; padding-top: 6mm; border-top: .5mm solid #000; font-weight: 700; }}
.pair {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10mm; }}
.pair b {{ display: block; font-size: 60mm; line-height: 1; letter-spacing: -.035em; }}
.pair .track {{ margin-top: 4mm; height: 9mm; }}
.pair .track.full {{ background: #000; }}
.pair div:last-child .track {{ background: #ddd; }}
.pair div:last-child .track i {{ background: #002c84; outline: 0; }}
.mock {{ padding: 6mm 8mm; border: .5mm solid #000; border-left: 3mm solid #002c84; }}
.mock h4 {{ font-size: 14.5mm; line-height: 1.15; }}
.mock .key {{ margin-top: 1.5mm; font-size: 13mm; color: #002c84; font-weight: 700; }}
.mock .src, .mock .meta, .mock .kotitle {{ margin-top: 2.5mm; font-size: 9.4mm; color: #444; }}
.mock .src .ko {{ display: inline; margin-left: 2mm; }}
.mock table {{ width: 100%; margin-top: 3mm; border-collapse: collapse; font-size: 9.8mm; line-height: 1.22; }}
.mock td {{ width: 50%; padding: 2.5mm 4mm 2.5mm 0; border-top: .3mm solid #999; vertical-align: top; }}
.mock td small {{ display: block; margin-top: 1mm; color: #555; font-size: 9mm; }}
.steps, .try {{ list-style: none; display: grid; gap: 0; border-top: .5mm solid #000; }}
.steps li, .try li {{ display: grid; grid-template-columns: 20mm minmax(0, 1fr); column-gap: 6mm; padding: 4.6mm 0; border-bottom: .3mm solid #bbb; }}
.steps li b, .try li b {{ grid-row: span 2; font-size: 32mm; line-height: .95; color: #002c84; }}
.steps h4 {{ font-size: 15mm; line-height: 1.1; }}
.steps h4 .ko {{ display: inline; margin-left: 3mm; }}
.steps p {{ margin-top: 1.5mm; font-size: 11.4mm; line-height: 1.22; }}
.try li {{ padding: 3.9mm 0 !important; }}
.try li p {{ font-size: 15mm; line-height: 1.2; }}
.try li .ko {{ font-size: 10.4mm; }}
h5 {{ margin-top: 2mm; padding-top: 6mm; border-top: .5mm solid #000; font-size: 15mm; }}
h5 .ko {{ display: inline; margin-left: 3mm; }}
.small {{ font-size: 12.6mm; line-height: 1.24; }}
.foot {{ height: 72mm; margin: 0 44mm; padding-top: 9mm; display: grid; grid-template-columns: 2fr 1fr; gap: 26mm; font-size: 10.4mm; line-height: 1.26; }}
.foot b {{ display: block; margin-bottom: 1.5mm; font-size: 11.5mm; }}
.foot b .ko {{ display: inline; margin-left: 3mm; }}
.foot div:last-child {{ text-align: right; color: #333; }}
.period {{ font-size: 13mm; font-weight: 700; }}
.heropair {{ display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); gap: 8mm; }}
.heropair b {{ display: block; font-size: 56mm; font-weight: 700; line-height: .95; letter-spacing: -.04em; }}
.heropair p {{ margin-top: 2mm; font-size: 11mm; line-height: 1.2; }}
.chart {{ border-top: .5mm solid #000; }}
.drow {{ display: grid; grid-template-columns: 176mm minmax(0, 1fr) 62mm; column-gap: 5mm; align-items: center; padding: 1.6mm 0; border-bottom: .3mm solid #bbb; font-size: 10.2mm; line-height: 1.12; }}
.drow .dn small {{ display: block; margin-top: .6mm; font-size: 8.6mm; color: #555; }}
.drow .dbar {{ display: flex; align-items: center; gap: 3mm; }}
.drow .dbar i {{ display: block; height: 9mm; background: #000; }}
.drow .dbar b {{ font-size: 10.6mm; }}
.drow em {{ font-style: normal; font-weight: 700; font-size: 15mm; color: #002c84; text-align: right; }}
.drow u {{ text-decoration: none; font-size: 11mm; text-align: right; color: #333; }}
.drow.head {{ align-items: end; font-size: 8.6mm; color: #333; }}
.drow.head em {{ font-size: 8.6mm; font-weight: 400; color: #002c84; line-height: 1.12; white-space: nowrap; justify-self: end; }}
.drow.head u {{ font-size: 8.6mm; line-height: 1.12; white-space: nowrap; justify-self: end; }}
.drow.head .ko {{ display: block; margin: 0; font-size: 8.6mm; word-break: keep-all; }}
.drow.own {{ margin: 0 -3mm; padding: 2.6mm 3mm; background: #002c84; color: #fff; border-bottom: 0; }}
.drow.own .dn small, .drow.own em, .drow.own u {{ color: #fff; }}
.drow.own .dbar i {{ background: #fff; }}
.grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); grid-template-rows: minmax(0, 1fr); }}
.col {{ display: flex; flex-direction: column; gap: 24mm; min-height: 0; }}
.col .panel {{ flex: 1 1 0; }}
.col.mid .panel:first-child {{ flex: 3.3 1 0; }}
.col.mid .panel:first-child .body {{ gap: 4.2mm; }}
.col.mid .cap {{ margin-top: 0; font-size: 11.6mm; line-height: 1.2; }}
.col.mid .note + .note {{ margin-top: 2mm; }}
.figs.rows {{ grid-template-columns: minmax(0, 1fr); }}
.figs.rows .fig {{ display: grid; grid-template-columns: 112mm minmax(0, 1fr); column-gap: 6mm; align-items: center; padding: 3mm 6mm; }}
.figs.rows .fig + .fig {{ border-top: 0; }}
.figs.rows .fig b {{ font-size: 40mm; }}
.figs.rows .fig p {{ margin-top: 0; font-size: 10.8mm; }}
.col:first-child .panel:first-child .rule li {{ padding: 3.2mm 0; }}
.col:first-child .panel:first-child .body {{ gap: 4.5mm; }}
.figs.three.even {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
.figs.three.even .fig b {{ font-size: 36mm; }}
.figs.three.even .fig {{ padding: 3mm 5mm 4mm; }}
.figs.three.even .fig p {{ font-size: 9.6mm; }}
.foot {{ grid-template-columns: 1.9fr 1fr auto auto; column-gap: 14mm; }}
.band .author b {{ display: block; font-size: 17mm; line-height: 1.1; }}
.band .author span {{ display: block; margin-top: 2mm; font-size: 10.5mm; }}
.foot .logo {{ display: block; height: 62mm; width: auto; margin-top: -3mm; }}
.foot div:nth-child(2) span {{ display: block; margin-bottom: 2mm; }}
{LAYOUTS.get(variant, '')}</style></head><body>
<header class="band">
  <div>
    <p class="eyebrow">{bi("The 2nd SNU Generative AI Competition")} </p>
    <h1>SNU Bridge</h1>
    <p class="tag">{tagline}</p>
  </div>
  <aside>{qr}<p>{bi("Scan to open the site")}</p><p>{html.escape(SITE.replace("https://", "").rstrip("/"))}</p><p class="author"><b>{html.escape(author.split(" · ")[0])}</b><span>{html.escape(" · ".join(author.split(" · ")[1:]))}</span></p></aside>
</header>
<main class="grid">{grid}</main>
<footer class="foot">
  <div>{foot_left}</div>
  <div>{bi("Board counts: {from} to {to}. Site figures as of {date}.", {"from": since[0], "to": until[0], "date": stamp[0]}, {"from": since[1], "to": until[1], "date": stamp[1]})}</div>
  {logo}
</footer>
</body></html>"""
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / ("poster.html" if variant == CHOSEN else f"poster-{variant}.html")
    target.write_text(page, encoding="utf-8")
    return target


def print_pdf(page):
    import fitz

    pdf = page.with_suffix(".pdf")
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--user-data-dir={profile}",
                        f"--print-to-pdf={pdf}", page.as_uri()], check=True, capture_output=True, timeout=180)
    doc = fitz.open(pdf)
    size = doc[0].rect
    width_mm, height_mm = size.width / 72 * 25.4, size.height / 72 * 25.4
    doc[0].get_pixmap(matrix=fitz.Matrix(0.42, 0.42)).save(page.with_suffix(".png"))
    words = len(doc[0].get_text().split())
    print(f"{pdf.relative_to(ROOT)}: {len(doc)} page(s), {width_mm:.1f} x {height_mm:.1f} mm, {pdf.stat().st_size // 1024} KB, {words} words in all (both languages)")
    if len(doc) != 1 or abs(width_mm - WIDTH_MM) > 1 or abs(height_mm - HEIGHT_MM) > 1:
        sys.exit("The PDF is not one page of the required size.")


if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else CHOSEN
    if variant not in LAYOUTS:
        sys.exit(f"No layout named {variant}. Choose from: {', '.join(LAYOUTS)}.")
    page = build(variant)
    if missing:  # before anything is printed: a poster with a line in English only must never be written
        sys.exit("These lines have no Korean yet:\n" + "\n".join(missing))
    print_pdf(page)
    if variant == CHOSEN and (ROOT / "site").is_dir():
        # The same page scaled to fit a browser pane, for the developer to click on a part and say what to change
        # (http://localhost:8770/poster/ with the local preview running). site/ is built again on GitHub and never
        # uploaded from here, so the author's name and the lab logo stay on this machine.
        preview = ROOT / "site" / "poster"
        preview.mkdir(exist_ok=True)
        (preview / "index.html").write_text(page.read_text(encoding="utf-8").replace(
            "</style>", "html { zoom: .14; overflow: auto !important; height: auto !important; } body { overflow: visible !important; }</style>", 1), encoding="utf-8")
        for name in ("snu-logo.png", "lab-logo.png"):
            if (OUT / name).exists():
                (preview / name).write_bytes((OUT / name).read_bytes())
    if variant != CHOSEN:  # a layout to compare: the sheet for the Korean reader belongs to the poster that is sent
        sys.exit()
    review = ["# Korean lines written for the poster only", "",
              "These are not on the site and have not been read by a Korean speaker. English first, Korean beneath.", ""]
    review += [line for english in used_new for line in (f"- {english}", f"  - {POSTER_KO[english]}")]
    print(f"{len(used_new)} Korean lines are written for the poster only: out/poster/korean-review.md")
    (OUT / "korean-review.md").write_text("\n".join(review) + "\n", encoding="utf-8")
