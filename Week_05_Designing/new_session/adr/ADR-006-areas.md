# ADR-006: Model areas as admin-defined named regions; "my area" is the client's chosen home area

| | |
|---|---|
| **Status** | Proposed (waiting on Q2, Q12) |
| **Date** | 2026-10-27 |
| **Deciders** | michaljaros, with Claude as architecture consultant |
| **System** | Not Far(m) From Home (NFFH) |
| **Requirements** | [../../Tasks/data/NFFH.txt](../../Tasks/data/NFFH.txt): stories 7, 30, 31, 35, 39 |
| **Analysis** | [../NFFH_architecture_notes.md](../NFFH_architecture_notes.md) §1.3 (C3), §5.5 (farms-by-area query) |
| **Supersedes** | — |
| **Related** | [ADR-001](ADR-001-modular-monolith.md) · [ADR-005](ADR-005-hot-products.md) · [ADR-007](ADR-007-deletion-policy.md) |

---

## 1. Context

### 1.1 What the system does

Clients look for farms "in my area" (7). The admin lists, adds and deletes areas (30, 35, 39) and lists farms by area (31).

### 1.2 What the requirements contain

The stories assume **areas are entities**: the admin creates and deletes them. A request process exists ("if there is some request for that area to be added", 35).

### 1.3 What the requirements do not contain

What an area is (a city, a province, a polygon?), how a client's area is known, whether a farm can be in several areas, and what happens when an area with farms is deleted (Q12).

### 1.4 Decision drivers

| # | Driver | Weight | Why |
|---|---|:-:|---|
| R1 | Fit the admin stories (areas as managed entities) | 5 | 30, 31, 35, 39 |
| R2 | Simple: no geocoding service | 4 | ADR-001 D2, D5 |
| R3 | Integrity on delete | 3 | 39 |

## 2. Decision

### 2.1 Areas

`farms.area(id, name UNIQUE, status ACTIVE|ARCHIVED)`. Areas are created by the admin (35) and owned by the farms module.

### 2.2 Farms

Each farm belongs to **exactly one** area (`farms.farm.area_id`, a FK inside the farms schema). The farm picks it at registration (17) from the active areas. If its area is missing, the farm asks the admin, which is the "request" in story 35.

### 2.3 Clients (default answer to Q2)

Each client picks a **home area** at registration (stored as `identity.account.home_area_id`, an ID reference without a cross-schema FK). "Farms in my area" (7) and hot products (6) default to the home area, and a selector lets the client browse other areas. No distance search.

### 2.4 Deleting an area (default answer to Q12)

`DELETE /api/admin/areas/{id}` is **refused (409)** while active farms reference the area, and the response lists them. After the admin moves those farms, the area is set to `ARCHIVED`. It is not physically deleted, because clients' `home_area_id` and old data point to it. Clients whose home area is archived are asked to pick a new one at their next login.

### 2.5 Farms by area (31)

The query in the notes §5.5 uses farms' own tables only and a `LEFT JOIN` with the status filter in the `ON` clause, so areas with zero farms are listed too.

### 2.6 What this ADR does not decide

Geographic search ("within 20 km"). It would need coordinates on clients and a distance query (possible later with PostGIS).

## 3. Options considered

| Option | Verdict | Why |
|---|---|---|
| **Admin-defined named areas + client home area** | **Chosen** | Matches 30, 35, 39 directly. No external service |
| Radius around the client's location | Rejected for v1 | The admin area stories would make no sense. Needs geolocation or geocoding |
| Areas from an external dataset (municipalities) | Rejected | Story 35 implies areas are added on request, not imported |
| Farm in several areas | Rejected | Complicates 31. Revisit if farms near borders complain |

## 4. Consequences

### 4.1 Positive

| Consequence | Practical meaning | Driver |
|---|---|---|
| Admin stories are plain CRUD in one module | Fast to build | R1, R2 |
| Refuse-then-archive | No farm loses its area silently | R3 |

### 4.2 Negative, and how they are handled

| Consequence | Practical meaning | Mitigation | Residual risk |
|---|---|---|---|
| A farm near a border shows up in one area only | Some clients miss it | Clients can browse neighbouring areas | Low |
| Admin must move farms before deleting an area | Extra step | The 409 response lists the farms | Low |

### 4.3 Impact on the people involved

The admin curates areas. Clients pick one area at sign-up.

### 4.4 Follow-up work

1. Area CRUD and the area picker in both registration forms.
2. The "pick a new home area" prompt.

## 5. Compliance

| Check | How | When |
|---|---|---|
| Delete refused with farms | Integration test | Every build |
| Empty areas listed in 31 | Test with an area without farms | Every build |

## 6. When to revisit

| Trigger | Response |
|---|---|
| PO wants distance search | Add coordinates for clients + PostGIS. Areas can stay for admin analysis |

## 7. Open questions

| # | Question | Current default |
|---|---|---|
| Q2 | Meaning of "my area" | 2.3 |
| Q12 | Deleting an area with farms | 2.4 |
