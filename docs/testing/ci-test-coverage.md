# What runs automatically in CI

October 23 update: [application-only scope](application-test-scope.md) supersedes quiz-inclusive receipts. Current code and documents passed the fresh local CI-entry rehearsal; hosted exact-revision proof remains pending the combined commit/push.

The cumulative verification workflow runs on every ordinary push to any branch and on pull requests, with no path or branch filters. Manual execution remains available. New pushes no longer cancel earlier runs through a workflow concurrency group. Each hosted job uses its own runner and independently owned synthetic database storage. GitHub capacity, service limits, explicit skip instructions or manual cancellation can still prevent completion; verify the run outcome rather than assuming every event passed.

A local `git commit` does not contact GitHub. Run the local suite before publishing, then push the commit to trigger hosted CI. A push containing several commits tests the final branch revision, rather than creating a separate job for every intermediate commit. Push commits separately if each revision needs its own observed run. No automatic Git hooks or automatic pushes are installed.

📚 Learn first: [GitHub push events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#push), which revision is checked; [workflow concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency), cancellation and pending runs. Official sources checked October 15, 2026.
↩ Return: open Actions, select the pushed commit, and inspect every required step and its synthetic verification artifact.

## Unit tests and real-system tests serve different purposes

A unit test checks a small piece of actual code in isolation. Existing Python tests exercise validation, email normalization, Unicode/whitespace boundaries, maintenance decisions, probe failure handling and setup safety. Database connectors are replaced with controlled test doubles where appropriate; assertions still execute the real application functions.

Database checks remain integration or system tests. Replacing PostgreSQL with a mock cannot prove database constraints, transaction rollback, reconnect persistence, locks or migration reversal. Renaming those checks as unit tests would not add coverage and converting them to mocks would remove important proof. All applicable application assertions remain; personal quiz checks are explicitly removed under the revised scope.

## Required execution map

| Layer | Existing execution in CI | What it establishes |
|---|---|---|
| Locked setup and doctor unit regressions | Locked Python/Node environments, `tools/test_*.py`, setup and doctor static/runtime checks | Fresh-runner prerequisites, isolated services and fail-closed setup behavior. |
| Python unit and regression tests | Original source tests before adaptation, then the complete suite baseline; 821 Python case/subtest inventory IDs, including 467 decoder cases and six MER-11 repository cases | Actual application helpers, controlled connection failures, non-disclosure, maintenance guards and setup/documentation behavior. |
| PostgreSQL integration tests | 383 case IDs against real disposable PostgreSQL | Constraints, Python/SQL whitespace parity, ownership prerequisites, rollback, reconnect, timestamps and cleanup behavior. |
| Python fault effectiveness | 321 Python catalogue entries: 314 executable faults with per-check witnesses, three proven aliases, and four explicitly excluded invalid startup diagnostics; includes 47 provider and 11 MER-11 note faults | Every inventoried case has demonstrated relevant fault detection. Unexpected survivors, invalid experiments or timeouts fail the gate. Excluded diagnostics are not counted as successful detections. |
| SQL fault effectiveness | 607 reviewed case/fault pairs across 126 implementations | Tests reject deliberately broken constraints and database behavior on independently guarded storage. |
| Lifecycle and migration audits | Five lifecycle checks/faults and 36 migration controls | Committed behavior, locking, preservation and guarded undo/reapplication audits. |
| Independent committed migration roundtrip | Additional 383-case replay and ordered schema comparison | Real migration undo/reapplication and reconnect behavior, restricted to disposable storage. |
| Harness, reporting and cleanup controls | Scheduling, transport, isolation, inventories, CI identity adaptation, artifact validation and cleanup controls | A missing case, contradictory PASS, failed required stage or unsafe target cannot silently become successful coverage. |
| Documentation and whitespace | Link/planning validation and Git whitespace checks | Documentation portability and formatting checks remain required. |

The seven-stage runner is `tools/run_test_suite.py`. Hosted CI invokes it through `tools/run_ci.py`, which also runs original Python sources and the separate committed migration roundtrip. The outer hosted validator now enforces reviewed inventory floors, six required MER-11 test IDs, eleven named note-fault witnesses, all seven stage outcomes, the 60-second cap and cleanup/source preservation. It verifies that case/fault reports exist and hashes them into `ci-summary.json`; the workflow retains those reports for review. `tests/suite-inventory.json` remains the case/fault inventory. Future work must add tests/faults to it and update reviewed floors only with an explicit coverage review. CI certifies automated checks for implemented scope; it cannot certify a feature that does not exist or manual learner/account checks.

## Confidentiality boundary

CI provisions synthetic fixtures on fresh isolated storage. It does not need personal database contents, account credentials or inference-provider keys. Repository permissions remain read-only and checkout does not retain credentials. Uploaded artifacts are explicitly restricted to CI-owned summaries, source hashes and synthetic migration evidence; raw private environment files, credentials and unrestricted logs are not uploaded. Never enable environment dumps or add private configuration to artifacts. A scan and a green suite do not guarantee the absence of every possible disclosure.

## Run locally

```bash
.venv/bin/python tools/run_test_suite.py
```

For a focused Python unit/regression run without the live PostgreSQL module:

```bash
.venv/bin/python -m pytest -q tests tools/test_doctor.py --ignore=tests/test_users_notes_database.py
```

The current cumulative scope includes MER-1 and MER-8 through MER-11. “MER-0–MER-11” is a scope range, not a claim that every planned feature is complete. Local readiness, learner explain-back, authenticated note ownership, real repository pool behavior, sharing/fetch-by-ID and deferred MER-10 HTTP transport remain manual, unimplemented or separately scoped. The focused command does not replace the full suite. See [all suite commands](test-suite-commands.md) for prerequisites and [observed CI results](cumulative-ci-verification.md) for actual hosted evidence.

## Observed verification

[GitHub run 38756597293](https://github.com/vipravlipare/Merlin/actions/runs/38756597293) passed for commit `35607dee40a3df10670c13074d9638f80692f930`, including the complete required hosted job after removing workflow cancellation. Local verification passed 329 Python tests plus three subtests, documentation validation and whitespace checks. Structural comparison confirmed the workflow's tests, faults, permissions and artifact rules were unchanged. The publication scan inspected 339 current files and 440 historical blobs, expanding compressed evidence, and reported no findings within its pattern/local-value scope. This is not a universal confidentiality guarantee. Actual minutes are unknown.
