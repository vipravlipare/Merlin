# Part 02 — D9 Project Charter

**Status: planning only. Prepared 2026-10-01.** No corpus, dataset, model, account, application code or fine-tune has been selected or run. Hardware: **Windows, 16 GB RAM, NVIDIA RTX 3050, 4 GB VRAM**. Disk space, driver, WSL GPU pass-through and administrator rights remain to be checked on Day 1.

## 1. Charter decision

Merlin is a private, local-first “second brain” for notes, tasks and synthetic expense analysis. It turns a learner’s own knowledge into searchable evidence and lets a bounded assistant propose or perform narrowly scoped actions with a human approval step.

The project proves from-scratch engineering judgment:

- secure modular backend and minimal web UI;
- ingestion, embeddings, vector retrieval and cited RAG;
- provider boundary over a local model;
- bounded tool loop, three role profiles and MCP;
- measured quality, latency, token usage and cost.

The project does not promise production reliability, current financial advice, autonomous spending, a general-purpose assistant, managed Kubernetes, or mastery of every named framework.

📚 Learn first (Must read | Deep dive): [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html), read “Overview” and “System Modeling”; stop before tool references; why: the charter must name assets, trust boundaries and misuse before features (~15 min).
Explain back: What private asset would be harmed if retrieval ignored the requesting user?
↩ Return to build: write the charter asset/boundary list in the learner’s planning notes; done when each proposed capability has an owner, data class and denial behavior; time box: 20 min within C-01/C-05; if stuck: hint rung 1—start with notes, expense rows, tokens and tool permissions.

## 2. Problem and users

### Primary user: the learner

The learner has notes spread across markdown files, tasks in several places and expense exports that are difficult to query together. Merlin makes one small, explainable system the place to practice:

- capture and organize a note;
- turn a note into a task;
- ask a question and see source citations;
- inspect a proposed agent action;
- approve or deny a mutation;
- measure whether retrieval and tool use worked.

### Secondary persona: interview reviewer

A reviewer needs a short reproducible path, seeded data, release evidence and truthful boundaries. The reviewer should be able to see the architecture, run the checks, inspect an evaluation report and ask why local-first, PostgreSQL, scratch RAG, MCP and approval gates were chosen.

The reviewer is not a production customer. No real person’s private notes, bank credentials or financial records enter the public demo.

### Problem statement

A beginner with fragmented notes, tasks and CSV exports needs one local-first system that can retrieve evidence and suggest bounded actions while preserving data ownership and making every AI claim measurable. Existing familiarity with APIs and team projects is not evidence of independent build ability, so each capability must be rebuilt, tested and explained from a blank file.

### Non-goals

- production bank connections or Bank of America access;
- autonomous financial transactions, purchases, account changes or deletion;
- medical, legal or financial advice;
- public hosting of private data;
- model training on private notes without a separate consent and license decision;
- a full collaborative editor, mobile app, native alarm writer or microservice estate;
- framework-first agent code;
- a claim of “secure” based only on using a library or container.

📚 Learn first (Must read): [Scrum Guide](https://scrumguides.org/scrum-guide.html), read “Product Goal” and “Sprint Goal”; stop before the appendix; why: a product goal states the outcome without turning every possible feature into a commitment (~10 min).
Explain back: Which non-goal protects the learner from silently becoming a financial product?
↩ Return to build: add the problem, primary/secondary personas and non-goals to the learner’s charter notes; done when a reviewer can tell what Merlin will refuse to do; time box: 15 min within C-01; if stuck: hint rung 1—write the unsafe request Merlin must decline.

## 3. Use cases and capability boundaries

| ID | User asks | Merlin may do | Merlin must never do | Evidence |
|---|---|---|---|---|
| UC-01 | “Save this markdown note under folder X with tags.” | Store a note after input validation and owner check. | Execute arbitrary filesystem commands or accept another user’s folder ID. | Notes acceptance table, owner-isolation test |
| UC-02 | “What did I write about vector search?” | Retrieve owned chunks and answer with source IDs/citations; refuse when evidence is absent. | Treat retrieved prose as an instruction or reveal another user’s chunks. | RAG golden set, citation report |
| UC-03 | “Make tomorrow’s highest-priority task.” | Propose task fields; require approval before mutation. | Create, edit or delete a task without exact approval. | Planner tool trace, denied/replay cases |
| UC-04 | “How much did category X cost in this synthetic CSV?” | Parse validated synthetic rows and calculate deterministic totals; optionally explain. | Infer real financial advice or send private rows to a hosted model without consent/redaction. | Pandas baseline, analyst cases |
| UC-05 | “Run this through my model.” | Use the local provider if enabled and record model/digest/timing. | Fall back silently to a hosted API or expose secrets in prompts/logs. | Gateway deny-path test, redacted trace |
| UC-06 | “Let my MCP client search notes.” | Expose scoped read tools; expose mutations only behind approval. | Accept an unknown client/tool scope or confuse protocol success with business authorization. | MCP contract and permission tests |
| UC-07 | “Show an interview reviewer what I built.” | Serve seeded data, diagrams, tests, metrics and a truthful claim list. | Present studied/unbuilt slices as shipped. | README, release notes, evidence map |

📚 Learn first (Must read | Deep dive): [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html), read indirect injection and tool-related defenses; stop before unrelated examples; why: notes, CSVs and tool output are untrusted data (~15 min).
Explain back: Why can a note contain an instruction that Merlin must display but must not obey?
↩ Return to build: convert UC-01–UC-07 into later story acceptance cases; done when every mutating use case has an approval, owner and negative case; time box: 25 min within C-05/C-13/C-14; if stuck: hint rung 2—separate “model proposes” from “server authorizes.”

## 4. Scope by rung and stop-here claims

Fixed dates remain review checkpoints. Part 1 capacity overrides the original assumption that each checkpoint’s entire feature list will fit.

| Rung | Checkpoint | Charter scope | Stop-here claim |
|---|---|---|---|
| Walking skeleton | Day 11 | Local Compose path, FastAPI health/validation, learner-written migrations, basic auth, CI skeleton, provider contract and bounded local streaming probe if gates pass. | “I set up and explained a from-scratch SDLC slice, API boundary, basic auth and local model contract.” |
| Knowledge core | Target about Day 26; original checkpoint Day 19 is a review | Notes/tasks slice, markdown + CSV ingestion, embeddings, pgvector exact retrieval, cited RAG, export/restore, minimal UI, ≥20-case retrieval/RAG golden subset. | “I built and measured a local notes/task/RAG slice with citations and owner filtering.” |
| Agentic core | Target about Day 33; original checkpoint Day 26 is a review | Shared bounded runtime with Notes Librarian, Planner and Budget Analyst profiles; scoped tools, approvals, redaction/consent, MCP server/client, agent UI trace, eval/CI contract, local deployment. AWS only if eligible and verified. | “I built a from-scratch bounded tool loop with MCP and approval controls against seeded/local data.” |
| Framework/platform slice | Conditional after scratch gates; original checkpoint Day 33 is a review | LangChain/LangGraph, n8n, LlamaIndex, fine-tune, MongoDB/Spring, kind or vector comparison only through explicit swaps. | Only slices with measured evidence are claimable; reading is “studied.” |
| Ship | Day 37 | Highest complete rung, hardening, runbook, README, demo, resume/LinkedIn evidence map. No new features Days 36–37. | Claims match completed evidence; unmet work remains visible. |

Stop-anywhere rule: a release cannot use the next rung’s name when its definition is incomplete. If model, UI, AWS or framework work fails, preserve the completed lower rung and document the failing gate.

📚 Learn first (Must read): [GitHub About README files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes), read the content overview; stop before advanced formatting; why: a stop-here claim must be reproducible by someone else (~10 min).
↩ Return to build: maintain a claim table with “built,” “studied,” “blocked,” evidence link and next action; done when the README never calls an incomplete rung built; time box: 20 min inside C-22; if stuck: hint rung 1—delete an unsupported adjective.

## 5. Measurable success criteria

| Outcome | Minimum measurable criterion | Proof artifact | Honest limit |
|---|---|---|---|
| Daily-use usefulness | Seeded note save, task create, search, citation view, export and restore each work in own acceptance cases. | Merged PRs, case tables, restore log, screenshots | Not a usability study; learner dogfooding is one person. |
| Knowledge quality | ≥20 retrieval/RAG cases; recall@5 target ≥0.80; citation-source validity 100%; missing-evidence refusals pass; baseline reported. | Versioned eval report and golden set | Target; failure narrows claims. |
| Agent safety | ≥20 tagged agent/MCP cases; unauthorized, changed-argument and replayed mutations = 0; tool accuracy target ≥0.90; limits exercised. | Agent trace, security report, approval audit | Does not prove all prompt attacks are stopped. |
| Latency | Record cold/warm p50/p95 retrieval, total response and TTFT; diagnostic target local TTFT p95 ≤5 s and total p95 ≤30 s. | Benchmark with hardware/model/digest and sample counts | RTX 3050/4 GB and 16 GB RAM may not meet it. |
| Cost/privacy | Local default; hosted calls disabled unless consented and budgeted; no secrets/private demo data in logs/public artifacts. | Provider deny-path, redaction and spend record | Existing electricity/internet not claimed free. |
| Engineering quality | Current revision passes defined checks; clean clone follows runbook; main remains deployable. | CI evidence, clean-clone log, review checklist | No enterprise availability or on-call claim. |
| Learning proof | Each major skill has explain-back, green own-code test, blank-page whiteboard and 2–3 day re-quiz. | LEARNING_LOG entries and quiz results | Reading alone is “studied.” |
| Portfolio/interview | 2-minute walkthrough, architecture diagram, ADR index, truthful claim list, seeded demo and one measured AI result. | README, demo script, resume evidence map | No seniority or production ownership claim. |

📚 Learn first (Must read): [pytest Get Started](https://docs.pytest.org/en/stable/getting-started.html), read assertions and fixtures; stop before plugin guidance; why: measurable success needs repeatable inputs (~15 min).
↩ Return to build: write the success table into the charter and map each row to a test/eval artifact; done when reviewer can find metric and evidence; time box: 20 min within C-03/C-12/C-22; if stuck: hint rung 1—one criterion, one artifact, one limit.

## 6. Public corpus scouting for RAG

A candidate is not license-cleared for redistribution until exact revision, attribution and local copy hash are recorded. A public URL does not itself grant redistribution rights.

| Candidate | License/attribution found 2026-10-01 | Format/fit | Recommendation |
|---|---|---|---|
| Python documentation | Python documentation: PSF License Agreement; examples/recipes from 3.8.6 onward dual PSF + Zero-Clause BSD. Retain notices. | HTML; beginner-relevant official API corpus. | Primary: small page allowlist with source URLs/revision. |
| Kubernetes documentation | Official repository/site licensing material identifies CC BY 4.0; attribution/link required. Embedded third-party assets require separate checks. | Markdown/HTML; platform corpus. | Secondary small deployment slice if hours allow. |
| MDN Web Docs | Generally CC BY-SA 2.5 or later; attribute Mozilla Contributors; derivatives preserve license family. | HTML; web/SSE/security pages. | Link-first; import only a narrow revision after accepting share-alike. |
| Learner-authored Merlin notes | Learner-owned, no external redistribution issue. | Markdown; exact domain relevance. | Always include; private notes stay local. |

Selected corpus plan: learner-authored notes plus a small Python documentation allowlist. Kubernetes and MDN remain alternates. First corpus version records source URL, title, retrieval date, revision/commit, license, attribution, excluded assets and content hash. Do not scrape an entire site.

📚 Learn first (Must read): [Python documentation license](https://docs.python.org/3/license.html), read terms and conditions; stop before incorporated-software list; why: source permissions differ from “free to read” (~10 min). [MDN attribution and license](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Attrib_copyright_license), read documentation licensing; stop before code examples; why: share-alike can affect a redistributed corpus (~10 min).
↩ Return to build: create the corpus record in planning notes; done when one allowlist has license, attribution, revision and hash fields; time box: 25 min within C-10; if stuck: learner-authored notes only.

## 7. Fine-tuning dataset scouting

Fine-tuning is not funded in Part 1. These candidates are for a tiny note-intent classifier only if a later swap funds labeling, training, held-out evaluation and license review. Dataset-host metadata is evidence to investigate, not a substitute for original terms.

| Candidate | License/size evidence found 2026-10-01 | Possible use | Constraints/recommendation |
|---|---|---|---|
| PolyAI BANKING77 | Hugging Face card: CC BY 4.0; 13,083 queries, 77 intents; metadata lists 10,003 train and 3,080 test. | Fine-grained intent baseline and Budget Analyst routing concept. | Banking text is not Merlin notes; no banking integration. Best external benchmark candidate after source terms/attribution record. |
| BLiMP | Hugging Face card metadata: CC BY 4.0; 67 grammatical subsets, 1,000 minimal pairs each. | Evaluation-only language sanity check. | Not a note classifier; no domain-transfer claim. Verify current card before use. |
| AG News | Candidate card metadata: Apache-2.0, text classification, 100K–1M band. | Lightweight topic-classification pipeline baseline. | Source-level provenance/terms still require checking; do not import until recorded. |
| Learner-authored synthetic note-intent set | Learner-created text/labels; repository license can be chosen. | Actual note classifier: reference, task, decision, question, sensitive, ignore. | Small but relevant; difficult negatives, leakage checks, train/validation/test and separate ≥20-case holdout required. Preferred final source if funded. |

Do not fine-tune on BANKING77, BLiMP or AG News as if they were Merlin notes. Use one external dataset for a reproducible baseline or pipeline exercise, then use learner-authored/synthetic notes for the actual claim. Never train on private notes without consent and retention/deletion decisions.

📚 Learn first (Must read): [Hugging Face dataset licenses](https://huggingface.co/docs/hub/main/en/repositories-licenses), read license metadata guidance; stop before creating a repository; why: dataset cards do not erase source obligations (~10 min). [Hugging Face PEFT](https://huggingface.co/docs/peft/index), read introduction; stop before installation; why: parameter-efficient fine-tuning still needs a baseline and held-out set (~10 min).
↩ Return to build: create a dataset decision record only if C-18 receives a swap; done when source license, attribution, revision, splits, leakage check and baseline are recorded; time box: 25 min inside conditional C-18; if stuck: learner-authored synthetic labels and defer external data.

## 8. Model choices and hardware fit

Hardware is sufficient to test small quantized local models, but 4 GB VRAM and 16 GB system RAM are constraints. Download size is not total runtime memory. Context length, KV cache, concurrent services, GPU offload and Docker/WSL overhead matter. First benchmark: sequential, short-context, local.

| Candidate | License/evidence | Hardware decision | Use |
|---|---|---|---|
| Qwen3 0.6B through Ollama | Publisher card: Apache-2.0; Ollama package about 523 MB Q4_K_M. | Default first probe; easiest fit likely. Quality unknown. | Gateway smoke, structured output and local baseline. |
| Qwen3 1.7B through Ollama | Publisher card: Apache-2.0; Ollama package about 1.4 GB Q4_K_M. | Second probe only after 0.6B; leave memory for Postgres/browser/Docker. | Same-case quality/latency comparison. |
| nomic-embed-text v1.5 through Ollama | Publisher card: Apache-2.0; Ollama catalog about 274 MB. Prefixes, dimensions and truncation require installed-artifact verification. | Embedding candidate; measure separately from chat model. | Local embeddings for pgvector/exact retrieval. |
| Anthropic Claude API | Official pricing documents billed token usage; exact model/limits/grant are account-dependent. | Hosted comparison candidate only; no calls before consent, redaction, spend limit and eligibility. | Synthetic-fixture provider contract and optional quality comparison. |

Model selection gate:

1. Record driver, WSL GPU visibility, free disk, idle RAM/VRAM and Docker limits.
2. Run the same short golden subset on Qwen3 0.6B.
3. Record cold/warm latency, TTFT, total latency, tokens/sec, peak memory, malformed structured outputs and tool-call accuracy.
4. Try Qwen3 1.7B only if the machine remains responsive.
5. Keep the smaller model if adequate; otherwise report the limit and narrow claims. Do not silently download a 7B model or move private data to a hosted provider.

📚 Learn first (Must read): [Ollama FAQ](https://docs.ollama.com/faq), read memory/concurrency/model-loading; stop before proxy configuration; why: model fit is measured runtime behavior (~10 min). [Ollama embeddings](https://docs.ollama.com/capabilities/embeddings), read model usage; stop before unrelated endpoints; why: chat and embedding memory/latency differ (~10 min).
↩ Return to build: Day 8 smoke test; done when driver/pass-through, model digest, peak memory, TTFT, total latency and tokens/sec are recorded; time box: 30 min in C-09; if stuck: Qwen3 0.6B, shorter context, one request at a time.

## 9. Top risks and triggers

| Risk | Trigger | Response/swap |
|---|---|---|
| Hardware pressure | WSL/Docker/model swaps or OOM | Reduce context/concurrency; use 0.6B; defer framework containers; preserve quality report. |
| Local quality too low | Tool accuracy/citation/refusal target fails | Narrow tasks, strengthen deterministic checks/retrieval, report failure; no silent hosted fallback. |
| Corpus ambiguity | Revision/source terms cannot be documented | Learner-authored notes and link-only references; do not redistribute ambiguous text. |
| Dataset mismatch | External labels do not represent note intents | Synthetic note labels or pipeline-only external data. |
| Fine-tuning quota/session | Colab/Kaggle access/time inadequate | CPU tiny experiment or defer; no deadline claim. |
| AWS charge risk | Paid plan, card hold or uncertain limits | Local Compose release; AWS studied/unbuilt. |
| Scope overrun | Core story exceeds likely hours | Stop at last complete rung; remove optional work; reserve is not feature budget. |
| Sensitive leakage | Private text appears in hosted request/log/demo | Block, redact, clean/rotate artifact, use seeded data and record incident. |
| Evaluation gaming | Threshold changes after failure | Freeze cases/metrics before rerun; preserve failed reports. |

📚 Learn first (Must read): [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html), read alert limitations; stop before service setup; why: an alarm is not a hard spending cap (~5 min).
↩ Return to build: add risks to the learner’s register; done when each trigger can cause a named scope change; time box: 20 min within C-01/C-21; if stuck: remove the optional item nearest the cut line.

## 10. Truthful README/LinkedIn summary

Use this text only after matching evidence exists. Before implementation, label Merlin planned.

> Merlin is a local-first AI second brain built from an empty repository over a 37-day learning track. It combines a notes/task core with a measured ingestion and retrieval path, then adds a bounded tool-using agent loop and MCP approval boundary. The project compares a handwritten baseline with any framework slice that receives explicit hours. Local Ollama inference keeps private seeded data on the machine by default. Evaluation reports publish the golden-set version, baseline, retrieval/task metrics, p50/p95 latency, time-to-first-token and token/cost accounting. The release lists what is built, studied and deferred; it does not claim production reliability, autonomous finance, broad model quality or framework mastery without evidence.

Claim checklist:

- Replace “combines” with “plans” until that slice passes its gate.
- Name exact model, digest, corpus revision and evaluation version.
- Report numbers with hardware and sample count.
- Say “local deployment” when AWS is not verified.
- Say “MCP server/client slice” only after protocol, scope and approval tests pass.
- Say “studied” for deferred frameworks/platforms/fine-tuning.

📚 Learn first (Must read): [Google code review guide](https://google.github.io/eng-practices/review/reviewer/), read reviewer overview; stop before linked deep dives; why: claims need reviewable evidence (~5 min).
↩ Return to build: create README/LinkedIn drafts from completed evidence only; done when every sentence maps to a test, eval, ADR, benchmark or release artifact; time box: 25 min within C-22; if stuck: replace the claim with “studied” or “planned.”

## 11. D9 acceptance and handoff

D9 is ready for Part 3 when problem/personas/use cases/non-goals, rung scope, success measures, capability boundaries, corpus and dataset records, model/hardware plan, risks and evidence-gated README claims are present.

No source is selected for redistribution by this Part. Part 4 must verify Windows/WSL2, NVIDIA driver/pass-through, disk, Docker and dependency compatibility before installation claims.

## 12. Resource index — checked 2026-10-01

| ID | Source | Status |
|---|---|---|
| P2-01 | [OWASP Threat Modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html) | verified |
| P2-02 | [Scrum Guide](https://scrumguides.org/scrum-guide.html) | verified |
| P2-03 | [OWASP LLM Prompt Injection](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) | verified |
| P2-04 | [GitHub README](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) | verified |
| P2-05 | [pytest](https://docs.pytest.org/en/stable/getting-started.html) | verified |
| P2-06 | [Python license](https://docs.python.org/3/license.html) | verified |
| P2-07 | [Kubernetes license](https://github.com/kubernetes/website/blob/main/LICENSE) | 🔎 verify exact revision/assets before import |
| P2-08 | [MDN licensing](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Attrib_copyright_license) | verified |
| P2-09 | [BANKING77 card](https://huggingface.co/datasets/PolyAI/banking77) | verified metadata; original terms still required |
| P2-10 | [BLiMP card](https://huggingface.co/datasets/nyu-mll/blimp) | 🔎 verify directly before use |
| P2-11 | [AG News candidate](https://huggingface.co/datasets/szhuggingface/ag_news) | verified card metadata; provenance/terms still required |
| P2-12 | [Hugging Face licenses](https://huggingface.co/docs/hub/main/en/repositories-licenses) | verified |
| P2-13 | [PEFT](https://huggingface.co/docs/peft/index) | verified |
| P2-14 | [Ollama FAQ](https://docs.ollama.com/faq) | verified |
| P2-15 | [Ollama embeddings](https://docs.ollama.com/capabilities/embeddings) | verified |
| P2-16 | [Qwen3 0.6B card](https://huggingface.co/Qwen/Qwen3-0.6B) | verified Apache-2.0 card |
| P2-17 | [Qwen3 1.7B card](https://huggingface.co/Qwen/Qwen3-1.7B) | verified Apache-2.0 card |
| P2-18 | [nomic card](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5) | verified Apache-2.0 card |
| P2-19 | [Ollama Qwen3 0.6B](https://ollama.com/library/qwen3:0.6b) | verified package; runtime fit unverified |
| P2-20 | [Ollama Qwen3 1.7B](https://ollama.com/library/qwen3:1.7b) | verified package; runtime fit unverified |
| P2-21 | [Ollama nomic](https://ollama.com/library/nomic-embed-text) | verified package; dimensions/runtime unverified |
| P2-22 | [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing) | verified billed pricing; grant/model eligibility unverified |
| P2-23 | [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html) | verified; alert/account behavior conditional |
| P2-24 | [Google code review](https://google.github.io/eng-practices/review/reviewer/) | verified |

All source checks were performed 2026-10-01. Context7 MCP was unavailable. Dataset cards and license pages are scouting evidence; Part 4/conditional first-use work must record exact revisions, checksums and original terms.

