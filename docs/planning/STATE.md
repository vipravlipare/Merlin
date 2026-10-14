# STATE.md — handoff capsule

Timeline: Oct 1–Nov 6, 2026, 37 days. S0 10 h; S1–S4 34 h each; S5 20 h. Targets: Knowledge Core Day 26; Agentic Core Day 33. Frameworks require swaps.

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
MER-1 step4: docs/testing/database-step-four-verification.md. PostgreSQL389 PASS in139.40s; reconnect/cascade and cleanup rollback baselines PASS; fingerprint/identity/empty tables preserved. 4.1–4.4 technical PASS;fresh disposable 4.3 proof. Learner001down TODO3–9 written;roundtrip two branches PASS,388 cases each. Down repairs:inventory/postchecks/header fixed;17 regressions PASS;source history unresolved. Evidence docs/testing/users-notes-down-migration-review.md. SQL ownership PASS;authenticated API PENDING. Steps1/3.3 learner-confirmed complete. Secret review PASS within scope;MER-1 Done confirmed in Jira.

Oct12–13 exhaustive necessity/performance review: all801original case/subtest rows,239Python faults,55legacy repeats,71SQLimplementations/653pairs,35JSfaults,16browser/5lifecycle faults,36migration controls and runner safeguards reviewed individually. Repaired fixture-only detections,wrongNULL-email oracle and false-PASS/contradictory-result gates. Consolidated27original cases;added2necessary cases. Current773ordinary+3subtests;Python232canonical+3provenaliases+4excludedstartupdiagnostics;SQL607pairs/126implementations;JS37;browser16;lifecycle5;migration36;infrastructure128. Bothmigrationundo/reapplybranchesactual;382businesscasesreplayedonceonlywithsame-run ordered-schema/runtime/target/source equivalence. Cross-branch resultgatecounterfactualsPASS. Freshsetupoverlapsrollback-onlybaselines;faultcontrolsafterbaselines;failure/interruptcleanupverified. Sourceapplication/migrationsunchanged. Default8Pythonworkers+2serialSQLpartitionson4guardedcopies;complete10-stagePASS36.83s,priorpartitiontrial41.63s. All773+3cases/faultsunchanged;15merge/selector+1routecontrolsadded. Historical43→51slowdown:workerdefaultmistakefixed;broaderhostvariationunproven. Proof:docs/testing/test-suite-parallel-sql-performance.md. Usermade38stargetoptional;correctnessfirst. Copywallnowincludespreflight/baselines,notcomparableold34.48s. Evidence:docs/testing/test-suite-second-review.md;individualCSV/JSON,durablefullreports. Finitecoverageisnotuniversalsecurityproof. Actualminutesunknown.

Earlier authorized probe,maintenance,Unicode,quiz,doctor and linter repairs remain in docs/testing/case-effectiveness-audit.md, now qualified by the necessity review. Never weaken assertions/security;repair responsible code. Assistant authored authorized fixes;learner mastery unassessed.001unchanged;002previously applied;never rerun applied up migrations.

Browser reload/submission/retry/restart/storage/print and committed reconnect/cascade, two-session expiry/purge locks, batch limit and rollback verified. Synthetic fixtures deleted; schema/ACL/role/index/default/trigger/view fingerprints and final Day6 identity/empty tables PASS. Scheduler stopped. Preserve Sprint0 merlin_postgres_data/cluster7691749973399031842. Isolated target merlin_d6/cluster7694311451826794534.

NEXT:MER-8 Day7 section1 learner-confirmed complete, not independently reverified. Review assistant-authored docs/architecture/health-api-contract.md (2.1), answer three explain-back questions;then design2.2negative cases and2.3fixtures before learner writes Python3.12server. Port8000brief127.0.0.1bind PASS Oct14;released,notreserved. No API implementation/runtime proof;CI status unverified;actual minutes unknown. Section2budget15+15+10=40min;Day7budget216+24reserve=240. Jira unchanged. Preserve database evidence/volumes. OmniRoute permanent client configuration remains pending;do not claim future sessions routed. AWS/DSA deferred.
