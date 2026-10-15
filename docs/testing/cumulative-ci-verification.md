# Cumulative CI implementation verification

The learner explicitly authorized AI implementation of the CI repair, followed by committing all reviewed changes and a guarded publication. The API remains unimplemented. Actual minutes are unknown. Day 7 section 3 allocates 15 minutes to the decision and swaps the remaining 50 minutes for the repair attempt; overrun is carried forward rather than hidden.

📚 Learn first: [workflow run history](https://docs.github.com/en/actions/how-tos/monitor-workflows/view-workflow-run-history), inspecting the commit and required jobs; [browser installation](https://playwright.dev/docs/browsers), matching the package and browser revision. Links verified October 14, 2026.
↩ Return: compare the exact published commit with its workflow run before declaring the new-day gate complete.

## What changed

The existing setup workflow retains its locked environments, doctor tests and synthetic service checks. It additionally installs locked Playwright dependencies, builds a pinned PostgreSQL runtime with PL/Python, and invokes `tools/run_ci.py`. Reports are restricted to synthetic verification artifacts.

`tools/ci_database.py` provisions a fresh, owned database with no network or published ports. Ownership, immutable image, volume and cluster identity checks precede writes and cleanup. Existing local databases and their guards remain intact. A disposable source copy substitutes only an explicit allowlist of local identity literals; source/executed hashes and reversible substitution checks establish that boundary. Tests run against original Python sources as well as the adapted complete suite. Committed migration undo/reapplication is an additional required verification.

## Actual local results

Final local execution on October 14 passed in **90.457 seconds**, including the original Python tests, complete ten-stage suite (**60.375 seconds**) and standalone committed migration roundtrip (**383 cases**, **20.415 seconds**). Cleanup passed. This cold CI-oriented run is distinct from the earlier approximately 40-second local suite configuration. It conservatively runs broader Python fault coverage after identity adaptation.

All retained cases and fault inventories remain required. The repair adds 47 CI controls; the runner verification now has 90 controls. Browser installation was repeated from the locked package into fresh storage. The pinned database image was built locally. These observations establish local execution, not hosted-runner success. The durable [local summary](cumulative-ci-results.json) identifies its base commit and explicitly marks uncommitted inputs.

First integration failure: Compose discovery did not recognize the fresh source because required ownership/discovery labels were absent. Fixed the labels and validated them. The next failure exposed a scheduler control expecting eight preflights after adding the ninth CI guard. Updated the exact inventory and added failure/timeout controls. Final execution passed; neither failed attempt was counted as successful coverage.

## Publication status

GitHub execution is **PENDING** until the reviewed changes are committed, published with the approved exact remote-tip lease, and the resulting workflow is observed. Do not fetch the older unsanitized history. Publication-file-review.json records the earlier publication audit snapshot; the CI additions require the final precommit scan as well.

The workflow uses read-only repository permissions and does not deploy. A successful finite suite does not establish universal security or implement future requirements. Cross-user API authorization remains pending an implemented ownership boundary.

## First hosted execution and compatibility repair

The first published run, [38665906998](https://github.com/vipravlipare/Merlin/actions/runs/38665906998), failed for commit `787af8a24d444b8d8bd0df69858f295eccd617ae`. Setup, browser provisioning and image build passed. Original Python sources passed, followed by the complete suite's ordinary Python/database and quiz baseline stages. The first failure was `database-isolation`: `Disposable Docker operation failed: commit`. CI cleanup and source preservation passed; subsequent fault stages were pending, not passed.

The runtime capture used `docker commit --no-pause`. That option exists in the local Docker CLI but not in the official Docker CLI v28 source. The first compatibility attempt used default pausing. Hosted execution exposed an intermittent first-query mismatch because runtime capture overlaps the native transport preflight on the same source. The final repair inspects Docker commit help and selects either `--pause=false` or `--no-pause`, preserving non-pausing capture. Unknown option sets fail closed. Three regressions exercise the actual runtime-preparation method for both CLI spellings and unsupported help; default pausing is rejected by these controls. Mounted database volumes remain excluded from image capture. Hosted re-execution is required to confirm the final fix.

📚 Learn first: [Docker commit](https://docs.docker.com/reference/cli/docker/container/commit/), default pausing and excluded mounted volumes; [Docker CLI v28 implementation](https://github.com/docker/cli/blob/v28.0.4/cli/command/container/commit.go), its supported flags. Checked October 15, 2026.
↩ Return: inspect the repaired commit's hosted run and record the first remaining failure or a successful required job.

The diagnostic run [38740202327](https://github.com/vipravlipare/Merlin/actions/runs/38740202327) passed all application and fault stages, then failed documentation because two links targeted global skill files on the author's machine. Those links now reference the repository's bundled skills. Run [38741667183](https://github.com/vipravlipare/Merlin/actions/runs/38741667183) exposed the intermittent `native_equivalence_0` mismatch during default-pausing capture. Sanitized diagnostics retain check names without raw SQL output. Thirty repeated native checks locally passed; that observation alone did not invalidate the hosted failure.

Local immutable-input verification of commit `7a91e6adee3c4cede54ea7fe4a6f82f1d470ad87` passed in 105.447 seconds, including all three required phases and cleanup. An earlier local attempt passed the full suite but correctly failed its enclosing integrity check after documentation changed mid-run; that attempt is not a complete CI pass.
