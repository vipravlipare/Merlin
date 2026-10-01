# Part 01 — Waterfall, assumptions, scope boundary and stack decisions

**Status: planning only. Prepared and web-checked 2026-10-01. No application feature, test, installation, account, deployment or benchmark has been completed by this Part.**

## 1. The 166-hour reality check

**The full requested product cannot honestly fit into 166 beginner hours.** Building all three agents, a polished full-stack app, several framework rewrites, fine-tuning, multiple databases, Spring Boot, Kubernetes, cloud operations and interview readiness is too much. The corrected budget leaves **104.90 hours for learning and implementation**, including setup, testing and documentation. Of those hours, this draft assigns **42.00 to learning and 62.90 to implementation and verification**.

This is an aggressive estimate for narrowly defined slices, not a guarantee. It cannot buy production security assurance, high availability, expert mastery, sustained on-call experience or ownership at team scale. Local model quality and speed are unknown until measured on the learner's hardware.

The funded priority is the **from-scratch core through rung 2**. A rung is a release with a specific demonstrated capability. The cut line is **after rung 2 and before rung 3**: framework and extra-platform implementations receive zero committed hours. Rungs 0–1 remain MUST; rung 2 remains SHOULD-1 and the protected next learning priority. If work takes longer, ship the last complete rung and retain the unfinished core in the backlog. Do not replace the core with easier framework demos.

**Original dates remain checkpoints; original feature-complete promises do not survive the ledger.** Only 50.10 net hours exist by Day 19 and 71.15 by Day 26. The draft moves the Knowledge Core completion target to Day 26 and the Agentic Core target to Day 33; both remain conditional on passing their gates. An earlier release must name its actual smaller scope. Never label an incomplete slice MVP-1 or MVP-2. Day 37 still ships the highest completed rung; Days 36–37 add no features.

The 25 planning Parts are mentor-produced specifications. Reading, adapting and implementing them costs learner time in the ledger. Reading every linked page in advance is neither required nor free.

📚 Learn first (Must read): [Scrum Guide][R01], read “The Sprint” and “Commitment: Definition of Done”; stop after those sections; why: time limits and demonstrable completion constrain scope (~10 min, within C-01/C-22 learning).
Explain back before proceeding: Why does a list of desired features not establish a feasible commitment?
↩ Return to build: on Day 5, annotate the scope boundary in your project planning notes; done when every feature is funded, conditional or deferred and no incomplete feature is called built; time box: 10 min inside C-01; if stuck: hint rung 1—separate an available hour from a desired outcome.

## 2. Five assumptions, each with a default

| ID | Assumption or unresolved input | Default used here | Change trigger |
|---|---|---|---|
| A-01 | Actual OS, CPU, RAM, GPU/VRAM, disk space and administrator access | **Confirmed: Windows, 16 GB RAM, NVIDIA RTX 3050 with 4 GB VRAM.** Use Windows + WSL2/Docker route. Disk space, driver version, CUDA/WSL GPU pass-through and administrator rights remain open. Start with the smallest local model. | Day 1 records disk/driver/pass-through; Day 8 measures fit. No GPU purchase is assumed. |
| A-02 | Meaning of $0 and cloud eligibility | Zero new out-of-pocket service/software/hardware spend; existing computer, power and internet excluded from the service budget. Local execution is the default. No paid-plan enrollment, card hold or purchased API credit is presumed acceptable. | Verified eligible free account and learner's account choices permit an optional cloud demonstration. |
| A-03 | Product audience and data | Personal app first, two seeded test identities for isolation tests. Synthetic expense CSV and learner-authored notes first. Public demo contains seeded data only. | Multi-user public deployment or real sensitive data requires the security gates, not merely a UI toggle. |
| A-04 | Repository, accounts and outside reviewers | GitHub/Jira Free; repository visibility is undecided and remains unchanged. Public code later is useful for the portfolio but needs a deliberate learner decision. Human reviewer availability is not guaranteed. | Account feature limits or inability to find a reviewer; record the gap instead of fabricating a review. |
| A-05 | Capacity and priorities | Exactly the 166-hour floor; no stretch-funded feature; scratch AI core outranks framework breadth. One shared agent runtime with three role/tool profiles. Optional scopes are swaps. | Re-estimate after S0 and every Monday using actual completed work; a bad week changes scope, not the deadline. |

📚 Learn first (Must read): [Install WSL][R02], read prerequisites and installation overview; stop before customization (~5 min); [Ollama FAQ][R03], read model loading, concurrency and memory discussion; stop before proxy configuration (~5 min). Why: OS compatibility and model download size do not establish runtime fit.
Explain back: What else consumes memory besides model weights?
↩ Return to build: Day 1, record OS/architecture, RAM, GPU/VRAM, free disk and virtualization availability in your future setup record; done when the model sizing decision has measured inputs; time box: 10 min within C-02; if stuck: hint rung 1—record “unknown” and inspect system information before choosing a larger model. No installation is performed by this Part.

## 3. Capacity contract

### 3.1 Recomputed calendar and waterfall

A **floor** is the time actually available; a **reserve** is uncommitted recovery time. A **ritual** is recurring review/logging work. Neither is feature implementation.

Build days are **14 A days** (Monday/Wednesday/Friday), **10 B days** (Tuesday/Thursday) and **8 C days** (Saturday/Sunday).

| Calculation | Hours |
|---|---:|
| S0: 1.5 + 1.5 + 3 + 3 + 1 | 10.00 |
| Build: 14 × 4 + 10 × 6 + 8 × 5 | 156.00 |
| Total floor | **166.00** |
| Exact 10% reserve: 166 × 0.10 | −16.60 |
| Committed work ceiling | **149.40** |
| Build DSA: 14 × 0.25 + 18 × 0.50 | −12.50 |
| Chill DSA: 5 × 0.25 | −1.25 |
| Build daily rituals: 14 × 0.50 + 18 × 0.75 | −20.50 |
| Chill daily rituals: 5 × 0.25 | −1.25 |
| Monday ceremonies: Days 12, 19, 26, 33 × 1.00 | −4.00 |
| Sunday extras: 4 mocks × 0.75 + 4 re-quizzes × 0.25 + 2 audits × 0.50 | −5.00 |
| Net learn + implement/verify/document | **104.90** |
| Learning | **42.00** |
| Implementation, setup, designed tests, debugging and evidence | **62.90** |

Thus **42 + 62.9 + 13.75 + 21.75 + 9 + 16.6 = 166**. Learning is 40.04% of the 104.9-hour net.

Corrections to the prompt's approximate waterfall: 10% is 16.6, not 16; build rituals are 20.5, not 20; chill DSA and rituals also consume 2.5 of the ten chill hours. Only **7.5 chill hours** remain for setup/learning. Monday Day 5 planning is inside its chill net block, not an extra fifth one-hour ceremony.

Sunday rules: reserve/catch-up first; mocks Days 11/18/25/32; AI system-design mocks on **both** Days 25 and 32. Audit Days 11 and 25 only. Sunday extras are 90/60/90/60 minutes, separately visible from daily rituals. This follows the explicit every-other-week audit cap over the conflicting “weekly audit” wording. The same activity is never billed twice.

Daily rituals cover a brief stand-up, state/log update, quiz/re-quiz scheduling, PR/Jira housekeeping and read-only AI review. Technical testing and fixing belong to component implementation. If a review or log exceeds its ritual budget, consume that day's component block or record reserve use; do not work invisibly.

### 3.2 Sprint capacities and reserve locations

| Sprint | Dates / days | Floor | Reserve | DSA | Daily rituals | Extra ceremonies | Net L+I |
|---|---|---:|---:|---:|---:|---:|---:|
| S0 | Oct 1–5 / 1–5 | 10.00 | 0.00 | 1.25 | 1.25 | 0.00 | **7.50** |
| S1 | Oct 6–12 / 6–12 | 34.00 | 3.20 | 2.75 | 4.50 | 2.50 | **21.05** |
| S2 | Oct 13–19 / 13–19 | 34.00 | 3.20 | 2.75 | 4.50 | 2.00 | **21.55** |
| S3 | Oct 20–26 / 20–26 | 34.00 | 3.20 | 2.75 | 4.50 | 2.50 | **21.05** |
| S4 | Oct 27–Nov 2 / 27–33 | 34.00 | 3.20 | 2.75 | 4.50 | 2.00 | **21.55** |
| S5 | Nov 3–6 / 34–37 | 20.00 | 3.80 | 1.50 | 2.50 | 0.00 | **12.20** |
| Total | 37 days | **166.00** | **16.60** | **13.75** | **21.75** | **9.00** | **104.90** |

For each full build week, reserve is Tue 0.6, Wed 0.2, Thu 0.6, Fri 0.2, Sat 0.4, Sun 1.0, Mon 0.2 hours. S5 reserve is Day 34 0.4, Day 35 0.2, Day 36 **3.0**, Day 37 0.2. Reserve covers unexpected work on committed scope; unused reserve is not automatically a feature budget.

Stretch ceilings are 8 hours on B days and 6 on C days: at most 10 × 2 + 8 × 1 = 28 extra hours, or 194 total. Stretch is catch-up only; S0 has no stretch.

### 3.3 Points and reconciliation

A **story point** is a rough relative size, not a productivity grade. For initial planning only, use **1 point ≈ 1.5 net beginner hours**, including learning, implementation and technical verification. Do not convert 166 into feature points.

The 104.9-hour net is about **69.9 point-equivalents**, not a promise to deliver 70 integer points. Sprint net ceilings are approximately 5.0 / 14.0 / 14.4 / 14.0 / 14.4 / 8.1 point-equivalents. Later stories use Fibonacci values and are split to fit a real day; an eight-point story is too large for this calendar despite the generic ≤8-point rule. Tasks remain ≤90 minutes and daily implementation steps ≤45 minutes. Do not sum parent Story estimates and their child Task hours as separate effort.

At Day 5, compare actual versus estimated hours for completed setup outcomes. Re-estimate the remaining components, preserve reserve, and replace these planning priors with measured throughput. S0 setup velocity does not prove feature velocity; recalibrate again on Day 12.

📚 Learn first (Must read): [Scrum Guide][R01], read “Sprint Planning” and “Sprint Review”; stop before “Sprint Retrospective”; why: choose a feasible forecast and inspect actual outcomes (~8 min).
Explain back: If ten hours of work were incomplete, why are they not ten hours of delivered value?
↩ Return to build: Day 5, write actual/estimated hours and the next sprint's bounded forecast in your project state; done when each promised outcome fits the net capacity and reserve remains explicit; time box: 15 min within C-01; if stuck: hint rung 2—list completed outcomes first, then size only the remaining work.

## 4. Security constraints before stack choices

A **threat model** describes assets, who can cross each boundary, how misuse could occur, and the test that proves a defense. **Authentication** establishes identity; **authorization** decides what that identity may do.

📚 Learn first (Must read): [OWASP Threat Modeling][R04], read “System Modeling” through “Review and Validation”; stop before development-team discussion (~15 min); [OWASP Authorization][R05], read “Deny by Default” and “Validate the Permissions on Every Request”; stop after those recommendations (~10 min).
Explain back: Why must a valid logged-in user still be prevented from retrieving another user's chunks?
↩ Return to build: before C-04/C-05 design on Day 6, draw the following boundaries in your design notes and write one negative case for each; done when every crossing has an identity, data classification and denial behavior; time box: 25 min inside those components; if stuck: hint rung 1—an authenticated request is not necessarily an authorized request.

| Boundary / asset | Threat | Core acceptance criterion |
|---|---|---|
| Browser → API / session | Stolen, expired or tampered identity; guessed record ID | Password hashing, short-lived validated JWTs and simple roles are core; identity is server-derived; two test users cannot read, edit, export or search one another's records. |
| API → database / notes and expenses | Unscoped query or unsafe input | Parameterized queries and mandatory owner filtering; retrieval joins and vector queries preserve the filter; negative tests include guessed IDs. |
| Uploaded file → ingestion | Bad format, path traversal, repeated ingestion, malicious content | Bound size/type; treat content as data; repeat import does not duplicate records; failure is visible and retryable. |
| Browser rendering / request origin | Script injection, forged cross-origin mutation or resource exhaustion | Render markdown safely; explicit allowed origins; CSRF protection when cookie authentication is used; input and request/login/model-call limits. C-05/C-23 fund baseline controls; a Redis-based extension is optional. |
| Retrieved text/tool result → model | Prompt injection attempts to change rules or expose data | Never treat document text as permission; tools enforce authority independently; injection tests include cross-user requests and forged approvals. |
| Agent/MCP → mutation | Unauthorized or replayed action | Approval binds actor, tool, exact arguments and expiry; changed arguments require new approval; denied/replayed requests do not mutate data. |
| App → hosted provider | Private information leaves the machine | Hosted routing disabled by default; no automatic local-to-hosted fallback; explicit per-request consent and redaction precede any network request. |
| Logs/backups/repository | Secret or private-data exposure | No credentials or raw financial/private-note text in public artifacts; seeded demonstrations; restore tested; audit metadata records decisions without full sensitive content. |
| Network/storage | Eavesdropping or stolen disk | No public app until transport encryption is verified; at-rest mechanism and coverage must be recorded, not inferred from use of Docker or Postgres. |

The requested **AES-256 at rest** is a specific, currently unverified requirement. Full-disk encryption may use a different configuration; a product name alone is not proof. Verify algorithm, protected volumes, recovery-key handling and backup protection. Windows edition/configuration can constrain BitLocker; macOS FileVault is not automatically evidence of the exact AES-256 requirement. Until a suitable $0 mechanism is verified, use synthetic data and record the gap. **TLS 1.3** must be verified on the actual exposed network path. Loopback-only development is a documented restricted mode, not a claim that plaintext traffic is TLS.

📚 Learn first (Must read): [OWASP Cryptographic Storage][R06], read “Where to Perform Encryption” and algorithm guidance (~8 min); [OWASP TLS][R07], read protocol/certificate recommendations (~7 min); [BitLocker overview][R08], read requirements and management overview (~5 min). Stop before implementation examples; why: encryption claims need an identified mechanism.
Explain back: Which copy of the data would remain exposed if only the main database volume were protected?
↩ Return to build: C-02/C-05, add a storage/transport evidence row to your setup/security notes; done when algorithm, coverage and a verification result are recorded or the release is explicitly restricted to synthetic local data; time box: 20 min within those budgets; if stuck: hint rung 1—list every persisted copy and every network hop.

## 5. Initial architecture decision records

An **ADR** is a short record of context, options, decision, trade-offs and how to explain the choice. All decisions below are planning choices; they have not been validated by a working stack.

### ADR-01 — One Python application, learner-written code

- **Context:** Python is the strongest existing skill; operating many services would consume learning time.
- **Options:** one modular application; separate services; a second primary Java backend.
- **Decision:** Python + FastAPI, with clearly separated notes, tasks, ingestion, retrieval and agent modules. One worker process only if a job must outlive a request; it uses the same codebase. Spring Boot is deferred.
- **Trade-offs:** fewer deployment boundaries and languages; less independent service scaling. A **modular monolith** means one application whose internal modules have clear responsibilities.
- **60-second explanation:** “I kept one backend because my constraint was learning and finishing a secure slice. Module boundaries let me test responsibilities without spending the project budget operating microservices.”

📚 Learn first (Must read): [FastAPI Tutorial][R09], read the tutorial introduction and “First Steps” via its navigation; stop before path-parameter details (~15 min).
Explain back: What responsibility belongs in the API boundary rather than the note-storage module?
↩ Return to build: C-06 on Days 6–9, write your own API boundary specification, then your first health endpoint; done when your designed success/failure cases pass and the response contains no secrets; time box: first 30-minute slice inside C-06; if stuck: hint rung 1—start with a single request and response. Do not copy the tutorial's full application.

### ADR-02 — PostgreSQL first; exact vector search before extra databases

- **Context:** Notes, tasks, owners and sources have relationships; retrieval must preserve ownership.
- **Options:** PostgreSQL + pgvector; MongoDB plus a separate vector database; multiple stores immediately.
- **Decision:** PostgreSQL is the authoritative store. SQLAlchemy translates Python database operations; Alembic records ordered schema changes that the learner writes. pgvector stores embedding vectors beside source metadata. Start with hand-written cosine/brute-force nearest-neighbor calculation, then exact pgvector search; approximate indexes only after a measured need.
- **Trade-offs:** one backup/authorization boundary, but careful schema and query design are required. MongoDB document-store depth B and Chroma/Qdrant comparison are unfunded. Redis is an optional running service during setup, not a claim of implemented caching/queues.
- **60-second explanation:** “I kept data and access-control metadata together. I first measured exact retrieval, then could justify an approximate index using recall and latency rather than choosing a database by fashion.”

📚 Learn first (Must read): [PostgreSQL tutorial][R10], read architectural fundamentals, tables and transactions (~20 min); [pgvector][R11], read “Getting Started” and “Querying”; stop before index tuning (~15 min); [Alembic tutorial][R12], read migration-environment overview; stop before generated code (~10 min).
Explain back: Why can a fast nearest-neighbor result still be a security failure?
↩ Return to build: C-04/C-11 on Days 6–7 and 16–21, specify owner/source keys and vector-version fields in plain tables, then write the migration and retrieval yourself; done when cross-user retrieval returns no records and exact results match your small hand-computed example; time box: first 45-minute slice per component; if stuck: hint rung 2—filter the candidate records before ranking, and test that boundary separately.

📚 Learn first (Must read): [SQLAlchemy Unified Tutorial][R36], read overview and transaction concepts; stop before object-mapping examples; why: distinguish Python objects from database transactions (~10 min, reused by LR-03).
Explain back: What must happen to both writes when the second write fails?
↩ Return to build: C-04 on Day 7, specify the rollback case before writing persistence code; done when the expected database state is explicit; time box: 15 min within C-04; if stuck: hint rung 1—one transaction has one success/failure boundary.

### ADR-03 — Local models, explicit provider boundary

An **embedding** is a numerical representation used to compare meaning. **RAG** retrieves evidence before asking a language model to answer. A **provider adapter** translates the application's request into a model provider's format.

- **Context:** $0 and private data are hard constraints; local hardware is unknown.
- **Options:** local Ollama; hosted inference; a provider interface with controlled routing.
- **Decision:** Ollama is the only enabled route initially. The learner writes the interface, streaming parser, timeout/retry policy, structured-output validation and usage accounting. A hosted adapter may be contract-tested against synthetic fixtures; actual hosted integration is unclaimed until a live authorized free run is possible. Hosted retry/fallback never bypasses consent.
- **Trade-offs:** no service charge for local inference, but hardware, electricity and slower throughput remain real. A small local model may not meet task or tool-selection targets. Recorded outputs test contracts, not live quality.
- **60-second explanation:** “I made data movement and spend an explicit decision. Local failure produces a visible error; it does not silently send private notes to a paid provider.”

📚 Learn first (Must read): [Ollama API introduction][R13], read base URL and API overview (~5 min); [Ollama streaming][R14], read newline-delimited responses (~10 min); [Ollama embeddings][R15], read model and embedding usage (~10 min). Stop before copying examples.
Explain back: Why must Ollama's streamed response format be parsed before being converted into browser events?
↩ Return to build: C-09 by Day 8, specify one streaming request, malformed output, timeout and usage record; done when your own implementation handles those cases and a blocked hosted route sends zero network requests; time box: first 45-minute slice in C-09; if stuck: hint rung 2—test a recorded stream before a live model.

| Model candidate | Verified publisher license / package | Selection rule |
|---|---|---|
| Qwen3-0.6B / Ollama qwen3:0.6b | [Publisher card][R16], Apache-2.0; [Ollama package][R17], Q4_K_M, 523 MB, short ID 7df6b6e09427 | First hardware/latency probe; no claim of adequate agent quality. |
| Qwen3-1.7B / Ollama qwen3:1.7b | [Publisher card][R18], Apache-2.0; [Ollama package][R19], Q4_K_M, 1.4 GB, short ID 8f68893c685c | Compare only if memory headroom exists; use the same cases. |
| nomic-embed-text-v1.5 | [Publisher card][R20], Apache-2.0; [Ollama catalog][R21], 274 MB package listed | Respect query/document prefixes; verify installed vector dimension and truncation/context behavior. |

Download size is not RAM/VRAM demand. Run one model request at a time, start with a bounded context, record available/peak memory, warm/cold latency and tokens/sec, and stop increasing size if the machine swaps or fails. Record full installed model digests; short IDs and mutable tags are insufficient reproducibility pins. These are license findings for named artifacts, not permission to redistribute unrelated scraped corpora. Part 2 scouts at least three public corpora and three fine-tuning datasets; none is selected here.

📚 Learn first (Must read): [Qwen3-0.6B model card][R16], read model limitations and license label (~5 min); [nomic model card][R20], read usage/task-prefix guidance and license (~10 min); [Ollama FAQ][R03], read memory/concurrency guidance (~5 min).
Explain back: Why can the same model file run with different memory and latency on different context lengths?
↩ Return to build: Day 8, record the chat-model digest and a bounded hardware smoke benchmark in your future docs/evals record; done when memory and throughput are measured and license attribution is recorded; time box: 30 min within C-09. Record the embedding artifact separately on Day 16 within C-11; if stuck: hint rung 1—reduce concurrent services and context before increasing model size.

### ADR-04 — Minimal React interface and ordinary HTTP

- **Context:** TypeScript/React are beginner topics; the UI must expose real system behavior.
- **Options:** React with hooks/Context; adding Zustand or Redux now; multiple native apps.
- **Decision:** React + TypeScript, hooks and Context first. A hook is a React mechanism for state and lifecycle behavior. No global state library is funded until a concrete state-sharing problem justifies it. Browser streaming uses **server-sent events (SSE)**, a one-way HTTP event stream; do not confuse it with Ollama's newline-delimited JSON.
- **Trade-offs:** small surface, limited polish; no mobile/native app, virtualized graph canvas or cross-device real-time sync. Fund login, notes/tasks, citations and minimal approval/tool-trace cards. Preserve safe saves, export/restore, a minimal keyboard path and dark mode; no elaborate editor.
- **60-second explanation:** “I limited UI scope to the paths proving the backend and AI behavior. State stays near its owner, and streaming is a transport detail with explicit loading, cancellation and failure states.”

📚 Learn first (Must read): [React Quick Start][R22], read components, events and sharing state; stop before the tutorial link (~25 min); [TypeScript Handbook introduction][R23], read purpose/prerequisites; stop at the next chapter (~5 min); [MDN SSE][R24], read concepts and event-stream format (~10 min).
Explain back: Which state is saved on the server, and which state should disappear when the page reloads?
↩ Return to build: C-15 beginning Day 13, write props/state/events and loading/error behavior before manually writing components; done when the learner can explain the re-render caused by each event and the first form works with a real API; time box: first 45-minute slice within C-15; if stuck: hint rung 1—build one field and one request before a full screen.

### ADR-05 — Local release first; AWS is conditional

- **Context:** A cloud budget alarm does not guarantee a zero bill, and model hosting may exceed free resources.
- **Options:** local Compose; an eligible AWS Free plan demonstration; paid AWS; moving to another cloud.
- **Decision:** Docker Compose is the reproducible local release. AWS remains the preferred optional deployment learning path with least privilege, logs and teardown. Do not enroll in a Paid plan to satisfy a keyword. GCP is not an automatic workaround; its terms would require a new ADR and a funded swap. No hosted Kubernetes, NAT Gateway or always-on public model server.
- **Trade-offs:** a local demo and runbook provide evidence but do not prove cloud operations. A cloud API unable to reach a real model is a partial deployment; no end-to-end cloud AI claim. No promise that a free compute instance can run Ollama.
- **60-second explanation:** “I separated deployment evidence from service availability. If my account cannot demonstrate a protected zero-cost route, I ship reproducibly locally and label AWS studied.”

📚 Learn first (Must read): [Docker Compose application model][R25], read services/networks/volumes; stop before the example (~10 min); [AWS Free Tier FAQ][R26], read eligibility, credits and expiration (~10 min); [AWS Budgets][R27], read alert limitations (~5 min).
Explain back: What could accrue charges before a budget alert arrives?
↩ Return to build: Day 2, record account eligibility without creating paid resources; later C-21 receives at most 3 net hours for one deployment path and teardown verification; done when cost eligibility is evidenced or the release is explicitly local-only; time box: 25 min on Day 2 within C-02; if stuck: hint rung 1—“unknown eligibility” means use the local route.

### ADR-06 — Scratch loop before frameworks; same evidence for comparison

An **agent** is a bounded loop that chooses permitted tools and uses their results. **MCP** is a protocol for exposing tools, resources and prompts to compatible clients. A **framework** supplies reusable orchestration abstractions.

- **Context:** The learning goal requires understanding control flow and permission checks.
- **Options:** handwritten loop; framework-first agent; handwritten loop followed by a measured rebuild.
- **Decision:** Handwritten tool registry → bounded loop → three role/tool profiles → MCP server/client → approval and evaluation gates. Use the official MCP SDK for protocol handling; “from scratch” does not mean rewriting the wire protocol or cryptography. Framework builds are conditional later work.
- **Trade-offs:** more explicit code to explain and debug; less prebuilt orchestration. Three profiles share a runtime, tools and storage; they are not three independent systems or a multi-agent supervisor.
- **60-second explanation:** “I proved my own state transitions, permissions and stopping rules first. A framework earns its place only if the same cases show an advantage I can explain.”

📚 Learn first (Must read): [Ollama tool calling][R28], read the single-call flow; stop before parallel examples (~10 min); [MCP architecture][R29], read participants and protocol layers; stop before detailed lifecycle examples (~15 min); [OWASP prompt injection][R30], read indirect injection and tool-related defenses (~10 min).
Explain back: Why is valid tool-call JSON not permission to execute it?
↩ Return to build: C-13/C-14 on Days 20–33, write allowed transitions, max steps, timeouts, scope checks and approval-replay cases before implementation; done when denial, bounded termination and approved mutation pass your tests; time box: first 45-minute slice in each component; if stuck: hint rung 2—drive one tool call with a recorded response before allowing model selection.

**Mandatory order for every conditional rebuild:** passing handwritten baseline → pinned framework version on the same data → comparison ADR. Compare correctness, code size, flexibility, debugging effort, latency, tokens/cost, lock-in and when each is appropriate. No generic “framework is better” claim.

### 5.1 Released planning pins, not a tested dependency lock

“Verified” below means the official release evidence was read on **2026-10-01**. It does not mean installed, mutually compatible, vulnerability-free or benchmarked. Recheck security advisories and resolve the learner's lockfiles on first use. If compatibility fails, change the pin in an ADR instead of installing “latest” silently.

Before **every** MCP/framework implementation session, re-read the pinned official documentation and changelog. Exact API details remain **🔎 verify** until checked for that installed version; checking a release number does not verify a method signature.

| Layer | Exact planning pin | Official release evidence | First use |
|---|---|---|---|
| Python | 3.12.15 | [Release][V01] | S0; 🔎 verify uv binary availability because upstream security release is source-only |
| uv | 0.12.21 | [Releases][V02] | S0 |
| Node.js | 24.21.0 LTS | [Release schedule/current LTS][V03] | S0 hooks; app tooling Day 13 |
| pnpm | 12.8.1 | [Releases][V04] | S0 |
| Docker Desktop | 4.93.0 | [Release notes][V05] | S0 Windows/macOS; Ubuntu Engine/Compose exact packages verified in Part 4 |
| FastAPI | 0.142.2 | [Release notes][V06] | Day 6 |
| PostgreSQL | 17.11 | [Release notes][V07] | S0/S1 |
| pgvector | 0.8.6 | [Changelog][V08] | Day 16 |
| React / react-dom | 19.3.0 / 19.3.0 | [Versions][V09] | Day 13 |
| TypeScript | 6.0.3 | [Releases][V10] | Day 13; deliberate conservative candidate, not latest-major claim |
| Ollama | 0.35.0 | [Releases][V11] | By Day 8 |
| MCP Python SDK | 2.2.0 | [Releases][V12] | Day 23 target, only after tool boundary exists |
| MCP protocol documentation | 2026-07-28 | [Versioned architecture][R29] | Day 23; negotiation/SDK compatibility 🔎 verify |
| LangChain + LangGraph | 1.4.3 + 1.2.12 | [LangChain][V13], [LangGraph][V14] | Unfunded; earliest Day 27 only if scratch core already complete |
| LlamaIndex | 0.14.25 | [Releases][V15] | Unfunded; earliest Day 29 |
| n8n | 2.41.4 | [Releases][V16] | Unfunded; earliest Day 28 |

🔎 **Pin-completion gate:** SQLAlchemy, Alembic, Pydantic, Pandas, NumPy, pytest, auth libraries, UI build tool, Redis, lint/scan tools and platform installers need exact compatible versions in Part 4 or their first-use Part. The current proposal does not invent a resolved dependency graph. No install-ready environment or runnable framework recipe is claimed here. Container images and actions must also have recorded immutable digests/commit identifiers. Hosted model ID is intentionally unselected while that route is disabled.

📚 Learn first (Must read): [uv Python management][R31], read managed Python and version selection (~8 min); [Semantic Versioning][R32], read specification items 1–8; stop before FAQ (~7 min).
Explain back: Why does an exact application version still fail to pin its transitive dependencies?
↩ Return to build: C-02/C-03, record requested versus resolved versions and the clean-install result in your setup evidence; done when another clone reproduces the same supported stack or the incompatible pin is documented; time box: 20 min within setup; if stuck: hint rung 1—separate interpreter, direct package, transitive package and model artifact.


## 6. Component ledger and cut line

**L = learning; I = learner implementation plus technical verification, setup and evidence.** Low/likely/high describe the same bounded slice under different debugging/learning outcomes; they are not measured velocity. Zero-funded rows mean deferred, not zero effort. Each estimate includes the relevant Learn → Return work in this Part; repeated references are refreshers, not extra reading assignments.

| Component | Skills | Low L / I | Likely L / I | High L / I | Likely total | Window and bounded slice |
|---|---|---:|---:|---:|---:|---|
| C-01 Repo & tooling | SK-22 | 0.75 / 1.25 | 1.00 / 2.00 | 1.50 / 3.50 | 3.00 | S0/S1: Git/Jira workflow, small PRs and setup specs |
| C-02 Environment & Compose | SK-19 | 2.00 / 2.00 | 3.00 / 3.00 | 4.00 / 5.00 | 6.00 | S0/S1: One local stack; account/hardware check; no extra platform installs |
| C-03 CI/CD & gates | SK-19/20 | 1.50 / 2.00 | 2.00 / 3.00 | 3.00 / 5.00 | 5.00 | S0–S4: CI skeleton, image build, later evaluation gate; no paid review bot |
| C-04 Data layer | SK-4/18 | 1.50 / 2.00 | 2.00 / 3.00 | 3.00 / 5.00 | 5.00 | S1/S2: Owner-scoped schema, learner-written migrations, restore path |
| C-05 Identity/security core | SK-21 | 1.00 / 1.50 | 1.50 / 2.50 | 3.00 / 5.00 | 4.00 | S1–S3: Password hashing, short-lived JWT, owner checks; no refresh/MFA app feature |
| C-06 API foundation | SK-4 | 1.00 / 1.50 | 1.50 / 2.50 | 2.50 / 4.00 | 4.00 | S1: Health, validation, error contract and module boundaries |
| C-07 Notes engine | SK-2/3/18 | 1.50 / 2.00 | 2.00 / 3.00 | 3.00 / 5.00 | 5.00 | S2/S3: Plain markdown, folder tree, tags/backlink list, safe saves/export |
| C-08 Task planner | SK-3 | 1.00 / 1.50 | 1.50 / 2.50 | 2.50 / 4.00 | 4.00 | S2/S3: Heap ordering and deadlines; recurrence deferred |
| C-09 LLM gateway/Ollama | SK-5/6 | 3.00 / 3.50 | 4.00 / 5.00 | 6.00 / 8.00 | 9.00 | S1–S3: One local provider, bounded streaming/structured output, hosted route disabled |
| C-10 Ingestion | SK-1/8 | 2.00 / 3.00 | 3.00 / 4.00 | 4.50 / 6.50 | 7.00 | S2/S3: Markdown + fixed expense CSV schema; idempotent retry; PDF/HTML deferred |
| C-11 Embeddings/vectors | SK-1/7/9 | 2.00 / 2.50 | 2.50 / 3.50 | 4.00 / 6.00 | 6.00 | S2/S3: Hand-computed comparison, exact search, owner filter and versioned vectors |
| C-12 RAG/evaluation | SK-10/20 | 2.00 / 3.00 | 3.00 / 4.00 | 4.50 / 6.50 | 7.00 | S2–S4: Citations/refusal; one versioned evaluation suite reused by CI |
| C-13 Tool registry/runtime | SK-12/13 | 2.50 / 3.00 | 3.50 / 4.50 | 5.00 / 8.00 | 8.00 | S3/S4: One bounded loop; Librarian, Planner, Budget Analyst profiles |
| C-14 MCP/approvals | SK-16/21 | 2.00 / 3.00 | 3.00 / 4.00 | 4.50 / 7.00 | 7.00 | S3/S4: Local stdio server/client, exact-action approvals, denial/replay cases |
| C-15 UI shell/chat | SK-2 | 2.00 / 3.00 | 3.00 / 4.00 | 5.00 / 7.00 | 7.00 | S2–S4: Minimal forms/citations/tool cards; 4h notes/tasks share + 3h agent share |
| C-16 Framework rebuilds | SK-11/14 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 | Unfunded: Conditional estimates below; no scheduled delivery |
| C-17 n8n automation | SK-15 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 | Unfunded: No scheduled delivery |
| C-18 Fine-tuning | SK-17 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 | Unfunded: No scheduled delivery |
| C-19 MongoDB/Spring audit service | SK-4/18 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 | Unfunded: No scheduled delivery |
| C-20 Observability | SK-20 | 0.75 / 1.25 | 1.00 / 2.00 | 2.00 / 3.00 | 3.00 | S1–S5: Structured redacted traces and timings; no external dashboard stack |
| C-21 Deploy/platform | SK-19 | 1.00 / 1.00 | 1.50 / 1.50 | 2.50 / 4.50 | 3.00 | S3/S4: One eligible AWS path OR local release/teardown; kind excluded |
| C-22 Docs/portfolio | SK-22 | 1.00 / 3.00 | 1.50 / 4.50 | 2.00 / 7.00 | 6.00 | S0–S5: Six hours total, including early README and final demo/resume |
| C-23 QA/hardening | SK-20/21/22 | 1.00 / 3.00 | 1.50 / 4.40 | 3.00 / 8.00 | 5.90 | S1–S5: Cross-component restore, injection/fault tests, final clean clone |
| C-24 Optional modules | See §6.3 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 | Unfunded: No clock/calendar/banking/native-app implementation |
| **Total funded scope** | | **29.50 / 43.00** | **42.00 / 62.90** | **65.50 / 108.00** | **104.90** | Low 72.50; high 173.50 |


The high scenario does not fit the 104.9-hour net. The response is a lower completed rung and a visible backlog, not using all stretch hours in advance or cutting security. C-23 funds integration/hardening across components; each component already includes its own acceptance tests. C-22 funds portfolio work once; README work on Day 4 is part of its six hours.

**Reconciliation to the prompt's suggested allocation:** foundation C-01–06 = 27; notes/tasks + 4 hours of C-15 = 13; C-09 = 9; C-10–12 = 20; C-13/14 + remaining 3 hours of C-15 = 18; C-21 = 3; C-20 = 3; C-22 = 6; C-23 = 5.9. Total **104.9**. The original 110-hour sketch omits explicit portfolio/hardening and is already above the corrected net. Replacing its 29 hours of framework/platform breadth funds the tighter core estimates and those missing obligations. CI/eval-gate effort is included in C-03, not charged again to C-21.

A whiteboard explanation, acceptance design, break-it experiment and short re-quiz are included in the applicable learning/verification blocks. Reading a topic does not confer depth A. Target depth **A** means build, test and explain; **B** means a thin working slice with limits; **C** means conceptual familiarity, and only after actually studying it.

### 6.1 First-use learning routes for ledger topics

These routes supplement the ADR blocks. They are prerequisite pointers, not fully delivered Skill Cards; Parts 14–15 expand them without adding hours. All tutorial code must be retyped, changed and explained by the learner; do not paste full examples into the project.

| Route / coverage | 📚 Learn first (Must read; stop marker; reason; time) | Explain back, then ↩ Return |
|---|---|---|
| LR-01 / C-01, SK-22 | [GitHub Hello World][R33], read branch → PR → merge; stop at completion; why: observable change history (10 min). [Conventional Commits][R34], read summary/specification; stop before FAQ (5 min). | Explain why a PR is evidence of a reviewed change. ↩ Return: Day 3, record issue-key → branch → commit → PR convention in your workflow notes; done when one setup-only PR follows it; time box 20 min within C-01; if stuck: hint 1—start with the issue key. |
| LR-02 / C-03, SK-19 | [GitHub Actions concepts][R35], read components; stop before next steps; why: CI is an automated check of a proposed change (10 min). | Explain job versus step. ↩ Return: Days 4–7, write your CI jobs/triggers/required-check spec before authoring configuration; done when a deliberately failing check blocks your defined merge process; time box 30 min within C-03; if stuck: hint 2—one check first. |
| LR-03 / C-04, SK-4/18 | [SQLAlchemy tutorial][R36], read overview and transaction section via navigation; stop before ORM mapping examples; why: distinguish database transaction from Python object state (15 min). | Explain commit versus rollback. ↩ Return: Day 7, specify a two-write rollback test before coding it; done when both writes succeed or neither persists; time box 30 min within C-04; if stuck: hint 1—identify the transaction boundary. |
| LR-04 / C-05, SK-21 | [Password Storage][R37], read Argon2id and salt guidance; stop before legacy migration; why: password hashes are not reversible encryption (10 min). | Explain why passwords cannot be encrypted and later returned. ↩ Return: Day 9, design wrong-password/expired-token/other-user cases; done when the learner's auth implementation passes those cases and logs no secrets; time box 30 min within C-05; if stuck: hint 1—separate identity validation from record ownership. |
| LR-05 / C-07/08, SK-3 | [Python data structures][R38], read lists/queues; stop before comprehensions (10 min). [heapq][R39], read heap invariant and priority-queue notes; stop before implementation details (10 min). | Explain a folder tree, a backlink graph and why a heap's first item has priority. ↩ Return: Days 13–16, draw two nested folders and three ordered tasks before writing code; done when ties, cycles and empty input have expected-result cases; time box 30 min within C-07/08; if stuck: hint 2—trace one insert by hand. |
| LR-06 / C-10/11, SK-1/7/8 | [Pandas tutorials][R40], read tabular input and missing-value sections via navigation (15 min). [NumPy basics][R41], read arrays, shapes and basic operations; stop before advanced topics (15 min). | Explain why a malformed CSV value should not silently become a valid expense. ↩ Return: Days 14–16, specify clean/reject/deduplicate outputs and compute similarity for two tiny vectors; done when hand results match the learner's parser/vector calculation; time box 45 min within C-10/11; if stuck: hint 1—use three rows before a real file. |
| LR-07 / C-12/23, SK-10/20 | [pytest Get Started][R42], read first test, assertions and fixtures; stop before plugin guidance; why: an evaluation requires repeatable known inputs (15 min). [pgvector][R11], read exact search behavior (5 min). | Explain retrieval failure versus answer-generation failure. ↩ Return: Days 16–21, author the §8 cases/expected citations before the retrieval test code; done when missing evidence and wrong-owner cases fail safely; time box 45 min within C-12; if stuck: hint 2—inspect retrieved IDs before inspecting prose. |
| LR-08 / C-20, SK-20 | [Ollama API][R13], read response metrics through endpoint navigation; stop before unrelated endpoints; why: performance claims need timed boundaries (10 min). | Explain cold versus warm latency. ↩ Return: Day 8 onward, define timing/token fields and redaction in trace records; done when a synthetic request can be followed without logging note content; time box 25 min within C-20; if stuck: hint 1—record start, first output and completion separately. |
| LR-09 / C-22, SK-22 | [About READMEs][R43], read what a README includes; stop before advanced formatting; why: another person must be able to understand/run the release (10 min). | Explain which screenshot would prove the claimed feature. ↩ Return: Day 4 and S5, write a brief actual-status README and a seeded demo script; done when every claim links to evidence or says “not built”; time box 25 min within C-22; if stuck: hint 1—describe one reproducible path. |
| LR-10 / conditional C-16, SK-14 | [LangGraph overview][R44], read capabilities; stop before code (10 min). | Explain state/node/edge as stored progress, a step and a transition. ↩ Return: only after scratch gates and an explicit swap, rebuild one existing agent and write ADR-07; done when the same golden set and security cases are compared; first time box 30 min inside the conditional estimate; if stuck: hint 1—map one existing transition. |
| LR-11 / conditional C-16, SK-11 | [LlamaIndex overview][R45], read framework purpose and ingestion/retrieval overview; stop before examples (10 min). | Explain what a framework node represents in your existing chunks. ↩ Return: only after scratch RAG passes and funding exists, compare its retrieval to the same baseline in ADR-08; done when source IDs/metrics can be compared; first time box 30 min; if stuck: hint 1—keep data unchanged. |
| LR-12 / conditional C-17, SK-15 | [n8n Community edition][R46], read features and limitations; stop at page end (10 min). | Explain trigger → action and why a webhook must be authenticated. ↩ Return: after the same task works in handwritten code and a swap funds it, draw one equivalent workflow for ADR-09; done when duplicate delivery and unauthorized requests have expected outcomes; first time box 30 min; if stuck: hint 2—reuse the API rather than bypassing it. |
| LR-13 / conditional C-18, SK-17 | [PEFT introduction][R47], read purpose; stop before installation/examples; why: fine-tuning changes model parameters using labeled data (10 min). | Explain why a held-out test case must not enter training. ↩ Return: only after prompted baseline and a funded swap, specify labels/splits/leakage checks and ADR-10; done when a separate ≥20-case test set and baseline exist; first time box 30 min; if stuck: hint 1—start with label quality, not GPU settings. |
| LR-14 / conditional C-19, SK-4/18 | [MongoDB manual][R48], read document-model introduction (10 min); [Spring Boot overview][R49], read purpose; stop before quickstart (5 min). | Explain a document store and an audit API in plain English. ↩ Return: after a funded swap, specify agent-trace storage and the single Java read API for ADR-11; done when duplication versus Postgres is justified; first time box 30 min; if stuck: hint 1—reuse existing traces. |
| LR-15 / conditional C-21, SK-19 | [kind Quick Start][R50], read introduction/requirements; stop before installation; why: kind runs a local Kubernetes cluster in containers (10 min). | Explain what this proves that Compose does not. ↩ Return: after a funded swap, specify one deployment/readiness/restart exercise for ADR-12; done when resource requirements fit measured hardware; first time box 30 min; if stuck: hint 1—do not claim a managed production cluster. |

### 6.2 Stand-alone versus folded optional estimates

**Stand-alone** means building a separate demonstration with its own data, setup and evaluation. **Folded** means reusing already-built app data, tools and evaluation. These are estimates, not benchmarked savings. Conditional hours are **not** included in 104.9.

| Skill / component | Stand-alone likely L / I | Folded low L / I | Folded likely L / I | Folded high L / I | Funded now |
|---|---:|---:|---:|---:|---:|
| LangChain + LangGraph / C-16 | 4 / 5 | 1.5 / 2.5 | 2.5 / 3.5 | 4 / 6 | 0 |
| n8n / C-17 | 2 / 3 | 0.5 / 1.5 | 1 / 2 | 2 / 3 | 0 |
| LlamaIndex / C-16 | 2 / 3 | 0.5 / 1.5 | 1 / 2 | 2 / 3 | 0 |
| Tiny classifier fine-tune / C-18 | 3 / 5 | 1 / 2 | 2 / 3 | 3 / 6 | 0 |
| MongoDB + Spring Boot / C-19 | 5 / 7 | 1.5 / 2.5 | 2.5 / 3.5 | 4 / 6 | 0 |
| kind / C-21 extension | 3 / 4 | 1 / 2 | 1.5 / 2.5 | 3 / 4 | 0 |
| Chroma/Qdrant comparison / C-11 extension | 2 / 2 | 0.5 / 0.5 | 0.5 / 1.5 | 1 / 2 | 0 |
| **Total** | **21 / 29 = 50** | **6.5 / 13 = 19.5** | **11 / 18 = 29** | **19 / 30 = 49** | **0** |

Core folding is already in the funded ledger: gateway streaming/structured-output primitives are reused by agents; ingestion feeds both RAG and the analyst; one versioned master evaluation suite supports manual checks, CI and later comparisons. PostgreSQL stores initial traces; MongoDB would replace that slice, not create another unrelated application. The conditional Spring API serves those traces. Optional training must retain a held-out split even if the evaluation infrastructure is shared.

Admit optional work in §3.2 order: LangChain/LangGraph → n8n → LlamaIndex → fine-tuning → MongoDB/Spring → kind → vector comparison. Initial cuts remove all optional builds; if any later become funded and then overrun, cut vector comparison, Spring Boot, kind and LlamaIndex first, preserving the scratch core. If MongoDB alone remains after cutting Spring, re-estimate the changed slice; do not keep claiming the combined service.

**Example valid swap:** if a measured re-estimate genuinely reduces remaining committed implementation by six hours while preserving every core acceptance criterion, fund the six-hour folded LangChain/LangGraph slice and remove those six hours from the old rows. Total stays 104.9. Merely “using the reserve” or working unrecorded evenings is not a scope swap.

### 6.3 Tier, depth and release truth

| Scope | Tier / target depth | Funding / claim boundary |
|---|---|---|
| Foundation, FastAPI, SQL, basic auth, notes/tasks, local LLM gateway, ingestion, embeddings, measured handwritten RAG | MUST; backend/AI target A, React B | Included in bounded ledger; mastery and original milestone dates unproven. |
| Tool registry, three shared-runtime agent profiles, MCP server/client, approvals, redaction/consent, CI eval gate | SHOULD-1; AI target A, UI B | Protected next priority; never substitute a framework for understanding the loop. |
| AWS minimal deployment | SHOULD-1; target B if actually deployed | 3 hours C-21; if blocked, spend on local deployment/recovery evidence and report AWS studied/unbuilt. |
| LangChain/LangGraph, LlamaIndex, n8n, fine-tuning | SHOULD-2; original B/B+ target downgraded to unfunded | Earliest conditional windows in §7; no framework implementation claim. |
| MongoDB, NoSQL implementation, Spring Boot, Kubernetes/kind, extra vector database | SHOULD-2; original B target downgraded to unfunded | PostgreSQL remains primary; optional theory is not a working slice. |
| Redis cache/queue/rate limiter; refresh-token rotation; app TOTP; hybrid search/reranker; cross-device SSE sync; Playwright/axe suite; AI PR action; supervisor agents; external tracing service | SHOULD-3; unfunded extensions | Installed Redis alone proves no queue/cache skill. Basic access control, injection defenses and core evals are already funded and cannot move into this optional bucket. |
| PDF/HTML ingestion; recurrence; graph visualization; polished editor/mobile/PWA | Deferred extensions | Markdown/CSV, graph data and minimal web UI remain the funded slice. |
| Clock/Ringtones, Calendar, Plaid Sandbox, Tauri/Expo, Go/C#/C++, Kafka/RocketMQ, gRPC, DynamoDB, Helm/RKE2, managed AI services, Podman comparison | COULD, depth C only after study; zero build hours | Retained in the later D8 gap/JD matrix; reason: no net capacity. No silent keyword claim. |
| Production bank integration, iOS system-alarm changes, microservice estate, full Django app, hardware project | WON'T | Outside this project. |
| Accessibility, REST, Linux basics, resilience, code review, security, observability | Core bounded exposure | Basic keyboard operation, request contracts, shell use, retry/timeout/fault cases and redacted traces; no broad expertise claim. Long-running on-call/distributed-systems ownership cannot be earned here. |

| Fixed checkpoint | Requested rung/date | Honest Part 1 forecast and proof |
|---|---|---|
| Day 11, Sun Oct 11 | MVP-0 / v0.1 | 26.50 net hours available. Skeleton is a high-risk target; stage later provider/CI/security extensions separately. Tag only if its complete definition passes; otherwise release setup/skeleton progress under an accurately named version. |
| Day 19, Mon Oct 19 | MVP-1 / v0.2 | 50.10 net hours available. Full knowledge scope is not a credible commitment yet; review actual notes/tasks/retrieval progress. Complete only what passes. |
| Day 26, Mon Oct 26 | MVP-2 / v0.3 | 71.15 net hours available. Revised target is Knowledge Core; agent work begins when dependencies pass. Do not label Knowledge Core Agentic Core. |
| Day 33, Mon Nov 2 | MVP-3 / v0.4 | 92.70 net hours available. Revised target is Agentic Core, with AWS status stated separately. Framework rung is unfunded. |
| Day 37, Fri Nov 6 | v1.0 | 104.90 net hours available. Release highest complete rung, hardening, demo and truthful evidence. No claim that a version number proves missing capabilities. |

Local-only Agentic Core must be labeled **“Agentic Core, local deployment; AWS criterion unmet”**, not the full original MVP-2. Security or evaluation failures block the corresponding release even if all UI screens exist. Dates do not justify relabeling failure as completion.


## 7. Chill scope, spill list and daily capacity

### 7.1 S0 contains setup and reading only

The S0 targets below are **timeboxes**, not an assertion that everything installs in ten hours. Total setup/learning capacity is 7.5 hours. The 15-minute DSA reading and 15-minute daily ritual on each chill day are already charged in §3.

| Day | Net setup plan; no feature code | 📚 Learn first | ↩ Return |
|---|---|---|---|
| 1, Thu Oct 1 | 1.00h: hardware/OS check 0.25; shell/editor/Git/SSH 0.50; uv/Python verification 0.25. Remaining installs spill. | [WSL prerequisites][R02], [GitHub SSH][R51], [uv installation][R52]; read prerequisites/overview only; stop before optional customization; why: a reproducible shell and identity (15 min total inside net). | Record verified versions and the next blocked install in your setup notes; done when the chosen shell and interpreter are identified; time box 45 min after reading; if stuck: hint 1—one tool at a time. |
| 2, Fri Oct 2 | 1.00h: GitHub/Jira 0.25; AWS eligibility/MFA/budget configuration or documented blocker 0.50; secret-handling notes 0.25. | [Jira getting started][R53], [AWS signup][R54], [AWS Budgets][R27]; read account/plan and alert sections; stop before resource creation; why: avoid paid enrollment (15 min inside net). | Record account status, MFA and budget evidence or exact blocker; done when no uncertain paid resource is required; time box 45 min after reading; if stuck: hint 1—keep AWS disabled. |
| 3, Sat Oct 3 | 2.50h: remaining Node/pnpm/Docker setup 0.75; repository/ignore/template specs then learner-written files 1.00; hooks/protection/manual fallback 0.75. | [Node LTS][V03], [pnpm installation][R55], [Get Docker][R56]; read OS/prerequisites; stop before optional services; why: install only tooling needed now (20 min inside net). | Write setup configuration yourself from Part 4/Part 12 specs; done when a setup-only PR and a deliberately rejected invalid commit/check demonstrate the workflow, or spill is named; time box remainder in ≤45-minute slices; if stuck: hint 2—defer decorative templates. |
| 4, Sun Oct 4 | 2.50h: CI skeleton 1.00; minimal Postgres/Redis Compose setup 0.50; README/SETUP outline 0.50; fresh-clone attempt 0.50. These are setup, not application features. | [GitHub Actions][R35], [Compose model][R25], [README contents][R43]; read overview sections; stop before extended examples; why: repeatable environment (20 min inside net). | Author configuration and documentation yourself; done when the setup check is green from a clean clone or a specific failure/spill is recorded; time box remainder in ≤45-minute slices; if stuck: hint 2—make one CI check meaningful before adding jobs. |
| 5, Mon Oct 5 | 0.50h: scope/checklist review 0.25; actual hours and S1 plan 0.25. No extra one-hour ceremony. | [Scrum Guide][R01], read Sprint Planning; stop before Daily Scrum; why: fit unfinished setup into S1 (5 min refresher inside net). | Write actual hours and an explicit swap for spill; done when the S1 forecast fits 21.05 net hours; time box 25 min after refresher; if stuck: hint 1—unfinished setup is work, not free overhead. |

Git means versioned change history; SSH authenticates the Git transport; uv manages Python environments; Node runs JavaScript tooling; pnpm manages JavaScript packages; Compose describes cooperating containers; a hook is a local check triggered by a Git operation. A lockfile records resolved dependencies. These concepts are expanded with official installation/verification instructions in Part 4, not installed by the mentor here.

### 7.2 Exact spill routing and just-in-time installations

**Hard spill rule:** at the daily cap, stop. Any failed S0 core setup moves to Day 6 first; CI skeleton may move to Day 7, its latest requested deadline. Feature work yields the same number of minutes. If the foundation still cannot run on Day 7, flag MVP-0 as blocked and use S1 for setup; do not claim both setup and feature progress in the same hours.

| Item | Day/window and swap | 📚 Learn first (official; stop; why) | ↩ Return |
|---|---|---|---|
| S0 core spill: editor/Git/SSH, uv/Python, Node/pnpm, Docker, Postgres/Redis, account/MFA/budget | Day 6, displaces C-06 feature start minute-for-minute; C-01/02 totals unchanged unless re-estimated | [VS Code setup][R57], [uv installation][R52], [Compose][R25]; read only failed prerequisite (≤15 min); stop when failure is understood | Verify the blocked tool in setup notes; done when the prerequisite succeeds or blocker is logged; first box 45 min; if stuck: hint 2—follow one official troubleshooting path. |
| CI skeleton, essential hooks and fresh-clone failures | Day 7, displaces later C-03/C-06 work; image build still required for completed MVP-0 | [GitHub Actions][R35], overview/components (10 min); stop before advanced workflows | Write the smallest valid config yourself; done when meaningful green/red runs are evidenced; first box 45 min; if stuck: hint 1—one check, one failure case. |
| Nonessential template polish and broader tooling | Day 12 review; only by swapping C-01/C-03 effort | [GitHub PR workflow][R33], review/merge (5 min); stop at merge | Retain only a template that resolves an observed omission; done when removed tasks stay deferred; box 15 min; if stuck: hint 1—omit cosmetic additions. |
| Ollama and chat-model download | Day 8 hard target; after local stack works | [Ollama API][R13] and [FAQ][R03], local server/model-loading sections (15 min); stop before hosted configuration | Complete the C-09 hardware smoke case; done when model digest, memory and timing are recorded; first box 45 min; if stuck: smaller model/shorter context, not a paid fallback. |
| Pandas/NumPy and markdown/CSV ingestion packages | Day 14 | [Pandas][R40], input tutorial; [NumPy][R41], arrays (20 min); stop before advanced examples | Resolve pins and three-row input cases before implementing ingestion; done when clean/reject/deduplicate outcomes are explicit; box 45 min in C-10; if stuck: hint 1—fixed schema. |
| Embedding model and pgvector | Day 16 | [Ollama embeddings][R15] and [pgvector][R11], getting started/querying (15 min); stop before approximate indexing | Record model dimension/prefixes/digest and exact-search baseline; done when manual and stored-vector results agree; box 45 min in C-11; if stuck: hint 2—use two vectors. |
| MCP SDK and Inspector | Day 23 target; contracts first, runtime only after tool boundary passes | [MCP architecture][R29] and [SDK docs][R58], participants/quickstart overview (15 min); stop before copying code | Pin compatible SDK/protocol and Inspector before use; done when a read-only tool contract is specified and mutating scope is denied by default; box 45 min in C-14; if stuck: stdio first. |
| AWS CLI beyond Day 2 account/budget work | Day 25 earliest, otherwise Day 32, only if C-21 eligible | [AWS CLI install][R59], OS prerequisites/version verification (10 min); stop before credentials setup | Record exact CLI version and least-privilege deployment identity; done when no long-lived key enters the repo; box 30 min within C-21; if blocked: local release. |
| LangChain/LangGraph | Day 27 earliest, **unfunded** | [LangGraph overview][R44], overview (10 min); stop before quickstart | Check scratch gate and written swap before install; done when ADR-07 comparison cases exist; first box 30 min inside conditional six hours; if blocked: defer. |
| n8n container | Day 28 earliest, **unfunded** | [Community edition][R46], feature/licensing limits (10 min); stop before setup | Check handwritten equivalent and swap before install; done when one equivalent authenticated workflow is specified; first box 30 min inside conditional three hours; if blocked: defer. |
| LlamaIndex | Day 29 earliest, **unfunded** | [Framework overview][R45], ingestion/retrieval (10 min); stop before examples | Check scratch RAG and swap before install; done when the same sources/golden set are retained; first box 30 min inside conditional three hours; if blocked: defer. |
| Hugging Face account, PEFT/training tools, Colab/Kaggle access | Day 30 earliest, **unfunded** | [PEFT][R47] and [Colab FAQ][R60], purpose/free limits (10 min); stop before paid plans | Verify access and task/model/data license, then pin exact libraries; done when CPU fallback and held-out cases exist; first box 30 min inside conditional five hours; if blocked: no fine-tuning claim. |
| MongoDB container; JDK 21 + Maven/Spring tooling | Day 31 earliest, **unfunded** | [MongoDB manual][R48] and [Spring Boot][R49], introduction/prerequisites (15 min); stop before examples | Verify exact Java/Maven/Spring compatibility and pins before any installation; done when trace-service contract and swap exist; first box 30 min inside conditional six hours; if blocked: retain Postgres. |
| kind/kubectl; Chroma/Qdrant | Day 32 / Day 33 earliest respectively, **unfunded and first-cut candidates** | [kind Quick Start][R50] and [pgvector comparison context][R11], requirements/exact baseline (10 min); stop before install | Obtain official installer docs and exact pins in the conditional Part before use; done when hardware, same-data comparison and swap are written; first box 30 min in conditional four/two hours; if blocked: defer. |
| Playwright browsers/axe; k6 | Day 34 earliest, **unfunded extensions** | [Playwright installation][R61], prerequisites; [k6 installation][R62], platform options (10 min); stop before commands | Admit only through a C-23 swap while preserving all core checks; done when a specific browser/load gap justifies the install; first box 30 min inside C-23; if blocked: keep funded manual/browser and API checks, no E2E/load-tool claim. |

These conditional Day 27–33 windows are not a seven-day schedule that fits all optional tools. They name the first possible day **after dependencies and a scope swap**. The default S4 schedule uses those hours for core completion. Downloads, troubleshooting, reading changelogs and recording pins all consume the assigned component time.

### 7.3 Every day's capacity balances

This is the **capacity ledger**, not a replacement for D6's detailed daily template. Parts 17–22 must expand each net cell into Learn → Implement → Verify, checklist IDs, explain-backs, quizzes and evidence. They may redistribute content, never silently exceed the row's hours.

Each row's Learn reference is a first-use reading or optional refresher of the route already introduced above, charged inside that row's learning allocation. It is not an extra daily assignment. The Return is the first bounded action; later Parts supply the remaining actions. Remaining net time is reserved for that row's component work, not new scope. Each row obeys **DSA + ritual + ceremony + reserve + net = floor**.

| Day / date / type | Floor | DSA | Ritual | Ceremony | Reserve | Net L+I | 📚 Learn first → ↩ Return (inside net) |
|---|---:|---:|---:|---:|---:|---:|---|
| 1 / Thu, Oct 1 / S | 1.50 | 0.25 | 0.25 | 0.00 | 0.00 | 1.00 | 📚 Learn first: [WSL prerequisites][R02], stop before installation (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: record hardware and the chosen setup route in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 2 / Fri, Oct 2 / S | 1.50 | 0.25 | 0.25 | 0.00 | 0.00 | 1.00 | 📚 Learn first: [Free Tier eligibility][R26], stop before signup (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: record account eligibility and a zero-spend decision in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 3 / Sat, Oct 3 / S | 3.00 | 0.25 | 0.25 | 0.00 | 0.00 | 2.50 | 📚 Learn first: [branch and pull request workflow][R33], stop after merge overview (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: specify the issue-key workflow and setup-only PR in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 4 / Sun, Oct 4 / S | 3.00 | 0.25 | 0.25 | 0.00 | 0.00 | 2.50 | 📚 Learn first: [workflow components][R35], stop before examples (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: specify one CI check and the fresh-clone procedure in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 5 / Mon, Oct 5 / S | 1.00 | 0.25 | 0.25 | 0.00 | 0.00 | 0.50 | 📚 Learn first: [Sprint Planning][R01], stop before Daily Scrum (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: reconcile actual S0 hours and the S1 forecast in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 6 / Tue, Oct 6 / B | 6.00 | 0.50 | 0.75 | 0.00 | 0.60 | 4.15 | 📚 Learn first: [First Steps][R09], stop before parameter tutorials (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: specify the API health boundary in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 7 / Wed, Oct 7 / A | 4.00 | 0.25 | 0.50 | 0.00 | 0.20 | 3.05 | 📚 Learn first: [transactions][R10], stop before advanced features (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: specify migrations and rollback cases in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 8 / Thu, Oct 8 / B | 6.00 | 0.50 | 0.75 | 0.00 | 0.60 | 4.15 | 📚 Learn first: [API overview][R13], stop before unrelated endpoints (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: record the local model stream and timeout cases in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 9 / Fri, Oct 9 / A | 4.00 | 0.25 | 0.50 | 0.00 | 0.20 | 3.05 | 📚 Learn first: [Argon2id guidance][R37], stop before legacy migration (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: design wrong-password and expiry cases in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 10 / Sat, Oct 10 / C | 5.00 | 0.50 | 0.75 | 0.00 | 0.40 | 3.35 | 📚 Learn first: [assertions][R42], stop before fixtures (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: check the skeleton against designed negative cases in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 11 / Sun, Oct 11 / C | 5.00 | 0.50 | 0.75 | 1.50 | 1.00 | 1.25 | 📚 Learn first: [Sprint Review][R01], stop before Retrospective (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: record the skeleton go/no-go and actual release scope in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 12 / Mon, Oct 12 / A | 4.00 | 0.25 | 0.50 | 1.00 | 0.20 | 2.05 | 📚 Learn first: [Sprint Retrospective][R01], stop at section end (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: reforecast using completed evidence in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 13 / Tue, Oct 13 / B | 6.00 | 0.50 | 0.75 | 0.00 | 0.60 | 4.15 | 📚 Learn first: [state and events][R22], stop before sharing-state examples (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: specify the first notes form in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 14 / Wed, Oct 14 / A | 4.00 | 0.25 | 0.50 | 0.00 | 0.20 | 3.05 | 📚 Learn first: [tabular input][R40], stop before combining tables (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: specify the three-row CSV acceptance cases in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 15 / Thu, Oct 15 / B | 6.00 | 0.50 | 0.75 | 0.00 | 0.60 | 4.15 | 📚 Learn first: [sharing state][R22], stop before tutorial link (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: verify the minimal note-save behavior in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 16 / Fri, Oct 16 / A | 4.00 | 0.25 | 0.50 | 0.00 | 0.20 | 3.05 | 📚 Learn first: [exact querying][R11], stop before indexing (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: compare exact retrieval with hand calculations in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 17 / Sat, Oct 17 / C | 5.00 | 0.50 | 0.75 | 0.00 | 0.40 | 3.35 | 📚 Learn first: [priority queue notes][R39], stop before implementation details (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: verify task priority and tie handling in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 18 / Sun, Oct 18 / C | 5.00 | 0.50 | 0.75 | 1.00 | 1.00 | 1.75 | 📚 Learn first: [transactions][R10], stop at section end (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: rehearse restore using seeded data in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 19 / Mon, Oct 19 / A | 4.00 | 0.25 | 0.50 | 1.00 | 0.20 | 2.05 | 📚 Learn first: [Sprint Review][R01], stop before Retrospective (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: record the knowledge-slice gap and next work in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 20 / Tue, Oct 20 / B | 6.00 | 0.50 | 0.75 | 0.00 | 0.60 | 4.15 | 📚 Learn first: [querying][R11], stop before indexing (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: inspect retrieval source IDs and owner filters in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 21 / Wed, Oct 21 / A | 4.00 | 0.25 | 0.50 | 0.00 | 0.20 | 3.05 | 📚 Learn first: [embedding usage][R15], stop before examples (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: verify the citation/refusal evaluation inputs in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 22 / Thu, Oct 22 / B | 6.00 | 0.50 | 0.75 | 0.00 | 0.60 | 4.15 | 📚 Learn first: [single tool call][R28], stop before parallel calls (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: specify allowed tools and authorization cases in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 23 / Fri, Oct 23 / A | 4.00 | 0.25 | 0.50 | 0.00 | 0.20 | 3.05 | 📚 Learn first: [protocol layers][R29], stop before lifecycle examples (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: specify MCP contracts after the tool boundary in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 24 / Sat, Oct 24 / C | 5.00 | 0.50 | 0.75 | 0.00 | 0.40 | 3.35 | 📚 Learn first: [tool result flow][R28], stop before parallel calls (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: trace the bounded agent loop in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 25 / Sun, Oct 25 / C | 5.00 | 0.50 | 0.75 | 1.50 | 1.00 | 1.25 | 📚 Learn first: [indirect injection][R30], stop before unrelated defenses (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: rehearse prompt-injection and recovery cases in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 26 / Mon, Oct 26 / A | 4.00 | 0.25 | 0.50 | 1.00 | 0.20 | 2.05 | 📚 Learn first: [Definition of Done][R01], stop at section end (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: record the Knowledge Core go/no-go in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 27 / Tue, Oct 27 / B | 6.00 | 0.50 | 0.75 | 0.00 | 0.60 | 4.15 | 📚 Learn first: [tool definitions][R28], stop before parallel examples (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: evaluate the three role/tool profiles in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 28 / Wed, Oct 28 / A | 4.00 | 0.25 | 0.50 | 0.00 | 0.20 | 3.05 | 📚 Learn first: [deny by default][R05], stop before later recommendations (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: bind approval to exact tool arguments in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 29 / Thu, Oct 29 / B | 6.00 | 0.50 | 0.75 | 0.00 | 0.60 | 4.15 | 📚 Learn first: [client/server participants][R29], stop before lifecycle examples (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: verify MCP denial and replay cases in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 30 / Fri, Oct 30 / A | 4.00 | 0.25 | 0.50 | 0.00 | 0.20 | 3.05 | 📚 Learn first: [event stream format][R24], stop before examples (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: verify UI tool cards and cancellation in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 31 / Sat, Oct 31 / C | 5.00 | 0.50 | 0.75 | 0.00 | 0.40 | 3.35 | 📚 Learn first: [assertions and fixtures][R42], stop before plugins (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: record deterministic and live eval results separately in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 32 / Sun, Nov 1 / C | 5.00 | 0.50 | 0.75 | 1.00 | 1.00 | 1.75 | 📚 Learn first: [eligibility and expiration][R26], stop before signup (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: record cloud eligibility or the local-release fallback in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 33 / Mon, Nov 2 / A | 4.00 | 0.25 | 0.50 | 1.00 | 0.20 | 2.05 | 📚 Learn first: [Definition of Done][R01], stop at section end (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: record highest completed rung and freeze scope in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 34 / Tue, Nov 3 / B | 6.00 | 0.50 | 0.75 | 0.00 | 0.40 | 4.35 | 📚 Learn first: [README contents][R43], stop before formatting (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: verify setup instructions against the release in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 35 / Wed, Nov 4 / A | 4.00 | 0.25 | 0.50 | 0.00 | 0.20 | 3.05 | 📚 Learn first: [README contents][R43], stop before formatting (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: complete the seeded demo and evidence claims in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 36 / Thu, Nov 5 / B | 6.00 | 0.50 | 0.75 | 0.00 | 3.00 | 1.75 | 📚 Learn first: [assertions][R42], stop before fixtures (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: use recovery time only for existing-scope defects in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |
| 37 / Fri, Nov 6 / A | 4.00 | 0.25 | 0.50 | 0.00 | 0.20 | 3.05 | 📚 Learn first: [version rules][R32], stop before FAQ (5 min first read; later refresher only if needed). Explain back the decision's purpose. ↩ Return: tag the verified release and list limitations in your setup/design/evidence notes and corresponding component; done when its check or explicit gap is recorded; first time box 15 min; if stuck: hint 1, narrow to one outcome. |


## 8. AI measurement contract

A **golden set** is a versioned set of hand-written inputs and expected outcomes. A **baseline** is a simpler method measured on the same cases. **p50/p95** are the middle and upper-tail observed latency percentiles; **time-to-first-token (TTFT)** measures when generated output first becomes visible. Twenty cases are a useful regression floor, not proof of broad reliability.

Create one master suite with **at least 100 hand-written cases**: 20 gateway/structured-output cases, 20 retrieval-and-answer cases, and 20 cases for **each** of Librarian, Planner and Budget Analyst. Cases can have multiple tags, but each feature's ≥20-case subset must be explicit. Author expected source IDs, allowed tools and expected effects before implementation. This work is included in C-09/C-12/C-13/C-14/C-23, not an invisible evaluation project.

| Feature | Golden subset and baseline | Required quality measure / initial acceptance target | Latency and cost evidence |
|---|---|---|---|
| Local gateway: streaming, structured output and routing | ≥20 cases covering success, cancellation, malformed output, timeout and disabled hosted route; baseline direct local request + recorded contract fixtures | Validated contract cases 100%; no private data or unexpected hosted call; live model invalid-output rate reported separately | Cold/warm p50/p95 total, TTFT, output tokens/sec; input/output tokens when provider reports them; model/digest/hardware. Local API charge $0; energy/time not claimed free. |
| Embeddings and retrieval | ≥20 hand-authored queries with expected owned source IDs; hand-built cosine/exact top-k and simple lexical baseline | Recall@5 ≥0.80 on the declared set; report MRR; owner-isolation failures = 0; vector version/dimension checks pass | Embedding and retrieval p50/p95 separately; batch size, corpus size, peak memory; TTFT not applicable to embeddings; API charge $0 locally |
| RAG with citations/refusal | Same ≥20 retrieval cases with answer/refusal expectations; baseline lexical retrieval plus answer and/or no-retrieval prompt, kept fixed | Citation-source validity 100%; manually scored supported-claim fraction ≥0.90; missing-evidence refusal cases all pass; report baseline and failures | End-to-end p50/p95 and TTFT, retrieved context tokens, input/output tokens, model/context limits and $0 local API charge |
| Notes Librarian | ≥20 cases: search, cite, deny, injected note, no evidence; baseline deterministic search tool | Task success ≥0.80; tool-name/argument accuracy ≥0.90; authorization/injection safety cases all pass | Per-step and total p50/p95, TTFT, tool duration, step/token limits and local token use/cost |
| Planner | ≥20 cases: ordering, proposed task creation, approval/denial/change/replay; baseline deterministic heap/deadline ordering | Task success ≥0.80; tool accuracy ≥0.90; unapproved, altered or replayed mutation count = 0 | Model/tool p50/p95 and TTFT; human approval wait recorded separately from execution; step/token totals and cost |
| Budget Analyst | ≥20 synthetic CSV questions with known totals/categories; baseline Pandas calculation | Numeric result agrees with deterministic totals within declared rounding; task success ≥0.80; tool accuracy ≥0.90; private-data exposure = 0 | Parser/analytics/model timings separately, total p50/p95/TTFT, tokens and cost |
| MCP/approval layer | Reuse ≥20 tagged agent cases including denied scopes, malformed input, replay and changed arguments; baseline direct authorized tool invocation | Contract and permission tests 100%; protocol success never substitutes for business success | Client/server overhead p50/p95; TTFT only for model-facing flows; protocol itself incurs no model tokens; trace total downstream usage |
| Conditional framework/n8n rebuilds | Identical relevant ≥20-case subset and scratch implementation baseline | No security regression; report quality delta even if negative; compare code size, debugging, flexibility and lock-in | Same hardware/data/config, p50/p95/TTFT, tokens/cost; framework overhead distinguished from model variance |
| Conditional fine-tuned classifier | Separate held-out ≥20 labeled notes, never trained on; baseline majority class + fixed prompted classifier | Macro-F1 and per-class errors; confusion matrix; improvement must be measured, not presumed | Inference p50/p95, TTFT N/A for a non-generative classifier; training wall time/memory, inference tokens if any, actual compute charge |

Targets above are **acceptance proposals**, not observed results. Freeze them and case IDs before evaluating. If the model fails, preserve the report, narrow the supported behavior explicitly and re-estimate; never quietly weaken thresholds after seeing failures.

For performance, a provisional diagnostic ceiling is local generated-response TTFT p95 ≤5 seconds and total p95 ≤30 seconds for bounded short responses. Hardware discovery may make that infeasible; record the failed target and decide whether to narrow the product. There is no claim that a tiny CPU model will meet it. For the non-LLM UI, define the prompt's <100 ms as input-to-visible-local-feedback, measured with browser timing; API, database and retrieval round trips are reported separately. A 100 ms server/network promise is not inferred from a responsive button.

Record at least one timed run per case, plus a clearly separate cold-start probe. State sample count, warm/cold state and percentile method; with 20 cases the tail estimate is coarse. Agent actions must be evaluated against the expected state change, not only the model's prose. Do not use an LLM judge as sole truth for correctness or authorization.

**CI gate from completed Agentic Core:** deterministic security/contract regressions fail every relevant PR; live model results use pinned prompts/models and the same golden suite at the release gate. If hosted CI cannot run Ollama at $0, recorded fixtures check behavior deterministically but **do not prove live-model quality**. A local live evaluation report is required before the release. An automated self-hosted eval runner is conditional on secure runner setup fitting C-03; otherwise the automated live-quality gate is explicitly unmet. No unauthenticated external PR may execute on a runner with private data or credentials.

📚 Learn first (Must read): [pytest Get Started][R42], read assertions/fixtures (~10 min); [pgvector][R11], read querying and exact versus approximate search (~10 min); [Ollama API][R13], inspect response usage/timing fields (~5 min). Stop before unrelated tuning.
Explain back: What does a passing recorded-fixture test prove, and what does it fail to prove about the current model?
↩ Return to build: C-12/C-13, author case IDs and expected outcomes in your future docs/evals files before writing the evaluator; done when each enabled AI feature has ≥20 cases, a baseline, a metric and latency/token/cost fields; first time box 45 min within those components; if stuck: hint rung 1—one input, one expected source/tool/effect, one reason it could fail.

## 9. Dated feasibility and risk register

**Checked 2026-10-01 using official sources.** “Verified page” means retrieved/read evidence, not confirmed account eligibility. Browser search was available and used. **Context7 MCP was not available** among this session's tools; official docs/release notes were used instead. API-level compatibility still requires checking the pinned documentation before implementation.

| Risk ID | Verified finding / remaining limit | Trigger and $0 response | 📚 Learn first → ↩ Return |
|---|---|---|---|
| F-01 Capacity | Corrected net 104.9; high component estimate 173.5; the full request does not fit | Any remaining likely estimate exceeds remaining net: use the cut ladder and ship a lower complete rung | 📚 [Scrum Guide][R01], Sprint Planning; stop before Daily Scrum (5 min). ↩ Return: Monday review, update component actual/remaining hours; done when total fits; box 10 min inside ceremony; if stuck: hint 1—remove optional scope first. |
| F-02 Hardware/Ollama | Named model licenses and package sizes verified; RAM/VRAM, usable disk, runtime speed and tool quality unknown | Out-of-memory, sustained swapping or failed quality: reduce model/context/concurrency, retain measured failure and re-scope | 📚 [Ollama FAQ][R03], memory/concurrency; stop before unrelated networking (5 min). ↩ Return: Day 8, capture memory/throughput; done when model fit is measured; box 15 min in C-09; if stuck: smallest model first. |
| F-03 AWS eligibility/card | [Free Tier FAQ][R26]: eligible new customers receive $100 initially and can earn up to $100 more; Free plan ends at six months or credit exhaustion. Prior customers are not assumed eligible. [New signup][R54] is rolling out; payment info may be requested with a temporary $1 hold. [Advanced signup][R63] requires a payment method. Ineligible signup leads to Paid plan. | No verified Free plan, unwanted hold or unclear terms: stop cloud setup and retain local Compose; do not count hypothetical credits | 📚 [AWS signup][R54], eligibility/payment section; stop before enrollment (10 min). ↩ Return: Day 2, record actual account plan/expiration/credit balance if available; done when $0 route or blocker is explicit; box 15 min in C-02; if stuck: local default. |
| F-04 AWS alerts/hosting | [Budgets][R27] alerts may lag charges; they are not a universal hard spending cap. Free instance capability for local models is not established. | Any route can accrue an out-of-pocket bill, or cannot serve live inference: no such public deployment. No NAT Gateway. Teardown and remaining resources must be verified. | 📚 [AWS Budgets][R27], limitations; stop before optional actions (5 min). ↩ Return: C-21, document compute/storage/network/log costs and teardown evidence; done when allowed services and zero-spend boundary are known; box 20 min; if stuck: deploy locally. |
| F-05 Hosted LLM | [Claude API pricing][R64] documents billed API usage. Universal free credits were **not** established; no credit is budgeted. Any special-program credit requires actual eligibility. | No verified free grant and no non-billing route: hosted calls remain disabled. A fixture-tested adapter is not a live integration or a local-vs-hosted quality benchmark. | 📚 [Claude API pricing][R64], token/tool pricing overview; stop before examples (5 min). ↩ Return: C-09, set $0 hosted-call allowance and test the deny path; done when no hosted request occurs; box 15 min; if stuck: hint 1—fail closed. |
| F-06 Colab/Kaggle | [Colab FAQ][R60]: free hardware/resources are not guaranteed; at most 12-hour free sessions depend on availability/usage. [Kaggle efficient GPU tips][R65]: official indexed text describes 30 weekly GPU hours or sometimes more, not reserved hardware. Direct Kaggle pages yielded no readable body in this session. | No suitable accelerator/access: tiny CPU-feasible experiment only if funded; otherwise fine-tuning stays unbuilt. 🔎 Verify actual Kaggle quota, phone/TPU requirements in account; no invented values. | 📚 [Colab FAQ][R60], free-resource limits; stop before paid products (5 min). ↩ Return: conditional Day 30, record actual quota/checkpoint/fallback plan; done when training fits the session; box 15 min inside conditional C-18; if blocked: defer. |
| F-07 Model/data licenses | Qwen3-0.6B/1.7B and nomic v1.5 publisher cards show Apache-2.0. Public accessibility of a dataset is not a redistribution license. Three-corpus/three-dataset scouting is Part 2. | Missing or incompatible license/PII: reject that source; use learner-authored/synthetic data | 📚 [Qwen card][R16] and [nomic card][R20], license/usage; stop before examples (5 min). ↩ Return: Part 2 scouting then C-10, record license, version, attribution and redistribution status per source; done when no unlicensed corpus is planned; box 20 min in C-10; if stuck: authored data. |
| F-08 n8n terms | [Community edition][R46] and [current license][R66]/[FAQ][R67] allow personal learning and operator-created workflows under restrictions; external users creating/configuring workflows is restricted. Fair-code/source-available, not unrestricted OSI open source. Self-hosting and API calls can still cost. | Use changes toward a workflow-hosting product: reassess license; no expansion here | 📚 [n8n license FAQ][R67], permitted/restricted use; stop after relevant examples (10 min). ↩ Return: conditional C-17, record personal local use and called-service costs; done when license scope is explicit; box 10 min; if stuck: defer. |
| F-09 Atlas | [MongoDB Free setup][R68] does not require a card; [Free cluster limits][R69]: one per project, 0.5 GB including indexes, no managed backup, constrained regions/resources, idle pause after 30 days. Server patch is platform-managed. | Need more storage/backup or exact server patch: choose local MongoDB only if optional slice funded; never upgrade silently | 📚 [Atlas limits][R69], storage/backup/version limitations; stop before paid tiers (5 min). ↩ Return: conditional C-19, record Free choice and export fallback; done when no paid setting is required; box 15 min; if stuck: retain Postgres. |
| F-10 GitHub | [Plans][R70]: Free includes public/private repositories; [branch protection][R71] is available on Free public repositories, not generally Free private ones. Visibility has not been changed. | Private Free cannot enforce protection: manual merge gate documented as unenforced; later public transition requires learner decision and clean seeded artifacts | 📚 [Protected branches][R71], availability; stop before configuration (5 min). ↩ Return: Day 3, record actual enforcement versus manual convention; done when README/workflow does not overstate protection; box 10 min in C-01; if stuck: manual gate. |
| F-11 Jira | [Pricing][R72]: Free up to 10 users, 2 GB storage. Automation quota wording differs across official pages; no fixed quota promised. | Required automation unavailable: manual issue updates within rituals; no paid add-on | 📚 [Jira pricing][R72], Free row; stop before paid tiers (5 min). ↩ Return: Day 2, record account limits and actual workflow choices; done when solo board works without paid dependence; box 10 min in C-01; if stuck: simple board. |
| F-12 Versions/security | Release existence verified; dependency compatibility, transitive lock, container digests and vulnerabilities unverified | Broken dependency/security advisory: repair pin and document the change, consuming component hours | 📚 [uv management][R31] and [MCP SDK releases][V12], relevant installed versions only (10 min); stop at next release. ↩ Return: first use and each framework session, re-read official docs/changelog, mark exact APIs 🔎 verify until checked; done when installed versions match evidence; box 15 min inside component; if stuck: smallest supported set. |
| F-13 Banking | [Plaid Sandbox][R73] is free/test-data based, with production differences. [Plaid Free/Trial FAQ][R74] also describes eligible US/Canada teams' limited free live Trial; therefore “all live Plaid is paid” would be wrong. Real Bank of America access/approval is unverified and outside scope. | No bank credentials, production linking or real-finance demo; Sandbox itself is unfunded COULD | 📚 [Plaid Sandbox][R73], limits; stop before integration (5 min only if considering swap). ↩ Return: C-24 backlog, retain Sandbox-only boundary; done when no production claim exists; box 5 min inside change-control review; if stuck: synthetic CSV already covers the analyst. |
| F-14 Docker/account cost | [Docker Desktop license][R75] permits personal/education use without a paid Desktop subscription; organizational use may differ. Existing install/OS support remains unchecked. | Unsupported machine/changed use category: verify a suitable free engine route before installation | 📚 [Desktop license][R75], free-use terms; stop before subscriptions (5 min). ↩ Return: C-02, record applicable use category; done when installation choice fits it; box 5 min inside setup; if stuck: official Linux Engine route in Part 4. |
| F-15 Learning/review reliability | No completed evidence exists. A read-only AI review is not a human review, and a tutorial is not proof of independent skill. | Cannot explain/rebuild or cannot obtain review: keep depth/claim incomplete; no invented reviewers | 📚 [Google public review guide][R76], reviewer overview; stop before linked deep dives (5 min). ↩ Return: C-22 and Monday review, record proof-gate gaps and real review attempts; done when claim language matches evidence; box 10 min in ceremonies/rituals; if stuck: log the honest gap. |

Account-specific free tiers, exact API behavior and hardware performance must be rechecked at use. These limits are part of the plan, not consent to enroll in services, publish a repository, contact reviewers or send private data.

## 10. Global Definition of Ready and Definition of Done

These are **gate templates**, not new feature tasks or duplicate hours. They become component-linked Jira checklist items in D12. Each pass inspects existing evidence; missing implementation returns to the component budget. A Jira Task has one verifiable outcome and ≤90 minutes; split anything larger. The small review timeboxes below do not imply that building the underlying behavior takes two minutes.

### 10.1 Definition of Ready

- [ ] **RDY-01 — State one outcome and its owner.** A Story describes who needs what and why; identifies component, rung, sprint/day, issue key, depth and evidence. Acceptance cases are designed before code.
  📚 Learn first (Must read): [Jira getting started][R53], read work/backlog overview; stop before administration; why: trace work to an outcome (3 min first use).
  Explain back: Which visible behavior would show this story is finished?
  ↩ Return: inspect the story description before starting; done when its outcome and evidence are unambiguous; time box 2 min within planning/learning; if stuck: hint 1—split multiple outcomes.

- [ ] **RDY-02 — Fit the work and dependencies.** Story fits one real day's net; tasks ≤90 minutes; steps ≤45 minutes; learning ≤2 hours per skill; dependency gates and swap are recorded.
  📚 Learn first (Must read): [Scrum Guide][R01], Sprint Planning; stop before Daily Scrum; why: use capacity rather than wishful scope (3 min first use).
  Explain back: Which funded item leaves if this one is added?
  ↩ Return: compare the story's L/I estimate to §7.3; done when no reserve or stretch is promised to a new feature; time box 2 min in planning; if stuck: hint 2—split at a testable boundary.

- [ ] **RDY-03 — Define the threat and negative case.** Identify identity, ownership, untrusted input, secrets and external data movement; include a security case and a performance/negative case where relevant.
  📚 Learn first (Must read): [OWASP Threat Modeling][R04], “Response and Mitigations”; stop before review; why: defenses must be testable (3 min first use).
  Explain back: Who must be denied even when the happy path works?
  ↩ Return: attach expected denial/error behavior to the story test-case table; done when the boundary is explicit; time box 3 min in component design; if stuck: hint 1—use a second user and malicious input.

- [ ] **RDY-04 — Establish learning and reproducibility.** Include Learn/stop marker/explain-back/Return, version/license prerequisites, baseline, golden cases for AI, and scratch-before-framework gate.
  📚 Learn first (Must read): [Semantic Versioning][R32], version rules; stop before FAQ; why: evidence must identify the tested artifact (3 min first use).
  Explain back: Can a framework comparison be fair if it changes the model and data too?
  ↩ Return: inspect prerequisites and case IDs; done when versions/data and first learner-written task are named; time box 3 min inside learning; if stuck: hint 1—hold baseline inputs fixed.

### 10.2 Definition of Done

- [ ] **DONE-01 — Pass the designed behavior.** User-authored implementation passes named happy, negative and security cases; no generated feature code or copied unexplained components.
  📚 Learn first (Must read): [pytest assertions][R42], first test/assertion section; stop before fixtures; why: success needs an observable result (3 min first use).
  Explain back: Which input would fail if the implementation were wrong?
  ↩ Return: link your case table and test result to the issue; done when each acceptance case has evidence; review box 2 min inside verification; if stuck: hint 2—reduce to the failing case.

- [ ] **DONE-02 — Pass quality and change checks.** Relevant lint/type/test/security checks pass; issue key appears in branch/commit/PR; self-review and read-only AI review findings are resolved or explicitly scoped.
  📚 Learn first (Must read): [GitHub Actions][R35], workflow components; stop before next steps; why: the checked revision must match the change (3 min first use).
  Explain back: Why is yesterday's green run not proof for today's commit?
  ↩ Return: attach the current revision's checks and review disposition; done when the merge process has no unexplained failure; review box 2 min inside rituals; if stuck: one failing check at a time.

- [ ] **DONE-03 — Demonstrate security at the changed boundary.** Passwords are hashed; JWTs are short-lived and validated; simple roles plus owner checks enforced. Test XSS handling for markdown, explicit allowed origins, input/file limits, CSRF defense if cookies authenticate mutations, and bounded request/login/model-call rates. No generic “secure” claim.
  📚 Learn first (Must read): [OWASP Authorization][R05] and [Password Storage][R37], relevant recommendations; stop after the changed control; why: core defenses are not optional polish (5 min first use).
  Explain back: Which check must still run when a model proposes the action?
  ↩ Return: record the specific negative security result and secret-scan result; done when the changed path cannot bypass that control; review box 3 min in verification; if stuck: hint 1—deny by default. Detailed control cases expand in Parts 8–11.

- [ ] **DONE-04 — Prove the AI claim.** Every enabled AI path meets §8: ≥20 cases, baseline, quality metric, p50/p95, TTFT or justified N/A, usage/cost, model/prompt/data versions and failure report. Regression blocks the corresponding claim.
  📚 Learn first (Must read): [Ollama API][R13], metrics fields; stop before other endpoints; why: measurements must identify what was timed (3 min first use).
  Explain back: Are fixture results being mistaken for live-model results?
  ↩ Return: link the evaluation report from the issue and README claim; done when all columns exist and safety regressions are zero; review box 3 min in verification; if stuck: remove the unsupported claim.

- [ ] **DONE-05 — Exercise failure and recovery.** Relevant break-it case passes: expired token, malformed import, interrupted model/worker, lost response, restore or changed approval. Backup/export restored into an isolated test instance before trusted use.
  📚 Learn first (Must read): [PostgreSQL transactions][R10] and [Compose model][R25], transaction/persistence concepts; stop before examples; why: restart is not the same as recovery (5 min first use).
  Explain back: Which committed data survives this failure?
  ↩ Return: link fault/recovery evidence; done when expected state after the fault is verified; review box 2 min in verification; if stuck: hint 1—record before and after state. The actual experiment is billed to component I/C-23.

- [ ] **DONE-06 — Prove learning.** Answer explain-backs; pass own acceptance test; whiteboard the component from blank in ten minutes; schedule a re-quiz two–three days later. Mark “built, learning proof pending” until the re-quiz passes.
  📚 Learn first (Must read): [Google review guide][R76], overview of reviewing understanding/correctness; stop before linked deep dives; why: reasoning must survive explanation (3 min first use).
  Explain back: Could you reproduce the design without the tutorial?
  ↩ Return: record proof status in your future LEARNING_LOG; done when all four gates pass, or the remaining gate is dated and the learned claim withheld; review box 2 min in rituals; if stuck: hint 1—name the confusion. Whiteboard/re-quiz work uses learning and ritual budgets, not extra time.

- [ ] **DONE-07 — Make operation and claims reproducible.** Setup, actual versions, run/stop/recovery instructions and limitations match the release; logs omit secrets; licenses/attributions recorded; screenshots use seeded data; cloud/hosted-only claims require actual evidence.
  📚 Learn first (Must read): [README guidance][R43], content overview; stop before formatting; why: a stranger needs a repeatable path (3 min first use).
  Explain back: What prerequisite would surprise a fresh-clone user?
  ↩ Return: link setup and evidence artifacts; done when a fresh-clone check succeeds or release is blocked with a precise reason; review box 2 min in verification; if stuck: hint 1—follow your own steps without relying on remembered state.

- [ ] **DONE-08 — Close the correct release scope.** Merge only passing work, update Jira and project state; at rung release, tag actual scope, list unmet requirements and preserve restart instructions. No new features Days 36–37.
  📚 Learn first (Must read): [Semantic Versioning][R32], version rules; stop before FAQ; why: a version names a release, not evidence by itself (3 min first use).
  Explain back: Which capabilities are claimable at this tag?
  ↩ Return: update your release/evidence links and next ≤3 actions; done when repository state, Jira and README agree; review box 3 min in rituals; if stuck: ship the last complete rung.

**Hint ladder applies throughout:** after 25 focused minutes stuck, log the block and climb one rung: (1) concept, (2) approach/pseudocode, (3) a key snippet ≤15 lines only after the learner supplies an attempt or explicitly requests it. Then use a Socratic question/answer exchange while the learner types. No rung-3 code is supplied in this Part.

## 11. Continuity, open items and acceptance of this Part

### 11.1 ID registry and later-Part obligations

- Components C-01–C-24 and skills SK-1–SK-22 retain the master prompt's numbering. C-16/17/18/19/24 are unfunded; extensions to other components remain separately marked.
- Epics E0–E10 are reserved, not delivered here. Story pattern E2-US04; component checklist pattern C-07.3; Jira project-key candidate MERLIN is **unconfirmed**, not a created board.
- ADR-01–06 are delivered planning decisions. ADR-07–12 are reserved conditional comparisons: agent frameworks, LlamaIndex, n8n, classifier, MongoDB/Spring and kind. Add vector-database comparison as a later ADR if funded.
- RDY-01–04 and DONE-01–08 are gate templates. No C-##.# tasks or Story IDs have been issued; Parts 5–7 derive the source checklist before Parts 8–9 create full stories.
- Part 9's abbreviated “E3–E8” list omits E9/E10 required by D1. Include E9/E10 in Part 9 or an explicit continuation; do not silently drop delivery or QA epics.
- Parts 10–11 expand threat model, encryption, browser auth, API/MCP and schema specs. Basic security/AI regression gates stay core even though the prompt also lists advanced audits among SHOULD-2.
- AWS basic learning may precede frameworks to satisfy the conditional rung-2 requirement; Kubernetes remains later/unfunded. Parts 17–22 must carry the revised checkpoint truth and this exact capacity ledger.
- Planning-file STATE is separate from the learner's future application STATE/LEARNING_LOG/docs/evals files. Only docs/planning files are written by the mentor now.

### 11.2 Pending inputs and verification register

| ID | Pending item | Owner / due / default |
|---|---|---|
| Q-01 | Disk space, NVIDIA driver, WSL GPU pass-through and administrator rights; OS/RAM/GPU now confirmed | Learner / Day 1 / Windows + WSL2 path; smallest model first |
| Q-02 | Existing AWS account eligibility, acceptable signup/hold, hosted grant and repository visibility | Learner / Day 2–3 / local-only, hosted off, visibility unchanged |
| Q-03 | Corpus/dataset selection, exact redistribution/attribution and model package digests | Part 2 scouting then learner first use / authored/synthetic data |
| VFY-01 | uv-managed Python 3.12.15 availability; exact compatible dependency/tool pins, lock resolution, image/action/model digests and advisories | Part 4/first use / no claim of a tested environment |
| VFY-02 | Exact API/SDK/transport support for MCP and each admitted framework; official docs/changelog before **every** framework session | Learner/mentor at scheduled use / 🔎 verify until checked |
| VFY-03 | Actual model memory/quality/latency and any embedding leaderboard-based choice | Day 8/16 / no leaderboard superiority claim, measure own cases |
| VFY-04 | Exact AES-256 storage coverage, TLS 1.3 path, OS-specific free mechanism and backup protection | Part 4 + Parts 10–11 / synthetic local data until verified |
| VFY-05 | Kaggle account quota/verification/TPU terms; direct docs body inaccessible in this session | Conditional training only / 🔎 verify, no quota promise |
| VFY-06 | Jira automation/import fields and account limits; GitHub checks/protection on chosen visibility | Part 3/Part 23 and learner account / manual workflow, disclose unenforced protection |
| VFY-07 | Cloud-to-model topology, free compute capacity, teardown and automated live eval gate at $0 | C-03/C-21 / local model/local release; no full cloud or live-CI claim |
| VFY-08 | Ubuntu Engine/Compose exact packages, JDK/Maven, Inspector, Chroma/Qdrant and other deferred install/API versions | Part 4 or conditional Part before use / do not install unpinned optional tools |

No assumption currently blocks writing Part 2. If hardware arrives, narrow A-01 there and carry the decision into STATE. All listed external-policy/source checks were attempted or completed as stated; remaining account/runtime/API checks are not disguised as verified facts.

**Part 1 review result:** exact calendar and waterfall reconcile; all 24 components have a funded/deferred disposition; no application code/configuration/SQL/test script is delivered; first-use and gate routes retain Learn → explain-back → Return; costs/licenses and evidence limits are explicit. This is a reviewed plan, not a claim that the learner has passed any gate.

**NEXT: Part 2 — D9 Project Charter.** Include problem/users/use cases, success criteria, scope by rung, AI capability map, ≥3 public corpus candidates and ≥3 fine-tuning dataset candidates with dated verified licenses/redistribution/attribution, ≥2 local models + one hosted candidate, hardware-fit caveats, risks and a one-page truthful README/LinkedIn summary. Keep optional datasets useful as scouting without committing fine-tuning hours.


## 12. Resource index — checked 2026-10-01

Every external link introduced in this Part is indexed here. **verified** means the official page or stated official indexed text was retrieved on 2026-10-01. Runtime APIs, compatibility, account terms applied to this learner and measurements are not verified by a documentation lookup. The VFY register in §11 is the complete remaining-check list. Current documentation can move beyond a planning pin; select the pinned version before using examples. The learner later copies needed entries into docs/LEARNING_RESOURCES.md; the mentor writes only under docs/planning now.

| ID | Official resource | Access status on 2026-10-01 |
|---|---|---|
| R01 | [Scrum Guide](https://scrumguides.org/scrum-guide.html) | verified |
| R02 | [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install) | verified |
| R03 | [Ollama FAQ](https://docs.ollama.com/faq) | verified |
| R04 | [OWASP Threat Modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html) | verified |
| R05 | [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | verified |
| R06 | [OWASP Cryptographic Storage](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html) | verified |
| R07 | [OWASP TLS](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html) | verified |
| R08 | [BitLocker overview](https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/) | verified |
| R09 | [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/) | verified |
| R10 | [PostgreSQL 17 tutorial](https://www.postgresql.org/docs/17/tutorial.html) | verified |
| R11 | [pgvector official repository](https://github.com/pgvector/pgvector) | verified |
| R12 | [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) | verified |
| R13 | [Ollama API introduction](https://docs.ollama.com/api/introduction) | verified |
| R14 | [Ollama streaming](https://docs.ollama.com/api/streaming) | verified |
| R15 | [Ollama embeddings](https://docs.ollama.com/capabilities/embeddings) | verified |
| R16 | [Qwen3-0.6B publisher model card](https://huggingface.co/Qwen/Qwen3-0.6B) | verified |
| R17 | [Qwen3-0.6B Ollama artifact](https://ollama.com/library/qwen3:0.6b) | verified |
| R18 | [Qwen3-1.7B publisher model card](https://huggingface.co/Qwen/Qwen3-1.7B) | verified |
| R19 | [Qwen3-1.7B Ollama artifact](https://ollama.com/library/qwen3:1.7b) | verified |
| R20 | [nomic embedding publisher card](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5) | verified |
| R21 | [nomic Ollama catalog](https://ollama.com/library/nomic-embed-text) | verified |
| R22 | [React Quick Start](https://react.dev/learn) | verified |
| R23 | [TypeScript Handbook introduction](https://www.typescriptlang.org/docs/handbook/intro.html) | verified |
| R24 | [MDN Using server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) | verified |
| R25 | [How Compose works](https://docs.docker.com/compose/intro/compose-application-model/) | verified |
| R26 | [AWS Free Tier FAQ](https://aws.amazon.com/free/free-tier-faqs/) | verified |
| R27 | [AWS Budgets and limitations](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html) | verified official indexed text; account behavior unverified |
| R28 | [Ollama tool calling](https://docs.ollama.com/capabilities/tool-calling) | verified |
| R29 | [MCP architecture, version 2026-07-28](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture) | verified |
| R30 | [OWASP LLM Prompt Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) | verified |
| R31 | [uv Python management](https://docs.astral.sh/uv/guides/install-python/) | verified |
| R32 | [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) | verified |
| R33 | [GitHub Hello World](https://docs.github.com/en/get-started/using-github/hello-world) | verified |
| R34 | [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) | verified |
| R35 | [Understanding GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions) | verified |
| R36 | [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/) | verified |
| R37 | [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) | verified |
| R38 | [Python data structures](https://docs.python.org/3/tutorial/datastructures.html) | verified |
| R39 | [Python heapq](https://docs.python.org/3/library/heapq.html) | verified |
| R40 | [Pandas introductory tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html) | verified |
| R41 | [NumPy absolute basics](https://numpy.org/doc/stable/user/absolute_beginners.html) | verified |
| R42 | [pytest Get Started](https://docs.pytest.org/en/stable/getting-started.html) | verified |
| R43 | [GitHub About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) | verified |
| R44 | [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) | verified |
| R45 | [LlamaIndex framework overview](https://developers.llamaindex.ai/python/framework/) | verified |
| R46 | [n8n Community edition features](https://docs.n8n.io/deploy/host-n8n/community-edition-features.md) | verified |
| R47 | [Hugging Face PEFT introduction](https://huggingface.co/docs/peft/index) | verified |
| R48 | [MongoDB manual](https://www.mongodb.com/docs/manual/) | verified |
| R49 | [Spring Boot overview](https://docs.spring.io/spring-boot/index.html) | verified |
| R50 | [kind Quick Start](https://kind.sigs.k8s.io/docs/user/quick-start/) | verified |
| R51 | [GitHub SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) | verified |
| R52 | [uv installation](https://docs.astral.sh/uv/getting-started/installation/) | verified |
| R53 | [Jira getting started](https://support.atlassian.com/jira-software-cloud/docs/get-started-with-jira-software-cloud/) | verified official indexed text |
| R54 | [AWS new signup](https://docs.aws.amazon.com/accounts/latest/reference/sign-in-new.html) | verified |
| R55 | [pnpm installation](https://pnpm.io/installation) | verified |
| R56 | [Get Docker](https://docs.docker.com/get-started/get-docker/) | verified |
| R57 | [VS Code getting started](https://code.visualstudio.com/docs/getstarted/overview) | verified |
| R58 | [MCP Python SDK documentation](https://py.sdk.modelcontextprotocol.io/) | verified |
| R59 | [AWS CLI installation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) | verified |
| R60 | [Colab FAQ](https://research.google.com/colaboratory/faq.html) | verified |
| R61 | [Playwright installation](https://playwright.dev/docs/intro) | verified |
| R62 | [k6 installation](https://grafana.com/docs/k6/latest/set-up/install-k6/) | verified |
| R63 | [AWS advanced signup](https://docs.aws.amazon.com/accounts/latest/reference/getting-started.html) | verified |
| R64 | [Claude API pricing](https://platform.claude.com/docs/en/about-claude/pricing) | verified |
| R65 | [Kaggle Efficient GPU Usage Tips](https://www.kaggle.com/docs/efficient-gpu-usage) | verified official indexed quota text only; 🔎 verify full page/account quota |
| R66 | [n8n Community license](https://docs.n8n.io/n8n-community-license/community-license) | verified |
| R67 | [n8n license FAQ](https://docs.n8n.io/n8n-community-license/community-license/license-faq) | verified |
| R68 | [MongoDB free database setup](https://www.mongodb.com/resources/products/fundamentals/create-database) | verified |
| R69 | [Atlas Free cluster limits](https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/) | verified |
| R70 | [GitHub plans](https://docs.github.com/en/get-started/learning-about-github/githubs-plans) | verified official indexed text |
| R71 | [Managing protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches?apiVersion=2022-11-28) | verified official indexed text |
| R72 | [Jira pricing](https://www.atlassian.com/software/jira/jira/pricing) | verified official indexed plan text; 🔎 verify account automation quota |
| R73 | [Plaid Sandbox](https://plaid.com/docs/sandbox/) | verified official indexed text |
| R74 | [Plaid Free/Trial FAQ](https://support.plaid.com/hc/en-us/articles/16194695660311-Can-I-use-Plaid-for-free) | verified official indexed text; not account eligibility |
| R75 | [Docker Desktop license](https://docs.docker.com/subscription-billing/desktop-license/) | verified |
| R76 | [Google public code-review guide](https://google.github.io/eng-practices/review/reviewer/) | verified |
| V01 | [Python 3.12.15 release](https://www.python.org/downloads/release/python-31215/) | verified |
| V02 | [uv releases](https://github.com/astral-sh/uv/releases) | verified |
| V03 | [Node.js releases](https://nodejs.org/en/about/previous-releases) | verified |
| V04 | [pnpm releases](https://github.com/pnpm/pnpm/releases) | verified |
| V05 | [Docker Desktop releases](https://docs.docker.com/desktop/release-notes/) | verified |
| V06 | [FastAPI release notes](https://fastapi.tiangolo.com/release-notes/) | verified |
| V07 | [PostgreSQL 17.11 release](https://www.postgresql.org/docs/release/17.11/) | verified |
| V08 | [pgvector changelog](https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md?plain=1) | verified |
| V09 | [React versions](https://react.dev/versions) | verified |
| V10 | [TypeScript releases](https://github.com/microsoft/TypeScript/releases) | verified |
| V11 | [Ollama releases](https://github.com/ollama/ollama/releases) | verified |
| V12 | [MCP Python SDK releases](https://github.com/modelcontextprotocol/python-sdk/releases) | verified |
| V13 | [LangChain releases](https://github.com/langchain-ai/langchain/releases) | verified |
| V14 | [LangGraph releases](https://github.com/langchain-ai/langgraph/releases) | verified |
| V15 | [LlamaIndex releases](https://github.com/run-llama/llama_index/releases) | verified |
| V16 | [n8n releases](https://github.com/n8n-io/n8n/releases) | verified |

Link corrections observed during research: GitHub Hello World and VS Code setup redirect to the listed canonical paths; MCP architecture redirects to the dated specification. Old n8n sustainable-use-license/community-edition paths returned Page Not Found; only the working moved pages above are used. The non-www Conventional Commits URL failed, while the indexed www URL opened successfully. Kaggle direct extraction failed; indexed-text verification is explicitly narrower. No inaccessible page is presented as fully read.

[R01]: https://scrumguides.org/scrum-guide.html
[R02]: https://learn.microsoft.com/en-us/windows/wsl/install
[R03]: https://docs.ollama.com/faq
[R04]: https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html
[R05]: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
[R06]: https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
[R07]: https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html
[R08]: https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/
[R09]: https://fastapi.tiangolo.com/tutorial/
[R10]: https://www.postgresql.org/docs/17/tutorial.html
[R11]: https://github.com/pgvector/pgvector
[R12]: https://alembic.sqlalchemy.org/en/latest/tutorial.html
[R13]: https://docs.ollama.com/api/introduction
[R14]: https://docs.ollama.com/api/streaming
[R15]: https://docs.ollama.com/capabilities/embeddings
[R16]: https://huggingface.co/Qwen/Qwen3-0.6B
[R17]: https://ollama.com/library/qwen3:0.6b
[R18]: https://huggingface.co/Qwen/Qwen3-1.7B
[R19]: https://ollama.com/library/qwen3:1.7b
[R20]: https://huggingface.co/nomic-ai/nomic-embed-text-v1.5
[R21]: https://ollama.com/library/nomic-embed-text
[R22]: https://react.dev/learn
[R23]: https://www.typescriptlang.org/docs/handbook/intro.html
[R24]: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
[R25]: https://docs.docker.com/compose/intro/compose-application-model/
[R26]: https://aws.amazon.com/free/free-tier-faqs/
[R27]: https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html
[R28]: https://docs.ollama.com/capabilities/tool-calling
[R29]: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture
[R30]: https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html
[R31]: https://docs.astral.sh/uv/guides/install-python/
[R32]: https://semver.org/spec/v2.0.0.html
[R33]: https://docs.github.com/en/get-started/using-github/hello-world
[R34]: https://www.conventionalcommits.org/en/v1.0.0/
[R35]: https://docs.github.com/en/actions/get-started/understand-github-actions
[R36]: https://docs.sqlalchemy.org/en/20/tutorial/
[R37]: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
[R38]: https://docs.python.org/3/tutorial/datastructures.html
[R39]: https://docs.python.org/3/library/heapq.html
[R40]: https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html
[R41]: https://numpy.org/doc/stable/user/absolute_beginners.html
[R42]: https://docs.pytest.org/en/stable/getting-started.html
[R43]: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
[R44]: https://docs.langchain.com/oss/python/langgraph/overview
[R45]: https://developers.llamaindex.ai/python/framework/
[R46]: https://docs.n8n.io/deploy/host-n8n/community-edition-features.md
[R47]: https://huggingface.co/docs/peft/index
[R48]: https://www.mongodb.com/docs/manual/
[R49]: https://docs.spring.io/spring-boot/index.html
[R50]: https://kind.sigs.k8s.io/docs/user/quick-start/
[R51]: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
[R52]: https://docs.astral.sh/uv/getting-started/installation/
[R53]: https://support.atlassian.com/jira-software-cloud/docs/get-started-with-jira-software-cloud/
[R54]: https://docs.aws.amazon.com/accounts/latest/reference/sign-in-new.html
[R55]: https://pnpm.io/installation
[R56]: https://docs.docker.com/get-started/get-docker/
[R57]: https://code.visualstudio.com/docs/getstarted/overview
[R58]: https://py.sdk.modelcontextprotocol.io/
[R59]: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
[R60]: https://research.google.com/colaboratory/faq.html
[R61]: https://playwright.dev/docs/intro
[R62]: https://grafana.com/docs/k6/latest/set-up/install-k6/
[R63]: https://docs.aws.amazon.com/accounts/latest/reference/getting-started.html
[R64]: https://platform.claude.com/docs/en/about-claude/pricing
[R65]: https://www.kaggle.com/docs/efficient-gpu-usage
[R66]: https://docs.n8n.io/n8n-community-license/community-license
[R67]: https://docs.n8n.io/n8n-community-license/community-license/license-faq
[R68]: https://www.mongodb.com/resources/products/fundamentals/create-database
[R69]: https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/
[R70]: https://docs.github.com/en/get-started/learning-about-github/githubs-plans
[R71]: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches?apiVersion=2022-11-28
[R72]: https://www.atlassian.com/software/jira/jira/pricing
[R73]: https://plaid.com/docs/sandbox/
[R74]: https://support.plaid.com/hc/en-us/articles/16194695660311-Can-I-use-Plaid-for-free
[R75]: https://docs.docker.com/subscription-billing/desktop-license/
[R76]: https://google.github.io/eng-practices/review/reviewer/
[V01]: https://www.python.org/downloads/release/python-31215/
[V02]: https://github.com/astral-sh/uv/releases
[V03]: https://nodejs.org/en/about/previous-releases
[V04]: https://github.com/pnpm/pnpm/releases
[V05]: https://docs.docker.com/desktop/release-notes/
[V06]: https://fastapi.tiangolo.com/release-notes/
[V07]: https://www.postgresql.org/docs/release/17.11/
[V08]: https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md?plain=1
[V09]: https://react.dev/versions
[V10]: https://github.com/microsoft/TypeScript/releases
[V11]: https://github.com/ollama/ollama/releases
[V12]: https://github.com/modelcontextprotocol/python-sdk/releases
[V13]: https://github.com/langchain-ai/langchain/releases
[V14]: https://github.com/langchain-ai/langgraph/releases
[V15]: https://github.com/run-llama/llama_index/releases
[V16]: https://github.com/n8n-io/n8n/releases
