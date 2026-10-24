# Day 10 — MER-11 owner-scoped notes

Checklist and evidence record for [MER-11](https://vipravlipare.atlassian.net/browse/MER-11), the Day 10 owner-scoped-notes story in `database-foundation-jira-guide.md`. The story has a 300-minute cap. The internal implementation, tests and local CI work were assistant-authored at the learner’s request; their presence does not prove learner authorship, review or understanding. Actual minutes remain unknown.

## Keep the original plan aligned

MER-11 and the Sprint 1 guide name **owner-scoped notes** for calendar Day 10. `docs/planning/MASTER_PROMPT.md` calls the Workflow Bible **Deliverable D10** in its D9–D13 deliverable sequence; that is not calendar Day 10 and remains a separate planning artifact. Keep both scopes in the original plan; do not substitute one for the other.

## Goal and safety boundary

Plan one small, read-only notes access path scoped to a trusted application identity. Reuse the existing notes schema and database ownership rules; do not add migrations, retention behavior, broad CRUD, or a new framework in this slice.

The current application has no authentication boundary or notes route. A request body’s `user_id` or a synthetic test actor is not proof of a real user’s identity. If the application has no trustworthy actor source, keep the read path internal to tests/design and do not expose a public or unauthenticated route. State clearly what the synthetic actor tests prove and what they cannot prove about authentication.

Before implementation, require cumulative CI through Day 9 to pass on the current exact revision, including provider parser cases/faults, prior application checks, migration safety, and cleanup. Latest recorded gate: commit `5032c6e14090c45a7062ea81abd6fbfecf3a48fb`, [run 40009971455](https://github.com/vipravlipare/Merlin/actions/runs/40009971455), all required steps PASS. At Day 10 start, verify HEAD still matches or observe a new green run for the current SHA. A local green run, prior commit, skipped check, or manual database state is not this gate.

## 1. Review current state and gate the work — 35 min

- [x] Read the Day 9 handoff and the current hosted cumulative run for the exact repository revision (10 min). Record its SHA, workflow URL, required-job result, and any missing gate. If it is not green, stop feature implementation and use this budget to investigate the failed gate. **Assistant-verified October 23:** HEAD `5032c6e14090c45a7062ea81abd6fbfecf3a48fb` matches [hosted run 40009971455](https://github.com/vipravlipare/Merlin/actions/runs/40009971455), completed success; the `setup` job and every required step passed. Only Day 10 planning documents are currently modified/untracked; application, tests, and CI inputs were not changed after that run. Actual minutes unknown.
- [x] Record that MASTER_PROMPT Deliverable D10 is the separate Workflow Bible, while calendar Day 10 is MER-11 owner-scoped notes (15 min). Preserve both parts of the original plan; do not replace one with the other. **Assistant-verified October 23:** MASTER_PROMPT §7 places D10 in the D9–D13 deliverable sequence; MER-11 and the Sprint 1 guide identify calendar Day 10 as owner-scoped notes. These are separate plan items, not a scope conflict. Actual minutes unknown.
- [x] Inspect current notes files and status evidence; identify the trust source for an application actor. Do not infer authentication from the database’s synthetic actor setting (10 min). **Assistant-verified October 23:** existing code includes note validation/maintenance and the health API, but no authentication module, trusted actor provider, notes repository, or notes route. Migration 001 has `merlin.actor_id` RLS policies and explicitly says the setting is not proof of authentication. Therefore no trusted application actor source exists yet; keep notes access internal and do not expose a route until authentication supplies that identity. Actual minutes unknown.

📚 Learn first: [MER-11](https://vipravlipare.atlassian.net/browse/MER-11), current scope; [PostgreSQL row security](https://www.postgresql.org/docs/17/ddl-rowsecurity.html), policy behavior and role exceptions.
↩ Return: write the exact CI SHA/result and the selected Day 10 scope in the handoff. If scope or a required prerequisite is unresolved, keep code changes stopped and carry it forward.

## 2. Learn the identity and transaction boundary — 45 min

- [ ] Learner reads PostgreSQL’s row-security behavior, including default deny and the superuser, `BYPASSRLS`, and table-owner exceptions (15 min). **Assistant-reviewed October 23:** default deny applies when RLS is enabled without an allowing policy; superusers and `BYPASSRLS` roles always bypass RLS; table owners normally bypass unless forced subject to RLS. Learner reading is not independently confirmed.
- [ ] Learner reads how transaction-local settings differ from session settings, then reviews the existing application transaction pattern (10 min). **Assistant-reviewed October 23:** PostgreSQL `SET LOCAL` lasts through the transaction and resets at commit/rollback. `app/notes_maintenance.py` uses a Psycopg connection context and transaction-local timeout settings; it is a maintenance worker, not a notes request path. `tests/test_users_notes_database.py` uses transaction-local synthetic actors; that does not establish authentication. Learner reading is not independently confirmed.
- [x] Explain in your own words why a client-supplied `user_id`, an administrator query, or a successful health check cannot prove user ownership (20 min). **Learner explain-back, October 23:** a client-provided `user_id` does not prove the authenticated identity, and a health check confirms service connectivity rather than note ownership. Clarification: an administrator query can access records but its elevated access does not prove that the requesting user owns them. Actual minutes unknown.

📚 Learn first: [PostgreSQL row security](https://www.postgresql.org/docs/17/ddl-rowsecurity.html), read policy behavior and bypass exceptions; [PostgreSQL SET](https://www.postgresql.org/docs/17/sql-set.html), read `LOCAL` and its transaction lifetime; [Psycopg transactions](https://www.psycopg.org/psycopg3/docs/basic/transactions.html), read transaction contexts.
↩ Return: explain how a trusted actor reaches the repository and why its database scope must end with the transaction. Do not claim that this creates login/authentication.

**Step 2 status:** 2.1–2.2 were assistant-reviewed; learner reading is not independently confirmed. 2.3 has a learner explain-back, with the administrator-query distinction clarified. Actual minutes unknown.

## 3. Select and specify one read-only slice — 45 min

- [x] Review the current notes schema, row-level policies, note rules, health API style, and their tests; distinguish existing behavior from proposed application behavior (15 min). **Assistant-reviewed October 23:** `migrations/001_users_notes.up.sql` defines users/notes tables, ownership and content constraints, maintenance rules, active-notes view, limited NOLOGIN roles and RLS keyed to transaction-local `merlin.actor_id`; its comments say this setting is not authentication. `app/note_rules.py` validates text and returns a blank-save decision without database writes. `app/notes_maintenance.py` is a guarded disposable-cluster cleanup worker, not a notes request path. `app/health_api.py` serves only `/health` and does not query the database. `tests/test_note_rules_and_maintenance.py` checks helper behavior and mocked worker calls; `tests/test_users_notes_database.py` contains opt-in PostgreSQL checks for constraints/RLS/roles; `tests/test_health_api.py` checks health HTTP behavior, not note ownership. The migration’s PostgreSQL behavior remains conditional on required PL/Python packages and disposable DB execution; no authenticated notes route/repository exists. Actual minutes unknown.
- [x] Choose one small operation: list the actor’s active notes, fetch one note by ID, or both only if the first remains within the cap (15 min). **Learner choice, October 23:** list the signed-in actor’s active notes, newest update first (`updated_at DESC`, with `id` as a stable tie-breaker), excluding trash. The current app has no trusted sign-in identity, so this remains a planned internal operation; do not expose a route yet. Actual minutes unknown.
- [x] Write expected outcomes for the owner and denial cases below before implementation (15 min). **Learner decisions, October 23:** the note list shows each active note’s stored title, or the first 175 weighted text units of its body when the title is absent, plus last-updated time; sort newest edits first. A different signed-in account sees a different owner-scoped set. Notes require a real signed-in identity; the current app has no authentication path, so no notes route is exposed yet. A user cannot access another user’s private notes. Future explicit sharing may expose only the notes shared with that user; sharing is outside this slice. Database failures show a safe error with no private data or internal details. Actual minutes unknown.

📚 Learn first: [current users/notes design](../architecture/users-notes-design.md), written schema and limits; [current database verification matrix](../testing/users-notes-database-verification.md), actor tests and admin-role limits.
↩ Return: record the operation, trusted actor source, transaction boundary, files by purpose, and exact expected response for a guessed foreign note ID. Do not rerun an applied migration or touch the protected Sprint 0 database volume.

**Follow-on product idea, outside this read-only Day 10 slice:** selecting a listed note opens its full saved content; editing should autosave without a Save button. Use Apple Notes as a reference for a dated, sortable note list and opening a note; use Google Docs as a reference for saving edits while typing. These are product references, not evidence that Merlin has editing, autosave, offline sync, conflict handling, or authentication. Basic login is already planned in MVP-0/Day 11 and C-05, but remains unverified. The protected list/detail route is now an explicit Sprint 3 (Days 20–26) catch-up target in `docs/sprints/part-20-sprint3.md`, with auth/least-privilege gates and acceptance checks. Explicit sharing is a separate, unfunded Sprint 4 (Days 27–33) candidate in `docs/sprints/part-21-sprint4.md`, contingent on a scope swap. Keep these features outside MER-11’s current completion claim.

📚 Learn first: [Apple Notes: organize notes and sort by date](https://support.apple.com/en-sa/guide/iphone/ipha61270292/ios); [Google Docs: create, view, or download a file](https://support.google.com/docs/answer/49114?hl=en), read “Save a file.” Pages reviewed October 23, 2026.
↩ Return: keep the current operation read-only; carry note opening and autosave into later scope with explicit failure, retry, offline, and conflict rules before implementation.

### Required behavior table

| Case | Expected result |
|---|---|
| Signed-in actor A opens the notes list | Show each active note’s title, or the first 175 weighted text units of its body if untitled, and last-updated time; exclude trash; sort by `updated_at` newest first and use `id` to break ties. |
| Different signed-in actor B opens the notes list | Show B’s owner-scoped notes, not A’s private notes. |
| B requests A’s guessed note ID | For an unshared note, return the same public result as a nonexistent ID; reveal no content or existence signal. Future sharing may expose only notes A explicitly shared with B; sharing is outside this slice. |
| Actor is absent or malformed | Fail closed before a query; never substitute a default account. Require real authentication before enabling a notes route. |
| Request contains a different `user_id` | It cannot select, create, or reveal another owner’s data. Scope comes from trusted authentication, not request input. |
| A pooled connection is reused for B | B sees only B’s records; A’s transaction identity does not remain active. |
| Database failure or private sentinel occurs | Return a safe generic error; no traceback, connection detail, note content, or private sentinel in output/log evidence. |
| No authenticated actor source exists | No public notes route is enabled. Synthetic actor coverage is labelled as internal boundary testing only. |

### Acceptance criteria

```gherkin
Scenario: Signed-in user sees their active notes in edit order
  Given trusted actor A has active notes and a trashed note
  When A opens the notes list
  Then only active notes owned by A are shown
  And each row shows its stored title, or the first 175 weighted body units when untitled
  And each row shows its last-updated time
  And notes are sorted newest edit first with a stable ID tie-breaker

Scenario: Another signed-in account sees its own notes only
  Given actors A and B each have a private note
  When B opens the notes list
  Then B's note is shown
  And A's private note is absent

Scenario: A guessed foreign note ID does not disclose a record
  Given actor B knows actor A's note ID
  When B requests that note
  Then the result matches a nonexistent note
  And no note content or existence signal is returned

Scenario: Explicit sharing grants access only to shared notes
  Given actor A explicitly shares one note with actor B
  And actor A has another private note
  When B accesses notes shared with B
  Then only the explicitly shared note is visible to B
  And A's other private note remains inaccessible
  # Future sharing behavior; outside the Day 10 read-only implementation slice.

Scenario: Missing login identity fails closed
  Given the request has no trusted actor
  When the notes read path is invoked
  Then it fails before querying the database
  And no public or unauthenticated notes route is exposed

Scenario: Reused database connection does not reuse an actor
  Given one pooled connection handled actor A's transaction
  When that connection is used for actor B
  Then B sees only B's notes
  And A's transaction-local actor setting has ended
```

## 4. Implement the narrow path and focused checks — 90 min

- [ ] Review and explain the assistant-authored internal repository draft in `app/notes_repository.py` (60 min). Written/refactored at the learner’s request October 23; full local suite passed October 24, but learner review remains open. The learner correctly explained why actor identity must be trusted, why the query also filters by owner, and when the transaction-local setting ends; review the body-preview behavior added afterward too. Check the read-only transaction, active-notes view, selected fields, 175-weighted-unit title fallback and stable ordering. No route is wired; no authentication is claimed. If the code is unclear or wrong, learner revises it before proceeding.
- [ ] Review the assistant-authored focused tests and run them (30 min). Written at the learner’s request October 23 and extended October 24 with malformed-actor rejection and two-actor reuse of one mocked connection. October 24 focused run: 208 tests passed in 0.39s. Opt-in PostgreSQL suite: 383 tests passed in 143.40s using synthetic data and rollback. Latest full guarded suite: 1,201 Python tests +3 subtests; 821/821 cases demonstrated and 314/314 applicable faults detected; all required stages, cleanup, and source preservation passed. The reuse case checks transaction-local actor and owner UUID arguments on both mocked calls; it does not prove PostgreSQL pool reset. The 383 database tests exercise database rules but do not invoke this repository. Database case F071 separately checks that the synthetic app role sees only its actor’s rows. This list-only slice has no fetch-by-ID, so guessed foreign-ID versus nonexistent-ID behavior is not applicable. Learner review remains open. Synthetic UUIDs do not prove authentication. Evidence: `docs/testing/day-ten-test-pass-review.md`; local runs only, not hosted exact-commit CI.

📚 Learn first: [Psycopg transaction contexts](https://www.psycopg.org/psycopg3/docs/basic/transactions.html), scoped commit/rollback and connection lifecycle; [input rules](../architecture/users-notes-design.md), 175 weighted title units and emoji/grapheme behavior.
↩ Return: run `.venv/bin/python -m pytest -q tests/test_notes_repository.py tests/test_note_rules_and_maintenance.py`, then run `.venv/bin/python tools/run_test_suite.py`. Record actual results. If the isolated database gate is available, run `MERLIN_RUN_DB_TESTS=1 .venv/bin/python -m pytest -q tests/test_users_notes_database.py`; this current suite validates database rules but not yet the new repository on a real pooled connection. If there is no trustworthy identity source, stop before connecting a route; document the internal-only result or carry it forward.

## 5. Prove test effectiveness and retained CI — 55 min

- [x] Inject isolated faults that omit the owner predicate, accept a malformed actor, bind a hardcoded owner instead of the current actor, leave an actor setting session-wide, or distinguish guessed foreign IDs from nonexistent IDs if a fetch-by-ID operation is later selected (15 min). The four applicable faults were detected at their validator-pinned test checks: `notes-owner-filter-removed`, `notes-malformed-actor-accepted`, `notes-owner-parameter-hardcoded`, and `notes-actor-setting-session-wide`. Fetch-by-ID concealment is inapplicable to this list-only slice. Evidence: `docs/testing/full-suite-case-fault-matrix.json` and `docs/testing/full-suite-case-fault-review.md`.
- [ ] Integrate the retained cases and faults into the inventory/result validators, then run the complete guarded suite and exact-revision hosted workflow required by the project (30 min). **Local portion complete:** cases and faults are in the inventory and witness validator; the fresh CI-entry rehearsal passed all three steps in 91.826s with the uncommitted Day 10 changes included. Its nested full suite passed in 59.125s under the 60s gate; all 11 MER-11 faults have pinned witnesses. Exact-revision hosted workflow remains pending until the combined code/document revision is pushed. Preserve every earlier Day 1–9 case, fault, migration gate, and cleanup control. Do not mark this item complete until the current revision has a passing hosted run.
- [x] Verify test-resource ownership and cleanup; preserve all existing protected volumes, services, model files, and credentials (10 min). The guarded suite used its private `/tmp` sandbox, passed ownership/isolation controls, removed only manifest-owned disposable resources, and reported cleanup and protected-source preservation PASS. No user content or credentials were used as fixtures. Summary: `/tmp/merlin-day10-ci-entry-20261024-r8/suite/summary.json`.

📚 Learn first: [pytest monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html), scoped fault isolation; [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html), setup and cleanup.
↩ Return: report each case/fault ID and its actual outcome, the full-suite runtime, exact hosted SHA/run, and cleanup result. Assistant-run local suite passed under the enforced 60-second cap at 55.43s, 56.183s, 58.477s, and 59.125s; the final 91.826s fresh CI-entry rehearsal passed all three steps, cleanup and source preservation. Hosted exact-revision CI remains open until publication; learner review remains open. The list-only slice has no foreign-ID fetch behavior to test. A shared mutation kill or setup failure does not prove a case effective.

## 6. Review, explain and hand off — 30 min

- [x] Review the diff and logs for secrets, private note content, owner-ID leakage, and unrelated scope (10 min). Assistant reviewed all changed/untracked code, tests, CI inputs and evidence; fixtures use synthetic records. A high-signal scan of 24 changed files found no credential candidates or private-note fixtures; `git diff --check` passed. Changes remain scoped to Day 10 and cumulative test/CI evidence. Learner may still review the same diff before publication.
- [ ] Learner explain-back: explain trusted-identity source, owner filter, RLS role limits, and connection reuse risk from memory (10 min). Earlier answers already cover trusted authentication, explicit owner filtering and transaction-local scope. Explain remaining RLS role limits, reuse risk, mock limits, and unimplemented list-sharing/fetch/auth behavior; assistant must review your words without supplying the answer first.
- [x] Write the Day 10 handoff with learner/assistant authorship, actual minutes or unknown, test/fault/CI evidence, first failure, open identity prerequisite, and exact next step (10 min). See `docs/planning/day-ten-handoff.md`; actual minutes remain unknown.

📚 Learn first: [Git diff review](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository), inspect the staged and unstaged scope.
↩ Return: read `docs/planning/day-ten-handoff.md`, then explain the four identity/ownership points above in your own words. Commit and push only after code, evidence and handoff are final; check hosted CI for that exact combined revision. Do not claim authenticated notes, production security, or completed ownership merely from synthetic actors or database-only checks.

## Budget and completion rule

The hard cap is **300 minutes**: 35 + 45 + 45 + 90 + 55 + 30. No invisible setup/CI time, stretch work, DSA, AWS, broad CRUD, UI, or migrations are added. Unfinished work replaces later feature scope.

Complete this checklist only for the slice actually proved. If no trusted identity exists, public/API access remains blocked and the issue must record that limit. Passing tests do not prove that login/authentication exists, that every database role is safe, or that all possible disclosure paths are absent.

Official documentation links checked October 23, 2026. The PostgreSQL 17 row-security/SET pages, Psycopg transaction page, and pytest monkeypatch/fixture documentation were reviewed; current installed versions still govern execution.
