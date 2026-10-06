# Part 18 — Sprint 1, Days 6–12

Goal: learner-owned database/API foundation, followed by the local provider boundary and green checks when their gates pass. A walking skeleton is a thin working path across required boundaries; it is not complete because those boundaries have planning files. October 6 audit confirms local Python/PostgreSQL/Redis readiness, not installed feature dependencies or a running API.

## Day 6 — Tuesday October 6 — First database foundation

Budget: **360 minutes floor**. Net work 249 + former DSA uncommitted 30 + rituals 45 + reserve 36 = 360. No stretch committed; actual learner minutes unknown. Local checklist IDs are not issued Jira keys. At most two active outcomes. The original broad database/auth/API/CI/provider forecast is narrowed; no promise to finish all of it today.

📚 Learn first: [current setup audit](part-04-environment-setup.md#current-coding-readiness-audit--october-6-2026), actual checks; [C-04 entry tasks](part-06-checklists-first-half.md#day-6-expanded-entry-tasks--october-6), prerequisite gates; stop before optional models/frameworks.
↩ Return: start C-04.01 then the first users/notes portion of C-04.02. Conditional C-04.03 is the first learner coding attempt, after dependency/isolation checks. Stop at the cap and record the next failed gate. CI/public reproduction remains a completion gap, not a reason to postpone all database learning.

| Block | Minutes | Outcome / stop boundary |
|---|---:|---|
| Existing setup spill / closure | 45 | Review remaining README/SETUP/doctor/CI gates against Part 17. Learner chooses one closure outcome; unfinished work displaces equal feature minutes, not extra hours. Record time. |
| C-04.01 learn/explain-back | 45 | Transaction rollback, server-derived ownership, privileged-role exceptions. |
| C-04.02 first slice design | 60 | Two 30-minute steps: adapt users/notes fields and constraints, then write acceptance/rollback/ownership cases. No all-table rewrite. |
| C-04.03 conditional coding | 60 | Dependency/isolation gate, 15 minutes; learner migration/connectivity attempt, 45 minutes. If prerequisites fail, stop before database changes; unfinished dependency work displaces coding. |
| Verify / record first failure | 39 | Run only cases for implemented work, record expected/observed results and redacted errors. Missing code is pending, never a passing test. |
| Uncommitted former DSA slot | 30 | Learner deferred; no automatic reassignment or mastery claim. |
| Rituals | 45 | Stand-up, actual ledger, diff/secret review, explain-back/restart point. Review existing quiz's missed concept if known. |
| Reserve | 36 | Unexpected committed-scope work only; unused minutes do not fund new scope. |
| **Total** | **360** | Net work is 249 minutes, including setup spill and verification. |

### Implementation entry and acceptance gates

📚 Learn first: [uv locked execution](https://docs.astral.sh/uv/concepts/projects/sync/), avoiding silent lock changes; [PostgreSQL transactions](https://www.postgresql.org/docs/17/tutorial-transactions.html), commit/rollback; stop before advanced examples. These pages and PostgreSQL row-security documentation were retrieved October 6, 2026.
↩ Return: verify the interpreter and quiet Compose configuration, then use the Part 11 case table in isolated synthetic storage. Done means personally written code and observed outcomes, not copied examples or assistant infrastructure checks. The 60-minute implementation block includes dependency selection/installation.

Gate 1: preserve Ubuntu `.venv` Python 3.12.14 and working image pins. Gate 2: first-use driver/migration/test packages must resolve together and pass a locked install/import check; current dependencies are empty. FastAPI/SQLAlchemy are introduced only when the selected slice needs them, not installed merely to fill a stack checklist. Gate 3: isolated test storage and synthetic identities must not share the retained setup volume. Gate 4: constraints, transaction rollback and ownership tests must pass before the migration/security item is Done. Gate 5: protected API work needs identity and a limited application database role; an administrative setup credential is not a safe deployed authorization boundary.

Safe startup checks in the existing checkout:

```bash
cd /home/vipra/Merlin
uv run --locked --offline python --version
docker compose config --quiet
docker compose ps
```

No feature code, SQL/DDL, workflow or doctor script is supplied here. Scratch reasoning and small explicit database operations come before ORM abstractions; compare the choices in an ADR when the abstraction is introduced. AI, pgvector, UI, AWS and implemented Redis caching are outside this first slice. Services currently remain running for coding; safely stop afterward with `docker compose stop --timeout 30 postgres redis`.

### Days 7–12 — Reforecast at actual progress

📚 Learn first: [Part 1 capacity and spill rules](part-01-waterfall-and-assumptions.md), daily floor and reserve; stop before optional scope.
↩ Return: use the Day 6 ledger to choose the next unchecked outcome. CI's requested latest deadline is Day 7; if unfinished, record a blocker and displace feature time. Day 8 Ollama is conditional on hardware/funded first-use gates, not automatic. Day 12 reviews actual evidence and scope. Expand each next day before execution; do not claim an executable full-sprint schedule from this outline. MVP-0 is conditional on its actual definition passing.

Resources: current official transaction/row-security/uv pages retrieved October 6; previous broader resource indexes are historical. Dependency API/version compatibility remains first-use verification. No new Context7 verification is claimed.
NEXT: learner C-04.01/.02, then conditional C-04.03; update actual minutes and reforecast Day 7.
