# Part 21 — Sprint 4, Days 27–33

Goal: finish scratch core, hardening, optional framework slices only by swap. Order if funded: LangChain/LangGraph, n8n, LlamaIndex, fine-tuning, Mongo/Spring, kind, vector comparison. The default plan uses S4 for core completion and evidence. Day 33 review; no automatic framework claim.

## Conditional carry-forward: explicit note sharing

The existing schema and MER-11 repository are owner-only. An archived schema audit mentions sharing as future work, but no active day gave sharing acceptance rules or funded time. This section makes it a **conditional Sprint 4 (Days 27–33) candidate**, after Sprint 3's authenticated owner-only list/detail routes and real-role tests pass. It is not part of MER-11 or a current S4 commitment. The S4 plan is already full: before scheduling, reforecast and swap the estimated **390 minutes** below from optional framework/platform scope. Do not add hours, take time from security verification, or begin before the owner-only access gate passes.

Candidate behavior: an owner grants one named user read access to one note and can revoke it. The recipient reads only that note; the owner's unrelated private notes remain hidden. Unrelated users, missing identities, revoked grants and guessed nonexistent grants reveal neither note content nor existence. No write grants, public links, group-wide access or folder inheritance are included.

| Candidate checklist item | Cap | Evidence required |
|---|---:|---|
| Design the actor/resource/action matrix, threats and revocation behavior; review the minimum schema/policy change. | 60 min | Owner, recipient, unrelated user, missing identity, revoked grant, guessed IDs and ordinary-role outcomes are specified. |
| Add the smallest reversible share-grant schema and RLS change in disposable storage. | 90 min | Migration up/down safety, recipient-only access, owner control and default-deny behavior; protected storage unchanged. |
| Add authenticated grant/revoke/read endpoints with parameterized checks. | 90 min | Only the owner grants/revokes; recipient reads only the shared note; private notes stay private; errors reveal no content. |
| Add real PostgreSQL tests through a limited non-owner, non-superuser, non-`BYPASSRLS` role and reused connection. | 90 min | Owner/recipient/other-user cases, revocation, guessed-versus-missing behavior, pool reset and cleanup pass. |
| Inject per-case authorization faults and retain proof in CI. | 60 min | Each named assertion detects its paired fault; inventory, rollback, source-preservation and cleanup controls pass. |

The 390-minute figure is an initial planning estimate, not observed duration; re-estimate before scheduling. If no clean swap exists, carry sharing to a later sprint and keep owner-only access. The database setting `merlin.actor_id` is not authentication.

📚 Learn first: [PostgreSQL row security](https://www.postgresql.org/docs/17/ddl-rowsecurity.html), policy composition and role bypass; [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), deny-by-default and per-request checks.
↩ Return: start only after the owner-only routes pass exact-commit CI. Before scheduling, record the grant/revoke matrix, refined estimate, scope swap and fault-to-assertion evidence plan.

📚 Learn first: [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview), read capabilities; stop before code; why: framework follows scratch baseline (~10 min).
↩ Return to build: verify scratch gate and written swap before any install; done when comparison uses same data/golden cases; time box: conditional 30 min first slice; if stuck: defer.

Resource index checked 2026-10-01: framework pages verified; APIs/changelogs remain 🔎 verify at first use.
NEXT: Part 22.

