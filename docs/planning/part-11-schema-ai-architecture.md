# Part 11 — D2 Schema, queries, AI architecture and observability

Schema is plain tables only: users/roles; notes/folders/tags/backlinks; tasks; sources/chunks; embeddings with model/version/dimension; evaluations; tool definitions; approvals; agent runs/steps; audit events. Every table has owner/tenant strategy, constraints, retention and index rationale. No SQL/DDL is supplied.

AI flow: parse→clean→dedupe→chunk→embed→index→owner-filtered retrieve→token-budget prompt→cite/refuse. Agent state records step, tool, arguments hash, approval, result class, tokens, latency and termination reason. MCP catalog marks read/mutate, scope, confirmation and transport.

Five planned queries: owner-scoped note search; due-task heap view; citation retrieval with source metadata; failed-ingestion retry; audit trail by run. Each later receives EXPLAIN expectation.

📚 Learn first: [PostgreSQL row security](https://www.postgresql.org/docs/17/ddl-rowsecurity.html), read default-deny behavior; stop before examples (~10 min).
↩ Return to build: write the schema tables and query contracts by hand; done when owner, version, retention and index rationale are explicit; time box: 45 min; if stuck: use one note/source/task path.

Resource index checked 2026-10-01: PostgreSQL tutorial/row security, pgvector, MCP architecture, Ollama API — verified.
NEXT: Part 12.


## Day 6 users/notes starter contract

This is an assistant-prepared design candidate, not a schema already installed or learner learning evidence. A primary key uniquely identifies a row; a foreign key requires a referenced row to exist. An index accelerates a matching access pattern and costs storage/write work. Start with two tables; future tasks, sources, audit and AI schemas require separate reviewed contracts.

📚 Learn first: [PostgreSQL tutorial](https://www.postgresql.org/docs/17/tutorial.html), tables and foreign keys; [row security](https://www.postgresql.org/docs/17/ddl-rowsecurity.html), default denial and bypass exceptions; stop before policy implementation.
↩ Return: C-04.02, rewrite the candidate in learner notes and approve the test expectations before C-04.03. Time box 60 minutes in Day 6; preserve the existing setup volume.

| Table / field | Proposed type / constraint | Purpose |
|---|---|---|
| users.id | UUID; primary key, required | Stable synthetic user identity. UUIDs are not authorization. |
| users.email | Text; required, normalized unique value | Define normalization before the uniqueness test; synthetic addresses only. |
| users.created_at | Time-zone-aware timestamp; required | Creation evidence; no password/login feature implied. |
| notes.id | UUID; primary key, required | Stable note identity. |
| notes.owner_id | UUID; required foreign key to users.id | Reject an absent owner. Deleting a referenced user is restricted for this slice; no silent cascade. |
| notes.title | Text; required, nonblank, at most 200 characters | Explicit validation and database constraint expectation. |
| notes.body | Text; required, empty allowed | Store beginner synthetic note content; no HTML rendering here. |
| notes.created_at / updated_at | Time-zone-aware timestamps; required | Define creation and update behavior in learner code. |

Index rationale: primary-key and unique-email lookup indexes follow their constraints. A notes index beginning with owner_id supports owner-scoped listing; add created_at/id ordering only if that exact list contract is selected. Do not add vector indexes or claim timing improvements without measurement.

Owner identity must be derived by the backend from authenticated context, never trusted from a client-supplied owner_id. Synthetic test actors can exercise the repository contract before login exists; they do not establish secure production authentication. Choose explicit repository owner filtering; if adding RLS defense, test through a non-owner, non-superuser, non-BYPASSRLS application role. Merely enabling RLS does not restrict every privileged role. [PostgreSQL documents those exceptions](https://www.postgresql.org/docs/17/ddl-rowsecurity.html).

| Acceptance case | Expected state / evidence |
|---|---|
| Isolated migration up | Only intended users/notes objects exist in the synthetic test database; setup cluster untouched. |
| Duplicate normalized email | Second insert rejected; first row unchanged. |
| Note with missing owner / blank or oversized title | Rejected; no invalid row retained. |
| Two writes, second fails | Entire transaction rolled back; no partial first write. |
| Commit and reconnect | Valid synthetic rows still present. |
| Actor A reads own note | Exactly the owned note returned. |
| Actor B guesses A's note ID / changes owner input | No unauthorized row returned or modified; count remains unchanged. Requires the implemented owner boundary, not a raw administrative query. |
| Migration rollback/reapply | In isolated synthetic storage only, downgrade removes the intended objects and reapply recreates them. This is not permission to drop real user data. |
| Errors and logs | No password, connection URL, private content or token exposed. |

Before writing code, record migration tool/driver/test versions, synchronous versus asynchronous connection choice, transaction scope and rollback risk. No runnable migration or DDL is delivered by this planning section. First-use dependency compatibility and practical owner tests remain unverified until learner execution.
