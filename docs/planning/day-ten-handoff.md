# Day 10 / MER-11 handoff

Recorded October 24, 2026. This handoff covers the list-only internal repository slice and cumulative CI evidence. It does not claim a login route, production authorization, or completion of manual learning tasks.

📚 Learn first: [Day 10 checklist](../sprints/day-ten-jira-checklist.md), especially sections 3–6; [full case/fault review](../testing/full-suite-case-fault-review.md); [cumulative CI map](../testing/ci-test-coverage.md).
↩ Return: answer the explain-back below in your own words, review the final combined diff, then run the local CI-entry command before the final commit/push.

## Work and authorship

- The learner selected the behavior: show the signed-in actor’s active notes newest first, display stored title or a bounded body preview, require a trusted actor, filter by owner, use a transaction-local actor setting, and keep shared/private ownership boundaries clear.
- The learner explicitly asked the assistant to implement and refactor the repository and tests. `app/notes_repository.py`, the weighted-preview helper changes, and focused repository tests are assistant-authored. Do not report them as learner-written.
- The learner supplied the security rationale: request-supplied identity is untrusted; the SQL owner filter is a second guard; `SET LOCAL` ends with its transaction. The learner also requested beginner-friendly code comments and honest assistant/learner attribution.
- The assistant authored the test inventory/witness repairs, full-suite runtime gate, hosted CI scope/result checks, artifacts and this evidence documentation. No later assistant code change is blanket-authorized beyond this scoped task.
- Actual learner and assistant minutes are unknown. Checklist budgets are estimates, not observed effort.

## Review and observed verification

The assistant reviewed changed and untracked application code, tests, fault definitions, CI inputs and evidence for private note content, credentials, unsafe owner disclosure and unrelated scope. Fixtures use synthetic UUIDs and note text. No real account credential or private note content was needed. `git diff --check` passed. This review is bounded; it does not prove that every possible secret or defect is absent.

The final nested guarded suite passed in 59.125 seconds under its 60-second gate with 20 Python-fault workers. The fresh CI-entry rehearsal passed in 91.826 seconds overall. It ran original-source Python tests, the complete suite and separate migration roundtrip with `--include-untracked`; cleanup passed. The suite reported 1,201 tests plus three subtests, 821 Python case IDs, 314 executable faults detected at their intended checks, 383 SQL cases, 607 SQL case/fault pairs, five lifecycle cases, 14 migration gates and 17 repair checks. The case/fault matrix is `docs/testing/full-suite-case-fault-matrix.json`. Temporary run summaries are under `/tmp` and can disappear.

The review corrected the `notes-missing-actor-accepted` witness to point at the explicit `None` actor check. The CI runner now enforces inventory floors, all six MER-11 case IDs, all eleven note-fault witnesses, the seven suite stages, the 60-second limit and isolated cleanup/source preservation. It checks all eight case/fault/migration reports and hashes them into `ci-summary.json`. The final local rehearsal passed. Hosted exact-revision CI remains pending the combined commit/push.

Historical first failures are preserved in [the Day 10 test review](../testing/day-ten-test-pass-review.md): stale mutation anchors left six faults unapplied, then outdated AST inventory IDs and a test-node spelling blocked later stages. In the fresh CI-entry rehearsal, copied identity adaptation initially left a stale witness hash; the copied hash is now refreshed and recorded. A later run narrowly exceeded 60 seconds, so the worker ceiling increased to 20 and an unchanged runtime image snapshot was removed. A control found Docker can omit `Config.Labels`; the adapter now handles that and has a regression control. The final fresh rehearsal then passed all three steps.

## Open boundaries

- No authentication/session route supplies a trusted actor. Do not connect this repository to request-provided `user_id`.
- Repository ownership tests use mocks. They do not prove real PostgreSQL RLS through `app.notes_repository` or real connection-pool reset.
- The selected behavior is list-only. Fetch-by-ID concealment and explicit sharing are not implemented.
- Basic login remains in the MVP-0/Day 11 and C-05 plan, but is not verified as built. The protected list/detail route is planned as a Sprint 3 catch-up slice in `docs/sprints/part-20-sprint3.md`; explicit sharing is an unfunded, conditional Sprint 4 candidate in `docs/sprints/part-21-sprint4.md`.
- MER-9 model readiness includes manual observations; CI does not claim model quality or production inference.
- MER-10 HTTP transport remains deferred. Decoder tests do not establish network redirects/proxy behavior, transport deadlines, cleanup or hosted fallback policy.
- The learner’s Step 6 explain-back and review of assistant-authored implementation remain personal tasks.
- The current Day 10 code and documentation are uncommitted. Hosted exact-revision CI must be observed after the combined commit is pushed. No commit or push has been made in this handoff.

## Learner explain-back still open

Your earlier answers already covered the key idea that identity must come from trusted authentication, the SQL owner filter adds a second check, and transaction-local settings end with their transaction. Finish the remaining parts from memory without reading the implementation first:

1. Why does testing as a PostgreSQL superuser or with `BYPASSRLS` fail to prove ordinary application-role denial? What role and two-actor condition would a valid denial test need?
2. How could a reused connection carry actor state if transaction boundaries were wrong? What do the mocked two-actor test and idle-connection guard prove, and what still needs a real PostgreSQL/pool test?
3. Name current checks for active-only ordering, trash exclusion, malformed identity and untitled previews. Which sharing, fetch-by-ID or authentication behaviors remain unimplemented?

I cannot answer for you. After you respond, I will identify what is correct, explain any gaps, and record any corrections as guided help rather than independent authorship.

## Exact next steps

1. Complete the learner explain-back above and review the assistant-authored code/tests.
2. Review the recorded final fresh CI-entry rehearsal over the implementation and tests. After updating the evidence paths/timings, the documentation linter and whitespace check were rerun and passed; hosted CI will test the exact combined revision after publication.
3. Make one combined code/document commit, then push it to trigger hosted CI. Confirm that workflow tested that exact revision and inspect the full evidence artifact.
4. Keep authentication, real repository/pool integration, sharing, fetch-by-ID and HTTP transport outside the current completion claim.

📚 Learn first: [transaction-local settings](https://www.postgresql.org/docs/17/sql-set.html), `SET LOCAL`; [GitHub push event](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#push), exact revision triggered by push.
↩ Return: resume at step 1; commit only after code, tests, CI evidence and handoff are final. Do not mark all manual or deferred work complete from green CI.
