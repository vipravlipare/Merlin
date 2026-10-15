# Cumulative CI gate before starting a new learning day

Decision: the learner requires CI to verify all completed work from earlier days before starting a new day's implementation. Day numbers refer to the learning sequence, not today's calendar date. This is a required readiness gate, not an optional improvement.

📚 Learn first: [GitHub workflow triggers](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow), read events and filters; [workflow run history](https://docs.github.com/en/actions/how-tos/monitor-workflows/view-workflow-run-history), read how to inspect a run and its jobs. Links opened October 14, 2026.
↩ Return: identify which checks the workflow invokes, compare that list with completed work, and record a passing run for the exact committed version before advancing. Workflow text and local execution alone do not prove a GitHub run passed.

## The rule in practice

| Starting point | Required cumulative automated coverage |
|---|---|
| Start Day 6 | Completed Days 1–5 setup checks, environment/lock validation, applicable regression checks, safe service startup and cleanup. |
| Start Day 7 | All prior setup checks plus the completed Day 6 database/input-rule cases, current fault audits, runner safety checks, migration verification and preservation/cleanup checks. |
| Start Day 8 and later | Everything retained from previous days plus checks for the newly completed day. Add checks during implementation rather than waiting until the following day to discover missing CI integration. |

CI runs on configured push/pull-request events; it does not understand the learning calendar automatically. The day-start check is our workflow decision: inspect the right run and confirm its coverage before proceeding. Automated tests do not certify personal account settings, learner understanding or requirements that have no implemented boundary. Keep those observations separate.

## Day 7 step 3.1 decision

**CI repair is the blocking priority. Carry the health API implementation forward until cumulative CI is verified.** The design in section 2 remains available; it does not count as an implemented API.

Use the existing 15-minute decision block to record this gap. Reassign the remaining 50 minutes of section 3 to the CI repair attempt. This is a time allocation, not a promise that clean-runner support and a remote run will fit. Preserve later verification/handoff time; if the repair exceeds its allocation, carry it forward without silently adding hours. Actual minutes are unknown.

## Workflow gaps identified before repair

Reviewed `.github/workflows/setup.yml` and the suite entry points on October 14, 2026. The table records the starting gaps. The repair is now implemented and locally verified; GitHub execution remains pending publication.

| Area | Current state | Requirement before Day 7 API implementation |
|---|---|---|
| Setup | Installs pinned tools/locked environments, runs doctor unit regressions, starts synthetic Compose services and checks runtime acceptance. | Retain these checks. Prove fresh-runner setup/cleanup for the tested commit. |
| Application and fault suite | Workflow does not invoke `tools/run_test_suite.py`. | Invoke the complete suite and require its validated result; do not substitute a subset or allow failed required stages. |
| Database provisioning | Day 6 tests/tools use the fixed local project/cluster identity. A fresh PostgreSQL cluster has a different identity. | Provision an independent synthetic CI target, capture its actual identity and verify ownership/isolation before any migration or write. Keep local source guards intact. Never copy personal database contents into CI or globally relax the identity checks. |
| Browser prerequisites | Suite expects pinned Playwright/Chromium under a temporary local installation unless explicitly configured. | Provision the audited browser dependencies on the clean runner and configure the suite's supported paths. Do not assume a laptop's `/tmp` files exist on GitHub. |
| Migration verification | Normal suite includes rollback-only migration audits; the standalone committed undo/reapplication verifier is separate. | Include committed disposable migration roundtrip verification as a required check as well, retaining ordered schema comparison and preservation evidence. |
| Fault effectiveness | Existing suite validates actual case/fault inventories, not only stage exit statuses. | Preserve those gates, isolated faults, timeout/failure handling and source preservation. Include applicable new regression controls. |
| Reporting | Setup logs alone do not demonstrate Day 6 coverage. | Record the exact commit, workflow/run URL, required-job outcomes and first failure. Keep synthetic/sanitized reports only; never upload raw private environment or credential data. |
| Cleanup | Setup workflow has final cleanup for its Compose resources. | Ensure CI also removes only its owned database copies, fixtures and browser/server processes on failure or cancellation. Preserve correct failure status if cleanup also fails. |

The database portability gap means a one-line workflow addition is insufficient. Design the CI-owned target boundary before changing guards or adding execution commands. Applied local migrations and both existing database volumes must remain unchanged.

## Acceptance and handoff

- [ ] A clean environment can provision every required dependency and synthetic target without personal credentials or a reused local database.
- [ ] Existing setup checks, all retained Day 6 cases/faults, runner controls and standalone migration roundtrip execute and validate their full inventories.
- [ ] A deliberately failing required check makes the job fail; missing dependencies or required cases cannot become a green skip.
- [ ] Owned resources are cleaned after success and failure; output and artifacts contain no compromising information.
- [ ] Required GitHub jobs pass for the exact reviewed commit; record the run URL and first failure if any. Current status: PENDING.

📚 Learn first: [the complete suite commands](../testing/test-suite-commands.md), prerequisites and safety boundaries; [the latest publication/refactor review](../testing/documentation-publication-security-review.md), limitations and remote-history state.
↩ Return: inspect [implementation verification](../testing/cumulative-ci-verification.md), then verify the published commit in GitHub Actions. The learner explicitly authorized AI implementation and the guarded publication of reviewed changes. Local execution passed; the remote day-start gate remains pending.
