# Prompt: write a department's requirement cards

Give this to an AI coding assistant working in this folder, after a person has downloaded the department's graduation
rules into `sources/<DEPARTMENT>/` and their page text has been extracted (see `tools/cards_pdf.py: pages`).
Replace the names in capitals. It was used for Naval Architecture and Ocean Engineering on 13 November 2026.
The writer must be followed by a different reader (`prompts/read-cards.md`): the writer's own check cannot see a wrong
reading of the Korean.

---

Create and edit ONLY the file `tools/cards_DEPARTMENT.py`. Do not edit any other file, do not read any `.env` file, do
not use the network, do not run git.

The project shows international students, who read little Korean, a department's graduate graduation requirements in
English as short "cards". Every card rests on Korean lines quoted word for word from the department's own rule
document, and a code check rejects a card whose quote is not in the document or whose English numbers are not in its quotes.

Write the cards for DEPARTMENT NAME (KOREAN NAME), graduate programs (master's 석사, PhD 박사, integrated MS-PhD
석박사통합), from: SOURCE FILES AND WHAT EACH IS.

Read first: `tools/cards_pdf.py` (the helper and what `write` checks) and `tools/cards_nuclear.py` (a short finished
example; follow its style, including the note at the top saying what the document is and where it is downloaded from).

- Card ids start with a two-letter prefix and a hyphen. `programs` is a list from "masters", "phd", "integrated",
  decided from the document's own section headings.
- `group` is one of: "finish_coursework", "credit_rules", "start_early", "before_exam", "for_degree", "every_semester".
- `title`: a short noun phrase. `key`: the one fact to take away, under about 70 characters. `rule`: 1 to 6 short
  English sentences, each saying only what the Korean says. `quotes`: the Korean lines the card rests on, copied exactly.
- `applies_from`: who the card applies to, in the document's words (entry year or term, and any date of application in
  the supplementary provisions). Where two versions of a rule apply to different entrants, write a card for each.
- `why`, `when`, `trap`: optional, one short sentence each, and only what a quote supports. Leave them "" rather than
  add advice or guesses. Any number in them must also be in the card's quotes.
- Keep course names in Korean with their course numbers. Do not invent English course titles.
- Never copy a person's name, phone number or email address.
- 수료 is completion of coursework, not graduation. Keep "at least" and "at most" straight. Keep every condition and
  exception that changes what a student must do. Where the document is silent or unclear, say so on the card.
- Cover every rule a graduate student must act on: credits, required courses, grades, limits on other-department or
  undergraduate courses, examinations (pass marks, timing, retakes), publications, thesis examination and submission,
  time limits, anything specific to international students. Skip blank forms and lists of people.

Run `cd tools && ../.venv/bin/python cards_DEPARTMENT.py` until it prints "N cards written". Do not delete a true number
from the English to pass the check; add the Korean line that carries it to `quotes`.

Report: the final line of the check; each card id with its programs and key; every place where you were unsure of the
Korean, with the line and the alternatives; and the rules you left out, with the reason.
