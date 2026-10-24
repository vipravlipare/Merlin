# Sprint 1 — Jira checklist guide

Updated October 23, 2026. **Use [MER-1](https://vipravlipare.atlassian.net/browse/MER-1) for Day 6.** Its 16 native Jira checkboxes are the single place to tick progress. The six old subtasks are redundant and are not additional work. The learner deleted MER-2–MER-7; October 7 live project read-back confirms they are absent and only the seven daily Stories remain. Use only the main checklist. Day 7, Day 9, and Day 10 now have detailed checklists in [Day 7](day-seven-jira-checklist.md), [Day 9](day-nine-jira-checklist.md), and [Day 10](day-ten-jira-checklist.md). Days 8, 11, and 12 remain short templates until their work is ready.

## Day 6 — users and notes

**Goal:** design users and notes, then attempt your first migration and Python connection if prerequisites pass. You write the code. A complete backend is not expected.

**Work top to bottom. Tick a box only after you have its evidence.** If blocked, leave it unchecked and record the next action.

### 1. Review setup and understand the rules — 90 min

- [ ] Review existing Sprint 0 evidence (45 min); reuse passing checks and name any blocker.
- [ ] Explain: if the second write fails in one transaction, rollback removes the first uncommitted write too.
- [ ] Explain: authenticated backend identity determines ownership; submitted owner_id is not proof.
- [ ] Explain: an admin connection can bypass restrictions, so it cannot prove ordinary-user denial.

📚 Learn first: [Transactions](https://www.postgresql.org/docs/17/tutorial-transactions.html) (stop before savepoints); [Row security](https://www.postgresql.org/docs/17/ddl-rowsecurity.html) (privilege exceptions).
↩ Return: write the three explanations in your own words (45 min).

### 2. Design users and notes — 60 min

- [ ] Write your own users table: ID, email and creation time; explain type, required fields and rules.
- [ ] Write your own notes table: ID, owner, title, body and creation/update times; decide email normalization, title limits, missing-owner/deletion behavior and index reasons.
- [ ] Write expected results for valid records, duplicate email, invalid notes, rollback, reconnect and cross-user access; review the design before coding.

📚 Learn first: [Constraints](https://www.postgresql.org/docs/17/ddl-constraints.html) (required, unique, primary/foreign-key and check rules); local Part 11 starter contract.
↩ Return: produce two Markdown tables and expected cases; 30 min design + 30 min cases/review.

### 3. Attempt your first implementation — 60 min

- [ ] Record chosen driver/migration/test approach and versions; verify locked installation and imports.
- [ ] Prove separate synthetic test project, network, ports, volume and cluster before database changes.
- [ ] Personally write, review and attempt the users/notes migration and Python connectivity probe on that isolated target.

📚 Learn first: [Locked dependencies](https://docs.astral.sh/uv/concepts/projects/sync/); local docs/sprints/database-foundation-start.md has full prerequisite commands.
↩ Return: 15 min entry checks + up to 45 min coding; prerequisite delays reduce coding within this hour. A driver connects Python; a migration changes database structure. Scratch numbered migrations plus psql are sufficient.

### 4. Verify what you implemented — 39 min

- [ ] Check valid inserts and rejected duplicate emails, missing owners and invalid titles.
- [ ] Check whole-transaction rollback and committed rows after reconnecting.
- [x] Check migration undo/reapplication in disposable storage only. Verified committed down/up, actual fresh baseline, all 389 rebuilt cases and source preservation: [4.3 evidence](../testing/database-step-four-verification.md#43-undoreapplication-current-review).
- [ ] Record actual PASS/FAIL/PENDING results and first failure; cross-user denial stays PENDING unless an ownership boundary exists.

📚 Learn first: [Testing](https://docs.pytest.org/en/stable/getting-started.html) (running tests); [Transactions](https://www.postgresql.org/docs/17/tutorial-transactions.html) (rollback).
↩ Return: compare expected/observed results for your code. Missing tests are not passes; admin queries do not prove ownership denial.

### 5. Leave a clear handoff — 45 min

- [x] Record authored work, observed results, actual minutes (or unknown), first blocker and exact next action. [Day 6 handoff](../planning/day-six-handoff.md).
- [x] Review changes for secrets; leave unfinished code/tests open and carry them forward. [Scoped secret review](../testing/day-six-secret-review-results.json); open carryover is recorded in the handoff.

📚 Learn first: [Reviewing changes](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository) (status/diff; stop before committing).
↩ Return: write a short restart note. A completed handoff does not mean unfinished implementation is Done.

**Limits:** never migrate, reset or delete Sprint 0 volume `merlin_postgres_data` or cluster `7691749973399031842`. Keep credentials private. No commit, push or GitHub upload. Login, complete API, UI, caching, AI and deployment are outside Day 6.

**360-minute cap:** steps 1–5 = 294; deferred/uncommitted DSA = 30; reserve = 36. AWS stays deferred. Unfinished work replaces later feature time. Keep the Story open if implementation or required tests remain unfinished.

Optional reference: `docs/sprints/database-foundation-start.md` for commands; `docs/architecture/part-11-schema-ai-architecture.md` for the candidate design. Each checklist group’s Learn/Return applies to its boxes.


## Short later-day templates

| Day | Ticket | Tentative focus | Daily cap |
|---|---|---|---:|
| 7 | [MER-8](https://vipravlipare.atlassian.net/browse/MER-8) | [First local API and CI review checklist](day-seven-jira-checklist.md) | 240 min |
| 8 | [MER-9](https://vipravlipare.atlassian.net/browse/MER-9) | Local provider readiness | 360 min |
| 9 | [MER-10](https://vipravlipare.atlassian.net/browse/MER-10) | [Small provider decoder checklist](day-nine-jira-checklist.md) | 240 min |
| 10 | [MER-11](https://vipravlipare.atlassian.net/browse/MER-11) | [Owner-scoped notes checklist](day-ten-jira-checklist.md) | 300 min |
| 11 | [MER-12](https://vipravlipare.atlassian.net/browse/MER-12) | Catch-up and verify the small working path | 300 min |
| 12 | [MER-13](https://vipravlipare.atlassian.net/browse/MER-13) | Sprint review and next plan | 240 min |

MASTER_PROMPT D10 is Deliverable 10 (the Workflow Bible), not calendar Day 10; it remains a separate planning artifact. MER-11 continues the schedule’s Day 10 owner-scoped-notes focus. Day 7 has five timed sections and 16 native checkboxes; no subtasks were added. Reforecast carryover before expanding. The seven caps total 2,040 minutes (34 hours). AWS and DSA remain deferred. Future framework versions and AI measurement gates are resolved before implementation, not treated as installed/completed by these placeholders.

## Optional details

[Exact prerequisite commands and observed readiness](database-foundation-start.md) · [Part 11 candidate](../architecture/part-11-schema-ai-architecture.md) · [Sprint 1 reference](../sprints/part-18-sprint1.md). These are references when needed, not additional Day 6 tickets.

## Ticket naming rule

Use one daily Story titled `Day N — clear outcome`. Keep steps as checkboxes inside that Story. Create no subtasks unless the learner explicitly requests them. Only daily Stories should be created in MER going forward.

The requested renumbering of MER-8–MER-13 to MER-2–MER-7 was not performed. Jira assigns real issue keys automatically; deleting subtasks does not provide a supported way to rename existing keys or rewind this project's counter. Keep the real ticket links in the table above. Day numbers in titles are the learning sequence; issue numbers are Jira's sequence.

If subtasks are explicitly requested later, use a distinct summary such as `D07-S01 — Verify connectivity`. This changes the title only: a subtask in MER still receives a MER issue key. A separate key prefix requires a separate project and is outside this change.

📚 Learn first: [Jira work items and keys](https://support.atlassian.com/jira-software-cloud/docs/what-is-a-work-item/); [Cloud issue-counter restrictions](https://support.atlassian.com/jira/kb/set-jira-project-issue-key-counter-to-a-custom-starting-number/). Official pages retrieved October 7, 2026; the counter guidance permits numbers after existing keys, not below them.
↩ Return: identify daily work by its `Day N` title and use its actual Jira link.

## Verification and handoff

Jira HTML read-back confirms 16 unchecked native task items in MER-1; actual browser clicking was not tested, and no learning item was checked on the learner's behalf. Native task-list markup follows the connector's retrieved content-format guide. Day 7–12 creation returned MER-8–MER-13 and successful sprint assignments; sprint-scoped read-back confirms the seven daily Stories; latest project read-back confirms seven To Do daily Stories and no subtasks; MER-2–MER-7 are absent. Current official PostgreSQL, pytest, uv, Git, FastAPI and Ollama references retrieved October 7, 2026. Context7 unavailable. Existing setup/dependency readiness was not rerun during this editorial task.

Next: open MER-1 and work top to bottom, starting with reused Sprint 0 evidence. No code, migrations, configuration, database operations or GitHub publication occurred.

