"""Cards as a plain Markdown table, for a person to look at before any website exists."""
from __future__ import annotations

from .cards import GROUPS


def render(all_cards: list[dict], gaps: list[dict], program: str) -> str:
    lines = [f"# {program}: {sum(program in c['programs'] for c in all_cards)} cards", ""]
    for group, label in GROUPS.items():
        rows = [c for c in all_cards if c["group"] == group and program in c["programs"]]
        if not rows:
            continue
        lines += [f"## {label}", "", "| Card | Rule | Why | When | Trap | Source | Check |", "|---|---|---|---|---|---|---|"]
        for c in rows:
            check = c.get("check", "unchecked") + (f": {c['check_problem']}" if c.get("check_problem") else "")
            cells = [c["title"], "<br>".join(c["rule"]), c["why"], c["when"], c["trap"],
                     f"p.{c['source_page']} {c['source_quote_ko']}", check]
            lines.append("| " + " | ".join(cell.replace("|", "/").replace("\n", " ") for cell in cells) + " |")
        lines.append("")
    if gaps:
        lines += ["## Rules the second reader found with no card", ""]
        lines += [f"- p.{g['page']} ({g['file']}): {g['missing']}" for g in gaps]
    return "\n".join(lines) + "\n"
