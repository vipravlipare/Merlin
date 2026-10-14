# Part 23 — D7 Jira Pack

Jira import specification: CSV chunks ≤40 rows; fields summary, issue type, parent/epic, points, sprint, labels, description, acceptance criteria and component. Stories use Gherkin and Learn/Return; Tasks map one-to-one to D12 checklist IDs; Bugs include reproduction/expected/actual; Spikes include question/stop rule/output. Current CSV columns and free-plan behavior remain 🔎 verify at import time.

Templates: planning agenda; stand-up; review script; retro; bug report; release note; pause/resume. Every item carries issue key in branch/commit/PR.

📚 Learn first: [Atlassian Jira CSV import](https://support.atlassian.com/jira-cloud-administration/docs/import-data-from-a-csv-file/), read current field requirements; stop before bulk import; why: import columns change (~10 min; 🔎 verify).
↩ Return to build: create a 40-row test import first; done when one Story, Task and Bug map correctly; time box: 30 min; if stuck: manual entry.

Resource index checked 2026-10-01: Atlassian Jira getting started/import pages 🔎 verify at current account.
NEXT: Part 24.


## Day 6 ready-to-create ticket — October 7 update

The complete [Day 6 Story, six child items and steps 1–5 checklist](../sprints/part-18-sprint1.md#jira-ready-ticket--day-6-database-foundation) are prepared in Part 18 to avoid duplicating the working checklist. October 7 live checks succeeded: Story MER-1 and Subtasks MER-2–MER-7 created in existing future MER Sprint 1 (ID 3), after exhaustive duplicate checks found no issues. All remain To Do; sprint unstarted. See [real links, readiness and exact next action](../sprints/database-foundation-start.md). These local changes must not be committed or pushed to GitHub under the learner's latest instruction.

📚 Learn first: [Atlassian team-managed subtasks](https://support.atlassian.com/jira-software-cloud/docs/manage-subtasks-in-team-managed-projects/), child tracking; stop before workflow changes. Retrieved October 7, 2026.
↩ Return: verify connected MER access and existing Sprint 1 before creating the draft; record the actual parent/child keys. Use child statuses if pasted Markdown checkboxes are not interactive. No paid plugin, import, duplicate sprint or unrelated issue is authorized.
