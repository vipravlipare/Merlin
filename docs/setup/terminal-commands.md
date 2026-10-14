# Terminal commands — what to use now

**Use the Ubuntu terminal in VS Code.** The editor should show `WSL: Ubuntu`. Run commands one at a time; stop at the first error. Do not copy the terminal prompt.

For Day 6 you need only **sections 1–3**. Section 4 is optional; section 5 is troubleshooting. You do not need to repeat setup, add dependencies again or start Redis for this database slice.

## 1. Start a database-work session — necessary

| Where / when | Command | Small reason |
|---|---|---|
| Ubuntu terminal, when opening a session | `cd /home/vipra/Merlin` | Select the project folder. Skip if already there. |
| Same terminal, before database work | `docker compose -p merlin-d6-20261008105707 ps` | Check the existing test database. Look for `healthy` and port `55432`. |

If PostgreSQL is healthy, continue. If the existing container is stopped, use:

```bash
docker compose -p merlin-d6-20261008105707 start postgres
```

Then run the `ps` command again until healthy. **Use `start` only when stopped.** If no test container exists, stop and ask for help; do not recreate it using guessed settings.

The `-p merlin-d6-20261008105707` part selects your disposable test project. Keep it in database service commands; otherwise you could select the original Sprint 0 project.

📚 Learn first: [Day 6 target guide](../sprints/database-foundation-start.md), current target evidence.
↩ Return: continue only when the named test container is healthy. This is not a migration or feature test.

## 2. Open PostgreSQL — necessary only for manual database work

Run in the **Ubuntu terminal**, after section 1:

```bash
psql -X -W -h 127.0.0.1 -p 55432 -U merlin_d6 -d merlin_d6 -P pager=off
```

**Reason:** open your test database, with a private password prompt. Enter the test password you created, never the original database password.

| Part | Meaning |
|---|---|
| `-X` | Ignore personal psql startup settings. |
| `-W` | Ask for your password; do not include it in a command. |
| `-h 127.0.0.1 -p 55432` | Connect to the local test port. |
| `-U merlin_d6 -d merlin_d6` | Choose the test role and database. |
| `-P pager=off` | Keep results out of the scrolling pager. |

Your prompt changes to a **psql prompt**. Ubuntu commands such as `docker`, `uv` and `git` do not belong there. To return to Ubuntu, type:

```text
\q
```

To check connectivity without entering an interactive session, append `-l` to the connection command. That lists databases and exits. You already passed this check; do not repeat it every time. If a pager opens elsewhere, press `q` to leave the pager.

📚 Learn first: [PostgreSQL psql reference](https://www.postgresql.org/docs/17/app-psql.html), connection options and interactive commands; previously retrieved October 7.
↩ Return: connect only to port `55432` and database `merlin_d6`. Connectivity does not prove ownership security; this role is administrative.

## 3. Finish the session — optional stop, necessary review

Run in the **Ubuntu terminal**, after exiting psql:

| When | Command | Small reason |
|---|---|---|
| Before recording your handoff | `git status --short` | See changed/new files. |
| After editing tracked files | `git diff --stat` | See which tracked files changed and how much. |
| Review tracked edits privately | `git diff` | Read actual changes; check for secrets. New untracked files must be opened separately. |
| Want to stop the test database | `docker compose -p merlin-d6-20261008105707 stop --timeout 30 postgres` | Stop it while keeping its data. Leaving it running is also allowed. |

Do not paste secrets from a diff. Record results and actual minutes, or “unknown.” **Do not commit, push or upload anything to GitHub.**

📚 Learn first: [Day 6 checklist](../sprints/database-foundation-jira-guide.md), handoff and secret review.
↩ Return: leave an exact next action. Review and a running database do not mean your feature is complete.

## 4. Other commands — only when needed

All commands below run in **Ubuntu**, from `/home/vipra/Merlin`.

| When to use | Command | Small reason |
|---|---|---|
| Dependencies/lockfile changed, or environment missing | `uv sync --locked` | Install exactly the locked dependencies. Not needed after every code edit. |
| Suspect wrong package versions | `uv pip show psycopg psycopg-binary pytest` | Inspect installed package metadata; not an import test. |
| Need to confirm test port | `docker compose -p merlin-d6-20261008105707 port postgres 5432` | Should show `127.0.0.1:55432`. |
| Open the checkout in VS Code | `code /home/vipra/Merlin` | Open the Ubuntu project. Skip if already open. |
| Start a new Codex CLI session | `codex -C /home/vipra/Merlin` | Start an assistant in this checkout. Not required for coding. |
| Resume the last Codex CLI session | `codex resume --last` | Continue that session instead of creating a new one. |
| Check whitespace errors in edits | `git diff --check` | Report formatting problems; not a feature test. |
| Verify environment file is ignored | `git check-ignore .env` | Expected output: `.env`. |
| Verify environment file is not tracked | `git ls-files .env` | Expected: no output. |

Installed versions evidenced October 8: Psycopg and binary adapter **3.3.6**, pytest **9.1.1**. Do not repeat `uv add` unless intentionally changing dependencies. No application start command or authored feature-test command has been verified yet.

📚 Learn first: [uv dependency syncing](https://docs.astral.sh/uv/concepts/projects/sync/), locked sync; previously retrieved October 7.
↩ Return: use a command only for its stated need; record the first failure instead of reinstalling everything.

## 5. Troubleshooting and one-time checks — not daily work

### If you are in Windows PowerShell

A prompt beginning `PS C:\…>` is Windows, not Ubuntu. Run this **in PowerShell**:

```powershell
wsl -d Ubuntu -u vipra --cd /home/vipra/Merlin
```

Then use the Ubuntu commands above. If Ubuntu is not found, run `wsl --list --verbose` in PowerShell and check the distribution name. Do not run Linux paths through Windows Codex.

For Windows File Explorer, paste this in its address bar:

```text
\\wsl.localhost\Ubuntu\home\vipra\Merlin
```

These are the Ubuntu files directly. Do not work in the stale `C:\Users\vipra\Merlin` copy. Preview this Markdown file in VS Code with **Ctrl+Shift+V**.

📚 Learn first: [Microsoft WSL commands](https://learn.microsoft.com/en-us/windows/wsl/basic-commands), entering a distribution; previously retrieved October 7.
↩ Return: verify the terminal is Ubuntu and the checkout is `/home/vipra/Merlin`.

### If Codex reports incompatible background-server features

Choose **Run without daemon this time**, or run in Ubuntu:

```bash
codex --no-daemon -C /home/vipra/Merlin
```

This was checked against local CLI help October 7. No provider/settings change is needed. CLI installation alone does not prove Jira connectivity.

### If the database target appears wrong

Run in Ubuntu, from the checkout; these read names and metadata only:

| Check | Command |
|---|---|
| Mounted volume | `docker inspect "$(docker compose -p merlin-d6-20261008105707 ps -q postgres)" --format '{{range .Mounts}}{{println .Name .Destination}}{{end}}'` |
| Network | `docker network inspect merlin-d6-20261008105707-network --format '{{.Name}}'` |

For cluster identity:

```bash
docker compose -p merlin-d6-20261008105707 exec -T postgres pg_controldata /var/lib/postgresql/data | grep 'Database system identifier'
```

This reads the cluster's identifier. Ripgrep is not needed.

| Verified test target, October 8 | Value |
|---|---|
| Project | `merlin-d6-20261008105707` |
| Volume | `merlin-d6-20261008105707_postgres_data` |
| Network | `merlin-d6-20261008105707-network` |
| Cluster | `7694311451826794534` |
| Host / port / database / role | `127.0.0.1` / `55432` / `merlin_d6` / `merlin_d6` |

**Preserve Sprint 0:** never migrate, reset or delete volume `merlin_postgres_data` or cluster `7691749973399031842`. Do not print full resolved Compose settings or container environments; they can contain passwords.

The `ss` port check, initial `export`/password input and `up --wait` were one-time creation steps. Repeating timestamp-based creation makes more test projects. Terminal overrides disappear when the terminal closes; commands above select the existing project explicitly and do not recreate it.

📚 Learn first: [Isolation creation guide](../sprints/database-foundation-start.md#isolated-storage-gate-learner-commands-not-executed), only if recreating a proven disposable target is actually necessary.
↩ Return: stop on any mismatch. Use existing storage; do not reset a database to fix connection errors.

## Reference documents — open only for the relevant task

- [Setup/reproduction](local-setup.md): new-machine or fresh-clone setup; completed setup need not be repeated.
- [Day 6 start guide](../sprints/database-foundation-start.md): prerequisite and migration gates. The reviewed learner design supersedes its historical starter schema examples.
- [Your design](../architecture/users-notes-design.md): current Users/Notes requirements.
- [Day 6 checklist](../sprints/database-foundation-jira-guide.md) and [MER-1](https://vipravlipare.atlassian.net/browse/MER-1): track evidence; do not recreate deleted subtasks.

Optional OmniRoute tools, frontend dependencies, original-stack recreation and publication commands are not part of today's command list. This edit changed documentation only; no service command or application test was executed.
