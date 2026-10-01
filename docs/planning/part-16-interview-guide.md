# Part 16 — D5 DSA, optimization and interview guide

Optimization budget: client feedback; API/database; retrieval; model TTFT/total; storage. Measure separately with browser timing, API logs, database explain plans and model timestamps. Never claim one p95 from a mixed path.

ADR talking points: scratch vs framework; pgvector vs Chroma/Qdrant; Postgres vs Mongo; FastAPI vs Spring; code vs n8n; RAG vs fine-tune; MCP vs function calling; Ollama vs hosted; SSE vs WebSocket; Context vs global state; AWS vs local. Each answer states constraint, decision, trade-off and evidence.

Question bank structure: tokens/context/sampling/streaming/tools; cosine/chunking/HNSW/IVFFlat/hybrid; RAG failure; evals; ReAct/loops/memory/approval; MCP; framework trade-offs; fine-tuning; Pandas/NumPy; databases; Docker/Kubernetes/AWS; CI/security; system design; STAR. Generate ≥80 questions in later question-bank checklist.

📚 Learn first: [NeetCode roadmap](https://neetcode.io/roadmap), read linked lists and trees; stop after one problem; why: DSA lane needs an app-linked practice source (~20 min; 🔎 verify current page).
↩ Return to build: answer one question aloud, state complexity and one failure case; done when logged with re-quiz date; time box: 30 min; if stuck: draw the data structure.

Resource index checked 2026-10-01: NeetCode 🔎 verify; Python heapq/data structures verified; Ollama metrics verified.
NEXT: Part 17.

