# Day 6 current migration rule review — October 8, 2026

**Historical comparison before restoration.** The subsequent authorized SQL edit restored email, title/body, blank-row checks, deadlines/cleanup and latest-edit indexes. Read the current design section for active status. Weighted Unicode enforcement, scheduler and backend rules remain pending.

Read-only comparison of `migrations/001_users_notes.up.sql` against the learner’s recorded decisions in `docs/architecture/users-notes-design.md`. Nothing was applied or tested in PostgreSQL.

## Why title and body disappeared

The later rewrite request explicitly specified Notes with `content TEXT`, alongside username-based Users. The assistant treated that list as a replacement schema and removed the earlier title/body/email/deadline fields. The request did not explicitly withdraw those product rules. Treating the omissions as cancellation was too broad: the current migration does not satisfy all recorded requirements.

UUIDv4 is the latest approved ID choice. Keep it for both tables. The UUID change itself did not remove title or body.

## Comparison

| Recorded requirement | Current migration evidence | Result |
|---|---|---|
| Permanent independent UUIDv4 IDs | Native defaults, primary keys, version/variant checks and update guard | Present, untested |
| Required existing owner; delete notes with account; forbid owner transfer | NOT NULL foreign key, ON DELETE CASCADE and update guard | Present, untested; other saved-data deletion and confirmation UI remain future work |
| Lowercase unique username, canonical lookup | Format check, UNIQUE, generated lowercase canonical and index | Present, untested; canonical is not a moderation/blocklist implementation |
| Optional email, original display casing, lowercase uniqueness, reject blank/padded storage | No email field or corresponding constraints/index | Missing |
| Optional title, blank title becomes absent, duplicate titles permitted | No title field | Missing |
| Body preserves whitespace; empty allowed subject to lifecycle | content holds text and allows empty values | Partial replacement; no agreed blankness/lifecycle enforcement |
| Title 175 and body 7,000 weighted characters; emoji 4, other characters 1 | No weighted validation | Missing; verified Unicode segmentation/classification still needed |
| Fully blank explicit save deletes; saved table rejects fully blank rows | Empty content accepted; no content CHECK | Missing; save deletion belongs in backend, rejection can be a database constraint |
| Title-only note expires 24 hours after first save; content cancels deadline; clearing content restarts it; repeated blank saves do not extend it | No deadline, deadline trigger or cleanup function | Missing; scheduled execution also needs a separate worker |
| Blank draft survives tab switch; cleanup after 10 minutes away, rechecking other-device activity | No editor/draft mechanism | Future application work, not provided by a migration |
| Device-reported creation/edit times, creation stable, initial update equals creation | Server timestamps override inserts/updates; optional device_edited_at only | Changed policy; device creation is not stored separately and no-op updates change updated_at |
| Owner timeline by latest update with note-ID tie-breaker | Index on user_id and created_at DESC | Different query; earlier update-time index absent; accessed-time tracking also absent |
| Private notes; authenticated identity determines owner | Owner RLS policies depend on backend-set actor | Conditional foundation only; trusted authentication and limited-role grants/tests absent; administrators bypass RLS |
| Linking, phone/social login, password authentication, session revocation, abuse/rate limits, sharing and fonts | Not implemented | Future application scope; do not claim migration implements them |
| Rollback/reapplication and expected acceptance results | No database execution evidence; down migration deferred | Pending |

## Exact next action

Restore the earlier email/title/body design as the target specification while keeping the approved UUIDv4 and username/canonical additions. Before editing SQL, reconcile device display timestamps with server timestamps and retain the approved update-time timeline requirement. Then restore constraints and the title-only deadline mechanism in the unapplied draft. Weighted validation and scheduled execution must remain explicitly pending until compatible tooling and execution are verified. Do not apply the current draft as though all rules are covered.

Keep the 360-minute Day 6 cap. Unfinished work displaces later feature time. Preserve Sprint 0 storage. No database changes, commit, push or upload occurred in this review.

📚 Learn first: [Recorded Users/Notes rules](../users-notes-design.md). This is a local specification comparison, not a new external documentation verification.
↩ Return: reconcile the schema before migration execution.
