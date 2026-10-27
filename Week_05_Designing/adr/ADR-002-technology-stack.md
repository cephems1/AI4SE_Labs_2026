# ADR-002: Technology stack — Spring Boot with Spring Modulith, PostgreSQL, React

| | |
|---|---|
| **Status** | Proposed: confirm the team's language experience (assumption A1) before accepting |
| **Date** | 2026-10-27 |
| **Deciders** | Michal Jaros (student), with Claude as architecture consultant |
| **Depends on** | [ADR-001](ADR-001-modular-monolith.md): modular monolith |
| **Related** | [ADR-003](ADR-003-authentication-sessions.md) authentication |

---

## 1. Context

[ADR-001](ADR-001-modular-monolith.md) chose a modular monolith but left the stack open. The stack must make the decisions in ADR-001 **easy to keep**, not just possible:

| Need from ADR-001 | What the stack must provide |
|---|---|
| Six modules with enforced boundaries (§2.4) | a way to define modules and **fail the build** on forbidden imports and cycles |
| Business-reaction and side-effect events (§2.4) | in-process events, both inside the transaction and after commit, with an outbox for after-commit events |
| Checkout as one transaction across modules (§2.6) | declarative transactions and direct SQL for the conditional `UPDATE` |
| PostgreSQL, schema per module, migrations per module (§2.5) | a mature migration tool that supports several schemas |
| Server-side sessions, CSRF, role and method-level authorization (§2.7, §2.8) | a mature security framework |
| OpenAPI-described REST API (§2.9) | OpenAPI generation from code |
| End-to-end tests against real PostgreSQL (§5) | Testcontainers support |

### Assumptions

* **A1.** The team (students) has used **Java** in university courses and knows it better than TypeScript on the backend or Python web frameworks. *Must be confirmed; if false, see §6.*
* **A2.** The team has some **React** or general JavaScript experience for the frontend.
* **A3.** Hosting is a single Linux VM or a container PaaS; there is no Kubernetes.

---

## 2. Decision

### 2.1 Backend

| Concern | Choice | Notes |
|---|---|---|
| Language | **Java**, current LTS release (21 or 25) | records for DTOs and value objects |
| Framework | **Spring Boot**, current stable release line | |
| Module structure and enforcement | **Spring Modulith** | each top-level package under `nffh` is a module; `ApplicationModules.of(NffhApplication.class).verify()` runs as a unit test and fails on forbidden access and cycles |
| Events | Spring application events + **Spring Modulith event publication registry** | business reactions: `@EventListener` (same transaction); side effects: `@ApplicationModuleListener` (after commit, stored in the `event_publication` table and retried if the app crashes) |
| Persistence | **Spring Data JPA** (Hibernate) for ordinary CRUD; **`JdbcClient`** with plain SQL for the conditional stock update, reporting views and anything performance-sensitive | JPA entities stay inside each module's `infrastructure` package |
| Migrations | **Flyway**, one folder per module (`db/migration/<module>`), each creating its own schema | applied in one ordered run at startup or in CI |
| Database | **PostgreSQL**, current supported major version | managed instance in production, container locally |
| Security | **Spring Security**: session management, CSRF, `@PreAuthorize` for role checks, password encoder for Argon2id | session storage per [ADR-003](ADR-003-authentication-sessions.md) |
| Validation | Jakarta Bean Validation on request DTOs | |
| API docs | **springdoc-openapi** generates `/v3/api-docs` | used to generate the frontend client |
| Errors | Spring's built-in `ProblemDetail` (RFC 9457) | one `@ControllerAdvice` in `shared` |
| Build | **Maven** (or Gradle if the team prefers) | |

### 2.2 Testing

| Level | Tooling |
|---|---|
| Unit (domain rules) | JUnit 5, AssertJ; no Spring context |
| Module boundaries | Spring Modulith `verify()` test |
| Module integration | `@ApplicationModuleTest` boots one module with its dependencies mocked |
| End to end and concurrency | `@SpringBootTest` + **Testcontainers** PostgreSQL; concurrent-checkout test with a thread pool |
| API contract | generated OpenAPI checked into the repo; CI fails if it changes without the frontend client being regenerated |

### 2.3 Frontend

| Concern | Choice |
|---|---|
| Language | **TypeScript** |
| Framework and build | **React** with **Vite** |
| Routing | React Router, with routes grouped by role (client, farmer, admin) |
| Server state | TanStack Query (caching, refetch, loading/error states) |
| API client | generated from the backend's OpenAPI document |
| Forms | React Hook Form with schema validation |
| Translations | i18next (Italian and English) |
| UI components | one accessible component library (e.g. Mantine or MUI), chosen in the first sprint |

### 2.4 Delivery and operations

| Concern | Choice |
|---|---|
| Source control and CI | Git repository with **GitHub Actions**: build, unit tests, module verification, Testcontainers tests, frontend lint and tests, Docker image build |
| Packaging | one Docker image for the backend; frontend static files served by the Nginx image |
| Local development | **Docker Compose**: `nginx`, `app`, `postgres` |
| Production | the same Compose file on one Linux VM, or a container PaaS with managed PostgreSQL |
| TLS | Let's Encrypt via Nginx (or provided by the PaaS) |
| Logs and health | JSON logs to stdout; Spring Boot Actuator `/actuator/health` (only `health` exposed publicly) |
| Backups | daily database backup with point-in-time recovery where the host supports it; a restore tested before launch |

---

## 3. Options considered

| Criterion | **Spring Boot + Spring Modulith** | NestJS (TypeScript) | Django + Django REST Framework |
|---|---|---|---|
| Modular-monolith support | **Built in**: modules, verification, module tests, event registry, generated module diagrams | Nest modules exist, but they do not prevent importing another module's internals; needs dependency-cruiser or ESLint rules | Django "apps" are loose; needs import-linter; no module test support |
| After-commit events with outbox | **Built in** (event publication registry) | hand-written | hand-written (`transaction.on_commit` without outbox) |
| Transactions across modules | declarative `@Transactional` | depends on ORM; Prisma's interactive transactions or TypeORM's query runner must be passed between modules by hand | `transaction.atomic`, simple |
| Direct SQL when needed | `JdbcClient`, easy | raw queries possible | raw SQL possible |
| Security framework | Spring Security: very complete; steep learning curve | Passport plus hand-written session store and guards | Django auth: complete and simple; DB sessions built in |
| Admin stories (US 25–39) | written by hand | written by hand | **Django admin** could cover much of it for free |
| One language front and back | no (Java + TypeScript) | **yes** | no (Python + TypeScript) |
| Team familiarity (A1) | assumed high | assumed medium | assumed low–medium |
| Memory per instance | higher (JVM, typically a few hundred MB) | low | low |

**Why Spring Boot + Spring Modulith wins:** ADR-001's main risk is boundary erosion, and its main non-trivial mechanics are cross-module transactions and reliable events. Spring Modulith addresses exactly these with ready-made, tested features, where the other two stacks need hand-written conventions and extra linting tools. Under assumption A1 it is also the stack the team knows best.

**Why not Django, despite Django admin:** Django admin would deliver many admin stories almost for free, which is tempting. But it reads and writes models directly, bypassing module interfaces and the rules in them (e.g. "deleting a product archives it", ban cascades). That would quietly break ADR-001 §2.2 ("every admin write goes through the owning module"). The project would gain speed and lose the architecture.

**Why not NestJS:** a good second choice, especially for a team strong in TypeScript (one language everywhere, shared types). It loses here because boundary enforcement, cross-module transactions and an event outbox must all be assembled by hand.

**Other options not shortlisted:** ASP.NET Core (equivalent strengths to Spring, but assumed less familiar); Go (good runtime, but little framework support for this style and more hand-written CRUD); server-rendered templates with HTMX instead of a SPA (simpler frontend, but ADR-001 §2.9 keeps the API clean for a later mobile app).

---

## 4. Consequences

### 4.1 Positive

* **ADR-001's rules become tests.** Module boundaries and cycles are checked on every build with no extra tooling.
* **Reliable side effects.** After-commit events are stored and retried, so a crash between commit and listener does not lose an `OrderPlaced` reaction.
* **Mature security.** Sessions, CSRF protection, password hashing and method-level checks come from a well-reviewed framework instead of custom code.
* **Generated documentation.** Spring Modulith can generate module diagrams from the code, so the architecture diagram stays true.
* **Contract safety between backend and frontend.** The TypeScript client is generated from OpenAPI; a breaking API change becomes a frontend compile error.
* **Large ecosystem and learning material**, which matters for a student team.

### 4.2 Negative, and how they are handled

| Cost | Mitigation |
|---|---|
| **Two languages** (Java backend, TypeScript frontend) | generated API client; clear frontend/backend split of work |
| **Spring's learning curve**, especially Spring Security and JPA pitfalls (lazy loading, N+1 queries) | use `JdbcClient` for queries where JPA is awkward; enable SQL logging in development; keep security configuration in one class with tests |
| **Higher memory use and slower start-up** than Node or Python | irrelevant at one or two instances; set JVM memory limits in the container |
| **"Magic" annotations** can hide behaviour | keep annotations to the standard set; integration tests prove transactions and security actually apply |
| **Dependency on Spring Modulith** for module verification | the module rules are plain package conventions; if Spring Modulith were dropped, ArchUnit can check the same rules |

---

## 5. Compliance

* The build contains a test calling `ApplicationModules.verify()`; it must never be skipped or disabled.
* Pull requests that add a dependency not listed in this ADR (e.g. a second ORM, a message broker) need a short justification in the PR, or a new ADR if it changes the architecture.

---

## 6. When to revisit

* **Assumption A1 is false** (the team is clearly stronger in TypeScript): switch to **NestJS + Prisma or Drizzle + dependency-cruiser**, keeping ADR-001 unchanged. Write an ADR-002a recording the switch. Do this before the first feature, not after.
* Spring Modulith stops being maintained: replace module verification with ArchUnit and events with a hand-written outbox.
* Hosting forces a very low memory limit (for example, under 512 MB for the whole stack).
