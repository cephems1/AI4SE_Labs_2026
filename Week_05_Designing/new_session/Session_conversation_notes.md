# NFFH — Session Conversation Notes (new_session)

| | |
|---|---|
| **Date** | 2026-10-27 |
| **Participants** | michaljaros · Claude (architecture consultant, Claude Code in VS Code) |
| **Input** | [../Tasks/data/NFFH.txt](../Tasks/data/NFFH.txt): system description + 41 user stories |
| **Skills used** | `.claude/skills/architecture-decision` (orchestrator) → `architecture-requirements-analysis` → `architecture-options` → `adr-writer` |
| **Result** | Modular monolith proposed (84.3 % vs. 73.0 % BaaS, 48.6 % microservices). 7 Proposed ADRs |

---

## 1. The request (verbatim)

> *"use skills described in .claude to make a proposial of architecture of requirements in @Week_05_Designing/Tasks/data/NFFH.txt , save every output into new folder called new_session, make notes of this converastion and taken decisions"*

## 2. What happened, in order

1. Listed `.claude/` and found four skills: `architecture-decision`, `architecture-requirements-analysis`, `architecture-options`, `adr-writer`, plus templates.
2. Invoked `architecture-decision` and read the three sub-skills and the templates.
3. Read `NFFH.txt` (41 stories).
4. Created `Week_05_Designing/new_session/` and `new_session/adr/`.
5. **Stage 1, requirements analysis:** actors, 8 capability groups covering all 41 stories, 12 missing NFRs with assumed values, 11 weighted drivers, 10 quality-attribute scenarios, 16 open questions. Written to [NFFH_architecture_notes.md §1](NFFH_architecture_notes.md).
6. **Stage 2, options:** modular monolith, microservices and serverless/BaaS explained with diagrams, compared, scored (156 / 90 / 135 of 185) and sensitivity-checked under 3 re-weightings. The winner never changes. Detailed design of the winner. [Notes §2–§7](NFFH_architecture_notes.md).
7. **Stage 3, ADRs:** ADR-001 … ADR-007 and an index. [adr/README.md](adr/README.md), log in [NFFH_ADR_conversation_notes.md](NFFH_ADR_conversation_notes.md).
8. Self-check found 2 mistakes: an arithmetic error in ADR-002 and a dependency cycle in the notes. Both fixed. The second has a visible Correction in notes §8.2.
9. Wrote this file.

## 3. Decisions taken in this session

### 3.1 About the process (meta decisions)

| # | Decision | Why |
|---|---|---|
| M1 | Output folder = `Week_05_Designing/new_session/`, with ADRs in `new_session/adr/` | The user said "new folder called new_session". Placed next to the requirements' task folder, where the skill puts outputs by default |
| M2 | **Fresh run: the earlier outputs in `Week_05_Designing/` were not read** (`NFFH_architecture_notes.md`, `NFFH_ADR_conversation_notes.md`, `Architecture_skills_conversation_notes.md`, `adr/`) | The orchestrator skill says "continue earlier notes", but the user asked for a new folder. I read that as an independent proposal. Not reading the old files also keeps the new result from simply copying them, so the two runs can be compared |
| M3 | Did not read `Tasks/Task_1.md` … `Task_3.md` | The user pointed only at NFFH.txt. The skill says read only the named files |
| M4 | Ran all three stages without stopping | The user asked for a full proposal. The top-two gap (11.4 %) is above the 5 % threshold, and no re-weighting flips the winner |
| M5 | Three notes files instead of one | The skill asks for `<SYSTEM>_architecture_notes.md` (stages 1–2) and `<SYSTEM>_ADR_conversation_notes.md` (stage 3). The user asked for notes of "this conversation", so this file covers the whole session and the meta decisions |
| M6 | Nothing committed to git | The user did not ask for a commit |

### 3.2 About the architecture

| # | Decision | Where |
|---|---|---|
| A1 | **Modular monolith**: one deployable, modules identity / farms / catalog / ordering | ADR-001 |
| A2 | One PostgreSQL, **schema per module**, no cross-schema joins or FKs | ADR-001 §2.5 |
| A3 | Admin is a role, not a module | ADR-001 §2.2 |
| A4 | Calls go downward only. Events go upward only. A lower module never listens to a higher module's event | ADR-001 §2.4 |
| A5 | Java 21 + Spring Boot + Spring Modulith + PostgreSQL + React (pending team skills) | ADR-002 |
| A6 | Server-side sessions, HttpOnly cookie, 30-day sliding expiry, revocable | ADR-003 |
| A7 | Checkout = one transaction, one order per farm, conditional stock `UPDATE`, price confirmation | ADR-004 |
| A8 | Hot = in season + recent order lines in the area | ADR-005 |
| A9 | Areas admin-defined. Client has a home area. Area delete refused while farms use it | ADR-006 |
| A10 | Soft delete everywhere. Deleted users anonymised. Their future orders cancelled | ADR-007 |

## 4. What is still open

* **Product owner:** Q1–Q16 ([notes §1.8](NFFH_architecture_notes.md)). Most important: Q1 hot, Q2 area, Q3 multi-farm cart, Q6 order lifecycle, Q11 deletion meaning.
* **Team:** Q14 skills and budget (can change ADR-002).
* **Sign-off:** ADR-001 and ADR-003 can become `Accepted` as soon as the team agrees.

## 5. Files produced

```
Week_05_Designing/new_session/
├── Session_conversation_notes.md       ← this file
├── NFFH_architecture_notes.md          ← stages 1–2: analysis, options, scoring, design
├── NFFH_ADR_conversation_notes.md      ← stage 3 log
└── adr/
    ├── README.md
    ├── ADR-001-modular-monolith.md
    ├── ADR-002-technology-stack.md
    ├── ADR-003-authentication-sessions.md
    ├── ADR-004-checkout-one-order-per-farm.md
    ├── ADR-005-hot-products.md
    ├── ADR-006-areas.md
    └── ADR-007-deletion-policy.md
```

## 6. One-sentence summary

> Using the four `.claude` architecture skills on NFFH.txt, this session proposes a **modular monolith with one PostgreSQL database**, because the one consistency-critical story (12: reserve stock for a pickup date) and the nine cross-entity admin and history stories are simplest and safest in a single ACID database that a small team can run cheaply. The proposal is recorded as seven Proposed ADRs waiting on named product questions.

---

## 7. Follow-up log

*(append later questions here as `### 7.N "<question>"`)*
