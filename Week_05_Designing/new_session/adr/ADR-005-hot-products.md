# ADR-005: Define "hot products" as in-season products ranked by recent order lines in the client's area

| | |
|---|---|
| **Status** | Proposed (waiting on Q1) |
| **Date** | 2026-10-27 |
| **Deciders** | michaljaros, with Claude as architecture consultant |
| **System** | Not Far(m) From Home (NFFH) |
| **Requirements** | [../../Tasks/data/NFFH.txt](../../Tasks/data/NFFH.txt): story 6 |
| **Analysis** | [../NFFH_architecture_notes.md](../NFFH_architecture_notes.md) §1.3 (C4), §5.5 |
| **Supersedes** | — |
| **Related** | [ADR-001](ADR-001-modular-monolith.md) (module and event rules) · [ADR-006](ADR-006-areas.md) (areas) |

---

## 1. Context

### 1.1 What the system does

Clients discover produce from farms near them. Story 6: *"As a Client, I want to See Hot products, so that I can discover the product in the season."*

### 1.2 What the requirements contain

Only story 6. Its "so that" clause ties "hot" to **season**.

### 1.3 What the requirements do not contain

What "hot" means, who decides it, whether it depends on area or popularity, and how many to show.

### 1.4 Decision drivers

| # | Driver | Weight | Why |
|---|---|:-:|---|
| H1 | Match the story's intent ("in the season") | 5 | Story 6 |
| H2 | Respect module boundaries | 4 | ADR-001 §2.4–2.5: catalog must not read ordering's tables |
| H3 | Easy to change once the PO answers Q1 | 4 | Undefined term |
| H4 | No extra work for farms beyond a season range | 3 | Farms update stock on phones |

## 2. Decision (default answer to Q1)

### 2.1 Definition

A product is **hot** if:
* it is `ACTIVE` and has `quantity_available > 0`;
* it belongs to an active farm in the area being browsed (the client's home area by default, ADR-006);
* the current month is inside its season range `[season_from_month, season_to_month]`, which may wrap over New Year (e.g. 11 → 2). Products without a season range are not hot.

### 2.2 Ranking

Ranked by the **number of order lines in the last 14 days**, then by name. The top 20 are shown. The ranking counts order lines, **not quantities**, because quantities have different units (kg, pieces, bunches) and must not be added.

### 2.3 Data and boundaries

* Catalog owns `catalog.product_popularity(product_id, day, order_line_count)`, PK `(product_id, day)`.
* It is updated **inside `catalog.reserveStock`**, in the same checkout transaction (ADR-004 §2.4 step 3). For each reserved line: `INSERT … ON CONFLICT (product_id, day) DO UPDATE SET order_line_count = product_popularity.order_line_count + 1`. Catalog already gets the lines through its own API, so it never reads ordering's tables and never depends on ordering.
* It is **not** fed by an `OrderPlaced` listener in catalog. That would make catalog depend on ordering's event type, and ordering already calls catalog: a cycle forbidden by ADR-001 §2.4. (This corrects the notes §5.2/§5.5, see notes §8.2.)
* Catalog gets the farm ids of the area from `farms.listActiveFarmIds(areaId)`. This is a downward call, so it is allowed.

### 2.4 Query (catalog schema only; self-checked)

```sql
SELECT p.id, p.name, p.unit, p.price_per_unit, p.farm_id,
       COALESCE(SUM(pp.order_line_count), 0) AS recent_lines
FROM catalog.product p
LEFT JOIN catalog.product_popularity pp
       ON pp.product_id = p.id
      AND pp.day >= CURRENT_DATE - 14       -- in ON: products with no recent orders stay in the list
WHERE p.status = 'ACTIVE'
  AND p.quantity_available > 0
  AND p.farm_id = ANY(:farm_ids)
  AND p.season_from_month IS NOT NULL
  AND (
        (p.season_from_month <= p.season_to_month
           AND :month BETWEEN p.season_from_month AND p.season_to_month)
     OR (p.season_from_month >  p.season_to_month
           AND (:month >= p.season_from_month OR :month <= p.season_to_month))
      )
GROUP BY p.id
ORDER BY recent_lines DESC, p.name
LIMIT 20;
```

### 2.5 Behind an interface

`HotProductPolicy` is the one class that implements 2.1–2.4. A different definition from the PO replaces that class and nothing else.

### 2.6 What this ADR does not decide

Personalisation and admin-curated "featured" products.

## 3. Options considered

| Option | Verdict | Why |
|---|---|---|
| **In season + ranked by recent order lines** | **Chosen** | Matches "in the season", still useful when many products are in season |
| Only "in season" flag set by the farm | Runner-up | Simplest. But with no ranking, the list is just alphabetical |
| Most ordered products (no season) | Rejected | Ignores the story's "in the season" |
| Admin picks hot products | Rejected | No admin story for it. Manual work every season |
| Rank by summed ordered quantity | Rejected | Adds kg to pieces. Meaningless |

## 4. Consequences

### 4.1 Positive

| Consequence | Practical meaning | Driver |
|---|---|---|
| Farms only set two months per product | Little extra work | H4 |
| No cross-module SQL | Boundaries hold | H2 |
| One replaceable class | Cheap to change after Q1 | H3 |

### 4.2 Negative, and how they are handled

| Consequence | Practical meaning | Mitigation | Residual risk |
|---|---|---|---|
| Counter update adds one upsert per line to the checkout transaction | Slightly longer checkout | The product rows are locked anyway. One extra indexed upsert per line | Low |
| Cancelled orders still count | Ranking slightly off | Acceptable for a ranking. `releaseStock` can decrement it if the PO cares | Low |
| Products without a season are never hot | Farms must opt in | Season fields shown in the product form | Low |
| New platform has no orders | Ranking is just by name at first | Fine. It improves with use | Low |

### 4.3 Impact on the people involved

Farms fill in a season range. Developers maintain one policy class and the counter update in `reserveStock`.

### 4.4 Follow-up work

1. Season fields in the product form.
2. Popularity table and the counter upsert in `reserveStock`.
3. Ask the PO (Q1).

## 5. Compliance

| Check | How | When |
|---|---|---|
| Season wrap works | Unit test: season 11 → 2 is hot in January, not in June | Every build |
| No cross-schema read, no catalog → ordering dependency | Architecture test (ADR-001 §5) | Every build |
| Units not summed | Code review of ranking changes | PR |

## 6. When to revisit

| Trigger | Response |
|---|---|
| PO defines "hot" differently | Replace `HotProductPolicy`. Mark this ADR superseded |
| Ranking query slow | Precompute a daily materialised list per area |

## 7. Open questions

| # | Question | Current default |
|---|---|---|
| Q1 | Meaning of "hot" | 2.1–2.2 |
| Q2 | Meaning of "my area" | ADR-006 |
