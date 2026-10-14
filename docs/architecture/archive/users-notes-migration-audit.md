# Historical Day 6 migration audit — October 8, 2026

Superseded by the later username/content rewrite. This audit describes the earlier email/title/body migration. See [current schema](../users-notes-design.md#current-schema--latest-explicit-rewrite-request) for active fields and prerequisites.

Compared the full [design](../users-notes-design.md), including its latest corrections, against [up.sql](../../../migrations/001_users_notes.up.sql). This is a source review only: no migration was applied, no PostgreSQL parser/execution check was run and no acceptance test passed. “Present” means SQL is written, not proven operational.

## Database and input rules

| Your rule | Current up.sql | Remaining work |
|---|---|---|
| Unique permanent Users ID | UUID primary key/default and immutable guard present | Design still says UUIDv7 proposed; migration uses UUIDv4. Align design; default does not enforce supplied UUID version. |
| Independent unique permanent Note ID | UUIDv4 default/primary key and immutable guard present | Cross-device persistence depends on later synchronization, not UUID alone. |
| Email optional; multiple users may lack it | Nullable field and unique lowercase index present | Login without email needs another verified method; not implemented. |
| Trim email; blank becomes NULL; preserve display casing | CHECK rejects blank/padded stored email; column preserves stored casing | Backend normalization is absent; database rejects bad input instead of converting it. Exact whitespace policy must match between layers. |
| Email unique regardless of casing | Lowercase unique expression index present | Test duplicate case variants and multiple NULLs. No email-format/ownership verification supplied. |
| Required creation timestamps with timezone support | TIMESTAMPTZ NOT NULL present | Validate explicit device offset before writing; PostgreSQL can accept input without an offset using its session timezone. |
| Creation time and note owner never change | BEFORE UPDATE guards present | Test each protected field; administrative users can disable guards. |
| Owner required and must exist | NOT NULL plus Users foreign key present | Existence is not authorization. |
| Deleting an account removes its notes | ON DELETE CASCADE present | Repeated warnings/confirmation are UI/backend work; deletion of all future data/backups requires separate policy. |
| Optional nonunique title; blank/whitespace becomes NULL | NULL allowed, whitespace-only non-NULL title rejected | Backend conversion remains absent. Duplicate titles are allowed. |
| Body optional to the user; stored empty text; preserve content whitespace | NOT NULL DEFAULT empty text; no content trimming | Omitted body defaults empty; explicitly supplied NULL is rejected. Backend maps missing input appropriately. |
| Title weighted length <=175 / body <=7000 | Comments only | **Missing enforcement**: emoji4/other visible character1. Choose exact Unicode segmentation/classification and compatible helper. |
| Fully blank notes are not saved | Content CHECK present with explicit NULL handling | Explicit save must delete existing blanked note/discard draft in backend; SQL currently rejects a blank update, not deletes it. |
| Title-only note expires after 24 hours; content cancels; clearing content restarts; repeated blank saves do not extend | Deadline field and trigger present | Test lifecycle branches; deadline is server-controlled. |
| Expired, still-blank-body notes deleted | Conditional cleanup function/index present; PUBLIC execution revoked | **Not scheduled**. Needs authorized worker, permissions and suitable RLS visibility. |
| Note update time initially equals creation | Timestamp trigger present | Test insertion. |
| Content edit sets current device time; no read-time changes; backward times allowed | Trigger preserves no-op/metadata time and accepts edit timestamp; reads do not fire it | **Partial**: omitted edit timestamp retains OLD value. Backend must supply fresh device instant; SQL cannot verify device provenance. |
| Find owner's notes newest-first with stable ties | Composite owner/update-desc/ID index present | Actual query and index-performance test absent. Last-accessed ordering needs additional future design. |
| Private owner-only access, trusted actor rather than submitted owner | ENABLE/FORCE RLS plus USING/WITH CHECK policies present | **Partial**: no authenticated backend, transaction-local identity setter, limited role/grants or bootstrap registration path. DB access can spoof merlin.actor_id. Superuser bypasses RLS. |
| Both database and backend enforce appropriate rules | Some SQL rules present | Backend remains absent; database definitions alone do not satisfy this requirement. |

## Editor and future product rules

These remain requirements, not missing columns to blindly add to this migration.

| Rule | Status / correct implementation location |
|---|---|
| Blank draft survives tab switch; delete after 10+ minutes away if still blank | Missing editor/draft lifecycle and cross-device activity recheck. No draft table/timer exists. |
| Show Month/Day/Year, AM/PM minute in device timezone; hide creation time unless properties opened | Future UI. Database stores instants, not display formatting or source timezone names. |
| Fonts/custom fonts and reasonable font sizes | Future UI; TEXT cannot enforce visual page size. |
| Sharing/collaboration, custom filters, last-accessed ordering | Deferred; current RLS is owner-only and no collaborator model exists. |
| Phone/Apple/Google and future sign-in methods; verified linking; no account maximum | Future authentication/identity tables. No linked provider identities exist. |
| Username/password, lowercase unique allowed usernames and moderation | Deferred; no username/password columns or hashing/authentication implementation. |
| Optional two-factor authentication and recovery/duplicate-account UI | Deferred; generic response decision still needs resolution. |
| Five-minute access tokens, refresh rotation, device storage and immediate revocation | Deferred; no token/session backend or storage configured. |
| Human-only registration, note rate limits, anti-abuse/DDoS protections | Missing backend/infrastructure controls; no zero-bot guarantee. |
| Cloud hosting | Preference only; no deployment. AWS remains deferred. |
| Multi-device synchronization and AI organization | Future backend/AI work; identity/indexes alone do not supply it. |

## Evidence still needed

All migration cases are unrun: valid/invalid inserts, uniqueness, foreign keys, whitespace cases, immutable guards, backward clock, deadline transitions/cleanup, rollback and committed persistence after reconnect. Limited-role cross-user denial remains pending. Weighted-limit boundary tests cannot pass until a validator exists. Down migration and disposable undo/reapplication are learner-deferred, not completed. Probe success was learner-reported, not a migration test.

## Document conflicts found

The design accumulated historical progress notes. Earlier “field absent,” “guards absent,” “permanent timer cancellation,” “countdown question pending” and “next write down” statements are superseded by later clarifications. The main Users row still proposes UUIDv7 while the current migration uses UUIDv4. Title-only retention is now one day; repeated blank saves keep the deadline, content cancels, and content-to-blank starts a new deadline. This audit is the current implementation-status map; historical notes must not be read as new blockers or passing evidence.

📚 Learn first: [Current SQL](../../../migrations/001_users_notes.up.sql) and [design](../users-notes-design.md); [PostgreSQL row security](https://www.postgresql.org/docs/17/ddl-rowsecurity.html), role bypass and policies (retrieved October 8).
↩ Return: first choose the exact weighted-counting tooling; then plan identity/limited-role verification and scheduler integration. Do not claim all rules implemented. No application/config/runtime changes made by this audit. Preserve Sprint 0 database; remaining work stays inside the 360-minute cap and displaces later features if unfinished.
