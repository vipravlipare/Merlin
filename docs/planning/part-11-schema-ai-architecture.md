# Part 11 — D2 Schema, queries, AI architecture and observability

Schema is plain tables only: users/roles; notes/folders/tags/backlinks; tasks; sources/chunks; embeddings with model/version/dimension; evaluations; tool definitions; approvals; agent runs/steps; audit events. Every table has owner/tenant strategy, constraints, retention and index rationale. No SQL/DDL is supplied.

AI flow: parse→clean→dedupe→chunk→embed→index→owner-filtered retrieve→token-budget prompt→cite/refuse. Agent state records step, tool, arguments hash, approval, result class, tokens, latency and termination reason. MCP catalog marks read/mutate, scope, confirmation and transport.

Five planned queries: owner-scoped note search; due-task heap view; citation retrieval with source metadata; failed-ingestion retry; audit trail by run. Each later receives EXPLAIN expectation.

📚 Learn first: [PostgreSQL row security](https://www.postgresql.org/docs/17/ddl-rowsecurity.html), read default-deny behavior; stop before examples (~10 min).
↩ Return to build: write the schema tables and query contracts by hand; done when owner, version, retention and index rationale are explicit; time box: 45 min; if stuck: use one note/source/task path.

Resource index checked 2026-10-01: PostgreSQL tutorial/row security, pgvector, MCP architecture, Ollama API — verified.
NEXT: Part 12.

