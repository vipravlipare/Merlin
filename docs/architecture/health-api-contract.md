# Day 7: GET /health contract and learning guide

This document covers MER-8 steps 2.1–2.3. A contract is a written agreement about what a client sends and what the server promises to return. Writing it first gives your implementation and your tests the same target. This is an assistant-authored draft for you to review and explain; it is not an implemented endpoint.

Tracker: [Day 7 checklist](../sprints/day-seven-jira-checklist.md), section 2; [MER-8](https://vipravlipare.atlassian.net/browse/MER-8).

## Learn the pieces before writing Python

📚 Learn first: [Python 3.12 HTTP server](https://docs.python.org/3.12/library/http.server.html), read `HTTPServer`, `BaseHTTPRequestHandler`, `send_response`, `send_header` and `end_headers`; stop before the file-serving handler examples. [The JSON specification](https://www.rfc-editor.org/rfc/rfc8259.html), read section 8.1 and the `application/json` media type registration in section 11. These links were opened October 14, 2026; Context7 was not used.

↩ Return: explain the method, address, port, path, status, headers and body below. Then review the contract in this file. No application code is needed for step 2.1.

Consider the request `GET http://127.0.0.1:8000/health`:

| Piece | Meaning in this endpoint |
|---|---|
| `GET` | The HTTP method: the client asks to read the health result. |
| `http` | The protocol used to communicate with the local server. |
| `127.0.0.1` | The IPv4 loopback address. Bind the server here to restrict its listening interface to loopback. |
| `8000` | The port: the numbered listening endpoint used to reach this server. It is separate from the URL path. |
| `/health` | The route: the path the application recognizes for this health request. |
| `200` | The response status code: this request succeeded. |
| `Content-Type: application/json` | A response header telling the client that the body is JSON. |
| `{"status":"ok"}` | The response body: a JSON object containing one string field. |

The HTTP status code and the JSON `status` field are different things. `200` is protocol information; `"ok"` is application data. Tests must check both. A response can contain the right body and still have the wrong HTTP code or content type.

## The contract

| Requirement | Agreed behavior |
|---|---|
| Server listening address | `127.0.0.1`, never `0.0.0.0` for this learning server. |
| Development port | `8000`, provided it is still available when you start the server. |
| Request | Method `GET`, path `/health`, no query string needed. |
| Request body | None required. |
| Credentials | None required or returned by this endpoint. |
| Success status | HTTP `200`. |
| Response content type | `application/json`. |
| Response body | A UTF-8 JSON object with exactly one field: `status`, whose value is the string `ok`. |
| Side effects | No database query, database write, file serving or external service request. |
| Meaning | The HTTP process can handle this request and produce its health response now. |
| Information exposure | No environment values, credentials, configuration paths or exception details in the response. |

An illustrative complete response could look like this; the server may also add ordinary HTTP headers:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 15

{"status":"ok"}
```

The example's body is 15 UTF-8 bytes without a trailing newline. If your serialization adds spaces or a newline, the length must reflect the actual bytes. The contract does not require HTTP/1.1 or this exact whitespace. Parse the JSON and compare its fields and values in tests; do not reject valid JSON solely because its formatting differs.

### Why there is no database check

This endpoint measures process liveness. It answers: “Can this HTTP process respond?” It does not answer: “Can Merlin reach PostgreSQL?” That would be a separate readiness concern.

If PostgreSQL is unavailable but this handler works, `/health` must still return the agreed healthy response. Requiring a database connection here would change the meaning of the endpoint. Likewise, receiving `200` proves nothing about login, ownership checks, AI providers or whether every feature works.

If the server is stopped, the client may get a connection error or timeout. There is then no HTTP response from this server. Do not confuse that with an HTTP `500`, which is a response from a server that encountered an error.

Loopback binding limits the listening interface; it does not authenticate callers. Other processes on your machine can contact it. Windows/WSL localhost forwarding can also make it reachable from your local Windows client. Do not treat this learning endpoint as an authorization boundary or a production deployment.

## How to do your 15-minute step

📚 Learn first: use the HTTP server reading above to distinguish the address/port from the handler's route, and the response headers from the body.
↩ Return: review this draft in your editor, explain it in your own words, and leave any unresolved decision explicit before writing code.

1. **Read and identify the pieces — 3 minutes.** Use the first table to explain what a client sends and what it receives.
2. **Review the contract — 8 minutes.** Open this file, check each requirement, and write your own short explanation of why `/health` does not access PostgreSQL. Keep the field name `status`, value `ok`, method `GET` and route `/health` consistent.
3. **Explain back and record your decision — 4 minutes.** Answer the questions below. Record actual time if known; 15 minutes is the planned budget, not observed elapsed time.

Open the file from your Ubuntu terminal:

```bash
code /home/vipra/Merlin/docs/architecture/health-api-contract.md
```

Press **Ctrl+Shift+V** for Markdown preview. Edit the Markdown itself to add your explanation.

Port 8000 was successfully bound briefly on `127.0.0.1` on October 14, 2026, then released without starting a server. That proves availability only at that moment. Before starting your eventual server, inspect listeners again:

```bash
ss -ltn '( sport = :8000 )'
```

A listening entry means the port is occupied. Do not terminate an unfamiliar process to free it. Choose another available port, such as 8001, and update the contract and later commands together. The actual server bind remains the final check because another process can acquire the port after inspection.

### Explain-back questions

1. If PostgreSQL is stopped, should this endpoint return `200`? Explain why.
2. What are the separate purposes of HTTP `200`, `Content-Type: application/json`, and `{"status":"ok"}`?
3. What changes if you bind to `0.0.0.0` instead of `127.0.0.1`, and why is that outside this contract?

Your answers:

- Question 1: pending your explanation.
    - Yes, the endpoint should still return 200 because the server connection is valid, and the request has succeeded.
- Question 2: pending your explanation.
    - The '200' or any number is to return how the server connection is, good or erroneous. The content type is to set the return content type, for example JSON. The status is to interpret the number and return the meaning of the number.
- Question 3: pending your explanation.
    - Replies with how the application data is doing according to the status.

## 2.2 — Expected results for requests and errors

This is the test-case part of the contract. Each row describes an input and the response that future tests must require. These are expected results, not observations from a running application.

📚 Learn first: [HTTP semantics, RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html), read sections 15.3.1 (200), 15.5.5 (404), 15.5.6 (405), 10.2.1 (Allow) and 15.6.1 (500); stop after those sections. Link opened October 14, 2026. A 405 response identifies a method unsupported by the target resource and includes its allowed methods. The particular JSON error messages below are our design decisions.
↩ Return: read the table and explain why an unknown path, an unsupported method and a handler failure have different results. Use these expectations when you later write the API and its tests.

All responses below use `Content-Type: application/json` and a UTF-8 JSON body. Compare parsed JSON objects exactly, allowing JSON formatting differences. Ordinary protocol headers are permitted. Error bodies contain only the specified `error` field.

| ID | Request or controlled condition | Expected HTTP status | Expected parsed JSON body | Additional requirement / error this catches |
|---|---|---|---|---|
| API-01 | `GET /health`, normal handler | `200` | `{"status":"ok"}` | Checks the successful route, status, content type and complete body; an arbitrary successful request is insufficient. |
| API-02 | `GET /missing`, an unrecognized route | `404` | `{"error":"Not found"}` | No fallback healthy response, redirect, directory listing or file content. |
| API-03 | `GET /.env`, an unrecognized sensitive-looking route | `404` | `{"error":"Not found"}` | Must not read or disclose an environment file. This explicit security regression remains separate from the ordinary unknown-path case. |
| API-04 | `POST /health`, no request body | `405` | `{"error":"Method not allowed"}` | Must include `Allow: GET`; must not run the healthy GET handler or write data. |
| API-05 | `PUT /health`, no request body | `405` | `{"error":"Method not allowed"}` | Must include `Allow: GET`; exercises the PUT dispatch separately from POST. |
| API-06 | `GET /health`, with an isolated test replacement that raises an exception containing `HEALTH_PRIVATE_SENTINEL` before response headers are sent | `500` | `{"error":"Internal server error"}` | Client receives a generic response, not a traceback, exception message, sentinel or partial healthy response. |
| API-07 | A normal `GET /health` after the API-06 test replacement has been removed | `200` | `{"status":"ok"}` | Confirms the failure did not terminate the server or leave the test replacement installed. |

### Decisions that prevent ambiguous tests

The routing decision comes first: an unrecognized path returns the generic 404 response, including when requested with POST or PUT. For the recognized `/health` path, GET is supported and POST/PUT return 405. The listed unsupported-method cases do not specify behavior for every HTTP method; broader method coverage must be designed explicitly rather than claimed from these two cases.

The forced error is created only inside an isolated test fixture. Do not add a public `/crash` route, special request header or query parameter to trigger it. The fixture and cleanup mechanism are designed in step 2.3; application code follows in section 3.

API-06 covers an exception before the HTTP response starts. Once a success status and headers have been sent, the server cannot replace them with a new 500 status. Keep health computation and JSON preparation before sending response headers. Handling errors during a partially written network response is a separate concern, not proof provided by this case.

For all cases, response headers and bodies must not expose credentials, environment values, private exception details or local file contents. Later disclosure tests should use synthetic fixture values and fake files, never real credentials or your actual `.env`. Exact JSON equality checks catch unexpected body fields; also inspect response headers for the synthetic sentinel. A correct status alone does not demonstrate non-disclosure.

Publication safety: `GET /.env` is a generic request used to test rejection of a sensitive-looking path. It does not disclose a real file, its contents or any credential. Keep this case in public documentation and tests; publish only synthetic fixture values and never copy private configuration into examples or evidence. The security requirement is that the server rejects the request and returns no file contents.

In later fault checks, deliberately change the healthy status/body, make an unknown path return health or serve a fake file, allow POST or PUT, omit `Allow`, or expose the synthetic exception message. The matching case must fail for the intended assertion. Keep these faults isolated and restore the working behavior; no executable tests or faults have been authored in this step.

Planned review budget: understand statuses (3 minutes), review the table (8 minutes), explain rejection/error differences (4 minutes), total 15 minutes. Actual minutes are unknown. The contract table is authored; implementation, test execution and fault-detection results are all PENDING.

## 2.3 — Test fixture, fault isolation and cleanup plan

A fixture prepares a controlled environment for a test and reliably removes it afterward. For this API, it provides a temporary local server, its actual URL and a way to replace the health computation safely. This section is a design, not executable fixture code.

📚 Learn first: [Python HTTP server](https://docs.python.org/3.12/library/http.server.html), review `HTTPServer` and request handlers; [Python socket servers](https://docs.python.org/3.12/library/socketserver.html), read `shutdown` and `server_close`; [pytest fixture cleanup](https://docs.pytest.org/en/stable/how-to/fixtures.html), read yield fixtures and safe teardown. Links verified October 14, 2026.
↩ Return: use the responsibilities and lifecycle below when you write the server and tests. Explain why shutdown must run outside the thread executing `serve_forever`.

### Files and responsibilities

| Planned filename | Responsibility |
|---|---|
| `app/health_api.py` | Route decisions, agreed JSON responses and request-handler construction. Accept a health-computation callable so tests can replace it for one isolated server. Importing this module must not open sockets or start threads. |
| `app/health_server.py` | Executable entry point: construct the real handler, bind development address `127.0.0.1:8000`, run the server and close it on interruption. No duplicated route logic. |
| `tests/test_health_api.py` | API-01–07 assertions, controlled loopback-server fixture, non-disclosure checks and shutdown/restart verification. Keep the fixture here initially rather than adding shared infrastructure without a second consumer. |
| Existing `tools/audit_python_cases.py` | Integrate the new cases and isolated API fault candidates into the existing case-effectiveness audit after implementation. Reuse the harness and complete-suite runner; do not create a second API fault framework. |

### Fixture lifecycle

1. Construct a fresh handler with the normal health callable or an explicitly injected test callable. Avoid mutable global fault flags.
2. Bind an `HTTPServer` to `127.0.0.1` and port `0`. Port zero asks the operating system to choose an available port atomically; read the assigned port from the server. The test URL uses this port, while the manual development contract retains port 8000.
3. Run `serve_forever` in a dedicated thread. Use explicit startup coordination and a bounded wait, not a fixed sleep or an unbounded retry loop. A startup failure must fail the fixture; it must not skip the tests.
4. Give the test its server URL and use a bounded HTTP client timeout, initially 3 seconds. Bound accepted-connection reads as well: a client timeout alone cannot stop a handler waiting for input. Read the complete response and close each client connection, including on assertion failure.
5. In teardown, call `shutdown` from the controlling test thread while the serving thread is active. Calling it from the serving thread can deadlock. Then call `server_close`, join the thread with a bounded timeout and fail cleanup if the thread remains alive. Close a bound socket even when startup fails; do not call a blocking shutdown on a loop that never started.
6. Prove the released address/port can be rebound and a fresh normal server can answer after shutdown. Test cleanup also when a request/assertion fails, not just after the happy path. Preserve the first functional failure and report any cleanup failure as additional evidence.

Use the server's own thread and socket only. Do not kill unrelated processes, delete real files, stop PostgreSQL or alter either existing database volume. Any synthetic file or private-looking sentinel belongs in pytest temporary storage and is removed by its fixture.

### Existing fault injections and new API coverage

The current suite already has Python, SQL, JavaScript, browser, database-lifecycle and migration fault audits. Those audits protect existing behavior; they do not prove coverage of an API that does not yet exist. The Python audit must explicitly inventory the new cases and applicable faults when they are implemented. A green run with no API cases is not API verification.

| Planned isolated fault | Required case detection |
|---|---|
| Healthy response has wrong status, JSON value/shape or content type | API-01 fails the corresponding response assertion. |
| Unknown route returns health instead of 404 | API-02 fails; API-03 also rejects sensitive-path fallback. |
| Unknown sensitive path serves a synthetic file | API-03 fails the body/non-disclosure assertion. Use no real private file. |
| POST or PUT is accepted, or 405 omits/wrongly sets `Allow` | API-04 or API-05 fails its method/status/header assertion. |
| Handler exception escapes, healthy response survives the error, or synthetic exception details appear in headers/body | API-06 fails its generic-response/non-disclosure assertion. |
| Fault replacement persists or server terminates after the exception | API-07 fails its recovery assertion. |
| Server binds broadly, leaks its socket or leaves its thread running | Fixture/binding and teardown checks fail independently of response cases. |

Each fault must apply to an isolated copy or that test server's handler dependency, restore in teardown, and be detected by the intended assertion. Setup failures, unexecuted cases, invalid mutations and timeouts are not substitutes for demonstrated detection. Integrate actual inventory and report validation into `tools/run_test_suite.py` in Day 7 section 4; do not merely add files that the audit never collects.

Retain the existing audit's subprocess timeout boundary around fault executions. Socket timeouts do not stop arbitrary faulty Python code, and `shutdown` itself waits for the serving loop. A stuck fault must be terminated within its owned subprocess and reported as a timeout, never left as an unbounded thread or mislabeled as a detected assertion failure.

Planned budget: responsibilities (3 minutes), lifecycle (4 minutes), fault/cleanup review (3 minutes), total 10 minutes. Actual minutes are unknown. All three section 2 design artifacts are now authored; learner understanding, application code and API fault verification remain pending.

## What happens after these design steps

Steps 2.2 and 2.3 are specified above. Section 2 totals 15 + 15 + 10 = 40 planned minutes. Review these expectations before implementing the server in section 3, including its CI scope decision first.

The standard-library approach will use a request handler, not a file-serving handler. Python's `SimpleHTTPRequestHandler` serves files and therefore is unsuitable for this small route contract. The standard-library HTTP server is a local learning prototype; the later FastAPI comparison follows scratch implementation and verification.

Only after you have written and started the server in section 3, a smoke request will be:

```bash
curl --include --max-time 3 http://127.0.0.1:8000/health
```

That command sends a GET and displays response headers and body. A connection failure before any server exists is expected; it is not evidence that this unimplemented endpoint has failed its contract. A successful smoke request also does not replace the later negative cases and fault injections.

📚 Learn first: [Python JSON](https://docs.python.org/3.12/library/json.html), read `dumps` and `loads` when you reach implementation; the link was opened October 14, 2026.
↩ Return: correct your three explanations here, review the 2.2 table, then review the fixture plan before [Day 7 section 3](../sprints/day-seven-jira-checklist.md). Keep implementation and runtime results pending until evidence exists.

## Current evidence

| Item | Status and evidence |
|---|---|
| Day 7 section 1 | Learner reports completion; this session did not independently reverify it. |
| Contract draft | Authored by the assistant; learner review and explain-back pending. |
| Port selection | PASS: brief loopback bind succeeded and was closed; availability is not reserved. |
| API implementation and runtime behavior | Learner authored the API and confirmed manual startup/shutdown/restart. The focused tests and complete suite passed; see [integration evidence](../testing/health-api-suite-integration.md). |
| Step 2.2 expected-result table | Authored by the assistant at your request; learner review pending. No cases executed. |
| Step 2.3 fixture and cleanup plan | Authored by the assistant; implementation and execution PENDING. |
| Executable API tests/fault checks | PASS locally: 17 API cases and 18 isolated faults integrated; full ten-stage suite PASS in 68.08 seconds. Remote API verification remains pending publication. |
| Actual learner minutes | Unknown. |
