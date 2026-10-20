"""Central configuration: model per role, loop limits, priority scale.

Every value can be overridden through environment variables (or the CLI in run.py),
so the network is not tied to the example corpus.
"""

import os

# One model per agent role. At least three distinct models are used (ANS4).
DEFAULT_MODELS = {
    "extract": "gpt-5-mini",        # many parallel calls over chunks -> cheap but capable
    "completeness": "gpt-5.4-nano", # verifier, different model than extractor (independent check)
    "taxonomy": "gpt-5.6-luna",     # one global call: areas + glossary + candidate assignment
    "consolidate": "gpt-6-luna",    # hardest step: dedup, conflicts, priorities, wording
    "review": "gpt-5.6-luna",       # critic over the whole document
    "revise": "gpt-6-luna",         # applies critic feedback
}


def model_for(role: str) -> str:
    return os.getenv(f"RN_MODEL_{role.upper()}", DEFAULT_MODELS[role])


def _int_env(name: str, default: int) -> int:
    return int(os.getenv(name, default))


# Corpus handling
SUPPORTED_EXTENSIONS = {".txt", ".md", ".eml", ".text", ".rst", ".csv", ".json", ".html", ".htm"}
CHUNK_CHARS = _int_env("RN_CHUNK_CHARS", 12000)

# Feedback loop limits
MAX_EXTRACTION_ROUNDS = _int_env("RN_MAX_EXTRACTION_ROUNDS", 2)      # re-extraction passes after the first one
MAX_CONSOLIDATION_ROUNDS = _int_env("RN_MAX_CONSOLIDATION_ROUNDS", 2) # patch passes for unaccounted candidates
MAX_REVIEW_ROUNDS = _int_env("RN_MAX_REVIEW_ROUNDS", 2)              # critic -> reviser iterations

MAX_CONCURRENCY = _int_env("RN_MAX_CONCURRENCY", 8)
LLM_TIMEOUT_S = _int_env("RN_LLM_TIMEOUT", 900)

# Deterministic quality gates (OS5)
MIN_DESCRIPTION_WORDS = 35
MAX_NAME_WORDS = 10

# Priority scale (OS6). Single source of truth used by prompts AND the rendered document.
PRIORITY_SCALE = [
    {
        "level": "P1",
        "label": "Must have",
        "meaning": "Essential for the system to be acceptable; without it the system fails its core purpose.",
        "criteria": "Explicitly marked as high priority / critical / mandatory by stakeholders, legally or "
                    "financially mandated, requested independently by several sources, or a prerequisite "
                    "for other requirements.",
    },
    {
        "level": "P2",
        "label": "Should have",
        "meaning": "Important and high value, but the system remains usable without it for a limited time "
                   "or a workaround exists.",
        "criteria": "Clearly requested and justified by stakeholders, used regularly in daily work, or "
                    "supported by a large share of survey respondents, without being marked critical.",
    },
    {
        "level": "P3",
        "label": "Could have",
        "meaning": "Desirable improvement of usability, efficiency or insight.",
        "criteria": "Mentioned by a single source, framed as nice-to-have, or affecting a narrow user group.",
    },
    {
        "level": "P4",
        "label": "Future consideration",
        "meaning": "Acknowledged but deferred; not planned for the first release.",
        "criteria": "Explicitly deferred by stakeholders, speculative ideas, or items that depend on "
                    "undecided external factors.",
    },
]
PRIORITY_LEVELS = [p["level"] for p in PRIORITY_SCALE]


def priority_scale_text() -> str:
    return "\n".join(
        f"- {p['level']} ({p['label']}): {p['meaning']} Assign when: {p['criteria']}" for p in PRIORITY_SCALE
    )


DISCARD_CATEGORIES = {
    "conflict": "Contradicts another (kept) requirement; the conflict was resolved in favour of the other one.",
    "superseded": "Replaced by a later or more authoritative decision in the corpus.",
    "nonsensical": "Not meaningful, infeasible, or clearly not intended as a serious requirement.",
    "out_of_scope": "Concerns something outside the system described by the corpus.",
    "not_a_requirement": "Context, opinion or observation that does not express a need for the system.",
}
