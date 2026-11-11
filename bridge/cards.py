"""The one record everything shares. The website, the calendar and the plugin read cards and nothing else."""
from __future__ import annotations

PROGRAMS = ["undergraduate", "masters", "phd", "integrated"]

# Cards are grouped by what they unlock, never by semester.
GROUPS = {
    "start_early": "Early preparation",
    "before_exam": "Qualification examination eligibility",
    "general_education": "General education",
    "major_courses": "Major courses",
    "finish_coursework": "Coursework completion",
    "credit_rules": "Credit and grade rules",
    "for_degree": "Degree conferral",
    "every_semester": "Each semester",
}

CARD = {
    "type": "object",
    "additionalProperties": False,
    "required": ["id", "programs", "group", "title", "key", "rule", "why", "when", "trap",
                 "applies_from", "source_file", "source_page", "source_quote_ko"],
    "properties": {
        "id": {"type": "string", "description": "Short lowercase slug, e.g. seminar-audit"},
        "programs": {"type": "array", "items": {"type": "string", "enum": PROGRAMS}},
        "group": {"type": "string", "enum": list(GROUPS)},
        "title": {"type": "string", "description": "Formal noun phrase, at most 8 words"},
        "key": {"type": "string", "description": "The key fact in at most 7 words, numbers as in the source"},
        "rule": {"type": "array", "items": {"type": "string"},
                 "description": "1 to 5 short lines. Numbers exactly as in the source."},
        "why": {"type": "string", "description": "One line: what this unlocks or blocks"},
        "when": {"type": "string", "description": "Months or timing stated in the source, else empty"},
        "trap": {"type": "string", "description": "The easy mistake, if the source states one, else empty"},
        "applies_from": {"type": "string", "description": "Entry-year condition stated in the source, else empty"},
        "source_file": {"type": "string"},
        "source_page": {"type": "integer"},
        "source_quote_ko": {"type": "string", "description": "The Korean line copied exactly from the page"},
    },
}

CARD_LIST = {
    "type": "object", "additionalProperties": False, "required": ["cards"],
    "properties": {"cards": {"type": "array", "items": CARD}},
}

PAGE_CHECK = {
    "type": "object", "additionalProperties": False, "required": ["cards", "missing"],
    "properties": {
        "cards": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["id", "verdict", "problem"],
            "properties": {
                "id": {"type": "string"},
                "verdict": {"type": "string", "enum": ["confirmed", "wrong", "not_on_page"]},
                "problem": {"type": "string", "description": "Empty when confirmed"},
            }}},
        "missing": {"type": "array", "items": {"type": "string"},
                    "description": "Rules on this page that a student must act on and no card covers"},
    },
}
