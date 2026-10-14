# Day 7: GET /health contract and learning guide

This document covers MER-8 step 2.1. A contract is a written agreement about what a client sends and what the server promises to return. Writing it first gives your implementation and your tests the same target. This is an assistant-authored draft for you to review and explain; it is not an implemented endpoint.

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
- Question 2: pending your explanation.
- Question 3: pending your explanation.

## What happens after this step

Step 2.2 uses this contract to write expected results for valid requests, unknown paths including `/.env`, unsupported `POST`/`PUT` methods and a forced handler error. Step 2.3 defines fixtures and cleanup. These take the remaining 15 + 10 minutes of section 2's 40-minute budget. Write those expectations before implementing the server in section 3.

The standard-library approach will use a request handler, not a file-serving handler. Python's `SimpleHTTPRequestHandler` serves files and therefore is unsuitable for this small route contract. The standard-library HTTP server is a local learning prototype; the later FastAPI comparison follows scratch implementation and verification.

Only after you have written and started the server in section 3, a smoke request will be:

```bash
curl --include --max-time 3 http://127.0.0.1:8000/health
```

That command sends a GET and displays response headers and body. A connection failure before any server exists is expected; it is not evidence that this unimplemented endpoint has failed its contract. A successful smoke request also does not replace the later negative cases and fault injections.

📚 Learn first: [Python JSON](https://docs.python.org/3.12/library/json.html), read `dumps` and `loads` when you reach implementation; the link was opened October 14, 2026.
↩ Return: complete your three explanations here, then move to [Day 7 step 2.2](../sprints/day-seven-jira-checklist.md). Keep implementation and runtime results pending until evidence exists.

## Current evidence

| Item | Status and evidence |
|---|---|
| Day 7 section 1 | Learner reports completion; this session did not independently reverify it. |
| Contract draft | Authored by the assistant; learner review and explain-back pending. |
| Port selection | PASS: brief loopback bind succeeded and was closed; availability is not reserved. |
| API implementation and runtime behavior | PENDING: no API feature code was written for this step. |
| Negative cases, fixtures and fault checks | PENDING: subsequent Day 7 steps. |
| Actual learner minutes | Unknown. |
