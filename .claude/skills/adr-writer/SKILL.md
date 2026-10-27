---
name: adr-writer
description: Write standalone Architecture Decision Records (ADRs) as numbered Markdown files in an adr/ folder with an index README, based on an architecture analysis or a decision already made in the conversation. Use when the user asks to "create an ADR", "write an ADR for <decision>", "record this decision", or to add follow-up ADRs (technology stack, authentication, domain rules).
---

# Writing ADRs

## Inputs

* The requirements file and the analysis/notes that led to the decision. Read both; the ADR must not contradict them. If it corrects them, say so in both places (see "Corrections").
* Existing `adr/` folder, if any: continue its numbering and conventions.

## Files

* Folder `adr/` next to the notes. One decision per file: `ADR-NNN-short-kebab-title.md`, numbers never reused.
* `adr/README.md` index: table `ADR | Title | Status | Waiting on`, plus a Conventions section. Create it with the first ADR, update it with every new one. Template: `templates/adr-index-template.md`.
* Each ADR follows `templates/adr-template.md`.

## Status

* `Proposed`: depends on an unanswered open question or an unknown (team skills, budget). Fill the "Waiting on" column.
* `Accepted`: the user has chosen it, or it follows directly from requirements with no open question.
* `Superseded by ADR-NNN` / `Deprecated`: an accepted ADR is not rewritten; a changed decision gets a new ADR that supersedes it. If a draft ADR existed inside notes, the full ADR says it supersedes that draft.

## Content rules

* **Self-contained.** Readable without the notes; link to the notes for long analysis (full scoring matrix, ER model) instead of copying it.
* **Context** states what the system does, which requirements matter for this decision (story numbers), what is missing and assumed, and the weighted drivers.
* **Decision is concrete and checkable.** Split it into numbered subsections (`2.1 …`): for an architecture style that means runtime/deployment, modules and responsibilities (including "not responsible for"), internal layout, dependency rules, data ownership, the critical workflow step by step, auth, authorization table, API conventions, external integrations, and **what this ADR does not decide** (pointing to the other ADRs).
* **Options considered** for each sub-question, with the score or reason each lost. Name the runner-up.
* **Consequences** are not a two-line list:
  * positives as a table: consequence · practical meaning · driver;
  * negatives as a table: consequence · practical meaning · mitigation · residual risk;
  * impact on people (developers, testers, operators, security reviewers, budget);
  * numbered follow-up work.
* **Compliance**: a table of checks that show the decision is being followed (architecture tests in CI, a concurrency test for the critical workflow, review rules), with when each runs.
* **When to revisit**: concrete triggers, and what the response would be (e.g. "extract a module, not rewrite").
* **Open questions** that may refine but not overturn the decision, each with the current default.
* Defaults for unanswered product questions go **inside** the ADR, clearly labelled "default answer to Qn".

## Splitting decisions

After the main architecture ADR, propose (and write if asked) separate ADRs for decisions it left open, typically: technology stack, authentication/sessions, the critical domain workflow, any undefined feature. List them as "Suggested next ADRs" in the notes.

## Corrections

If writing an ADR reveals a mistake in earlier notes (e.g. a wrong query), fix it in the ADR and add a visible **Correction** entry in the notes' follow-up log that links to the ADR. Do not silently edit the old section.

## Finish

1. Update `adr/README.md`.
2. Add cross-links: ADR header "Related" row, and a pointer from the analysis notes' follow-up log.
3. Append to the ADR conversation notes (see `architecture-decision` skill): request verbatim, what was done, decisions taken while writing (with why), ADR structure summary, one-sentence summary, suggested next ADRs.
