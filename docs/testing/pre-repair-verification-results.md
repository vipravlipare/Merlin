# Verification results — October 10, 2026 (historical)

Superseded by the [October 11 test-hardening and repair report](test-hardening-and-repairs.md). The runs below are retained as historical evidence; they do not describe the repaired source or installed schema.

This run fixes test gaps and tooling failures. Application helpers, the migration and database storage were not changed. Earlier audit counts describe earlier runs.

## Results

| Check | Actual result |
|---|---|
| `.venv/bin/python -m pytest -q` | 138 passed; 3 subtests passed |
| `pnpm test` | 32 quiz JavaScript tests passed |
| `.venv/bin/python tools/prd_lint.py docs/planning` | PASS: 25 Parts; zero errors or broken file links; one future-calendar warning |
| `.venv/bin/python tools/check_mutations.py` | All 25 injected Python faults detected; zero survivors |
| JavaScript mutation experiment | All 8 injected quiz faults detected; zero survivors |

## What changed

- Permanent Unicode tests reject lone high/low surrogates, embedded surrogates and literal surrogate pairs through every text entry point. Valid emoji and supplementary Unicode remain accepted.
- Maintenance tests assert the entire ordered SQL sequence, bound values and connection target. Unexpected SQL now fails a test. Database calls are mocked; these tests never run cleanup.
- The planning linter discovers Parts in their topic folders, checks Markdown/reference/HTML local file links, and distinguishes calendar entries from references to days. Twelve regression cases cover these changes.
- Moved-file references were repaired. Two learning sections now have explicit learning and return instructions.
- `pnpm test` runs the actual quiz script with Node’s built-in runner. Tests cover scoring, missing answers, critical questions, restore validation and deterministic shuffling. No placeholder test command remains.

## Python mutation evidence

Each fault is injected separately in memory into a fresh process. The unmodified baseline must pass first. A fault counts as detected only when pytest reports failing assertions, rather than collection errors or a timeout. No mutant is written to application files.

| Injected fault | Failing cases |
|---|---|
| emoji-weight-one | 16 |
| codepoint-instead-of-grapheme | 13 |
| title-bound-relaxed | 5 |
| title-bound-too-strict | 3 |
| body-bound-relaxed | 3 |
| body-bound-too-strict | 3 |
| body-stripped | 9 |
| real-title-stripped | 1 |
| email-lowercased | 2 |
| blank-title-stored-empty | 8 |
| draft-delete-protection-removed | 4 |
| nul-check-removed | 5 |
| target-check-skipped | 5 |
| identity-or-changed-to-and | 2 |
| target-port-original-db | 3 |
| batch1001-allowed | 1 |
| lock-timeout-removed | 3 |
| wrong-expiry-function | 4 |
| once-flag-ignored | 1 |
| custom-interval-ignored | 1 |
| cli-error-secret-leaked | 2 |
| strict-batch-guard-removed | 5 |
| strict-draft-guard-removed | 3 |
| utf8-guard-removed | 16 |
| unexpected-extra-sql | 3 |

The previous survivors now fail: removing UTF-8 validation triggers 16 failures; inserting unexpected SQL triggers 3 failures. These are deliberate faulty copies, not failures in the current code.

The eight JavaScript faults alter the pass threshold, bypass critical/missing-answer checks, invert scoring, allow duplicate question/choice IDs or invalid choices, and disable shuffling. Each causes a real assertion failure. Temporary quiz copies are removed after each experiment.

## Limits and next action

The remaining linter warning concerns missing primary DAY 7–37 calendar entries. It does not block linting; short future-day templates remain unexpanded. Heading fragments and external website availability were not checked by the local file-link scan.

These results do not prove that every possible defect is covered. The 511 catalogue entries remain proposed checks, not 511 executed faults. JavaScript browser interaction and persistence across real browser reloads are not verified by the pure-logic tests.

Actual PostgreSQL valid/invalid inserts, transaction rollback, reconnect, limited-role ownership and cleanup behavior remain PENDING. Migration undo/reapplication remains PENDING because the down migration is missing. No authenticated backend exists yet. Do not mark those Jira acceptance boxes complete.

Next: the learner prepares one valid synthetic user/note case on the verified disposable `merlin_d6` cluster, records expected results, and runs it before the negative cases. Do not rerun the applied up migration. Preserve Sprint 0 storage.

Day 6 remains capped at 360 minutes: implementation 60 minutes and verification 39 minutes. Actual learner minutes are unknown. DSA and AWS remain deferred.

📚 Learn first: [database verification guide](users-notes-database-verification.md), especially the difference between helper tests and database acceptance tests.
↩ Return: record actual PASS/FAIL/PENDING for the first database case; no passing result may be inferred from this helper test run.
