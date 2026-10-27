# ADR-003: Authenticate with server-side, revocable sessions in an HttpOnly cookie

| | |
|---|---|
| **Status** | Proposed (no blocking question; waiting on team sign-off. Q13 may refine the admin part) |
| **Date** | 2026-10-27 |
| **Deciders** | michaljaros, with Claude as architecture consultant |
| **System** | Not Far(m) From Home (NFFH) |
| **Requirements** | [../../Tasks/data/NFFH.txt](../../Tasks/data/NFFH.txt) |
| **Analysis** | [../NFFH_architecture_notes.md](../NFFH_architecture_notes.md) §1.3 (C1), QAS4–QAS6, §5.5 |
| **Supersedes** | — |
| **Related** | [ADR-001](ADR-001-modular-monolith.md) · [ADR-002](ADR-002-technology-stack.md) · [ADR-007](ADR-007-deletion-policy.md) |

---

## 1. Context

### 1.1 What the system does

Three roles (client, farm, admin) use one web app (ADR-001). The identity module owns accounts and sessions.

### 1.2 What the requirements contain

| Need | Stories |
|---|---|
| Register (client, farm) | 1, 17 |
| Login | 2, 18, 22 |
| **Stay logged in across reloads** | 3, 19, 23 |
| **Logout** | 4, 20, 24 |
| See own data | 5, 21 |
| **Admin deletes or modifies a user**, which must lock them out | 25, 29 |

### 1.3 What the requirements do not contain

Session length, password rules, MFA, account recovery, email verification. **Assumed:** 30-day "stay logged in". Passwords ≥ 10 characters checked against a breached-password list. Password reset by email is a later story. No MFA in v1 except optionally for admins (Q13).

### 1.4 Decision drivers

| # | Driver | Weight | Why |
|---|---|:-:|---|
| A1 | Revocation takes effect immediately | 5 | 4, 20, 24, 25 (QAS5) |
| A2 | Persistent login without re-entering credentials | 5 | 3, 19, 23 (QAS4) |
| A3 | Resistance to XSS token theft and CSRF | 4 | Personal data, GDPR |
| A4 | Simplicity in a single deployable | 4 | ADR-001 D2 |

## 2. Decision

### 2.1 Session mechanism

* On login, generate a 256-bit random token. Store **only its SHA-256 hash** in `identity.session(token_hash, account_id, created_at, last_seen_at, expires_at, user_agent)`.
* Send the token as cookie `nffh_session` with `HttpOnly; Secure; SameSite=Lax; Path=/`, max-age 30 days.
* **Sliding expiry:** each request at least 1 hour after the last update moves `expires_at` to now + 30 days. Absolute maximum 90 days, then the user logs in again.
* Admin sessions: 12 h sliding, 7 days absolute. Admins carry the most rights, and story 23 does not say how long.
* Rotate the token on login and on privilege change, to prevent session fixation.

### 2.2 Logout and revocation

* Logout (4, 20, 24) deletes the session row and clears the cookie.
* Admin delete or block (25, 29) deletes **all** of the user's session rows in the same transaction as the status change. The user's next request gets 401 (QAS5).
* "Log out everywhere" comes for free: delete by `account_id`.

### 2.3 Passwords and login protection

* Argon2id (or bcrypt cost ≥ 12 if the framework lacks Argon2).
* Rate limit: 5 failed attempts per account per 15 min, plus a per-IP limit. Generic error message.
* Admins are created by seeding or by another admin. There is no public admin registration.

### 2.4 CSRF and transport

* `SameSite=Lax` plus a synchronizer CSRF token (header `X-CSRF-Token`) on all state-changing requests.
* HTTPS only, HSTS. The SPA runs on the same origin (ADR-002), so no CORS is needed.

### 2.5 Request flow

The auth filter hashes the cookie value, loads the session together with the account in one indexed query, rejects it if expired or if the account status is not `ACTIVE`, then puts `(accountId, role)` in the request context. Modules receive an `Actor` object. They never read the cookie.

### 2.6 What this ADR does not decide

Password reset and email verification (later stories). Social login. MFA for non-admins.

## 3. Options considered

| Option | Verdict | Why not chosen |
|---|---|---|
| **Server-side session + HttpOnly cookie** | **Chosen** | — |
| Stateless JWT access token (15 min) + refresh token | Runner-up | Revocation (25) waits for the access token to expire, or needs a deny-list. That is a session table again, with more moving parts |
| JWT in `localStorage` | Rejected | Readable by any XSS. Fails A3 |
| Managed auth provider (Auth0, Cognito, BaaS auth) | Rejected for v1 | External dependency and cost for three simple roles. Revisit if SSO or social login is required |

## 4. Consequences

### 4.1 Positive

| Consequence | Practical meaning | Driver |
|---|---|---|
| Delete a row and the user is out | 4, 20, 24, 25 behave exactly as users expect | A1 |
| 30-day cookie | 3, 19, 23 satisfied | A2 |
| Token not readable by JS, CSRF token | Main web attacks covered | A3 |
| Framework-native (Spring Security / Django / express-session) | Little custom code | A4 |

### 4.2 Negative, and how they are handled

| Consequence | Practical meaning | Mitigation | Residual risk |
|---|---|---|---|
| A DB read on every request | Extra latency | Indexed lookup by hash (< 1 ms). Optional 30 s cache, which delays revocation by at most 30 s | Low |
| A native mobile app later needs a token flow | Cookie flow is web-only | Add a token endpoint then | Low |
| Session table grows | Expired rows | Nightly cleanup job | Low |

### 4.3 Impact on the people involved

Developers use the framework's session support. Security reviewers check one filter. Testers get a helper for "log in as role X".

### 4.4 Follow-up work

1. Session table migration and cleanup job.
2. Auth filter + `Actor` context.
3. Rate limiter.
4. Tests for QAS4 and QAS5.

## 5. Compliance

| Check | How | When |
|---|---|---|
| Cookie flags | Integration test asserts `HttpOnly`, `Secure`, `SameSite` | Every build |
| Revocation | Test: log in on 2 clients → admin deletes the user → both get 401 | Every build |
| Raw tokens never stored | Test inspects the `session` table | Every build |
| CSRF | Test: POST without the token → 403 | Every build |

## 6. When to revisit

| Trigger | Response |
|---|---|
| A native mobile app is planned | Add an OAuth-style token endpoint next to the cookie flow |
| SSO or social login is required | Consider a managed identity provider, keeping the internal `Actor` model |

## 7. Open questions

| # | Question | Current default |
|---|---|---|
| Q13 | What may the admin change on a user? MFA for admins? | Profile fields, block/unblock, force logout. TOTP MFA for admins recommended |
