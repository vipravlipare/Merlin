# Part 17 — Sprint 0 execution and evidence

Canonical calendar: Days 1–5, October 1–5, 2026; no separate Day 0. Environment/service requirements and reproduction commands live in [Part 04](part-04-environment-setup.md). Original ten documents remain recoverable in [the verified archive](archive/setup-sprint0-originals-2026-10-02.tar.gz). All Day 4 file changes are planning documents; doctor/CI remain specifications as explicitly requested.

## Day 4 closure checklist

📚 Learn first: [README guidance][readme], getting started; [Compose down](https://docs.docker.com/reference/cli/docker/compose/down/), volume lifecycle; stop before deployment (inside existing blocks).
↩ Return: compare each requested outcome with dated evidence below; never infer learner learning or elapsed time from assistant execution.

| Requested outcome | Result |
|---|---|
| LEARN: reproducibility explanation | Answer and questions delivered; learner explain-back pending |
| VERIFY: recreation, same volume/cluster, Redis disposable policy, safe stop | PASS October 2; both services remain stopped with ExitCode 0; both named volumes retained in follow-up check |
| DOCUMENT: sanitized Section 8/hardware evidence, troubleshooting, SETUP outline | Delivered below; assistant-prepared, not falsely attributed to learner |
| CI/DOCTOR: specifications only | Delivered below with inputs, outcomes, failure/security criteria; no workflow/script required by this block |
| DSA | Deferred by earlier explicit learner instruction; 30-minute slot uncommitted |
| RITUAL: status, actual minutes, spill | Stand-up/next action/spill rule recorded; actual learner minutes unknown |

Unqualified “all Day 4 learning complete” requires learner explain-back and actual-time ledger. No account signup is required to finish these documentation/specification tasks. Fresh-clone execution, authored public docs and a green CI run remain follow-up gates before a release/reproducibility claim.


Local checklist IDs are not issued Jira keys; setup has no assigned points. All blocks fit caps; optional reading is inside these blocks. Earlier Day 2 105-minute and Day 3 210-minute drafts were invalid. DSA is deferred; its slots remain uncommitted and are not silently repurposed.

## Day 1 — Thu Oct 1 — Baseline | operationally complete

90 minutes: learn 15, hardware/WSL 20, tools/editor/SSH 25, Docker 15, evidence/ritual 15.
📚 Learn first: [WSL][wsl] and [Docker WSL integration][docker-wsl], prerequisites; stop before optional tools.
↩ Return: retain prior baseline, record missing evidence only; no repeated installation or invented historical time.

## Day 2 — Fri Oct 2 — Accounts and Compose review | operationally complete

90 minutes: learn 15 + accounts 30 + S8-02 review 15 + uncommitted 15 + ritual 15.
📚 Learn first: [account gates](part-04-environment-setup.md#accounts-and-security) and [S8-02](part-04-environment-setup.md#s8-02--configuration-contract); stop before paid plans or stack recreation.
↩ Return: accounts/review evidenced; personal facts and explain-back remain named pending; preserve storage and record actual time when available.

## Day 3 — Sat Oct 3 — Runtime proof | operationally complete early

180 minutes: learn 30 + implement 60 + verify 30 + storage 15 + uncommitted 30 + ritual 15.
📚 Learn first: [S8-03](part-04-environment-setup.md#s8-03--runtime-authentication-and-process-proof) and [S8-04](part-04-environment-setup.md#s8-04--storage-retention); distinguish health, authentication and retention before commands.
↩ Return: S8-01–S8-05 pass; use Day 4 results below, preserve proof rather than repeating transition. No DSA/cache implementation or mastery claim.

## Day 4 — Sun Oct 4 — Retention, docs, reproducibility | deliverables complete; learner evidence pending

180 minutes: learn 20 + retention/evidence review 40 + documentation 45 + CI/doctor specifications 35 + uncommitted 30 + ritual 10. Retention rerun October 2 under the latest instruction; services stopped afterward. These are planned allocations, not learner actual minutes.
📚 Learn first: [README guidance][readme], setup; [GitHub Actions concepts][actions], jobs/steps; stop before advanced workflows.
↩ Return: learner-owned hardware/troubleshooting notes, SETUP/README, doctor/CI specifications and fresh-clone evidence; stop at cap, swap spill with equal Day 6 feature minutes. Requested Day 4 retention, sanitized documentation, outlines and specifications are delivered; no application code or workflow implementation is claimed.

## Day 5 — Mon Oct 5 — Review and go/no-go | audit delivered; closure blocked

60 minutes: review 20 + retrospective 15 + plan 15 + decision 10.
📚 Learn first: this evidence and [Sprint 1](part-18-sprint1.md), Day 6 only.
↩ Return: confirm safe evidence, limitations, actual time, one success/failure/process change, first Day 6 IDs and displaced minutes; continue only with Section 8 acceptance and named remaining setup gates.

## Day 4 results, SETUP outline and reproducibility

Executed early October 2, 2026; canonical Day 4 date remains October 4. Retention test completed 19:44:43 EDT. Assistant-prepared documentation/specifications are not learner authorship or mastery evidence.

📚 Learn first: [S8-05](part-04-environment-setup.md#s8-05--sanitized-evidence-and-learning); [README guidance][readme], About READMEs and relative links; stop before formatting (20-minute planned learning block).
↩ Return: explain why a fresh checkout needs recorded prerequisites, committed inputs/locks, private configuration instructions and repeatable checks. Done means another clean directory can follow those instructions without hidden local files. Learner explain-back remains pending.

Fresh-clone answer: a clone contains committed files, not ignored secrets, private clients or untracked setup. Reproducibility therefore requires versioned setup instructions and lockfiles, an independently supplied private environment, explicit client prerequisites, safe isolated storage and observed acceptance checks. Copying the working directory or its `.env` does not prove a fresh clone works.

### D4-VERIFY — Observed evidence

📚 Learn first: [Compose down](https://docs.docker.com/reference/cli/docker/compose/down/), default removals and volumes option; stop before image removal.
↩ Return: baseline mounts/cluster, recreate without `--volumes`, compare, verify Redis policy/PONG, then stop; planned 40 minutes. Completed; no additional transition needed.

| Check | October 2 result |
|---|---|
| Quiet configuration / recreated health | PASS; PostgreSQL and Redis healthy after down/up |
| PostgreSQL identity | PASS; `merlin_postgres_data`, `/var/lib/postgresql/data`, cluster `7691749973399031842` unchanged |
| Redis mount/policy | PASS; `merlin_redis_data` at `/data`; save empty, appendonly no, maxmemory 134217728, noeviction; PONG |
| Final state | Both containers stopped (`exited`); both named volumes still exist; no volume deletion |
| Hardware refresh | Ubuntu 26.04 LTS, x86_64, WSL kernel 6.6.87.2; Linux RAM 8,157,048,832 bytes, swap 2,147,483,648 bytes; Ubuntu filesystem 951 GiB available |

Host Windows RAM is historically 16 GB; WSL memory is its separate allocation. Linux virtual-disk free space does not prove equivalent Windows backing-disk capacity; earlier Windows C: snapshot was 38 GiB. GPU/driver details retain their previous attribution.

Troubleshooting observation: Redis CONFIG keys can change order and an empty final value can disappear if output is stripped. An initial comparison rejected identical policies. Rechecking JSON as a key/value mapping passed; no Redis setting changed. Retention already showed identical mounts/cluster. This was verification logic, not a database failure.

Resume only when needed: `docker compose up --wait --wait-timeout 120 postgres redis`. Stop safely: `docker compose stop --timeout 30 postgres redis`. No automatic startup claim is made for stopped containers.

### D4-DOC — SETUP.md and README v0 content outline

📚 Learn first: [README guidance][readme], getting started; [12-factor configuration](https://12factor.net/), Config and Dev/prod parity; stop before other factors.
↩ Return: documentation block 45 minutes includes outlines, hardware/evidence and fresh-clone checklist; keep this planning content here until the learner creates publication files. No root README or `docs/SETUP.md` is claimed written.

SETUP.md: scope/local-only status; Ubuntu shortcut and canonical path; host prerequisites and observed tool versions; account/MFA facts; Git/SSH identity; uv/Python constraint and lock install; Node/pnpm constraint and lock install; Compose pins/loopback/resources; private environment **names only**, secure local creation and Git checks; host client prerequisite (ignored rootless tools are not cloned); doctor checks; isolated fresh clone; start/stop; retention/rollback; troubleshooting; privacy; deferred tools.

README v0: Merlin learning-project purpose; planned AI/notes/tasks scope; currently built setup only; architecture placeholder; prerequisite list and five-command setup target; link to SETUP/doctor; acceptance/evals planned, not built; known blockers; license/attribution placeholder; planning link. Five commands remain a target until observed. Do not advertise application features, a green CI badge or tested deployment.

### D4-SPEC — Doctor and CI skeleton specifications

📚 Learn first: [GitHub Actions concepts][actions], workflows/jobs/steps/runners; stop before deployment (inside 35-minute specification block).
↩ Return: learner later authors doctor/workflow files; done here means defined inputs, expected outcomes and security checks, not an implemented script or green workflow.

Doctor inputs: intended OS, declared versions/locks, service endpoints and required variable names. Output per check: ID, PASS/WARN/FAIL, safe reason and first fix; never values of credentials. Any required FAIL yields nonzero overall result; deferred GPU/Ollama is WARN or explicitly not applicable, never a false PASS.

| Check/test input | Expected outcome / safe first fix |
|---|---|
| Wrong checkout/OS; missing Git identity or SSH access | FAIL; reopen Ubuntu path or follow Git/SSH setup |
| Wrong interpreter/manager; missing or inconsistent lock | FAIL; use declared uv/Python or Node/pnpm and reproduce locked install |
| Missing Docker; invalid Compose; unhealthy required service | FAIL; report context/integration/config/health gate without resolved output |
| Absent environment name; tracked `.env` | FAIL; private configuration instruction or untrack with learner review; never echo value |
| Stopped local stack | Report stopped state; FAIL only when the selected runtime check requires running services; no hidden startup |
| Auth negative test accepts wrong password | FAIL; inspect endpoint/authentication rules; preserve database volume |
| Resource/port/storage mismatch | FAIL; compare S8-02/04 contract; never destructive repair |
| Disk/RAM, time zone, permissions, branch/commit/cleanliness | Record observed values; WARN for documented local changes, FAIL for secret exposure or required prerequisite failure |
| Optional model absent before Day 8 | Not applicable; no download or GPU-use claim |

CI skeleton: proposed pull-request and manual triggers; read-only repository permissions; explicit runner/version selection; pinned full action commit digests verified when authored; no paid runner assumption. Steps: checkout, declared tools, locked dependency checks where metadata exists, documentation/whitespace/secret-boundary checks, quiet Compose validation using **synthetic CI-only** inputs. Runtime test is a separately selected job with disposable isolated project/volumes, health/positive-negative auth/PONG checks and guaranteed teardown of its own resources. No AWS/deploy step, production secret, real dump, privileged pull-request execution or learner-volume access. Logs/artifacts sanitized. No application tests invented. CI acceptance requires an actual passing run later; workflow not created by this specification.

### D4-CLONE — Original blocker and safe test (tracking gate now resolved)

📚 Learn first: [Git recording changes][git], tracked versus untracked files; stop before committing examples.
↩ Return: inside Day 4 check/documentation capacity, review/stage only intended safe files, then learner commits them; fresh-clone proof follows. Do not commit/push automatically or treat specifications as execution.

Before publication, observed `git ls-files`: `docker-compose.yml`, `.gitignore`, `pyproject.toml`, `uv.lock`, `package.json`, `pnpm-lock.yaml` are untracked. HEAD has AGENTS.md, docs and tools; a fresh clone cannot contain the current working setup. That original tracking blocker is resolved by the publication update below. Clone configuration now passes; missing doctor/workflow/public setup documentation and isolated runtime reproduction remain explicit execution gates.

Fresh-clone checklist: (1) clone a reviewed commit into a disposable directory; (2) confirm all required setup files are tracked, while `.env`/`.tools` are absent; (3) follow documented prerequisites and at most five setup commands; (4) create new synthetic private credentials locally; (5) use a distinct Compose project, container names, network and free loopback ports—current fixed Merlin identities must not collide; (6) run doctor and health/auth/PONG checks; (7) test only implemented acceptance cases, with no invented seed/eval; (8) stop/remove only that clone’s disposable resources, never `merlin_postgres_data`; (9) record commit, commands, time, first failure/fix and no-secret result. Until isolation and tracked instructions exist, stop before runtime creation.

### D4-LEARN — Answers and re-quiz

📚 Learn first: [Git recording changes][git], tracked files; [README guidance][readme], prerequisites and relative links; stop before commit examples.
↩ Return: inside the 20-minute learning block, explain these answers in your own words; assistant model answers do not count as learner mastery.

A fresh clone is reproducible when its reviewed commit contains the declared configuration/locks/instructions and a clean environment can repeat checks using separately supplied private inputs. Ignored clients and untracked files are absent, so instructions must list them explicitly. A healthy PostgreSQL process does not prove password rejection or retained cluster identity: each needs its own test. An isolated clone must not reuse the working project's fixed container names, ports or named volumes because its teardown could interfere with learner data. A named volume outlives ordinary container removal; Redis remains disposable because snapshot/AOF writes are disabled. Re-quiz on Day 5: explain these distinctions without the answer bank; then whiteboard folder/service/storage boundaries in existing ritual time. No tree exercise is required while DSA is deferred.

### D4-EOD — Ritual and remaining gates

📚 Learn first: [S8-05 evidence/learning questions](part-04-environment-setup.md#s8-05--sanitized-evidence-and-learning); stop before new tools.
↩ Return: 10-minute ritual; record actual learner minutes, learning answers and spill. Those facts cannot be supplied by the assistant.

Stand-up: retention/recreation, safe stop, sanitized hardware evidence, troubleshooting and SETUP/README/doctor/CI specifications delivered. Blocker: working setup is untracked; doctor/CI/public docs and fresh-clone execution remain unimplemented/unproven. Next: learner reviews and commits setup, authors specified files and proves isolated clone; then Day 5 review. DSA remains deferred, its 30 minutes uncommitted. Planned total 20 + 40 + 45 + 35 + 30 + 10 = 180 minutes; actual learner time unknown. Any spill displaces equal Day 6 feature time, never adds hours. Quiz: why are ignored tools absent from a clone; why is healthy storage insufficient authentication proof; why must clone resources be isolated? Day 4 operational verification and requested planning deliverables are complete. Learner learning/actual-minute evidence remains pending; fresh-clone execution is a named reproducibility follow-up, not a completed claim.


## Sprint 0 completion audit — October 2, 2026

This audit compares the current guide with the earlier revised execution plan. The earlier text is historical, not a second active schedule. No new runtime recreation is needed: the October 2 retention proof and subsequent stopped-state check still apply to unchanged Compose configuration.

📚 Learn first: [Part 04](part-04-environment-setup.md), acceptance and security; [Git clone](https://git-scm.com/docs/git-clone), description; stop before advanced clone options (inside Day 5 review).
↩ Return: review every row within the planned 20-minute review block; treat missing implementation/proof as open rather than replacing it with a document. Evidence was inspected October 2; planned time is not actual learner time.

| Earlier plan item | Current audit / remaining action |
|---|---|
| Atlassian account/email/MFA/Free/Scrum/recovery | Learner-confirmed complete; team-managed type remains unconfirmed |
| GitHub remote deferred | Historical statement superseded: remote exists in WSL; browser MFA/visibility still learner-confirmed gates |
| AWS decision | Complete decision: deferred, no signup/payment/CLI/deployment; not a missing AWS account task |
| Section 8 corrections and S8-01–05 | Operational PASS; exact pins/private inputs/auth/health/limits/Redis/logging/retention/evidence recorded in Part 04 and here |
| Day 1 installation | Baseline retained; no repeated work |
| Day 2/3 hour totals | Old 105/210-minute schedules violate caps; current totals 90/180 minutes retained |
| DSA linked lists/trees | Learner-deferred; 15/30-minute slots uncommitted; no study/cache feature claimed |
| Day 4 required retention/evidence/outlines/specifications | Delivered; stopped stack and preserved volumes verified; assistant authorship explicit |
| Actual learner time, explain-back, whiteboard/re-quiz | Pending learner evidence; estimates not invented |
| README v0 and SETUP publication | Outlines delivered, public files absent; overall environment reproducibility remains open |
| Doctor and CI | Specifications delivered; no doctor implementation, workflow or actual green CI run; overall Sprint 0 completion remains open |
| Tracked setup | RESOLVED: reviewed inputs committed in `db05acb`; clean clone contains them |
| Fresh clone | Partial PASS: clean committed clone and quiet configuration; doctor/isolated runtime not tested |
| Review and S1 go/no-go | Review delivered below; NO-GO for declaring full Sprint 0 complete; setup remediation may continue |

`.env` is ignored and not tracked; `.tools/ubuntu-clients` is ignored; whitespace check passes. This secret-boundary evidence does not prove all future staged files are safe. Full resolved Compose configuration and private backup contents were not printed.

### D5-RETRO — Draft grounded in observed work

📚 Learn first: [Git recording changes][git], inspect changes; stop before commit examples (inside the 15-minute retrospective block).
↩ Return: learner confirms or replaces these observations and supplies actual setup time; a prepared retrospective is not proof of learner participation.

Success: PostgreSQL cluster identity survived pinned-image recreation without deleting storage. Failure: order-sensitive Redis CONFIG comparison initially rejected equivalent settings; keyed comparison corrected the verification. Process change: compare semantic key/value data and separate configuration, runtime, storage and learning proof. Actual learner setup time: unknown. No numerical spill is calculated without actual minutes; confirmed spill replaces equal Day 6 feature time, never adds hours.

### D5-PLAN — Bounded next work

📚 Learn first: [Sprint 1](part-18-sprint1.md), goal; [foundation checklist](part-06-checklists-first-half.md), C-02 and C-04; stop before feature implementation (inside the 15-minute planning block).
↩ Return: close reproducibility before issuing a Day 6 implementation promise; local checklist IDs are not Jira ticket keys. Part 18 is currently a short outline, not a fully sized daily execution plan.

First candidate after setup closure: C-04.01 PostgreSQL transaction/row-security learning, then C-04.02 schema specification. Neither is started or automatically assigned to Jira. Do not promise migrations/login while setup spill is unsized. Day 6 allocation must be derived from its funded capacity and remaining setup work; preserve scratch-first/security core and swap optional work rather than add hours.

### D5-DECISION — Explicit go/no-go

📚 Learn first: [Part 1 readiness gates](part-01-waterfall-and-assumptions.md), RDY-01–04; stop before optional extensions (inside the 10-minute decision block).
↩ Return: mark GO only when the agreed setup acceptance proofs exist and personal/learning gaps have truthful dispositions. Today's decision is NO-GO for full Sprint 0 completion; Section 8 acceptance itself is PASS.

The narrow Day 4 request asked for doctor/CI **specifications only**; those are delivered. The wider Sprint 0/environment contract also asks for a green CI skeleton and fresh-clone reproducibility; those cannot be satisfied by specifications. Keep both facts visible. Do not silently downgrade the wider contract to make the sprint look complete.

### S0-CLOSE — Concrete route to full completion

📚 Learn first: [Actions concepts][actions], workflow/job/step; [Git clone](https://git-scm.com/docs/git-clone), committed repository checkout; stop before deployments.
↩ Return: use remaining setup capacity or explicitly displaced Day 6 feature minutes; follow this order and record each first failing gate. Each action is bounded to at most 45 minutes and may stop safely at its gate; estimates require recalibration from learner time.

1. **Personal/learning evidence:** confirm GitHub browser MFA and current visibility, Jira team-managed type; explain fresh-clone prerequisites/private inputs in your own words; record approximate actual minutes or explicitly unknown, whiteboard/re-quiz status. No new paid account needed.
2. **Publish documentation:** learner writes README v0 and SETUP using the delivered outlines, with exact declared install/start/stop commands, prerequisites, safe environment names and honest unbuilt list. The five-command target remains unverified until execution.
3. **Author doctor/CI:** learner implements the supplied checks and minimal workflow, without app features; actual CI run must pass with synthetic private inputs and sanitized logs. Runner/action versions/digests and account free-use availability are verified at authoring time, not invented now.
4. **Review and record setup:** privately review intended configuration, ignore rules, metadata/locks and docs; `.env`, `.tools`, dumps and recovery material remain excluded. Learner commits only reviewed files. No blanket `git add .`; no publication/visibility change assumed.
5. **Isolated clone proof:** clone that commit, follow documented prerequisites, supply new synthetic private credentials, use distinct container/network/port/storage identities, run doctor/auth/PONG checks and clean up only its resources. Current fixed Merlin identities require an explicitly reviewed isolation design before runtime execution. Original PostgreSQL volume remains untouched.
6. **Final review:** record commit/run IDs, clone command count/time/result, actual-time/spill disposition, remaining learning evidence and any limitations; repeat Day 5 decision. Only then label Sprint 0 complete and expand the Day 6 plan.

Repository policy remains planning-only for new artifacts: AGENTS.md says “Write only under `docs/planning/`” and “Never create application code, config files, scripts, SQL/DDL or CI files.” Earlier authorization covered the already completed setup changes; the current Day 4 instruction explicitly asks for CI/doctor specifications. This audit therefore delivers the remaining specifications/route without asserting that prohibited implementations or learner evidence exist. No skill adds an approval gate.

Resource index: README, Compose down, Git clone and GitHub Actions docs accessed/verified October 2, 2026; inherited references verified October 1–2 as documented in Part 04. Context7 unavailable. Account eligibility and unexecuted optional APIs remain 🔎 verify.

[wsl]: https://learn.microsoft.com/en-us/windows/wsl/install
[docker-wsl]: https://docs.docker.com/desktop/features/wsl/
[git]: https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository
[readme]: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
[actions]: https://docs.github.com/en/actions/get-started/understand-github-actions

## GitHub publication update — October 2

📚 Learn first: [Git recording changes][git], tracked setup inputs; stop before unrelated changes.
↩ Return: the learner explicitly requests committing and uploading the corrected Ubuntu version. Review exact files, exclude private configuration/tools, commit to existing `setup/E0-US01-environment` branch and verify remote commit equality. No main-branch merge or visibility change is requested.

The learner states GitHub/Jira should work; this is not a confirmation of specific security settings. Existing Atlassian facts retain their earlier learner confirmation. GitHub browser MFA/visibility and Jira team-managed type remain unknown, not reasons to create new accounts. Actual minutes/learning answers are unknown rather than fabricated. Publication closes the untracked-input gate once the reviewed setup is committed. Fresh-clone configuration validation is separate from isolated runtime/doctor/CI proof; no automatic claim of full Sprint 0 completion.

### Publication and clean-clone proof

Reviewed setup commit: `db05acb306f4ac7d03cfca65d39803c4313b671a`, branch `setup/E0-US01-environment`. This includes corrected Compose, ignored-secret boundary, Python/Node metadata and locks, separate Parts 04/17, verified original-doc archive and installed Caveman skill assets. Existing third-party skill assets were recorded, not authored as Merlin feature code.

A clean local Git clone of this commit contained all selected setup/planning files; `.env` and `.tools` were absent. `docker compose config --quiet` passed with separately supplied synthetic environment values. Whitespace check passed. No clone runtime was created, no learner volume touched, and no app/doctor/CI success inferred. This resolves the earlier untracked-input/configuration gate, not the full runtime reproducibility gate. Account settings and actual learner time/mastery remain unknown; user expectation of access is recorded without demanding another signup.

The upload target is the existing GitHub setup branch. The final remote verification is performed after the evidence commit; no main merge or default-branch change is implied. Follow-up completion scope is now public documentation, implemented doctor/CI with a real passing run, isolated clone runtime and learning/time disposition. Day 4 requested specifications are complete; wider Sprint 0 remains honestly open.

## Runtime clone and quick quiz update — October 2

📚 Learn first: [Part 04](part-04-environment-setup.md), authentication/storage; [OmniRoute source skills](https://github.com/diegosouzapw/OmniRoute/tree/23a11484862b3bb589a55e85b00e4ac53ffeb234/skills), catalog only; stop before gateway configuration or provider signup.
↩ Return: use this observed proof and answer the five questions within existing learning/ritual time; no new feature or paid service. The assistant grades understanding rather than asserting it beforehand.

Installed 46 upstream skills at source commit `23a11484862b3bb589a55e85b00e4ac53ffeb234`, repository `diegosouzapw/OmniRoute`, release/v3.8.52. All installed entries contain SKILL.md name/description metadata; provenance/hash recorded in skills-lock.json. Skill instructions are available next turn; no OmniRoute server, provider credentials, routing changes or measured token savings claimed. Installation was explicitly requested and is distinct from the deferred application tools.

A clean clone of the committed setup was started as a unique disposable Compose project with synthetic credentials. Verification adaptation removed fixed container names and host ports and assigned unique network/volume names in memory; no permanent Compose change. Both services became healthy; PostgreSQL correct-password access passed and deliberately wrong password was rejected; Redis returned PONG. Test project resources/volumes were removed; original `merlin_postgres_data` and `merlin_redis_data` were confirmed present. This proves isolated container runtime behavior; it does not prove host-port access in that clone, a published five-command README, doctor implementation or green hosted CI. Those wider gates remain visible.

Quick quiz (one sentence each):
1. Why must `.env` stay out of GitHub?
2. Can a healthy PostgreSQL container still accept a wrong password, and why must we test that?
3. What remains unchanged after PostgreSQL recreation to prove storage retention?
4. Why can local setup work while a fresh clone fails?
5. Does GitHub SSH login also protect Jira browser login?

Grading: each question gets 0 incorrect/missing, 1 partially correct, 2 correct with the essential reason; total 10. Explain each correction and retest missed concepts. A short-quiz pass requires at least 8/10 and no remaining misconception about secret publication, password rejection or storage deletion. Quiz result remains pending. A quiz alone is not full mastery: retain whiteboard/acceptance/re-quiz evidence and unknown actual minutes honestly. No DSA questions while deferred.

Current closure: local Section 8 operational proof, requested Day 4 planning deliverables, GitHub publication, configuration clone and adapted isolated runtime pass. Wider Sprint 0 still lacks implemented doctor/CI, public README/SETUP reproducibility and learner evidence. Existing AGENTS.md explicitly forbids agent-created scripts/CI; no script/workflow was written under the specification-only Day 4 scope. Do not mark full Sprint 0 complete solely because skills or quiz were added.

## Beginner lesson — PostgreSQL and Sprint 0 foundations

Quiz feedback: Q1 (.env private information) 2/2; Q5 (GitHub SSH does not protect Jira browser login) 2/2. Q2–Q4 are pending teaching/retry, not answered incorrectly. Score so far: 4/4 on answered questions; no full-quiz pass or mastery claim.

### What PostgreSQL does

📚 Learn first: [PostgreSQL concepts](https://www.postgresql.org/docs/17/tutorial-concepts.html), tables/databases; [architecture](https://www.postgresql.org/docs/17/tutorial-arch.html), client/server; stop before installation (inside existing learning time).
↩ Return: explain server versus client and describe one planned note record; done when the learner can identify where data lives without claiming the application exists. No SQL or feature code required.

PostgreSQL, often called Postgres, is software that manages stored information. Merlin is planned to use it for records such as users, notes and tasks. Those application features/tables are not built merely because the database service is installed. PostgreSQL organizes records in tables. A table is like a structured spreadsheet: a column describes a field, and a row describes one record. Columns have data types so a date, number and text value are distinguished.

Example of a future notes table, for explanation only:

| id | owner_id | title |
|---|---|---|
| 101 | 7 | Study PostgreSQL |
| 102 | 7 | Prepare interview |

An ID identifies a record. A primary key is a table's chosen unique identifier. An owner_id can refer to a user's identifier; a foreign-key rule can ensure the referenced user exists. That relationship does not automatically prevent another person reading the note: the application must enforce ownership/authorization. Constraints enforce rules such as required fields or uniqueness. Indexes can speed lookups but cost space and work when records change. Design/query/security details belong to later sprints, not Sprint 0 mastery.

A database groups tables and other objects. A PostgreSQL cluster here means the databases managed by one initialized server instance; it does not mean multiple cloud machines. Your current cluster includes merlin_db plus PostgreSQL's maintenance/template databases. The PostgreSQL server is the running program that handles requests and manages its data files. `psql` is a client program used to communicate with it; installing a client does not itself create a server.

### How a future save request works

📚 Learn first: [PostgreSQL architecture](https://www.postgresql.org/docs/17/tutorial-arch.html), cooperating processes; [transactions](https://www.postgresql.org/docs/17/tutorial-transactions.html), all-or-nothing; stop before savepoint examples.
↩ Return: narrate a future save/read request and why related changes may need one transaction; conceptual preview only, inside existing learning capacity.

When the future user clicks Save, the browser sends a request to Merlin's backend. The backend checks the signed-in user's identity and ownership, then uses a database client library to connect to PostgreSQL. The connection identifies an address, port, database and role; the role is the database identity, separate from a Merlin browser user. The backend asks for an operation in SQL, the language for requesting reads/changes. PostgreSQL checks database permissions, executes the operation, and returns a result. The backend then responds to the browser. A browser should not receive the database password to connect directly.

A transaction groups related changes into an operation that can succeed together or be canceled together. Commit finalizes the transaction; rollback cancels its changes. This matters when a partial change would leave inconsistent records. Transactions and their safeguards do not replace backups or correct application permissions. Later study will cover concurrency, isolation, indexes, migrations and backup restoration; trying to master every database topic during setup would exceed Sprint 0's hours.

### Your Docker setup and data

📚 Learn first: [Docker volumes](https://docs.docker.com/engine/storage/volumes/), persistence; [official Postgres image](https://hub.docker.com/_/postgres), initialization variables; stop before custom image examples.
↩ Return: identify image/container/volume in the actual setup; explain what survives recreation and why editing .env is not password rotation. Do not run destructive commands for this lesson.

The image is the packaged PostgreSQL software at a pinned version/digest. A container is an instance running that software. Compose is the description Docker uses to start the services with their settings. Your container is merlin-db; the Compose service is postgres. Its data directory is mounted from the named volume merlin_postgres_data. A mount makes that separately managed storage accessible inside the container. Recreating the container can reuse the volume, keeping the cluster instead of initializing an empty replacement.

We checked two storage identifiers: the named volume and PostgreSQL's cluster ID, 7691749973399031842. Both remained unchanged after recreation. That proves the existing setup cluster was reused; it is not proof of a production backup restore or every application's future data correctness. Containers may get new IDs while retained storage stays the same. Stopping services preserves volumes. Deleting a volume can remove data, so never delete it to repair login problems.

The private .env provides setup inputs. The official image uses initialization variables when creating an empty data directory. An existing cluster already has stored roles/passwords; changing POSTGRES_PASSWORD in .env alone does not update those stored credentials. A password change requires a deliberate database operation with appropriate privileges. Keep real credentials out of history/logs/screenshots/Git, even in a private repository.

### Health, authentication and addresses

📚 Learn first: [pg_isready](https://www.postgresql.org/docs/17/app-pg-isready.html), status and notes; [authentication rules](https://www.postgresql.org/docs/17/auth-pg-hba-conf.html), matching records; stop before advanced methods.
↩ Return: explain the three independent tests: ready, correct-password success/wrong-password rejection, and unchanged storage identity. Done when those are not treated as interchangeable.

A health check asks whether the server is accepting connections. It does not certify passwords, ownership rules or retained data. Depending on its authentication configuration, a local connection may be trusted without checking a password. That is why an appropriate password-protected endpoint must succeed with the correct password and reject a deliberately wrong one. Your recorded host/container password checks passed; PostgreSQL's own database roles are separate from Linux process ownership and browser-account MFA.

A host address identifies where to connect; a port identifies a service endpoint there. Your Ubuntu host client uses 127.0.0.1:5432. A different container on the Compose network can use postgres:5432. Inside a container, localhost means that container itself, not automatically the Ubuntu host or another service. Loopback bindings restrict ordinary remote access; they do not protect against every local process. Non-root service processes and RAM/CPU limits constrain privileges/resources but are not a complete security guarantee.

### Why a fresh clone can fail

📚 Learn first: [Git clone](https://git-scm.com/docs/git-clone), repository checkout; [README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes), getting started; stop before advanced options.
↩ Return: name three things present locally but absent from a clone, then explain the safe documented replacement for each. No copying private secrets or preserved learner volumes into a test clone.

A commit is a recorded snapshot of selected project files; a push uploads commits to the GitHub branch; a clone obtains repository history and checks out a recorded version. It does not copy your entire computer. Locally you may have installed Python/Docker/psql, an ignored .env, ignored .tools clients, uncommitted changes or an already initialized database. Another clone lacks those machine-specific dependencies, secrets and database state. Even on your machine, a clean clone does not acquire ignored files or uncommitted changes from the original folder.

Example: your current directory starts successfully because .env already exists. A clone has Compose but no password input, so configuration fails. The fix is instructions to create a new private environment with the required names, not committing the real password. Likewise, a clone cannot run a missing psql executable; prerequisites must describe how to obtain a supported client. An image pin records exact container software; a lockfile records dependency resolution, but neither installs dependencies by merely existing. README/SETUP instructions, declared versions/locks and observed clean-environment checks make these hidden prerequisites explicit.

Our committed clone passed configuration. An isolated runtime also passed after temporary verification adjustments for names/network/volumes and host ports. That is useful proof, but it is not yet proof that a new user can follow a published five-command setup without adjustments. A new clone must not collide with or delete your original containers/volumes.

### What you should know after Sprint 0

📚 Learn first: [Part 04](part-04-environment-setup.md), actual setup boundaries; this lesson's official links; stop before optional frameworks.
↩ Return: explain each row in plain language; quiz/whiteboard/re-quiz happen inside learning/ritual capacity. DSA stays deferred. Understanding and implementation completion are distinct gates.

| Topic | Minimum understanding |
|---|---|
| Windows and Ubuntu/WSL | Windows hosts the machine; development runs in Ubuntu; Windows shortcut/views open the same Ubuntu checkout |
| Git/GitHub | Git records versions locally; GitHub hosts pushed history; branch/commit identifies the uploaded version |
| SSH/MFA/Jira | SSH key authenticates Git transport; browser MFA adds another factor for that account; Jira tracks work, it does not secure your database |
| Python/uv and Node/pnpm | Runtimes execute programs; managers create/install project environments; declared versions/locks support repeatability |
| Docker/Compose | Image packages software; container runs it; Compose defines services/settings; volume retains data separately |
| PostgreSQL/psql | Server manages durable records; psql is one client; health, credential checking and retention need separate proof |
| Redis | Separate fast data service; PONG tests responsiveness; this project's Redis is disposable with persistence disabled, not a built cache feature |
| Secrets/ports/limits/logging | Keep credentials private; bind local ports; bound CPU/RAM and logs; never claim those alone are production security |
| Doctor/CI/fresh clone | Doctor reports prerequisites/checks; CI automates checks on recorded code; a fresh clone tests whether instructions omit hidden local setup |
| Evidence and scope | Observed test results support specific claims; setup passing does not mean features or learner mastery are complete |

Resource index: PostgreSQL concepts/architecture/transactions/pg_isready/authentication, official Postgres image, Docker volumes and Git clone opened successfully October 2, 2026. Explanation is grounded in those sources and attributed project evidence; no new installation/runtime test this lesson.

Re-quiz after reading: (1) What is the difference between PostgreSQL and psql? (2) Why does healthy not prove wrong passwords are rejected? (3) What must survive container recreation? (4) Give two reasons a fresh clone could fail and a safe fix for each. Answer in your own words; no need to memorize every term at once.

## Interactive Sprint 0 quiz — October 3

📚 Learn first: [beginner lesson above](#beginner-lesson--postgresql-and-sprint-0-foundations), review only the concepts you need; stop before answer memorization.
↩ Return: open [Sprint 0 MCQ quiz](../../Docs/Quizzes/sprint-0-quiz.html), answer all 35 questions, submit for corrections, retry missed concepts and explain corrections in your own words. Use existing learning/ritual capacity, not extra invisible hours.

The learner explicitly requested an HTML learning artifact in Docs/Quizzes; this scoped exception permits that file outside the planning directory and does not authorize application features. The quiz covers all ten October 3 explain-back topics plus service/storage/security/reproducibility/resource/account/planning/skill boundaries. The learner's original ten answers were assessed; detailed feedback is embedded in the post-submission review rather than disclosed in chat. No full understanding pass is claimed before the learner completes and explains the quiz.

Both Ubuntu and C:\Users\vipra\Merlin\docs\planning\part-17-sprint0.md were read. Windows is an inactive older 768-word draft; Ubuntu has later evidence/corrections. Historical differences are explained in the quiz; old Windows files were not changed or synchronized. Windows may open the active quiz through \\wsl$\Ubuntu\home\vipra\Merlin\Docs\Quizzes\sprint-0-quiz.html.

One self-contained HTML file, with no external libraries, fonts, network requests or services. Choices shuffle, explanations remain hidden before submission, browser-local progress is optional with graceful fallback, missed-question retries are labeled practice, and print/PDF uses the browser. Scoring threshold is 80% without missed critical secret/authentication/storage questions; that is a knowledge check, not full Sprint 0 completion. Browser-local results are not automatically visible to the assistant: share the result or follow-up explain-back to record learning evidence.

Verification: JavaScript syntax passes. A Node DOM harness checks question-bank uniqueness, score/critical gates, shuffle permutations, invalid-answer handling, unanswered submission, hidden prior feedback, rendering/scoring, saved-result restoration, missed retries and full reset. No real-browser visual test was available, so no screenshot/cross-browser proof is claimed. Source documents and their existing official resources ground the questions; this task did not perform a new runtime audit or change database services.
