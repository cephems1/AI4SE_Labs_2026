# NFFH — ADR Conversation Notes

| | |
|---|---|
| **Date** | 2026-10-27 |
| **Participants** | Michal Jaros (student) · Claude (architecture consultant) |
| **Topic** | Writing a standalone ADR for the modular monolith chosen for NFFH |
| **Output** | [adr/ADR-001-modular-monolith.md](adr/ADR-001-modular-monolith.md) |
| **Previous conversation** | [NFFH_architecture_notes.md](NFFH_architecture_notes.md): architecture selection (three options, scoring, detailed design) |

---

## 1. The request (verbatim)

> *"create an adr for Modular monolith for rquirements described in @Week_05_Designing/Tasks/data/NFFH.txt. The architecture notes are in @Week_05_Designing/NFFH_architecture_notes.md . In some .md files. make notes of this conversation so it could be referenced later"*

## 2. What was done

1. Read the requirements, [Tasks/data/NFFH.txt](Tasks/data/NFFH.txt) (41 user stories).
2. Read the architecture notes from the previous conversation, which already chose the modular monolith (score 147/170) and contained a short draft ADR in §4 with status "Proposed".
3. Wrote a full, standalone ADR at [adr/ADR-001-modular-monolith.md](adr/ADR-001-modular-monolith.md).
4. Wrote these notes and added a pointer to them in §9.2 of the architecture notes.

`Task_1.md` to `Task_3.md` were not read, in line with the instruction from the previous conversation.

## 3. Decisions taken while writing the ADR

| Choice | Why |
|---|---|
| **Separate `adr/` folder**, file `ADR-001-modular-monolith.md` | Common convention: one file per decision, numbered, so later ADRs (stack choice, auth, etc.) can sit next to it. |
| **Status `Accepted`** (the draft in the notes said `Proposed`) | The previous conversation ended with the modular monolith chosen, and this request asked for an ADR for it. The ADR states that it supersedes the draft in notes §4. |
| **Self-contained, but links to the notes** for detail | An ADR should be readable on its own; the long analysis (option descriptions, full scoring matrix, ER model, API sketch) stays in the notes to avoid duplication. |
| **Decision written as nine concrete sub-decisions** | "Modular monolith" alone is too vague to check. The ADR pins down modules, boundary rules, schema-per-module, transactional checkout, server-side sessions, authorization, REST + SPA, and the Google Maps deep link. |
| **Technology stack left open** | The previous conversation did not choose one. This should be its own ADR (suggested ADR-002). |
| **Added a "Compliance" section** | Turns the decision into things CI can check: boundary tests, the concurrent-checkout test. |
| **Open questions kept, but marked as not overturning the decision** | Q1–Q4 and Q6 change module design, not the architectural style. |

## 4. ADR structure (for quick reference)

1. **Context**: system summary, story groups, missing NFRs and inferred assumptions, ten weighted drivers (D1–D10).
2. **Decision**: one deployable, six modules, boundary rules, one PostgreSQL with schema per module, ACID checkout via conditional `UPDATE`, revocable server-side sessions, role + ownership authorization, REST/JSON + SPA, Google Maps deep link.
3. **Alternatives**: Microservices (80, rejected), Serverless/BaaS (121, runner-up), plain layered monolith (not shortlisted).
4. **Consequences**: positives, negatives with mitigations, follow-up work.
5. **Compliance**: how CI and review enforce the decision.
6. **When to revisit**: multiple teams, divergent scaling needs, cost, data residency. Response is to extract a module, not rewrite.
7. **Open questions**: Q1–Q4, Q6 with current assumptions.

## 5. One-sentence summary

> NFFH is one deployable backend split into six enforced business modules over one PostgreSQL database, because its two hardest requirements, atomic stock reservation and cross-data admin reports, are trivial with one transactional database, and the module seams keep the option to extract services later.

## 6. Suggested next ADRs

| # | Topic |
|---|---|
| ADR-002 | Technology stack (Spring Boot / NestJS / Django) |
| ADR-003 | Authentication: server-side sessions vs. short JWT + refresh token |
| ADR-004 | Multi-farm cart and order split (once Q1 is answered) |
| ADR-005 | Definition of "hot products" (once Q3 is answered) |

---

*Append later follow-ups on the ADR below.*

## 7. Follow-up log

### 7.1 "Decisions and consequences are too short; write also ADR-002 to ADR-005"

**ADR-001 expanded.**

* **Decision** went from nine bullet points to eleven subsections (§2.1–§2.11): runtime and statelessness, module responsibilities (including "not responsible for", and Back-office owning no business tables), internal module layout, dependency rules with two kinds of events (business reaction inside the transaction vs. side effect after commit with outbox), data rules (schema ownership, cross-schema foreign keys only in dependency direction, soft delete, type conventions), checkout step by step, authorization table, API conventions (RFC 9457 errors, generated OpenAPI client), external integrations, and what is left to the other ADRs.
* **Consequences** now has a table of positives with practical meaning and drivers, a table of negatives with practical meaning, mitigation and residual risk, the impact on developers, testers, operators, security reviewers and budget, and a numbered follow-up list. Compliance became a table of checks.

**New ADRs** (index: [adr/README.md](adr/README.md)):

| ADR | Decision | Status | Key reasoning |
|---|---|---|---|
| [ADR-002](adr/ADR-002-technology-stack.md) | Java + Spring Boot + **Spring Modulith**, JPA + `JdbcClient`, Flyway, PostgreSQL, Testcontainers; React + TypeScript + Vite; Docker Compose, GitHub Actions | Proposed | Spring Modulith gives module verification, after-commit events with an outbox and module tests out of the box. NestJS is the fallback if the team is stronger in TypeScript. Django rejected because Django admin would bypass module rules. |
| [ADR-003](adr/ADR-003-authentication-sessions.md) | Opaque session token in an HttpOnly cookie, SHA-256 hash in `identity.user_session`; remember-me 30 days sliding (max 90), admins 8 h; Argon2id; rate limiting; CSRF token; admins seeded; ban = revoke all sessions; GDPR erasure = anonymize | Accepted | JWTs cannot be revoked immediately, which conflicts with logout and ban stories. Spring Session JDBC noted as an acceptable simpler alternative. |
| [ADR-004](adr/ADR-004-cart-and-order-per-farm.md) | Server-side cart, multi-farm, no stock held; checkout all-or-nothing, one order per farm with its own pickup date; pickup tomorrow to +14 days; lifecycle `RESERVED → PICKED_UP / CANCELLED / NO_SHOW` with stock release; idempotency key | Proposed | Pickup is at the farm, so one order per farm is natural. Adds cancel / picked-up / no-show endpoints beyond the stories, because without them reserved stock never returns. |
| [ADR-005](adr/ADR-005-hot-products.md) | Hotness = number of distinct non-cancelled orders in the last 14 days in the client's area; max 3 per farm; in-season fallback; counts kept in Catalog's own table fed by Ordering's events; cached 5 min | Proposed | Counting orders (not quantities) makes kg and pieces comparable; event-fed table respects ADR-001's data ownership. |

**Correction found while writing ADR-005.** The hot-products SQL in [NFFH_architecture_notes.md](NFFH_architecture_notes.md) §5.6.4 has three problems: the 14-day filter sits on a `LEFT JOIN` to `orders` and so filters nothing; it sums quantities across different units; and Catalog reads Ordering's tables, breaking module ownership. ADR-005 replaces it. A note was added to the architecture notes (§9.3).

**Defaults that still need the product owner:** Q1 (multi-farm cart), Q2 (pickup dates), Q3 (hot products), Q4 (order lifecycle), Q6 (GDPR erasure). Q6 is handled with an assumed default inside ADR-003 §2.8.
