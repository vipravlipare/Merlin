# Day 7 — First local API: learn, design, build, test

Tracker: [MER-8](https://vipravlipare.atlassian.net/browse/MER-8). Expanded October 11, 2026; Day 7 is the learning sequence, not an assertion of actual work dates.

Goal: understand HTTP and implement one small, tested local health endpoint after reviewing CI carryover. You write application code; assistance provides specifications/review unless explicitly authorized. Day 6 is complete. Budget: 240 minutes; work top to bottom and tick only after evidence exists. Actual minutes are not known in advance.

### 1. Review the handoff and learn HTTP basics — 45 min

- [ ] 1.1 Read the Day 6 handoff and reuse its passing database/test evidence (10 min). Day 6 is complete; do not rebuild or rerun installed migrations.
- [ ] 1.2 Review .github/workflows/setup.yml and name what it actually tests (10 min). Record CI gaps and any verified run/commit; a remote green run is not proof of uncommitted local code.
- [ ] 1.3 Learn request method/path, response status/headers/body, JSON and loopback binding (15 min). Read Python HTTPServer/BaseHTTPRequestHandler before using FastAPI.
- [ ] 1.4 Explain why HTTP 200 does not prove database readiness or authentication, why unknown paths must not serve files, and why tests need an intentionally broken implementation (10 min).

📚 Learn first: [Python HTTP server](https://docs.python.org/3.12/library/http.server.html) — read HTTPServer and BaseHTTPRequestHandler; stop before CGI/file serving; [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) — read triggers, jobs and permissions.
↩ Return: Write three explanations in your own words and record the first real blocker. Read docs/planning/day-six-handoff.md for current evidence.

### 2. Design one small API and its tests — 40 min

- [ ] 2.1 Write a Markdown contract for GET /health: 200, application/json, and a small status=ok response; choose an unused loopback-only port (15 min). This is process liveness only, with no database query or credentials.
- [ ] 2.2 Write expected results for a valid request, unknown paths including /.env, unsupported POST/PUT, and a forced handler error (15 min). Require 404, 405 with Allow: GET, and a generic 500 respectively; never return files, tracebacks or private values.
- [ ] 2.3 Define the test fixture and shutdown/cleanup plan (10 min). Separate route logic from the server entry point so tests can inject faults safely; record implementation/test filenames by purpose.

📚 Learn first: [Python HTTP server](https://docs.python.org/3.12/library/http.server.html) — read request handler methods and response headers; [Python HTTP client](https://docs.python.org/3.12/library/http.client.html) — read HTTPConnection/request/getresponse.
↩ Return: Produce the endpoint contract and input/expected-result table before coding. Health checks must not certify ownership/security or expose environment values.

### 3. Build the first scratch API — 65 min

- [ ] 3.1 Resolve the CI scope decision first (15 min): review the existing setup workflow against current work and record gaps. If CI repair is the blocking priority, swap the API block for that repair and carry the API forward; never add invisible time or claim unexecuted CI coverage.
- [ ] 3.2 Personally write the minimal HTTP handler/server using the existing Python 3.12 standard library (35 min). Bind only to 127.0.0.1; implement the agreed route/status/error contract without serving files or adding database writes.
- [ ] 3.3 Start the server, make one real HTTP request, and verify shutdown/restart (15 min). Record commands, response and actual authored changes; dependency/startup delays reduce coding time inside this block.

📚 Learn first: [Python HTTP server](https://docs.python.org/3.12/library/http.server.html) — use the documented handler/server lifecycle; [Python JSON](https://docs.python.org/3.12/library/json.html) — read dumps/loads.
↩ Return: Show one real request/response and explain request routing through your own code. The standard-library server is a local learning prototype, not a production server. A FastAPI version and comparison ADR come after scratch acceptance in a separately budgeted slice.

### 4. Verify behavior and test effectiveness — 45 min

- [ ] 4.1 Write/run focused API cases for correct status, JSON shape/content type, unknown-path non-disclosure, unsupported methods and generic failure; check loopback binding and server cleanup (15 min). Check observations against the contract, not only that a request succeeds.
- [ ] 4.2 Inject isolated faults such as wrong healthy status/body, accepting POST, serving an unknown file path, and leaking a sentinel error value (15 min). Each corresponding test must fail for its intended reason. Do not install faulty code in the running app or weaken assertions.
- [ ] 4.3 Integrate the new cases and applicable faults into the complete suite, then run .venv/bin/python tools/run_test_suite.py (10 min). Preserve all Day 6 cases/faults; ensure new baseline cases demonstrate relevant fault detection rather than silently passing with no audit coverage.
- [ ] 4.4 Record actual PASS/FAIL/PENDING, first failure and measured runtime (5 min). If integration or required API tests are unfinished, leave them open. Authenticated API ownership denial remains PENDING until that boundary exists.

📚 Learn first: [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) — read teardown/cleanup; [pytest monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html) — read restoring isolated changes.
↩ Return: Keep failing evidence and repair responsible code. Use docs/testing/test-suite-commands.md; the previous approximately 53-second runtime is a measurement, not a speed guarantee after new tests.

### 5. Review and leave a clear handoff — 21 min

- [ ] 5.1 Review the diff and secret handling; confirm no environment file, credential, traceback or private error value is included in responses or publishable changes (10 min). Stop the learning server and preserve both existing database volumes.
- [ ] 5.2 Record authorship, observed results, actual minutes or unknown, first blocker and exact next action in a purpose-named handoff under docs/planning/ (11 min). Carry unfinished implementation/tests/CI forward; do not mark the Story Done just because planning or one smoke request succeeded.

📚 Learn first: [Reviewing changes](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository) — review status/diff before any separately authorized commit.
↩ Return: Leave a restart note the next session can follow without chat history. Preserve assistant/learner authorship and distinguish technical proof from learner confirmation.

## Budget and stop rule

240-minute cap: sections 1–5 = 45 + 40 + 65 + 45 + 21 = 216 minutes; reserve = 24 minutes; total = 240. Each checkbox is at most 35 minutes. Carryover and prerequisite failures replace new scope. No stretch hours or optional framework work are committed. If blocked, use reserve for the same scope, leave the unmet box open, and record the restart action.

## Scope and safety

Scope and limits: no login, note CRUD, database readiness claim, public hosting, UI, providers/AI, caching, deployment or new migrations. Never reset/delete Sprint 0 volume merlin_postgres_data or cluster 7691749973399031842. Do not rerun installed up migrations. Credentials remain private. This checklist expansion does not authorize commit/push/GitHub upload, a remote workflow dispatch or deployment. AWS and DSA remain deferred.

## Completion criteria

Definition of Done: explain the HTTP boundary; the agreed local endpoint and negative cases work; corresponding isolated faults are detected; all original tests/faults remain and the complete suite passes; CI scope/status is recorded honestly; server cleanup, secret review and handoff are complete. If the CI-only swap is used, keep API implementation/verification items pending and describe the partial outcome. Framework follow-up: FastAPI only after scratch acceptance, with pinned versions and a comparison ADR; not additional Day 7 work.

Official documentation links opened October 11, 2026. Context7 was unavailable. Existing runtime pins: Python 3.12.14, pytest 9.1.1; no new framework dependency is introduced by this planning change.

The local setup workflow currently runs setup/doctor checks, not the full Day 6 fault suite. Record that gap rather than claiming complete CI coverage. Any remote green run must be attributed to its actual commit.
