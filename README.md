# SNU Bridge

Graduation requirements and department notices in English, for international students. Official department files and
the department's notice board go in; a static website comes out. See `AGENTS.md` for the design and the rules.

## Set up
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env   # then put your own key in .env
```

## Run
```bash
.venv/bin/python -m bridge pages ECE     # list what will be read (no model call)
.venv/bin/python -m bridge extract ECE   # pages -> data/ECE/cards.json
.venv/bin/python -m bridge check ECE     # second reading; flags disagreements and gaps
.venv/bin/python -m bridge table ECE     # out/ECE-<program>.md for a person to review
.venv/bin/python -m bridge notices ECE   # read the department board; records new and changed notices
.venv/bin/python -m bridge briefs ECE    # translate notices that are new or changed (uses the model)
.venv/bin/python -m bridge site          # build site/index.html and site/cards.json
```
The requirement cards are currently written by hand: `cd tools && ../.venv/bin/python build_ece.py` writes
`data/ECE/cards.json`, and `.venv/bin/python tools/check_quotes.py` checks the undergraduate quotes.

## How it stays up to date without anyone's laptop
`.github/workflows/update.yml` runs on GitHub every morning (07:17 in Seoul). It reads each department's board, translates
notices that are new or changed, saves them to `data/`, rebuilds the site and publishes it with GitHub Pages.
Pushing to `main` republishes the site without reading the board. The "Run workflow" button does a full run on demand.

## Taking over
1. Get access to this repository (or fork it) and turn on Pages: Settings > Pages > Source: GitHub Actions.
2. Add your own model key: Settings > Secrets and variables > Actions > New repository secret, named `ANTHROPIC_API_KEY` (the workflow also accepts `API_KEY`).
   Translating one notice costs about 0.06 USD on Claude Opus. To use another provider, change `bridge/llm.py` only.
3. Each semester, download the new official files into `sources/<department>/`, list them in its `config.json`,
   and update the cards. Nothing else needs a person.
4. GitHub pauses scheduled workflows in a repository with no activity for 60 days; it emails first. Press
   "Run workflow" once to resume.

## Checks
```bash
.venv/bin/python tools/check_quotes.py     # undergraduate cards: Korean quote and course codes found in every entry year's file
.venv/bin/python tools/check_updates.py    # "later notices" on cards: each Korean quote found in the notice it cites
.venv/bin/python tools/evidence.py         # recount the Korean and English boards for the Background and Method page
.venv/bin/python tools/korean_review.py    # every English and Korean sentence pair, as a sheet for a Korean reader
.venv/bin/python tools/audit.py prepare    # a second reader re-reads cards against the page images (see the file's top)
```
When two sources differ, the most recent official one is the rule: add a line to `sources/<department>/updates.json`
with the notice number and the exact Korean line, and it appears on the card as "Added or changed by later notices".

## The department's own files
The official PDFs and spreadsheets are not in this repository, because they are the department's documents, not ours.
`sources/<department>/config.json` lists each file with the page it was downloaded from. Download them into that folder
before running `pages`, `extract`, `check` or `tools/check_quotes.py`. The daily update and the site build do not need them.

## Add a department
Create `sources/<name>/`, put the official files in it, and write a `config.json` like the ECE one.
