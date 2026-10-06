# STATE.md — handoff capsule

Timeline: Oct 1–Nov 6, 2026, 37 days. S0 10 h; S1–S4 34 h each; S5 20 h. Part 1 honest targets: Knowledge Core around Day 26, Agentic Core Day 33; frameworks unfunded unless swapped.

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
- Q-01 Windows, 16 GB RAM, RTX 3050 4 GB; remaining host hardware facts unverified.
- Q-02 AWS/account/card/credit eligibility, hosted API grant, repo visibility.
- Q-03 corpus/dataset licenses and model/package digests.
- VFY-01 dependency compatibility, uv binary, lockfiles, image/action/model digests.
- VFY-02 MCP/framework APIs and changelogs before every framework session.
- VFY-03 model quality/memory/latency; VFY-04 AES-256/TLS 1.3 coverage.
- VFY-05 Kaggle quota/verification; VFY-06 Jira/GitHub account limits.
- VFY-07 cloud topology and live eval gate; VFY-08 deferred installers/APIs.
- Context7 unavailable. Relevant Docker/Postgres/Redis/Atlassian/AWS docs opened 2026-10-02; account-specific eligibility unverified; target image manifests verified October 2.

Last Part: October 6 infrastructure audit passes Python 3.12.14 and healthy PostgreSQL/Redis, host/container positive-negative authentication, loopback, resources/logs, UID999 and retained cluster. Planning budgets/dependencies corrected; Day6/users-notes contract supplied. Global Caveman/46 OmniRoute skills installed in Ubuntu/Windows; defaults loaded. OmniRoute3.8.51 user service enabled/healthy/localhost-only; stacked compression saved. Nine providers listed; DuckDuckGo chat/streaming pass, forced tool call absent. OpenAI credential check passes; OpenCode external free tier blocked; Cloudflare browser absent. Codex routing/savings unproved. ChatGPT plugin absent; personalization manual. Part17 has activation steps.
NEXT: Merlin Part18 Day6 C-04.01/.02 now; C-04.03 requires compatible locked packages and isolated synthetic storage. Day6 cap360: net249/uncommittedDSA30/ritual45/reserve36; setup spill replaces feature time, CI deadlineDay7. FullS0 doctor/CI/public reproduction and learner facts remain open; latest audit edits uncommitted. Existing runtime proofs retained; both services healthy. New session: codex -C /home/vipra/Merlin. Caveman global defaults installed; both Ubuntu/Windows Codex providers remain default, not OmniRoute. Gateway integration optional: persistent client key/tool-compatible model needed before switching. Adapted isolated clone passed; preserve cluster7691749973399031842. Quiz34/35 learner-reported; minutes/mastery unknown; AWS/DSA deferred.

Delivery: planning plus explicitly authorized setup-only Compose/ignore/client/shortcut changes; no application features.

Resources: October 6 transaction/row-security/uv docs retrieved; package compatibility remains first-use verification. Account eligibility and personal learning facts remain unverified.
