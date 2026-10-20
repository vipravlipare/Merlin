# Local model readiness probe contract

Authored by the assistant at the learner's request, October 19, 2026. This completes Day 8 item 2.3's design artifact. It does not establish installation, successful execution, learner understanding or production readiness. Actual minutes are unknown. Tracker: [MER-9](https://vipravlipare.atlassian.net/browse/MER-9).

📚 Learn first: [Generate API](https://docs.ollama.com/api/generate), request options, completion and timing fields; [FAQ](https://docs.ollama.com/faq), context, memory, GPU placement and local-only operation; [API errors](https://docs.ollama.com/api/errors), status and error objects. Stop before cloud integrations. Official references opened October 19, 2026; current documentation must still be checked against the pinned runtime during execution.
↩ Return: after the prior-day CI/publication gate and installation prerequisites are resolved, execute the section 3 probe against these expectations. Record observations below; do not replace expected results with whatever the model happened to return.

## Purpose and boundary

Determine whether one small local model can complete bounded requests on the learner's laptop without unacceptable resource pressure. No Merlin endpoint, provider adapter, parser implementation, database write, production deployment or quality claim is part of this experiment. Merlin's existing health endpoint remains independent of Ollama. Personal Codex/OmniRoute routing is unchanged.

Use Ubuntu/WSL only, Ollama 0.40.6 and qwen3:0.6b Q4_K_M (Apache-2.0). Record actual binary version and full installed model digest before accepting results. The digest remains PENDING until download. A tag or catalog short ID is insufficient. Inspect model metadata for supported options; unsupported limits or thinking controls are a failed compatibility gate, not permission to omit bounds silently.

## Access and data rules

- Bind the owned Ollama listener explicitly to IPv4 loopback, 127.0.0.1:11434. Inspect the actual listener before requests. Do not use all-interface binding, tunnels, public forwarding or cloud models. Loopback is not authentication against other local processes.
- Use the direct loopback destination, without an outbound HTTP proxy for local requests or redirect following. No hosted fallback, retries to another provider, API keys or account enrollment.
- Allow exactly one active request and one loaded model. No application/browser/agent integration or concurrent benchmark. Synthetic input only: `Return the word READY and nothing else.` No personal documents, repository contents, credentials, tools or file access.
- Do not start a second listener or stop a pre-existing service. Establish ownership first. If the port is occupied unexpectedly, record BLOCKED and investigate without killing it.

## Request and resource limits

These are conservative experiment policies, not vendor guarantees or measured performance targets. Change them only through a recorded design decision before repeating measurements.

| Setting | Agreed value or rule |
|---|---|
| Endpoint | POST /api/generate on the direct loopback listener |
| Model | qwen3:0.6b; installed digest verified before and after the experiment |
| Response mode | stream=false for this first probe; streaming parser tests remain future work |
| Context | num_ctx=2048; prompt at most 256 UTF-8 bytes; record actual evaluated token count |
| Generation | num_predict=64; temperature=0; think=false after verifying support; no conversation history or raw template override |
| Connection deadline | 2 seconds |
| Total request deadline | 60 seconds including cold loading, identical for cold and warm requests; no automatic retry |
| Response storage | At most 256 KiB per response; exceeding the limit is a probe failure and requires cleanup |
| Model residency | keep_alive=2m for the measured sequence; explicitly unload afterward; do not depend on the timer alone |
| Repetitions | One unloaded-model cold request, then three sequential warm requests, with identical input/settings |
| Installation/download | Consume existing section 3.1/3.2 time boxes of 20/15 minutes; stop when the block expires and carry unfinished work forward |

Before installation/download and again before inference, require at least 2 GiB available WSL RAM and 10 GiB free filesystem space. Before loading require at least 2 GiB free VRAM; actual placement still needs observation. Confirm adequate free space on the Windows host volume backing WSL as well: Linux virtual disk capacity alone does not establish physical host capacity. If host free space is unknown, pause downloads until inspected.

Watch available RAM and GPU memory approximately once per second during inference. Stop the experiment if available WSL RAM drops below 1 GiB, free VRAM falls below 256 MiB, free disk falls below 5 GiB, any OOM event occurs, or the desktop becomes unresponsive. Sampled observations do not establish an exact peak. Do not deliberately provoke OOM to test these limits.

Check a short idle baseline before loading for active swapping. Use at least five interval samples and disregard a tool's first since-boot summary. Persistent swap-in or swap-out across three consecutive samples, during idle or inference, means stop and investigate pressure. Existing occupied swap alone is not failure. Do not disable swap, clear caches or raise WSL limits to force a passing result. Stop unrelated learner-owned workloads gracefully only when appropriate; preserve both database volumes and shared services.

## Expected results and acceptance cases

Every execution is initially PENDING. A deliberately negative case can PASS its expectation without being a successful generation. Keep transport, protocol, safety and generated-content outcomes separate.

| ID | Input or condition | Required observation |
|---|---|---|
| PROBE-01 | Known model, agreed bounded synthetic request | HTTP 200; application/json media type; valid JSON object; matching model identity and verified digest; done=true; nonempty response string; no error field. Exact READY compliance is recorded separately, not assumed. |
| PROBE-02 | Same request after unloading versus three warm requests | Four independently recorded results with identical limits. Record load timing and verify residency before calling a request warm. A restarted process, changed digest or intervening unload invalidates that comparison. |
| PROBE-03 | Synthetically named model confirmed absent from local inventory | HTTP 404 and a JSON error object; no successful generation or automatic download/provider fallback. Record only a safe error category, not arbitrary raw errors. |
| PROBE-04 | An independently verified unused loopback port, without stopping someone else's server | Connection failure within the agreed deadline; no HTTP success and no request to another destination. A genuine connection error must not be mislabeled as an HTTP 500. |
| PROBE-05 | Deliberately short client deadline on the owned request | If the deadline expires, classify timeout, not a successful completion; close the connection, do not retry/fallback, and verify server work stops during cleanup. If a fast response wins the race, the timeout case remains PENDING/inconclusive; use a future isolated delayed fixture instead of claiming proof. |
| PROBE-06 | Token cap reached or no useful final answer | Record completion reason and generated token count. A length-limited response is not proof of following the prompt. Empty output, invalid JSON, missing completion, an error object or exceeded bounds fails the corresponding requirement. |
| PROBE-07 | Resource or listener rule breached | Stop requests and clean up owned work. Record the breached gate and observed values. Do not relax thresholds retrospectively or expose a public listener to continue. |
| PROBE-08 | End of probe, failure, timeout or interruption | Client connections closed; owned model unloaded; no leftover owned generation; owned listener stopped if this experiment started it. Pre-existing service state and both database volumes preserved. |

Capture HTTP status and exit status separately. Do not pipe quiet curl output into grep as the sole check: an empty pipeline does not establish service health, model inventory or digest. Keep startup diagnostics visible for local troubleshooting, then review before recording publishable evidence.

## Measurement and interpretation

Record client wall time, load_duration, prompt_eval_count, prompt_eval_duration, eval_count and eval_duration when present. Ollama duration fields are nanoseconds; generation rate is eval_count divided by eval_duration in seconds, only when duration is positive. Missing fields stay PENDING, never zero. Capture cold/warm observations separately; four requests are insufficient for a credible p95 or broad quality claim. A non-streaming request does not measure time to first generated token.

Record observed RAM/VRAM and GPU/CPU placement from runtime observations. A working nvidia-smi or visible /dev/dxg does not prove Ollama uses the GPU. CPU execution is not a transport failure, but the GPU-acceleration check stays unproven unless placement evidence supports it. Stop on the resource rules regardless of placement.

No new service spend is permitted. Record hardware/electricity/network costs as unmeasured, not zero. This smoke experiment is not the required feature evaluation: any future AI quality claim needs at least 20 labeled cases, a baseline, an agreed metric/threshold, latency and cost measurements. Worldwide deployment requires separate security, capacity and hosting decisions.

## Cleanup and failure handling

Stop issuing requests immediately on failure or interruption. Close the client, unload the selected model and verify no request remains active. A client timeout does not prove the server canceled computation. Allow at most 10 seconds for cancellation/unload; if work persists, gracefully terminate only the experiment-owned server and verify exit. Unverified cancellation/cleanup is FAIL or PENDING, never successful safety proof. If a pre-existing server cannot be safely controlled, do not run the forced-timeout experiment on it.

Preserve downloaded model files for reuse unless removal is separately requested; unloading frees runtime memory and is different from deleting weights. Do not change driver installations, global routing, firewall rules, shared services or database storage. Do not suppress errors, install deliberately faulty application code or execute destructive cleanup.

## Evidence locations and responsibilities — Day 8 item 2.4

This section defines evidence destinations only. Do not create extra reports, scripts or an application adapter merely to run this manual probe. Keep expected behavior above separate from observed results below; never overwrite earlier failures with a later PASS.

| File | Purpose and required contents | Creation rule |
|---|---|---|
| `docs/evals/local-model-readiness.md` — this file | The probe contract plus actual installation version, full model digest, quantization/license attribution, settings, hardware observations, each PROBE case, cold/warm measurements and cleanup results. Each attempt identifies expected versus observed behavior, PASS/FAIL/PENDING and its first failure. | Already exists; append reviewed observations during execution. Do not infer execution from this document's existence. |
| `docs/planning/day-eight-handoff.md` | Authorship, actual dates/minutes or unknown, completed and unfinished outcomes, first blocker, evidence references and exact restart action. Link this readiness record rather than copying its measurements. | Create during section 5.2; currently planned, not evidence of a completed handoff. |
| `docs/architecture/local-provider-contract.md` | Future application-client boundary: transport, buffering/parser rules, errors, deadlines/cancellation, retry policy, non-disclosure and prohibited hosted fallback, with acceptance expectations. | Created as a planning specification for Day 8 item 4.2 requirements review. Implementation is separately scoped and PENDING; no adapter, implementation filename or test file is required for the present manual probe. |
| `docs/planning/STATE.md` and `docs/sprints/day-eight-jira-checklist.md` | Short current status and next action; point to the detailed evidence. Jira MER-9 tracks only outcomes supported by those observations. | Update as outcomes are reviewed; leave unexecuted work open. |

For each installation/download attempt, record start and end time with timezone, elapsed minutes, selected artifact/version, outcome and first failure or stop condition. If timing was not captured, write `unknown`; do not treat the 20-minute installation or 15-minute download allocation as actual time spent. Record incomplete downloads as incomplete and preserve that result when resuming. Reaching a time box, violating a resource threshold, unknown host disk headroom or uncertain ownership stops that attempt under the existing contract rules; it does not authorize an automatic extension or larger model.

For each inference attempt, record its PROBE ID, cold/warm label where applicable, actual settings/digest, client exit status, HTTP status when one exists, expected versus observed result, elapsed time, sampled resource observations, cleanup and exact next action. Mark absent measurements PENDING or unknown as appropriate. Record only synthetic prompts and reviewed outputs/errors; never copy credentials, private account configuration or personal logs. No dated filenames or standalone JSON evidence file is needed for this small manual experiment.

📚 Learn first: the request/resource limits, acceptance-case table and cleanup sections in this contract; revisit the official references above only for an unclear field. Stop before implementing the future provider boundary.
↩ Return: append the first actual installation receipt here during section 3.1 once its entry gates pass. Item 2.4 is complete when these destinations and recording rules are defined, not when future observations have run.

## Section 3.1 installation receipt

October 19, 2026: the learner authorized committing/pushing the reviewed documentation, observing CI and then installing Ollama 0.40.6. Published commit `8602ccf14311142549a2e7b0f5d2527961872b6e` passed the required `setup` job and every step in [run 39198877902](https://github.com/vipravlipare/Merlin/actions/runs/39198877902), including complete cases/faults, committed disposable migration roundtrip and cleanup. This resolves the publication prerequisite for the published snapshot; this subsequent receipt is a new local documentation change.

No previous Ollama executable was found. Ubuntu/WSL reports x86_64. Before download, available WSL RAM was approximately 3.3 GiB; Linux filesystem free space was 944G and the Windows backing drive reported 95G free. Downloaded the official versioned Linux amd64 archive and verified SHA-256 `c164ab8b1b28e2a247c29719b8e404c423c5b83ae64c3ab4e59d50c7ff7fc5e0` against the release asset metadata.

Installed under the learner's user-local tools directory with an `ollama` symlink in the existing PATH, preserving the archive's binary/library layout. System-wide sudo required interactive authentication, so no system-wide installation or service configuration was performed. The downloaded installer script was not executed. A temporary uv environment supplied zstandard for archive inspection and extraction; no project dependency/lockfile changed. Safe tar extraction filtering was used after checksum verification.

`command -v ollama` resolves the installed command. `ollama --version` exits successfully and reports client version **0.40.6**, with an expected warning that no server is running. Section **3.1 PASS for installation/version verification**. No model download or generation was performed; service startup, GPU placement, full model digest, runtime compatibility and all inference cases remain PENDING. Do not treat the absent-server warning as a successful service-health check.

The final RAM sample showed approximately 2.0 GiB available and 1.9 GiB swap occupied. Recheck pressure before section 3.2/3.3; do not infer active swapping from occupancy. Actual elapsed installation minutes are not reliably captured and remain **unknown**; this receipt does not certify that the planned 20-minute block was met. Record any overrun as carryover, not invisible additional work. The release archive remains in temporary download storage; no model is loaded, no autostart was enabled, and no database volumes or coding-agent routing were changed.

## Section 3.2 model download receipt

October 19, 2026: **PASS** for downloading and verifying only qwen3:0.6b. The owned server reported Ollama 0.40.6 and used IPv4 loopback with cloud disabled. Inventory was empty before the pull and contained exactly the selected model afterward. No generation, embeddings, additional models, GPU packages, project dependencies or database changes were introduced.

| Artifact | Verified value |
|---|---|
| Full Ollama model digest | `sha256:7df6b6e09427a769808717c0a93cadc4ae99ed4eb8bf5ca557c90846becea435` |
| Weights digest | `sha256:7f4030143c1c477224c5434f8272c662a8b042079a0a584f0a27a1684fe2e1fa` |
| Quantization | Q4_K_M, reported by installed model inventory |
| Installed model size | 522,653,767 bytes reported by the inventory |
| License | Apache-2.0; attribution: Qwen Team, Qwen3-0.6B; preserve the installed license/notice when redistributing |
| License blob digest | `sha256:d18a5cc71b84bc4af394a31116bd3932b42241de70c77d2b76d69a314ec8aa12` |

Attribution sources: [Qwen's publisher model card](https://huggingface.co/Qwen/Qwen3-0.6B) and [Ollama's model package](https://ollama.com/library/qwen3:0.6b); package page reviewed October 19, 2026. The installed license layer was also checked for Apache License Version 2.0. All six referenced blobs, including configuration, weights, template, license, parameters and preserved original manifest, passed independent SHA-256 and size verification.

First verification failure: the temporary verification script incorrectly equated the API model digest with the hash of the augmented local manifest. The API reports the preserved original manifest digest, without a `sha256:` prefix. Verified that original blob's complete hash and proved its configuration/layers exactly equal the installed manifest after removing only its original-manifest reference. The API and original-manifest digest agree. The augmented local manifest has separate hash `sha256:6f76d4346c34ba89df6e137fb661b4bb4daf322c1151b6ef0dfda981070a851f`; do not substitute this for the API model digest. No model bytes or expectations were altered to bypass the failed check. The original failed temporary receipt remains separate from its corrected verification receipt.

Resource observations: pre-download available WSL RAM was 2,156,371,968 bytes, above the 2 GiB entry gate. The approximately one-second monitor recorded minimum available RAM 2,124,939,264 bytes, above the 1 GiB stop threshold. Initial Linux/host free disk was approximately 1,010.6/85.1 billion bytes; final Linux/host free disk was 1,010,108,047,360 / 84,721,082,368 bytes. Neither disk stop threshold was crossed. Five interval samples before the operation and five during it showed zero swap-in/out; ignore the first since-boot summary. Existing swap occupancy was not treated as active swapping. These are sampled observations, not exact peaks or proof against every OOM condition.

The timed download/server/first verification attempt ran from 21:57:04.088974 to 21:58:36.426133 UTC, **92.346 seconds**. Corrective verification followed without redownloading. Record this separately from inference time; it does not measure generation latency. The model remains downloaded for reuse. The owned server exited, and a subsequent privileged listener/process check found no listener on 11434 or matching owned server process. No model was intentionally loaded for inference; GPU acceleration, memory fit during generation and all inference cases remain PENDING. Recheck the 2 GiB entry gate before section 3.3.

## Section 3.3 first learner attempt — FAIL

October 19, 2026, learner-supplied evidence: listener bound correctly to 127.0.0.1:11434; inventory matched the installed model digest. The bounded generation request received zero bytes, curl exit 28 and HTTP placeholder 000 after 60.002684 seconds. No JSON response was available. This is not a passing inference observation. Actual learner minutes remain unknown.

The server logged a CUDA GPU-discovery watchdog timeout and stale-memory fallback, followed by runner launch at 18:06:58 and runner availability at 18:07:38 (40.36 seconds). All 29 layers were offloaded to the GPU and a 2048-token context was allocated. The request ended at 18:07:55 after the client's one-minute deadline; the server logged 500 and task cancellation. The client did not receive that HTTP status, so retain HTTP 000 as its observation. No completed output is shown. GPU discovery and runner startup consumed much of the request budget; the underlying cause of their delay is not yet isolated. Model corruption, driver failure and active swapping are not established by this log.

Later learner samples showed 2.1 GiB available RAM, nearly full swap, five idle intervals with no swap-in/out, and no GPU allocation. Those later samples do not establish resource usage during the failed request. The scheduler reported host-memory pressure and disabled mmap during loading, which is a relevant contributing hypothesis rather than proof of OOM. A prompt-cache size limit in the runner log is a capacity setting, not evidence that this amount of RAM was allocated. The model completed loading, but no successful generated answer is established.

Cleanup: learner showed empty loaded-model inventory, stop/unload requests and Ctrl+C. A subsequent process inspection found no ollama/llama-server process. Direct model-free CUDA 13/12 list-device diagnostics returned no devices in both invocations; these did not reproduce Ollama's managed backend-discovery setup and are inconclusive, not evidence that the GPU is absent or either backend fixes the issue. Installed runner dynamic libraries resolved. No model files, drivers, runtime pins or application code were changed.

Next diagnostic: compare managed discovery/startup using one explicitly selected backend at a time, preserving the 60-second request deadline and all resource/cleanup gates. First inspect the pinned runtime's supported backend selection. A controlled CUDA 12 trial may distinguish backend initialization behavior, but is not yet a proven fix. Preserve this original failure, do not relabel a preloaded run as cold, and do not raise the deadline merely to obtain PASS. Section 3.3 remains open.

## Section 3.3 controlled backend follow-up

October 19, 2026: assistant-executed diagnostic authorized by the learner. The original failed attempt above remains valid. Each trial started an owned Ollama 0.40.6 process with the same explicit loopback, local-only, single-request settings; only OLLAMA_LLM_LIBRARY changed. The pinned runtime's envconfig/config.go and discover/runner.go were inspected to verify cuda_v13/cuda_v12 backend selection. Initial managed discovery was allowed up to 45 seconds, separately recorded; no model was preloaded. Each identical synthetic generation retained its original 60-second request deadline, 2048 context and 64-token cap. This is not a repeat of the automatic-backend baseline, and disk/driver caches were not cleared.

| Observation | CUDA 13 | CUDA 12 |
|---|---:|---:|
| Managed initial discovery | 4.431 s | 4.466 s |
| Client request wall time | 17.452 s | 4.441 s |
| Server load_duration | 3.738 s | 3.227 s |
| Output token count | 3 | 3 |
| Server eval_duration | 13.321 s | 0.180 s |
| HTTP / curl exit | 200 / 0 | 200 / 0 |
| JSON completion | done=true, done_reason=stop | done=true, done_reason=stop |
| Response | Ready. | Ready. |
| Minimum sampled available RAM | 1,416,085,504 bytes | 1,797,959,680 bytes |
| Generation contract outcome | PASS | PASS |
| Exact READY instruction compliance | FAIL | FAIL |

Both responses had JSON media type, the expected model identity, nonempty output and no error. Both loaded-model inventories reported the previously verified full digest, 2048 context, and 693,423,308 bytes of model residency entirely attributed to VRAM. Logs showed all 29 layers offloaded and the requested backend selected. No GPU discovery watchdog was observed in either follow-up trial. Initial RAM/VRAM gates passed; sampled RAM stayed above 1 GiB, free VRAM above 256 MiB and no three-consecutive-sample swap condition triggered. Sampling does not establish exact peaks or exclude every transient condition.

The first CUDA 12 preflight attempt was BLOCKED before its server started: a bind probe without address reuse reported an address in use immediately after the previous process exited. Corrected the operational check to require no actual listener and use address reuse for its reservation; no process was killed to free the port. The successful CUDA 12 trial followed. Preserve this harness failure separately from inference outcomes.

Both owned server groups were stopped afterward. The original cause of the automatic-backend watchdog remains unresolved; these two passing trials establish that both installed backends can generate under the agreed deadline on this machine. CUDA 12 was faster in this single ordered comparison, but cache/order and host variability are uncontrolled. Use an explicit cuda_v12 setting for the next local diagnostic session as a provisional choice, not a permanent global override or established performance fix. No runtime, model, drivers, global configuration or app code was changed.

Section **3.3 PASS** for the specified service/request/identity/cleanup scope; exact prompt compliance is separately FAIL and no AI quality claim follows. Section 3.4's planned cold/three-warm measurements remain open; neither this comparison nor the earlier failure supplies that complete benchmark. Assistant authorship does not prove the learner personally executed or understood these diagnostics. Full raw private diagnostic logs remain temporary and are not publication artifacts.

## Section 3.4 cold and warm measurements

October 19, 2026: **PASS for measurement scope**, assistant-executed with learner authorization. The experiment ran from 22:25:17.615170 to 22:25:27.825039 UTC, 10.213 seconds including managed discovery, four requests and cleanup; this is execution time, not total documentation/review minutes. Initial managed GPU discovery took 3.182 seconds and is excluded from each request's curl wall time. No load/generate request preceded the cold request. The service had an empty loaded-model inventory; before each warm request, residency and the full digest were checked. There was no intervening unload/restart.

All four requests used Ollama 0.40.6, explicit cuda_v12, the same previously verified model digest, synthetic READY prompt, stream=false, think=false, context 2048, output cap 64, temperature 0, keep_alive=2m, connection deadline 2 seconds and total deadline 60 seconds. One request at a time; no retries. Cold means **model not resident**, not a cleared operating-system file cache or rebooted GPU/driver. Earlier diagnostics may have warmed filesystem/driver caches.

| Run | Client wall s | First-byte s | API total s | API load s | Prompt evaluation s | Input tokens | Cached input tokens | Output tokens | Generation s | Generation tokens/s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Cold | 3.227785 | 3.227712 | 3.226277 | 2.995954 | 0.146304 | 24 | 0 | 3 | 0.080156 | 37.43 |
| Warm 1 | 0.043842 | 0.043556 | 0.040042 | 0.001777 | 0.010925 | 24 | 23 | 3 | 0.021658 | 138.52 |
| Warm 2 | 0.054822 | 0.054562 | 0.050211 | 0.002701 | 0.017071 | 24 | 23 | 3 | 0.021619 | 138.77 |
| Warm 3 | 0.057639 | 0.057418 | 0.051383 | 0.002118 | 0.013096 | 24 | 23 | 3 | 0.027808 | 107.88 |

API timings were converted from nanoseconds; generation rate is output tokens divided by API eval_duration in seconds. Curl wall time measures the HTTP operation, independently of the monitoring loop's polling delay. First-byte timing is curl time_starttransfer and can include response headers; **time to first generated content/token remains PENDING** because stream=false does not expose when internal generation first emitted a token. Do not substitute first-byte time for token latency. API component timings are not assumed to sum exactly to total wall time.

Every request returned HTTP 200, curl exit 0, JSON media type, expected model identity, done=true, done_reason=stop and nonempty response `Ready.`. No error field. Generation liveness passes; exact requested uppercase READY compliance remains FAIL for all four. Warm requests reused 23 cached input tokens, so these are repeated-prompt warm measurements, not unrelated-prompt throughput. Three output tokens and three warm observations cannot establish sustained throughput, p95, quality or production capacity.

Resource evidence: entry available RAM 2,274,578,432 bytes; minimum across recorded samples 1,745,698,816 bytes, above the 1 GiB stop gate. Maximum **sampled** GPU allocation 765 MiB, with sampled free VRAM at least 3201 MiB. Each post-response loaded-model inventory reported total size and size_vram both 693,423,308 bytes, matching the chosen digest and 2048 context. This establishes reported GPU placement, not an exact physical-memory peak. The cold request had three resource samples; warm requests finished faster than sampling and their single observations were taken around/after completion, so transient peaks are **unmeasured**. No sustained three-sample swap condition triggered; initial idle interval samples showed zero swap-in/out. Disk headroom checks passed.

Cleanup passed: explicit unload returned an empty loaded-model inventory, the owned server stopped, a subsequent listener/process check found no Ollama/runner or listener on 11434, and nvidia-smi reported 0 MiB used. No model/runtime/global configuration/app code changed. The earlier failed cold request and backend comparison remain separate historical observations. This benchmark is local hardware evidence, not hosted CI coverage. Next item: 3.5 review the experiment and record any justified simplification without weakening limits or adding an adapter.

## Section 3.5 experiment review

October 19, 2026: **COMPLETE for review scope**, assistant-authored at the learner's request. Actual review minutes are unknown; no claim that the entire work fit ten minutes. No application code, tests, configuration or reusable scripts were written/refactored in this step. Learner-owned API behavior remains unchanged.

| Review area | Finding and decision |
|---|---|
| Clarity | Keep contract expectations, first failures, backend comparison and the four-run measurements separately attributed. Retain the distinction between model-unloaded and filesystem-cold, first byte and first token, measured samples and unmeasured peaks, and generation success and exact prompt compliance. Earlier dated PENDING entries describe their original snapshots; the latest observation table is the current result summary. |
| Dependencies | Existing curl, Python standard library, NVIDIA tooling and the selected Ollama runtime suffice for the probe. A temporary uv environment used zstandard solely to extract the release archive; no project dependency or lockfile changed. No model SDK, framework, adapter, embeddings, second model or extra GPU package is needed. Do not turn temporary diagnostic scripts into application infrastructure merely to retain the experiment. |
| Refactoring | No learner application change is needed to preserve or explain these observations. No refactor is authorized by this review block. Keep the temporary diagnostics outside the project; a future maintained provider client/test harness needs its own scoped authorization, safe cleanup/error review and regression checks. |
| Existing API | Application, tests, tooling, CI configuration and dependency manifests are unchanged from published commit 8602ccf. All recorded Python source hashes still match the hosted implementation receipt. No API server listener was present at review time; the API was not restarted or altered. |
| Cleanup | The four-run receipt confirms explicit unload and owned-server exit. Fresh privileged checks found no listener on 11434 or 8000 and no Ollama/llama-server process. Keep downloaded weights/runtime for reuse; deleting them is not necessary cleanup. Temporary diagnostics/logs remain outside Git; review rather than publish raw logs. |
| Database preservation | Read-only Docker volume inspection confirmed both protected volumes still exist: merlin_postgres_data and merlin-d6-20261008105707_postgres_data. This step made no database connections, migration calls, writes, stops or deletion. Existence checks do not constitute a new contents/schema fingerprint comparison. |
| Remaining limitations | Original automatic-backend watchdog cause is unresolved; cuda_v12 is a provisional per-session diagnostic choice. Exact READY compliance remains FAIL. First-token latency, exact resource peaks, broader quality/load/security and remaining negative cases remain unproven. Do not broaden the acceptance claims to close these gaps. |

Next action: section 4.1, compare the required healthy, missing-model, unavailable-service and bounded-timeout cases with this contract. Preserve original outcomes and ownership-aware cleanup. This review adds no new dependency, global override, code change or CI coverage claim; new documentation remains unpublished until separately reviewed publication.

### Separately authorized application cleanup after section 3.5

The learner subsequently explicitly authorized only the small refactors identified in code review. Added type hints and spacing to the health handler, removed the redundant handler-factory comment in the server entry point, and formatted the database probe connection arguments across lines. Preserved routing, serialization/error boundaries, socket timeout, loopback binding, read-only probe behavior, SQL and connection parameters. No new dependency or abstraction was introduced; note validation and maintenance code were unchanged.

Formatting moved the probe import-guard mutation from line 21 to line 30. Updated only that diagnostic identifier in the suite runner and inventory; its existing classification and all assertions/counts remain unchanged. Kept the existing 405 response call compatible with isolated fault selectors rather than rewriting the fault harness for cosmetic wrapping.

Verification before/after: the same 232 focused tests passed. The complete guarded suite then passed all ten stages, including 729 Python/database tests plus three subtests, 349 demonstrated Python case IDs and all 250 canonical Python faults detected with zero survivors/invalid/timeouts/unapplied. SQL, JavaScript/browser, lifecycle, migration, documentation and preservation/cleanup gates passed. Raw local results: /tmp/merlin-small-refactor-suite/summary.json. Historical hosted source hashes now describe the pre-refactor revision; these new source changes have local proof only until committed/published and independently verified by hosted CI. No commit or push was performed for this cleanup.

## Section 4.1 healthy and negative contract observations

October 19, 2026: **PASS for the four requested observations**, assistant-executed with learner authorization. Used the unchanged pinned Ollama/model and explicit session-only cuda_v12, loopback, cloud-disabled, single-request settings. The healthy request retained the 2048 context, 64-token cap and 60-second deadline. Expected errors are retained as successful negative checks, not discarded or relabeled healthy generations. The complete execution, including discovery and cleanup, took 10.422 seconds; total planning/review minutes are unknown.

| Contract case | Observed outcome | Result against expectation |
|---|---|---|
| PROBE-01 healthy | HTTP 200, curl exit 0, application/json, correct model, nonempty response Ready., done=true, done_reason=stop, no error; 4.408811 s | PASS for generation contract; exact uppercase READY compliance remains FAIL |
| PROBE-04 unavailable service | Reserved an ephemeral loopback TCP socket without listening, preventing another listener from taking that destination during the check. Curl exit 7, no HTTP response/body, 0.000154 s | PASS expected connection failure; HTTP placeholder 000 is not an HTTP 500 |
| PROBE-03 missing model | Synthetic nonexistent model confirmed absent before request; HTTP 404, curl exit 0, JSON error object, 0.002334 s | PASS expected model-not-found. Curl exit 0 reflects completed HTTP transport because --fail was deliberately not used; it does not mean generation succeeded. |
| PROBE-05 bounded client timeout | Same synthetic generation request with deliberate 0.001-second total deadline; curl exit 28, no HTTP response/body, 0.001483 s | PASS for observed client deadline and owned-process cleanup. No assertion that the handler received or began this request. |

The missing-model check left the inventory unchanged: exactly the previously verified qwen3:0.6b digest, with no automatic model download. The operation used no hosted endpoint or fallback and no redirects or proxy for loopback calls. Initial memory/disk/VRAM gates passed; minimum recorded available RAM was 1,737,781,248 bytes, above the 1 GiB stop threshold. No sustained three-sample swap condition triggered and sampled GPU/disk stop gates were not crossed. These remain sampled observations, not exact resource peaks.

A 1 ms timeout can occur before the server accepts the request; the log did not show cancellation for that attempt. This proves a bounded client outcome, **not automatic server-side cancellation after inference begins**. The original 60-second failure did log task cancellation and remains separate historical evidence. For this new forced-timeout check, explicitly terminated the experiment-owned server group and observed exit in 0.165 seconds, within the 10-second cleanup budget. A subsequent privileged check found no Ollama/llama-server process or listener on 11434 and reported 0 MiB GPU allocation. Thus no work remained after cleanup; do not claim that merely closing the client guaranteed it.

No pre-existing listener/service was stopped. The owned unavailable-service socket was released. Both protected database volumes remained present on read-only inspection; no database operation, migration or storage change was performed. Application code, tests, dependencies, model bytes and global runtime settings were unchanged in this step. Section 4.1 is complete; provider parser/fault effectiveness and in-flight cancellation guarantees remain future implementation/verification scope. Next: 4.2's streaming/error requirements review.

## Actual inference observations — follow-up generation passed

| Evidence | Status |
|---|---|
| Contract authored and checked against checklist | COMPLETE; assistant-authored planning artifact |
| Hardware inspection and runtime/model selection | Recorded in the Day 8 checklist, sections 2.1–2.2 |
| Binary version and host backing-volume headroom | PASS for section 3.1 as recorded above; recheck headroom before further downloads |
| Full installed model digest | PASS section 3.2; complete digest, license and blob checks recorded above |
| PROBE-01 and basic GPU placement | PASS in controlled backend trials; exact prompt compliance FAIL |
| PROBE-02 cold/three-warm measurements | PASS as scoped above; first-token latency PENDING, exact prompt compliance FAIL |
| PROBE-03/04 missing model and unavailable service | PASS expected failures in section 4.1 |
| PROBE-05 client timeout and explicit owned-process cleanup | PASS as scoped in section 4.1; active-handler cancellation effectiveness unproven |
| PROBE-06/07 additional boundary checks | PENDING beyond recorded token counts/resource observations; no fault-effectiveness claim |
| First execution failures | Earlier installation attempt command-not-found/127; first inference attempt timed out at 60.002684 s. Both preserved above. |
| Follow-up owned-server cleanup | PASS; verify listener/process/GPU state after each future attempt |
| Actual minutes and learner explain-back | Unknown / not established by assistant authorship |

When executing, add the actual date, input identity, expected versus observed result, settings/version/digest, wall time, resource observations, PASS/FAIL/PENDING, first blocker and exact next action. Publish only reviewed synthetic evidence. Do not attach raw personal logs or private error values.

## Section 4.3 retained suite and cumulative CI review

October 19, 2026: **local coverage/proof PASS; hosted verification of the unpublished refactor PENDING**. Compared the entire current tests/suite-inventory.json with published commit 8602ccf. Every field is identical except the probe's existing line-based diagnostic ID moving from ast-database_connectivity_probe-21-11 to ast-database_connectivity_probe-30-11 after formatting. No case, fault, assertion requirement or diagnostic classification was removed; the matching runner reference was updated. All Day 6/7 application, database, browser/JavaScript, lifecycle and migration inventories remain required.

The authorized source cleanup already ran `.venv/bin/python tools/run_test_suite.py --out-dir /tmp/merlin-small-refactor-suite`. That complete ten-stage run PASSED from 22:31:59.539377 to 22:32:50.703660 UTC, **51.164283 seconds**. It included 729 Python/database tests plus three subtests, 40 JavaScript cases, all 349 Python case IDs demonstrated, 250 canonical Python faults DETECTED, three separately attributed aliases and four separately excluded import diagnostics. Zero unexpected survivors, invalid faults, timeouts or unapplied faults. SQL, browser, JavaScript, lifecycle and migration fault stages, source preservation and disposable cleanup passed.

Rechecked all **36** source hashes recorded by that Python audit against current files: no mismatch. No code/test/config changes followed the verified refactor; subsequent changes are documentation. Reused that matching complete-run proof and reran documentation lint and whitespace checks rather than repeating expensive database/fault stages. Documentation lint passed with its existing one warning/27 verify items; no new error. Local PASS does not establish a hosted run for this working tree.

Reviewed the workflow and tools/run_ci.py: push/PR verification still invokes the complete suite, validates all ten expected stage names, exit/status outcomes, source preservation and cleanup, then separately requires the committed disposable migration roundtrip. It has no requirement for a local Ollama process, GPU, downloaded weights or personal credentials. Public GitHub job results were rechecked for **8602ccf14311142549a2e7b0f5d2527961872b6e**, [run 39198877902](https://github.com/vipravlipare/Merlin/actions/runs/39198877902): required setup job and every listed step succeeded, including cases/faults, migration and cleanup. This proof covers the published snapshot, not the later uncommitted refactor.

No deterministic provider parser/tests/faults have been implemented; the 24 planned rows in the provider contract remain PENDING and therefore are not claimed as CI coverage. Hardware timings, CUDA observations and manual local negative checks remain separately attributed local evidence. Future implemented provider tests must use synthetic independently owned fixtures with no GPU/model/private-service dependency and join the complete inventory/result validation.

**Overall 4.3 stays open until publication reconciliation:** review the current refactor/planning/evidence diff, obtain authorization for committing and normally pushing these new changes, then observe the exact new commit's required CI job. Earlier publication approval was for the previously reviewed changes; this review does not infer permission to publish the later source cleanup. No commit/push/dispatch was performed in 4.3. Actual review minutes unknown. There is no current local test failure; the first remaining blocker is unpublished-source hosted proof.

## Section 4.2 streaming and error requirements review

October 19, 2026: COMPLETE for specification/review only. See [the scratch local provider contract](../architecture/local-provider-contract.md) for framing, split UTF-8/JSON records, strict parsing/completion, mid-stream error objects under HTTP 200, bounded buffers/timeouts/cancellation, fixed public errors, zero automatic retries and zero unauthorized hosted requests. Its 24 acceptance-case/fault expectations remain PENDING implementation and execution; the manual model probe proves none of those parser/retry controls. Server-side in-flight cancellation remains unproven. Actual review minutes unknown. No code, tests, faults, dependencies or CI configuration were created/changed for this review. Next: section 4.3 retained suite and CI verification, including the separately authorized application refactor's unpublished source changes.

## Section 4.4 actual status, timing and first blocker

Recorded October 19, 2026. This is an evidence summary, not a new execution or a claim that Day 8 is Done. Assistant authored the contract/review and executed the authorized installation, model download, diagnostic follow-ups and measurements. The learner supplied the initial hardware and failed-request observations. Actual total learner/assistant minutes are **unknown**; measured command wall times below are not total learning, implementation or review time. The planned 14-minute recording block is not an observed duration.

| Outcome | Actual status and evidence |
|---|---|
| 2.1 hardware inspection / 2.2 selection | PASS for inspection/selection. Ubuntu/WSL, pinned Ollama 0.40.6 and qwen3:0.6b Q4_K_M selected. These are not production-sizing proof. |
| 2.3 contract / 2.4 evidence plan | COMPLETE as assistant-authored planning artifacts; execution was recorded independently. |
| 3.1 installation | PASS: command resolves and client reports 0.40.6, official archive hash verified. Actual installation minutes and 20-minute compliance unknown. |
| 3.2 model download | PASS: only selected model installed; full digest, six blob hashes/sizes and Apache-2.0 attribution verified. Timed download/initial verification attempt 92.346 s; corrective digest verification followed separately. |
| Original learner generation | FAIL: zero bytes, curl 28, HTTP placeholder 000, 60.002684 s. GPU discovery watchdog and slow runner initialization observed; underlying intermittent cause unresolved. |
| 3.3 controlled follow-ups | PASS for healthy generation/identity/GPU placement and cleanup on both backends. CUDA 13 request 17.452 s; CUDA 12 request 4.441 s. One ordered comparison does not establish permanent superiority. |
| 3.4 one model-unloaded cold / three resident warm | PASS for measurements: 3.227785 / 0.043842 / 0.054822 / 0.057639 s client wall. Full load/evaluation/token/rate evidence above; warm prompts reused 23 input tokens. First-token latency PENDING; no exact peak or p95 claim. |
| Exact requested READY output | FAIL: observed Ready. instead. Preserve this content failure separately from successful generation; no assertion or prompt was weakened to hide it. |
| 3.5 review and separately authorized refactor | Review COMPLETE; small source cleanup passed 232 focused tests before/after and the full suite. Not a fix for the model watchdog or instruction-compliance failure. |
| 4.1 healthy and negative observations | PASS as scoped: healthy 200/4.408811 s; missing-model 404/0.002334 s; unavailable-service curl 7/0.000154 s; forced-timeout curl 28/0.001483 s. Negative outcomes are expected failures, not successful answers. |
| Cancellation and cleanup | Owned process-group termination after forced timeout 0.165 s; no listener, runner or GPU allocation afterward. Automatic cancellation after the server starts inference remains PENDING: a 1 ms deadline may precede handler entry. |
| 4.2 future client requirements | COMPLETE for design. All 24 proposed protocol cases/faults, parser/client implementation and integration remain PENDING. |
| 4.3 retained coverage and local suite | PASS locally: inventory retained except relocated diagnostic line ID, all 36 recorded source hashes match. Complete guarded run 51.164283 s, all ten stages, 250 canonical faults detected and preservation/cleanup PASS. |
| 4.3 hosted coverage of current changes | PENDING: latest observed published CI PASS is 8602ccf/run39198877902. Later source refactor/evidence/docs are unpublished and have no exact hosted result yet. Local hardware probes are not hosted CI. |
| AI quality / production readiness | PENDING and unclaimed. No labeled task-quality evaluation, comparative baseline or production load/security acceptance has run. |

**First failure history:** initial install attempt was command-not-found/exit 127, resolved by the pinned installation. Model-download verification then exposed an incorrect local-manifest/API digest assumption; the original receipt remains FAIL and the verified original-manifest/blob relationship is separately recorded. The first actual inference failed at the 60-second deadline. An intermediate backend preflight encountered a recently used socket address; it did not prove model failure and was corrected without stopping another service. Do not overwrite these attempts with later PASS results.

**First current blocker:** section 4.3 publication reconciliation. Exact next action is obtain authorization to commit and normally push the reviewed later refactor/docs, then observe required CI for that new commit before closing 4.3. Section 4.4 can be complete for honest recording while 4.3 and the story remain open. Do not mark the entire verification block or Day 8 Done from this summary. Original watchdog diagnosis, exact output compliance, provider client/tests/faults and final section 5 review/handoff remain explicitly carried forward.

### Quality and cost gate

Before any claim that an AI feature is useful, accurate or production-ready, require a versioned set of **at least 20 labeled task cases**, a non-AI or other agreed baseline, a named quality metric with a threshold decided before scoring, measured latency (including an honestly measured first-content/token metric where applicable) and cost/token evidence. The 24 proposed parser/protocol cases are not that golden set. Neither four repetitions of one synthetic prompt nor a 200 response establishes quality. The exact-output failure must remain represented when designing that future evaluation.

Observed operations used local downloaded weights and local inference; no paid-provider inference, subscription enrollment, purchased credit or new hosted deployment was performed. **Observed new service purchases for these operations: $0.** This is an action-scope statement, not an audit of all account billing or a guarantee against unrelated charges. Hardware purchase/depreciation, electricity and internet/data costs were not measured and are **unknown**, not zero. Future hosted inference/deployment cost and worldwide capacity remain PENDING separate scope/budget decisions. No paid fallback is authorized by a local failure.

Recording this section made no application/test/config changes and ran no new model request. The remaining code changes retain their existing local test proof and pending hosted status. Refer to the exact outcome rows rather than treating the document's completion as evidence that unfinished software exists.

## Section 5.1 publication and resource-preservation review

October 19, 2026: **COMPLETE within the reviewed scope**, before any new commit. Actual review minutes unknown. Reviewed the pending application cleanup, relocated diagnostic references, readiness evidence, planning state/checklist and new provider contract. The recorded prompt/output and absent-model inputs are synthetic; no personal documents or private model prompts were copied into these changes. Model/archive/blob hashes and license attribution are public artifact identities, not credentials. The provider contract uses fixed error requirements and synthetic sentinel expectations rather than real private error examples. Existing API response/error behavior was not altered by the type/formatting cleanup.

The publication scan inspected 351 current tracked/non-ignored files and 476 reachable historical blobs, expanding 74 gzip objects and two archives (847 scanned objects overall). It found no matches for its credential/key/token/credential-URL patterns or known local private-value comparisons. Changed prose and code were also reviewed for private prompts, raw runtime logs and combined access details. Raw temporary server logs, model files and private local configuration are outside the publication set. No secret-removal change was indicated by this review. This is finite evidence, not a guarantee against every secret or attack; remote-only history, screenshots and unrelated external copies are not certified.

Fresh privileged listener/process checks found **no listener on 11434 or 8000 and no Ollama/llama-server process**. No additional unload/stop/kill was needed; do not restart a server merely to stop it. The previous four-run benchmark explicitly unloaded its owned model, and subsequent owned-process timeout cleanup was verified. Downloaded model weights and the user-local runtime remain for reuse; no shared tool was uninstalled or global startup/routing configuration altered.

Read-only Docker inspection confirmed **both protected volumes still present**, with the existing PostgreSQL/Redis services still running and their reported health states healthy. No service was stopped in this review; no database connection, write, migration, downgrade, volume deletion or content-fingerprint recomputation was performed. Volume presence and unchanged running services are preservation observations, not a new full data-integrity audit. Unrelated running services were left alone.

Documentation lint and whitespace checks passed, with the existing one documentation warning and 27 verification items. No application/test/config behavior changed in this step, so the matching local suite proof is retained. No commit, push or remote dispatch was performed. Section 4.3's exact hosted verification of the unpublished refactor remains PENDING. Next: 5.2 purpose-named Day 8 handoff, followed by the learner's 5.3 explain-back; do not close the story from this review alone.

## Final Day 8 closeout

October 19, 2026: the learner explicitly confirms items 1.1 and 5.3 complete, and authorizes publication/completion of 4.3. The reviewed refactor, retained diagnostic references, contract and evidence were committed and normally pushed as **ea1e2b216c9f5ddc1b15617651ddf9c3cb48f2df**. [GitHub run 39365222970](https://github.com/vipravlipare/Merlin/actions/runs/39365222970) completed its required setup job successfully; every listed step passed, including all prior application cases/faults, committed disposable migration verification, artifact retention and cleanup. This establishes exact published-source hosted proof for 4.3; earlier PENDING/publication-blocker statements above are historical and superseded.

**4.3 COMPLETE. Day 8 readiness scope complete**, subject to the recorded learner confirmations and finite evidence limits. Future provider software/24 protocol checks, golden-set quality evaluation, first-token/peak measurements, reliable in-flight cancellation and production scaling remain deferred; original watchdog and exact READY failures remain recorded. These are not claimed as delivered features. The laptop runtime/model configuration is unchanged. This closeout is documentation only; the normal push triggers a separate cumulative run whose actual outcome must be observed independently.
