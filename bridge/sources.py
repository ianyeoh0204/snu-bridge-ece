"""Read one department folder. PDF pages become images because official files are often pictures."""
from __future__ import annotations

import html
import json
import re
import zipfile
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent
DPI = 110


def _page_numbers(spec: str | None, count: int) -> list[int]:
    if not spec:
        return list(range(1, count + 1))
    pages: list[int] = []
    for part in spec.split(","):
        first, _, last = part.partition("-")
        pages += range(int(first), int(last or first) + 1)
    return [p for p in pages if 1 <= p <= count]


def _xlsx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        shared = re.findall(r"<si>(.*?)</si>", z.read("xl/sharedStrings.xml").decode("utf-8"), flags=re.S)
    lines = ["".join(re.findall(r"<t[^>]*>(.*?)</t>", item, flags=re.S)) for item in shared]
    return "\n".join(html.unescape(line) for line in lines if line.strip())


def load(department: str) -> list[dict]:
    """Return every readable unit: {"file", "name", "page", "png"} or {"file", "name", "page", "text"}."""
    folder = ROOT / "sources" / department
    config = json.loads((folder / "config.json").read_text(encoding="utf-8"))
    units: list[dict] = []
    for entry in config["files"]:
        path = folder / entry["file"]
        if path.suffix.lower() == ".xlsx":
            units.append({"file": entry["file"], "name": entry["name"], "page": 1, "text": _xlsx_text(path)})
            continue
        with fitz.open(path) as doc:
            for number in _page_numbers(entry.get("pages"), doc.page_count):
                png = doc[number - 1].get_pixmap(dpi=DPI).tobytes("png")
                units.append({"file": entry["file"], "name": entry["name"], "page": number, "png": png})
    return units
