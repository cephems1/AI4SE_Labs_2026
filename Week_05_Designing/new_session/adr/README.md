# NFFH — Architecture Decision Records

Decisions for **Not Far(m) From Home**. Requirements: [../../Tasks/data/NFFH.txt](../../Tasks/data/NFFH.txt). Background analysis: [../NFFH_architecture_notes.md](../NFFH_architecture_notes.md). How these ADRs were written: [../NFFH_ADR_conversation_notes.md](../NFFH_ADR_conversation_notes.md).

| ADR | Title | Status | Waiting on |
|---|---|---|---|
| [ADR-001](ADR-001-modular-monolith.md) | Build NFFH as a modular monolith with one PostgreSQL database | Proposed | Team sign-off only |
| [ADR-002](ADR-002-technology-stack.md) | Java 21 + Spring Boot / Spring Modulith, PostgreSQL, React SPA | Proposed | Q14 (team skills) |
| [ADR-003](ADR-003-authentication-sessions.md) | Server-side, revocable sessions in an HttpOnly cookie | Proposed | Team sign-off; Q13 refines the admin part |
| [ADR-004](ADR-004-checkout-one-order-per-farm.md) | Checkout: one transaction, one order per farm, conditional stock decrement | Proposed | Q3, Q4, Q6 |
| [ADR-005](ADR-005-hot-products.md) | "Hot products" = in season, ranked by recent order lines | Proposed | Q1 |
| [ADR-006](ADR-006-areas.md) | Areas are admin-defined regions; "my area" = client's home area | Proposed | Q2, Q12 |
| [ADR-007](ADR-007-deletion-policy.md) | Soft delete for referenced data; anonymise deleted users | Proposed | Q11, Q12 |

Open questions Q1–Q16 are listed in the notes, §1.8.

## Conventions

* One decision per file, numbered `ADR-NNN-short-title.md`. Numbers are never reused.
* Sections: Context · Decision · Options considered · Consequences · Compliance · When to revisit · Open questions.
* Status: `Proposed` → `Accepted` → (`Superseded by ADR-NNN` | `Deprecated`). An accepted ADR is not rewritten; a changed decision gets a new ADR that supersedes it.
* All ADRs start as `Proposed`, because the user asked for a *proposal*. ADR-001 and ADR-003 depend on no open product question and can move to `Accepted` as soon as the team signs off.
* Defaults for unanswered product questions are written inside the ADRs and labelled "default answer to Qn".
