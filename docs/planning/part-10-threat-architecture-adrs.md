# Part 10 — D2 Threat model, architecture and ADRs

Trust zones: browser; API; worker/agent; database/vector store; local model; optional hosted provider; MCP clients; AWS boundary. Threats: spoofing, tampering, repudiation, information disclosure, denial of service, elevation; AI injection/tool poisoning/confused deputy/data exfiltration.

Architecture: browser → API modular monolith → worker/agent loop → scoped tool registry/MCP → local Ollama or explicitly consented hosted provider; Postgres/pgvector authoritative; Redis optional; Compose local; AWS conditional. Every edge names protocol, identity and timeout.

ADR topics: scratch vs framework; Postgres vs Mongo; pgvector vs Chroma/Qdrant; FastAPI vs Spring; code vs n8n; RAG vs fine-tune vs long context; MCP vs function calling; Ollama vs hosted; SSE vs WebSocket; Context/Zustand/Redux; AWS vs local.

📚 Learn first: [OWASP Threat Modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html), read decomposition, threat identification and mitigation; stop before references (~20 min).
↩ Return to build: draw the trust-boundary diagram and STRIDE table; done when every boundary has a threat, control and test; time box: 45 min; if stuck: browser→API first.

Resource index checked 2026-10-01: OWASP Threat Modeling, Authorization, LLM Prompt Injection, PostgreSQL row security — verified.
NEXT: Part 11.

