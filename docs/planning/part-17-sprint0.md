# Part 17 — Sprint 0 execution and evidence

## Setup closure — October 6, 2026

**Sprint 0 operational setup: PASS. Sprint 1 foundation: GO. Learner practical mastery: still in progress.** The app itself is not built. The earlier dated audits below remain history; their absent-document/doctor/CI/clone blockers are superseded by this observed closure.

📚 Learn first: [visual Sprint 0 learning guide](SPRINT0_LEARNING.md), overview and Sections 7–9; [SETUP](../SETUP.md), prerequisites and the five project commands; stop before optional tools.
↩ Return: use [the command reference](TERMINAL_COMMANDS.md), answer the five explain-back questions, and proceed to [bounded Day 6](part-18-sprint1.md#day-6--tuesday-october-6--first-database-foundation). Keep learner facts separate from software evidence; no app feature or authorship is inferred.

| Closure gate | Observed result |
|---|---|
| README/SETUP | Published setup purpose, declared prerequisites, private configuration, exact five-command project path, troubleshooting and safe lifecycle guidance |
| Doctor implementation | Read-only static/runtime checker; safe failure reasons and nonzero required-failure exit; native host and in-container PostgreSQL positive/negative authentication; Redis PONG/policy; ports/resources/logs/UID/mounts/cluster checks |
| Doctor regression tests | Eight stdlib tests PASS locally and in hosted CI, including secrecy, timeout classification, explicit password rejection and isolated clone acceptance |
| Locked installation | `uv sync --locked` and pnpm frozen installation PASS; pnpm lock corrected through its manager; no application dependencies added |
| Hosted CI | **PASS**, commit `3b7d3ed46d97bfeeb0711c55dc14926a18ea0d30`, [run 37534267500](https://github.com/vipravlipare/Merlin/actions/runs/37534267500); all setup/install/lock/test/static/runtime/cleanup steps successful |
| Unmodified public clone | **PASS**, same commit, cloned from GitHub to `/tmp/merlin-s0-proof-final-20261006`; documented five-command sequence with only destination changed; no source/Compose overrides, original credentials or hidden `.tools` copied; `git diff --exit-code` PASS |
| Independent clone storage | Project `merlin-1049b72834`, its own project-scoped volumes/network/loopback ports; cluster `7693673063843803175`, distinct from original. Full doctor PASS; synthetic resources removed after proof |
| Retention transition | Earlier unchanged public clone `288cc2b531ffc5032315cb1cc92756f601e544e9`, project `merlin-04782689fc`, retained cluster `7693668956165697574` through ordinary down/up; doctor with expected cluster PASS; only its synthetic resources removed afterward |
| Original storage/security | Original `merlin_postgres_data` and cluster `7691749973399031842` preserved; host/container correct passwords accepted and wrong passwords explicitly rejected. Original services remain running for learner work |
| Section 8 / hardware / evidence | Existing dated S8-01–S8-05 and hardware evidence retained; secrets and resolved Compose output excluded. No backup restore, production transport or app-owner authorization claim |
| Personal accounts / time | Learner confirms setup minutes **unknown**, GitHub configured and Jira MER **team-managed Scrum**. Earlier Jira email/MFA/sign-in/Free-plan/private recovery confirmations retained. GitHub repository observed public; browser GitHub MFA not explicitly confirmed |
| Learning | Prior quiz34/35 learner-reported. October6 answers correctly identify secret exclusion and health/auth distinction; committed-input rationale and retention explain-back are partial; CI was unfamiliar and is now taught. Whiteboard and spaced re-quiz remain pending |
| Deferrals / scope | DSA learner-deferred; AWS/payment/CLI/deployment deferred; no application features or optional model/framework installers claimed. Gateway routing is optional and not proved by installed skills |

### Commands actually reproduced

Host prerequisites were installed/documented separately. The helper generates private mode0600 inputs, checkout-specific identities and free loopback ports. Command five checks the generated setup. These commands operated on the published passing revision, with no setup-source changes:

```bash
git clone --branch setup/E0-US01-environment https://github.com/vipravlipare/Merlin.git /tmp/merlin-s0-proof-final-20261006
cd /tmp/merlin-s0-proof-final-20261006
uv sync --locked
uv run --locked python tools/setup_local.py
uv run --locked python tools/doctor.py
```

The initial version also passed unchanged locally, but hosted CI exposed an invalid job-level context expression and pnpm's shebangless placeholder when its native installer was disabled. The former was removed; the pinned manager's installer now runs outside the checkout, while project dependency lifecycle scripts stay disabled. Strict doctor version/authentication checks were preserved. This is an integration failure/fix, not a database failure. Sanitized doctor errors become public CI annotations; raw credentials stay private.

Compose now generates container names and supports checkout-specific project/network/host ports. Defaults retain project `merlin`, network `merlin-network`, original host ports and volume identity. This removes earlier fixed-name collisions without changing original data. Native clients are documented host prerequisites, independently installed outside the repository; a clone does not carry them.

### Day 5 review, retrospective and next action

Assistant-prepared review: Section8, public instructions, doctor, passing hosted CI and unchanged clone checks pass. Application tests are N/A, not fake successes. Optional tools remain deferred. Operational decision is GO for Day6 learning/design and conditional learner implementation after first-use dependency/isolation checks.

Assistant-prepared retrospective observations: success — a published clone and independent runner reproduce setup; failure — local-only checks missed workflow context and package-manager installer assumptions; process change — trust observed CI and clean-clone evidence rather than installation inventory. These are offered observations, not invented learner-authored reflections.

Actual learner setup minutes: **unknown**, explicitly reported. Historical time caps and planned allocations remain unchanged; unknown time cannot justify reclaiming reserved or DSA minutes. Any future measured setup spill replaces equal Day6 feature time. No new hours are invented. Next learner action: read the visual guide's CI section, complete the five explain-backs and draw host/container/storage boundaries, then C-04.01/.02. Record practical review and re-quiz when actually performed. Full learning/account-certification claims remain qualified; operational setup no longer waits for missing scripts or CI.

## Earlier readiness decision — October 6, 2026 (superseded by closure update)

**Section 8 infrastructure: PASS. Start bounded Day 6 database learning/design: GO. Full Sprint 0 completion and release/reproducibility claims: still OPEN.** See [today's runtime audit](part-04-environment-setup.md#current-coding-readiness-audit--october-6-2026) and [the executable Day 6 plan](part-18-sprint1.md#day-6--tuesday-october-6--first-database-foundation).

📚 Learn first: [uv locking/syncing](https://docs.astral.sh/uv/concepts/projects/sync/), locked execution; stop before dependency updates.
↩ Return: preserve the verified services and finish one bounded learner-owned outcome; learning/design can begin while doctor/CI/public documentation remain open. Merge/release gates still require their actual evidence. Account-specific personal facts, actual learner minutes and explain-back remain honestly attributed, not inferred.

PostgreSQL/Redis are **running and healthy now**, with host/container positive and negative authentication, retained cluster, loopback, resources, logs and non-root ownership verified. The earlier October 2 sections below are historical evidence; their stopped-state and untracked-file blockers do not describe today's checkout. Setup files were subsequently committed, and an isolated adapted clone passed runtime checks. Public unmodified reproduction, doctor/CI implementation and a real passing CI run remain outstanding. A learner-reported 34/35 quiz score is useful evidence, not proof of every practical learning gate.

Day 6 retains a six-hour cap: setup spill displaces feature work minute-for-minute; CI's requested latest deadline is Day 7. DSA remains deferred and its slot uncommitted. This decision permits starting the foundation, not marking C-04, Sprint 0, or a runnable backend Done.


Canonical calendar: Days 1–5, October 1–5, 2026; no separate Day 0. Environment/service requirements and reproduction commands live in [Part 04](part-04-environment-setup.md). Original ten documents remain recoverable in [the verified archive](archive/setup-sprint0-originals-2026-10-02.tar.gz). Original Day 4 delivery was planning-only. The later explicit request authorized the published setup implementation; application feature code remains learner-owned.

## Historical Day 4 closure checklist

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

## Day 5 — Mon Oct 5 — Review and go/no-go | operational review complete; learner ritual pending

60 minutes: review 20 + retrospective 15 + plan 15 + decision 10.
📚 Learn first: this evidence and [Sprint 1](part-18-sprint1.md), Day 6 only.
↩ Return: confirm safe evidence, limitations, actual time, one success/failure/process change, first Day 6 IDs and displaced minutes; continue only with Section 8 acceptance and named remaining setup gates.

## Historical Day 4 results, SETUP outline and reproducibility

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
↩ Return: open [Sprint 0 MCQ quiz](../../Quizzes/sprint-0-quiz.html), answer all 35 questions, submit for corrections, retry missed concepts and explain corrections in your own words. Use existing learning/ritual capacity, not extra invisible hours.

The learner explicitly requested an HTML learning artifact in Quizzes; this scoped exception permits that file outside the planning directory and does not authorize application features. The quiz covers all ten October 3 explain-back topics plus service/storage/security/reproducibility/resource/account/planning/skill boundaries. The learner's original ten answers were assessed; detailed feedback is embedded in the post-submission review rather than disclosed in chat. No full understanding pass is claimed before the learner completes and explains the quiz.

Both Ubuntu and C:\Users\vipra\Merlin\docs\planning\part-17-sprint0.md were read. Windows is an inactive older 768-word draft; Ubuntu has later evidence/corrections. Historical differences are explained in the quiz; old Windows files were not changed or synchronized. Windows may open the active quiz through \\wsl$\Ubuntu\home\vipra\Merlin\Quizzes\sprint-0-quiz.html.

One self-contained HTML file, with no external libraries, fonts, network requests or services. Choices shuffle, explanations remain hidden before submission, browser-local progress is optional with graceful fallback, missed-question retries are labeled practice, and print/PDF uses the browser. Scoring threshold is 80% without missed critical secret/authentication/storage questions; that is a knowledge check, not full Sprint 0 completion. Browser-local results are not automatically visible to the assistant: share the result or follow-up explain-back to record learning evidence.

Verification: JavaScript syntax passes. A Node DOM harness checks question-bank uniqueness, score/critical gates, shuffle permutations, invalid-answer handling, unanswered submission, hidden prior feedback, rendering/scoring, saved-result restoration, missed retries and full reset. No real-browser visual test was available, so no screenshot/cross-browser proof is claimed. Source documents and their existing official resources ground the questions; this task did not perform a new runtime audit or change database services.

## System Design reading update — October 3

📚 Learn first: [System Design reading section](../../Quizzes/sprint-0-quiz.html#system-design), setup rationale and examples; stop before optional product installation.
↩ Return: read the five expanded topics and explain a decision plus its trade-off in your own words, inside existing learning/ritual time. This section contains no additional questions.

Learner reports finishing the MCQ quiz with 34/35. Record as learner-reported: missed question/critical-gate result and explain-back are unknown; no complete Sprint 0/mastery claim. The HTML now has a separate System Design reading section and direct navigation. It covers all earlier interview rationales and expands Ubuntu/WSL versus native Windows, relational/document/key–value/graph/wide-column models, file/object/block storage, caching/Redis versus PostgreSQL, named volumes and loopback mappings. Alternatives are illustrative, not installed/funded components.

Existing 35-question bank, quiz JavaScript, storage key and saved-result behavior are byte-for-byte unchanged. Syntax/scoring/DOM-harness checks pass. Official Microsoft/PostgreSQL/Redis/Docker/MongoDB/Neo4j/Cassandra/AWS source pages checked October 3; citations are inside the reading section. No new live-service or real-browser visual claim. Reload the same browser URL and choose System Design; changing browser/origin may use a different local progress store.

## Global Caveman / OmniRoute setup — October 6

Latest explicit learner request authorizes global agent tooling outside Merlin. This is separate from Merlin application implementation and does not close missing CI/doctor/reproduction gates. Actual learner setup minutes remain unknown; any time charged to the project displaces feature time within the existing cap.

📚 Learn first: [global skill discovery](https://learn.chatgpt.com/docs/build-skills), user scope; [global agent instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md), precedence; [ChatGPT personalization](https://learn.chatgpt.com/docs/personalize), custom instructions; stop before unrelated plugins. Official pages retrieved October 6, 2026.
↩ Return: open a new Codex session outside Merlin and confirm Caveman instructions plus `$caveman` and the matching OmniRoute skill appear. Installed skills are instructions; provider sign-in and a successful request are separate routing gates.

| Item | Observed state |
|---|---|
| Ubuntu global skills | Caveman plus 46 OmniRoute repository skills installed in `/home/vipra/.agents/skills`. OmniRoute skills pinned to upstream commit `23a11484862b3bb589a55e85b00e4ac53ffeb234`. |
| Windows global skills | Same 47 skill bundles copied to `C:\Users\vipra\.agents\skills`; each SKILL.md byte-compared with Ubuntu. These are independent global installations, not a second active Merlin checkout. |
| Default chat style | Global `.codex/AGENTS.md` written in both user homes. Caveman applies by default; technical/security substance stays; files and beginner explanations remain normal English. The new global instructions subsequently loaded in this session. Project-specific instructions can override defaults. |
| Gateway binary | OmniRoute 3.8.51 globally installed in Ubuntu; registry metadata identifies the requested upstream repository. The older requested-source release 3.8.52 was not published on npm, so it was not falsely reported installed. Node 24.21.0 is supported. |
| Service / binding | Ubuntu user service `omniroute.service` enabled and active; health endpoint returns HTTP 200; listener is only `127.0.0.1:20128`. Persistent server-host setting saved; private gateway environment mode 0600. Starts with the Ubuntu user session; Windows shutdown/WSL shutdown stops it. No always-running cloud service claim. |
| Compression | REST setting saved and verified as `stacked` (RTK + Caveman), including after service restart. CLI compression calls encountered disabled MCP and did not apply settings; supported REST endpoint was used instead. No upstream code patch or MCP exposure was required. |
| Provider / inference | **Zero configured provider connections.** No routed model response or measured savings proved. Existing working Codex model connection remains in place rather than switching to an empty gateway. |
| ChatGPT plugin scope | Catalog searches for Caveman and OmniRoute returned no matching plugins. Local filesystem installs do not prove account-wide ChatGPT/web/mobile installation. Skills and inference-provider routing are separate capabilities. |

### Learner steps required to finish activation

📚 Learn first: [OmniRoute upstream](https://github.com/diegosouzapw/OmniRoute), provider connection and Codex integration; [Codex custom providers](https://learn.chatgpt.com/docs/config-file/config-advanced), provider endpoint; stop before replacing the working default. Upstream repository and current installed CLI options were inspected October 6.
↩ Return: complete provider authentication privately, then report only successful connection status and chosen model name. The assistant can finish client routing and test one synthetic response afterward. Do not paste passwords, tokens, cookies or API keys into chat.

1. Open `http://localhost:20128` in the Windows browser while Ubuntu is running. Complete any initial dashboard password prompt and keep that password private.
2. Open **Providers**, choose **OpenAI Codex** (provider ID `codex`, OAuth), and use its Connect/sign-in action. Complete the browser authorization yourself; this is not the separate cloud-agent or web-cookie provider. If only paid API signup is offered, stop and record that gate rather than accepting billing terms.
3. Verify the connection reports connected, and note the model offered. No additional paid provider is required by this request. Dashboard sign-in does not itself prove a proxied model response; that will be tested next.
4. In ChatGPT open **Settings → Personalization → Custom instructions**. Add: “Use Caveman-style concise replies by default: answer first, remove filler, preserve accuracy and security details. Explain fully when I ask. Use normal English in files.” These account settings cannot be edited by the available tools here.
5. Open a new Codex session or refresh its skills. Global skills should be available on the next turn; standalone filesystem availability on supported local clients is distinct from account-wide plugin availability. ChatGPT-wide OmniRoute routing remains unestablished; only a client explicitly configured for the gateway can be claimed routed.

The user service can be stopped with `systemctl --user stop omniroute.service`, resumed with `systemctl --user start omniroute.service`, or disabled at startup with `systemctl --user disable --now omniroute.service`. No original Codex provider configuration was replaced. Gateway credentials stay under the private Ubuntu user profile, never inside Merlin or Git.

### Live gateway verification — October 6 follow-up

📚 Learn first: [OmniRoute inference skill](/home/vipra/.agents/skills/omni-inference/SKILL.md), chat versus Responses endpoints; [authentication skill](/home/vipra/.agents/skills/omni-auth/SKILL.md), management versus inference credentials; stop before adding providers.
↩ Return: use the results below to select the next failed gate. A valid provider credential or a listed model is not a passing model/tool-call test. No permanent client routing was changed.

| Observed test | Result |
|---|---|
| Local gateway health | HTTP 200 using built-in loopback CLI authentication. Unauthenticated access now returns 401. |
| Connections | Nine listed: two Amazon Q, Kimi Coding, OpenAI, UncloseAI, OpenCode Free, Cloudflare Playground, DuckDuckGo, AI Horde. This is inventory, not nine passing providers. |
| Gateway keys / URLs | No persistent gateway API key existed. Temporary test keys authenticated both `/v1/models` and `/api/v1/models`; each returned HTTP 200 and 536 catalog entries. Both prefixes work in this installed release; the earlier strict rejection of `/api/v1` was incorrect. Catalog entries do not prove available models. |
| OpenAI | Credential-validation endpoint returned valid=true. No paid OpenAI model response was requested; billing/quota/inference remain unproved. |
| OpenCode | Connection test unsupported. Actual free-model request returned HTTP 403: free tier can only be used within OpenCode. Do not treat it as a verified external Codex fallback. |
| Cloudflare Playground | Actual small-model request returned HTTP 502 because the browser executable is absent. No browser/model installation was performed. |
| DuckDuckGo chat | `ddgw/gpt-5.4-mini`, synthetic “Reply with exactly OK”, HTTP 200, reply OK, approximately 1.842 seconds. One smoke result, not a latency benchmark. |
| DuckDuckGo Responses | HTTP 200, SSE stream completed with 16 events, but a forced harmless `smoke_echo` function produced **zero function calls**. Streaming passes; tool compatibility fails this test. No tool was executed. |
| Compression | Tested responses report `off; source=off`. Stored stacked setting alone does not prove compression applied or tokens saved. Global Caveman chat preference remains separate. |
| Cleanup / limits | Every newly created temporary gateway key removed successfully. No permanent key created, credentials displayed, Codex default changed or private project data sent. Other listed providers remain untested. |

Next gate: create a persistent gateway key privately through Dashboard Endpoints/API Manager for an actual configured client; select a provider/model that passes tool-call tests before switching Codex. Keep the current working Codex connection until then. Do not use the upstream OpenAI provider secret as the gateway client key. No full-provider or all-clients success claim is justified by this audit.

### Earlier Sprint 1 entry / new-session handoff — October 6 (superseded)

📚 Learn first: [Day 6](part-18-sprint1.md#day-6--tuesday-october-6--first-database-foundation), scope and budgets; [global instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md), project precedence; stop before changing providers.
↩ Return: start C-04.01/.02 now in Ubuntu; conditional implementation follows the stated dependency/isolation gates. Carry remaining setup as visible spill within the same daily cap, not an unqualified Sprint 0 completion claim.

Current recheck: Python 3.12.14, quiet Compose configuration and ignored/untracked `.env` pass; PostgreSQL/Redis remain healthy and loopback-bound. Existing positive/negative authentication and retained-cluster proof are reused. Day 1 operational baseline, Days 2–3 account/runtime evidence and Day 4 requested verification/specifications remain delivered. Day 5 review/go-no-go is documented; actual learner ritual/security/learning facts remain pending. Public README/SETUP, implemented doctor/CI, actual passing CI and documented unmodified clone reproduction still prevent formal full Sprint 0 closure. Current audit/planning edits are uncommitted, so the latest handoff is not claimed uploaded.

New Ubuntu terminal session:

```bash
codex -C /home/vipra/Merlin
```

Resume the latest session instead: `codex resume --last`. In the desktop app, start a new Codex chat and choose Merlin's Ubuntu project folder. Global Caveman instructions and skill bundles are present in both Ubuntu and Windows user profiles; local project overrides/custom Codex homes can affect discovery. Check `/skills` or `$caveman` in the CLI rather than assuming every cloud device shares these local files.

Both inspected user configurations still use the default model provider. OmniRoute skills are available, but **neither terminal nor desktop Codex has been switched to gateway inference**. A new session does not fix missing gateway credentials or failed tool-call compatibility. Keep working Codex authentication; gateway integration is optional to starting Sprint 1 and remains a separate unproved setup gate. ChatGPT account custom instructions and web/mobile plugin availability remain distinct from these filesystem settings.
