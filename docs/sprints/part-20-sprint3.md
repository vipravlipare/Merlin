# Part 20 — Sprint 3, Days 20–26

Goal: scratch tool registry, bounded agents, MCP, approvals, redaction/consent, agent UI, eval gate and local release. Three profiles share one runtime. Intervals/greedy and DP intro. AWS is conditional; local claim is separate. Day 26 is review; original MVP-2 name requires all gates.

## MER-11 carry-forward: authenticated owner-scoped note reads

MER-11 intentionally stopped at an internal list-only repository. The project already places basic login in MVP-0/Day 11 and defines C-05.01–C-05.04 for learning, design, login/owner checks and security tests; these are prerequisites, not evidence that authentication is implemented. The Day 10 work did not connect request-supplied IDs to identity. The fixed calendar is now in Sprint 3 (Days 20–26), so this is the current catch-up target. Reserve up to **270 minutes** from the existing 34-hour S3 floor and swap out an equal amount of lower-priority scope before starting. Do not add hours or cut required security tests. If identity or the least-privilege database role is not ready, keep the routes disabled and reforecast.

Planned behavior: `GET /api/notes` lists the verified actor’s active notes newest first, with title/body-preview and update time. `GET /api/notes/{note_id}` returns full content only for an active note the actor owns. A guessed foreign ID and a nonexistent ID have the same public not-found result. The actor comes only from verified server authentication; submitted `user_id`/`owner_id` cannot change scope. Use the limited application role, explicit parameterized owner filtering, transaction-local identity and the active-notes/trash boundary. No create, edit, delete, sharing or authentication bypass is included.

| Planned checklist item | Cap | Evidence required |
|---|---:|---|
| Verify the C-05 login/token and role prerequisites; write route and denial contracts before wiring either route. | 45 min | Valid, absent, expired and tampered identity; client owner-ID substitution; active/trash behavior; foreign-versus-missing response; no route when identity is unavailable. |
| Wire authenticated list and detail routes to the internal repository. | 90 min | Actor derived from validated auth context; list order/fields and full-note detail meet contract; every query is owner-scoped. |
| Add guarded PostgreSQL integration with two synthetic users and a limited non-owner, non-superuser, non-`BYPASSRLS` role. | 90 min | Owner sees own rows; other actor gets no private rows; foreign/missing IDs are indistinguishable; real pool reuse does not retain actor state; rollback, cleanup and source preservation pass. |
| Add per-case faults and cumulative CI gates for authorization, disclosure and cleanup. | 45 min | Intended denial assertions detect paired faults; private sentinels/details do not escape; Day 1–19 required gates remain. |

Each checklist item is capped at 90 minutes. A mock test does not satisfy the real PostgreSQL/pool gate. Never test normal row denial as a superuser, table owner or `BYPASSRLS` role. This plan does not claim a notes route or trusted login currently exists.

📚 Learn first: [FastAPI OAuth2/JWT and password hashing](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/); [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html); [PostgreSQL row security](https://www.postgresql.org/docs/17/ddl-rowsecurity.html). Verify installed versions and the chosen token/session design at implementation time.
↩ Return: first verify C-05 identity and least-privilege database prerequisites; then record exact tests and observed denial results. This is planned work, not a MER-11 completion claim.

📚 Learn first: [MCP architecture](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture), read participants and protocol layers; stop before lifecycle (~15 min).
↩ Return to build: implement one read tool and one denied mutation case; done when scope and approval evidence exist; time box: day net capacity; if stuck: max-step loop with recorded tool output.

Resource index checked 2026-10-01: MCP/Ollama/OWASP sources verified.
NEXT: Part 21.

