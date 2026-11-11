# -*- coding: utf-8 -*-
"""Write every hand-written ECE card to data/ECE/cards.json. Run from the tools folder: python build_ece.py"""
from cards_ece_graduate_part1 import CARDS as PART1, write
from cards_ece_graduate_part2 import CARDS as PART2
from cards_ece_undergraduate import CARDS as UNDERGRADUATE
from wording import WORDING

graduate = PART1 + PART2
for c in graduate:
    c["title"], c["key"] = WORDING[c["id"]]
    c["entry_years"] = []
# What later notices add or change (sources/ECE/updates.json), attached to the cards they concern.
import json
from pathlib import Path
everything = graduate + UNDERGRADUATE
by_id = {c["id"]: c for c in everything}
for c in everything:
    c["updates"] = []
for u in json.loads((Path(__file__).resolve().parent.parent / "sources/ECE/updates.json").read_text(encoding="utf-8"))["updates"]:
    for card_id in u["cards"]:
        by_id[card_id]["updates"].append({"text": u["text"], "notice": u["notice"], "quote_ko": u["quote_ko"]})
write(everything)
