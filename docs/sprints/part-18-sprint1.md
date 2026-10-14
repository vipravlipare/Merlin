# Part 18 — Sprint 1, Days 6–12

Goal: learner-owned database/API foundation, followed by the local provider boundary and green checks when their gates pass. A walking skeleton is a thin working path across required boundaries; it is not complete because those boundaries have planning files. October 6 audit confirms local Python/PostgreSQL/Redis readiness, not installed feature dependencies or a running API.

## Day 6 — Tuesday October 6 — First database foundation

Budget: **360 minutes floor**. Net work 249 + former DSA uncommitted 30 + rituals 45 + reserve 36 = 360. No stretch committed; actual learner minutes unknown. Local checklist IDs are not issued Jira keys. At most two active outcomes. The original broad database/auth/API/CI/provider forecast is narrowed; no promise to finish all of it today.

📚 Learn first: [current setup audit](../setup/part-04-environment-setup.md#current-coding-readiness-audit--october-6-2026), actual checks; [C-04 entry tasks](../checklists/part-06-checklists-first-half.md#day-6-expanded-entry-tasks--october-6), prerequisite gates; stop before optional models/frameworks.
↩ Return: start C-04.01 then the first users/notes portion of C-04.02. Conditional C-04.03 is the first learner coding attempt, after dependency/isolation checks. Stop at the cap and record the next failed gate. Read current Part 17 for observed CI/public-clone acceptance; earlier completion gaps are historical once its closure table passes. Learner learning evidence remains separate.

| Block | Minutes | Outcome / stop boundary |
|---|---:|---|
| Existing setup spill / closure | 45 | Review completed README/SETUP/doctor/CI evidence against Part 17; complete learner explain-back and prerequisite checks. Do not silently reclaim the allocation for features; record actual time and any remaining spill. |
| C-04.01 learn/explain-back | 45 | Transaction rollback, server-derived ownership, privileged-role exceptions. |
| C-04.02 first slice design | 60 | Two 30-minute steps: adapt users/notes fields and constraints, then write acceptance/rollback/ownership cases. No all-table rewrite. |
| C-04.03 conditional coding | 60 | Dependency/isolation gate, 15 minutes; learner migration/connectivity attempt, 45 minutes. If prerequisites fail, stop before database changes; unfinished dependency work displaces coding. |
| Verify / record first failure | 39 | Run only cases for implemented work, record expected/observed results and redacted errors. Missing code is pending, never a passing test. |
| Uncommitted former DSA slot | 30 | Learner deferred; no automatic reassignment or mastery claim. |
| Rituals | 45 | Stand-up, actual ledger, diff/secret review, explain-back/restart point. Review existing quiz's missed concept if known. |
| Reserve | 36 | Unexpected committed-scope work only; unused minutes do not fund new scope. |
| **Total** | **360** | Net work is 249 minutes, including setup spill and verification. |

### Day 6 checklist — steps 1–5

**Goal:** understand and design the first users/notes slice, then attempt and verify learner-written database work. Reading is preparation; tick an item only after producing its evidence. Start with Step 1 and use at most two active work items.

Canonical Day 6 remains October 6. If you execute it October 7 or later, record the actual date; do not skip unfinished work simply to match the calendar. The five steps use **294 minutes**, including rituals; add the uncommitted DSA slot 30 and reserve 36 for the unchanged **360-minute cap**. No application code, migration or SQL is supplied by this plan.

#### Step 1 — Review setup and explain the database rules | 90 minutes

Allocation: existing setup review 45 + C-04.01 learning 45. Reuse current passing evidence rather than reinstalling tools or recreating the original database.

📚 Learn first: [Sprint 0 closure](part-17-sprint0.md#setup-closure--october-6-2026), observed acceptance; [PostgreSQL transactions](https://www.postgresql.org/docs/17/tutorial-transactions.html), all-or-nothing and commit/rollback; [row security](https://www.postgresql.org/docs/17/ddl-rowsecurity.html), owner/superuser/bypass exceptions; stop before savepoints and policy implementation.
↩ Return: write the explanations in your learner evidence note and draw client → backend identity → database. Done when you can explain each boundary; stop at 90 minutes including setup review, and record any confusion instead of claiming mastery.

- [ ] Review README/SETUP, doctor, published CI and unchanged-clone evidence against Part 17; record any current prerequisite blocker.
- [ ] Confirm the Ubuntu working folder and private configuration boundary; complete or name remaining Sprint0 explain-back gaps.
- [ ] Explain what happens to the first uncommitted write when the second write in the same transaction fails and the transaction is rolled back.
- [ ] Explain why owner identity must come from trusted backend/authenticated context, not a submitted `owner_id`.
- [ ] Explain why an administrative database connection cannot prove ordinary-user row-security denial.
- [ ] Draw the ownership boundary and record the actual date/minutes, or “unknown”.

**Output:** setup review and three learner explanations. Software checks do not supply your answers.

#### Step 2 — Design users and notes | 60 minutes | C-04.02 first slice

Two 30-minute portions: fields/rules, then expected cases. The larger C-04.02 also covers future tables; completing this slice does not finish the whole component.

📚 Learn first: [Part 11 starter contract](../architecture/part-11-schema-ai-architecture.md#day-6-usersnotes-starter-contract), candidate fields and acceptance table; stop before future AI schemas.
↩ Return: write your own plain-table design and explain every rule/index. Done when both tables and success/failure/ownership expectations are reviewable; stop at 60 minutes. Request a concept hint after sharing the uncertain portion, rather than copying a migration.

- [ ] Define `users`: ID, normalized email and creation time; record types, required fields, primary key and uniqueness rules.
- [ ] Define `notes`: ID, owner, title, body, creation/update times; record types, foreign key and constraints.
- [ ] Decide email normalization, nonblank title with maximum 200 characters, empty-body behavior, timestamp updates and deletion of a referenced owner.
- [ ] Explain how one note belongs to one user and why a UUID is not authorization.
- [ ] Justify each selected index using an actual lookup/listing pattern; do not add vector indexes or unmeasured performance claims.
- [ ] Write expected results for valid records, duplicate email, missing owner, invalid titles, transaction rollback, reconnect and cross-user denial.
- [ ] Review the design before coding; record unresolved choices instead of inventing agreement.

**Output:** learner-authored Markdown schema and input/expected-result cases. No SQL yet; tasks, sources and audit tables remain later work.

#### Step 3 — Verify prerequisites, then write the first migration | 60 minutes | C-04.03 conditional

A driver lets Python communicate with PostgreSQL. A migration is a versioned database-structure change. Use 15 minutes for the entry gate and up to 45 for the learner attempt; unfinished prerequisite work reduces coding time in the same block.

📚 Learn first: [uv locked execution](https://docs.astral.sh/uv/concepts/projects/sync/), lock consistency; [Day 6 dependency/storage gates](#implementation-entry-and-acceptance-gates), prerequisites; stop before framework expansion. Verify the chosen packages' official version/API documentation at first use.
↩ Return: verify dependencies and isolation before personally writing code. Done only after the migration/connectivity attempt and its required cases have observed evidence; at the cap, preserve work and record the exact failed gate. Never reset or migrate the retained setup cluster as an experiment.

- [ ] Record database driver, migration/test approach, exact selected versions, synchronous/asynchronous choice and transaction scope.
- [ ] Verify compatible resolution, locked installation and required imports. Introduce only packages this slice needs; do not install FastAPI/ORMs just to fill a stack list.
- [ ] Confirm a separate test project/network/ports/named volumes and synthetic data; record safe identities without passwords.
- [ ] Confirm test storage is not `merlin_postgres_data` or cluster `7691749973399031842`; if isolation is uncertain, stop before changes.
- [ ] Personally write the first users/notes migration and a minimal connection/readiness query in the agreed learner-code location.
- [ ] Apply only to isolated storage; record what the migration changes and how to undo it there.
- [ ] Keep credentials private and out of source, shell arguments, error logs and Jira.

**Output:** selected dependency evidence and your code attempt. If entry gates fail, this step remains incomplete; “attempted” is not “implemented”.

#### Step 4 — Verify what you implemented | 39 minutes

📚 Learn first: [Part 11 acceptance cases](../architecture/part-11-schema-ai-architecture.md#day-6-usersnotes-starter-contract), expected state and ownership limits; stop before application expansion.
↩ Return: run the applicable cases and record expected versus observed outcomes. Done when the cases required for implemented work pass; missing code is pending and failures remain open. Stop at 39 minutes; tests that do not fit displace later feature work rather than adding hours.

- [ ] Confirm migration creates only the intended objects in isolated storage and leaves the original cluster untouched.
- [ ] Verify valid user/note writes and data present after commit/reconnect.
- [ ] Verify duplicate normalized email, nonexistent owner, blank title and oversized title are rejected without invalid retained rows.
- [ ] Force a failure in the second write of one transaction; verify the first write does not remain after rollback.
- [ ] Verify migration rollback/reapply in disposable storage only; do not confuse schema downgrade with transaction rollback or backup restore.
- [ ] If an owner-scoped repository boundary exists, test actor A accessing A's note and actor B guessing A's ID/changing owner input; require no unauthorized rows or modifications.
- [ ] If ownership code does not exist, leave denial tests **pending**, link later C-04.04 work and do not claim secure ownership or protected-API completion. Administrative queries do not prove denial; RLS tests need a suitable non-owner, non-superuser, non-BYPASSRLS role.
- [ ] Record case status PASS/FAIL/PENDING, safe commands/results and the first failure/fix; review errors for secrets. Reuse current setup CI proof, but do not claim it tests the new feature code automatically.

**Output:** an honest result table. Foreign keys validate references; they do not by themselves prevent another user accessing a note.

#### Step 5 — Review and leave a clear restart point | 45 minutes, existing rituals

📚 Learn first: [Git recording changes](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository), inspect changes; [Part 1 spill rule](../project/part-01-waterfall-and-assumptions.md), swap-not-add; stop before publishing examples.
↩ Return: write the handoff and update local evidence/Jira when connected. Done when progress, time, blocker and next action are explicit and secret review passes; stop at 45 minutes. User's current instruction prohibits committing or pushing this work to GitHub.

- [ ] Record stand-up: completed outcome, current blocker and next action.
- [ ] Record actual date and minutes for each block, or “unknown”; keep DSA deferred and its 30 minutes uncommitted.
- [ ] Review the local diff and files for secrets; do not commit or push to GitHub under the current instruction.
- [ ] Review the migration and results; list unresolved tests, ownership limitations and dependencies.
- [ ] Write the exact next unchecked action and where the learner's evidence/code is located; carry unfinished work forward explicitly.
- [ ] Answer a short end-of-day quiz: rollback versus downgrade; trusted ownership versus submitted ID; why setup CI cannot prove an unbuilt feature.
- [ ] Give a 60-second interview explanation of the users/notes relationship, isolation and transaction choice; record learning gaps and schedule the spaced re-quiz inside existing future ritual time.
- [ ] Update only genuinely completed Jira child items; keep incomplete implementation items open. Do not mark the parent Done merely because the time box ended.

**Output:** learner handoff, time ledger and reviewed checklist. Keep the existing 36-minute reserve for unexpected scoped work; do not spend it on new features automatically.

#### How to check off learning and coding

The five steps above supply the Learn/Return links and time limits for this review. Record evidence beside each checked item; reading alone cannot complete a learning item.

| Evidence stage | Check it off when | Keep it open when |
|---|---|---|
| Learned | You explain the concept in your own words and answer a follow-up without copying the answer bank | You only read the explanation or still need the answer supplied |
| Designed | Your users/notes field tables, decisions and expected test results are reviewed | A required rule or expected result is missing |
| Coded | Your migration/connectivity code exists, dependencies work and storage isolation is proven | Only a plan exists, installation fails or storage identity is uncertain |
| Verified | Required implemented cases have observed passing results | A required case fails or has not run; future ownership code remains explicitly pending |
| Handed off | Safe evidence, actual minutes or “unknown”, first blocker and exact next action are recorded | Results or restart instructions are missing |

These stages are independent: a checked learning item does not mark coding or verification Done. Day 6 produces a first database foundation, not a complete backend.

### Jira-ready ticket — Day 6 database foundation

**Current tracking rule:** use MER-1’s 16 native checkboxes. The six-child specification below records the original creation plan; latest STATE makes MER-2–7 redundant pending manual deletion. Do not treat them as additional completion gates.

**Connection/publication status — October 7, 2026:** Live Atlassian access worked. MER board 2 and existing future `MER Sprint 1` ID 3 were inspected; exhaustive pre-create project JQL returned no issues. Created [Story MER-1](https://vipravlipare.atlassian.net/browse/MER-1) in that sprint and six Subtasks MER-2 through MER-7. Read-back confirms all To Do and correct parents. No sprint created/started; no learner completion claimed. See [current readiness, exact commands and real ticket mapping](database-foundation-start.md). Assignee, points and due date unset; no existing Epic found. No GitHub publication authorized.

| Jira field | Ready value |
|---|---|
| Space | `MER` — existing team-managed Scrum space |
| Work type | Story; use its supported child/subtask type for the six bounded items below |
| Title / Summary | Day 6 — Build and verify the first users/notes database foundation |
| Sprint | Existing Sprint 1 if present; actual Jira sprint name/ID must be read after connection. Do not create or start a duplicate sprint |
| Status / Assignee | Initial To Do; assign to the learner after account identity is confirmed |
| Labels | `sprint-1`, `day-6`, `database`, `learner-owned` |
| Points | Proposed 3 points for 249 net minutes (about 4.15 h, provisional 1 point ≈ 1.5 h). Not yet assigned; do not count points again on child items |
| Canonical date / due date | Day 6 October 6, 2026; actual execution may be October 7 or later. Do not invent a new due date |
| Parent / Epic | Link to the existing relevant database-foundation parent only after finding its real key; no invented Epic |
| Description | Use the goal, five numbered steps and checkboxes above, plus the completion criteria below |
| Evidence | Learner note with table design, expected/observed cases, exact safe test identities, actual time and restart point; no secrets |

**Story:** As the learner building Merlin, I want a designed, isolated and verified users/notes database foundation so that later API work starts from explicit data rules and observed behavior.

#### Child work items — six bounded outcomes, no extra hours

These are local planning IDs, not Jira keys. Once Jira is connected, record returned `MER-…` keys beside them. Each child inherits the relevant Learn/Return block and checklist above; no paid checklist plugin is required to track its status.

| Local mapping | Child title | Minutes | Done criterion / checklist source |
|---|---|---:|---|
| D6-SETUP | Review existing setup evidence and entry readiness | 45 | Step1 setup items evidenced; personal gaps named, not silently passed |
| C-04.01 | Explain transactions and ownership boundaries | 45 | Step1 three answers and boundary drawing reviewed |
| C-04.02 first slice | Design users/notes and acceptance expectations | 60 | Step2 tables/rules/index rationale and case expectations reviewed; broader C-04.02 remains partial |
| C-04.03 | Write first isolated migration/connectivity slice | 60 | Step3 entry gates pass, learner code exists and required implemented cases pass; an attempt alone is not Done |
| D6-VERIFY | Verify implemented database behavior | 39 | Step4 required implemented cases have observed results; future ownership work explicitly pending if absent |
| D6-EOD | Review changes and record handoff | 45 | Step5 time/evidence/security/restart checklist complete |
| **Tracked total** | **Five steps, six children** | **294** | Plus uncommitted DSA 30 + reserve 36 = 360 |

#### Parent completion criteria

- [ ] Setup review, three explanations, users/notes design and expected cases are reviewed.
- [ ] Compatible dependencies and isolated storage are verified; learner-written migration/connectivity work exists.
- [ ] Implemented migration, constraint, transaction, reconnect and rollback/reapply cases pass with safe evidence; required failures remain open.
- [ ] Ownership-denial expectations are explicit. Any unimplemented boundary stays linked to pending C-04.04; the parent does not certify authentication or ownership security. Do not mark C-04.03/security completion beyond its actual cases.
- [ ] Original setup storage is preserved, evidence contains no secrets, actual minutes/unknown and next action are recorded.
- [ ] All child outcomes are genuinely complete; no item is closed merely for reading, hitting the cap or naming a blocker.

If coding or required verification remains unfinished, keep the parent open/In Progress and name the first blocked child. The **day's handoff** can be complete while the **implementation story** stays open. New login, protected API, tasks/sources/audit tables, UI, Redis caching, AI/models and AWS deployment are out of scope.

Acceptance examples for the ticket:

```gherkin
Scenario: A transaction is rolled back after the second write fails
  Given isolated synthetic storage and one transaction containing two writes
  When the second write fails and the transaction is rolled back
  Then neither write remains from that transaction

Scenario: Invalid note data is rejected
  Given the reviewed users/notes constraints are implemented
  When a note has a nonexistent owner or an invalid title
  Then the write is rejected and no invalid row remains

Scenario: Required implementation is unfinished
  Given dependencies, migration code or required verification is incomplete
  When the Day 6 time box ends
  Then the story stays open and the handoff identifies the next failed gate
```

Jira creation and checklist review belong inside the existing setup/ritual allocations; they do not add hours.

**Creation recipe used October 7 (do not repeat):** create the Story in MER, use the title/fields above and paste steps 1–5 plus completion criteria into Description. Add six child work items using the table; track their statuses. Markdown checkboxes are directly usable in this local file; Jira rich-text rendering may require recreating checklist formatting, so child statuses are the reliable fallback. No paid add-on or CSV import is needed.

📚 Learn first: [Atlassian create a work item/child](https://support.atlassian.com/jira-software-cloud/docs/create-a-work-item-and-a-subtask/), Create and child work items; [team-managed subtasks](https://support.atlassian.com/jira-software-cloud/docs/manage-subtasks-in-team-managed-projects/), parent/child tracking; stop before workflow customization. Official pages retrieved October 7, 2026; actual MER fields/permissions still require connected inspection.
↩ Return: after Atlassian sign-in/authorization, verify the site, MER space, existing sprint and any duplicate work item before creating the prepared Story/children. Done means returned real keys and matching checklists; until then keep this draft local. Never send account passwords, recovery codes or API secrets in chat or upload these drafts to GitHub.

### Implementation entry and acceptance gates

📚 Learn first: [uv locked execution](https://docs.astral.sh/uv/concepts/projects/sync/), avoiding silent lock changes; [PostgreSQL transactions](https://www.postgresql.org/docs/17/tutorial-transactions.html), commit/rollback; stop before advanced examples. These pages and PostgreSQL row-security documentation were retrieved October 6, 2026.
↩ Return: verify the interpreter and quiet Compose configuration, then use the Part 11 case table in isolated synthetic storage. Done means personally written code and observed outcomes, not copied examples or assistant infrastructure checks. The 60-minute implementation block includes dependency selection/installation.

Gate 1: preserve Ubuntu `.venv` Python 3.12.14 and working image pins. Gate 2: first-use driver/migration/test packages must resolve together and pass a locked install/import check; current dependencies are empty. FastAPI/SQLAlchemy are introduced only when the selected slice needs them, not installed merely to fill a stack checklist. Gate 3: isolated test storage and synthetic identities must not share the retained setup volume. Gate 4: required migration, constraint, transaction, reconnect and downgrade/reapply cases must pass before the first migration slice is Done. Ownership-security completion separately requires an implemented boundary and passing cross-user tests; absent ownership code stays pending under C-04.04 and cannot support a security claim. Gate 5: protected API work needs identity and a limited application database role; an administrative setup credential is not a safe deployed authorization boundary.

Safe startup checks in the existing checkout:

```bash
cd /home/vipra/Merlin
uv run --locked --offline python --version
docker compose config --quiet
docker compose ps
```

No feature code, SQL/DDL, workflow or doctor script is supplied here. Scratch reasoning and small explicit database operations come before ORM abstractions; compare the choices in an ADR when the abstraction is introduced. AI, pgvector, UI, AWS and implemented Redis caching are outside this first slice. Services currently remain running for coding; safely stop afterward with `docker compose stop --timeout 30 postgres redis`.

### Days 7–12 — Reforecast at actual progress

📚 Learn first: [Part 1 capacity and spill rules](../project/part-01-waterfall-and-assumptions.md), daily floor and reserve; stop before optional scope.
↩ Return: use the Day 6 ledger to choose the next unchecked outcome. CI's requested latest deadline is Day 7; if unfinished, record a blocker and displace feature time. Day 8 Ollama is conditional on hardware/funded first-use gates, not automatic. Day 12 reviews actual evidence and scope. Expand each next day before execution; do not claim an executable full-sprint schedule from this outline. MVP-0 is conditional on its actual definition passing.

Resources: current official transaction/row-security/uv pages retrieved October 6; previous broader resource indexes are historical. Dependency API/version compatibility remains first-use verification. No new Context7 verification is claimed.
NEXT: learner C-04.01/.02, then conditional C-04.03; update actual minutes and reforecast Day 7.
