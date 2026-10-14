# Second-pass SQL necessity review

Reviewed 2026-10-12. No database commands or fresh experiments ran.

Two pairs of baseline scripts were exactly equal, including fixture preparation, role, input, count and row-state assertions:

| Removed duplicate ID | Canonical retained ID | Preserved mutations |
|---|---|---|
| sql-valid-batch-cleanup_expired_blank_notes-1 | expiry-batch-one | Remove batch LIMIT; reverse oldest-row ordering |
| sql-valid-batch-purge_deleted_notes-1 | purge-batch-one | Remove batch LIMIT; reverse oldest-row ordering |

Canonical scripts remain unchanged. The complete prior mutation-pair inventory equals the new inventory after mapping these two aliases. No distinct fault implementation or assertion was removed. The new catalogue has 382 CASES plus reconnect, giving 383 SQL baselines and 607 fault pairs. Existing migration replay uses the current CASES catalogue, so it preserves the canonical assertions without replaying duplicate IDs.

F049-F050 now checks NULL email on the two users it explicitly inserts, extra/missing. Previously it checked seed a/b, whose emails the NULL-uniqueness mutant changes during preparation. Preparation alone could therefore falsify the old oracle without installing the defective index. The repaired oracle observes the intended operation.

Latest reviewed historical report contains 385 baselines and 607 pairs: 581 assertion detections, 26 behavior errors, zero survivals. These results precede these edits and do not prove the modified catalogue passes. Offline checks prove all other IDs remain, the exact duplicate assertions are retained under canonical IDs, and the full mutation union is preserved. Fresh suite validation is required.

Migration full-replay reduction remains conditional: both PUBLIC CREATE branches, rebuilds, permission assertions and schema comparisons must stay. The present fingerprint is not a complete equivalence proof for every column type/collation/runtime property, so this review did not remove the second replay. All five lifecycle cases and all negative migration safety checks remain unchanged. Same kill sets alone never establish Unicode-input redundancy.

## Backup preparation overlap

Preparing copies during source baselines is a reasonable optimization while retaining the current safeguards. Baseline fixtures roll back, and the actual second-write FK error closes its transaction before reconnect. PostgreSQL supports base backups of running clusters with concurrent clients and includes the necessary WAL when configured accordingly. This is documented in [PostgreSQL 17 pg_basebackup](https://www.postgresql.org/docs/17/app-pgbasebackup.html), verified 2026-10-12.

Keep the fresh backup, full manifest/checksum/WAL verification, runtime digest, empty-source/custom-tablespace refusal, private independent storage and network boundaries. Copy admission must still verify completed recovery, exact identity/data directory, zero rows, expected schema fingerprint, fsync, full_page_writes and synchronous_commit. [PostgreSQL 17 pg_verifybackup](https://www.postgresql.org/docs/17/app-pgverifybackup.html), verified 2026-10-12, explicitly requires real restoration checks in addition to backup verification.

No fault may start before both baselines finish. This includes live isolation-control faults, not only application mutation lanes. Join startup before cleanup on baseline failure, startup failure or interruption. Source references: tools/run_test_suite.py:389; tools/database_test_session.py:99; tools/database_sandboxes.py:62; tools/verify_database_sandboxes.py:114. No backup-overlap benchmark was performed by this reviewer.
