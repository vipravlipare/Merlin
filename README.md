# Merlin

Merlin is a beginner learning project for building a local-first notes/tasks and AI application. **Currently implemented: local development setup, the users/notes database foundation, input rules, disposable maintenance and the test/fault suite.** There is no application HTTP API, login, UI, RAG pipeline, agent or production deployment yet. Day 7's health endpoint is designed but not implemented.

The development environment is Ubuntu under WSL, Python 3.12 managed by uv, Node 24/pnpm 12, and Docker Compose with pinned PostgreSQL 17 and Redis 8 images. PostgreSQL is intended to hold durable relational data. Redis currently provides a disposable local smoke-test service; application caching is not implemented.

- [Setup and five-command fresh-clone path](docs/setup/local-setup.md)
- [Terminal commands and Windows Explorer location](docs/setup/terminal-commands.md)
- [Sprint 0 evidence and current limits](docs/sprints/part-17-sprint0.md)
- [Sprint 1: first learner-owned backend slice](docs/sprints/part-18-sprint1.md)
- [Sprint 0 engineering lessons](docs/learning/sprint-0-learning.md)
- [Interactive Sprint 0 quiz](quizzes/sprint-0-quiz.html)
- [Current application walkthrough](docs/learning/current-app-setup-walkthrough.md)
- [Complete test and fault-suite commands](docs/testing/test-suite-commands.md)
- [Day 7 health API contract](docs/architecture/health-api-contract.md)

Run `uv run --locked python tools/doctor.py` to inspect your setup. The doctor does not start services, repair databases, rotate credentials or delete volumes. Required failures return a nonzero status. It does not execute the application test/fault suite; use `.venv/bin/python tools/run_test_suite.py` for the complete suite after its documented prerequisites are ready.

CI is configured to validate locked setup inputs, doctor regressions, isolated service checks, the complete application/fault suite and committed disposable migration roundtrips. See the [cumulative CI gate](docs/delivery/cumulative-ci-gate.md) and [local verification](docs/testing/cumulative-ci-verification.md). It does not deploy or certify unbuilt application features. A passing run must be observed in [GitHub Actions](https://github.com/vipravlipare/Merlin/actions); no permanent green claim is made merely because a workflow exists.

Keep `.env`, private keys, recovery codes, client tools and database dumps out of Git. Use synthetic data only; this local setup is not production security hardening. Optional AWS, models, pgvector and extra application frameworks remain deferred until funded first use. Global Codex/OmniRoute tooling is optional and is not a dependency of Merlin startup.

Authorship: the assistant prepared setup automation and documentation at the learner's explicit request. The learner owns application implementation and must provide their own learning evidence. No project-wide software license is established by the npm metadata; third-party skill licenses and provenance remain with their bundled sources.
