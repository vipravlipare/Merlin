# STATE.md — handoff capsule

Timeline: 37 days, Thu Oct 1–Fri Nov 6, 2026. S0 chill Days 1–5 (10 h); S1–S4 Tue→Mon (34 h each); S5 Days 34–37 (20 h). Original rung checkpoints: MVP-0 Day 11, MVP-1 Day 19, MVP-2 Day 26, MVP-3 Day 33, v1.0 Day 37. Part 1 revises honest targets: Knowledge Core about Day 26; Agentic Core about Day 33; framework rung is unfunded unless swapped.

Decisions:
- Stack: Python/FastAPI modular monolith; PostgreSQL + pgvector; React/TypeScript; Ollama local-first; Docker Compose; MCP after scratch tools/agent loop.
- Cloud: AWS optional and conditional; local release is default $0 path. Budget alerts are not hard caps.
- ADR-01 one Python app; ADR-02 Postgres/vector-first; ADR-03 local provider boundary; ADR-04 lean React + SSE; ADR-05 local-first/AWS conditional; ADR-06 scratch before frameworks.
- Cut line: after protected scratch core/rung 2, before framework/platform breadth. C-16–C-19 and C-24 have zero funded hours; optional work is swap-not-add.
- Security/evals: auth, owner filters, injection defenses, redaction/consent, golden sets and regression checks stay core.

ID registry:
- Components C-01–C-24; skills SK-01–SK-22.
- Epics E0–E10 reserved; story pattern E2-US04; checklist pattern C-07.3.
- ADR-01–ADR-06 delivered; ADR-07–ADR-12 reserved conditional.
- RDY-01–RDY-04 and DONE-01–DONE-08 defined.
- Part 1 has no Jira stories/tasks issued.

Consistency numbers:
- Floor 166.00 h; exact 10% reserve 16.60; committed ceiling 149.40.
- DSA 13.75; rituals 21.75; ceremonies 9.00; net Learn + Implement 104.90.
- Planned split: Learn 42.00; Implement/setup/tests/docs/evidence 62.90.
- Points prior: 1 point ≈ 1.5 beginner net hours; ~69.9 point-equivalents.
- Sprint net: S0 7.50; S1 21.05; S2 21.55; S3 21.05; S4 21.55; S5 12.20.
- Component likely ledger total 104.90; low 72.50; high 173.50.

Rule Card: R1 Learn→Return everywhere; R2 official links only, verify uncertain URLs; R3 learner owns feature code; latest request permits assistant setup edits; R4 explain-back, acceptance test, whiteboard, re-quiz; R5 honest hours and swap-not-add; R6 security in stories; R7 public-source parity/ADRs; R8 Jira-native ≤90-min tasks; R9 stop-anywhere; R10 terse chat; R11 files truth + STATE; R12 scratch before frameworks; R13 ≥20-case golden set, baseline, metric, latency and cost for AI.

Open questions / verify:
- Q-01 OS/RAM/GPU resolved: Windows, 16 GB RAM, RTX 3050 4 GB VRAM. Disk space, NVIDIA driver, WSL GPU pass-through and admin rights remain open.
- Q-02 AWS/account/card/credit eligibility, hosted API grant, repo visibility.
- Q-03 corpus/dataset licenses and model/package digests.
- VFY-01 dependency compatibility, uv binary, lockfiles, image/action/model digests.
- VFY-02 MCP/framework APIs and changelogs before every framework session.
- VFY-03 model quality/memory/latency; VFY-04 AES-256/TLS 1.3 coverage.
- VFY-05 Kaggle quota/verification; VFY-06 Jira/GitHub account limits.
- VFY-07 cloud topology and live eval gate; VFY-08 deferred installers/APIs.
- Context7 unavailable. Relevant Docker/Postgres/Redis/Atlassian/AWS docs opened 2026-10-02; account-specific eligibility unverified; target image manifests verified October 2.

Last Part: October 3: learner reports MCQ result 34/35; critical miss/explain-back unknown. Quizzes/sprint-0-quiz.html now includes separate System Design reading: tool rationales, Ubuntu/native Windows, storage models/layers, caching, Redis/PostgreSQL, volumes and loopback. Official source links verified. Existing 35 questions/JavaScript/storage key unchanged; quiz harness checks pass. No additional questions or live-runtime changes.
NEXT: Learner reloads quiz and opens System Design; practice reason plus trade-off and share missed concept if desired. Publish reading/evidence on setup branch. MCQ result remains learner-reported, not full mastery. Full Sprint 0 still lacks implemented doctor/CI/green run and documented unmodified setup reproduction; DSA/AWS deferred. Preserve cluster 7691749973399031842; no gateway configuration.

Delivery: planning plus explicitly authorized setup-only Compose/ignore/client/shortcut changes; no application features.

Resources: Parts 1–25 retain resource indexes. October 2 Docker/Postgres/Redis/Atlassian/AWS documentation access verified; Context7 unavailable. Host authentication, storage recreation and target pins pass. Account eligibility, optional licenses and remaining hardware/security facts require verification. See consolidated dated evidence.
