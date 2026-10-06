# Part 03 — D10 Workflow Bible

Status: planning only. This manual turns a Jira item into one learner-written, tested, reviewed and explainable change. It applies to Windows + WSL2, 16 GB RAM and RTX 3050 4 GB VRAM.

## 1. End-to-end workflow

Idea → Jira Epic/Story/Task → checklist item (≤90 min) → Learn + stop marker + explain-back → Return: design + test cases → branch with issue key → learner writes code/config/schema → local verify → Conventional Commit → Pull Request → CI → self-review → read-only AI review → human review when available → merge to green main → deploy/release check → evidence artifact → Jira Done + STATE/learning log.

A checklist item has one outcome. A Story may have several checklist items; its parent is not Done until all required items and evidence pass.

📚 Learn first (Must read | Deep dive): [GitHub Hello World](https://docs.github.com/en/get-started/using-github/hello-world), read branch, commit, pull request and merge; stop after merge; why: the workflow needs visible change history (~15 min).
↩ Return to build: draw this workflow in learner notes and map one future issue through it; done when every arrow names an artifact; time box: 20 min in C-01; if stuck: hint rung 1—start at one setup-only PR.

## 2. Issue lifecycle and WIP limit

WIP means work in progress. Limit active work to two checklist items: one implementation item and one learning/verification item.

| State | Entry | Exit evidence |
|---|---|---|
| Ready | Goal, scope, component, rung, estimate, dependencies, security case, performance/negative case and Learn/Return exist. | RDY-01–04 pass. |
| In Progress | Learner selects one item and creates issue-key branch. | Explain-back answered; design/test cases written. |
| In Review | Change pushed; local checks pass; PR links evidence. | CI green; self-review done; AI review comments logged. |
| Blocked | Same issue has named symptom after 25 focused minutes. | Blocker, hint rung, next experiment and time logged. |
| Done | Acceptance, security, performance, learning and documentation gates pass. | DONE-01–08; Jira links merged PR/release/evidence. |
| Deferred | Scope swap, failed dependency, unavailable account or time limit. | Reason, smallest substitute and next date recorded. |

Never leave an item In Progress overnight without a state note: last green check, next action, blocker and restart instruction.

📚 Learn first (Must read): [Jira getting started](https://support.atlassian.com/jira-software-cloud/docs/get-started-with-jira-software-cloud/), read work item and backlog overview; stop before administration; why: visible states prevent hidden work (~10 min).
↩ Return to build: configure board columns and WIP rule; done when one implementation and one learning item are visible; time box: 20 min in C-01; if stuck: use a written board until account features are confirmed.

## 3. Daily templates

Each day’s blocks must equal the Part 1 capacity row.

- Type S: use Part 17's corrected day-specific setup allocations; no feature code. DSA is learner-deferred and its slot remains uncommitted.
- Type A, 4 h: net learning/design/implementation/verification 183 min + uncommitted former DSA 15 min + ritual 30 min + reserve 12 min = 240 min. Monday additionally has a 60-minute ceremony inside the floor, reducing net work to 123 min.
- Type B, 6 h: net work 249 min + uncommitted former DSA 30 min + ritual 45 min + reserve 36 min = 360 min. Day 6 uses the concrete Part 18 split; stretch is not committed capacity.
- Type C: use the actual Part 1 row. Saturday 5 h: net 201 + uncommitted 30 + ritual 45 + reserve 24 = 300 min. Sunday 5 h: net 75 or 105 + uncommitted 30 + ritual 45 + reserve 60 + scheduled ceremony 90 or 60 = 300 min. Sunday extras are inside the floor, never added afterward.

These totals replace the earlier templates that exceeded their stated caps. Net work includes verification and setup spill; neither is an extra block. Unused reserve and deferred DSA do not automatically become feature time.

📚 Learn first (Must read): [Scrum Guide](https://scrumguides.org/scrum-guide.html), read Sprint Planning, Daily Scrum, Sprint Review and Sprint Retrospective; stop after those sections; why: ceremonies have different purposes (~20 min).
↩ Return to build: copy the matching S/A/B/C template into the daily note; done when floor, DSA, rituals, reserve and ceremony sum exactly; time box: 15 min on Day 5; if stuck: use Part 1’s capacity table.

## 4. Weekly rhythm

Monday: demo increment, compare planned/actual hours, record defects/evidence gaps, retro, re-estimate, choose continue / slow-and-cut / stop-and-polish.

Tuesday–Saturday: pull only from Ready, preserve WIP ≤2, write a short stand-up and update learning evidence.

Sunday: buffer first; run scheduled mock, re-quiz and alternating audit; do not start work that cannot reach a safe boundary before Monday.

Every day: update learner-owned STATE, LEARNING_LOG, PR/Jira links, tests/evals and “if behind” cut option. Keep private data out of demo artifacts.

📚 Learn first (Must read): [Google code review guide](https://google.github.io/eng-practices/review/reviewer/), read reviewer overview; stop before linked deep dives; why: review is a quality activity, not a merge button (~5 min).
↩ Return to build: use this script on the next Monday; done when review names evidence, retro names one change and planning preserves reserve; time box: 60 min inside ceremony; if stuck: ask what evidence changed since last Monday.

## 5. Git and pull requests

Branch name: issue key plus short verb phrase, such as MERLIN-123-add-owner-filter. Every commit and PR title carries the issue key and a Conventional Commit type.

PR body: problem/result; scope/non-scope; test-case table and commands; security/negative case; benchmark/eval fields; seeded screenshots/logs; Learn/Return proof; limitation; rollback/revert note.

Self-review order: diff → tests → secrets → ownership filters → errors/timeouts → docs → claim language. The AI reviewer is read-only; the learner changes code.

📚 Learn first (Must read): [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), read summary and specification; stop before FAQ; why: commit history becomes an evidence index (~8 min).
↩ Return to build: write branch/commit/PR naming in workflow notes; done when a setup PR follows it and links checks; time box: 15 min in C-01/C-03; if stuck: use type(scope): summary and place issue key in body.

## 6. Learning workflow

Read only the official sections needed. Stop. Answer three explain-backs. Draw the concept from memory. Design acceptance and negative cases. Implement the smallest slice personally. Verify, review and record confusion. Re-quiz 2–3 days later. Whiteboard in ten minutes.

After 25 focused minutes stuck: rung 1 concept, rung 2 approach/pseudocode, rung 3 key snippet ≤15 lines only after an attempt or explicit request. Do not retype full tutorial code unchanged.

📚 Learn first (Must read): [pytest Get Started](https://docs.pytest.org/en/stable/getting-started.html), read first test and assertions; stop before plugin guidance; why: acceptance cases need repeatable inputs (~10 min).
↩ Return to build: add one skill entry to LEARNING_LOG with date, confusion, resolution and re-quiz date; done when it links to own-code evidence; time box: 15 min in ritual; if stuck: record proof pending.

## 7. Unblock workflow

At minute 0 write expected behavior and smallest input. At minute 10 inspect first failing boundary. At minute 25 stop, log symptom and climb one hint rung. Ask with expected behavior, actual behavior, smallest reproduction, attempts and suspected boundary. After a hint, learner types and modifies the result. Human questions include the case table and one specific question. Account/tool investigation stops at its planned limit and uses the documented substitute.

📚 Learn first (Must read): [OWASP Error Handling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html), read error-handling goals; stop before language examples; why: error text must aid recovery without leaking secrets (~10 min).
↩ Return to build: create a blocker note for the first failure; done when symptom, time, hint rung and next experiment exist; time box: 5 min after threshold; if stuck: defer with evidence.

## 8. ADR and design workflow

Use Context → Options → Decision → Trade-offs → 60-second explanation → Evidence/revisit trigger. Record rejected options and the constraint. For AI/framework comparisons, hold data, golden set, prompt and hardware constant. Scratch implementation passes before framework comparison.

📚 Learn first (Must read): [ADR overview](https://adr.github.io/), read purpose and format; stop before tooling options; why: decisions need durable context (~10 min; 🔎 verify at first use).
↩ Return to build: draft an ADR before the next unplanned choice; done when one decision and one trade-off are testable; time box: 20 min in design; if stuck: list two options and preserve the core.

## 9. Change control, pause and resume

Swap-not-add: adding a feature names an equal likely-hour removal. Cut COULD, then SHOULD-3, then SHOULD-2 from the bottom. Never cut scratch LLM API, embeddings/RAG, tool loop, MCP or eval gates.

Pause at a clean checklist boundary; merge green work; write last green commit, current rung, known bug, next three actions, setup/verification instruction and data-safety note. Do not pause with private data or an unreviewed migration.

Resume by reading project STATE, planning STATE, last PR, known bugs and next three actions; run doctor/fresh-clone check; rerun smallest acceptance test; pull exactly one Ready item.

📚 Learn first (Must read): [12factor.net](https://12factor.net/), read Processes and Dev/prod parity; stop before other factors; why: restartable work needs explicit state and environment assumptions (~10 min).
↩ Return to build: write pause/resume template; done when a cold restart identifies one safe next action in 15 min; time box: 20 min in C-01/C-22; if stuck: record the last green boundary.

## 10. Templates pack

Jira Story: As a persona, I want capability, so that value. Include Gherkin happy path, security/authorization case, performance/negative case, evidence, component/checklist, rung, points, day, Learn/Return.

Checklist Task: ID; verb + one outcome; component/rung/day; Learn first; explain-back; Return; acceptance; security/negative case; evidence; time box ≤90 min; stuck/swap.

Stand-up: yesterday/result; today/one outcome; blocker; evidence; cut option; restart point.

PR: problem; scope; test table; security; benchmark/eval; screenshots/logs; ADR/docs; limitations; review; rollback.

ADR: context; options; decision; trade-offs; 60-second explanation; evidence; revisit trigger.

Runbook: purpose; prerequisites; start/stop; health; logs; failure symptoms; rollback/recovery; secrets/data warning; teardown; owner.

Retro: keep; stop; start; next experiment; scope swap; risk trigger.

Release note: tag/date; built; studied; deferred; tests/evals; limits; setup; rollback; claimable sentence.

📚 Learn first (Must read): [GitHub Actions concepts](https://docs.github.com/en/actions/get-started/understand-github-actions), read components and required checks; stop before advanced examples; why: templates must point to reproducible checks (~10 min).
↩ Return to build: copy templates into learner-owned notes during D13/P0; done when one Story, PR, ADR, runbook and release note share an issue key; time box: 30 min in C-01/C-03; if stuck: start with Story + checklist.

## 11. Worked example: owner-scoped note search

Story: As the learner, I want to search notes, so that I can find evidence without exposing another user’s notes.

Ready: C-07/C-12, MUST, Knowledge Core; owner filter, citation, security case, latency measure and ≥20-case retrieval subset planned.

Learn: read PostgreSQL row security and pgvector exact-query guidance; stop before index tuning; explain why ranking before ownership filtering is unsafe.

Return: write query/data contract and test cases before implementation.

Implement: learner writes the smallest route/service/repository slice; no framework RAG; one source ID returned.

Verify: own-user hit, no-evidence refusal, guessed-ID denial, injected-note case, p50/p95 retrieval timing, redacted logs, export/restore.

Review: self-review, read-only AI review, human review if available; record changes.

Done: tests/eval pass, evidence linked, re-quiz scheduled, PR merged, Jira updated, README claim matches.

📚 Learn first (Must read): [PostgreSQL row security](https://www.postgresql.org/docs/17/ddl-rowsecurity.html), read policy behavior; stop before examples; why: ownership must be enforced at the data boundary (~10 min).
↩ Return to build: turn this into the first vertical Story during the PRD Part; done when case table and evidence links exist before code; time box: 20 min; if stuck: hint rung 2—write the two-user case first.

## 12. Acceptance and resources

D10 passes when the learner can run from blank issue through evidence-backed Done, pause/resume in 15 minutes, and name the scope swap when a day fails. This is a specification; it creates no application files.

Resource index, checked 2026-10-01:

- [W01 Scrum Guide](https://scrumguides.org/scrum-guide.html) — verified.
- [W02 GitHub Hello World](https://docs.github.com/en/get-started/using-github/hello-world) — verified.
- [W03 Jira getting started](https://support.atlassian.com/jira-software-cloud/docs/get-started-with-jira-software-cloud/) — verified indexed text.
- [W04 Google code review guide](https://google.github.io/eng-practices/review/reviewer/) — verified.
- [W05 Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) — verified.
- [W06 pytest getting started](https://docs.pytest.org/en/stable/getting-started.html) — verified.
- [W07 OWASP Error Handling](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html) — 🔎 verify at first use.
- [W08 ADR overview](https://adr.github.io/) — 🔎 verify at first use.
- [W09 12factor Processes/Dev-prod parity](https://12factor.net/) — verified.
- [W10 GitHub Actions concepts](https://docs.github.com/en/actions/get-started/understand-github-actions) — verified.
- [W11 PostgreSQL row security](https://www.postgresql.org/docs/17/ddl-rowsecurity.html) — verified.

NEXT: Part 4 — D13 Environment Setup Guide.

