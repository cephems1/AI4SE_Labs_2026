# ADR-003: Authentication with server-side, revocable sessions

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-10-27 |
| **Deciders** | Michal Jaros (student), with Claude as architecture consultant |
| **Depends on** | [ADR-001](ADR-001-modular-monolith.md) §2.7, [ADR-002](ADR-002-technology-stack.md) (Spring Security) |
| **Stories** | 1–5, 17–25 |

---

## 1. Context

Eleven of the 41 stories are about authentication, for all three roles:

| Need | Stories |
|---|---|
| Register (client, farm) | 1, 17 |
| Log in | 2, 18, 22 |
| **Stay logged in across reloads** ("not put my credentials every time") | 3, 19, 23 |
| **Log out** so nobody else can use the account | 4, 20, 24 |
| See own profile | 5, 21 |
| **Admin deletes a malevolent user** | 25 |

Two of these pull in opposite directions:

* **Stay logged in** wants long-lived credentials in the browser.
* **Logout** and **admin ban** want those credentials to stop working **immediately**, on the very next request.

Other forces:

* The client is a browser SPA served from the **same domain** as the API (`/api` behind Nginx, ADR-001 §2.1). There is no third-party client yet.
* The backend is stateless and may run as several replicas, so session state cannot live in process memory.
* Personal data (names, e-mails, phone numbers) is under **GDPR**.
* There is **no story for registering an admin**.

---

## 2. Decision

### 2.1 Sessions

* On successful login, the server generates a **random opaque token** (256 bits from a cryptographically secure generator).
* The **SHA-256 hash** of the token is stored in `identity.user_session` with `user_id`, `created_at`, `last_seen_at`, `expires_at`, `revoked_at`, `remember_me`, and the user agent for the "active sessions" view. The token itself is **never stored**, so a database leak does not leak usable sessions.
* The token is sent to the browser as a cookie:
  `NFFH_SESSION=<token>; HttpOnly; Secure; SameSite=Lax; Path=/api`
  * `HttpOnly`: JavaScript cannot read it, so an XSS bug cannot steal it.
  * `Secure`: only sent over HTTPS.
  * `SameSite=Lax`: not sent on cross-site POSTs, which blocks most CSRF.
* On every request, an authentication filter hashes the cookie value and looks it up. The request is authenticated only if the session exists, is not revoked, is not expired, and the user's status is `ACTIVE`.

### 2.2 Lifetimes ("remember me")

| Login option | Cookie | Idle timeout | Absolute maximum |
|---|---|---|---|
| `rememberMe = true` (US 3, 19, 23) | persistent, `Max-Age` 30 days | 30 days, **sliding**: each use extends it | 90 days, then log in again |
| `rememberMe = false` | browser-session cookie (deleted when the browser closes) | 2 hours | 12 hours |
| **Admin**, either option | as above | **8 hours** | 7 days |

To avoid a database write on every request, `last_seen_at` and the sliding expiry are updated **at most once per 5 minutes** per session.

The token is **rotated** (new token, old one revoked) on login and on any privilege change, to prevent session fixation.

### 2.3 Logout, ban and revocation

| Event | Effect |
|---|---|
| Logout (US 4, 20, 24) | sets `revoked_at` on the current session; the cookie is cleared |
| "Log out everywhere" (own profile) | revokes all of the user's sessions |
| Password change | revokes all sessions except the current one |
| Admin bans or deletes a user (US 25) | sets the user's status to `BANNED`, revokes **all** their sessions, and publishes `UserBanned` in the same transaction (ADR-001 §2.4 business reaction) |

Because every request checks the database, revocation takes effect **on the next request**. Expired and revoked sessions older than 30 days are deleted by a nightly job.

### 2.4 Passwords and login protection

* Passwords are hashed with **Argon2id** (Spring Security's `Argon2PasswordEncoder`, parameters per current OWASP guidance). Stored hashes carry their parameters, so they can be strengthened later and re-hashed on next login.
* Minimum length 10 characters; checked against a list of common passwords. No forced composition rules.
* Login returns the same generic message ("invalid e-mail or password") whether the e-mail exists or not.
* **Rate limiting** on `/api/auth/login` and `/api/auth/register`: per IP and per account (e.g. 5 failures per account per 15 minutes, then a growing delay). No permanent lockout, which an attacker could abuse.
* E-mail addresses are stored lowercased and unique.

### 2.5 CSRF

`SameSite=Lax` blocks most cross-site requests, but not all (older browsers, same-site subdomains). So in addition, every state-changing request (`POST`, `PUT`, `PATCH`, `DELETE`) must carry a **CSRF token**: Spring Security's cookie-to-header pattern, where the SPA reads a non-HttpOnly `XSRF-TOKEN` cookie and sends it back as the `X-XSRF-TOKEN` header.

### 2.6 Registration

* `POST /api/auth/register` with `role = CLIENT` or `role = FARMER`. **`ADMIN` is never accepted** from the request.
* A client chooses a home **area** at registration (needed for US 6, 7).
* A farmer's registration creates the account (Identity) and the farm profile (Directory) in one transaction (ADR-001 §2.2).
* E-mail verification is **not** in v1 (no story asks for it), but `email_verified_at` is in the schema so it can be added without migration pain.

### 2.7 Admin accounts

* There is no admin registration. Admins are created by a **seed migration** with an e-mail from configuration and a random one-time password printed once to the deployment log, which must be changed on first login.
* Admin sessions are shorter (§2.2), and admin logins and admin write actions are written to an audit log.

### 2.8 Personal data and account deletion (open question Q6)

* "Delete user" (US 25) means **ban**, not hard delete: past orders must keep their integrity for farmers and statistics.
* On a GDPR erasure request, the user is **anonymized**: name, e-mail, phone and password hash are replaced or removed, status becomes `DELETED`, and all sessions are revoked. Orders keep only the anonymous user id.
* Until Q6 is answered, anonymization is built as an admin action, not automatic.

### 2.9 Where it lives

All of this is in the **Identity & Access** module. Other modules see only `CurrentUser` (id, role, farm id for farmers) from the shared kernel. They never touch sessions or passwords.

---

## 3. Options considered

| Option | Stay logged in | Immediate logout and ban | Complexity | Verdict |
|---|---|---|---|---|
| **A. Server-side sessions in PostgreSQL (chosen)** | yes (persistent cookie) | **yes**, next request | low | **Chosen** |
| B. Stateless JWT only (access token valid for days) | yes | **no**: a stolen or logged-out token works until it expires | low | Rejected: breaks US 4, 20, 24, 25 |
| C. Short JWT (15 min) + rotating refresh token stored in DB | yes | within up to 15 minutes, or immediately with a deny-list (which is a session table again) | medium–high: two tokens, refresh flow, rotation and reuse detection | Rejected for now |
| D. External identity provider (Keycloak, Auth0, Cognito) | yes | yes | medium: another system to run or pay for, redirects, configuration | Rejected for now |
| E. Spring Session JDBC (framework-managed session table) | yes | yes | low | Close alternative; see note |

**Why not JWT (B, C)?** JWTs pay off when many independent services must verify a user without calling a central store. NFFH is one application with one database (ADR-001), so a session lookup costs one indexed query. Making JWTs revocable means adding a database lookup anyway, which removes their advantage while keeping their complexity.

**Why not an external identity provider (D)?** It adds a system to run or a vendor to pay, for features NFFH does not need (single sign-on, social login, multi-factor). It can be introduced later behind the Identity module's interface if those needs appear.

**Note on E:** Spring Session JDBC would give working, revocable sessions with almost no code, and is an acceptable fallback if time is short. It was not chosen as the default because it stores the session id unhashed and its schema is less suited to the "active sessions" and "log out everywhere" views. The difference is small; the team may pick E and record that in this ADR.

---

## 4. Consequences

### 4.1 Positive

* **Logout and ban are immediate and certain.** There is no window in which a revoked session still works.
* **Stolen-cookie risk is reduced:** `HttpOnly` blocks theft by script, `Secure` blocks theft on the network, and hashing blocks use of a leaked database.
* **Simple mental model and code:** one cookie, one table, one filter. No token refresh logic in the SPA.
* **Works with several replicas** because sessions are in the shared database.
* **Supports useful extras cheaply:** "active sessions", "log out everywhere", admin audit.

### 4.2 Negative, and how they are handled

| Cost | Mitigation |
|---|---|
| A database lookup on every authenticated request | indexed lookup by primary key (the hash); throttled `last_seen_at` writes; can add a 30-second in-memory cache per instance if ever needed (revocation would then take up to 30 s) |
| Cookies need CSRF protection | `SameSite=Lax` plus CSRF token (§2.5), handled by Spring Security |
| Cookie auth fits a same-domain browser app; a future **native mobile app** cannot use cookies as comfortably | add a bearer-token variant of the **same** session token (`Authorization: Bearer …`) for mobile clients; the session table stays the same |
| Some custom code if option E is not used | keep it small and fully covered by tests (§5) |
| No e-mail verification in v1 | column prepared; add when spam registrations appear |

---

## 5. Compliance

Integration tests (Testcontainers, real database) must cover:

* After logout, the old cookie gets `401`.
* After an admin bans a user, all that user's sessions get `401` on the next request.
* A `rememberMe` session survives a simulated browser restart; a non-`rememberMe` session expires after the idle timeout.
* A state-changing request without a valid CSRF token gets `403`.
* `POST /api/auth/register` with `role = ADMIN` is rejected.
* The `user_session` table never contains a raw token (checked by comparing with the cookie value).

---

## 6. When to revisit

* A native mobile app or a third-party API client is planned: add the bearer variant (§4.2).
* Single sign-on, social login or multi-factor authentication is required: consider an external identity provider (option D).
* Parts of the system are extracted into services that must verify users independently: consider option C.
