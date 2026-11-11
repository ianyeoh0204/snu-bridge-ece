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
write(graduate + UNDERGRADUATE)
