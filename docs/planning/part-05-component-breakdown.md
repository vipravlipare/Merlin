# Part 05 — D11 Component Breakdown

Status: planning specification. Components are boundaries for later checklists, stories and evidence. The learner writes implementation code and configuration.

## 1. Dependency graph and build order

C-01 Repo/tooling → C-02 Environment/Compose → C-03 CI/quality → C-04 Data → C-05 Identity/security → C-06 API → C-07 Notes and C-08 Tasks → C-09 Gateway/Ollama → C-10 Ingestion → C-11 Embeddings/vector → C-12 RAG/evals → C-13 Tools/agents → C-14 MCP/approvals → C-15 UI/chat → C-20 Observability → C-21 Deploy → C-23 QA/hardening → C-22 Portfolio.

C-16 Frameworks, C-17 n8n, C-18 fine-tuning, C-19 Mongo/Spring and C-24 optional modules branch only after their scratch/core gates and an explicit swap.

📚 Learn first: [OWASP Threat Modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html), read system modeling; stop before threat tools; why: boundaries precede components (~10 min).
↩ Return: draw this graph in notes; done when each arrow has a dependency reason; time box 15 min; if stuck: identify the first data owner.

## 2. Component matrix

| ID | Purpose / interface / MVP slice | Dependencies; skills; target depth | Likely L/I; risk; demo |
|---|---|---|---|---|
| C-01 Repo & tooling | Git, Jira, hooks, issue templates, branch/review convention. MVP: clean setup PR. | none; SK-22; A | 1/2; account limits; show issue→PR→merge. |
| C-02 Environment & Compose | Windows/WSL2, Docker, Postgres/Redis profiles, health. MVP: local core profile. | C-01; SK-19; A | 3/3; 16 GB pressure; start/stop/doctor. |
| C-03 CI/CD & quality | lint/types/tests/build/scan/eval gate specs. MVP: green CI skeleton. | C-01/02; SK-19/20; A | 2/3; hosted runner cannot run Ollama; show checks and fixture gate. |
| C-04 Data layer | owner-scoped tables, migrations, transactions, restore. MVP: users/notes/tasks/source records. | C-02; SK-4/18; A | 2/3; migration mistakes; explain rollback/EXPLAIN. |
| C-05 Identity/security | password hashing, short JWT, roles, owner checks, validation/rate limits. MVP: login and isolation. | C-04/06; SK-21; A | 1.5/2.5; security gaps; demonstrate denial cases. |
| C-06 API foundation | FastAPI routes, dependency boundary, errors, health, SSE contract. MVP: health + one typed route. | C-02/04/05; SK-4; A | 1.5/2.5; beginner async; API docs/test table. |
| C-07 Notes | folders, markdown, tags, backlinks, safe save/export. MVP: CRUD + owner filter. | C-04/05/06; SK-2/3; A | 2/3; editor scope; save/search demo. |
| C-08 Tasks | deadlines, heap order, recurrence placeholder. MVP: create/list/prioritize. | C-04/05/06; SK-3; A | 1.5/2.5; recurrence cut; ordered task demo. |
| C-09 LLM gateway/Ollama | provider interface, streaming, structured output, retries, usage. MVP: local Qwen smoke route. | C-02/06; SK-5/6; A | 4/5; hardware/model quality; TTFT demo. |
| C-10 Ingestion | markdown/CSV parse, clean, dedupe, chunk, idempotency, failure record. MVP: notes + fixed expense CSV. | C-04/09; SK-1/8; A | 3/4; malformed data; repeat import demo. |
| C-11 Embeddings/vector | cosine from scratch, local embedding, pgvector exact search, version. MVP: owner-filtered top-k. | C-04/09/10; SK-1/7/9; A | 2.5/3.5; dimension mismatch; recall/latency table. |
| C-12 RAG/evals | retrieve, prompt, citations, refusal, golden set, baseline. MVP: measured cited answer. | C-09/11; SK-10/20; A | 3/4; hallucination/injection; eval report. |
| C-13 Tools/agent runtime | registry, schema validation, bounds, profiles, memory/traces. MVP: one bounded loop, three profiles. | C-05/09/12; SK-12/13; A | 3.5/4.5; loops/misuse; trace and denied call. |
| C-14 MCP/approvals | MCP server/client, scopes, approval queue, replay defense. MVP: read tool + approved mutation. | C-13/05; SK-16/21; A | 3/4; confused deputy; inspector/contract evidence. |
| C-15 UI/chat | React forms, notes/tasks, citations, SSE, tool cards. MVP: minimal vertical UI. | C-06/07/08/12/14; SK-2; B | 3/4; beginner TS; manual integration demo. |
| C-16 Framework rebuilds | optional LangChain/LangGraph/LlamaIndex comparisons. MVP: none funded. | C-12/13/14; SK-11/14; B | 0/0 funded; scratch gate; same-set ADR. |
| C-17 n8n | optional authenticated workflows. MVP: none funded. | C-06/13; SK-15; B | 0/0; fair-code terms; equivalent workflow only if swap. |
| C-18 Fine-tuning | optional tiny classifier, baseline/held-out set. MVP: none funded. | C-09/12; SK-17; B | 0/0; quota/license; report unbuilt. |
| C-19 MongoDB/Spring audit | optional trace service. MVP: none funded. | C-13/20; SK-4/18; B | 0/0; duplicated storage; Postgres remains source. |
| C-20 Observability | redacted logs, traces, timing, cost fields. MVP: structured local traces. | C-06/09/13; SK-20; A | 1/2; sensitive logs; inspect trace. |
| C-21 Cloud/platform | local release, optional AWS path, kind deferred. MVP: local runbook. | C-02/03/20; SK-19; B | 1.5/1.5; cost/eligibility; teardown evidence. |
| C-22 Docs/portfolio | README, ADR index, demo, resume/LinkedIn. MVP: truthful v0 README. | all; SK-22; A | 1.5/4.5; claims drift; reviewer runs demo. |
| C-23 QA/hardening | restore, fault, injection, security, manual/API checks. MVP: core break-it set. | all funded core; SK-20/21/22; A | 1.5/4.4; time squeeze; failure report. |
| C-24 Optional modules | clock, calendar, Plaid, native/mobile. MVP: none. | core; depth C | 0/0; scope explosion; backlog only. |

Likely total: 42 learning + 62.9 implementation = 104.9. Low total 72.5; high total 173.5. Optional rows have zero committed hours.

📚 Learn first: [Jira work items](https://support.atlassian.com/jira-software-cloud/docs/create-a-work-item-and-a-subtask/), read work item/subtask distinction; stop before automation; why: each component becomes traceable work (~8 min).
↩ Return: create a component register with owner, dependencies, target rung, hours and evidence; done when later checklist IDs can point to one component; time box 20 min; if stuck: register C-01 first.

## 3. Vertical slices by rung

- Walking skeleton: C-01–06 plus the smallest C-09 local contract, with C-03 checks.
- Knowledge core: C-07–12 and the smallest C-15 UI, with C-20 traces and C-23 denial/restore checks.
- Agentic core: C-13–15, C-14 approval/MCP, C-20 eval traces, C-21 local deployment.
- Framework/platform: C-16–19 and C-21 extensions only after scratch acceptance and swap.
- Ship: C-22/23 hardening and evidence; no new feature Days 36–37.

Each slice must have a user-visible path, one security case, one performance/negative case, one evidence artifact and a stop boundary.

## 4. Traceability starter

| JD keyword | Components | First proving evidence |
|---|---|---|
| FastAPI/PostgreSQL | C-04/06 | health, migration, owner-filter test |
| Docker/CI/CD | C-02/03 | Compose health, green CI, image/scan spec |
| Pandas/NumPy/ingestion | C-10 | three-row clean/reject/dedupe table |
| Embeddings/vector DB/RAG | C-11/12 | recall/MRR/citation report |
| LLM APIs/Ollama | C-09 | local stream, TTFT/tokens, deny-hosted test |
| agents/tool use/MCP | C-13/14 | bounded trace, approval and replay denial |
| React/TypeScript | C-15 | manual UI integration |
| AWS/Kubernetes | C-21 | local runbook; cloud/kind only if built |
| LangChain/LangGraph/LlamaIndex/n8n | C-16/17 | same-golden-set comparison only |
| fine-tuning | C-18 | baseline/held-out F1 only if funded |
| MongoDB/Spring/Redis | C-19/02 | studied or actual slice, never implied by install |
| security/observability | C-05/20/23 | threat case, redacted trace, fault report |

📚 Learn first: [Google engineering practices](https://google.github.io/eng-practices/), read code review overview; stop before language-specific guides; why: evidence should be reviewable (~8 min; 🔎 verify index at first use).
↩ Return: add story/checklist/evidence columns in Parts 6–9; done when every funded component maps to a day and JD keyword or an honest downgrade; time box 20 min; if stuck: mark “studied” instead of inventing proof.

## 5. Acceptance and resources

D11 passes when C-01–C-24 each has purpose, interface, dependency, MVP, extension/rung, skill, hours, risk and demo; the critical path and cut line are visible; no optional component receives hidden hours.

Resources checked 2026-10-01: [PostgreSQL tutorial](https://www.postgresql.org/docs/17/tutorial.html), [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/), [Docker Compose model](https://docs.docker.com/compose/intro/compose-application-model/), [OWASP authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), [GitHub Actions concepts](https://docs.github.com/en/actions/get-started/understand-github-actions) — verified. Jira work-item page — verified indexed text. Context7 MCP unavailable.

NEXT: Part 6 — D12 Component Checklists, first half.

