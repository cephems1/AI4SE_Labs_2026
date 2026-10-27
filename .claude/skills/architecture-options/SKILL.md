---
name: architecture-options
description: Propose several structurally different candidate architectures for a system, explain each fully, compare them against weighted architectural drivers with a scoring matrix and sensitivity check, recommend one, and work out a detailed design of the winner. Use after requirements analysis, or when the user asks to "propose N architectures", "compare architectures", "which architecture should we use", or "score these options".
---

# Proposing and comparing architectures

Prerequisite: the drivers, weights, scenarios and open questions from `architecture-requirements-analysis`. If they don't exist yet, run that skill first.

## 1. Choose the candidates

* Default **3** options (or the number the user asks for). They must differ on a **structural axis that matters for this system**, usually: number of deployable units, data ownership (one DB vs. DB per service), and who runs the infrastructure. A good default spread for a web product:
  * **Modular monolith** (one deployable, business modules with enforced boundaries, one DB with schema per module);
  * **Microservices** (API gateway, DB per service, broker, sagas);
  * **Serverless / BaaS** (managed auth + managed DB with row-level security + functions).
  Swap in others when the domain calls for it: event-driven / streaming, space-based, micro-kernel / plugin, CQRS + event sourcing, edge/offline-first, pipeline/batch.
* Add a short table **"Styles considered but not shortlisted"** with why (e.g. hexagonal is complementary, it organizes code *inside* a deployable).
* Start with a 3-column overview table: deployable units · databases · who runs the infrastructure.

## 2. Explain each option fully

Same structure for every option so they can be compared:

1. **Idea**: a paragraph a non-expert can follow.
2. **Diagram** (Mermaid flowchart).
3. **Components / modules / services** table: name · owns · stories.
4. **How the critical workflow runs** (the one with consistency risk), with a sequence diagram where it differs between options (e.g. local ACID transaction vs. saga with compensations).
5. **Data**: where it lives, who may read what.
6. **Deployment**.
7. **Strengths** and **weaknesses for this system specifically**, not generic lists.

## 3. Compare

1. **Side-by-side table** on generic dimensions: deployables, consistency, cross-entity queries, dev complexity, ops complexity, cost at this scale, scalability ceiling, fault isolation, testability, modifiability, lock-in, team size it suits.
2. **"How each option handles the hard parts"** table: one row per hard requirement found in the analysis (with story numbers), one column per option. This is the most persuasive table; make it concrete.
3. **Weighted scoring matrix**: rows = drivers with the weights from the analysis, scores 1–5 per option, weighted = weight × score, totals and percentage of the maximum (Σweights × 5). Double-check the arithmetic.
4. **Rationale for the less obvious scores**: one bullet each for any score that a reader might dispute.
5. **Sensitivity check**: 2–3 plausible re-weightings ("demo in two weeks", "national rollout with many teams", "no cloud provider allowed") with the recomputed totals and whether the winner changes.

## 4. Decide

* State the winner, the runner-up and why the runner-up lost (not only why the winner won).
* Write a **short draft ADR** in the notes (Status `Proposed`, Context / Decision / Alternatives / Consequences / Revisit when). The full ADR is the job of `adr-writer`.
* If the top two are within 5 % or the sensitivity check flips the result, present both and ask the user to choose.

## 5. Detailed design of the chosen option

Enough that ADRs and implementation can start:

* module/service catalogue with public interface examples and a **story-to-module mapping** (confirm all stories are covered);
* dependency rules (direction, no cycles, public API only, events for upward notifications) with a diagram;
* code structure (stack-neutral folder tree);
* data model (Mermaid ER) with design notes (snapshots, soft delete, ownership);
* API sketch table: method & path · role · story;
* key mechanisms: auth/sessions, authorization (role + ownership), the critical workflow, any undefined feature with a proposed default, external integrations;
* example technology stacks (2–3 ecosystems), deployment diagram, CI, observability;
* evolution path and risks with mitigations.

**Self-check** every SQL query, sequence and diagram against the chosen architecture's own rules before writing it down (module data ownership, join semantics, unit consistency, transaction boundaries).

## 6. Close

Open questions (from the analysis, refined), glossary of terms used, next steps. Then offer: "Shall I write the ADR(s)?" (→ `adr-writer`).
