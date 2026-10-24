# Part 19 — Sprint 2, Days 13–19

Goal: notes/tasks, minimal UI, ingestion, embeddings, exact vectors and hand-built RAG. Markdown + fixed CSV only; citations and refusal; golden set/baseline/recall/MRR/latency/cost. Graph BFS/DFS DSA. Day 19 review may show the full Knowledge Core is not complete; do not relabel.

## MER-11 carry-forward

MER-11 selected an internal, owner-filtered active-note list and explicitly left login, routes, fetch-by-ID, and sharing unimplemented. MVP-0 already plans basic login at Day 11 and C-05.01–C-05.04 cover authentication and owner checks, but no evidence says those tasks are built. Since Sprint 2 (Days 13–19) has passed on the fixed calendar, the protected route/detail work is carried into the current Sprint 3 plan; conditional sharing is placed in Sprint 4. These additions are plans, not completed features.

📚 Learn first: [Sprint 3 protected note routes](part-20-sprint3.md), authentication gate and owner-read cases; [Sprint 4 explicit sharing](part-21-sprint4.md), grant/revoke contract.
↩ Return: resume at the Sprint 3 auth prerequisite and protected list/detail slice; do not expose either route before trusted identity and real-role denial evidence pass.

📚 Learn first: [Ollama embeddings](https://docs.ollama.com/capabilities/embeddings), read embedding usage; stop before unrelated endpoints (~10 min).
↩ Return to build: start with one source→chunk→vector→citation path; done when owner filter and one failure case pass; time box: day net capacity; if stuck: exact search and learner-authored notes.

Resource index checked 2026-10-01: Pandas/NumPy/pgvector/RAG sources verified.
NEXT: Part 20.

