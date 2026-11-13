"""Usage: python -m bridge notices DEPARTMENT
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
        missing = [line.split()[0] for line in failed if not (ROOT / "data" / department / "briefs" / f"{line.split()[0]}.json").exists()]
        if missing:  # an earlier translation still stands for the others; these have none to show
            sys.exit(f"{len(missing)} notices have no translation yet: {', '.join(missing)}.")
        return
    if command == "notices":
        from . import notices
        found, changes = notices.update(department)
        print(f"{len(found)} notices on record, {len(changes)} changes")
        for line in changes[:200]:
            print(" ", line)
        return
    sys.exit(__doc__)


if __name__ == "__main__":
    main()
