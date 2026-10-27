---
name: architecture-requirements-analysis
description: Analyse a requirements document (system description, user stories) from an architect's point of view, producing actors, capability groups, missing non-functional requirements, explicit assumptions, weighted architectural drivers, quality-attribute scenarios and open questions for the product owner. Use as the first step before proposing or choosing an architecture, or when the user asks to "analyse requirements for architecture" or "derive architectural drivers / quality attributes".
---

# Requirements analysis for architecture

Output goes into the notes file as the "Requirements analysis" section. Produce the subsections below in this order.

## 1. The system in one sentence

Who does what with what. Then call out anything **out of scope** that removes complexity (e.g. "no online payment, no delivery").

## 2. Actors

Table: actor · names used for it in the stories · story numbers / count. Include external systems (maps, payment providers, email).

## 3. Stories grouped by capability

Table: capability · story numbers · **notes for the architect**. In the notes, point out:

* stories that imply hidden mechanics (e.g. "don't re-enter credentials on reload" → persistent session; "logout" + "admin deletes user" → revocable sessions);
* undefined terms ("hot products", "my area");
* the workflows with real **consistency risk** (concurrent updates, money, stock);
* authorization beyond roles (ownership: "only my own products");
* reporting / cross-entity queries, and how many stories they are;
* integrity problems (deleting something that others reference).

Check that every story appears in exactly one group; say so ("all N stories covered").

## 4. What the requirements do not say

Most student/startup requirement sets contain no NFRs. List the missing ones explicitly (scale, performance, availability, security/privacy, budget, team size, deadline, regulation such as GDPR, likely evolution) and give the **inferred value with the reasoning**, labelled as an assumption.

## 5. Architectural drivers

Table with columns: `# | Driver | Weight (1–5) | Why (traced to stories or assumptions)`.

* 8–12 drivers. Typical ones: consistency of the critical workflow, cross-entity queries, simplicity/time-to-market, operational cost, security (authN, sessions, RBAC, ownership), modifiability, scalability, availability, testability, portability/vendor independence, performance, interoperability.
* Weights must reflect *this* system, not textbook defaults. Explain any weight of 5 and any weight of 1–2 for a quality that is often assumed important (e.g. "scalability = 2: regional platform").
* These weights are reused unchanged in the scoring matrix.

## 6. Quality-attribute scenarios

For the top drivers, write concrete, testable scenarios (ATAM style: source → stimulus → environment → response → measure). Example: "Two clients check out the last 2 kg at the same moment → exactly one succeeds, the other gets a clear message, stock never goes negative." Mark assumed numeric targets as *(assumed)*.

## 7. Working assumptions

Short bullet list of domain assumptions that shape the design (e.g. "one farm = one user account", "a client has one home area").

## 8. Open questions for the product owner

Table: `# | Question | Affects (components) | Proposed default`. Every undefined term and every inferred NFR should produce a question. Number them Q1… so later ADRs can reference them.

## Rules

* Only read the files the user pointed to; respect any "ignore" instruction.
* Never invent a requirement. If something is inferred, say "inferred" or "assumed".
* Keep story numbers in every table so later stages can trace back.
