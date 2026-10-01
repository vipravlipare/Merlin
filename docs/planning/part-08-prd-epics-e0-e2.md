# Part 08 — D1 PRD, Epics E0–E2

Status: planning specification. Stories derive from D11/D12 and later receive Jira keys.

## Product requirements

Vision: local-first notes/tasks with measured retrieval and bounded actions. NFR targets: owner isolation zero failures; local non-LLM interaction diagnostic target under 100 ms; AI TTFT/total recorded; CI current revision green; no secret in logs; release claims evidence-backed.

### E0 Engineering Foundation and SDLC

Goal: reproducible learner-owned workflow. Stories cover environment/Compose, Jira/Git workflow, CI skeleton, review, SBOM and README.

### E1 Identity and Security

Goal: identify users, authorize every record/tool, redact hosted requests and test injection. Basic auth is MUST; refresh/TOTP are deferred.

### E2 Notes and Tasks Core

Goal: notes tree/tags/backlinks and heap-prioritized tasks with export/restore. Minimal React UI only.

Every story must include: persona/value, Gherkin happy/security/negative/performance cases, Fibonacci points, day/rung, C-## checklist, evidence, Learn first and Return. Backend stories add input→expected tables and hint ladders; frontend stories add props/state/events/manual integration.

📚 Learn first: [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/), read first steps; stop before advanced dependencies (~15 min).
↩ Return to build: create the first E0–E2 story from a D12 item; done when Gherkin, estimate, component and evidence are present; time box: 30 min; if stuck: one vertical slice.

Resource index checked 2026-10-01: FastAPI, OWASP Authorization, React, PostgreSQL, GitHub Actions — verified.
NEXT: Part 9.

