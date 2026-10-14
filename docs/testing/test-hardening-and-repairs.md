# Test hardening and defect repairs — October 11, 2026

Historical repair report. Current case totals, browser/concurrency evidence and additional defects are in the [individual case effectiveness audit](case-effectiveness-audit.md).

The previous session's failures were reproduced before repair. The learner then explicitly requested fixing responsible code and recording a rule against compromising functionality or security to obtain passing tests. That request authorized the assistant-authored repairs below. These changes do not establish learner mastery or completion of the remaining application.

## What failed, why, and what changed

| Defect | Reproduced behavior | Responsible repair |
|---|---|---|
| Probe database error handling | `ProgrammingError` escaped rather than producing the sanitized failure and exit status 1. Expanded tests showed the same problem for `DataError` and `InternalError` during connection entry, read-only setup, cursor entry, execution, fetching and transaction exit. | `app/database_connectivity_probe.py` catches `psycopg.Error`, produces a generic stderr message, and exits 1. It still exposes unrelated programming errors and reports success only after connection context exit. |
| Python/PostgreSQL whitespace disagreement | Python treated eight characters as whitespace that the installed SQL POSIX class treated as content. SQL admitted empty-looking saved notes and padded emails, failed to normalize titles, omitted blank-body deadlines, refused owner deletion of blank drafts, and disagreed with maintenance visibility/expiry rules. | Separate migration 002 installs shared PL/Python blank-text and email-cleanliness predicates, then updates every affected constraint, trigger, cleanup predicate and policy. Original migration 001 was not rerun. |
| Quiz answer storage | `typeof []` is `object`; `validSaved` accepted empty, dense and sparse answer arrays. Assigning question-ID keys to an array can create NULL holes when JSON is saved, making later restoration reject progress. | `quizzes/sprint-0-quiz.html` explicitly rejects answer arrays. Valid object maps, including empty maps and repeated JSON round trips, remain accepted. |
| Maintenance malformed-identity handling — newly exposed | Missing identity rows, NULL cluster identifiers and nonnumeric identifiers escaped as raw `TypeError`/`ValueError`. A nonnumeric identifier appeared in the exception text. Cleanup was blocked, but the CLI's generic failure contract was broken. | `app/notes_maintenance.py` converts only identity parsing failures into a generic `RuntimeError`, with exception chaining suppressed. The existing CLI handler sanitizes that error. Identity and cleanup safety gates remain required. |

The eight SQL/Python disagreements were U+001C, U+001D, U+001E, U+001F, U+0085, U+00A0, U+2007 and U+202F. This is an observation of the installed database, not a claim that every PostgreSQL locale classifies characters identically.

📚 Learn first: [Python string whitespace operations](https://docs.python.org/3.12/library/stdtypes.html#str.isspace), read `str.isspace` and `str.strip`; [PostgreSQL pattern matching](https://www.postgresql.org/docs/17/functions-matching.html), read the POSIX character-class and locale discussion; [Psycopg exceptions](https://www.psycopg.org/psycopg3/docs/api/errors.html), read the exception hierarchy. All were opened October 11, 2026.
↩ Return: explain why a database rejection must identify the intended constraint, why successful execution does not prove successful transaction exit, and why invisible text is not always whitespace. Done when you can predict the relevant positive and negative test outcomes without running them. Time box: 15 minutes within the existing learner budget. If stuck, compare each defect with its named regression test.

## Stronger regression proof

Added 271 executable cases across four existing test files:

- Probe: 25 additions cover four database error classes across six stages and preserve propagation of unrelated programming bugs.
- Python text/maintenance: 35 additions cover every whitespace character in title normalization, draft handling, real-content preservation and email handling; three invisible nonwhitespace characters; and three malformed identity responses at the actual CLI boundary.
- PostgreSQL: 206 additions cover all 29 whitespace characters separately through title normalization, body deadlines, three email cases, owner draft deletion and limited-role maintenance. U+200B, U+FEFF and U+2060 must remain real content. A final module gate proves that identity is unchanged and both tables are empty after all rollback-only tests.
- Quiz: five additions cover array shapes, repeated JSON restoration and validation across JavaScript execution contexts. Existing scoring, critical-question, missing-answer and shuffle checks remain intact.

Expected outcomes were not relaxed. The existing low-level malformed-identity assertion was updated from raw conversion exceptions to the new deliberate sanitized `RuntimeError` contract; it still proves that the sole query is identity lookup and cleanup never runs. This is a documented code behavior change, not acceptance of the original failure.

## Actual runs

| Stage | Python | Disposable PostgreSQL | Quiz JavaScript |
|---|---|---|---|
| Original suites, before repair | 208 passed, 1 failed; 183 DB cases skipped; 3 passing subtests | 169 passed, 14 failed | 34 passed, 1 failed |
| Strengthened suites, before repair | 247 passed, 22 failed; 389 DB cases skipped; 3 passing subtests | 319 passed, 70 failed | 36 passed, 4 failed |
| After code repair | 269 passed; 389 DB cases skipped; 3 passing subtests | 389 passed | 40 passed |

The strengthened failing baseline contained 96 failing cases across four causes, not 96 independent application defects. The old assertions were retained. Known failures were never marked skipped or expected failures to obtain a green suite.

Final combined result: **698 passing cases, zero failures**, plus three passing Python subtests. Database tests were executed separately rather than counted as passes from the default suite's skip output. Original database run: 67.92 seconds; strengthened failing database run: 148.48 seconds; repaired database run: 141.40 seconds. The final database module's identity/empty-table teardown passed.

Post-repair Python mutation checks detected all 55 existing injected faults, using the complete maintenance/text unit suite without deselections. The earlier investigative mutation run excluded the newly failing malformed-identity tests so its baseline could pass; it is superseded by the complete post-repair mutation run. Those 55 faults concern text rules and maintenance, not every possible probe, SQL or browser defect.

Commands used:

```bash
.venv/bin/python -m pytest -q --tb=short
MERLIN_RUN_DB_TESTS=1 .venv/bin/python -m pytest -q tests/test_users_notes_database.py --tb=short
pnpm test
.venv/bin/python tools/check_mutations.py
git diff --check
```

## Database migration and preservation evidence

The identity gate confirmed database `merlin_d6`, cluster `7694311451826794534`, and empty users/notes tables before schema repair. Migration 002 has forward and rollback files. A transaction-only dry run applied the forward changes, checked NULL/Unicode helper behavior and helper ownership/permissions, applied the rollback, and compared original function definitions, owners, ACLs, constraints and policies. That comparison passed; the entire dry run rolled back.

The forward migration was then committed once to the disposable Day 6 database. Constraints were validated normally; no rows were deleted to make validation succeed. No privileges were broadened on protected tables, no actor policy was removed, and cleanup functions remain invoker functions with bounded batch behavior. New helper execution is restricted to the existing owner/app/maintenance roles; PUBLIC execution is revoked. The final database suite checks the relevant limited-role behaviors.

The preserved Sprint 0 cluster `7691749973399031842` was excluded from every database command. No container, volume, password, role-login credential or running scheduler was changed. Migration 001's down migration remains missing; migration 002's validated rollback does not resolve that separate gap. Do not rerun either applied up migration.

📚 Learn first: [PostgreSQL CREATE FUNCTION](https://www.postgresql.org/docs/17/sql-createfunction.html), read replacement semantics, NULL handling and invoker security; [PL/Python data values](https://www.postgresql.org/docs/17/plpython-data.html), read NULL handling; [Array.isArray](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/isArray), read why it distinguishes arrays from objects. Verified October 11, 2026.
↩ Return: review migration 002 and the quiz guard, then explain why NULL must return a deliberate boolean in the helper and why the SQL repair must change installed definitions. Done when you can identify the forward and rollback effects without copying the implementation. Time box: 10 minutes within the existing learner budget. If stuck, compare migration 002 with migration 001 and the corresponding regression case.

## Limits and remaining work

No finite test suite is ironclad. These results cover the current helpers, installed schema and quiz logic. They do not prove authenticated API ownership, because an authenticated backend does not exist yet. Browser rendering, event handling and real localStorage reloads still require browser verification. The quiz tests execute its actual pure logic and JSON round trips; they do not simulate a browser UI.

Committed user/note persistence after reconnect and migration 001 undo/reapplication remain unproven. Concurrent cleanup/locking behavior and performance require separate evidence; sequential cases are not proof of concurrency. Do not mark these acceptance items complete.

Actual learner minutes are unknown. Assistant-authored repair and test evidence is not a learner-authored implementation claim. No Jira changes, commit, push or upload were performed. The correctness/security rule is recorded in repository `AGENTS.md`.
