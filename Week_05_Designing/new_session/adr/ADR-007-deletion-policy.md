# ADR-007: Never physically delete referenced data; use soft delete, and anonymise deleted users

| | |
|---|---|
| **Status** | Proposed (waiting on Q11, Q12) |
| **Date** | 2026-10-27 |
| **Deciders** | michaljaros, with Claude as architecture consultant |
| **System** | Not Far(m) From Home (NFFH) |
| **Requirements** | [../../Tasks/data/NFFH.txt](../../Tasks/data/NFFH.txt): stories 15, 25, 38, 39, 40, 41 |
| **Analysis** | [../NFFH_architecture_notes.md](../NFFH_architecture_notes.md) §1.3 (C4, C7), QAS9, §5.5 |
| **Supersedes** | — |
| **Related** | [ADR-001](ADR-001-modular-monolith.md) §2.5 (no cross-schema FKs) · [ADR-003](ADR-003-authentication-sessions.md) (revocation) · [ADR-004](ADR-004-checkout-one-order-per-farm.md) (cancellation) · [ADR-006](ADR-006-areas.md) (areas) |

---

## 1. Context

### 1.1 What the system does

Orders reference clients, farms and products. Farms reference areas.

### 1.2 What the requirements contain

| Delete action | Story | Referenced by |
|---|---|---|
| Farm removes a product | 15 | carts, past orders |
| Admin deletes a malevolent user | 25 | sessions, carts, orders, (farm) products |
| Admin deletes a product | 38 | carts, past orders |
| Admin deletes an area | 39 | farms, clients' home area |
| History must stay readable | 40, 41 | — |

### 1.3 What the requirements do not contain

What "delete" means for history and personal data (Q11). GDPR is assumed to apply: the right to erasure, but also keeping records the farm may need.

### 1.4 Decision drivers

| # | Driver | Weight | Why |
|---|---|:-:|---|
| X1 | History stays readable | 5 | 40, 41, QAS9 |
| X2 | IDs never dangle across modules | 4 | ADR-001 has no cross-schema FKs |
| X3 | Deleted users are really out, and their personal data is gone | 4 | 25, GDPR |

## 2. Decision

### 2.1 Products (15, 38)

`status = ARCHIVED`. They disappear from the catalog and from hot products and are removed from all carts (catalog publishes `ProductArchived` and ordering's handler deletes the cart items in the same transaction). Order lines keep their snapshots.

### 2.2 Users (25), default answer to Q11

One transaction in identity:
1. `status = DELETED`.
2. Email replaced by `deleted-<id>@invalid`. Name, phone and password hash cleared.
3. All sessions deleted (ADR-003).
4. Publish `UserDeleted(id, role)`.

Same-transaction handlers:
* **Client:** ordering cancels the client's future `RESERVED` orders (stock released, ADR-004 §2.6) and empties the cart.
* **Farm:** farms sets the farm `DEACTIVATED` and publishes `FarmDeactivated`. Catalog archives its products. Ordering cancels its future `RESERVED` orders. The farm's address is cleared, but the name snapshot on old orders stays, because it is business data the client needs for their history.

Past orders are kept. Their `client_id` points to the anonymised account, and they show as "deleted user".

### 2.3 Areas (39)

Refused while active farms reference them, then archived (ADR-006 §2.4).

### 2.4 Physical deletion

Only for data nobody references: expired sessions, cart items. Admin hard purge of anonymised accounts after a retention period (default 10 years for order records, to be confirmed by the PO and legal) is a later story.

### 2.5 Audit

Every admin delete or modify is written to `audit.admin_action(admin_id, action, target_id, at)`.

### 2.6 What this ADR does not decide

The legal retention period. A self-service "delete my account" (no story yet). It would reuse 2.2.

## 3. Options considered

| Option | Verdict | Why |
|---|---|---|
| **Soft delete + anonymisation** | **Chosen** | History intact, IDs stable, personal data removed |
| Hard delete with cascade | Rejected | Destroys order history (40, 41). Impossible without FKs across schemas |
| Hard delete, orders keep snapshots of everything | Rejected | Copies even more personal data into orders, which works against GDPR |
| Block only (no anonymisation) | Rejected | Personal data stays forever. Story 25 says "delete" |

## 4. Consequences

### 4.1 Positive

| Consequence | Practical meaning | Driver |
|---|---|---|
| Old orders always render | No broken history | X1 |
| No dangling IDs | Lack of cross-schema FKs is safe | X2 |
| Deleted users are locked out and anonymised | Story 25 and GDPR satisfied | X3 |

### 4.2 Negative, and how they are handled

| Consequence | Practical meaning | Mitigation | Residual risk |
|---|---|---|---|
| Every query must filter by status | A forgotten filter shows archived data | Default repository methods filter. Tests | Medium |
| Tables keep growing | More rows | Irrelevant at this scale | Low |
| Deletion cascade spans 4 modules | More code paths | All in one transaction. One integration test per role | Low |

### 4.3 Impact on the people involved

The admin gets predictable results and an audit trail. Developers must use status-aware queries.

### 4.4 Follow-up work

1. Status columns and default filters.
2. `UserDeleted`, `FarmDeactivated` and `ProductArchived` handlers.
3. Audit table.
4. Ask the PO and legal about retention (Q11).

## 5. Compliance

| Check | How | When |
|---|---|---|
| QAS9 | Archive a product with orders → order views unchanged | Every build |
| User deletion | Delete a client with a future order → order cancelled, stock back, sessions gone, PII empty | Every build |
| Farm deletion | Delete a farm → products archived, future orders cancelled | Every build |
| No physical delete of referenced rows | Review rule + test that the repositories expose no hard-delete for these tables | PR / build |

## 6. When to revisit

| Trigger | Response |
|---|---|
| Legal advice on retention | Add the purge job |
| A "delete my account" story | Reuse 2.2 |

## 7. Open questions

| # | Question | Current default |
|---|---|---|
| Q11 | Meaning of "delete user" for history | 2.2 |
| Q12 | Delete an area with farms | ADR-006 §2.4 |
