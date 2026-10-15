# Merlin documents — start here

- [Parallel SQL performance: 36.83-second full verification and coverage proof](testing/test-suite-parallel-sql-performance.md)
- [Final second review: every case/fault, repairs and observed results](testing/test-suite-second-review.md)
Current work: [cumulative CI repair and hosted verification](testing/cumulative-ci-verification.md), then the [Day 7 health API contract and learning guide](architecture/health-api-contract.md), step 2.1 of the [Day 7 Jira checklist](sprints/day-seven-jira-checklist.md). Section 1 is learner-confirmed complete. Previous evidence: [Day 6 handoff](planning/day-six-handoff.md) and [test-suite necessity review](testing/test-suite-necessity-review.md).

For a beginner explanation of the current implementation, read [How Merlin works today](learning/current-app-setup-walkthrough.md).

For today’s work, open the [health API contract](architecture/health-api-contract.md). Track Day 7 in [Jira MER-8](https://vipravlipare.atlassian.net/browse/MER-8).

📚 Learn first: the Day 7 contract guide, request/response table and linked Python HTTP documentation.
↩ Return: review the contract and answer its three explain-back questions; then design the negative cases before writing server code.

| Folder | What belongs here |
|---|---|
| `sprints/` | Sprint 0–5 agendas/evidence (Parts 17–22) and Day 6 start/checklist guides |
| `setup/` | Environment setup (Part 4), terminal commands and troubleshooting |
| `learning/` | Sprint 0 learning, skill cards and interview study (Parts 14–16) |
| `project/` | Capacity, charter, workflow, components and requirements (Parts 1–3, 5, 8–9) |
| `architecture/` | Threat model, architecture, database and AI design (Parts 10–11), plus your own design notes |
| `checklists/` | Implementation checklists (Parts 6–7) |
| `delivery/` | SDLC, Jira, readiness and portfolio plans (Parts 12–13, 23–25) |
| `testing/` | Test audits, fault catalogues and current verification results |
| `planning/` | Session handoff, master instructions, navigation and verification register |

[Terminal commands](setup/terminal-commands.md) · [Sprint 0 learning](learning/sprint-0-learning.md) · [Published setup instructions](setup/local-setup.md) · [Session handoff](planning/STATE.md) · [Full navigation](planning/MASTER_NAVIGATION.md)

Numbered Parts retain their names and content. No application code or runtime configuration was changed. Quizzes remain in the root `quizzes/` folder. Documentation moves remain local; nothing is committed or pushed.

## Open from Ubuntu

```bash
code /home/vipra/Merlin/docs/README.md
code /home/vipra/Merlin/docs/sprints/database-foundation-start.md
```

Press **Ctrl+Shift+V** in VS Code to open Markdown preview. In Windows Explorer, open `\\wsl.localhost\Ubuntu\home\vipra\Merlin\docs`.

## Where to write your Day 6 work

Create your own `docs/architecture/users-notes-design.md` in VS Code. Put your users/notes field tables, design decisions and expected test results there. This file is intentionally not written for you.

Keep learning explanations in `docs/learning/`, daily progress and observed results in `docs/sprints/`, and environment instructions in `docs/setup/`. Keep `docs/planning/` for session control documents. Use this index to find documents by purpose.

📚 Learn first: [Part 11 candidate design](architecture/part-11-schema-ai-architecture.md); read only the users/notes slice.
↩ Return: create your design note, add the Users heading and columns Field, Type, Required?, Rules and Reason; explain why an ID should remain stable when an email changes. No SQL or database changes yet.

Current test evidence: [individual case effectiveness audit](testing/case-effectiveness-audit.md). Earlier results remain linked from that report.

File naming: [complete inventory and rename review](planning/file-naming-review.md).

Jira completion: [MER-1 checklist audit](testing/mer-1-completion-audit.md).

Current MER-1 step 4: [database verification results and migration undo requirements](testing/database-step-four-verification.md).

Migration 001 undo: [scaffold fill-in guide](learning/users-notes-down-migration-guide.md).

Run all tests and injected faults: [test-suite terminal commands](testing/test-suite-commands.md).

Test-suite repair and speed: [failure investigation and measured performance](testing/test-suite-performance.md).
