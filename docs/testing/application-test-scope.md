# Application-only cumulative test scope

Recorded October 23, 2026. The learner explicitly requested removal of personal quiz tests and fault injections. This changes the accepted suite scope; it does not suppress a failing application requirement. The quiz HTML remains available for personal learning. Historical results remain historical and are not rewritten. Actual work minutes are unknown. No project commit, push or workflow dispatch was performed.

📚 Learn first: [current execution map](ci-test-coverage.md), [suite commands](test-suite-commands.md), [individual necessity reviews](test-suite-second-review.md), [health API contract](../architecture/health-api-contract.md) and [decoder contract](../architecture/local-provider-contract.md).
↩ Return: run the seven retained stages, review their actual outcomes and keep hosted exact-commit verification pending until separately authorized publication.

## Deliberately removed

- All 40 personal quiz JavaScript cases and 37 quiz logic faults.
- All 16 personal quiz browser workflows and their mutations.
- The quiz-only external HTML link-check parameter and automatic quiz-directory scan. Generic Markdown/HTML link parsing, README/AGENTS entrypoint checks and documentation validation remain verification-harness checks.
- Quiz/browser result validators, fixtures, classifier controls, scheduler lane and inventory keys.
- Quiz-only Playwright manifests, CI browser installation/environment and the npm quiz-test command. Node/pnpm setup remains because Sprint 0 setup/doctor checks still verify those implemented prerequisites.

Removed source files: tests/quiz.test.js, tools/audit_quiz_cases.py, tools/audit_quiz_browser.mjs, .github/ci/browser/package.json and .github/ci/browser/package-lock.json. The test-evidence renderer now consumes Python, SQL and lifecycle reports without requiring quiz/browser reports or the historical focused F077 rerun.

The generic runner still proves baseline-first execution, concurrent independent Python/database work, serial database fallback, failed prerequisites, first-failure stopping, interrupts, exact inventories, intended assertion attribution, source freshness, isolation and cleanup. Only controls tied to removed quiz/browser requirements were removed; a new scope control checks the seven retained stages and absence of generated quiz/browser environment settings.

## Every retained category has an implemented owner

| Implemented work | Retained tests/faults | Boundary and limits |
|---|---|---|
| Sprint 0 foundation | tools/test_doctor.py, tests/test_doctor_failure_cases.py; setup/doctor faults | Reproducible setup, runtime/static checks, synthetic service authentication, safe diagnostic evidence and refusal of unsafe configuration. These are foundation checks, not future application login tests. |
| Planning and verification harness | tests/test_prd_lint.py, linter faults and runner/transport/isolation controls | Portable project guides, precise planning rules, trustworthy outcomes, guarded execution and cleanup. These support the implemented learning project and its CI; they are not product features. |
| Day 6 / MER-1 | tests/test_note_rules_and_maintenance.py, tests/test_database_connectivity_probe.py, tests/test_users_notes_database.py; note/probe/SQL faults | Actual validation, Unicode and whitespace limits, database constraints/roles, save/delete/maintenance behavior, bounded workers, transaction failure/reconnect and safe probe failures. SET ROLE tests prove database permissions; authenticated API ownership is still unimplemented. |
| Day 6 preservation and migration safety | SQL case/fault audit, lifecycle audit, migration undo/reapply controls and separate committed rehearsal | Actual foreign keys, committed cascade, locks, rollback, purge/expiry bounds, synthetic migration roundtrips, refusal gates, source preservation and owned cleanup. Never apply faulty migrations to protected source storage. |
| Day 7 / MER-8 | tests/test_health_api.py and health API faults | Implemented scratch health endpoint, route/method handling, safe error bodies, no file disclosure, loopback server behavior and resource cleanup. |
| Day 8 / MER-9 | Recorded local-model readiness observations | Manual readiness remains separately attributed. No automated model-quality, production inference or hosted-provider claim is added. |
| Day 9 / MER-10 | All 467 tests/test_local_provider.py cases and 47 provider faults | Actual byte decoder framing, strict JSON/UTF-8/schema, exactly-one completion, clean EOF, resource bounds, fixed failures, no partial success/retry/disclosure and no decoder external calls. HTTP transport/deadlines/proxy/redirect/fallback/cancellation remain deferred. |

“MER0–MER10” means the cumulative implemented foundation through MER-10. It does not assert that eleven numbered stories exist or that future planned features are built. The remaining 815 Python case/subtest IDs, 297 canonical Python faults, three aliases, four excluded diagnostics, 383 SQL cases, 607 SQL case/fault applications, five lifecycle cases and migration inventories remain explicitly reviewed. All 126 retained runner controls and five Python isolation controls protect this execution. Excluded diagnostics are not successful fault detections.

Every retained Python node, fault behavior, SQL pairing and migration inventory is unchanged from the prior audit except the single deliberately removed quiz link parameter. Removing the quiz scan changes breadth-first AST indexes: all 28 linter faulty ASTs were compared after deleting only that scan, proving identical retained faulty behavior; 25 catalogue IDs were deliberately renamed. The exact old/new identities and proof are recorded in the results receipt. The first complete run correctly failed its inventory gate until these reviewed names were reconciled; its 815 Python case IDs and 297 canonical fault outcomes had passed. The [earlier complete per-case evidence](precommit-suite-audit-evidence.json.gz) and [historical rationale index](test-necessity-review/complete-case-index.csv) remain useful source snapshots. Current source hashes and actual selected outcomes are recorded in the [application-only results](application-test-scope-results.json); earlier complete-suite receipts do not certify changed harness inputs.

## Verification

Current local complete-suite and fresh synthetic CI-entry outcomes are recorded in the results receipt. The complete runner now has seven mandatory stages: Python/database baseline; Python fault effectiveness; SQL fault effectiveness; database lifecycle; migration audits; documentation; whitespace. It retains every applicable application/security/preservation assertion. The separate CI-entry committed rehearsal remains required.

Observed application-only result: all seven local stages PASS in 59.44176 seconds. Fresh synthetic CI-entry execution PASS in 97.291 seconds, including its own complete suite and the separate committed 383-case migration rehearsal. Source preservation and owned cleanup PASS. The 1,195 tests plus three subtests and all 297 canonical Python faults passed their required gates; all 815 Python case/subtest IDs demonstrate detection. SQL/lifecycle/migration inventories and 126 runner controls passed. No unexpected survivor, invalid experiment, timeout or unapplied fault remains. Final receipt/handoff documentation edits were checked after execution.

Finite tests and fault injections do not establish universal correctness/security, independent learner authorship, a working model transport or model quality. Hosted CI remains pending for these unpublished changes. Runtime comparisons with the old suite describe removal of personal-learning scope, not a faster Python implementation.

📚 Learn first: [cumulative CI gate](../delivery/cumulative-ci-gate.md) and [Day 9 handoff](../planning/day-nine-handoff.md).
↩ Return: inspect the application-only receipt and final diff; separately authorize publication, then observe the exact hosted revision before closing MER-10 item 4.4 or beginning Day 10.
