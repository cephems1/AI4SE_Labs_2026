# NFFH: Comparison of the Original Run and the Skill-Based Run (`new_session/`)

| | |
|---|---|
| **Date** | 2026-10-27 |
| **Requirements** | [Tasks/data/NFFH.txt](Tasks/data/NFFH.txt): 41 user stories |
| **Original run** | Two manual conversations: [NFFH_architecture_notes.md](NFFH_architecture_notes.md), [NFFH_ADR_conversation_notes.md](NFFH_ADR_conversation_notes.md), [adr/](adr/README.md) (ADR-001 to ADR-005) |
| **Skill-based run** | One session with the four `.claude/skills/` skills built in [Architecture_skills_conversation_notes.md](Architecture_skills_conversation_notes.md): [new_session/](new_session/Session_conversation_notes.md) (ADR-001 to ADR-007) |
| **Independence** | The new session says it did not read the original outputs ([new_session/Session_conversation_notes.md](new_session/Session_conversation_notes.md), M2). The two runs can therefore be compared as independent attempts at the same task. |

---

## 1. Summary

* **The main decision is the same.** Both runs choose a **modular monolith with one PostgreSQL database and a schema per module**. Both compare it with the same two alternatives, and both rank Serverless/BaaS second and Microservices last. Both choose Java + Spring Boot + Spring Modulith + React, and server-side revocable sessions. Both use one order per farm and a conditional `UPDATE` at checkout.
* **The design inside the monolith differs.** The new run has **4 modules instead of 6**: no separate Cart or Back-office module, because admin is a role and not a module. It also **forbids all cross-schema joins and foreign keys**, where the original allowed them in the dependency direction.
* **"Hot products" got a different definition.** The original defines it by popularity, with being in season as a fallback. The new run requires the product to be in season and uses popularity only to rank the results.
* **The new run is more systematic.** It writes numeric NFR assumptions, 10 full quality-attribute scenarios, 16 open questions, 11 drivers, a sensitivity check with computed numbers, and 7 smaller ADRs. It also caught its own mistakes before finishing. The original run found its mistakes only later, when the user asked follow-up questions.
* **The original ADRs go deeper in some areas.** ADR-001 lists more consequences. ADR-003 covers more session edge cases. ADR-004 adds an idempotency key and a fuller order lifecycle.
* **The comparison exposed a likely defect in the original ADR-005.** Catalog listens to Ordering's `OrderPlaced` event and calls `Ordering.countOrdersByProductAndDay`. That creates a Catalog → Ordering dependency, which is a cycle against ADR-001's own dependency diagram. The new session found the same cycle in its own draft and fixed it (§6.1).

---

## 2. Process

| Aspect | Original run | New run (skills) |
|---|---|---|
| Conversations | 2 (architecture selection, then ADRs) plus 2 follow-ups from the user | 1 session, all three stages without stopping |
| Who chose the architecture | The user, after the recommendation | Nobody yet. The run produced a *proposal* |
| Notes files | 2 (architecture notes, ADR notes) | 3 (architecture notes, ADR notes, a session file with meta decisions M1–M6) |
| How errors were found | By the user's follow-up "decisions and consequences are too short", and while writing ADR-005 (the broken hot-products SQL) | By the skill's built-in self-check while writing the ADRs: 2 errors (arithmetic in ADR-002, a dependency cycle) |
| How corrections were recorded | A visible correction note in the notes (§9.3) | A visible correction note (§8.2), plus ⚠ markers next to the old text |
| Depth of the first ADR draft | Short. It was expanded only after the user complained | Full structure from the start (the skill encodes the "too short" lesson) |

**What this shows.** The skills captured the lessons from the original conversations. Consequence tables, a self-check of every query, visible corrections and splitting decisions into separate ADRs all appear without being asked for. What was lost is the user acting as decider: the new run stays at `Proposed` everywhere.

---

## 3. Requirements analysis (stage 1)

| Item | Original | New |
|---|---|---|
| Capability groups | 10 groups. Some stories appear in two groups (e.g. 17) | 8 groups (C1–C8). **Every story in exactly one group, with the total checked = 41** |
| Missing NFRs | Qualitative ("regional", "small team") | **Quantified assumptions**: ≤ 5,000 clients, ≤ 100 concurrent users, p95 < 500 ms, 99.5 %, RPO 24 h, ≤ €30/month, 2–4 developers |
| Drivers | 10, Σ weights 34, max 170 | 11, Σ weights 37, max 185. **Adds D8 "Integrity on deletion"** |
| Quality-attribute scenarios | 6, short form | 10, full form (source, stimulus, environment, response, measure). Adds a price change in the cart (QAS2), a multi-farm all-or-nothing checkout (QAS3) and deleting a product that has orders (QAS9) |
| Open questions | Q1–Q10 | Q1–Q16. New: units/step (Q16), what an admin may edit (Q13), team skills (Q14), the meaning of "my area" (Q2) |
| Styles considered but not shortlisted | 4 | 6 (adds micro-kernel, space-based, offline-first) |

> **Watch the numbering.** The question numbers differ between the runs. "Hot products" is **Q3** in the original and **Q1** in the new run. The multi-farm cart is **Q1** in the original and **Q3** in the new run.

---

## 4. Options and scoring (stage 2)

### 4.1 Results

| Option | Original score | Original % | New score | New % |
|---|:-:|:-:|:-:|:-:|
| A. Modular monolith | 147 / 170 | 86 % | 156 / 185 | 84.3 % |
| C. Serverless / BaaS | 121 / 170 | 71 % | 135 / 185 | 73.0 % |
| B. Microservices | 80 / 170 | 47 % | 90 / 185 | 48.6 % |
| Gap between A and C | 26 points | 15 % | 21 points | 11.4 % |

The ranking and the size of the gaps are almost identical, even though the two scorings were done independently.

### 4.2 Scores that differ (same driver in both runs)

| Driver | Option | Original | New | Comment |
|---|---|:-:|:-:|---|
| Ops cost | A | 5 | 4 | The new run gives the cheapest-to-run score to BaaS |
| Ops cost | C | 4 | 5 | |
| Modifiability | B | 3 | **5** | The new run rewards changes that stay inside one service. The original penalised changes that cross services |
| Testability | A | 4 | 5 | |
| Vendor independence | A | 5 | 4 | |
| Scalability | C | 5 | 4 | |
| Integrity on deletion (new driver) | A / B / C | n/a | 4 / 2 / 4 | Scores A lower because the new run forbids cross-schema foreign keys |

### 4.3 Sensitivity check

| | Original | New |
|---|---|---|
| Scenarios | 3 ("demo in two weeks", "national rollout", "no cloud") | 3 ("demo in two weeks", "national rollout", "zero budget") |
| Computed numerically | Only the first (A 157 vs. C 144). The other two are argued in words | **All three**, with the changed weights and the new maximum shown |
| Closest call | — | "Demo in two weeks": A 83.6 % vs. C 79.4 % (4.2 points). Written into ADR-001 as a revisit trigger |

---

## 5. ADR by ADR

### 5.1 Overview

| Topic | Original | New |
|---|---|---|
| Architecture style | ADR-001, **Accepted** | ADR-001, **Proposed** |
| Technology stack | ADR-002, Proposed | ADR-002, Proposed |
| Authentication | ADR-003, **Accepted** | ADR-003, **Proposed** |
| Cart and checkout | ADR-004, Proposed | ADR-004, Proposed |
| Hot products | ADR-005, Proposed | ADR-005, Proposed |
| Areas | Not an ADR (notes §5.6.5 only) | **ADR-006**, Proposed |
| Deletion and anonymisation | Inside ADR-003 §2.8 and notes §5.6.6 | **ADR-007**, Proposed |
| Size | 975 lines in 5 ADRs | 1,110 lines in 7 ADRs. Each ADR is shorter |
| Template | Context · Decision · Alternatives · Consequences · Compliance · Revisit | Same, plus a fixed context structure (does / contains / does not contain / drivers), its own **drivers per ADR**, "what this ADR does not decide" and an **Open questions** section in each ADR |

**Status.** The original accepted ADR-001 and ADR-003 because the user had already chosen. The new run kept everything `Proposed` because the user asked only for a *proposal* (W1). Both choices are correct for their requests.

### 5.2 ADR-001: Modular monolith

| Decision point | Original | New |
|---|---|---|
| Modules | **6**: Identity & Access, Directory, Catalog & Inventory, Cart, Ordering, Back-office | **4**: identity, farms, catalog, ordering. Cart is part of ordering |
| Admin stories | A **Back-office module** that owns no business tables. Admin writes go through the owning module. Admin reads use cross-schema **reporting views** | **"Admin is a role, not a module."** Each admin story lives in the module that owns its data |
| Cross-schema foreign keys | **Allowed** in the dependency direction, and listed as an extraction cost | **Forbidden**. References are plain IDs, and integrity comes from soft delete (ADR-007) |
| Cross-schema reads | Allowed in Back-office's read-only views | **Forbidden**. Admin "all orders" = a page of orders plus one batch lookup of names each from identity and farms |
| Event rule | Two kinds: business reaction (same transaction) and side effect (after commit, outbox) | The same two kinds, **plus the explicit rule "a lower module never listens to a higher module's event"** |
| SPA hosting | Nginx serves the SPA. `/api` is proxied to the app | The SPA is built into the backend image and served from the same origin |
| Internal layout | `api / web / application / domain / infrastructure` | `api / internal`, with ports and adapters only in checkout |
| Consequences | 10 positive, 9 negative with mitigations | 6 positive, 5 negative with mitigation **and residual risk** |
| Compliance | 5 checks | 7 checks, including a scan for cross-schema SQL, a test with 50 parallel checkouts and a PR template question |

**Trade-off.** The new run's stricter data rules keep modules easier to extract. The cost is that the admin cross-entity stories need composition in application code instead of SQL joins. Cross-entity admin queries (D4) were one of the two main reasons for choosing the monolith. The new run still scores A at 5 on that driver, but the advantage over the alternatives is smaller than the score suggests.

### 5.3 ADR-002: Technology stack

| | Original | New |
|---|---|---|
| Choice | Java + Spring Boot + Spring Modulith, JPA + `JdbcClient`, Flyway, PostgreSQL, React + Vite | Java 21 + Spring Boot 3 + Spring Modulith, Spring Data JDBC (or JPA), Flyway, PostgreSQL 16, React + Vite |
| How the options were compared | Qualitative table with 9 criteria | **Weighted scoring**: Java 85, Python 78, TypeScript 77 (out of 105) |
| Runner-up | **NestJS** | **Django** |
| View on Django | Rejected: Django admin would bypass the module rules | Runner-up: lost only on module boundary enforcement |
| Frontend detail | Rich: TanStack Query, React Hook Form, i18next, generated OpenAPI client | Lighter. Adds **Playwright** end-to-end tests |
| Deciding assumption | A1: the team knows Java | Q14: team skills. Says explicitly that the familiarity score can flip the result |

### 5.4 ADR-003: Authentication

The mechanism is the same: an opaque 256-bit token, only its SHA-256 hash stored, an `HttpOnly; Secure; SameSite=Lax` cookie, a 30-day sliding expiry with a 90-day absolute maximum, Argon2id, rate limiting and a CSRF token. The differences are in the details:

| Detail | Original | New |
|---|---|---|
| Logout | Sets `revoked_at` (the row is kept) | **Deletes** the row |
| Without "remember me" | Browser-session cookie, 2 h idle, 12 h max | No such variant. Every login gets 30 days |
| Admin session | 8 h idle, 7 days max | 12 h sliding, 7 days max |
| Cookie path | `/api` | `/` |
| CSRF pattern | Cookie-to-header (`XSRF-TOKEN`) | Synchronizer token (`X-CSRF-Token`) |
| Sliding-expiry write | At most every 5 min | At most every 1 hour |
| Effect of a ban | Status `BANNED`, sessions revoked | Status `DELETED`, anonymised, sessions deleted (ADR-007) |
| Options compared | 5, including **Spring Session JDBC** as an acceptable fallback | 4, including **JWT in `localStorage`** (rejected because of XSS) |
| Extras | Password change, "active sessions" view, e-mail verification column, seeded admin with one-time password | Optional TOTP MFA for admins (Q13) |

### 5.5 ADR-004: Cart and checkout

Both runs use a **multi-farm cart, one order per farm, all-or-nothing checkout, stock reserved only at checkout, pickup from tomorrow up to 14 days ahead, line snapshots and a `checkout_id`**.

| Detail | Original | New |
|---|---|---|
| Focus of the ADR | Cart and order model | The checkout transaction, with the SQL and 7 numbered steps |
| Protection against double submit | **`Idempotency-Key` header** | `SELECT … FOR UPDATE` on the cart rows |
| Price change while in the cart | Server computes the total; the cart shows live prices | **The client sends `expectedTotal`; a different total gives `409` with the new total** (QAS2) |
| Pickup days | Any day. Farm opening days may come later | Farm's `pickup_weekdays` **already in the design** |
| States | `RESERVED → PICKED_UP / CANCELLED / NO_SHOW` | `RESERVED → COMPLETED / CANCELLED / NO_SHOW` |
| Stock on `NO_SHOW` | **Released**, plus an automatic no-show 7 days after the pickup date | **Not released** (the produce may have spoiled). The farm adjusts stock by hand |
| Building endpoints that no story asks for | Built and flagged | Designed, but **built only after the product owner approves new stories** (W7) |
| Extra safety | — | `CHECK (quantity_available >= 0)`, `version` increment, the case of a farm editing stock during a checkout (§2.5), a deadlock test run 100 times |

### 5.6 ADR-005: Hot products (largest difference)

| | Original | New |
|---|---|---|
| Reading of story 6 | "Hot" = **popular now**. Season is the fallback | "In the season" = **required**. Popularity only ranks |
| Season data | Boolean `in_season` flag | Month range `season_from_month`–`season_to_month`, which can wrap over New Year |
| Popularity measure | Distinct orders in 14 days, **excluding cancelled and no-show** | Order lines in 14 days. **Cancelled orders still count** (accepted) |
| How the counter is fed | **After-commit events from Ordering** (`OrderPlaced`, `OrderCancelled`, `OrderNoShow`) through an outbox, plus a rebuild command that calls Ordering | **Inside `catalog.reserveStock`**, in the checkout transaction. No event and no call to Ordering |
| List | 12 items, **max 3 per farm**, a `reason` label (`POPULAR` / `IN_SEASON`), cached 5 min | 20 items, no per-farm cap, no cache, behind a replaceable `HotProductPolicy` |
| Cold start | Fills with in-season products | Ranking falls back to alphabetical order |

The original list is better for users: fair across farms, honest labels, and it ignores cancelled orders. The new design is better for the architecture: it has no dependency cycle and is easier to replace. See §6.1.

### 5.7 ADR-006 and ADR-007 (new run only)

* **ADR-006 Areas.** Admin-defined named areas, one area per farm, a home area for each client that they can change while browsing. Deleting an area is refused while farms use it, after which the area is archived. The original reached the same rules in notes §5.6.5, but never made them an ADR.
* **ADR-007 Deletion.** Soft delete everywhere and anonymisation of deleted users. A cascade across 4 modules through `UserDeleted`, `FarmDeactivated` and `ProductArchived`, and an audit table. The original covered part of this in ADR-003 §2.8 (ban, with anonymisation only as a manual admin action). The new run makes it a cross-cutting decision, because without cross-schema foreign keys it is needed for integrity.

---

## 6. Correctness findings from the comparison

### 6.1 Dependency cycle in the original ADR-005 (likely defect, still open)

* Original ADR-001 §2.4 allows **Ordering → Catalog** and says events are for a *lower* module causing a reaction in a *higher* one.
* Original ADR-005 §2.3 makes **Catalog listen to Ordering's `OrderPlaced`, `OrderCancelled` and `OrderNoShow`**. Its rebuild command calls **`Ordering.countOrdersByProductAndDay`** directly.
* Both create a **Catalog → Ordering** dependency, so there is a cycle. Spring Modulith's `verify()`, which ADR-005 §5 says "still passes", would most likely report it, because a listener that uses another module's event type depends on that module.
* The new session made **the same mistake in its first draft** (notes §5.2), found it with the self-check and fixed it (notes §8.2, new ADR-001 §2.4, new ADR-005 §2.3).
* **Suggested fix for the original:** move the counter update into `Catalog.reserveStock` / `releaseStock`, as the new run does. Or move the popularity read model into Ordering (or a module above it) and let Catalog ask it through an interface owned by Catalog. The first option keeps the original's exclusion of cancelled orders, as long as `releaseStock` decrements the counter.

### 6.2 Smaller points

| # | Where | Finding |
|---|---|---|
| 1 | New ADR-005 §2.4 | `pp.day >= CURRENT_DATE - 14` covers **15** calendar days (today plus 14). The original used `- 13`. Minor off-by-one |
| 2 | New ADR-005 §4.2 | Cancelled orders still count. The ADR says `releaseStock` "can decrement it if the PO cares", but that is a one-line change that would match the original's better behaviour |
| 3 | New ADR-001 §5 / D4 | Admin "all orders filtered by area" needs three module calls. The design is correct, but the D4 score of 5 is generous given the stricter rules |
| 4 | Original ADR-001 §1.2 | Counts 15 admin stories (25–39) but the notes count 18 (22–39). Both are right, but they group the stories differently |
| 5 | Original notes §5.6.4 | The broken hot-products SQL is still in the notes, and only a correction note at the end warns about it. The new run puts ⚠ markers next to the wrong text itself |

---

## 7. Conclusions

1. **The architecture decision is stable.** Two independent runs reached the same style, the same runner-up, nearly the same scores, the same stack and the same authentication mechanism. That is good evidence that the decision follows from the requirements and not from the wording of one conversation.
2. **The skills made the output more systematic and self-checking.** Quantified assumptions, complete story mapping, computed sensitivity, per-ADR drivers and open questions, and errors caught before the user saw them. These are the lessons from the original follow-ups, now applied automatically.
3. **The differences are in design choices that the requirements leave open:** the module cut (6 vs. 4), cross-schema rules, the meaning of "hot", no-show stock, and idempotency. These are exactly the points the open questions flag. Different but defensible answers are expected there.
4. **Each run has something the other should adopt:**
   * *Original → new:* idempotency key, max products per farm and `reason` labels for hot products, excluding cancelled orders from popularity, the "no remember me" session variant, Spring Session JDBC as a fallback.
   * *New → original:* fix the Catalog → Ordering cycle (§6.1), the price-confirmation `409` (QAS2), the `CHECK` constraint, pickup weekdays, ADRs for areas and deletion, and per-ADR open questions.
5. **Possible skill improvements:** (a) tell the orchestrator to ask whether earlier outputs should be continued or ignored, instead of guessing; (b) add "check every event listener's direction against the dependency diagram" to the self-check list, since both runs made the same cycle mistake; (c) keep the question numbering stable across runs (e.g. derive it from capability order) to make comparisons easier.
