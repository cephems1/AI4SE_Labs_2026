# NFFH — ADR Conversation Notes (new session)

| | |
|---|---|
| **Project** | **Not Far(m) From Home (NFFH)**: "km 0" platform for reserving farm produce with pickup at the farm |
| **Requirements source** | [../Tasks/data/NFFH.txt](../Tasks/data/NFFH.txt) |
| **Date** | 2026-10-27 |
| **Participants** | michaljaros · Claude (architecture consultant) |
| **Result** | 7 ADRs in [adr/](adr/README.md), all `Proposed` |
| **Previous conversation** | Stages 1–2 of this session: [NFFH_architecture_notes.md](NFFH_architecture_notes.md). Whole session: [Session_conversation_notes.md](Session_conversation_notes.md) |

---

## 0. Conversation log

### 0.1 The request (verbatim)

> *"use skills described in .claude to make a proposial of architecture of requirements in @Week_05_Designing/Tasks/data/NFFH.txt , save every output into new folder called new_session, make notes of this converastion and taken decisions"*

There was no separate ADR request. Stage 3 ran as part of the full `architecture-decision` workflow, because the user asked for the whole proposal in one go and the scoring gap (11.4 %) was above the 5 % stop threshold.

### 0.2 What was done, step by step

1. Re-used the analysis and scoring from [NFFH_architecture_notes.md](NFFH_architecture_notes.md) (same session) and the requirements file.
2. Read the `adr-writer` skill and its two templates.
3. Created `new_session/adr/`. **Did not** continue the numbering of the older `Week_05_Designing/adr/` folder: this is an independent set, so it starts at ADR-001.
4. Wrote ADR-001 (style), then split out ADR-002 … ADR-007 as separate decisions.
5. Self-checked every SQL query, sequence and rule against ADR-001's own rules. This found two mistakes (section 3).
6. Wrote [adr/README.md](adr/README.md), added the cross-links, and appended to the analysis notes' follow-up log (§8.1, §8.2).

### 0.3 TL;DR

* **ADR-001** modular monolith (4 modules, 1 PostgreSQL, schema per module, checkout in one transaction).
* **ADR-002** Java 21 + Spring Boot + Spring Modulith + PostgreSQL + React (waits on team skills).
* **ADR-003** server-side revocable sessions in an HttpOnly cookie.
* **ADR-004** checkout: one order per farm, all-or-nothing, conditional `UPDATE` on stock, price confirmation.
* **ADR-005** hot products = in season, ranked by recent order lines.
* **ADR-006** areas = admin-defined regions, client home area.
* **ADR-007** soft delete and anonymisation.

---

## 1. ADR structure

| ADR | Status | Waiting on | Key content |
|---|---|---|---|
| [001](adr/ADR-001-modular-monolith.md) | Proposed | sign-off | 11 sub-decisions: runtime, modules, layout, dependency rules, data ownership, checkout, auth, authorization table, API, Maps, non-decisions. Scores 156 / 135 / 90 |
| [002](adr/ADR-002-technology-stack.md) | Proposed | Q14 | Stack scoring: Java 85, Python 78, TypeScript 77. Team familiarity can flip it |
| [003](adr/ADR-003-authentication-sessions.md) | Proposed | sign-off, Q13 | Token hash in DB, 30-day sliding / 90-day absolute, admin 12 h, CSRF, Argon2id |
| [004](adr/ADR-004-checkout-one-order-per-farm.md) | Proposed | Q3, Q4, Q6 | 7-step transaction, SQL, order state machine, deadlock-free ordering |
| [005](adr/ADR-005-hot-products.md) | Proposed | Q1 | Definition, ranking query, popularity counter in catalog |
| [006](adr/ADR-006-areas.md) | Proposed | Q2, Q12 | Areas, home area, refuse-then-archive delete |
| [007](adr/ADR-007-deletion-policy.md) | Proposed | Q11, Q12 | Per-entity deletion rules, user anonymisation cascade, audit |

Each ADR follows the template: Context (what the system does / what the requirements contain / what they do not / drivers) · Decision (numbered sub-decisions + "what this ADR does not decide") · Options considered (runner-up named) · Consequences (positive table, negative table with mitigation and residual risk, people, follow-up work) · Compliance · When to revisit · Open questions.

## 2. Decisions taken while writing

| # | Decision | Why |
|---|---|---|
| W1 | **All ADRs are `Proposed`**, including ADR-001 | The user asked for a *proposal*, and no one has chosen yet. The README notes that ADR-001 and ADR-003 depend on no product question and can be accepted on sign-off |
| W2 | **Seven ADRs, not one** | The skill says separate decisions get separate records. Each of 002–007 can change on its own (different open questions) without reopening the style |
| W3 | Areas (ADR-006) and deletion (ADR-007) as their own ADRs, not part of ADR-005 | They answer different open questions (Q2/Q12 vs. Q11) and touch different modules |
| W4 | **Numbering starts at 001** in `new_session/adr/` | Fresh, independent set in a new folder. Continuing the old folder's numbers would suggest these continue those ADRs |
| W5 | Full scoring matrix and ER model **linked, not copied** into ADR-001 | Keeps the ADR self-contained but short. The skill says link long analysis |
| W6 | Defaults for Q1–Q16 written inside the ADRs, labelled "default answer to Qn" | So development can start before the PO answers |
| W7 | Cancel / complete / no-show states designed in ADR-004 but **marked as needing new stories** | They are not in the 41 stories. Building them silently would invent requirements |
| W8 | "Admin is a role, not a module" stated in ADR-001 §2.2 | Prevents an admin module that reads every other module's tables |
| W9 | ADR-002 status waits on Q14 even though Java scored highest | The familiarity score (weight 5) was guessed. A real answer can flip the result |

## 3. Mistakes found by the self-check

| # | Where | Mistake | Fix |
|---|---|---|---|
| E1 | ADR-002 §3, first draft | Totals for TypeScript (76) and Python (74) were mis-added. Correct values are 77 and 78, so Python, not TypeScript, is the runner-up | Fixed in the same file before it was finished (no history to keep). Recorded here for transparency |
| E2 | Notes §5.2, §5.4, §5.5 | Catalog listening to ordering's `OrderPlaced` event → catalog → ordering dependency → **cycle** | Counter moved into `catalog.reserveStock`. Rule "a lower module never listens to a higher module's event" added to ADR-001 §2.4. **Correction** entry in [notes §8.2](NFFH_architecture_notes.md), with visible ⚠ markers on the old text |

Other self-checks that passed: the conditional `UPDATE` touches only catalog's schema. Lines are locked in `product_id` order (deadlock-free). Both `LEFT JOIN` queries (farms by area, hot products) keep their filter in `ON`, so they keep zero-count rows. The ranking counts order lines, never adds quantities of different units. Every story maps to exactly one module (15 + 9 + 10 + 7 = 41).

## 4. One-sentence summary

> Seven Proposed ADRs record a modular monolith for NFFH, with its stack, sessions, the checkout rule (one transaction, one order per farm, atomic conditional stock decrement), and defaults for the three undefined areas of the requirements (hot products, areas, deletion), each waiting on a named open question.

## 5. Suggested next ADRs

1. **Hosting provider and backups** (after the budget answer in Q14).
2. **Order lifecycle stories** (cancel / complete / no-show) once the PO approves them. This may supersede part of ADR-004 §2.6.
3. **Online payment** if it enters scope (Q5): a new `payments` module and order states.
4. **Notifications** (Q7): email on order placed and cancelled.
5. **Password reset and email verification.**

---

*Later follow-up questions and answers are appended below.*

## 6. Follow-up log

*(empty)*
