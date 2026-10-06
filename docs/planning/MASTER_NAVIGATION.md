# Merlin Master Navigation Guide

This guide is the working map for the project. Repo rules require planning files under `docs/planning/`; this is the closest allowed location to a repo-level master guide.

## Current working location

Use **VS Code connected to `WSL: Ubuntu`**. Open `/home/vipra/Merlin`. Run Linux commands in the VS Code WSL terminal. Keep the repository in the Linux filesystem. Do not use `C:\Users\vipra\Merlin` as the active implementation checkout.

Current environment already verified:

- WSL2 Ubuntu, Windows 11, i7-12700H, 15.69 GiB host RAM, RTX 3050 4 GiB.
- `uv 0.12.21`, Python 3.12.14, Node 24.21.0 LTS, pnpm 12.8.1.
- Docker Engine 29.7.2, Linux `amd64`, Compose v5.4.0.
- VS Code WSL extension, VS Code Server, Python, Pylance, and debugger extensions.

## Windows access to this same checkout

Open `\\wsl$\Ubuntu\home\vipra\Merlin` in Windows Explorer; use VS Code WSL for development. Follow [single-checkout steps](part-04-environment-setup.md). This exposes the Ubuntu files directly; the old `C:\Users\vipra\Merlin` copy remains stale and should not receive active edits. No automatic sync is needed or configured.

## Read order for every work session

1. Read `AGENTS.md`.
2. Read `docs/planning/STATE.md`.
3. Read this file.
4. Open the current day in the matching sprint file.
5. Open the checklist IDs named by that day.
6. Follow `LEARN → explain-back → RETURN → implement → verify → evidence`.
7. Update learner-owned state, learning log, Jira, branch, PR, and evidence.

## October 2 operational handoff

Sprint 0 Days 1–3 operational setup passes. Use the Windows desktop **Merlin Ubuntu** shortcut, or open `/home/vipra/Merlin` in VS Code WSL. Windows share access to `\\wsl$\Ubuntu\home\vipra\Merlin` was verified. Old C: files remain historical; do not edit them or sync them over the active checkout.

## Immediate work queue

### A. Section 8 — operationally complete

Read [final Day 3 evidence](part-04-environment-setup.md). October 6: corrected services postgres/redis are running and healthy; images are digest-pinned; secret boundary, host/container positive/negative auth, PING, non-root processes, resource/logging policies and storage retention pass. PostgreSQL volume and cluster identity are preserved. Do not rerun the transition without a concrete reason. Part 04 contains the reproduction steps.

### B. Accounts and next-day boundary

Atlassian MER access/email/MFA/sign-in/Free plan/Scrum/recovery status are learner-confirmed; AWS remains deferred. GitHub web MFA/visibility and team-managed type remain separately unverified; no personal account setting was changed by the mentor. DSA is learner-deferred. Actual minutes, mastery/re-quiz and whiteboard remain unreported. Requested Day 4 documentation and doctor/CI specifications are delivered in [Part 17](part-17-sprint0.md). Learner learning/time and fresh-clone execution remain open; no workflow/script implementation is claimed.

### C. Keep Section 9 deferred

Read the optional-tools table in `part-04-environment-setup.md`. Do not install Ollama, models, MongoDB, Java, kind, kubectl, n8n, Chroma/Qdrant, Hugging Face, Colab/Kaggle, Playwright, or k6 until the scheduled day and gate.

## Planning documents: what exists and what it means

All numbered Part files 1–25 exist. They are the planning source, not proof that implementation is complete.

| Need | Read first | Status |
|---|---|---|
| Reality check and stack | Part 1 | Exists; hour ledger and cut line defined |
| Project charter | Part 2 | Exists; verify licenses and model choices before use |
| Workflow | Part 3 | Exists; use as daily operating procedure |
| Environment | Part 4 | Section 8 operationally passes; later environment gates pending |
| Components | Part 5 | Exists; source for implementation boundaries |
| Checklists | Parts 6–7 | Exists; source for Jira tasks |
| PRD/Epics | Parts 8–9 | Exists as compact specifications; full story detail still needs expansion before Jira import |
| Architecture/database | Parts 10–11 | Exists as compact specifications; use before schema/API implementation |
| SDLC playbook | Parts 12–13 | Exists as compact specifications |
| Skill cards/DSA | Parts 14–15 | Exists as compact specifications |
| Interview guide | Part 16 | Exists as compact specification |
| Daily schedule | Parts 17–22 | Exists; follow current sprint/day |
| Jira pack | Part 23 | Exists as compact specification; do not import until account/space is ready |
| Readiness audit | Part 24 | Exists; run at rung checkpoints |
| Portfolio pack | Part 25 | Exists; use only after evidence exists |

## PRD answer

A PRD is already present in Parts 8–9. It covers vision, epics E0–E10, priorities, velocity assumptions, risks, and cut order. It is **not yet a complete Jira-ready PRD** under the full MASTER_PROMPT requirement: individual stories need full Gherkin security/performance cases, points, days, checklist IDs, evidence, Learn/Return blocks, backend test tables, and hint ladders. Expand stories only when implementation reaches that component; do not block Section 8 on rewriting the whole PRD.

After Day 4/5 setup gates, story expansion starts with E0/E1 and Day 6 checklist IDs. Keep scope swap-not-add.

## Daily navigation

For each day, use this order:

1. Sprint file: `part-17-sprint0.md` for Days 1–5, then `part-18` through `part-22`.
2. Part 5 component entry for the component.
3. Part 6 or 7 checklist item.
4. Relevant skill card in Part 14 or 15.
5. Relevant architecture section in Parts 10 or 11.
6. Relevant PRD story in Parts 8 or 9.
7. Write code/config/tests yourself.
8. Run named verification and security checks.
9. Commit, PR, read-only review, merge, evidence, Jira Done.

## Stop conditions

Stop and record a blocker when: a secret would enter Git; a service would bind publicly; a task exceeds its time box; a framework is introduced before the scratch version passes; an AI claim lacks golden set, baseline, metric, latency, and cost; or remaining hours require adding scope instead of swapping scope.

## What counts as complete

Section 8 is complete only after S8-01 through S8-05 pass with dated sanitized evidence. Part 4 is complete only after Sections 1–9 gates are either passed or honestly marked deferred with an owner and next action. The project is not built because planning documents exist; implementation evidence must come from learner-authored code, configuration, tests, PRs, benchmarks, and releases.

Historical Day 4 update: retention passed and services were stopped. Setup inputs were later committed and an isolated adapted clone passed. October 6 services are running; public unmodified reproduction, doctor/CI and learner ritual evidence remain open. Continue at STATE NEXT.

Sprint 0 audit: [Part 17 S0-CLOSE](part-17-sprint0.md#s0-close--concrete-route-to-full-completion) defines remaining implementation/clone/personal gates. Section 8 passes; full-S0 NO-GO until reproduction/CI proof exists. Day 5 audit is delivered, learner ritual evidence pending.

## Start coding — October 6

📚 Learn first: [current environment audit](part-04-environment-setup.md#current-coding-readiness-audit--october-6-2026), current versus historical evidence; stop before optional installers.
↩ Return: open [Day 6](part-18-sprint1.md#day-6--tuesday-october-6--first-database-foundation), then C-04.01/.02 in Part 6. Local foundations are ready; dependency compatibility and isolated migration prerequisites must pass before C-04.03. The first users/notes slice is not an instruction to build every backend component today.
