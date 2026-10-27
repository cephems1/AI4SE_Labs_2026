# ADR-001: Build NFFH as a modular monolith with one PostgreSQL database

| | |
|---|---|
| **Status** | Proposed (no open question blocks it; waiting only on team sign-off) |
| **Date** | 2026-10-27 |
| **Deciders** | michaljaros, with Claude as architecture consultant |
| **System** | Not Far(m) From Home (NFFH): local farms list produce, clients reserve it and pick it up at the farm |
| **Requirements** | [../../Tasks/data/NFFH.txt](../../Tasks/data/NFFH.txt): system description + 41 user stories |
| **Analysis** | [../NFFH_architecture_notes.md](../NFFH_architecture_notes.md): drivers, scenarios, the three options, full scoring matrix, ER model, API sketch |
| **Supersedes** | Draft ADR in the notes, section 4.1 |
| **Related** | [ADR-002](ADR-002-technology-stack.md) stack · [ADR-003](ADR-003-authentication-sessions.md) sessions · [ADR-004](ADR-004-checkout-one-order-per-farm.md) checkout · [ADR-005](ADR-005-hot-products.md) hot products · [ADR-006](ADR-006-areas.md) areas · [ADR-007](ADR-007-deletion-policy.md) deletion |

---

## 1. Context

### 1.1 What the system does

NFFH is a "km 0" marketplace. Farms publish products with price and available quantity. Clients browse farms and products in their area, fill a cart and complete an order that reserves the stock and fixes a pickup date at the farm. An administrator maintains users, areas and products and looks at platform-wide data. There is no online payment and no delivery.

### 1.2 What the requirements contain

| Group | Stories | Why it matters for this decision |
|---|---|---|
| Identity and sessions | 1–4, 17–20, 22–24 | Persistent but revocable sessions for three roles |
| Catalog and farm inventory | 6, 8, 14–16 | Farms write the same stock that checkout consumes. Ownership rules |
| Cart and **checkout** | 9–12 | **The one consistency-critical workflow**: reserving limited stock |
| Order history | 40, 41 | Must survive price changes and product removal |
| Admin maintenance and reporting | 25–39 | 9 stories (26–28, 31–34, 40, 41) query across users, farms, areas, products and orders |
| Maps | 13 | A link only |

### 1.3 What the requirements do not contain

No NFRs at all. Assumed (notes §1.4): one region, ≤ 5,000 clients, ≤ 200 farms, ≤ 100 concurrent users. 99.5 % availability. GDPR applies. A team of 2–4, one semester, hosting ≤ €30/month. Payment at pickup. All are listed as open questions Q1–Q16 in the notes.

### 1.4 Decision drivers

| # | Driver | Weight | Why |
|---|---|:-:|---|
| D1 | Reservation consistency | 5 | Story 12 vs. 9–11, 14–16 |
| D2 | Simplicity / time-to-market | 5 | 41 CRUD-heavy stories, small team |
| D3 | Security & access control | 4 | 1–4, 17–25, 29; ownership in 14–16 |
| D4 | Cross-entity queries | 4 | 26–28, 31–34, 40, 41 |
| D5 | Operational cost | 4 | Small budget, no on-call |
| D6 | Modifiability | 3 | Payment, cancel and notifications likely next |
| D7 | Testability | 3 | Checkout and ownership rules |
| D8 | Integrity on deletion | 3 | 15, 25, 38, 39 |
| D9 | Scalability | 2 | Regional platform |
| D10 | Availability | 2 | Reservation for a later day |
| D11 | Vendor independence | 2 | Avoid lock-in, not critical |

## 2. Decision

NFFH is built as **one deployable backend** (which also serves the web SPA) made of **four business modules** (identity, farms, catalog, ordering) with enforced boundaries. It uses **one PostgreSQL database with one schema per module**. The checkout runs as **one local ACID transaction**.

### 2.1 Runtime and deployment

* One container image, run as 1 instance (2 possible, since there is no in-memory session state) on a PaaS or small VM.
* One managed PostgreSQL with daily backups and point-in-time recovery if available.
* The SPA is built into the same image and served from the same origin, so cookies need no CORS setup.

### 2.2 Modules and responsibilities

| Module | Responsible for | Not responsible for | Stories |
|---|---|---|---|
| identity | accounts, passwords, roles, sessions, account status, anonymisation | farm data, orders | 1–5, 18–20, 22–25, 27–29 |
| farms | areas, farm profiles, coordinates, pickup weekdays, Maps link | accounts, products | 7, 13, 17, 21, 30–32, 35, 39 |
| catalog | products, stock, prices, units, season, hot ranking | carts, orders | 6, 8, 14–16, 33, 34, 36–38 |
| ordering | carts, checkout, orders, order lines (snapshots), order lists | stock rules (delegated to catalog) | 9–12, 26, 40, 41 |

All 41 stories are mapped to exactly one module. **Admin is a role, not a module.** Admin stories live in the module that owns the data.

### 2.3 Internal layout

Each module has `api/` (public interface, DTOs, events) and `internal/` (domain, persistence, controllers). A `shared/` kernel holds value types only (`Money`, `Quantity(value, unit)`, IDs, clock). The checkout inside ordering uses ports-and-adapters so it can be tested without HTTP.

### 2.4 Dependency rules

1. Synchronous calls only downward: **ordering → catalog → farms → identity** (ordering may also call farms and identity directly). No cycles.
2. Only through the other module's `api/` package.
3. Upward notifications are in-process domain events, published by a lower module and handled by a higher one: `UserDeleted` (identity → farms, ordering), `FarmDeactivated` (farms → catalog, ordering), `ProductArchived` (catalog → ordering). `OrderPlaced` and `OrderCancelled` are published for future modules above ordering (notifications, payments). **A lower module never listens to a higher module's event**, because that would be a dependency cycle. Handlers that must be atomic run in the same transaction. Handlers that may lag run after commit from a persisted event-publication log.
4. The HTTP layer does authentication, role check and calls one module. No business logic.

### 2.5 Data ownership

* Schemas `identity`, `farms`, `catalog`, `ordering`. A module reads and writes **only its own schema**.
* **No SQL joins and no foreign keys across schemas.** References across modules are IDs. Integrity across modules comes from soft delete (IDs never disappear, [ADR-007](ADR-007-deletion-policy.md)) and API checks.
* Foreign keys and `CHECK` constraints are used *inside* a schema (e.g. `CHECK (quantity_available >= 0)`).
* Order lines store snapshots of product name, unit and price.

### 2.6 The critical workflow

The checkout runs in one transaction that spans ordering and catalog. This is allowed because both are in one process and one database. Steps, details in [ADR-004](ADR-004-checkout-one-order-per-farm.md):

1. Lock the client's cart rows.
2. Validate the pickup date per farm (`farms.pickupPolicy`).
3. `catalog.reserveStock(lines sorted by productId)`: a conditional `UPDATE … WHERE quantity_available >= :q` per line. 0 rows affected means insufficient stock.
4. Compare the recomputed total with the total the client confirmed.
5. Insert one order per farm with line snapshots, then clear the cart.
6. Commit. `OrderPlaced` is recorded for after-commit listeners.

Any failure rolls everything back and returns `409` with the failing lines or the new total.

### 2.7 Authentication

Server-side sessions with an opaque token in an HttpOnly cookie, 30-day sliding expiry, revocable. See [ADR-003](ADR-003-authentication-sessions.md).

### 2.8 Authorization

| Action | CLIENT | FARM | ADMIN |
|---|:-:|:-:|:-:|
| Browse areas, farms, products, hot products (6–8, 13) | ✔ | ✔ | ✔ |
| Cart and checkout (9–12) | own | — | — |
| My orders (40, 41) | own | own farm | — |
| Products create / update / remove (14–16, 36–38) | — | own farm only | any |
| Users list / detail / modify / delete (25, 27–29) | — | — | ✔ |
| Areas create / delete (35, 39) | — | — | ✔ |
| Platform lists (26, 30–34) | — | — | ✔ |

Ownership is enforced **inside the module service**, not only at the controller.

### 2.9 API conventions

REST + JSON under `/api`, admin endpoints under `/api/admin`. Paged lists. Errors as RFC 9457 problem details. `409` for stock and price conflicts, `403` for ownership violations, `422` for validation. Full sketch in the notes §5.6.

### 2.10 External integrations

Google Maps only as a URL (`https://www.google.com/maps/search/?api=1&query=<lat>,<lng>`). No API key, no server call.

### 2.11 What this ADR does not decide

* Language, framework and hosting provider → [ADR-002](ADR-002-technology-stack.md).
* Session details → [ADR-003](ADR-003-authentication-sessions.md).
* Order splitting, pickup-date rules and price changes → [ADR-004](ADR-004-checkout-one-order-per-farm.md).
* Meaning of "hot products" → [ADR-005](ADR-005-hot-products.md). Meaning of "my area" → [ADR-006](ADR-006-areas.md).
* What deleting users, products and areas does → [ADR-007](ADR-007-deletion-policy.md).
* Payment and notifications (out of scope for v1).

## 3. Options considered

| Option | Score (of 185) | Why not chosen |
|---|:-:|---|
| **A. Modular monolith** | **156 (84.3 %)** | **Chosen** |
| C. Serverless / BaaS (managed auth + Postgres with RLS + functions) | 135 (73.0 %) | **Runner-up.** Business rules spread across RLS, SQL functions and client. Weaker testability and modifiability, delayed token revocation, high lock-in |
| B. Microservices (gateway, DB per service, broker, sagas) | 90 (48.6 %) | Turns checkout into a saga and admin queries into an eventually-consistent read model. Highest cost and team size, for scalability nobody asked for |

Sensitivity (notes §3.5): A stays first under "demo in two weeks" (83.6 % vs. C 79.4 %), "national rollout" (81.4 % vs. C 71.0 %) and "no servers, zero budget" (82.6 % vs. C 76.3 %).

### 3.1 Serverless / BaaS (runner-up)

It is the fastest and cheapest way to start, with auth and persistent sessions built in, and it would make the checkout atomic through a SQL function. It lost because NFFH's rules (ownership, deletion cascades, checkout, hot ranking) would live in RLS policies and PL/pgSQL scattered over many tables. That is harder to test (D7) and change (D6). One missed policy leaks data (D3). And everything is tied to one provider (D11).

### 3.2 Microservices (rejected)

The decisive problem is D1: with stock in the Catalog service and orders in the Order service, the checkout becomes a saga with `PENDING` orders, compensation and an asynchronous answer to the client. The answer to the stated requirement gets worse, and nothing in the requirements pays for it.

### 3.3 Classic layered monolith (not shortlisted)

Same deployment as A without module boundaries. Rejected because it has no guard against erosion and no extraction path.

## 4. Consequences

### 4.1 Positive

| Consequence | Practical meaning | Driver |
|---|---|---|
| Checkout is one ACID transaction | Stock can't go negative, no partial multi-farm checkout, simple code | D1 |
| One deployable, one DB | One pipeline, one log, one backup; a 2–4 person team can run it | D2, D5 |
| Admin and history lists are plain queries in one process | No read model, no staleness | D4 |
| Whole app testable in-process against a real PostgreSQL | Fast, deterministic integration tests including concurrency | D7 |
| Modules own schemas | Clear ownership, and a module can be extracted later | D6 |
| Server-side sessions are trivial here | Logout and admin delete take effect on the next request | D3 |

### 4.2 Negative, and how they are handled

| Consequence | Practical meaning | Mitigation | Residual risk |
|---|---|---|---|
| Boundaries can erode | Someone joins across schemas "just once" | Architecture tests in CI, review rule | Low |
| Checkout transaction couples ordering and catalog | Extracting catalog later needs a saga | Documented. The coupling sits behind `reserveStock` | Low (no extraction planned) |
| No FKs across schemas | DB doesn't catch a dangling cross-module ID | Soft delete only (ADR-007), API checks, tests | Low |
| No fault isolation | A bug that crashes the process takes everything down | PaaS auto-restart, 2 instances possible | Medium, accepted (D10 = 2) |
| Scales as one unit | Can't scale browsing separately | Read replica first, extraction later | Low at assumed scale |

### 4.3 Impact on the people involved

* **Developers:** one repo, one language, one local run (app + Postgres in Docker). They must learn and respect the module rules.
* **Testers:** can test the whole flow in-process. The concurrency test is a CI job, not a manual check.
* **Operators:** one service, one DB, one dashboard. No broker, no cluster.
* **Security reviewers:** one auth filter and one place per module for ownership checks.
* **Budget:** roughly one small instance plus a small managed DB *(assumed €10–25/month)*.

### 4.4 Follow-up work this decision creates

1. Decide the stack (ADR-002) and create the repo skeleton with the four modules and empty `api/` packages.
2. Add the architecture tests before any feature code.
3. Write migrations per schema.
4. Implement the checkout with its concurrency test first (ADR-004).
5. Implement sessions (ADR-003) and the deletion procedures (ADR-007).
6. Get answers to Q1–Q16 from the product owner.

## 5. Compliance: how we know the decision is followed

| Check | How | When |
|---|---|---|
| No cycles, calls only via `api/` | Architecture test (e.g. Spring Modulith `verify()` / ArchUnit / dependency-cruiser) | Every CI build |
| No cross-schema SQL | Test that scans repository SQL for other schemas, plus a DB role per module where the framework allows it | Every CI build |
| Stock never negative | 50 parallel checkouts on stock 2 → exactly 2 orders, stock = 0 | Every CI build |
| Multi-farm checkout is all-or-nothing | Integration test with one short line | Every CI build |
| Ownership enforced | Test matrix: each product endpoint × {own farm, other farm, client, admin} | Every CI build |
| One deployable | Pipeline produces exactly one image | Review of pipeline changes |
| ADR respected in design changes | PR template asks "does this change a module boundary or the schema ownership?" | Every PR |

## 6. When to revisit

| Trigger | Response |
|---|---|
| Sustained load beyond one server, or a national rollout | Read replica for browsing. Then extract the hottest module (likely catalog browsing). Don't rewrite |
| Three or more teams working in parallel | Give each team module ownership. Consider extracting modules that release independently |
| Online payment added | New `payments` module and new order states. This ADR still holds |
| Goal changes to a throw-away demo in days | Re-score. Option C was within 4.2 % in that scenario |
| Boundary violations keep appearing in review | Tighten the tests (DB roles per schema) before considering anything else |

## 7. Open questions that may refine, but not overturn, this decision

| # | Question | Current default |
|---|---|---|
| Q8 | Expected scale and region | One region, ≤ 100 concurrent users |
| Q9 | Availability and support hours | 99.5 %, best effort |
| Q14 | Team size, skills, budget | 2–4 developers, ≤ €30/month (affects ADR-002, not this ADR) |
| Q5 / Q7 | Payment, notifications | Out of v1. Would be new modules |
