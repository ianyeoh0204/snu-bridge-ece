# SNU Bridge

Graduation requirements and department notices in English, for international students. The code builds a static website
from each department's official rule documents and its notice board. `AGENTS.md` holds the design, the rules and the
history of decisions.

Four departments are on the site: Electrical and Computer Engineering (ECE), Aerospace, Naval Architecture and Ocean
Engineering, and Nuclear Engineering.

## Set up
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env   # then put your own key in .env
```

## Run
```bash
.venv/bin/python -m bridge notices ECE   # read the department's board and record new and changed notices
.venv/bin/python -m bridge briefs ECE    # translate the notices that are new or changed (calls the model)
.venv/bin/python -m bridge site          # build site/index.html, site/cards.json and the calendar site/ece.ics
```
Replace `ECE` with `AEROSPACE`, `NAVAL` or `NUCLEAR` for the other departments.

The calendar (`bridge/deadlines.py`) holds only the dates that a notice prints with a weekday. Code checks each date
against that weekday and against the English line. No model is asked for a date. The build writes the calendar for a
department whose `config.json` has `site`, the public address of the page. Students subscribe to it from the Notices page.

## How it stays up to date without anyone's laptop
`.github/workflows/update.yml` runs on GitHub once a day. Its schedule says 07:17 in Seoul, but GitHub starts scheduled
jobs late (the run of 12 Nov 2026 began at 12:08), so the site and the poster promise no time of day.

Each run reads every department's board, translates at most 40 new or changed notices per department, saves them to
`data/`, rebuilds the site and publishes it with GitHub Pages. A department whose site is down does not stop the others.
The page is still rebuilt, and the run is marked failed at the end so that GitHub emails the owner.

A push to `main` republishes the site without reading the boards. The "Run workflow" button does a full run on demand.

## Taking over
1. Get access to this repository (or fork it) and turn on Pages under Settings > Pages > Source: GitHub Actions.
2. Add your own model key under Settings > Secrets and variables > Actions > New repository secret. Name it
   `ANTHROPIC_API_KEY` (the workflow also accepts `API_KEY`). To use another provider, change `bridge/llm.py` only.
3. Each semester, download the new official files into `sources/<department>/`, list them in its `config.json` and
   update the cards. Nothing else needs a person.
4. GitHub pauses scheduled workflows in a repository with no activity for 60 days, and emails first. Press
   "Run workflow" once to resume.

## Requirement cards
A person downloads each department's rule documents. An AI assistant writes the cards from them, one script per
department, and code checks every card against the Korean before saving it.
```bash
(cd tools && ../.venv/bin/python build_ece.py)   # ECE: writes data/ECE/cards.json
.venv/bin/python tools/pages_aerospace.py        # Aerospace: read its graduate rule pages (two rule sets per page, by entry year)
.venv/bin/python tools/cards_aerospace.py        # Aerospace: check every card and write data/AEROSPACE/cards.json
.venv/bin/python tools/cards_naval.py            # Naval: the same, from its rule PDFs in sources/NAVAL/
.venv/bin/python tools/cards_nuclear.py          # Nuclear: the same, from its rule PDFs in sources/NUCLEAR/
```
Each of the last three also loads that department's undergraduate cards from `tools/cards_<department>_undergraduate.py`.

## Checks
```bash
.venv/bin/python tools/check_quotes.py     # ECE undergraduate cards: the Korean quote and course codes are in every entry year's file
.venv/bin/python tools/check_updates.py    # "later notices" on ECE cards: each Korean quote is in the notice it cites
.venv/bin/python tools/audit.py prepare    # ECE: a second reader re-reads cards against the page images (see the top of the file)
.venv/bin/python tools/evidence.py         # recount ECE's Korean and English boards for the Background and Method page
.venv/bin/python tools/survey.py count     # count Korean and English notices in ten engineering departments
.venv/bin/python tools/survey.py aggregate # write the totals to data/survey.json (the commands `check` and `sample` verify the count)
.venv/bin/python tools/korean_review.py    # every English and Korean sentence pair, as a sheet for a Korean reader
.venv/bin/python tools/reader_sheet.py     # ten notices beside their Korean originals, as a sheet for a Korean-speaking reader
.venv/bin/python tools/poster.py           # the competition poster as a PDF in out/poster/, drawn from the same data as the site
```
`sources/context.json` holds the facts and links for the first step of the Background page, which covers what the
university has said and done this year. Re-read each cited page before changing a line there.

When two sources differ, the most recent official one is the rule. Add a line to `sources/<department>/updates.json`
with the notice number and the exact Korean line. The card then shows it under "Added or changed by later notices".

## The department's own files
The official PDFs and spreadsheets are not in this repository, because they are the department's documents, not ours.
`sources/<department>/config.json` lists each file with the page it was downloaded from. Download them into that folder
before running a card script, `tools/check_quotes.py` or `tools/audit.py`. The daily update and the site build do not
need them.

## Add a department
ECE is the main department (`"main": true` in its config). The page opens on it, and the Background page is about its
boards. Aerospace, Naval and Nuclear were each added in about a day, in four steps.

1. **Notices.** Create `sources/<NAME>/config.json` with the board's addresses and a `since` date. Copy
   `sources/NUCLEAR/config.json` as a start. Run `python -m bridge notices <NAME>` and `python -m bridge briefs <NAME>`
   on your own machine first. Never push a new department folder without its translated notices, or the daily job
   translates them all on GitHub. The readers in `bridge/notices.py` and `bridge/briefs.py` fit the board software these
   four departments use. Other software needs its own two readers, and `tools/survey.py` shows how the other engineering
   sites list their posts. For a slow site, set `board.pause` in its config to the seconds to wait between requests
   (Naval uses 5).
2. **Requirements.** A person downloads the department's graduation rules into `sources/<NAME>/`. PDFs there are never
   uploaded. An AI assistant writes `tools/cards_<name>.py` from `prompts/write-cards.md`. The checks in
   `tools/cards_pdf.py` refuse a card whose Korean quote is not in the document or whose numbers are not in a quote.
   For rules published as web pages, follow `tools/pages_aerospace.py`. Undergraduate rules differ by year of admission,
   so each undergraduate card lists its `entry_years`. Where every year has its own file, the card's quotes must be in
   each of them. `tools/cards_nuclear_undergraduate.py` is the shortest example.
3. **Second reading.** A model from another maker reads every card against the Korean with `prompts/read-cards.md`.
   Correct the cards and repeat until the findings no longer change what a student must do. Record the result in
   `data/<NAME>/audit.json`.
4. **Publish.** Add `programs`, `headline_cards` and `files` to the config and run `python -m bridge site`. Look at the
   department in the switch under the header, then push.

A folder with a `board` and `"pilot": true` but no cards appears on the Notices page only, as a pilot.

## The part done in ChatGPT Edu
`navigator/instructions.md` holds the instructions for the assistant that a student uses for what this site does not
read: images, attachments and the student's own questions about a notice. Paste them into a ChatGPT Edu project. They are
plain text, so they can move to a plugin or skill when the workspace offers one.

## Sending the source
On the sending day, pull first. The daily job saves new notices on GitHub, and the poster prints the day it was built.
```bash
git pull
.venv/bin/python tools/poster.py
git archive --format=zip --prefix=snubridge/ -o out/snubridge-source.zip HEAD
```
Look at `out/poster/poster.png` before sending. The last command packs exactly what is in the repository. It contains no key, no downloaded department documents and nothing from `out/`.
