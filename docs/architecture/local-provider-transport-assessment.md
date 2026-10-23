# Day 9 item 3.3: local HTTP transport assessment

Recorded October 23, 2026 for MER-10. Assistant-authored assessment and learner work specification, requested before further manual coding. **Assessment complete; transport deferred.** No HTTP client, transport test, dependency, service or endpoint was added. `/health` is unchanged. Actual minutes are unknown; the original ten-minute block is not a measured duration.

📚 Learn first: [existing provider contract](local-provider-contract.md#bounds-retry-policy-and-cancellation), mandatory deadlines and LP-16–22/24; [Python HTTPConnection](https://docs.python.org/3.12/library/http.client.html#http.client.HTTPConnection), timeout, response handling and close; [monotonic clock](https://docs.python.org/3.12/library/time.html#time.monotonic), measuring elapsed time. Official pages opened October 23, 2026. Python pages describe 3.12.15; the project uses 3.12.14. Current Ollama references still need pinned 0.40.6 compatibility proof before implementation. No Context7 verification is claimed.
↩ Return: review the stop decision below, complete the decoder learning/verification work, and keep live transport for a separately budgeted learner-owned task.

## Decision and prerequisite evidence

Do not add live transport in this ten-minute assessment block. The existing decoder has useful passing baseline evidence, but a fully verified transport and all applicable safety gates cannot honestly be promised within the remaining allocation. This is the ticket's permitted parser-only stop, not a reduced transport requirement.

| Gate | Observed state |
|---|---|
| Retained provider baseline | Fresh run: `.venv/bin/python -m pytest -q tests/test_local_provider.py` — **117 passed in 0.22 seconds**. No model, database or socket was needed. |
| Nearest regression evidence | The 3.2 receipt records **349 focused cases passed in 3.34 seconds**, including those 117 provider cases. This assessment did not rerun the broader group. |
| Every required decoder baseline | **Not certified by the 117-case count.** Reconcile D-01–38 and their variants with retained executable checks. In particular D-37's explicit external-call traps are not present in the current provider test file. The source being byte-only is useful review evidence, not an executed trap test. |
| Individual effectiveness and retained verification | Four 3.2 counterfactuals were observed earlier. Complete provider case/fault inventory, permanent fault integration, full-suite execution and expanded-source hosted proof remain open under 4.1–4.4. The current suite inventory has no provider entries. |
| Learner understanding | The learner reported the 3.2 explain-back unanswered. Assistant implementation does not complete that learning proof. |
| Transport safety | No implementation or executed LP-16–22/24 network evidence exists. Decoder tests do not prove timeouts, cancellation, routing or network cleanup. |

Assessment can complete without authorizing a live connection. The selected rung remains a bounded decoder under verification; it is not yet a fully closed decoder story or a connected provider. Use the optional transport allocation for the existing verification backlog, not extra unrecorded work. If ten minutes is insufficient, carry the remaining checks forward.

## Smallest later implementation boundary

Keep decode_response byte-only. A future small transport owns one request, supplies bounded bytes to that decoder and closes its own connection/response. Reuse Python's standard library if its implementation can meet all gates; do not introduce a gateway hierarchy, SDK, async stack or raw HTTP parser merely to shorten the task. The standard library is a candidate, not a claim that a single HTTPConnection timeout solves the contract.

The eventual transport must not accept a user-supplied URL/model selector. Its destination is the existing literal IPv4 loopback 127.0.0.1:11434, path POST /api/generate, model qwen3:0.6b. Production request values remain fixed: stream=true, context 2048, output cap 64, temperature 0 and think=false after pinned-runtime compatibility confirmation. Synthetic prompt input is at most 256 UTF-8 bytes. Preserve the approved model digest/runtime from the readiness record; do not download or upgrade anything for this assessment.

No redirect handling, environment proxy discovery, hosted fallback, authentication key, automatic retry, model pull/login, shared-service kill or model unload belongs in the request path. One failure ends one request. A future test seam may inject an owned loopback fixture and clock internally; it must not become a public arbitrary-destination option.

HTTP status/media validation precedes decoder success: require 200 with application/x-ndjson, allowing media-type parameters. Reject redirects, non-2xx and unrelated media types. Keep non-success bodies bounded and private; do not echo their contents. A mid-stream error under 200 must still fail through the decoder. Public unavailable, timeout and missing-model categories/messages need a recorded extension to the current error map before transport implementation; they are not currently implemented categories.

## Deadline and cleanup design obligations

| Boundary | Existing mandatory policy | What must be demonstrated |
|---|---|---|
| Connect | At most 2 seconds, subject to remaining absolute budget | Stalled/refused connection has safe classification; no second attempt. Literal loopback prevents hostname lookup from expanding the destination policy. |
| Entire request | Absolute 60 seconds from request start, including request sending, headers and reads | Measure with a monotonic clock. Recompute remaining time before blocking operations. Slow progress must never renew the absolute deadline. |
| Headers and body idle | At most 10 seconds without received bytes, also bounded by absolute time | Missing headers, slow header trickles, stalled body and slow body trickles are distinct tests. Bound header bytes as well as waiting; select and document a finite header-size policy before coding. |
| Decoder | 65,536 bytes per record; 262,144 bytes total | Read bounded pieces, count all wire bytes, and do not read an unbounded body before passing it to the decoder. Preserve malformed/truncated/error behavior. |
| Cancellation | Cancellation before request, during blocked header/body reads and after partial output | Stop producing output/retries and release owned request resources within a declared, tested cancellation-latency budget. No polling/interrupt mechanism is selected by this assessment. |
| Cleanup | Owned fixture cleanup bounded to 10 seconds; no shared service termination | Close response/connection on success, protocol failure, timeout and cancellation. A close failure must remain a safe visible failure; it must not erase an earlier failure or silently certify success. |

Python documents HTTPConnection's timeout as a timeout for blocking operations, not this application's complete absolute deadline. A call such as response-header parsing may perform multiple internal reads; checking a clock only before/after the whole call can miss a slow-trickle deadline. A safe implementation must control or independently interrupt those waits and prove bounded cleanup. Resetting a socket timeout for each outer read alone is insufficient evidence. See [HTTP client timeout semantics](https://docs.python.org/3.12/library/http.client.html) and [socket timeouts](https://docs.python.org/3.12/library/socket.html#socket.socket.settimeout).

There is no selected cancellation API or header aggregate-byte cap yet. Those are concrete design carryovers, not defaults to invent while wiring live use. An owned fixture can prove that simulated server work ends after cancellation; that does not establish real Ollama in-flight cancellation. Keep actual server-side cancellation PENDING until observed, without weakening client cleanup requirements.

## Required future transport proof

Each row is a specification, **PENDING implementation and execution**. Tests must use independently owned synthetic loopback fixtures and deterministic clocks where suitable, without a GPU, model download, personal credentials or existing Ollama service. Retain real bounded socket tests for behavior that a mocked clock alone cannot prove. Faults run only in memory or disposable copies and must fail their intended assertion.

| Mapping | Inputs/boundaries | Required result and intended fault |
|---|---|---|
| LP-11/12 | Valid 200 NDJSON; 404 missing model; other failures; 200 HTML/JSON; malformed headers; error after partial text | Exact success only for valid protocol; fixed safe failures otherwise. Fault: trust status/body alone or ignore content type. |
| LP-16 connect/send | Stalled connection and request send | Bound waits within connect/absolute policy; zero retry. Fault: omit applicable timeout. |
| LP-16 headers | No headers, trickled status/header bytes, excessive headers | Idle, absolute and selected byte bounds hold. Fault: renew total budget for each arriving byte. |
| LP-16 body | No bytes, stalled partial line, endless slow progress | Idle/absolute deadlines both hold; no partial answer. Fault: rely only on idle timeout. |
| LP-17 | Cancellation before connection, during header/body wait and after text | Zero initial call when pre-canceled; otherwise stop/close within selected budget; no retry. Fault: check cancellation only between full records. |
| LP-18 | Owned fixture confirms work started, then cancellation | Observe fixture work termination separately from client closure. Real Ollama cancellation remains separately attributed. Fault: declare server stopped from client exit alone. |
| LP-19 | Synthetic private sentinels in pre-header, status, mid-stream and close failures | Absent from public messages, formatted chains and ordinary logs; safe failure remains visible. Fault: echo upstream exception. |
| LP-20/21 | Hostile redirect; proxy environment; tempting hosted fallback; unauthorized endpoint/model input | No redirect/proxy/hosted calls, including on failure. Reject selectors before transport. Fault: follow Location or use ambient proxy/fallback. |
| LP-22 | Timeout/protocol/read failure after partial text, including after done | One request only; never return partial success. Fault: reconnect/replay or return at done. |
| LP-24 | Success, failure, cancellation and cleanup failure | Owned response/connection closed, cleanup failure safe/visible, no shared process/model/volume changes. Fault: suppress close failure or terminate a shared service. |

Every retained case/fault must protect a named boundary; shared mutation kills do not prove duplicate cases. Tests must record actual request destinations/counts and cleanup outcomes, not only a PASS label. Integrate all applicable transport checks into the existing suite/inventory and clean-runner CI before claiming a completed provider connection.

## What remains for the learner

1. **Now: explain the decoder.** In your own words: why is done=true only a candidate, what happens on failure after it, and why can response be absent on terminal records? Review the assistant-authored 3.2 changes. No coding is needed to answer.
2. **Next: finish the decoder verification rung.** Work through Day 9 3.4 and 4.1–4.3, map required D-case variants, add missing retained tests/faults and integrate them. You own new test/harness changes unless you specifically authorize assistance. Keep prior checks and evidence intact. Record new exact hosted verification only after separately authorized publication.
3. **Later, if still wanted: scope transport before coding.** Allocate real time by swapping optional scope; settle the header cap, interruptible absolute deadline/cancellation design, fixed transport errors and fixture ownership. Then personally implement/test that complete slice or explicitly authorize that particular assistance. Do not create an empty transport module now.

Do not start Ollama, run a live curl, change /health, rerun migrations or stop pre-existing services to complete this assessment. A live model request is supplementary after transport proof, not a prerequisite for parser-only progress. Unknown work minutes remain unknown. No claim of model quality, first-token latency or production readiness follows from this assessment.

📚 Learn first: [Day 9 remaining checklist](../sprints/day-nine-jira-checklist.md), 3.4 and sections 4–5; [3.2 preparation and receipt](../learning/provider-completion-preparation.md); [Ollama streaming](https://docs.ollama.com/api/streaming) and [Generate API](https://docs.ollama.com/api/generate), framing/request fields only. These official links were opened October 23, 2026; they are not pinned-runtime execution evidence.
↩ Return: answer the three decoder questions, then complete retained decoder verification. Carry the unbuilt connection and all LP transport obligations into the next explicitly budgeted task. MER-10 remains open.
