# Part 07 — D12 Checklists, second half and release checklists

Status: planning specification.

## C-13–C-24

C-13 tasks: tool schema and registry; deterministic tool tests; max steps/timeouts/token budget; three role profiles; memory/trace; tool-output injection case. C-14 tasks: MCP architecture; server/client contract; read scopes; mutation approval; exact-argument binding; replay/changed-argument denial; Inspector evidence. C-15 tasks: React shell; typed fetch; SSE state; citation card; tool card; approve/deny; keyboard/error/loading states. C-16–C-19 tasks are conditional and start only after scratch gates and an explicit swap. C-20 tasks: redacted structured trace, TTFT/p50/p95 fields, cost/token fields, alert/runbook. C-21 tasks: local release, optional AWS eligibility, least privilege, teardown; kind is conditional. C-22 tasks: README, diagram, demo, resume/LinkedIn claims. C-23 tasks: restore, expired token, malformed import, killed worker, injection suite and clean clone. C-24 is backlog only.

📚 Learn first: [MCP architecture](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture), read participants/protocol layers; stop before lifecycle examples (~15 min).
↩ Return to build: create the next C-13–C-23 task with one acceptance case; done when a scope/evidence link exists; time box: 30 min; if stuck: read-only tool first.

## Rung release checklist

- [ ] All required component gates pass.
- [ ] Security and negative cases pass.
- [ ] AI golden set, baseline, metric, latency and cost report is versioned.
- [ ] Fresh clone and runbook pass.
- [ ] Seeded screenshots/demo recorded.
- [ ] README says built/studied/deferred accurately.
- [ ] PRs merged, Jira updated, tag/release notes written.
- [ ] Next three actions and known bugs stored.

📚 Learn first: [Semantic Versioning](https://semver.org/spec/v2.0.0.html), read rules 1–8; stop before FAQ (~7 min).
↩ Return to build: run this list before each tag; done when every checkbox links evidence; time box: 45 min; if stuck: stop at last complete rung.

## Daily-use checklist

Autosave safe; export/restore tested; keyboard path works; dark mode does not hide controls; seeded data only; private data remains local; agent mutations require approval; error state is recoverable.

Resource index checked 2026-10-01: MCP architecture, Semantic Versioning, OWASP prompt injection, README guidance — verified.
NEXT: Part 8.

