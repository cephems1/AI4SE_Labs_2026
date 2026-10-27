# ADR-002: Use Java 21 + Spring Boot with Spring Modulith, PostgreSQL and a React SPA

| | |
|---|---|
| **Status** | Proposed (waiting on Q14: team skills) |
| **Date** | 2026-10-27 |
| **Deciders** | michaljaros, with Claude as architecture consultant |
| **System** | Not Far(m) From Home (NFFH) |
| **Requirements** | [../../Tasks/data/NFFH.txt](../../Tasks/data/NFFH.txt) |
| **Analysis** | [../NFFH_architecture_notes.md](../NFFH_architecture_notes.md) §5.7 (stack options), §5.8 (deployment) |
| **Supersedes** | — |
| **Related** | [ADR-001](ADR-001-modular-monolith.md) architecture style · [ADR-003](ADR-003-authentication-sessions.md) sessions |

---

## 1. Context

### 1.1 What the system does

See ADR-001 §1.1. ADR-001 fixes a modular monolith with four modules, one PostgreSQL with a schema per module, a checkout in one ACID transaction, in-process domain events with a persisted publication log, and server-side sessions.

### 1.2 What the requirements contain

Nothing about technology. What matters for the stack:
* stories 9–12 need reliable transactions and row-level conditional updates;
* 3, 19, 23 need persistent sessions;
* the client and farm stories (6–16) are used on phones, so the SPA must be responsive;
* 26–34 are admin tables with filters and paging.

### 1.3 What the requirements do not contain

Team size, skills, deadline and budget (Q14). **Assumed:** 2–4 developers who know at least one of Java, TypeScript or Python from courses. One semester. Hosting ≤ €30/month.

### 1.4 Decision drivers

| # | Driver | Weight | Why |
|---|---|:-:|---|
| S1 | Team already knows it | 5 | Biggest effect on time-to-market (ADR-001 D2) |
| S2 | First-class module boundary enforcement | 4 | ADR-001 depends on it (compliance §5) |
| S3 | Mature transactions and PostgreSQL support | 4 | Checkout (D1) |
| S4 | Built-in session and security support | 3 | ADR-003 |
| S5 | Ecosystem for testing against a real DB | 3 | Concurrency test (QAS1) |
| S6 | Cheap to host | 2 | D5 |

## 2. Decision

**Default stack (to confirm against Q14):**

### 2.1 Backend

Java 21, Spring Boot 3.x, **Spring Modulith** (one top-level package per module, `verify()` architecture test, persisted event publication registry for after-commit events), Spring Security, Spring Data JDBC (or JPA), Flyway migrations with one folder per schema.

### 2.2 Database

PostgreSQL 16, managed. Schemas `identity`, `farms`, `catalog`, `ordering`, plus `event_publication` (Spring Modulith) and `audit`.

### 2.3 Frontend

React + TypeScript built with Vite, one SPA with three role-based areas (client, farm, admin). Built into the backend image and served from the same origin. Mobile-first CSS. i18n with IT and EN (Q15).

### 2.4 Testing

JUnit 5, Testcontainers (real PostgreSQL), ArchUnit + Spring Modulith `verify()`, Playwright for a few end-to-end flows (register → add to cart → checkout).

### 2.5 Build, hosting and operations

Gradle or Maven. One Docker image. GitHub Actions CI. A PaaS that runs containers plus managed PostgreSQL (any provider with an EU region, because of GDPR). Structured JSON logs, Spring Actuator health and metrics.

### 2.6 What this ADR does not decide

The specific PaaS vendor and the UI component library. Either can change without a new ADR.

## 3. Options considered

| Option | S1 (5) | S2 (4) | S3 (4) | S4 (3) | S5 (3) | S6 (2) | Total (max 105) |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **Java / Spring Boot + Modulith + React** | 3 | 5 | 5 | 5 | 5 | 3 | **85** |
| Python / Django (+ HTMX or React) | 3 | 3 | 4 | 5 | 4 | 4 | 78 |
| TypeScript / NestJS + Prisma/Kysely + React | 4 | 3 | 4 | 3 | 4 | 4 | 77 |

Arithmetic: Java 15+20+20+15+15+6 = 85. Python 15+12+16+15+12+8 = 78. TypeScript 20+12+16+9+12+8 = 77.

S1 is **scored as unknown (3) for Java and Python** and 4 for TypeScript, because a team that writes React already knows TypeScript. **This is the score that Q14 can flip:** if the team rates its Python or TypeScript as 5 and its Java as 1–2, Java loses 5–10 points and drops to 75–80. That is below Python with S1 = 5 (88) and TypeScript with S1 = 5 (82).

### 3.1 Python / Django (runner-up)

Excellent built-in sessions, admin UI and ORM. It could even replace parts of the admin stories with Django admin. It lost on S2: apps are not isolated by default, and import-linter is needed to enforce boundaries.

### 3.2 TypeScript / NestJS

One language from front to back, and NestJS modules map well to ADR-001's modules. It lost on S2 (boundaries need extra tooling such as dependency-cruiser, and nothing is built into the framework) and on S4 (sessions and CSRF need assembling from libraries).

## 4. Consequences

### 4.1 Positive

| Consequence | Practical meaning | Driver |
|---|---|---|
| Module rules checked by the framework | `verify()` fails the build on cycles or internal access | S2, ADR-001 §5 |
| Event publication registry | After-commit events (e.g. `OrderPlaced` for a future notifications module) are not lost on a crash | S3 |
| Spring Security sessions + CSRF | ADR-003 is mostly configuration | S4 |
| Testcontainers | The concurrency test runs against real PostgreSQL in CI | S5 |

### 4.2 Negative, and how they are handled

| Consequence | Practical meaning | Mitigation | Residual risk |
|---|---|---|---|
| Two languages (Java + TS) | Context switching | Clear split: backend team / frontend team, or pair | Low |
| JVM memory footprint | Slightly bigger instance | 512 MB–1 GB is enough at this scale | Low |
| Spring learning curve | Slower first weeks if unknown | Starter template. Stick to a small subset | Medium if Q14 says "no Java" |

### 4.3 Impact on the people involved

Developers need Java 21 and Node for the SPA build. Operators handle one image. The budget is unchanged from ADR-001.

### 4.4 Follow-up work

1. Ask the team (Q14). If Java is unknown, switch to the runner-up and record it as a new ADR that supersedes this one.
2. Generate the project skeleton with the four module packages and `ModularityTests`.
3. Set up CI with Testcontainers.

## 5. Compliance

| Check | How | When |
|---|---|---|
| Modules verified | `ApplicationModules.of(App.class).verify()` test | Every build |
| No cross-schema SQL | ArchUnit rule + review | Every build / PR |
| Migrations per schema | Flyway locations per module | Every build |

## 6. When to revisit

| Trigger | Response |
|---|---|
| Q14 answer: the team does not know Java | Supersede with the TypeScript or Python option |
| Hosting cost above budget | Smaller JVM settings, or a GraalVM native image |

## 7. Open questions

| # | Question | Current default |
|---|---|---|
| Q14 | Team skills, size, budget | 2–4 developers, Java + TS acceptable |
| Q15 | Languages, devices | IT + EN, responsive web |
