# SNU Bridge: read this before every task

## What it is
The list a senior gives a new international student, kept correct by the department's own notices.
For each program it shows everything needed to graduate: what, when it opens, what it blocks, and the
official page that says so. Users are international students whose Korean is weak.

## How it works
1. `sources/<department>/` holds official files, downloaded by a person. `config.json` lists which to read.
2. Cards: requirement cards are written with an AI assistant from those files, one small script per department in `tools/`,
   and checked by code against the Korean (`tools/build_ece.py`, `tools/cards_*.py`).
3. Second reading: a model from another maker re-reads every card against its source (`tools/audit.py`, `prompts/read-cards.md`).
4. Notices: a daily job reads the department board, translates each new notice and ties it to a card (`bridge/notices.py`, `bridge/briefs.py`).
5. Publish: `python -m bridge site` rebuilds `site/index.html` from the cards (`bridge/site.py`), and the calendar file of deadlines (`bridge/deadlines.py`).
6. Plugin: the ChatGPT plugin reads the same cards and any screenshot a student pastes. (not built)

One record is shared by everything: the card. Its fields are set by the card scripts in `tools/`; `bridge/cards.py` holds only the groups.
Only `bridge/llm.py` talks to a model. Changing provider means changing that one file.

## The three screens (approved 11 Nov 2026)
0. Home (added 11 Nov): browse before entering. Programs with one number each, and the latest notices.
1. My roadmap: pick department, program, entry term. A strip shows what is open or expected this month.
   Cards are grouped by what they unlock, never by semester.
2. One card: at most five short lines, then why it matters, when, the trap, and the source page with the Korean line.
3. Notices: latest posts, one English line each, tied to a card or marked other. Calendar subscription.
Plus a "why and how" page for the poster's QR code.

## Rules
1. Glance first. No paragraphs on a first screen. One short line per item. Detail only on tap.
2. Recommend, never prescribe. Say "recommended before X because Y", not "do this in semester 2".
3. Real data only. No mock notices, no placeholder cards, no invented dates.
4. Every card carries its source file, page and Korean line. A card without a source is not published.
5. One step at a time. Each step ends with something the developer looks at and approves.
6. Prove it. End every task with the commands run, their real output, and what is not done or unsure.
7. Never copy personal names, emails or phone numbers from any source.
8. The ECE site's robots.txt disallows `/webdata`. Never fetch it. At most one request per second.
9. Keep code small. Standard library first. No new dependency without a reason.
10. Must run without the developer's laptop once deployed, and a stranger must be able to take it over.

## Scope
ECE graduate programs first (master's, PhD, integrated), then ECE undergraduate (both built). Then other departments,
one folder each. Visa, housing and life outside academics belong to other offices and are out of scope.

## Dates
Poster PDF and source archive due Fri 20 Nov 2026, 23:59. Booth demo Mon 30 Nov 2026, 14:00.

## Status (11 Nov 2026)
(Written 11 Nov. The counts, the extractor, the 07:17 promise and the pilot wording here are superseded by the sections of
12 and 13 Nov below.)
- Tone: formal, as for an official page. Card titles are noun phrases with a short key fact beneath (`tools/wording.py`).
- Cards: 98, all written by hand in Claude Code and marked `unchecked`. `tools/build_ece.py` writes `data/ECE/cards.json`.
  - Graduate: 69, from the handbook pages (`tools/cards_ece_graduate_part*.py`).
  - Undergraduate: 29, from the graduation audit card of each entry year, 2023 to 2026 (`tools/cards_ece_undergraduate.py`).
    A card with `entry_years` applies only to those years; 24 cards show for any one year. `tools/check_quotes.py`
    confirms every Korean quote and course code against every year the card applies to (0 failures).
    Not covered yet: the separate documents for double/minor majors and for the College of Liberal Studies.
- Notices: `python -m bridge notices ECE` records every notice since the date in `sources/ECE/config.json` (75 on record).
  `sources/ECE/notice_links.json` ties a notice to cards by title pattern.
- Notice translations: `python -m bridge briefs ECE` reads each notice body and writes `data/ECE/briefs/<id>.json`
  (English title, summary, dates with the Korean original, steps, full translation). Each quoted date is checked by code
  against the notice text; a date that is not found is shown as such. Resumable; a changed notice is translated again.
  Steps that belong to one case start with the case name and a colon ("Online attendance: ..."); the site shows the
  name once as a heading (`stepBlocks` in the template).
  State on 11 Nov: 75 of 75 translated, 243 dates all found in the notice title or text, 17 notices contain images
  that were not read (the page says so). Cost so far about 4.50 USD on Opus (roughly 0.06 USD per notice).
- Site: Requirements (program switch, year of admission for undergraduate, ticks saved in the browser) and Notices
  (by month, audience filter that follows the program, translation on tap, link to the original and the related requirement).
  A fresh browser lands on Home; Requirements opens on `default_program` from the config.
- Home view (approved look, 11 Nov): a blue band with the name and one line on what the site is, one column per program
  with its headline fact (`headline_cards` in the config), and the five latest notices as a board that turns once from
  Korean to English, with a language switch. Addresses: none or `#home`, `#requirements`, `#notices`, `#card-<id>`, `#notice-<id>`.
- Look (chosen by the developer on 11 Nov, replacing the Apple-style one): Swiss signage. One typeface (Helvetica), black and
  white plus SNU blue #002c84 as the only accent, black bars for section headings, visible grid lines, no rounded corners,
  no shadows, everything left-aligned. Yellow #ffd60a marks cautions only (developer's request: important things must
  stand out). Keep new elements inside this vocabulary.
- Motion (developer's request, 11 Nov): on Home and on "Why and how", parts move into place once when they scroll into view
  (section bars slide in, squares and bars fill, board rows turn, numbers count up). Plain CSS transitions and one small
  scroll check, no library. The finished page is the resting state, so nothing is hidden if the script fails, and
  reduced-motion users get it at once. Requirements and Notices stay still: they are for reading, not for show. The developer rejected an editorial
  "gazette" look as the worst of three: too many words.
- Extract and check code exist; the batch extractor is untested. The first single-request run failed at the output limit.
- Deployed (11 Nov) from the public repository, renamed `ianyeoh0204/snubridge` on 13 Nov: https://ianyeoh0204.github.io/snubridge/ (the old address `snu-bridge-ece` no longer serves the site).
  `.github/workflows/update.yml` reads the boards, translates, rebuilds and publishes every morning at 07:17 Seoul time;
  a push republishes only. The department's own files are deliberately not in the repository (see README).
  A notice counts as changed only when its text changes; the attachment download counter is stripped first
  (`COUNTER` in `bridge/briefs.py`), otherwise most notices would be translated again every day.
  First full run on GitHub passed on 11 Nov: 75 checked, 0 translated, 0 failed. The model key is the secret `API_KEY`.
  Unreadable attachments and images send the student to the `assistant` named in the config (ChatGPT Edu until the plugin exists).
- "Why and how" page (`#about`, built 11 Nov, awaiting the developer's approval before it is pushed): counted evidence
  first, then the method. `tools/evidence.py` counts posts and views per year on the Korean academic board and the English
  notice board into `data/ECE/evidence.json`; `sources/ECE/evidence_notes.json` holds what a person compared or read
  (the ten most-read notices against the English board, the pages where Korean and English differ, the chain of notices),
  each with its link and the date checked. No number on that page is typed into the template. The comparison is shown three ways
  the developer chose: one square per notice (500 against 64), the two boards side by side for the period the site covers,
  and bars by year. English only so far;
  a Korean version needs a Korean reader's check. Re-run the count and re-check the notes before 20 Nov and 30 Nov.
- Two languages on one page (developer's idea, 11 Nov): every sentence the site itself says is shown in English with the
  Korean beneath it in small type. No language switch, so one language can never be updated without the other being seen.
  The pairs live in `bridge/text.json` (English sentence to Korean sentence); the page asks for them with `B("...")`.
  `python -m bridge site` stops if the page uses a sentence with no Korean, or if a pair is no longer used. Labels in
  `sources/<department>/evidence_notes.json` are `{"en", "ko"}` pairs and are checked the same way.
  Rules and notices are never rewritten in Korean by us: the Korean shown for them is the department's own text.
  Done on every page (122 pairs). `B(...)` puts the Korean on its own small line; `L(...)` gives the one-line form
  "English · 한국어" for labels inside a sentence. `tools/korean_review.py` writes `out/korean-review.md`, every pair with a
  prompt for a Korean check (ChatGPT first, then a Korean reader).
  The page once called "Why and how" is now "Background and Method" (more formal, the developer's request); its address stays `#about`.
- Audit (11 Nov, local only until the developer approves): `tools/audit.py` has a second reader from a different maker
  (GPT through `codex exec -s read-only -i page.png --output-schema`) re-read 40 graduate cards against the handbook page
  images, with cards carrying a deliberately wrong number mixed in. First reading: 27 of 40 agreed in full. After
  corrections and re-reading: 36 agreed, 4 settled by the author with a reason (`sources/ECE/audit_notes.json`), 0 open;
  6 of 6 planted errors caught. Results live in `data/ECE/audit.json`; a card shows "Re-read by a second reader on <date>".
  Ten notices with deadlines were compared with the Korean original: 0 wrong dates, but every summary left out something
  (who exactly must act, conditions, further dates). Most of it is in the stored `applies_to` and the full translation.
- Two sourcing rules from the developer (11 Nov): (1) never delete a true fact because its cited page does not state it;
  cite the place that does. (2) When sources differ, the most recent official one is the rule. Both are carried by
  `sources/ECE/updates.json`: lines shown on a card as "Added or changed by later notices", each with the notice and a
  Korean quote that `tools/check_updates.py` finds word for word in that notice.
- Notice instructions, version 2 (12 Nov): after the audit, `SYSTEM` in `bridge/briefs.py` requires who exactly must act,
  every date a student could need, and a `conditions` list; `PROMPT_VERSION` makes every notice translate again when the
  instructions change. The site shows "Who must act" and "Conditions and exceptions" on each notice. The same ten notices
  were read again by the second reader: points that could mislead fell from 66 to 4.
  Never push a new `PROMPT_VERSION` without the re-translated briefs, or the daily job will redo them all on GitHub.
- Audit complete for all 98 cards (12 Nov): 74 agreed at the first reading; after corrections the second reader agrees
  with 91, and 7 are settled by the author with a reason on the card (mostly rules that run over a page break);
  11 of 11 planted errors were caught. Re-run it after any change to card text: `tools/audit.py prepare-rest <prefix> <snapshot>`.
- Not built: plugin. (The calendar file was built on 12 Nov, see the end of this file.)

## Other departments (12 Nov 2026)
(The counts in this section, 7,791 and 21, and the "500 against 64" in the Status section above, were replaced later the same
day. The current figures and rules are in "One period, one measure, ten departments" below. The instruction here not to
start a second department's requirements before 20 Nov was lifted by the developer on 12 Nov.)
- Survey: `tools/survey.py` counted the public notice boards of nine other engineering departments for 1 Jan 2025 to
  11 Nov 2026: 7,791 Korean notices, 21 of them with a title in English. Totals are in `data/survey.json` and on
  the About page ("Other engineering departments"); the full post lists and every fetched page stay in `out/survey/`
  (not published, titles can name people). Each count was repeated from the board's own row numbering. "English" is a
  title test, backed by a seeded sample of 90 opened notices (2 held a short English passage, none a full version).
  Materials Science (paging disallowed by robots.txt) and Architecture (everything disallowed) are not counted.
  The eleven sites read use six kinds of board software.
- Pilot: `sources/AEROSPACE/` is a notices-only department (112 notices since 1 Sep 2026, translated 12 Nov for about
  5.80 USD). `bridge/site.py` keeps pilots out of `departments` (the template takes the first department as the site's own)
  and passes them as `pilots`; the Notices page gets a department switch, a yellow pilot line, and the addresses
  `#notices-<DEPARTMENT>` and `#notice-<DEPARTMENT>-<id>`. Pilot translations were not re-read by the second reader and the
  page says so. The daily job now also translates new Aerospace notices (about 45 a month, roughly 2 to 3 USD).
- `bridge/notices.py`: the list reader now accepts both ECE's rows and Aerospace's (dashed dates, a category above the
  title, list pages numbered from 1, a first page of pinned notices only). It was checked to read ECE's 75 notices
  exactly as stored. A speaker's name after "Prof." or "Dr." in a title is replaced with "[name]".
- `bridge/briefs.py`: attachment links are found on both kinds of page (`md=down` on ECE, `bm=down` on Aerospace).
  Re-reading all 112 Aerospace notices gave the same text hash as stored, so the daily job does not translate them again.
- The developer wants the poster to say where and how the site can expand. Do not start a second department's
  requirements before the poster and source archive (20 Nov) are done.

## Background page, notices and the extra page (12 Nov 2026, published)
- The About page ("Background and Method") is six short steps, widest first, because the developer loses focus on a long
  scroll and wants the story told big to small: Why now, Engineering departments, ECE, In practice, How it works, Checks
  and limits. Only the step on screen is built. The steps are listed in a menu under the About tab (hover or focus; on a
  touch screen the first tap opens it), not as a block on the page; each step shows its own title with "n / 6" above it
  and a "Next" link below. Addresses: `#about` and `#about-<why|engineering|department|examples|method|checks>`.
- "Why now" ties the project to what the university itself has said in 2026. Its facts and links are in
  `sources/context.json`; each was read on the cited page on 12 Nov. Rules for that step: say plainly that the link
  between internationalisation and the AI Native Campus is this project's own reading; say which AI does what
  (translations by Claude through the API; an OpenAI model through ChatGPT Edu was the second reader); keep the names of
  university offices off the page; ranking figures are "as reported by" the two newspapers (QS's page could not be read).
  The developer's memory of a "go global" motto was wrong; the 80th-anniversary motto is something else and is not used.
- Notices: prompt version 2 made the short parts (summary, who must act, dates, conditions, steps) longer than the full
  translation for 65 of 75 ECE notices and 96 of 112 Aerospace notices (the developer noticed). The page now shows the
  summary and dates, then the full translation open and the checklist closed, unless the short parts really are shorter.
  A cleaner fix is shorter summaries in a prompt version 3, which means translating everything again (about 12 USD).
- `bridge/korean_blocks.html` is an extra page, built to `site/korean-blocks.html` and linked from the footer: the
  developer's own Korean grammar notes (examples written with Claude) in English, in the "sottsass" look of the
  open-source reacticle project, deliberately unlike the main site. Its English was read once by ChatGPT; no Korean
  speaker has read it yet, and its footer says it is a student's study notes.
- The developer's ChatGPT Edu quota is kept for the booth demo: do not run ChatGPT or Codex reviews without asking.
  Korean lines added on 12 Nov after that point are unchecked and wait for the developer's Korean-speaking reader.
- Each department's notice page is labelled a pilot until its requirements are written. The developer asked about a home
  page per major: wait until a second department has requirements; for now Home carries one line to each pilot.

## Calendar of deadlines (12 Nov 2026, published)
- `bridge/deadlines.py` writes `site/<department in lower case>.ics` (ECE: `ece.ics`) on every build, for a department whose config has `site` (the
  public address) and that is not a pilot. The Notices page shows one line with three links: Apple Calendar or Outlook
  (`webcal:`), Google Calendar, and the plain file. Students subscribe once; the daily build keeps the file current.
- No model is asked for a date. Code reads the Korean date line that was already confirmed word for word in the notice,
  and keeps it only if it prints a weekday the date really falls on, the English line names the same day, month and
  year, and the line is one date or a period (then the event is the last day, titled "Last day: ..."). A time is kept
  only if the English shows the same one. ECE on 12 Nov: 149 events from 243 date lines in 75 notices.
- Two errors the first version made, both fixed and worth remembering: a notice that printed the wrong weekday was
  placed a year later, where the weekday happened to fit (now a date without a printed year must lie within 300 days
  of the notice and agree with any year in the English); and the first day of a period passed as a deadline when the
  last day could not be read (now left out).
- Do not promise reminders. Each event carries an alarm, but Google Calendar ignores alarms in subscribed calendars
  (found in users' reports, not tested here). The page and poster say "deadlines in your calendar" and tell the student
  to set a notification in their own app. Calendar apps also fetch on their own schedule, so say nothing about speed.
- An event keeps its identifier while its date line and notice stay the same, so a rebuild does not duplicate it.
- The developer has not yet subscribed on a phone with Apple and with Google. Do that before the booth demo.

## Poster (12 Nov 2026, first draft with the developer for comments)
- `tools/poster.py` draws the poster (1445 mm wide, 1400 mm high, one page) from the same data as the site and prints
  it to `out/poster/poster.pdf` with Chrome, then measures the page. Six numbered panels in the site's look: Why now,
  The gap, What it does, How it works, Checked, Try it. Rebuild it just before sending so "Figures as of" is that day.
- The author's name is read from `out/poster/author.txt` and never written in a published file.
- Korean lines written only for the poster are in `POSTER_KO` and listed in `out/poster/korean-review.md`. None has been
  read by a Korean speaker; that must happen before the poster is sent (20 Nov).
- The developer finds long text tiring. Add a line only by removing or shortening another, and check that no panel
  overflows after any change (each panel's `.body` must not scroll).

## One period, one measure, ten departments, and the chosen poster (12 Nov 2026, published)
- The developer found the numbers unconvincing, and was right: the departments table mixed two measures (English-titled
  notices on Korean boards beside posts on English boards, so "40" sat next to a total of "21"), two periods (the other
  departments from 2025, this department from 2024), and it kept this department outside the total.
- One closed period everywhere: 1 January 2025 to 31 October 2026 (`WINDOW`/`UNTIL` in `tools/survey.py`, `SINCE`/`UNTIL`
  in `tools/evidence.py`). The start cannot be earlier: Mechanical Engineering's board begins on 2 January 2025.
- One test for English everywhere: the title is in English (Latin letters, no Korean), on either board, a notice posted
  on both counted once (`in_english`). The table's middle column adds up to the headline.
- One rule for all ten departments, this one included (the developer: "ECE is also engineering, make it uniform"):
  a department's notice boards are counted; boards it keeps apart for jobs, scholarships, news or seminars are not.
  A first attempt counted all six ECE boards and called that uniform; reading the other departments' menus showed six
  of them have a separate job board and three a separate scholarship board, none counted. So ECE is counted on four
  boards (academic, admissions, campus life, other). Ten departments: 8,477 notices on Korean boards, 60 with an English
  title. ECE: 891 and 35; its English board has 39 posts, 32 titled in English. The board this site translates, ECE's
  academic board, has 325 notices and none titled in English; the ECE step looks at that board alone and says so.
  Before any claim that departments were treated alike, check each one's menu, not only this department's.
- Do not generalise about English boards (ECE's is mostly English). State the two facts: Aerospace's last post is from August 2021 (seen on the page), Industrial's 33
  posts all have Korean titles. All numbered boards match their own row numbering inside the period; Computer Science
  prints none. The sample is 86 opened notices in the nine other departments, 2 with a line of English.
- Do not say "every morning" or "07:17": the scheduled run of 12 Nov started at 12:08 Seoul time. Say "once a day" or "daily".
- The live counts (notices, calendar events, requirements) are not board counts; the poster footer labels both.
- `sources/context.json` also holds the recruiting figures from the News1 report (re-read 12 Nov): 1 billion won to
  27 colleges and schools, a new undergraduate division from September 2027 with about 36 new students expected.
- Poster: the developer chose the evidence-first version of three drafts. `tools/poster.py` now draws only that one
  (`out/poster/poster.pdf`). Their further requests, all done: "Why now" is about SNU bringing in more international
  students; no clock time, "Daily" and the cost per notice instead; the gap panel is the tall one with all ten
  departments as rows; Checked is one short row of three figures (they found four large figures too much); the lab logo
  (`out/poster/lab-logo.png`, not published, like the author's name) sits in the footer in its red-on-white form.
  Every line has Korean again (46 poster-only lines in `out/poster/korean-review.md`, none read by a Korean speaker).

## Outside review of the poster (12 Nov 2026, late; page changes published)
- The developer suspected "illusions" on the poster and asked for a ChatGPT check (their explicit request, so the quota
  rule did not block it). One read-only Codex run (`out/poster/review-prompt.md`, answer in `out/poster/review-chatgpt.md`)
  reproduced every number, found none wrong, and found about a dozen lines that made a narrow check look like a broader
  claim. All were rewritten. The lessons, for every later line on the poster and the page:
  - Never put two counts side by side that are not part and whole. The "English title, either board" figure (60 beside
    8,477) is gone: the page and poster now show notices on Korean boards (8,477), how many of them have an English title
    (25), and posts on the separate English boards as their own column (80, of which 36 titled in English).
  - "0 of 325" was true and still misleading (a title test read as "nothing in English"); it is removed.
  - Say what a check measured: 91 of 98 cards agreed by the second AI reader and 7 settled by the author, not "98 of 98";
    dates "found word for word" check the quote, not the translation; the sample is a text test, not proof that no
    English version exists; the cost is an estimate ("about 0.06 USD").
  - The daily job translates notices only. Requirement cards were written and re-read once; do not draw them as a step
    of the daily chain. "Without the developer's laptop", not "no one's computer".
  - Attribute and qualify borrowed facts (QS rank "as reported by", the new division "planned for September 2027").
  - `codex exec` waits on standard input and hangs: run it with `< /dev/null`.
- Still open from that review, for the site: the requirement example and the calendar wording on the Notices page.
- The developer read "325" beside "39" on the ECE step as "39 of 325", and had seen English titles on the department's
  site that a bare "0" seemed to deny. Each number now names its page ("Page 1: Korean site, Academic tab", "Page 2:
  English site, Notice board", both linked), a line says the second is not a part of the first, and a table lists
  every tab of the Korean site with its notices and English titles (`tabs` in `data/survey.json`): the English titles
  are on the Scholarships tab (12), not the Academic one (0). Never show a count without saying which page it is from.
- Showing where a number comes from (the developer's question): name the page and the period beside the number, and
  where the things counted are few, list every one with its link. The engineering step lists all 25 English-titled
  notices (`english_titles` in `data/survey.json`), and the poster points to that list.

## A second department with requirements: Aerospace (12 Nov 2026, published on the developer's yes)
- The developer asked for two or three more departments built like ECE but without the second reader (the ChatGPT Edu
  quota is kept for the demo). Aerospace is first because its graduate rules are plain text on its own website.
- `tools/pages_aerospace.py` reads four rule pages into `out/aerospace/` (not published). Each page holds two rule sets,
  `tab-2020` (entrants up to 2020) and `tab-2021` (entrants from 2021), with different numbers: other-department credits
  for a master's are 12 in the old set and 9 in the new. They are separated by element id with a real HTML parser.
  Cutting the raw text at the first mention of the id put both sets in one file, and the tab captions in the page text
  are in a misleading order. Checked against the page's DOM in a browser.
- `tools/cards_aerospace.py` holds 30 hand-written cards for entrants from 2021 (master's 16, PhD 16, integrated 14) and
  writes `data/AEROSPACE/cards.json` only if every Korean quote is in the 2021 tab of the page it cites and every number
  in the English is in a quote. A deliberately wrong number was rejected. This replaces the second reader; it does not
  catch a wrong reading of the Korean, and at ECE the second reader disagreed with 24 of 98 cards at first reading.
  Course names stay in Korean with their numbers (the pages give no English names). Not covered: entrants up to 2020,
  undergraduate rules, research-student registration.
- Site: `bridge/site.py` puts the department marked `"main": true` first. The page shows one department at a time; a bar
  under the header switches (stored as `bridge:dept`, then a reload). A department without an audit shows a yellow line
  ("checked by code only, not re-read") in that bar, on each card's source line and on its notices. The Background page
  always opens on the main department. Older addresses `#notices-AEROSPACE` and `#notice-AEROSPACE-<id>` switch department.
- Before publishing: the poster's "One department's…" tagline and its "added as a pilot" step become untrue; fix them and
  freeze the department list before the Korean reader gets the lines. Nuclear and Naval publish their rules as files, so
  the developer has to download those into `sources/` first.
- An independent read then stood in for the second reader: a separate Claude session, given only the four source texts and
  the cards, found no wrong or swapped number and no card on the wrong program, but flagged 12 of the 30 cards: dropped
  conditions (the PhD thesis card had lost its document window and the research-student condition), "why" and "trap"
  lines the Korean does not support, one mistranslated trap, and two rules no card covered. All were applied; there are
  now 32 cards. The page says "checked by code and one independent AI reading from the same maker", which is what happened.
  The code check never reads `why`, `when` or `trap`: keep those fields to what a quote says.
- Decided with the developer on 12 Nov: stop at two departments. Nuclear and Naval are not built before 20 Nov; one
  extra department proves the setup carries over, and each further one adds risk under a real department's name.

## Proposal against the build (12 Nov 2026)
- The proposal the judges accepted promised, for the finals: (1) a Navigator in ChatGPT Edu, (2) a collector with change
  detection and one alert channel, (3) a web page with briefs reviewed by the applicant and a Korean-speaking labmate,
  (4) a pilot with 30 notices scored and about five students timed, then (5) one guide, "before you graduate".
  Built: 2 (daily, calendar instead of alerts), the page of 3, and 5 far beyond (98 cards, plus a second department).
  Not done: the human review in 3, the pilot in 4. Changed: translation is by Claude, not ChatGPT Edu, and the page says so.
- Two gaps being closed: `navigator/instructions.md` (the ChatGPT Edu part, rewritten from the September GPT, not yet run;
  the developer tries it with the quota kept for the demo), and `tools/reader_sheet.py`, which writes a sheet of ten
  notices for the developer's Korean-speaking labmate. Until that reading happens, never call a brief "reviewed by a person".
- Source for the 20th: `git archive` of HEAD into `out/snu-bridge-source.zip`. Rebuild it on the day it is sent.

## 13 Nov 2026
- Scheduled runs so far: 12 Nov at 12:08 and 13 Nov at 11:40 Seoul time, both successful, both more than four hours
  after the 07:17 schedule. "Daily" holds; no clock time does.
- The developer read the ten-notice sheet and found it correct, and does not want the site to say anything like
  "reviewed by a person": it looks unprofessional. Do not add such a label. In daily operation there is no human step:
  AI translates, code checks the quoted dates, and the Korean original is one tap away. Review by a department office
  is what the proposal offers the university if it adopts this, not something this project does.
- `navigator/instructions.md` was tried through Codex with the lighter model the developer asked for (`gpt-6.1-sol`,
  low effort): it behaved as intended on a pasted notice and on a poster image, and was tightened twice (no names of
  people, staff included; only dates a student acts on; three short lines first).
- The developer downloaded Nuclear's and Naval's graduate rule files into the older folder
  `../snu-ece-notice-navigator/sources/Nuclear` and `/Naval`, after agreeing to stop at two departments. Ask before building.
- Later on 13 Nov the developer asked for Nuclear and Naval "today" after all. Both are published. The rule PDFs were
  downloaded by the developer and sit in `sources/NUCLEAR/` and `sources/NAVAL/` (never uploaded).
  `tools/cards_pdf.py` holds the shared checks: each quote in the file it cites, every number in the English (and in
  why, when, trap) in a quote, and the page shown is the page the first quote is found on.
  - Nuclear (`tools/cards_nuclear.py`): 10 cards, entrants from 2021. The independent read found no wrong number and
    flagged 6 cards: dates of application in the supplementary provisions (부칙) that the cards had dropped, and 초심, a
    term the document never defines. The card now says so and sends the student to the office.
  - Naval (`tools/cards_naval.py`): 44 cards, drafted by a helper session from the 18-page rules and then read by a
    separate one, which found no wrong number or program and four real problems (a timing, a dropped "general
    admission track" qualifier, an unusable literal line, an unsupported "applies to"). The 2026 and 2025 versions
    differ only in the comprehensive examination subjects, so those have a card per version. Several lines in the
    document are ambiguous in Korean; the cards quote them and say the document does not settle it.
  - Notices: 52 (Nuclear) and 54 (Naval) since 1 Oct 2026. Nuclear's notice pages end with a different button row
    (`class="function"`), now accepted by `bridge/briefs.py`. Naval's site returned HTTP 500 and then refused
    connections at one request a second from three workers; `out/translate_gently.py` (one request every five
    seconds, a minute's pause after a failure) finished it. If the daily job fails on Naval, that is the first suspect.
  - A helper that writes cards must be followed by a different one that only reads; the writer's own report listed 18
    doubtful readings, and the reader settled or confirmed each.

## Second reader for every department's cards (13 Nov 2026, published)
- The developer asked whether the booth answer could be "double-checked by two frontier models", and offered Kiro
  (`kiro-cli`), which serves OpenAI models, for the reading. Command used, read-only, changing no file:
  `kiro-cli chat --no-interactive --trust-workspace --model gpt-5.6-sol --trust-tools=fs_read "<prompts/read-cards.md filled in>" < /dev/null`.
  Sol costs 4.4 times Kiro's base credit and Terra 2.2; the developer finds Terra enough, so use Terra for later passes.
- Result, recorded in `data/<DEPARTMENT>/audit.json` and shown on each card ("Re-read by a second reader on ..."):
  Nuclear 10 of 10 agreed; Aerospace 27 of 32 and Naval 39 of 44 agreed, the other 5 in each corrected as the reader
  asked and not read again ("settled by the author", with that reason on the card). With ECE's 91 of 98 that is 167 of
  184. First readings: Nuclear 7 of 10, Aerospace 28 of 32, Naval 38 of 44. No reading found a wrong number.
- This reading differs from ECE's: it compared cards with extracted text, not page images, and no planted errors were
  mixed in. Each pass finds smaller things than the last; stop when a finding no longer changes what a student does.
- What may be said: every requirement card in all four departments was written by one model and re-read by a model
  from another maker. Notices are translated by one model with dates checked by code; only ten ECE notices were re-read
  by the second model, and a department's Notices page still says its translations were not re-read.
  (Superseded by the Wrap-up below: all notices up to 13 Nov were re-read.)
- `navigator/instructions.md`: on the developer's decision the assistant gives the staff contact a notice lists (name,
  room, email) and addresses the email draft to that person. The public site still never copies names or contact details.
- `prompts/write-cards.md` and `prompts/read-cards.md` are the two prompts used to add a department, kept in the
  repository so that whoever takes this over can add the next one (README, "Add a department").
- Figures the developer got from the "Univ in Data" assistant on aichat.snu (대학알리미, not checked at the source by
  me): share of international students meeting the language standard 46.1% (2025 disclosure) and 45.5% (2026);
  international student dropout 7.9% and 6.8%; all students 2.3% (2025). Its "180" and "200" degree-seeking students
  cannot be the whole university (a university post puts Engineering alone at about 220) and are probably the
  undergraduate disclosure only. Nothing from it is on the poster or the site.

## Wrap-up (13 Nov 2026)
- The repository is `ianyeoh0204/snubridge` (the developer: "snu-bridge-ece" read as ECE only). The site address changed with
  it, so the poster's QR code, the calendar address and the assistant's instructions were rebuilt; anyone subscribed to
  the old calendar address must subscribe again.
- Removed as unused: `bridge/extract.py`, `bridge/check.py`, `bridge/table.py` and their commands (an automatic card
  extractor that was never run to completion; cards are written per department instead), and `data/ECE/notice_titles_en.json`.
- Daily job hardened after a read of the older repositories showed the gap: one department's site failing used to stop
  the loop, lose that run's translations and skip the rebuild. Now each department is read on its own, at most 40
  notices are translated per department per run, the page is always rebuilt, and the run is marked failed at the end
  (GitHub emails the owner) if any department could not be read. A first list page with no rows is an error, not
  "nothing new". `board.pause` in a config sets the seconds between requests (Naval: 5).
- The developer had the cost per notice ("about 0.06 USD") removed from the poster and the site: it depends on the model
  used, and the point is that the flow is automatic by design. Do not put a cost figure back.
- Older repositories (13 Nov, on the developer's yes): the daily jobs of `ianyeoh0204/snu-bridge` and
  `ianyeoh0204/snu-bridge-students` are disabled and the Pages sites `snu-bridge-site` and `snu-bridge-students` are
  unpublished (nothing deleted; both can be switched back on). They were still reading the ECE site daily and spending
  the developer's SNU gateway credit. The developer had asked the older project to read images and attachments while
  waiting for the office's permission; this project does not, and that stays so until permission arrives.
- Each notice has a button that copies a question for ChatGPT Edu carrying the ORIGINAL notice's address (the
  developer's point: the assistant should read the department's own page, not pass through this site's translation).
  Ideas from the older repositories the developer declined: a "due next" list (not relevant to every student), and a
  booth script for now (after 20 Nov).
- Notices re-read by the second maker (13 Nov, the developer: "run anything that needs second confirmation" with the
  lighter model): GPT-5.6 Terra through Kiro compared the short English parts of all 294 notices with their Korean text
  (`out/second_read_notices.py`; the Korean texts and raw answers stay in `out/`). 251 stood as written; it raised 55
  points on the other 43. 21 points were the standard "contact the department office" line this site writes on purpose,
  26 were real and were corrected in 22 notices (a wrong count of documents, a dropped period, "by 18:00" for a start
  time, a missing exception for 2020 entrants), the rest were judged not to matter. No wrong date was found.
  Counts per department are in `data/<DEPARTMENT>/notice_reading.json` and on each Notices page, which also says newer
  notices are not re-read: the daily job has no second maker in it. A corrected brief carries `second_reading`; it is
  lost, rightly, when the notice changes and is translated again.
  What may be said now: every requirement card and every notice translated up to 13 Nov 2026 was written by one model
  and re-read by a model from another maker; new notices are translated daily by one model with dates checked by code.
- A manual full run on 13 Nov read all four departments without a failure (Naval at five seconds a request) but then
  could not save: commits had been pushed to `main` during its 16 minutes. The save step now rebases onto those before
  pushing. Avoid pushing while a scheduled run is in progress all the same.
- Home page boxes (the developer, 13 Nov: every department should look like ECE's): a program's headline card must have
  a key shaped "<number> <unit>; <rest>" so the box shows a big number. Aerospace and Naval lead with credits like ECE.
  Nuclear's rule document gives no credit numbers (it leaves them to the university's regulations), so its boxes lead
  with the examination pass mark. Do not add credit numbers for Nuclear without a source that states them.
- The second full manual run of the daily job passed (15 min 46 s, all four departments read, saved and published).

## Undergraduate requirements for Aerospace, Naval and Nuclear (13 Nov 2026, published)
- The developer asked why those three had no undergraduate information ("make it complete") and downloaded the rule
  files, which sit in each `sources/<DEPARTMENT>/` (never uploaded). Three helper sessions drafted
  `tools/cards_<department>_undergraduate.py` from `out/undergrad/brief.md`; each department's main card script imports
  and saves them with its graduate cards. GPT-5.6 Terra through Kiro then read every card against the Korean.
  - Aerospace: 38 cards, 2023 to 2026 entrants, one rule file per year. Reader agreed with 37.
  - Naval: 31 cards, 2023 to 2026, from one 50-page file that covers every year from 2013 (pages 3 to 11 are the years
    covered). Reader agreed with 30. Its "45 major credits with another major" for 2023 and 2024 comes from merged table
    cells seen on the rendered page; the card says so and sends the student to the office.
  - Nuclear: 24 cards, 2023 to 2025 only: the department has posted no guide for 2026 entrants. Reader agreed with all.
    In the 2023 guide the two thesis courses carry no required mark although the stated required credits need them;
    the cards report that without deciding.
  Totals now: 277 cards in four departments, 258 agreed by the second reader, 19 settled by the author.
- `tools/cards_pdf.py`: `verify` checks cards; a card with `entry_years` whose source is "ug" is checked against the
  file of every year it lists when the texts are named "ug-<year>", and the site then cites the reader's own year's file
  (`series` and `entry_year` in the config's `files`). An undergraduate card without `entry_years` is refused.
- A program's `headline_cards` entry may be a list, for a total that differs by year of admission.
- None of these documents states a rule for international students, a thesis requirement, or (Nuclear, Naval) a grade
  average; the total cards say what the document leaves out rather than borrow it from elsewhere.
- Poster chart (the developer, 13 Nov): the middle column "of them, English title" was removed as confusing; a row now
  shows the Korean board's notices and what the English side holds. Computer Science and Civil show "same": their
  English menu lists the Korean board's own notices (checked live for Computer Science: same notices, same day, Korean
  titles), which is why a student there says both boards update together. No "(this site)" after ECE's name.
- Naval's two bachelor's-thesis cards (apply at least 2 semesters before graduating; advisor assignment) rest on text of
  the department's "학부 졸업" document that the developer pasted on 13 Nov; the paste is kept, not uploaded, beside the
  PDFs and is read by `tools/cards_naval_undergraduate.py` until the PDF itself is put there. 279 cards in all.

## Review before sending (13 Nov 2026, evening)
- The developer asked for a full review. Five read-only reviewers (poster, site text, cards, daily job, repository),
  each finding challenged by a second agent: 56 confirmed. The pattern behind most of them: lines written when the site
  had one department were still on the page ("requirements cover one department", "written by hand", "its notices were
  not re-read"). After adding a department, search `bridge/text.json`, `tools/poster.py`, the comments and the configs
  for every sentence that counts departments or says who read what.
- Counts now: 279 cards in four departments, 261 agreed by the second reader, 18 settled by the author. Seven cards
  whose title, key line or one rule line was reworded after their reading (two Nuclear, five Naval) were read again by
  GPT-5.6 Terra through Kiro (`out/review/second-maker-*-reworded.*`): all seven agreed. Any later change to a card's
  text needs the same, or the card becomes "settled by the author".
- Poster figures say their scope: "261 of 279 requirements, 4 departments"; "11 of 11 planted errors caught, in the ECE
  readings" (no planted errors were used for the other three); "841 of 847 quoted dates, 4 departments" (the 6 not found
  are marked on their notices). The alternative, ECE's own 241 of 241 with an ECE label, is equally true.
- Site: an unknown board word is now shown to every audience (Nuclear's Notices page had opened on 10 of 53 notices);
  the Notices line says the second reading covered the short parts, not the full translation; a card with no
  "Relevance" text no longer shows the empty label; no university office is named.
- A lecturer's name had come through in one ECE translation, inside an attachment's file name the model repeated. It is
  removed from the file; it is still in the repository's history (rewriting history is the developer's decision).
  `TITLED_NAME` only cleans the attachment list, not the model's text: check after any re-translation of a notice whose
  attachment name carries a person's name.
- Daily job: `actions/checkout` takes `main` (a push that waited behind a run no longer republishes an older page);
  five failures in a row stop a department and a failed request keeps the pace; the run is marked failed when a notice
  has no translation at all; a retitled notice is translated again; a pinned row is recognised by `noti-ico`;
  the limit is 150 minutes; `anthropic` is pinned to the version the translations were made with.
- Accepted as they are (the reviewers agreed): ECE's handbook gives two slightly different months for the defense
  results on pages 12 and 25, and each card follows its page; Naval's undergraduate cards cite the page where the quote
  first appears in a file that repeats it per year; Nuclear undergraduate stops at 2025 entrants, which Home says.
- New Korean lines from this review are unread by a Korean speaker, like the poster's: see `out/korean-new-lines.md`.

## Background page made the same as the poster (13 Nov 2026, night)
The developer read the page and found three places where the site and the poster had drifted apart.
- **One sentence, one copy.** A sentence shown on both the poster and the site lives in `bridge/text.json` only.
  `POSTER_KO` holds lines the poster alone prints. The first Background step ("Why now") now uses the poster's five
  sentences: the lead, the 1 billion won to 27 colleges, the division planned for September 2027, the President's
  address, and "Our reading". The older site wording ("two directions") named no figure, and the developer could not
  see in it that the university wants more international students. News1 was re-read on 13 Nov 2026 and holds all four
  figures. It also says colleges are to get extra funds by evaluation; the page does not use that.
- **Departments table.** The column "Of them, with an English title" is gone from both tables on the site, as on the
  poster. One row showed two different "English title" counts (Korean board and English board). The total of 25 stays
  above the table with its list of links. Do not bring a per-department English-title column back.
  Each row's English side is one count (posts on its English board), and the poster's two sentences under its chart
  (80 posts on 7 boards, 36 titled in English; Aerospace and Industrial Engineering) stand under the site's table.
- **The sample.** `tools/survey.py sample` counts pages with a run of eight or more English words beyond the site's own
  menus. The sentence says that and no more: "had a passage of English in the page text".
- The two links under one item ran together on a narrow screen (`.plain li > span` made the link row a block).
- The developer compared step 1 in two wordings and chose the unslop rewording ("pretty good, easy to understand"):
  whole sentences with the actor named, no label-and-colon openings. It is 6 words longer over ten lines; the rules
  reword, they do not cut. Four of the ten lines are also the poster's, so the poster was rebuilt with them and measured
  (no overflow). The other five Background steps are still in the earlier wording.
- The departments table shows a plain number for the English board (the developer: the heading already says what it
  is): the post count, "same", or "–", with the poster's legend line under the table. Energy Resources' last-post date
  (19 February 2024) is no longer on the page; it is in `data/survey.json`.

## The whole Background page and the poster in the chosen wording (13 Nov 2026, late night)
- The developer asked for the other five Background steps and the poster in the same wording as step 1 (the pstack
  `unslop` rules): whole sentences, the actor named ("This project read the boards"), no label-and-colon openings.
  34 more lines were reworded (764 to 795 words: it rewords, it does not cut). Labels, headings and the captions that
  read on from a big number were left alone. The limit phrases from the outside review were kept word for word
  ("Code, not AI", "not a part of the first", "not a measure of how much was translated", "have not been re-read").
- Not reworded, and not to be: requirement cards (any change to a card's text voids its second reading and the
  "261 of 279") and notice translations (they would have to be translated again). Home, Requirements and Notices
  labels are a few words each.
- Poster and site share a sentence where they say the same thing: Collect and Publish in "How it works" are now the
  poster's sentences (the site adds a second sentence of its own, as a second pair). Where the site carries more detail
  (Translate and Check as two steps, the second reader's page images) the wording is aligned, not identical.
- "Bodies and attachments were not read" left the title-count line: the line after it says only titles were tested,
  and the sample of 86 did read page text. "It runs on GitHub" became "The daily job runs on GitHub" (cards are not
  written there). The poster's requirements step now says an AI model wrote them, which the README already said.
- Second maker (GPT-5.6 Terra through Kiro, read-only; `out/review/reworded-*`): all 44 reworded lines, each old
  English, new English and Korean. 8 points: 1 Korean wording corrected ("짧은 부분" for "short parts"), 1 false alarm
  (the Korean amount is filled with its own value, 10억), 2 are the changes the developer had already seen and chosen
  in step 1 ("put them into English"; "working case of generative AI in administration" dropped), 4 are the true
  narrowings and additions listed above.
- `out/korean-new-lines.md` is generated, not edited by hand: every pair in `bridge/text.json` that differs from commit
  1cc6121. `out/poster/poster-before-unslop.png` is the poster before this pass.
- Poster (14 Nov, the developer's requests): the lab logo is 62 mm high (was 46). The line under "How it works" is
  "Claude writes the English. An OpenAI model, from a different maker, re-read every requirement card against the
  Korean." The developer could not follow "(ECE through ChatGPT Edu)", so it is gone. The footer says "For images and
  attachments, use ChatGPT Edu. The site does not read them." in the developer's own phrasing.
- A second poster layout to compare (14 Nov): `python tools/poster.py equal` writes `out/poster/poster-equal.*` with a
  lower blue band (196 mm, was 300) and every Korean line the same size as its English. The developer's reason: the
  judges read Korean. It fits with no overflow. The poster that is sent is still `poster.pdf` until the developer picks.
- A third layout (14 Nov): `python tools/poster.py balanced`, the lower band with Korean at 85% of its English and never
  smaller than on the first poster. It leaves room in every panel (146 to 393 px between parts at screen scale), which
  could go to larger small type in both languages. Three files to compare: `poster`, `poster-equal`, `poster-balanced`.
- The developer chose the "equal" layout (14 Nov): it is now what `python tools/poster.py` draws as `out/poster/poster.*`.
  `first` and `balanced` remain as arguments, to compare. The chart's column headings keep each language on one line.
  Every build also writes a scaled copy to `site/poster/` (local only): with the preview running, the developer opens
  http://localhost:8770/poster/ and clicks the part to change, as on the site. The developer asked why not Canva: the
  poster is drawn by code so that every number comes from the same data as the site and is right on the day it is built.
- Poster and site, the developer's requests of 14 Nov (later):
  - The chart shows a number in every row. A department with no separate English board counts 0 (Computer Science,
    Civil, Naval), and the column is headed "Separate English board posts" so that the 0 is exact. Do not show the
    Korean board's count there: it would read as 1,251 English posts. The "same" and "–" legend is gone from both; the
    site keeps one line in the notes under the table saying which three departments these are and why.
  - "A student project" is gone from the poster and the site (the developer: it reads as written by AI, and everyone
    at the competition knows). "Not an official Seoul National University website" stays in all three places.
  - The poster carries the university emblem (`out/poster/snu-logo.png`, not published) beside the lab logo, and the
    author's name at 17 mm. The emblem is never used on the site, which must not look official.
- Poster (14 Nov, later still): both marks in the footer are 80 mm high (the footer is 98 mm and the panels gave up
  12 mm). The note "The second reader is an AI model. It is not a check by a person or by the department." is off the
  poster: the developer found it redundant beside "agreed by the second AI reader". The room it freed went to a larger
  chart. The site keeps its own sentence, because there no other line says the second reader is an AI model.
- A product-first layout to compare (14 Nov, night): `python tools/poster.py product` writes `out/poster/poster-product.*`.
  The developer could not find the requirements, the notices or the calendar on the poster and thought the missing
  English notices were overstated. In this layout "What it does" is the tall panel with three large numbers (279
  requirements, 295 notices in English, 149 calendar dates), each with a real example; the requirement example is the
  master's credit card (24 credits), not the module seminar; "The gap" is an ordinary panel without the two notes on
  Aerospace's and Industrial's boards, which stay on the site. The poster that is sent is still `poster.pdf` (the
  "equal" layout) until the developer picks.

## The poster as something to point at (14 Nov 2026, night)
- The developer: the poster "looks nice but does not help me explain to the audience", and small edits were not fixing
  it. A fresh model with no history, playing a judge, said the same and why: no picture of the site anywhere, eleven
  large numbers of equal weight, every number needing a footnote, the scope changing from panel to panel (one
  department, ten, four, ECE), and a third of the sheet spent on things nobody needs to point at.
- The rule that replaces line-by-line editing: the poster follows the spoken explanation. Each panel is headed by a
  sentence the presenter says and holds one thing to point at. Anything the presenter would not say or point at comes
  off (so: no "student project", no "not an official website", no "the second reader is an AI model", no "Try it"
  instructions, no ten-row chart; the chart and the Why-now detail stay on the site).
- `python tools/poster.py talk` draws that layout to `out/poster/poster-talk.*`, to compare. Its three pictures are
  real screenshots taken by `tools/poster_shots.py` (run `python -m bridge site` first): the ECE Korean academic board
  as the department shows it, the newest notice as this site shows it, and a requirement with its source. The board
  picture is cropped to titles and dates; check it for a person's name before printing, since titles change daily.
- The poster that is sent is still `poster.pdf` (the "equal" layout) until the developer picks. "Not an official Seoul
  National University website" is off the poster at the developer's request; the site's footer keeps it.
- A second fresh model proposed a structure; taken from it: the example notice must carry real dates that print a
  weekday, so that the picture shows what the date check does (`tools/poster_shots.py` now picks, among the six rows
  the board picture shows, the notice with the most such dates), and the tagline says every item "links to" its Korean
  source, not "shows" it, which is not exact for a notice's full translation. Not taken, left for the developer: label
  headings ("The problem", "What a student gets"), a two-pane Korean and English notice drawn from the Korean text, and
  dropping "11 of 11". One broken sentence in a notice summary (58196, left by a correction on 13 Nov) was repaired.
- The developer rejected the screenshot layout (14 Nov, night) and it is removed, with `tools/poster_shots.py`:
  "you built the webpage, do you still need to screenshot?", and no panel about what the site does not do ("why see
  things in a bad perspective?"). Their framing, to keep: the website is for knowing all the information at a glance,
  and ChatGPT Edu is for further questions. So ChatGPT Edu is shown as a feature, never as a limit.
  The lesson: when the developer names the parts that need changing, change those parts. An outside reviewer's advice
  is input for the developer to weigh, not a reason to replace a layout they chose.
- The poster that is sent is now the "product" layout (`CHOSEN` in `tools/poster.py`): "What it does" is four named
  parts (Requirements, Notices, Calendar, Ask ChatGPT Edu) under the developer's sentence "The website shows all the
  information at a glance", each example drawn from the data, then "Where it extends". "Try it" step 3 is the ChatGPT
  Edu button. The footer's "What it does not do" block is one line: "Translations are made by AI. Every notice links to
  its Korean original, and every requirement cites its source."
- Say "an assistant in ChatGPT Edu" or "the ChatGPT Edu button", not "plugin": what exists is a button on each notice
  that copies a question, and `navigator/instructions.md` for a ChatGPT Edu project. No plugin has been built.
- Background pages made shorter (14 Nov, the developer: "everything below here feels too redundant", long detail
  makes the reader lose attention or take the site for one more AI app). On "Engineering departments" the list of 25
  notices and the notes on method, and on the ECE page everything from the tab table down, are folded behind one closed
  line each (`more(...)` in the template, class `fold`). They are folded, not deleted: the poster says all 25 are
  listed on the site, and the developer's own rule is that every number can be traced. Do not unfold them by default.
- The last Background page is "Checks" (was "Checks and limits"). Its closing block is "Ask ChatGPT Edu", in the
  poster's two sentences, and "This is not an official Seoul National University website" is gone from that page (the
  developer: everyone knows). The site's footer still says it once, in small type.

## Wrap-up of the site's own wording (14 Nov 2026, the developer: "this is a webpage they want to deploy")
The test for a line on a student-facing page: would the department office keep it if it ran the site next semester?
A line that reports to the developer how the project was checked belongs on About, not above a list a student reads.
- About is three pages, named as the poster's panels: Why now, The gap, How it works (`#about-why|gap|how`). The six
  older addresses still open the page their step is now part of (`STEP_MOVED` in the template).
  - The gap: the ten-department table; this department's two boards (the bars by year and the counting note moved into
    its fold); "In practice" as one sentence with its two examples folded.
  - How it works: the four steps; "Checks" with the poster's three figures over all four departments (261 of 279,
    11 of 11 in the ECE readings, 841 of 847), in the poster's words, and the notice re-reading as one sentence summed
    over the four departments (272 of 294 stood, 22 corrected); ECE's eight figures folded under them; Ask ChatGPT Edu;
    Extending to another department; Passing it on.
  - A sentence the site and the poster both print was moved from `POSTER_KO` to `bridge/text.json` (four lines).
- Removed, each for a reason the developer gave:
  - Everyone knows: "It is not an official Seoul National University website" (footer; now nowhere on the site or poster).
  - A report to the developer: the second reader's counts above the Notices list (they are on About); "This project did
    not read them from QS" (the line still says the two newspapers reported the figures); "The second reader is an AI
    model ... not a check by a person or by the department" (the Checks sentence already says "a second AI reader from
    another maker").
  - Said twice: the line under "Graduation requirements" (Home says it); "English titles are unofficial translations;
    the original notices are in Korean" on the Notices count line (the lede and the footer say it).
  - Said twice on the merged "How it works" page: each step is one sentence (the semester files and the source links are
    said under "Passing it on" and "Ask ChatGPT Edu"); the ECE-only counts under the four steps are gone, because the
    Checks row under them gives the same figures for all four departments; "without the developer's laptop" is said once
    there; the per-department lines under "Extending" no longer repeat the second reading.
  - The extra page's footer (`bridge/korean_blocks.html`) no longer says "student project" or "not an official website".
- Kept on purpose: "Re-read by a second reader on <date>" on each requirement and "Translated by AI on <date>..." on each
  notice. They are short, and they are what the 261 of 279 rests on.
- No sentence was written new. Korean was only cut, except "앞 단계에서는" to "위 표에서는" ("The table above counts...").
- Later the same day, on the developer's word: the footer is three sentences (unofficial translation, confirm with the
  office, last updated). "Made for the 2nd SNU Generative AI Competition" and the link to the extra Korean page are gone;
  `korean-blocks.html` is still built but nothing links to it.
- Second maker over the site's own pages (GPT-5.6 Terra through Kiro, read-only). What it read: the six pages as the main
  department (ECE) shows them, as plain text made by a script, with two notices and three requirements as examples, and the
  poster's text without the author line. It did not read the other three departments' pages, or any card or notice content; `out/review/site-read-*` and `out/review/site-pages/`). It was told the
  developer's tests (said twice, report to the developer, inconsistent, overclaiming, everyone knows, negative framing,
  Korean mismatch) and reproduced 295 notices, 279 requirements, 261, 18, 11 of 11, 841 of 847, 8,477, 80 and 149.
  Eleven points. Taken (5): the calendar line said "from these notices" beside a filtered count of 47, now "from this
  department's notices"; "and each was checked against that weekday" cut from the same note; "Once a day" was both a bar
  label and the first words under it, the label is gone; the poster's tagline said "A department's" on a sheet about
  four, now "Four departments'" (counted from the data); "the requirements covered" on the poster is "the requirements".
  Not taken (6): two were the count-up animation caught mid-count in the text dump (Home shows 130, 24, 36, 60 credits);
  "Re-read by a second reader" on each requirement stays (the developer was asked and removed only the other two);
  "Translated by AI on <date>..." on each notice stays (it sends the student to the original); the gap page's first
  sentence stays (8,477 notices on Korean boards against 80 posts on English boards, and the next sentence says so);
  "The website shows all the information at a glance" is the developer's own sentence.

## Final check (14 Nov 2026): four Opus 5.5 readers and a click-through
The developer asked for a last check of every button and every wording by a few Opus 5.5 agents. Four read-only readers,
one scope each, on one frozen build (`out/review/final-pages/`: the three student pages of all four departments, the three
About pages and the poster's text): student pages, every number recounted from the data, every control and route read as
code, every English and Korean pair. Every finding was checked on the page or in the data before anything was changed.
`bridge/korean_blocks.html` is out of the repository and the build (a copy is in `out/`, not published).
- The numbers all reproduce (8,477, 25, the ten rows, 80 and 36, 261 of 279, 18, 11 of 11, 841 of 847, 295, 149, 181).
  Wording corrected where it said more than was counted: the 80 posts are on "the separate English boards of 7
  departments" (two departments have more than one board, so "7 boards" was wrong); the poster's "each with its file, page
  and Korean line" is "its source and Korean line" (94 of the 279 cards cite a web page or a yearly file and show no page
  number); "re-read them once" lost its "once" (three departments were read more than once); "the first two newspapers
  below" (three links follow); the two ECE captions said summaries "left out something" where the count is any point
  that could mislead.
- Found by reading the code, and fixed: notice headers ran off a 375 px screen in Nuclear, Aerospace and Naval (long
  category tags could not wrap); the About list stayed open over the page on a phone (hover is now for devices that
  hover, and every page change closes the list); a `#card-` address for a card of another program or year opened nothing
  (it now shows that program); an address for another department's card or notice opened the wrong department (it now
  switches, so a shared link and a calendar event land on the right notice); opening About from another department left
  the visitor on ECE (leaving About by a tab goes back to their department; `bridge:from`); "Recent notices" on a card
  opened the Korean page under an English title (it opens this site's page of the notice); the copy button said "Copied"
  when nothing was copied; a browser that stores nothing could not switch department (the choice then rides in the
  address as `?dept=`, and ticks count for the page).
- Student pages: "1 items" is "1 item" (and "1 notice", which the first notice of each new month would have shown wrong);
  under a filter the Notices count is "47 of 75 notices since 1 July 2026", a part and its whole; "Attachments", not
  "Attachments (Korean)" (some are English files); Home's line under the board is gone (the footer says both things).
- Korean, 13 of 15 points taken: one phrase that could read as "rewritten" for "reused", one count that could read as
  per department, 영문 for every "English board" and 게시물 for every "post", the formal ending where three lines used the
  casual one, "실제 사례" for the heading "In practice". An Opus read is not the Korean speaker's read; the sheets still go out.
- Not taken, with the reason: card and notice content (out of scope; changing a card voids its second reading); the
  count "0 of 30 completed" beside 35 items (the five that repeat every semester have no tick box, and sit under their own
  heading); "Also on this site: ..., 70 requirements and 113 notices" (live counts, not evidence); "Caution. Images in this
  notice that could not be read" (a student must know the picture was not translated, and the line says what to do);
  method notes inside closed folds; the Notices filter resetting on each visit; the poster's inviting "-보세요" endings.
- Tested in the page after the fixes, desktop and 375 px: every tab, the menu's first and second tap, all folds, all old
  About addresses, department switch and return from About, program and year buttons, a tick across a reload and with
  storage blocked, the filter with its counts, the copy button (the question carries the original notice's address),
  the calendar links and file (149 events), cross-department addresses, no sideways scroll, no console error.
