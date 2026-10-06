# Part 06 — D12 Checklists, first half

Status: planning specification. Every item is one Jira Task, one outcome, ≤90 minutes.

## C-01–C-06

| ID | Phase | Task | Done when |
|---|---|---|---|
| C-01.01 | L | Read GitHub PR workflow and explain branch→PR→merge. | Explain-back recorded. |
| C-01.02 | D | Specify issue-key branch/commit/PR convention. | Example accepted. |
| C-01.03 | T | Design secret and clean-clone checks. | Negative cases listed. |
| C-02.01 | L | Record Windows/WSL2, 16 GB, RTX 3050 hardware. | Driver/disk/pass-through status recorded. |
| C-02.02 | D | Specify core Compose services and loopback ports. | Health/volume/teardown fields complete. |
| C-02.03 | T | Design database/Redis health checks. | Expected pass/fail output written. |
| C-03.01 | L | Read GitHub Actions components. | Job/step explanation passes. |
| C-03.02 | D | Specify lint/type/test/build/scan workflow. | Required checks named. |
| C-03.03 | T | Design fixture-based AI regression gate. | Golden-set failure case exists. |
| C-04.01 | L | Read PostgreSQL transactions and row security. | Explain rollback/owner filtering. |
| C-04.02 | D | Specify users, notes, tasks, sources and audit tables in plain tables. | Keys/constraints/index rationale complete. |
| C-04.03 | I | Write first learner migration and health query. | Own code passes migration/rollback cases. |
| C-04.04 | T/S | Test guessed IDs and cross-user queries. | Zero unauthorized rows. |
| C-05.01 | L | Read OWASP password storage/authorization. | Explain hash vs encryption and deny-by-default. |
| C-05.02 | D | Specify password, short JWT, role and ownership behavior. | Expiry/tamper/role cases complete. |
| C-05.03 | I | Write login and owner checks. | Own tests pass. |
| C-05.04 | S/T | Test XSS, CORS, CSRF mode, rate limits and secret logging. | Findings recorded. |
| C-06.01 | L | Read FastAPI first steps and validation. | Boundary explanation passes. |
| C-06.02 | D | Specify health, error and typed route contracts. | Input/output/error table complete. |
| C-06.03 | I | Write health and one vertical route. | Local acceptance passes. |
| C-06.04 | T/O | Add timeout, redacted logging and health evidence. | Logs contain no secrets. |

📚 Learn first: [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), read deny-by-default and per-request validation; stop there (~10 min).
↩ Return to build: execute the next unchecked C-## item; done when its evidence link is recorded; time box: 90 min; if stuck: Part 3 hint ladder.

## C-07–C-12 summary

C-07 notes: folder tree, markdown safety, tags, backlinks, export, owner tests. C-08 tasks: heap ordering, deadlines, tie cases, empty input. C-09 gateway: local provider contract, streaming, structured output, retry/timeout, cost fields, hosted deny path. C-10 ingestion: markdown/CSV schemas, cleaning, dedupe, chunking, idempotency, dead-letter record. C-11 vectors: cosine from scratch, embedding version/dimension, exact pgvector, recall/latency. C-12 RAG/evals: citations, refusal, ≥20 cases, baseline, recall/MRR, latency/tokens/cost and regression gate. Each component repeats L→D→I→T→S→O→X→Z with one task per outcome.

📚 Learn first: [pgvector](https://github.com/pgvector/pgvector), read getting started/querying; stop before index tuning.
↩ Return to build: expand the next component’s summary into one checklist item before implementation; done when the test case and evidence are named; time box: 30 min; if stuck: keep exact search.

Resource index checked 2026-10-01: OWASP Authorization, PostgreSQL row security, FastAPI tutorial, GitHub Actions, pgvector, Ollama API — verified.
NEXT: Part 7.


## Day 6 expanded entry tasks — October 6

### C-04.01 — Explain transaction and ownership boundaries | 45 minutes | L

📚 Learn first: [PostgreSQL transactions](https://www.postgresql.org/docs/17/tutorial-transactions.html), all-or-nothing and commit/rollback; [row security](https://www.postgresql.org/docs/17/ddl-rowsecurity.html), default deny and privileged-role exceptions; stop before savepoints and policy examples. Pages retrieved October 6, 2026.
↩ Return: explain what survives a failed second write, where authenticated owner identity comes from, and why an administrative connection cannot prove RLS denial. Done when the learner supplies the explanations and draws client → backend identity → database. Stop at 45 minutes; record uncertainty instead of claiming mastery.

### C-04.02 — Specify the first users/notes slice | 60 minutes | D

📚 Learn first: [Part 11 starter contract](part-11-schema-ai-architecture.md#day-6-usersnotes-starter-contract), keys, ownership and test matrix; stop before future AI schemas.
↩ Return: adapt the plain-table contract and explain each constraint/index. Done when success, failure, rollback and two-user denial expectations are explicit; time box 60 minutes. Tasks, sources and audit remain future expansion of C-04.02, so the whole item is not Done today.

Hint ladder: 1—one note belongs to one user. 2—write the absent-owner and wrong-owner cases before indexes. 3—after a redacted attempt, request a focused design hint; no assistant-authored migration is supplied.

### C-04.03 — First learner-written migration/connectivity attempt | 60 minutes | I, conditional

📚 Learn first: [uv locking/syncing](https://docs.astral.sh/uv/concepts/projects/sync/), exact versus locked installation; [PostgreSQL transactions](https://www.postgresql.org/docs/17/tutorial-transactions.html), rollback; stop before advanced examples.
↩ Return: select and verify compatible first-use database driver, migration and test dependencies; record exact versions and locked imports before writing migration code. Use synthetic data in an isolated test database/project with distinct storage; never migrate/reset the preserved setup cluster as a learning experiment. Done only after personally written code passes Part 11 cases. Sixty minutes is an attempt cap, not a promise of completion; dependency setup consumes the same block. If prerequisites fail, stop implementation and record the first failing gate. Protected API authorization and C-04.04 require later identity work; no security completion claim today.
