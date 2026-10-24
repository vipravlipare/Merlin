# Day 11 — Catch up and verify one working path

Jira: [MER-12](https://vipravlipare.atlassian.net/browse/MER-12). The fixed calendar assigned Day 11 to October 11, 2026. Work resumes October 24; this is catch-up, not a date reset or extra time. Maximum: **300 minutes**, including reading, implementation, testing, CI wait, review and handoff. Record actual minutes; unknown stays unknown.

## Current starting point

- MER-11 is Done. It contains an internal, assistant-authored active-note repository and focused tests, but no authentication boundary or public notes route. Learner code review and some explain-back remain learning follow-ups; do not report them as completed.
- Hosted cumulative CI passed on commit `255ec47b4fd300efde3d84701bb2ab1202559880`, [run 40107329920](https://github.com/vipravlipare/Merlin/actions/runs/40107329920). The required `setup`, `prepare`, database, and both Python fault-shard jobs passed. The 60-second check measures the longest required test-execution lane; runner setup and queue time are outside that cap. The full GitHub workflow took longer than 60 seconds.
- `/health` remains unchanged. Local provider HTTP transport remains deferred. No password login, token validation, authenticated actor dependency, or notes endpoint is claimed as built.
- Day 11 is not an automatic MVP-0 release. The original walking-skeleton definition also requires a Compose path, API, migrations, CI image build, provider streaming to Ollama, and README evidence. Release only the highest fully verified slice.

## Checklist — 300 minutes total

### 1. Reconcile carryover and choose one outcome — 30 minutes

- [ ] Inspect the current branch, worktree, latest commit and hosted CI result. Read the MER-11 outcome and handoff. Name existing code, missing authentication pieces, the single Day 11 outcome, and anything explicitly deferred.

📚 Learn first: [MER-11](https://vipravlipare.atlassian.net/browse/MER-11), read its current scope and limits; [Git status and diff](https://git-scm.com/docs/git-status), read the short status format.  
↩ Return: record the exact starting SHA and choose one small path. Done when code, tests, CI status and open learning follow-ups are distinguished. Stop at 30 minutes; do not add work to the day cap.

### 2. Specify the authentication boundary — 60 minutes

- [ ] In your own words, explain how a password becomes a one-way hash, how a signed short-lived token is validated, and how the server derives the actor from that validated token. Decide the minimum login and current-user behavior, token lifetime, error response, and required negative cases. Do not use a request-supplied `user_id` as identity.

📚 Learn first: [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), read Argon2id and password verification; [FastAPI OAuth2 with password hashing and JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), read password verification, token creation and current-user validation. Pages checked October 24, 2026.  
↩ Return: write a short request/response table for valid login, wrong password, unknown account, missing token, invalid signature and expired token. Name the selected algorithm and locked package versions only after checking the repository. Done when the actor source and every denial result are explicit. Stop at 60 minutes; if implementation needs unreviewed dependencies or schema changes, record them and keep protected routes disabled.

### 3. Personally implement one narrow authentication path — 90 minutes

- [ ] If prerequisites pass, write one login path and one current-user path using the agreed design and synthetic test accounts. Keep notes data and notes routes inaccessible. Derive identity only from a validated credential. If the required API, dependency lock or isolated database target is not ready, stop at the first failed gate and record a smaller verified path instead of bypassing it.

📚 Learn first: [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/), read the password and bearer-token sections relevant to the selected flow; [FastAPI dependency injection](https://fastapi.tiangolo.com/tutorial/dependencies/), read dependencies used by path operations. Pages checked October 24, 2026.  
↩ Return: personally write and explain each changed application line. Done when login can identify the synthetic test user and the current-user path returns that same server-validated identity, or the blocker is recorded with the route disabled. Do not claim registration, production readiness, or protected note access unless those behaviors are implemented and proved. Stop at 90 minutes.

### 4. Add focused positive and denial tests — 60 minutes

- [ ] Add tests for valid login; wrong password and unknown account; missing, malformed, modified and expired credentials; identity taken from the verified token rather than request input; safe errors without passwords, tokens or private values in responses/logs; and rate limiting if the selected endpoint can be retried without bounds. If cookies are selected, include the agreed CSRF and origin checks.

📚 Learn first: [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/), read `TestClient` and application tests; [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), review verification and storage rules. Pages checked October 24, 2026.  
↩ Return: map every expected result to a named test and assertion. Use synthetic accounts and tokens only. Done when success and rejection cases fail for the intended reason, and no test weakens an existing assertion. Stop at 60 minutes; unresolved cases stay open.

### 5. Run focused checks and cumulative CI — 45 minutes

- [ ] Run focused tests, then the documented cumulative test suite. Commit and push only reviewed, intended changes. Check the required hosted workflow on the exact tested SHA; record job results, retained test/fault inventory, runtime basis, cleanup and first failure. Never treat skipped checks, another commit, a local pass or a test failure caused only by setup as proof.

📚 Learn first: [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html), read test execution and assertion reporting; [GitHub Actions workflow runs](https://docs.github.com/en/actions/how-tos/monitor-workflows/use-workflow-run-logs), read job and step results. Pages checked October 24, 2026.  
↩ Return: use the project’s documented commands and disposable test target. Done when the exact pushed SHA has a green required check and the full inventory/result validators pass. Keep the current 60-second longest-test-lane limit; report full workflow elapsed time separately. Stop at 45 minutes; if CI needs longer, record actual time and continue only within the 300-minute cap.

### 6. Review, explain and hand off — 15 minutes

- [ ] Review the diff and output for secrets, private content, unplanned changes and unsafe identity handling. Explain the password-hash, token-validation and actor-derivation flow from memory. Record learner-authored versus assistant-reviewed work, actual minutes, test/CI evidence, open gaps and the next exact step.

📚 Learn first: [Git diff](https://git-scm.com/docs/git-diff), read how to review changed lines; revisit the selected FastAPI and OWASP sections above.  
↩ Return: write a concise handoff with commit SHA and hosted run URL. Done when another session can identify what works, what remains unbuilt and the first next action. Do not call the full MVP-0 complete unless every original acceptance condition has evidence.

## Stop rules and acceptance

- Do not expose notes routes until the application has a trustworthy identity source and the database path enforces the verified actor with the required owner boundary.
- Do not alter `/health`, weaken CI, bypass migration checks, use a protected database volume, or publish credentials/private data.
- Do not add invisible hours. Any unfinished work replaces later scope or remains open; it does not become an assumed pass.
- MER-12 is complete only for the small path actually implemented and verified. Login, authenticated note access, local provider transport, full MVP-0 and production security remain separate claims unless their own gates pass.
