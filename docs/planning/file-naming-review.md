# File naming review

Reviewed all 104 maintained project files, including hidden repository configuration and compressed evidence. Filenames describe purpose; dates remain in report bodies and original archive metadata. Dependencies, Git internals, generated caches and installed third-party skill bundles retain their tool-defined names.

## Changes

Renamed 16 files and one evidence folder. Updated documentation references and the evidence generator. Required configuration names, Python module names, migration sequence numbers and numbered planning Parts remain appropriate and stable. Original compressed evidence and the setup archive retained their byte-for-byte hashes.

| Previous path | Current path |
|---|---|
| `docs/testing/case-effectiveness-audit-2026-10-11.md` | `docs/testing/case-effectiveness-audit.md` |
| `docs/testing/test-hardening-2026-10-11.md` | `docs/testing/test-hardening-and-repairs.md` |
| `docs/testing/current-verification-results.md` | `docs/testing/pre-repair-verification-results.md` |
| `docs/planning/current-failure-fix-guide.md` | `docs/planning/historical-failure-repair-guide.md` |
| `docs/setup/archive/sprint-0-original-setup-2026-10-02.tar.gz` | `docs/setup/archive/sprint-0-original-setup.tar.gz` |
| `docs/testing/evidence-2026-10-11/` | `docs/testing/case-effectiveness-evidence/` |
| `docs/testing/evidence-2026-10-11/sql-cases.md` | `docs/testing/case-effectiveness-evidence/database-cases.md` |
| `docs/testing/evidence-2026-10-11/quiz-cases.md` | `docs/testing/case-effectiveness-evidence/quiz-logic-cases.md` |
| `docs/testing/evidence-2026-10-11/browser-cases.md` | `docs/testing/case-effectiveness-evidence/quiz-browser-cases.md` |
| `docs/testing/evidence-2026-10-11/lifecycle-cases.md` | `docs/testing/case-effectiveness-evidence/database-lifecycle-cases.md` |
| `docs/testing/evidence-2026-10-11/python.json.gz` | `docs/testing/case-effectiveness-evidence/python-test-results.json.gz` |
| `docs/testing/evidence-2026-10-11/sql.json.gz` | `docs/testing/case-effectiveness-evidence/database-test-results.json.gz` |
| `docs/testing/evidence-2026-10-11/sql_timestamp_rerun.json.gz` | `docs/testing/case-effectiveness-evidence/timestamp-case-results.json.gz` |
| `docs/testing/evidence-2026-10-11/quiz.json.gz` | `docs/testing/case-effectiveness-evidence/quiz-logic-results.json.gz` |
| `docs/testing/evidence-2026-10-11/browser.json.gz` | `docs/testing/case-effectiveness-evidence/quiz-browser-results.json.gz` |
| `docs/testing/evidence-2026-10-11/lifecycle.json.gz` | `docs/testing/case-effectiveness-evidence/database-lifecycle-results.json.gz` |
| `docs/testing/evidence-2026-10-11/summary.json` | `docs/testing/case-effectiveness-evidence/audit-summary.json` |

## Reviewed inventory

| File | Purpose |
|---|---|
| `.env.example` | Environment-variable example with no real credentials. |
| `.github/workflows/setup.yml` | Automated setup verification workflow. |
| `.gitignore` | Files excluded from Git tracking. |
| `.python-version` | Required Python interpreter version. |
| `AGENTS.md` | Persistent agent instructions, safety rules and naming conventions. |
| `README.md` | Repository entry point and project navigation. |
| `app/database_connectivity_probe.py` | database connectivity probe |
| `app/note_rules.py` | Input rules to call before a future API writes notes or account email. |
| `app/notes_maintenance.py` | Foreground scheduler restricted to the known disposable Day 6 cluster. |
| `docker-compose.yml` | Local PostgreSQL and Redis service configuration. |
| `docs/README.md` | Merlin documents — start here |
| `docs/architecture/archive/users-notes-migration-audit.md` | Historical Day 6 migration audit — October 8, 2026 |
| `docs/architecture/archive/users-notes-schema-restore-review.md` | Day 6 current migration rule review — October 8, 2026 |
| `docs/architecture/part-10-threat-architecture-adrs.md` | Part 10 — D2 Threat model, architecture and ADRs |
| `docs/architecture/part-11-schema-ai-architecture.md` | Part 11 — D2 Schema, queries, AI architecture and observability |
| `docs/architecture/users-notes-design.md` | Day 6 — implemented draft rules |
| `docs/checklists/database-code-review-checklist.md` | Day 6: read these four files |
| `docs/checklists/part-06-checklists-first-half.md` | Part 06 — D12 Checklists, first half |
| `docs/checklists/part-07-checklists-second-half.md` | Part 07 — D12 Checklists, second half and release checklists |
| `docs/delivery/part-12-sdlc-p0-p4.md` | Part 12 — D3 SDLC Playbook P0–P4 |
| `docs/delivery/part-13-sdlc-p5-p12-parity.md` | Part 13 — D3 SDLC Playbook P5–P12 and parity |
| `docs/delivery/part-23-jira-pack.md` | Part 23 — D7 Jira Pack |
| `docs/delivery/part-24-audit-readiness.md` | Part 24 — D8 Audit, JD coverage and self-sufficiency |
| `docs/delivery/part-25-portfolio-share-pack.md` | Part 25 — D14 Portfolio and Share Pack |
| `docs/learning/docker-and-database-migrations.md` | What the Docker setup and first migration did |
| `docs/learning/input-type-validation-fixes.md` | Fix the eight input-validation failures |
| `docs/learning/part-14-skill-cards-first-half.md` | Part 14 — D4 Skill Cards, first half |
| `docs/learning/part-15-skill-cards-second-half-dsa.md` | Part 15 — D4 Skill Cards, second half and DSA ramp |
| `docs/learning/part-16-interview-guide.md` | Part 16 — D5 DSA, optimization and interview guide |
| `docs/learning/sprint-0-learning.md` | Sprint 0 — your setup, explained simply |
| `docs/learning/unicode-text-validation-fix.md` | Reject text that cannot encode as UTF-8 |
| `docs/planning/MASTER_NAVIGATION.md` | Merlin Master Navigation Guide |
| `docs/planning/MASTER_PROMPT.md` | MASTER PROMPT v6 (final): AI-Engineering Focus, 37-Day Agile SDLC Build (Thu Oct 1 → Fri Nov 6, 2026) |
| `docs/planning/STATE.md` | STATE.md — handoff capsule |
| `docs/planning/VERIFY_LIST.md` | 🔎 Verify list (generated) |
| `docs/planning/historical-failure-repair-guide.md` | Fix the three observed failures |
| `docs/project/part-01-waterfall-and-assumptions.md` | Part 01 — Waterfall, assumptions, scope boundary and stack decisions |
| `docs/project/part-02-project-charter.md` | Part 02 — D9 Project Charter |
| `docs/project/part-03-workflow-bible.md` | Part 03 — D10 Workflow Bible |
| `docs/project/part-05-component-breakdown.md` | Part 05 — D11 Component Breakdown |
| `docs/project/part-08-prd-epics-e0-e2.md` | Part 08 — D1 PRD, Epics E0–E2 |
| `docs/project/part-09-prd-epics-e3-e10.md` | Part 09 — D1 PRD, Epics E3–E10, velocity and risks |
| `docs/setup/archive/sprint-0-original-setup.tar.gz` | Original Sprint 0 setup documents preserved as an immutable archive. |
| `docs/setup/codex-global-skills.md` | Global Codex skills: Terminal and Windows desktop |
| `docs/setup/local-setup.md` | Merlin local setup |
| `docs/setup/part-04-environment-setup.md` | Part 04 — Environment setup and Section 8 |
| `docs/setup/postgres-python-runtime-setup.md` | Finish the Day 6 migration attempt: runtime prerequisite |
| `docs/setup/terminal-commands.md` | Terminal commands — what to use now |
| `docs/sprints/database-foundation-jira-guide.md` | Sprint 1 — simple Jira checklist |
| `docs/sprints/database-foundation-progress.md` | Day 6 verification and live Jira status |
| `docs/sprints/database-foundation-start.md` | Day 6 coding preparation — observed October 7, 2026 |
| `docs/sprints/part-17-sprint0.md` | Part 17 — Sprint 0 execution and evidence |
| `docs/sprints/part-18-sprint1.md` | Part 18 — Sprint 1, Days 6–12 |
| `docs/sprints/part-19-sprint2.md` | Part 19 — Sprint 2, Days 13–19 |
| `docs/sprints/part-20-sprint3.md` | Part 20 — Sprint 3, Days 20–26 |
| `docs/sprints/part-21-sprint4.md` | Part 21 — Sprint 4, Days 27–33 |
| `docs/sprints/part-22-sprint5.md` | Part 22 — Sprint 5, Days 34–37 |
| `docs/testing/case-effectiveness-audit.md` | Individual test effectiveness audit — October 11, 2026 |
| `docs/testing/case-effectiveness-evidence/audit-summary.json` | Aggregate case counts, injected-fault outcomes and preservation summary. |
| `docs/testing/case-effectiveness-evidence/database-cases.md` | PostgreSQL cases |
| `docs/testing/case-effectiveness-evidence/database-lifecycle-cases.md` | Committed reconnect and two-session cases |
| `docs/testing/case-effectiveness-evidence/database-lifecycle-results.json.gz` | Preserved database lifecycle results audit output, assertions and provenance. |
| `docs/testing/case-effectiveness-evidence/database-test-results.json.gz` | Preserved database test results audit output, assertions and provenance. |
| `docs/testing/case-effectiveness-evidence/fault-catalogue.md` | Injected fault catalogue |
| `docs/testing/case-effectiveness-evidence/python-cases.md` | Python cases and individual subtests |
| `docs/testing/case-effectiveness-evidence/python-test-results.json.gz` | Preserved python test results audit output, assertions and provenance. |
| `docs/testing/case-effectiveness-evidence/quiz-browser-cases.md` | Real Chromium workflow cases |
| `docs/testing/case-effectiveness-evidence/quiz-browser-results.json.gz` | Preserved quiz browser results audit output, assertions and provenance. |
| `docs/testing/case-effectiveness-evidence/quiz-logic-cases.md` | Quiz logic cases |
| `docs/testing/case-effectiveness-evidence/quiz-logic-results.json.gz` | Preserved quiz logic results audit output, assertions and provenance. |
| `docs/testing/case-effectiveness-evidence/timestamp-case-results.json.gz` | Preserved timestamp case results audit output, assertions and provenance. |
| `docs/testing/notes-unit-test-audit.md` | Manual review of the notes/maintenance tests |
| `docs/testing/notes-unit-test-deep-audit.md` | Deep review of every current unit case |
| `docs/testing/pre-repair-verification-results.md` | Verification results — October 10, 2026 (historical) |
| `docs/testing/test-hardening-and-repairs.md` | Test hardening and defect repairs — October 11, 2026 |
| `docs/testing/testing-policy-and-fault-catalogue.md` | Strict testing policy and 150 defect scenarios |
| `docs/testing/unicode-boundary-fault-catalogue.md` | Expanded fault review: 511 scenario entries |
| `docs/testing/users-notes-database-verification.md` | Verify the database foundation — 39 minutes |
| `migrations/001_users_notes.up.sql` | Apply users/notes foundation schema. |
| `migrations/002_whitespace_parity.down.sql` | Revert Python/PostgreSQL whitespace compatibility changes. |
| `migrations/002_whitespace_parity.up.sql` | Apply Python/PostgreSQL whitespace compatibility changes. |
| `package.json` | Node package metadata, package manager pin and quiz test command. |
| `pnpm-lock.yaml` | Resolved JavaScript dependency lockfile. |
| `pyproject.toml` | Python project metadata, dependency and test configuration. |
| `quizzes/sprint-0-quiz.html` | Interactive Sprint 0 learning quiz. |
| `skills-lock.json` | Installed skills provenance and revision lockfile. |
| `tests/quiz.test.js` | Test the quiz's actual JavaScript without copying its scoring implementation. |
| `tests/test_database_connectivity_probe.py` | Test probe control flow without opening PostgreSQL or reading a password. |
| `tests/test_doctor_failure_cases.py` | The setup checker must reject bad evidence without exposing command output. |
| `tests/test_note_rules_and_maintenance.py` | Unit tests: real validation, simulated database connections; no SQL runs here. |
| `tests/test_prd_lint.py` | Planning checks must find moved Parts and reject genuinely broken links. |
| `tests/test_users_notes_database.py` | Opt-in PostgreSQL checks: synthetic rows, fixed disposable cluster, always rollback. |
| `tools/audit_database_cases.py` | Exercise every SQL case against transaction-local faulty schema definitions. |
| `tools/audit_database_lifecycle.py` | Committed-fixture reconnect and concurrency tests on the isolated Day 6 DB. |
| `tools/audit_python_cases.py` | Measure real Python test outcomes and which source faults each case detects. |
| `tools/audit_quiz_browser.mjs` | Real Chromium behavior checks. All pages and faulty HTML copies stay in memory. |
| `tools/audit_quiz_cases.py` | Run the actual quiz cases against isolated faulty copies of the HTML script. |
| `tools/check_mutations.py` | Check known behavioral faults in memory; application files and databases stay untouched. |
| `tools/doctor.py` | Read-only setup checks. Captured command output is never printed verbatim. |
| `tools/prd_lint.py` | prd_lint.py: checks planning docs against the master prompt's rules. |
| `tools/setup_local.py` | Create private local inputs when absent, then start this checkout's services. |
| `tools/test_doctor.py` | Regression checks for private output and meaningful authentication proof. |
| `tools/write_test_audit.py` | Render case-by-case evidence from completed, genuine audit runs. |
| `uv.lock` | Resolved Python dependency lockfile. |
| `docs/planning/file-naming-review.md` | This inventory, rename record and verification outcome. |

## Verification

Documentation lint passed with zero errors and the existing incomplete-schedule warning. The report generator produced exactly the same 13 evidence files under their new names in a temporary directory. Seven archive hashes matched before and after. No maintained file or folder has a calendar date in its name; no archived result or assertion was rewritten. Dates inside historical records remain evidence of when a run occurred. Naming rules are recorded in repository `AGENTS.md`.
