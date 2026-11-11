# SNU Bridge: read this before every task

## What it is
The list a senior gives a new international student, kept correct by the department's own notices.
For each program it shows everything needed to graduate: what, when it opens, what it blocks, and the
official page that says so. Users are international students whose Korean is weak.

## How it works
1. `sources/<department>/` holds official files, downloaded by a person. `config.json` lists which to read.
2. Extract: a model reads every page, pictures included, and writes cards (`bridge/extract.py`).
3. Check: a second reading of each page against its cards. Disagreements are flagged, never published (`bridge/check.py`).
4. Notices: a daily job reads the department board, ties each notice to a card, updates its dates. (not built)
5. Publish: `python -m bridge site` rebuilds `site/index.html` from the cards (`bridge/site.py`). Calendar file: not built.
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
- Deployed (11 Nov): https://ianyeoh0204.github.io/snu-bridge-ece/ from the public repository `ianyeoh0204/snu-bridge-ece`.
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
- Not built: calendar file, plugin.
