# Prompt: a second reader checks a department's requirement cards

Give this to an AI model from a DIFFERENT maker than the one that wrote the cards, in a tool that can read files in this
folder but is told not to change them. Replace DEPARTMENT, SOURCES and CARDS. It was used on 13 November 2026 through
`kiro-cli chat --no-interactive --model gpt-5.6-sol --trust-tools=fs_read "<this text>" < /dev/null`.
Run it, correct the cards, and run it again; stop when what it finds no longer changes what a student must do, and
record the result in `data/<DEPARTMENT>/audit.json` (see `data/NAVAL/audit.json`). Expect each pass to find something.

---

REVIEW ONLY. Do not create, edit, move or delete any file anywhere. Do not run shell commands that change anything. Do not read any `.env` file. Do not use the network. Only read the files named below.

You are an independent second reader from a different AI maker than the author. Another AI wrote English "requirement cards" that summarise a Korean university department's graduate graduation rules for international students who read little Korean (Seoul National University, DEPARTMENT). A code check already confirms that each Korean quote exists in the source and that every number in the English appears in the card's quotes. It cannot see a swapped number, a wrong direction or unit, a dropped condition, a claim the Korean does not make, or a card shown to the wrong program. Find those.

Korean source text (authoritative): SOURCES
Cards: CARDS (JSON list). Each card has: id, programs (masters = 석사, phd = 박사, integrated = 석박사통합), title, key, rule (English lines), why, when, trap, applies_from, quotes_ko (the Korean lines it rests on).

For EVERY card: find its quotes in the source, read the surrounding section to see which program and which students they belong to, and compare every English statement in title, key, rule, why, when, trap and applies_from with the Korean.

Answer in English with:
1. A numbered list of real problems only, most serious first. For each: the card id; the English text; the Korean it should match (quote it); what is wrong; a corrected English line. Kinds of problem: (a) a number, limit, "at least"/"at most", unit, deadline or timing that differs from the Korean; (b) a card whose programs do not match the section its quote comes from; (c) a condition or exception in the Korean that the English drops and that changes what a student must do; (d) an English statement the Korean does not support; (e) a mistranslated term.
2. A final line in exactly this form: `VERDICT: <number of cards you checked> checked, <number> agree, <number> have a problem. Ids with a problem: <comma-separated ids or none>`.
If a card is correct, do not discuss it.
