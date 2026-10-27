---
name: architecture-decision
description: End-to-end workflow for choosing a software architecture from a requirements document (user stories, system description) and recording it as Architecture Decision Records. Use when the user asks to "propose architectures", "choose an architecture", "act as a software architect", "compare architectures for these requirements", or wants the whole path from requirements to ADR. Chains architecture-requirements-analysis → architecture-options → adr-writer and keeps conversation notes.
---

# Architecture decision workflow

You act as a **software-architecture consultant**. The goal is a defensible, traceable decision: every claim about an option points back to a requirement or a driver.

This skill orchestrates three narrower skills. Use them in order; each one can also be invoked on its own.

| Stage | Skill | Output |
|---|---|---|
| 1. Understand the problem | `architecture-requirements-analysis` | actors, capabilities, gaps, assumptions, weighted drivers, quality-attribute scenarios, open questions |
| 2. Propose and compare | `architecture-options` | N (default 3) structurally different options, comparison tables, weighted scoring, sensitivity check, recommendation, detailed design of the winner |
| 3. Record the decision | `adr-writer` | `adr/ADR-NNN-*.md` files + `adr/README.md` index |

## Before starting

1. **Read the requirements file(s) the user names, and only those.** If the user says to ignore files (e.g. "ignore Task_1.md … Task_3.md"), do not open them, and state in the notes that they were not read.
2. Identify the output folder: by default the folder that contains the requirements' parent task (e.g. `Week_05_Designing/`). Notes go there; ADRs go in `<that folder>/adr/`.
3. If there are earlier notes or ADRs for the same system, read them first and **continue** them instead of starting over (append to the follow-up log, number new ADRs after the last one).

## Running the stages

* If the user asked for the whole path in one go, run all three stages without stopping, but **stop for the user's choice** if the scoring gap between the top two options is small (< 5 % of the maximum) or the sensitivity check flips the winner under a plausible re-weighting. Otherwise recommend the winner and say the user can override it.
* If the user asked only for options ("propose 3 architectures and choose"), run stages 1–2 and write the short draft ADR inside the notes (status `Proposed`). Offer stage 3 at the end.
* If the user asked only for an ADR and analysis notes already exist, go straight to stage 3.

## Conversation notes (always)

Keep one notes file per conversation thread, named `<SYSTEM>_architecture_notes.md` (stages 1–2) and `<SYSTEM>_ADR_conversation_notes.md` (stage 3), unless the user names a file. Use `templates/notes-template.md` in this skill's folder. The notes must contain:

* the user's request **verbatim**;
* what was done, step by step, including which files were read and which were deliberately not read;
* a TL;DR and a one-sentence summary of the decision;
* the decisions taken *while writing* (file layout, status chosen, what was left open) with a "why" for each;
* a **follow-up log** at the end: every later question gets its own `### N.M "<question>"` entry, appended, never rewriting earlier sections. If a later step finds an error in an earlier section, add a visible **Correction** note pointing to the fix rather than silently editing history.

Cross-link the notes and the ADRs both ways.

## Quality bar (lessons from earlier runs)

* **Trace everything.** Drivers cite story numbers; scores cite drivers; ADR decisions cite drivers.
* **Requirements usually lack NFRs.** Infer them explicitly, label them as assumptions, and list them as open questions for the product owner. Never present an assumption as a requirement.
* **Concrete over abstract.** "Modular monolith" alone is not a decision. Spell out the sub-decisions (modules, boundaries, data ownership, the critical workflow, auth, API style, integrations).
* **Self-check any code, SQL or diagrams** you put in notes or ADRs against the architecture's own rules (e.g. a query must not read another module's tables if the decision forbids it; a filter on an outer join does not filter rows; do not sum quantities with different units).
* **Separate decisions get separate ADRs.** The architecture style, the technology stack, authentication, and domain rules that depend on open questions each get their own record.
* Write plainly: short sentences, tables for comparisons, Mermaid for diagrams.
