# Merlin

Merlin is a beginner learning project for building a local-first notes/tasks and AI application. **Currently implemented: development setup only.** There is no running application API, login, UI, RAG pipeline, agent, production deployment or application test suite yet.

The development environment is Ubuntu under WSL, Python 3.12 managed by uv, Node 24/pnpm 12, and Docker Compose with pinned PostgreSQL 17 and Redis 8 images. PostgreSQL is intended to hold durable relational data. Redis currently provides a disposable local smoke-test service; application caching is not implemented.

- [Setup and five-command fresh-clone path](docs/SETUP.md)
- [Terminal commands and Windows Explorer location](docs/planning/TERMINAL_COMMANDS.md)
- [Sprint 0 evidence and current limits](docs/planning/part-17-sprint0.md)
- [Sprint 1: first learner-owned backend slice](docs/planning/part-18-sprint1.md)
- [Sprint 0 engineering lessons](docs/planning/SPRINT0_LEARNING.md)
- [Interactive Sprint 0 quiz](Quizzes/sprint-0-quiz.html)

Run `uv run --locked python tools/doctor.py` to inspect your setup. The doctor does not start services, repair databases, rotate credentials or delete volumes. Required failures return a nonzero status; application tests are explicitly not applicable until application code exists.

CI validates locked setup inputs, doctor regression tests, quiet Compose configuration and isolated service checks with freshly generated synthetic credentials. It does not deploy or certify unbuilt application features. A passing run must be observed in [GitHub Actions](https://github.com/vipravlipare/Merlin/actions); no permanent green claim is made merely because a workflow exists.

Keep `.env`, private keys, recovery codes, client tools and database dumps out of Git. Use synthetic data only; this local setup is not production security hardening. Optional AWS, models, pgvector and extra application frameworks remain deferred until funded first use. Global Codex/OmniRoute tooling is optional and is not a dependency of Merlin startup.

Authorship: the assistant prepared setup automation and documentation at the learner's explicit request. The learner owns application implementation and must provide their own learning evidence. No project-wide software license is established by the npm metadata; third-party skill licenses and provenance remain with their bundled sources.
