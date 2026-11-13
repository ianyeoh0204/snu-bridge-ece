"""The groups a requirement card can belong to. The fields of a card are set by the card scripts in tools/."""
from __future__ import annotations

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
