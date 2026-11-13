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

One record is shared by everything: the card, defined in `bridge/cards.py`.
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
