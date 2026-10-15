# STATE.md — handoff capsule

Timeline: Oct1–Nov6,2026;37days. S0 10h;S1–S4 34h each;S5 20h. Targets:KnowledgeCore Day26;AgenticCore Day33. Frameworks require swaps.

Decisions:
- Stack: Python/FastAPI modular monolith; PostgreSQL + pgvector; React/TypeScript; Ollama local-first; Docker Compose; MCP after scratch tools/agent loop.
- Cloud: AWS conditional; local release default $0. Budget alerts are not hard caps.
- ADR-01 one Python app; ADR-02 Postgres/vector-first; ADR-03 local provider boundary; ADR-04 lean React + SSE; ADR-05 local-first/AWS conditional; ADR-06 scratch before frameworks.
- Cut line: after protected scratch core/rung 2, before framework/platform breadth. C-16–C-19 and C-24 have zero funded hours; optional work is swap-not-add.
- Security/evals: auth, owner filters, injection defenses, redaction/consent, golden sets and regression checks stay core.

ID registry:
- Components C-01–C-24; skills SK-01–SK-22.
- Epics E0–E10 reserved; story pattern E2-US04; checklist pattern C-07.3.
- ADR-01–ADR-06 delivered; ADR-07–ADR-12 reserved conditional.
- RDY-01–RDY-04 and DONE-01–DONE-08 defined.

Consistency numbers:
- Floor 166.00 h; exact 10% reserve 16.60; committed ceiling 149.40.
- DSA 13.75; rituals 21.75; ceremonies 9.00; net Learn + Implement 104.90.
- Planned split: Learn 42.00; Implement/setup/tests/docs/evidence 62.90.
- Points prior: 1 point ≈ 1.5 beginner net hours; ~69.9 point-equivalents.
- Sprint net: S0 7.50; S1 21.05; S2 21.55; S3 21.05; S4 21.55; S5 12.20.
- Component likely ledger total 104.90; low 72.50; high 173.50.

Rule Card: R1 Learn→Return everywhere; R2 official links only; R3 learner owns feature code, Oct11 explicitly authorized defect repairs/tests; R4 explain-back, acceptance test, whiteboard, re-quiz; R5 honest hours and swap-not-add; R6 security in stories; R7 public-source parity/ADRs; R8 Jira-native ≤90-min tasks; R9 stop-anywhere; R10 terse chat; R11 files truth + STATE; R12 scratch before frameworks; R13 ≥20-case golden set, baseline, metric, latency and cost for AI. Never weaken tests/security to obtain green results; repair responsible code when authorized.

Global skills/preferences installed in WSL and Windows. Oct14 OmniRoute gateway, native Responses and fresh temporary Codex tool-loop/free-fallback checks PASS; primary connection restored. Permanent WSL/Windows Codex defaults NOT installed; fresh Desktop routing/activation PENDING. Resume global config/auth/startup installation and verify actual fresh clients. Details: docs/setup/codex-global-skills.md (earlier audit).

Last Part: Oct7 PASS; cluster7691749973399031842 preserved. MER-1 replaces deleted children.
MER-1 step4: docs/testing/database-step-four-verification.md. PostgreSQL389 PASS in139.40s; reconnect/cascade and cleanup rollback baselines PASS; fingerprint/identity/empty tables preserved. 4.1–4.4 technical PASS;fresh disposable 4.3 proof. roundtrip two branches PASS,388 cases each. Down repairs:inventory/postchecks/header fixed;17 regressions PASS;source history unresolved. Evidence docs/testing/users-notes-down-migration-review.md. SQL ownership PASS;authenticated API PENDING. Steps1/3.3 learner-confirmed complete. Secret review PASS within scope;MER-1 Done confirmed in Jira.

Oct12–13 exhaustive necessity/performance review: all801original case/subtest rows,239Python faults,55legacy repeats,71SQLimplementations/653pairs,35JSfaults,16browser/5lifecycle faults,36migration controls and runner safeguards reviewed individually. Repaired fixture-only detections,wrongNULL-email oracle and false-PASS/contradictory-result gates. Consolidated27original cases;added2necessary cases. Current773ordinary+3subtests;Python232canonical+3provenaliases+4excludedstartupdiagnostics;SQL607pairs/126implementations;JS37;browser16;lifecycle5;migration36;infrastructure128. Bothmigrationundo/reapplybranchesactual;382businesscasesreplayedonceonlywithsame-run ordered-schema/runtime/target/source equivalence. Cross-branch resultgatecounterfactualsPASS. Freshsetupoverlapsrollback-onlybaselines;faultcontrolsafterbaselines;failure/interruptcleanupverified. Sourceapplication/migrationsunchanged. Default8Pythonworkers+2serialSQLpartitionson4guardedcopies;complete10-stagePASS36.83s,priorpartitiontrial41.63s. All773+3cases/faultsunchanged;15merge/selector+1routecontrolsadded. Historical43→51slowdown:workerdefaultmistakefixed;broaderhostvariationunproven. Proof:docs/testing/test-suite-parallel-sql-performance.md.  Copywallnowincludespreflight/baselines,notcomparableold34.48s. Evidence:docs/testing/test-suite-second-review.md;individualCSV/JSON,durablefullreports. Finitecoverageisnotuniversalsecurityproof.

Earlier repairs: docs/testing/case-effectiveness-audit.md; necessity review qualifies findings. Never rerun applied migrations.

Browser reload/submission/retry/restart/storage/print and committed reconnect/cascade, two-session expiry/purge locks, batch limit and rollback verified. Synthetic fixtures deleted; schema/ACL/role/index/default/trigger/view fingerprints and final Day6 identity/empty tables PASS.  Preserve Sprint0 merlin_postgres_data/cluster7691749973399031842. Isolated target merlin_d6/cluster7694311451826794534.

Oct14 authorized publication/refactor review: current files and reachable history scanned; personal security records sanitized.17commits rewritten with private external backup;Day6now4ca8cd83. Remote sanitized via approved lease. Fixed standalone schema-order oracle and compressor retry/privacy;removed two dead/duplicate branches. Full baseline43.12s,after40.32s PASS;88runner controls and3counterfactuals PASS;standalone383cases PASS20.44s. Migration bytes/ordinary inventory preserved. Details:docs/testing/documentation-publication-security-review.md. Committed787af8a.

NEXT: Day7 cumulativeCI PASS88934c1f4391fa4448c721d7f52f462dd8ae60bd/run38750908546;prior177e755/run38746965661alsoPASS. User requested all retained tests/faults on each commit. Complete coverage already integrated;removed workflow concurrency cancellation so newer pushes preserve older runs. Existing unit tests retained;real database/browser tests remain integration checks. Docs:docs/testing/ci-test-coverage.md. Published35607dee40a3df10670c13074d9638f80692f930;run38756597293PASS. Local-only commits cannot trigger GitHub;multi-commit pushes test tip. No app/tests/migration/inventory changes. API learner-owned/unimplemented;2.1answers need correction;2.2/2.3design ready. Section3 swapped15min decision+50min repair;minutesunknown. Future days require cumulative previous-dayCI. OmniRoute defaults PENDING;preserve volumes;AWS/DSA deferred.
