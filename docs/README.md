# Merlin documents — start here

- [Parallel SQL performance: 36.83-second full verification and coverage proof](testing/test-suite-parallel-sql-performance.md)
- [Final second review: every case/fault, repairs and observed results](testing/test-suite-second-review.md)
- [Current MER-0–MER-11 case-by-case and fault-by-fault review](testing/full-suite-case-fault-review.md) with [complete outcome matrix](testing/full-suite-case-fault-matrix.json)
Completed: [Day 9 handoff](planning/day-nine-handoff.md) and [checklist](sprints/day-nine-jira-checklist.md), tracked in [Jira MER-10](https://vipravlipare.atlassian.net/browse/MER-10). The bounded decoder, retained cases/faults, and cumulative suite are complete for the explicitly scoped parser-only outcome. Hosted run [40009971455](https://github.com/vipravlipare/Merlin/actions/runs/40009971455) passed on final revision `5032c6e14090c45a7062ea81abd6fbfecf3a48fb`; Jira is Done. HTTP transport remains deferred; no connected provider is claimed.

Learning and authorship: [decoder preparation, reviews and second-pass receipt](learning/provider-completion-preparation.md). Learner attempts and helper extraction are distinguished from explicitly authorized assistant implementation, test and harness work. Section 5.2 is recorded complete with guided corrections; independent perfect recall is not claimed.

Transport decision: [3.3 assessment](architecture/local-provider-transport-assessment.md). Assessment complete; the unbuilt network connection and its full safety requirements need a separately budgeted slice.

Verification: [application-only suite scope](testing/application-test-scope.md), [retained decoder map](testing/provider-decoder-baseline-review.md), and [integrated proof](testing/provider-decoder-suite-verification.md). All 38 decoder families mapped, 459 provider cases pass, and 34 provider faults are detected. The full local suite, fresh synthetic CI entry, and hosted cumulative run passed.

Day 10 / [Jira MER-11](https://vipravlipare.atlassian.net/browse/MER-11) is Done. Hosted cumulative CI passed on exact commit `255ec47b4fd300efde3d84701bb2ab1202559880`, [run 40107329920](https://github.com/vipravlipare/Merlin/actions/runs/40107329920). All required jobs and the final evidence merge passed. The 60-second cap measures the longest required test-execution lane; full workflow setup time is reported separately. Read the [Day 10 checklist](sprints/day-ten-jira-checklist.md) and [handoff](planning/day-ten-handoff.md) for scope limits and learner follow-ups. MASTER_PROMPT D10 is the separate Workflow Bible deliverable, not calendar Day 10.

Next: [Day 11 / Jira MER-12 catch-up checklist](sprints/day-eleven-jira-checklist.md). The planned calendar date was October 11; work resumes October 24 within the original 300-minute cap. Start by reconciling carryover, then choose one small path. Basic authentication remains unimplemented; do not expose protected notes routes or claim MVP-0 without its full acceptance evidence.

Later notes scope: basic login is already planned under Day 11/C-05 but is not verified as built. The [Sprint 3 plan](sprints/part-20-sprint3.md) carries the protected owner-scoped list/detail API into the current sprint, gated on trusted authentication and a least-privilege database role. The [Sprint 4 plan](sprints/part-21-sprint4.md) records explicit note sharing as a conditional candidate requiring a 390-minute scope swap; it is not funded or committed.

For a beginner explanation of the earlier application foundation, read [How Merlin works today](learning/current-app-setup-walkthrough.md); compare historical descriptions with the latest handoff.

📚 Learn first: [FastAPI authentication and JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), the [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), and the Day 11 checklist's stop rules. Pages checked October 24, 2026.
↩ Return: read the MER-12 checklist and record its starting SHA, one chosen outcome and actual time. The learner writes application code; CI and Jira evidence must match the exact revision being discussed.

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

Day 9 latest: [4.2–4.4 verification](testing/provider-decoder-suite-verification.md) — 34 provider faults detected; full guarded suite, fresh synthetic CI entry point, and exact hosted cumulative runs 40008698978/40009971455 PASS. MER-10 is Done for the parser-only outcome; HTTP transport remains deferred.

- [Pre-commit cumulative suite audit](testing/precommit-suite-audit.md): repaired decoder and fault-reporting gaps, complete case/fault evidence, measured reporting costs and publication limits.

- [Application-only cumulative test scope](testing/application-test-scope.md): personal quizzes excluded; implemented-work ownership map, current seven-stage verification and evidence.
