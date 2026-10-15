# Documentation and publication security review

Review date: October 14, 2026. Requested scope: material already committed and currently being worked on, including documentation and compressed evidence. No files were uploaded, pushed or published by this review.

## Observed results

| Check | Result |
|---|---|
| Current tracked files plus non-ignored untracked files | 322 files scanned at the initial snapshot; no matching secrets found. |
| Git history reachable from all local refs | 390 historical file blobs scanned; no matching secrets found. This includes the Day 6 commit and older reachable versions. |
| Compressed evidence | 74 gzip streams expanded across current/history snapshots, including two archive occurrences and their individual members. Archive contents were read without extracting them into the repository. |
| Total scanned objects, including archive members | 732. Repeated current/history content is deliberately included. |
| Known local private values | Compared against private credential values from local environment/authentication files without displaying or recording those values. No matches found in publication targets. |
| Recognizable secret patterns | Checked private-key headers, provider/GitHub key formats, AWS access-key formats, JWT-like tokens and credential-bearing URLs. No matches found. |
| Tracked private files | No actual environment file, Codex auth file, gateway key file or PEM/P12/PFX key file tracked. `.env.example` contains a blank password and configuration examples. |
| Tracked screenshots/images | None found requiring visual review. |
| Generic sensitive-path examples | Kept `GET /.env`: this describes an attack input and required rejection, not a private file's contents. |

Earlier targeted assignment review identified environment-variable references and synthetic test values rather than actual credentials. Synthetic values in failure reports are necessary to demonstrate non-disclosure and must remain distinguishable from real credentials.

The first pattern scan found no live secret requiring removal or credential rotation. Subsequent contextual review identified actual personal account-security state and recovery-storage descriptions. These were removed from current documentation, archive members and affected local history at the learner's explicit request. The contract and AGENTS.md now require synthetic fixtures and prohibit publishing real secrets, sensitive configuration values or private file contents.

## What this result does and does not mean

This is an observed scan result, not a guarantee that every possible secret format can be recognized. It covers local Git refs and current publication-target files. Remote-only history, other repositories, ignored private files as publication targets, external screenshots and provider-side credential status are outside this review. Local account names, database identifiers, public Jira links and source-code fingerprints are not credentials; this review does not certify that all such metadata is suitable for every sharing context.

If a real credential is ever discovered in a committed version, removing it from the latest document does not invalidate the older version or revoke the credential. Record the finding without reproducing its value, revoke/rotate it with the relevant provider, and agree on any required history cleanup before publication. Local history handling for this review is recorded below.

## Day 7 test-design status

[The health API contract](../architecture/health-api-contract.md) now contains step 2.3: purpose-named implementation/test files, loopback fixture, operating-system-assigned test port, bounded waits, client closure, shutdown outside the serving thread, socket closure, thread join, fault restoration and restart checks.

Existing fault injections protect existing functionality. New API fault checks remain PENDING until the learner implements the endpoint and corresponding executable cases. The contract maps planned faults to API-01–07 and fixture safety checks; it does not claim existing audits already exercise this future API.

📚 Learn first: [the contract's fixture and cleanup plan](../architecture/health-api-contract.md), section 2.3; then [the existing suite command guide](test-suite-commands.md).
↩ Return: review the design, resolve the CI scope decision in Day 7 section 3, and implement the server yourself before claiming API tests or faults pass. Keep real secrets out of examples and evidence.

## Existing suite verification

Complete suite PASS: all 10 stages passed in 40.94 seconds. Python fault audit: 232 detected, zero survived/invalid/timeout/unapplied; three demonstrated aliases and four explicitly excluded invalid startup diagnostics remain separately recorded. SQL, JavaScript, browser, lifecycle and migration audits also passed their result gates. Disposable cleanup and source preservation passed. Durable result: [suite results](publication-review-suite-results.json). Documentation lint retains its existing one warning and 27 verify items; it checks 25 numbered Parts, not every document. The first sandboxed attempt stopped at the native PostgreSQL prerequisite, before functional stages; the retry uses approved Docker/socket access. Preserve this distinction rather than treating a prerequisite restriction as a detected application fault.

## Complete file review and authorized refactors

The follow-up review covered every tracked and non-ignored current project file, including hidden bundled skills, configuration, executable sources, dependency locks, JSON/CSV reports, compressed evidence and archive members. Generated evidence was processed in full with contextual candidate review; this is not a claim of manually reading each generated line. Installed dependencies, caches, Git internals and real ignored private environment files are not publication targets and were not rewritten.

The final snapshot includes 328 current files and 390 reachable historical blobs, with 74 compressed streams expanded. No matching live credential or known local private value was found; none of the 65 reviewed disclosure lines remain in reachable history. The [per-file inventory](publication-file-review.json) records the classification, content hash, review method and disposition of each file. Detailed source review covered all application, migration, quiz, test, tool and bundled executable files. The automated review also compared publication targets against known local private values without reporting those values. No matching live credential was found. Local usernames, public project links, loopback addresses, synthetic fixtures and database identity fingerprints were retained because they do not grant access; the fingerprints are required to prevent operations on the wrong database.

Removed material included personal account verification/authentication/recovery state and a credential-validation result. Generic MFA teaching, defensive request paths such as `GET /.env`, all learning links and storage-preservation evidence remain. Older archival instructions now require personal security evidence to stay private. The [archive preservation note](../setup/archive/README.md) explains why this historical reference is sanitized.

Code changes:

- Removed an unreachable SQL lexer branch and an identical repeated dependency-package assignment. Existing lexer and dependency-scope controls verify behavior preservation.
- Fixed the standalone committed migration verifier: only its outer schema inventory is unordered; nested index/ACL arrays retain their meaningful order. Before the fix, a counterexample with reversed index keys incorrectly compared equal. Seven independent controls now cover literal expected normalization, inventory-order equivalence, nested-order rejection, missing rows, changed owners, generated trigger names and boolean/OID distinction.
- Fixed the bundled compressor's repair retry so it preserves the initial privacy boundary: YAML frontmatter and preserved code stay local. Reordered or identical repeated blocks retain original identities and can still be repaired; the final validator remains in force. Raw external CLI failure output is replaced by a generic exception. Six no-network controls exercise a real validation retry, protected data exclusion/restoration, repair ordering and error non-disclosure. Remaining prose still goes to an external provider when the skill is explicitly invoked; do not use this tool on private documents.
- Updated the root README's outdated setup-only claim to describe the existing database foundation and test suite accurately. No new API feature was implemented.

Applied SQL files, ordinary case inventory and existing fault catalogues were preserved. Broad formatting changes were rejected where they would disrupt fault-source coordinates without a demonstrated benefit. Assistant changes were explicitly authorized by the learner; this does not authorize writing future features.

## Local Git history handling

After explicit learner approval, a private, mode-0600 bundle backup was created outside the repository. All 18 reachable local commits were examined. The rewrite sanitized 28 unique historical documentation/archive blobs with 138 exact redactions; 17 commits consequently received new IDs. Commit authors, dates, messages, parent structure and non-documentation source contents were preserved. Superseded reflog reachability and local unreachable objects were removed. No public backup ref was retained.

The Day 6 commit is now `4ca8cd83b7d4bd21249da6eac6b7c980c9224b88`; its message remains **Day 6 (Database foundation and test-suite verification) - Complete**. Local remote-tracking history was also sanitized so it cannot keep the superseded blobs reachable. This does not change the actual remote repository or claim its history is clean.

The remote was not contacted, pushed or rewritten. If older history is already published there, it remains there until a separately authorized remote cleanup. Fetching that old history can reintroduce removed local records. A normal push may reject the rewritten history; a guarded history update and coordination with any other clones are separate publication work. Do not silently force-push or claim this review removed external copies.

## Fresh verification after changes

The complete baseline passed in **43.12 seconds**. After changes, all ten suite stages passed in **40.32 seconds**. These are observations under current host load, not a guaranteed speed improvement. A final targeted rerun checked all **88 runner controls**, including the 13 new controls, after the last assertion-hardening edit.

The standalone verifier is outside the normal ten-stage suite, so it was run separately on disposable storage: **PASS**, nine checks, **383 rebuilt database cases**, **20.44 seconds**, source preservation and cleanup confirmed. Applied migration source bytes remained unchanged.

Three isolated counterfactuals reintroduced the private repair-prompt leak, raw CLI error leak and nested-array sorting defect. Each failed a corresponding assertion; no external inference request was made. Durable evidence is in [verification results](publication-refactor-verification.json) and [runner controls](publication-refactor-controls.json). API implementation and API fault execution remain PENDING.
