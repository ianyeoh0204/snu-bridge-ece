# -*- coding: utf-8 -*-
"""Check sources/ECE/updates.json: every Korean quote must be found word for word in the notice it cites.
Run from the project folder: .venv/bin/python tools/check_updates.py   (one request per second)"""
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from bridge import briefs  # noqa: E402

squash = lambda s: re.sub(r"\s+", "", s)
config = json.loads((ROOT / "sources/ECE/config.json").read_text(encoding="utf-8"))["board"]
updates = json.loads((ROOT / "sources/ECE/updates.json").read_text(encoding="utf-8"))["updates"]
texts, failures = {}, 0
for update in updates:
    number = update["notice"]
    if number not in texts:
        texts[number] = squash(briefs.read(config["detail_url"].format(id=number))["text"])
        time.sleep(1)
    if squash(update["quote_ko"]) not in texts[number]:
        failures += 1
        print("NOT FOUND in notice", number, ":", update["quote_ko"])
print(f"{len(updates)} updates from {len(texts)} notices, {failures} quotes not found")
sys.exit(1 if failures else 0)
