# Scratch local provider streaming and error contract

Day 8 item 4.2. Assistant-authored planning specification at the learner's request, October 19, 2026. **Review COMPLETE; implementation, automated tests and isolated faults PENDING.** Actual review minutes unknown. No client, adapter, parser, retry mechanism or application endpoint is implemented by this document.

📚 Learn first: [Ollama streaming](https://docs.ollama.com/api/streaming), newline-delimited JSON and response media types; [API errors](https://docs.ollama.com/api/errors), errors before and after headers; [Generate API](https://docs.ollama.com/api/generate), completion and timing fields. Official references opened October 19, 2026; the future implementation must check them against pinned Ollama 0.40.6. Stop before framework clients or cloud integration.
↩ Return: use the acceptance table below when separately scoping the learner-written scratch client. Implement parser/transport checks with synthetic fixtures before claiming production readiness or correctness from a live model response. This specification does not authorize code changes.

## Scope and trust boundary

Merlin's future scratch provider client calls only the selected local Ollama generation endpoint. Ollama runs the model; Merlin validates the transport and protocol before treating any answer as complete. The existing process-liveness endpoint stays independent of model/database readiness. Personal Codex/OmniRoute routing is outside this application boundary.

Retain the pinned local model, digest, synthetic inputs and resource policies in [the readiness contract](../evals/local-model-readiness.md). This slice specifies explicit stream=true behavior; earlier stream=false probe results are not streaming-parser proof. No SDK/framework, persistence, tool execution, hosted fallback or extra model is needed. Generated text remains untrusted data and never becomes executable instructions or trusted HTML.

Only the agreed literal loopback destination 127.0.0.1:11434 and fixed local model are permitted. Never derive the destination, redirect target or model from prompt content. Reject unauthorized schemes/hosts/ports and hosted-model selectors before transport creation. Disable redirects and ambient proxy use for this local call. Do not invoke login, pull, remote tools, a gateway or another provider on failure. No credentials are needed. A future hosted route requires its own explicit consent, budget and policy; it is absent here.

## Response framing and completion

1. Check HTTP status and media type before consuming output as a successful generation. For success require HTTP 200 with application/x-ndjson (optional charset parameters allowed). Non-2xx responses are errors even if the connection completed normally. A JSON error response may use application/json. Never interpret HTML or another media type as model output.
2. Treat network chunks as arbitrary bytes. One chunk can contain several records, part of a record, or part of a UTF-8 character. Accumulate bytes until a full newline-delimited record is available; decode strictly only complete records or use an incremental strict decoder. Preserve original text order without inserting spaces or losing punctuation.
3. Accept LF and CRLF record endings; ignore whitespace-only lines within the same byte/time limits. Every nonblank record must be one JSON object. Reject invalid UTF-8, malformed JSON, duplicate object keys, non-finite numbers and non-object records. Never silently repair, skip or coerce a corrupt record.
4. Normal records must identify the expected model and carry a genuine Boolean done. A present response field must be a string; nonterminal generation records require it. A terminal metadata-only record may omit response or contain an empty response. An empty-string fragment is valid but does not count as a first generated-content event. Thinking content, if unexpectedly present with think=false, is not surfaced as the final answer or written to public logs.
5. Handle an error member before success/completion processing, regardless of HTTP 200, prior fragments or a concurrent done field. Stop with a generic provider error. Do not append error text to the generated answer. Ollama documents that mid-stream errors cannot change already-sent HTTP headers.
6. Exactly one done=true record is required. A candidate terminal record is not final success until the response ends cleanly with no additional nonblank records. Reject multiple completions, records after completion, model changes and wrong field types. Unknown metadata fields may be ignored within byte limits; they must not alter control flow or routing.
7. At EOF, accept a final non-newline-terminated record only if it is complete valid JSON satisfying the same schema. An incomplete UTF-8 sequence or JSON record is truncation. Clean EOF without done=true, including EOF after valid partial text, is an incomplete-generation error. Do not require a network chunk to end at a token boundary.
8. Provisional fragments may be displayed only as explicitly incomplete output. Do not persist, score or publish them as a completed answer after error, cancellation or missing completion. For this bounded smoke task require some nonempty final response content. done_reason=length is completed transport with a length-limited answer, not proof of task success. Exact READY compliance remains a separate content check.

## Bounds, retry policy and cancellation

Use the existing 2048 context, 64-output-token request cap and synthetic prompt at most 256 UTF-8 bytes. Parser policy: at most 64 KiB per record and 256 KiB cumulative response bytes, including delimiters, metadata and blank lines. Fail before accepting excess data; byte limits include the unfinished buffer so a missing newline cannot grow it indefinitely. An observed token count above the requested bound is failure. Output text must not change the request's limits.

Connection deadline is 2 seconds; total deadline is an absolute 60 seconds from request start, including connection, headers, initial loading and all reads. Add a 10-second maximum interval without received bytes, subject to the same total deadline. These are explicit future-client policies; the earlier curl probe did not prove an idle-read timeout. Resetting an idle timer on receipt must never extend the total deadline. Bound header reads, connection establishment and cleanup as well as body parsing. Respect transport cancellation while waiting; an EOF/exception caused by cancellation must not become success.

**Automatic retry count is zero.** No retry after timeout, malformed response, mid-stream error or user cancellation; no silent replay of partial generations. Report the classified failure and let a deliberate new caller action create a new request. A future retry policy requires separate design/effectiveness proof and must not reset the original operation budget or send data to another provider.

On cancellation/deadline/protocol failure, stop yielding data and close the request's connection/response. Distinguish a requested cancellation from an observed termination of server work. The application client must never kill a shared Ollama service, unload another request's model or stop unrelated processes to cancel one request. A disposable test may terminate only its own fixture/process group, with cleanup bounded to 10 seconds. Until supported in-flight cancellation is observed, record **server-side cancellation PENDING** and prevent the failed operation from being treated as complete or silently retried. Do not claim cancellation from a deadline that expired before the handler started.

## Safe errors and diagnostics

Return only fixed public messages/categories: unavailable, timeout, canceled, missing-model, invalid-response or provider-failure. Caller-visible responses and ordinary logs must not contain raw provider errors, exception/traceback text, prompts, generated private content, credential-bearing URLs, account configuration or local file paths. HTTP status is safe evidence when actually received; no received status is absent/unknown, not an invented HTTP 500. Never echo a failing payload to explain a validation error.

Synthetic fixtures may contain clearly artificial sentinels to prove redaction. Assert their absence in every public response and ordinary log path, including exceptions before headers, mid-stream, decoding and cleanup. Diagnostic artifacts must use explicit allowlisted fields such as category, synthetic case ID and measured timings; private raw logs are not automatic publication artifacts. Sanitization failure is a test failure, not grounds to remove the sentinel check.

## Planned cases and intended fault detection

All rows below are **PENDING implementation/test/fault execution**. They are specifications, not existing tests. A future fault must be isolated and fail its intended assertion; setup errors or a generic red result do not establish effectiveness. Keep the full case/fault inventory and actual failures when integrating into cumulative CI.

| ID | Input/boundary | Required outcome | Intended isolated fault |
|---|---|---|---|
| LP-01 | Valid fragments plus final completion | Exact ordered reconstructed response, one success | Drop/reorder/duplicate fragments |
| LP-02 | JSON record split at every byte boundary | Same result for every split | Parse individual network chunks |
| LP-03 | Multiple records in one chunk | Consume every record in order | Consume only first record |
| LP-04 | Multibyte UTF-8 character split across chunks | Preserve character | Decode each chunk independently |
| LP-05 | LF/CRLF, bounded blank lines, valid final record without newline | Consistent accepted result | Treat record delimiter as output or drop final record |
| LP-06 | Malformed JSON, duplicate keys or invalid UTF-8 | Invalid-response, no final success | Skip/repair corrupt record |
| LP-07 | EOF during a JSON or UTF-8 sequence | Truncation error | Discard unfinished tail and report success |
| LP-08 | Valid partial records but no done=true | Incomplete-generation error | Treat EOF as completion |
| LP-09 | JSON scalar/array; wrong response/done types; wrong model | Invalid-response | Coerce types or ignore identity |
| LP-10 | Terminal record with no text after valid fragments | Accept metadata-only completion | Require text in every record |
| LP-11 | Error object under non-2xx status | Generic classified error, no generation | Ignore HTTP failure |
| LP-12 | Error object mid-stream under HTTP 200, also with done=true | Generic error, partial output not committed | Trust HTTP 200 or prioritize done over error |
| LP-13 | Duplicate completion or record after done | Reject stream | Return immediately at first done and ignore trailing data |
| LP-14 | Empty fragments/terminal-only empty answer | No first-content timestamp; no successful smoke answer | Count empty output as generated content |
| LP-15 | Oversized record, unfinished buffer or cumulative blank-line/metadata flood | Stop at byte cap, bounded memory | Bound only completed/output text |
| LP-16 | Connect stall, no headers, idle stream, endless slow trickle | Correct connect/idle/absolute timeout classification | Reset total deadline for every chunk |
| LP-17 | Cancel before request, during blocked read and after partial output | No further output/retry; request resources close | Ignore cancellation until next complete line |
| LP-18 | Fixture confirms inference started, then client cancels | Observe owned fixture work termination or mark server cancellation PENDING/FAIL honestly | Claim cancellation from client exit alone |
| LP-19 | Private synthetic sentinel in provider, decoder or cleanup error | Sentinel absent in public output and ordinary logs | Echo raw exception/error payload |
| LP-20 | Local failure with an unauthorized hosted provider configured as a temptation | Exactly zero hosted transport calls, no redirects/proxy bypass | Fallback or retry through another provider |
| LP-21 | Unauthorized endpoint/model selector before transport; hostile redirect | Zero unauthorized requests | Validate only after connection or follow redirect |
| LP-22 | Transport/protocol errors after partial text | Zero automatic retries and no completed partial answer | Retry entire generation or commit partial answer |
| LP-23 | Valid terminal with length stop, unusual metadata, missing optional metrics | Preserve length-limit category; optional metrics unknown; metadata does not control routing | Treat missing metrics as zero or length stop as task success |
| LP-24 | Failure during response close or owned fixture cleanup | Public error remains generic; cleanup failure visible; no shared-service kill | Suppress cleanup failure or stop global service |

The table is a transport/protocol test specification, **not** the ≥20-case labeled golden set for AI quality. Synthetic local fixtures must exercise each distinct boundary and require zero external network use in CI. Live Ollama results are supplementary pinned hardware observations and cannot substitute for parser, retry, non-disclosure or cancellation tests.

## Evidence and handoff

Current manual observations stay in [local model readiness](../evals/local-model-readiness.md). Future code/test filenames are selected only when the implementation slice is agreed; do not create empty modules or tests now. Record case-level PASS/FAIL/PENDING and first failure only after execution. Measure request wall time, first byte and first nonempty generated-content delivery separately. With streaming, content-delivery latency still is not a direct timestamp of the model's internal first-token computation.

Day 8 item 4.2 is complete for **requirements review**. Every implementation, automated case, isolated fault and provider-client CI integration above remains **PENDING**. The original model watchdog, exact READY compliance failures, unmeasured resource peaks and unmeasured first-token latency remain open in their original evidence. No permission to rewrite application code, install packages or publish is implied.
