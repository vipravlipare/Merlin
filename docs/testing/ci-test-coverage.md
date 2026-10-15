# What runs automatically in CI

The cumulative verification workflow runs on every ordinary push to any branch and on pull requests, with no path or branch filters. Manual execution remains available. New pushes no longer cancel earlier runs through a workflow concurrency group. Each hosted job uses its own runner and independently owned synthetic database storage. GitHub capacity, service limits, explicit skip instructions or manual cancellation can still prevent completion; verify the run outcome rather than assuming every event passed.

A local `git commit` does not contact GitHub. Run the local suite before publishing, then push the commit to trigger hosted CI. A push containing several commits tests the final branch revision, rather than creating a separate job for every intermediate commit. Push commits separately if each revision needs its own observed run. No automatic Git hooks or automatic pushes are installed.

📚 Learn first: [GitHub push events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#push), which revision is checked; [workflow concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency), cancellation and pending runs. Official sources checked October 15, 2026.
↩ Return: open Actions, select the pushed commit, and inspect every required step and its synthetic verification artifact.

## Unit tests and real-system tests serve different purposes

A unit test checks a small piece of actual code in isolation. Existing Python tests exercise validation, email normalization, Unicode/whitespace boundaries, maintenance decisions, probe failure handling and setup safety. Database connectors are replaced with controlled test doubles where appropriate; assertions still execute the real application functions. JavaScript tests exercise the actual quiz logic.

Database and browser checks remain integration or system tests. Replacing PostgreSQL with a mock cannot prove database constraints, transaction rollback, reconnect persistence, locks or migration reversal. A simulated browser cannot prove the actual browser workflow. Renaming those checks as unit tests would not add coverage and converting them to mocks would remove important proof. All existing test bodies, assertions and fault inventories are retained.

## Required execution map

| Layer | Existing execution in CI | What it establishes |
|---|---|---|
| Locked setup and doctor unit regressions | Locked Python/Node environments, `tools/test_*.py`, setup and doctor static/runtime checks | Fresh-runner prerequisites, isolated services and fail-closed setup behavior. |
| Python unit and regression tests | Original source tests before adaptation, then the complete suite baseline; 332 Python case/subtest inventory IDs | Actual application helpers, controlled connection failures, non-disclosure, maintenance guards and setup/documentation behavior. |
| PostgreSQL integration tests | 383 case IDs against real disposable PostgreSQL | Constraints, Python/SQL whitespace parity, ownership prerequisites, rollback, reconnect, timestamps and cleanup behavior. |
| JavaScript unit/regression tests | 40 quiz case IDs | Actual quiz scoring, state and input handling. |
| Python fault effectiveness | 232 canonical faults, three proven aliases; four explicitly excluded invalid startup diagnostics | Every inventoried case has demonstrated relevant fault detection. Unexpected survivors, invalid experiments or timeouts fail the gate. Excluded diagnostics are not counted as successful detections. |
| SQL fault effectiveness | 607 reviewed case/fault pairs across 126 implementations | Tests reject deliberately broken constraints and database behavior on independently guarded storage. |
| JavaScript and browser faults | 37 JavaScript faults and 16 real-browser workflows with isolated faults | Logic failures and actual browser interaction failures are detected. |
| Lifecycle and migration audits | Five lifecycle checks/faults and 36 migration controls | Committed behavior, locking, preservation and guarded undo/reapplication audits. |
| Independent committed migration roundtrip | Additional 383-case replay and ordered schema comparison | Real migration undo/reapplication and reconnect behavior, restricted to disposable storage. |
| Harness, reporting and cleanup controls | Scheduling, transport, isolation, inventories, CI identity adaptation, artifact validation and cleanup controls | A missing case, contradictory PASS, failed required stage or unsafe target cannot silently become successful coverage. |
| Documentation and whitespace | Link/planning validation and Git whitespace checks | Documentation portability and formatting checks remain required. |

The ten-stage runner is `tools/run_test_suite.py`. Hosted CI invokes it through `tools/run_ci.py`, which also runs original Python sources and the separate committed migration roundtrip. `tests/suite-inventory.json` is the reviewed inventory: execution cannot regenerate it to accept missing cases. Future work must add its tests and applicable faults to the suite and inventory as part of implementation. CI cannot certify an API that has not been implemented or manual account/learning checks.

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

The focused command does not replace the full suite. See [all suite commands](test-suite-commands.md) for prerequisites and [observed CI results](cumulative-ci-verification.md) for actual hosted evidence.
