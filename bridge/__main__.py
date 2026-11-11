"""Usage: python -m bridge pages|extract|check|table|notices DEPARTMENT
       python -m bridge briefs DEPARTMENT [HOW_MANY]
       python -m bridge site"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load_env() -> None:
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            key, sep, value = line.partition("=")
            if sep and value.strip() and not key.strip().startswith("#"):
                os.environ.setdefault(key.strip(), value.strip())


def main() -> None:
    try:
        _main()
    finally:
        from . import llm
        if llm.usage["calls"]:
            print(f"model {llm.MODEL}: {llm.usage['calls']} calls, {llm.usage['input_tokens']} input tokens, "
                  f"{llm.usage['cached_tokens']} cached, {llm.usage['output_tokens']} output tokens")


def _main() -> None:
    if sys.argv[1:] == ["site"]:
        from . import site
        print(f"site written to {site.build().relative_to(ROOT)}")
        return
    if len(sys.argv) not in (3, 4) or (len(sys.argv) == 4 and sys.argv[1] != "briefs"):
        sys.exit(__doc__)
    command, department = sys.argv[1], sys.argv[2]
    _load_env()
    if command == "briefs":
        from . import briefs
        written, failed, checked = briefs.update(department, int(sys.argv[3]) if len(sys.argv) == 4 else 0)
        print(f"{checked} notices checked, {len(written)} translated, {len(failed)} failed")
        for line in failed:
            print(f"::warning::{line}")  # shown on the run's page on GitHub
        if failed and not checked:
            sys.exit("No notice could be read. The department site may be down or its page layout may have changed.")
        return
    from . import cards, check, extract, llm, sources, table  # after .env, so settings apply

    data = ROOT / "data" / department
    data.mkdir(parents=True, exist_ok=True)
    cards_file, gaps_file = data / "cards.json", data / "gaps.json"

    if command == "notices":
        from . import notices
        found, changes = notices.update(department)
        print(f"{len(found)} notices on record, {len(changes)} changes")
        for line in changes[:200]:
            print(" ", line)
        return
    if command == "pages":
        units = sources.load(department)
        for unit in units:
            size = f"{len(unit['png']) // 1024} KB image" if "png" in unit else f"{len(unit['text'])} chars text"
            print(f"{unit['name']:<45} page {unit['page']:>2}  {size}")
        print(f"{len(units)} units ready to send")
    elif command == "extract":
        result = extract.run(department, data / "extract_state.json")
        cards_file.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{len(result)} cards written to {cards_file.relative_to(ROOT)}")
    elif command == "check":
        result = json.loads(cards_file.read_text(encoding="utf-8"))
        gaps = check.run(department, result)
        cards_file.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
        gaps_file.write_text(json.dumps(gaps, ensure_ascii=False, indent=1), encoding="utf-8")
        tally: dict[str, int] = {}
        for card in result:
            tally[card["check"]] = tally.get(card["check"], 0) + 1
        print(f"checked {len(result)} cards: {tally}; {len(gaps)} rules found with no card")
    elif command == "table":
        result = json.loads(cards_file.read_text(encoding="utf-8"))
        gaps = json.loads(gaps_file.read_text(encoding="utf-8")) if gaps_file.exists() else []
        out = ROOT / "out"
        out.mkdir(exist_ok=True)
        for program in cards.PROGRAMS:
            (out / f"{department}-{program}.md").write_text(table.render(result, gaps, program), encoding="utf-8")
        print(f"tables written to out/ for {', '.join(cards.PROGRAMS)}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
