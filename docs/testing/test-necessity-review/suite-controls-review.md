# Every runner and infrastructure control

Current named infrastructure controls: 128. Every retained control passed.

| Group | Control | Decision | Why |
|---|---|---|---|
| coordinator | pass | KEEP | Baseline-first ordering, independent lane overlap, target routing, all stages and cleanup succeed. |
| coordinator | serial | KEEP | Fallback executes database stages serially without sandbox-target inheritance. |
| coordinator | failure | KEEP | Zero process exit with rejected evidence must fail the stage and leave dependent work pending. |
| coordinator | setup-failure | KEEP | Failed copy creation must stop database faults and final gates. |
| coordinator | interrupt | KEEP | Real SIGINT must terminate every active child process and clean copy resources. |
| coordinator | preflight-pass | KEEP | All eight prerequisites run; only independent groups overlap. |
| coordinator | preflight-failure | KEEP | Nonzero prerequisite exit prevents baselines and suppresses private error text. |
| coordinator | preflight-timeout | KEEP | Timed-out prerequisite prevents baseline execution; cannot become success. |
| native transport | native_equivalence_0 | KEEP | Quoted semicolons, doubled quotes, NULL and scalar output match psql. Independent native_expected control now verifies status/output as well. Independent native_expected control now verifies status/output as well. Independent native_expected control now verifies status/output as well. Independent native_expected control now verifies status/output as well. |
| native transport | native_equivalence_1 | KEEP | ON_ERROR_STOP stops after division-by-zero and preserves diagnostic equivalence. Independent native_expected control now verifies status/output as well. Independent native_expected control now verifies status/output as well. Independent native_expected control now verifies status/output as well. Independent native_expected control now verifies status/output as well. |
| native transport | native_equivalence_2 | KEEP | AUTOCOMMIT directive and explicit transaction match direct psql. Independent native_expected control now verifies status/output as well. Independent native_expected control now verifies status/output as well. Independent native_expected control now verifies status/output as well. Independent native_expected control now verifies status/output as well. |
| native transport | native_equivalence_3 | KEEP | SET LOCAL state and rollback match psql. Independent native_expected control now verifies status/output as well. Independent native_expected control now verifies status/output as well. Independent native_expected control now verifies status/output as well. Independent native_expected control now verifies status/output as well. |
| native transport | large_script_complete | KEEP | A 400KB input with delayed server output must not be truncated across communicate retries. |
| native transport | fresh_connection | KEEP | Both calls must succeed with positive numeric backend IDs that differ. Previously differing error/success output could pass; repaired. |
| native transport | timeout_raised | KEEP | A real sleeping PostgreSQL query must raise the configured client timeout. |
| native transport | timeout_connection_closed | KEEP | Timed-out server session must disappear; a client exception alone does not prove server cancellation. |
| native transport | wrong_container_rejected | KEEP | Refuse nonmatching container identity before transport execution. |
| native transport | interrupt_connection_closed | KEEP | SIGINT must close the running query and return a failed child status. |
| native transport | preserved | KEEP | Identity, fingerprint and empty tables must match before and after transport controls. |
| terminal isolation | fork-probe | KEEP | Real controlling-terminal input must become EOF in fork workers, including import-time prompts. |
| terminal isolation | subprocess-probe | KEEP | The subprocess fallback must also detach from terminal input. |
| terminal isolation | stdin-isolated | KEEP | Independent input() regression proves ordinary workers cannot inherit interactive stdin. |
| terminal isolation | real-timeout | KEEP | A real sleeping worker must time out, never be classified as a detection. |
| database isolation | route-sql | KEEP | Queries reach the SQL physical copy, not the source or another lane. |
| database isolation | route-lifecycle | KEEP | Committed lifecycle queries reach their separate physical copy. |
| database isolation | route-migration | KEEP | Destructive migration queries reach their separate physical copy. |
| database isolation | cpu-limit-changed | KEEP | Reject unexpected CPU allocation before destructive test work. |
| database isolation | memory-limit-changed | KEEP | Reject unexpected memory allocation. |
| database isolation | external-network-refused | KEEP | Reject network-accessible copy metadata. |
| database isolation | shared-source-volume-refused | KEEP | Reject a source-mounted volume independently of path checks. |
| database isolation | published-port-refused | KEEP | Reject published host ports independently of network mode. |
| database isolation | stale-desktop-port-refused | KEEP | Reject inherited Desktop forwarding metadata. |
| database isolation | source-as-clone | KEEP | Refuse treating the source container as a disposable clone. |
| database isolation | source-volume-path | KEEP | Refuse the original PostgreSQL data path. |
| database isolation | wrong-source | KEEP | Refuse a manifest owned by another source identity. |
| database isolation | wrong-container | KEEP | Refuse nonexistent/mismatching target container identity. |
| database isolation | crossed-socket | KEEP | Refuse another lane socket, preserving storage/socket ownership. |
| database isolation | wrong-fingerprint | KEEP | A valid-looking target with wrong schema fingerprint must never fall back to source. |
| database isolation | public-manifest-refused | KEEP | Manifest must remain private and owned by the current user. |
| database isolation | manifest-symlink-refused | KEEP | Open manifests without following symlinks. |
| database isolation | changed-runtime-content-invalidates-cache | KEEP | Content hash must change when a dependency file changes; this is a hash-unit control, not image-corruption end-to-end proof. |
| database isolation | missing-runtime-file-refused | KEEP | Missing dependency code must prevent runtime hash reuse. |
| database isolation | live-fault-isolated-from-other-copies-and-source | KEEP | A real faulty SQL function in one copy must not affect either other copy or source. |
| database isolation | control-fault-rolled-back | KEEP | The deliberately faulty function must be restored after its transaction. |
| preflight invocation | scheduling | KEEP | Execute the eight coordinator controls before baselines. |
| preflight invocation | native | KEEP | Execute eleven transport controls, with real PostgreSQL cancellation. |
| preflight invocation | imports | KEEP | Required Python modules import and interpreter is Python3.12; does not verify every installed package version. |
| preflight invocation | node | KEEP | Node major version24 is required; does not promise a particular patch version. |
| preflight invocation | transport | KEEP | Reusable SQL transport starts under the target identity/fingerprint guard. |
| preflight invocation | preservation | KEEP | Original target is the isolated Day6 cluster with empty user/note tables. |
| preflight invocation | browser | KEEP | Pinned Playwright1.58.2 and Chromium145.0.7632.6 actually launch; no product compilation here. |
| preflight invocation | python-isolation | KEEP | Execute all four real controlling-terminal worker checks. |
| legacy repeated fault | emoji-weight-one | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | codepoint-instead-of-grapheme | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | title-bound-relaxed | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | title-bound-too-strict | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | body-bound-relaxed | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | body-bound-too-strict | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | body-stripped | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | real-title-stripped | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | email-lowercased | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | blank-title-stored-empty | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | draft-delete-protection-removed | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | nul-check-removed | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | target-check-skipped | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | identity-or-changed-to-and | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | target-port-original-db | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | batch1001-allowed | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | lock-timeout-removed | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | wrong-expiry-function | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | once-flag-ignored | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | custom-interval-ignored | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | cli-error-secret-leaked | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | strict-batch-guard-removed | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | strict-draft-guard-removed | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | utf8-guard-removed | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | unexpected-extra-sql | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | email-padding-retained | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | optional-email-empty-string | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | empty-email-empty-string | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | none-body-not-normalized | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | draft-title-bypasses-limit | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | draft-body-bypasses-limit | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | save-default-is-draft | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | text-type-guard-disabled | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | valid-unicode-rejected-ascii | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | nul-only-at-start | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | valid-body-erased | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | valid-title-erased | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | blank-save-never-deletes | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | target-host-public | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | target-database-original | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | target-user-original | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | connection-timeout-unbounded | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | batch-zero-allowed | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | batch1000-rejected | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | statement-timeout-removed | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | purge-parameter-altered | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | cleanup-counts-swapped | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | early-explicit-commit | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | default-interval-altered | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | nine-second-interval-allowed | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | ten-second-interval-rejected | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | runtime-error-not-sanitized | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | output-counts-swapped | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | interrupt-message-omitted | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| legacy repeated fault | nul-error-echoes-input | MERGE | Exact implementation is retained in the canonical per-case Python audit; remove its second mandatory execution, not the fault or baseline. |
| stage | python-tests | KEEP | Independent unmodified Python and direct PostgreSQL baselines must pass before faults. |
| stage | quiz-tests | KEEP | Independent unmodified offline JavaScript baseline must pass before faults. |
| stage | legacy-python-faults | MERGE | All55 literal fault transformations already run in the canonical Python audit. |
| stage | python-case-faults | KEEP | Canonical per-case Python sensitivity, selected dependency scopes and invalid diagnostics. |
| stage | database-case-faults | KEEP | Stored SQL constraints, triggers, role boundaries, worker behavior and reconnect verification. |
| stage | timestamp-case-faults | MERGE | F077 and its same recipes already run in the complete SQL audit; keep --only F077 for focused debugging. |
| stage | quiz-case-faults | KEEP | Pure scoring/cache-logic fault checks complement real browser behavior. |
| stage | browser-case-faults | KEEP | Real DOM, event, storage, reload and retry behavior with paired faulty HTML. |
| stage | database-lifecycle-faults | KEEP | Committed state and two-session locks cannot be proven by rollback-only cases or mocks. |
| stage | migration-undo-faults | KEEP | Undo/reapply, refusal gates, locks and damage repair stay in disposable storage. |
| stage | documentation | KEEP | Validate learning/return/navigation links and authored Part contracts. |
| stage | whitespace | KEEP | Reject accidental patch whitespace defects; not an application behavior test. |
| integrated guard | assertions-enabled | KEEP | Refuse optimized Python, because result gates use assertions. |
| integrated guard | suite-lock | KEEP | Reject simultaneous full runners using a no-follow lock and nonblocking flock. |
| integrated guard | output-directory | KEEP | Refuse reusing a nonempty result folder; old evidence cannot masquerade as this run. |
| integrated guard | environment-sanitization | KEEP | Remove inherited pytest filters and sandbox targeting; enable all database tests. |
| integrated guard | fresh-backup | KEEP | Always take and verify a new physical backup; database contents/results are never cached. |
| integrated guard | source-tablespaces | KEEP | Refuse custom tablespaces before backup to avoid restoring original absolute paths. |
| integrated guard | runtime-source-digest | KEEP | Verify source dependency file content and image provenance; verify again in every clone. |
| integrated guard | manifest-shape | KEEP | Validate exact manifest fields and lane paths before publishing private targets. |
| integrated guard | owned-cleanup | KEEP | Inventory per-run labels and verify each container/volume ownership before removal. |
| integrated guard | post-cleanup-source | KEEP | Original identity/fingerprint/empty target must be preserved after all destructive work. |
| integrated guard | SQL-request-reset | KEEP | Every reusable request must rollback and discard session state; startup/requests enforce target identity. |
| integrated guard | complete-report-inventory | KEEP | Reports must contain every reviewed case/fault/pair exactly once; previous validators accepted six fabricated truncated reports. |
| integrated guard | baseline-fault-consistency | KEEP | Do not accept effectiveness labels when underlying baseline or mutation outcomes contradict them. |
| integrated guard | no-foreign-error-leak | KEEP | Runner prerequisite errors omit private captured output. |
| native expected result | native_expected_0 | KEEP | Independent expected status/output prevents two identically broken transports from passing the equivalence oracle. |
| native expected result | native_expected_1 | KEEP | Independent expected status/output prevents two identically broken transports from passing the equivalence oracle. |
| native expected result | native_expected_2 | KEEP | Independent expected status/output prevents two identically broken transports from passing the equivalence oracle. |
| native expected result | native_expected_3 | KEEP | Independent expected status/output prevents two identically broken transports from passing the equivalence oracle. |
| SQL boundary lexer | lexer-quoted-semicolon | KEEP | Preserve the named SQL string/comment statement boundary or reject its unterminated form before execution. |
| SQL boundary lexer | lexer-doubled-string-quote | KEEP | Preserve the named SQL string/comment statement boundary or reject its unterminated form before execution. |
| SQL boundary lexer | lexer-quoted-identifier | KEEP | Preserve the named SQL string/comment statement boundary or reject its unterminated form before execution. |
| SQL boundary lexer | lexer-nested-block-comment | KEEP | Preserve the named SQL string/comment statement boundary or reject its unterminated form before execution. |
| SQL boundary lexer | lexer-line-comment | KEEP | Preserve the named SQL string/comment statement boundary or reject its unterminated form before execution. |
| SQL boundary lexer | lexer-dollar-body | KEEP | Preserve the named SQL string/comment statement boundary or reject its unterminated form before execution. |
| SQL boundary lexer | lexer-tagged-dollar-body | KEEP | Preserve the named SQL string/comment statement boundary or reject its unterminated form before execution. |
| SQL boundary lexer | lexer-escaped-string | KEEP | Preserve the named SQL string/comment statement boundary or reject its unterminated form before execution. |
| SQL boundary lexer | lexer-unterminated-string | KEEP | Preserve the named SQL string/comment statement boundary or reject its unterminated form before execution. |
| SQL boundary lexer | lexer-unterminated-identifier | KEEP | Preserve the named SQL string/comment statement boundary or reject its unterminated form before execution. |
| SQL boundary lexer | lexer-unterminated-dollar | KEEP | Preserve the named SQL string/comment statement boundary or reject its unterminated form before execution. |
| SQL boundary lexer | lexer-unterminated-block-comment | KEEP | Preserve the named SQL string/comment statement boundary or reject its unterminated form before execution. |
| coordinator lifecycle | baseline-failure | KEEP | Join asynchronous copy setup, preserve the first blocker and clean owned resources without starting faults after this failure/interrupt. |
| coordinator lifecycle | interrupt-setup | KEEP | Join asynchronous copy setup, preserve the first blocker and clean owned resources without starting faults after this failure/interrupt. |
| coordinator lifecycle | prerequisite-failure | KEEP | Join asynchronous copy setup, preserve the first blocker and clean owned resources without starting faults after this failure/interrupt. |
| result-validator counterfactual | migration-undo-faults-complete-positive | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | migration-undo-faults-contradictory-schema | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | migration-undo-faults-contradictory-runtime | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | migration-undo-faults-wrong-target | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | migration-undo-faults-missing-source | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | migration-undo-faults-false-validation | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | migration-undo-faults-malformed-schema-digest | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | migration-undo-faults-wrong-replay-count | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | migration-undo-faults-wrong-replay-mode | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | migration-undo-faults-missing-branch | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | legacy-python-faults-complete-positive | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | legacy-python-faults-truncated | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | legacy-python-faults-duplicate | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | python-case-faults-complete-positive | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | python-case-faults-truncated | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | python-case-faults-duplicate | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | python-case-faults-missing-fault | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | python-case-faults-missing-source-manifest | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | python-case-faults-contradictory-baseline | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | python-case-faults-missing-scope-proof | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | python-case-faults-invented-detection | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | database-case-faults-complete-positive | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | database-case-faults-truncated | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | database-case-faults-duplicate | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | database-case-faults-missing-source-manifest | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | database-case-faults-contradictory-preservation | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | database-case-faults-missing-pair | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | quiz-case-faults-complete-positive | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | quiz-case-faults-truncated | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | quiz-case-faults-duplicate | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | quiz-case-faults-missing-fault | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | quiz-case-faults-missing-source-manifest | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | quiz-case-faults-contradictory-baseline | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | quiz-case-faults-invented-detection | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | browser-case-faults-complete-positive | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | browser-case-faults-truncated | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | browser-case-faults-duplicate | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | browser-case-faults-missing-source-manifest | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | browser-case-faults-contradictory-mutation | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | database-lifecycle-faults-complete-positive | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | database-lifecycle-faults-truncated | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | database-lifecycle-faults-duplicate | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| result-validator counterfactual | database-lifecycle-faults-contradictory-mutation | KEEP | The complete positive report is accepted; this specific omitted, duplicated, contradictory or wrongly targeted report is rejected by the real validator. |
| SQL shard proof | sql-shards-complete-positive | KEEP | The actual merger must accept the complete partition or refuse this exact missing/duplicated/crossed/wrongly targeted/unpreserved evidence or invalid selector before database transport. |
| SQL shard proof | sql-shards-missing-case | KEEP | The actual merger must accept the complete partition or refuse this exact missing/duplicated/crossed/wrongly targeted/unpreserved evidence or invalid selector before database transport. |
| SQL shard proof | sql-shards-duplicate-case | KEEP | The actual merger must accept the complete partition or refuse this exact missing/duplicated/crossed/wrongly targeted/unpreserved evidence or invalid selector before database transport. |
| SQL shard proof | sql-shards-crossed-case | KEEP | The actual merger must accept the complete partition or refuse this exact missing/duplicated/crossed/wrongly targeted/unpreserved evidence or invalid selector before database transport. |
| SQL shard proof | sql-shards-wrong-index | KEEP | The actual merger must accept the complete partition or refuse this exact missing/duplicated/crossed/wrongly targeted/unpreserved evidence or invalid selector before database transport. |
| SQL shard proof | sql-shards-wrong-source | KEEP | The actual merger must accept the complete partition or refuse this exact missing/duplicated/crossed/wrongly targeted/unpreserved evidence or invalid selector before database transport. |
| SQL shard proof | sql-shards-false-preservation | KEEP | The actual merger must accept the complete partition or refuse this exact missing/duplicated/crossed/wrongly targeted/unpreserved evidence or invalid selector before database transport. |
| SQL shard proof | sql-shards-wrong-fingerprint | KEEP | The actual merger must accept the complete partition or refuse this exact missing/duplicated/crossed/wrongly targeted/unpreserved evidence or invalid selector before database transport. |
| SQL shard proof | sql-shards-duplicate-target | KEEP | The actual merger must accept the complete partition or refuse this exact missing/duplicated/crossed/wrongly targeted/unpreserved evidence or invalid selector before database transport. |
| SQL shard proof | sql-shards-missing-shard | KEEP | The actual merger must accept the complete partition or refuse this exact missing/duplicated/crossed/wrongly targeted/unpreserved evidence or invalid selector before database transport. |
| SQL shard proof | sql-shards-refuse-2/2 | KEEP | The actual merger must accept the complete partition or refuse this exact missing/duplicated/crossed/wrongly targeted/unpreserved evidence or invalid selector before database transport. |
| SQL shard proof | sql-shards-refuse--1/2 | KEEP | The actual merger must accept the complete partition or refuse this exact missing/duplicated/crossed/wrongly targeted/unpreserved evidence or invalid selector before database transport. |
| SQL shard proof | sql-shards-refuse-0/0 | KEEP | The actual merger must accept the complete partition or refuse this exact missing/duplicated/crossed/wrongly targeted/unpreserved evidence or invalid selector before database transport. |
| SQL shard proof | sql-shards-refuse-x/2 | KEEP | The actual merger must accept the complete partition or refuse this exact missing/duplicated/crossed/wrongly targeted/unpreserved evidence or invalid selector before database transport. |
| SQL shard proof | sql-shards-refuse-partial-filter | KEEP | The actual merger must accept the complete partition or refuse this exact missing/duplicated/crossed/wrongly targeted/unpreserved evidence or invalid selector before database transport. |
| independent target route | route-sql-second | KEEP | Extra SQL target must route to its own verified private data directory; live faulty SQL cannot affect this copy. |
| SQL parent shard gate | sql-parent-shards-complete-positive | KEEP | The real parent validator must accept complete partition reports and refuse contradictory merged proof, changed child outcomes, missing child report, wrong source or reused target. |
| SQL parent shard gate | sql-parent-shards-contradictory-merged-proof | KEEP | The real parent validator must accept complete partition reports and refuse contradictory merged proof, changed child outcomes, missing child report, wrong source or reused target. |
| SQL parent shard gate | sql-parent-shards-changed-child-outcome | KEEP | The real parent validator must accept complete partition reports and refuse contradictory merged proof, changed child outcomes, missing child report, wrong source or reused target. |
| SQL parent shard gate | sql-parent-shards-missing-child | KEEP | The real parent validator must accept complete partition reports and refuse contradictory merged proof, changed child outcomes, missing child report, wrong source or reused target. |
| SQL parent shard gate | sql-parent-shards-wrong-child-source | KEEP | The real parent validator must accept complete partition reports and refuse contradictory merged proof, changed child outcomes, missing child report, wrong source or reused target. |
| SQL parent shard gate | sql-parent-shards-crossed-target | KEEP | The real parent validator must accept complete partition reports and refuse contradictory merged proof, changed child outcomes, missing child report, wrong source or reused target. |
