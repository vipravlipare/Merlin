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
| `docs/architecture/local-provider-contract.md` | Future application-client boundary: transport, buffering/parser rules, errors, deadlines/cancellation, retry policy, non-disclosure and prohibited hosted fallback, with acceptance expectations. | Create only when that scratch implementation slice is separately scoped. No adapter, implementation filename or test file is required for the present manual probe. |
| `docs/planning/STATE.md` and `docs/sprints/day-eight-jira-checklist.md` | Short current status and next action; point to the detailed evidence. Jira MER-9 tracks only outcomes supported by those observations. | Update as outcomes are reviewed; leave unexecuted work open. |

For each installation/download attempt, record start and end time with timezone, elapsed minutes, selected artifact/version, outcome and first failure or stop condition. If timing was not captured, write `unknown`; do not treat the 20-minute installation or 15-minute download allocation as actual time spent. Record incomplete downloads as incomplete and preserve that result when resuming. Reaching a time box, violating a resource threshold, unknown host disk headroom or uncertain ownership stops that attempt under the existing contract rules; it does not authorize an automatic extension or larger model.

For each inference attempt, record its PROBE ID, cold/warm label where applicable, actual settings/digest, client exit status, HTTP status when one exists, expected versus observed result, elapsed time, sampled resource observations, cleanup and exact next action. Mark absent measurements PENDING or unknown as appropriate. Record only synthetic prompts and reviewed outputs/errors; never copy credentials, private account configuration or personal logs. No dated filenames or standalone JSON evidence file is needed for this small manual experiment.

📚 Learn first: the request/resource limits, acceptance-case table and cleanup sections in this contract; revisit the official references above only for an unclear field. Stop before implementing the future provider boundary.
↩ Return: append the first actual installation receipt here during section 3.1 once its entry gates pass. Item 2.4 is complete when these destinations and recording rules are defined, not when future observations have run.

## Actual observations — not executed

| Evidence | Status |
|---|---|
| Contract authored and checked against checklist | COMPLETE; assistant-authored planning artifact |
| Hardware inspection and runtime/model selection | Recorded in the Day 8 checklist, sections 2.1–2.2 |
| Binary version, full digest and host backing-volume headroom | PENDING |
| PROBE-01 through PROBE-08, cold/warm timings and placement | PENDING |
| First execution failure | No contract execution yet; prior attempt was command-not-found/exit 127 |
| Cleanup observations | PENDING; no service started by this contract authoring task |
| Actual minutes and learner explain-back | Unknown / not established by assistant authorship |

When executing, add the actual date, input identity, expected versus observed result, settings/version/digest, wall time, resource observations, PASS/FAIL/PENDING, first blocker and exact next action. Publish only reviewed synthetic evidence. Do not attach raw personal logs or private error values.
