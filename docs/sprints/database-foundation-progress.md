# Day 6 verification and live Jira status

**Historical progress record.** The latest live checklist and evidence-based verdict are in the [MER-1 completion audit](../testing/mer-1-completion-audit.md). Earlier absent-schema, blocked-runtime and pending-test findings below are superseded by later successful implementation and verification.

**Latest update October10:** the learner has now successfully applied the migration. Fresh separate read-only inspection confirms users/notes/active_notes and embedded Unicode counting; both tables are empty. Step3.3 migration attempt now has evidence. Prior tables-absent/PLPython-blocked statements below are historical. Step4 actual data/transaction/ownership/undo tests remain pending. See [setup and migration explanation](../learning/docker-and-database-migrations.md).

Observed October 10, 2026. Read [MER-1](https://vipravlipare.atlassian.net/browse/MER-1) through the connected Atlassian tool; no Jira changes were made.

## Live checklist

MER-1 is In Progress. Ten of sixteen boxes are checked: Step 1 has four checked; Step 2 has three checked; Step 3 has three checked. Step 4 has four unchecked; Step 5 has two unchecked. These are observed Jira marks, not independent proof of each learning outcome.

The Step 3 box combines migration and probe attempts. Source files and the learner-reported working probe exist, but there is no recorded successful migration application. The live database has no users/notes tables. Preserve that distinction in the handoff; a checked attempt does not establish a working schema.

The ticket still names the old docs/sprints/database-foundation-start.md reference; its purpose-based replacement is docs/sprints/database-foundation-start.md. That local document also contains historical setup claims. Use current STATE.md and this snapshot for current observed results.

## Step 4 results

## Requirement-by-requirement completion audit

This audit evaluates the checkbox text, not whether Jira displays a tick. DONE means the specified observable outcome has evidence; PARTIAL means only part of a combined requirement is supported; UNVERIFIED means the required personal outcome has not been observed; PENDING means execution is missing or blocked.

| Checkbox requirement | Evidence-based result | What exists / what is missing |
|---|---|---|
| Review Sprint 0 evidence, reuse checks, name blocker | PARTIAL | Prior setup evidence reused and current blocker named. The learner's personal evidence review is not independently recorded. |
| Explain transaction failure and rollback | UNVERIFIED | Explanations and questions exist; no learner answer located in current evidence. Passing mock tests are not an explain-back. |
| Explain authenticated ownership versus submitted owner_id | UNVERIFIED | Specification exists; no learner explain-back located. |
| Explain why admin access cannot prove ordinary-user denial | UNVERIFIED | Specification exists; no learner explain-back located. |
| Write users design with type, required fields and rules | DONE for design artifact | Current users table records UUID, optional email, server times and rules; user supplied decisions in this conversation. This is not database implementation evidence. |
| Write notes design, normalization, limits, owner/deletion and index reasons | DONE for design artifact | Current notes table and surrounding sections record these choices; detailed listing/index purposes also appear in the audit and SQL comments. No deployed behavior implied. |
| Expected results for valid/duplicate/invalid/rollback/reconnect/cross-user cases; design review | DONE for specification/review artifact | Database verification matrix contains explicit expectations and current reviews exist. Authenticated cross-user behavior is still a pending execution outcome. |
| Record approach/versions; locked installation/imports | DONE | Scratch numbered SQL plus psql, Psycopg and pytest approach recorded. Current imports: psycopg/binary3.3.6, pytest9.1.1, emoji2.16.0, regex2026.9.29. Fresh uv sync --locked --check --offline passes and would make no changes. This does not establish server PL/Python availability. |
| Prove isolated project/network/ports/volume/cluster | DONE for recorded isolation proof | Learner supplied distinct project, loopback55432, network, volume and cluster evidence earlier; fresh DB/cluster identity matches. Full isolation properties were not all rechecked this turn. |
| Personally write/review/attempt migration AND probe | PARTIAL | Both source files exist, reviews exist and learner reported probe success. Current schema absent; no migration application attempt/error evidence located. Some migration code was assistant-written under earlier explicit requests, so learner personal authorship/review cannot be inferred for every section. |
| Valid inserts and duplicate email/missing owner/invalid title rejection | PENDING | Requires actual SQL tests; tables absent. |
| Whole-transaction rollback and commit/reconnect | PENDING | No actual PostgreSQL execution evidence. |
| Disposable migration undo/reapplication | PENDING | No down file; up migration dependency blocked. |
| Record actual outcomes and first failure; cross-user pending | DONE for current results record | This snapshot plus STATE records unit PASS, historical failures/fixes, database PENDING and first blocker. Cross-user remains PENDING. |
| Handoff: authored work/results/time/blocker/next action | DONE for current handoff artifact | STATE and this snapshot identify work, actual results, unknown minutes, blocker and next action. Personal end-of-day learning reflection is not implied. |
| Review changes for secrets and carry unfinished work | PARTIAL | Private .env permissions/ignore checked; unfinished work recorded. No comprehensive content review of every changed/untracked file was performed. Git status is not a secret scan. |

No Jira checkboxes were changed. The first unverified learning requirements are the three personal explain-backs; the first technical blocker is the isolated server runtime. Neither requires repeating completed Sprint 0 setup.

### Which currently checked boxes need correction?

Step 3's final combined migration/probe box should remain unchecked: probe success is reported, but there is no recorded migration execution attempt or resulting error. Writing/reviewing a migration is not attempting it on the target. Absence of tables proves it has not produced the schema, though a failed attempt could still satisfy an attempt requirement if its evidence were recorded. Do not force a migration run while dependencies are blocked just to obtain a checkmark.

The three Step 1 explain-back boxes are not verified by available evidence. They should remain open unless the learner actually supplied the explanations; reading assistant explanations is insufficient. Their marked state does not prove misunderstanding, and this audit cannot claim the learner never explained them outside the recorded session.

Step 1's evidence-review box has operational evidence but lacks a recorded personal review. Keep it checked only if the learner actually reviewed that evidence and can identify the blocker. It does not require repeating working setup.

The three Step 2 boxes and first two Step 3 boxes have supporting artifacts/checks. All four Step 4 boxes currently remain unchecked. The result-recording requirement has now been satisfied by the current local evidence snapshot; it can be checked independently while the three execution requirements stay open. Jira was not edited.

| Ticket requirement | Actual status | Evidence or missing prerequisite |
|---|---|---|
| Valid inserts; duplicate email, missing owner and invalid title rejection | PENDING / blocked | No users/notes tables; Python helper tests do not exercise SQL constraints. |
| Whole-transaction rollback and committed rows after reconnect | PENDING / blocked | No real database fixture or transaction evidence. Mock context tests are not rollback proof. |
| Migration undo/reapplication in disposable storage | PENDING / blocked | Up migration prerequisites unavailable; no down migration file exists. |
| Record PASS/FAIL/PENDING and first failure/blocker | Results recorded locally here | Latest existing unit suite: 90 PASS in 0.40 seconds. Twelve direct surrogate rejections and three valid controls PASS; these are separate from pytest count. Initial unit failures were fixed; current first database blocker is absent PL/Python. |
| Cross-user denial | PENDING | Draft SQL policies are not deployed; no real limited-role ownership test or authenticated backend boundary evidence. |

The result-recording box can only represent an honest current snapshot, not completion of the other verification boxes. It remains unchecked in Jira because this request was read-only.

## Current read-only database proof

The explicit project merlin-d6-20261008105707 reports database merlin_d6 and cluster 7694311451826794534. The pg_available_extensions query returned zero plpython3u rows. Both to_regclass lookups returned NULL for public.users/public.notes. This confirms current prerequisites remain blocked, rather than relying on an older inspection. No extension, table, migration or maintenance change was made.

First blocker: this isolated image does not offer the extension required by the up migration. The database server also needs its own compatible pinned emoji/regex runtime; packages in the application .venv do not satisfy that gate. Do not remove validation or alter passing tests to bypass missing dependencies.

## Exact next action

Prepare and review an isolated PostgreSQL runtime plan that provides PL/Python and the pinned Unicode packages, without changing preserved Sprint 0 storage. The learner implements any approved configuration under the repository's current code-ownership rules. Once the disposable server gate passes, review/attempt the up migration as one transaction, then run valid/invalid SQL cases and real rollback/reconnect tests. Write and review the down migration before disposable undo/reapplication. Do not run migration commands while the prerequisite remains missing.

Preserve volume merlin_postgres_data and cluster 7691749973399031842. No commit, push or upload. Day 6 remains capped at 360 minutes, including the 39-minute verification block; actual minutes remain unknown. Unfinished database work displaces later feature time. AWS and DSA remain deferred.

📚 Learn first: [database verification matrix](../testing/users-notes-database-verification.md), use its SQL case expectations and read-only gate; its earlier 82/8 unit counts are historical and superseded by this snapshot. [Current handoff](../planning/STATE.md).

↩ Return: resolve the isolated server runtime prerequisite before trying the first valid insert. Keep database results PENDING until the actual checks run.
