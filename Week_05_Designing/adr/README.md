# NFFH — Architecture Decision Records

Decisions for **Not Far(m) From Home**. Requirements: [../Tasks/data/NFFH.txt](../Tasks/data/NFFH.txt). Background analysis: [../NFFH_architecture_notes.md](../NFFH_architecture_notes.md).

| ADR | Title | Status | Waiting on |
|---|---|---|---|
| [ADR-001](ADR-001-modular-monolith.md) | Build NFFH as a modular monolith | Accepted | — |
| [ADR-002](ADR-002-technology-stack.md) | Technology stack: Spring Boot with Spring Modulith, PostgreSQL, React | Proposed | team's language experience |
| [ADR-003](ADR-003-authentication-sessions.md) | Authentication with server-side, revocable sessions | Accepted | — |
| [ADR-004](ADR-004-cart-and-order-per-farm.md) | Multi-farm cart, one order per farm at checkout | Proposed | product owner: Q1, Q2, Q4 |
| [ADR-005](ADR-005-hot-products.md) | "Hot products" = recently most-ordered in the client's area, with an in-season fallback | Proposed | product owner: Q3 |

## Conventions

* One decision per file, numbered `ADR-NNN-short-title.md`. Numbers are never reused.
* Sections: Context · Decision · Options considered · Consequences · Compliance · When to revisit.
* Status: `Proposed` → `Accepted` → (`Superseded by ADR-NNN` | `Deprecated`). An accepted ADR is not rewritten; a changed decision gets a new ADR that supersedes it.
