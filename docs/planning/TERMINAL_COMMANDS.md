# Merlin terminal commands and folder locations

Run Linux commands in **Ubuntu/WSL**, not ordinary Windows PowerShell. Canonical checkout: `/home/vipra/Merlin`. This reference covers setup and daily development; no application/API start command exists yet.

## Find Ubuntu in Windows File Explorer

Press **Win+E**, press **Ctrl+L**, paste this address, then press **Enter**:

```text
\\wsl.localhost\Ubuntu\home\vipra\Merlin
```

Alternative:

```text
\\wsl$\Ubuntu\home\vipra\Merlin
```

You are viewing the Ubuntu files directly, not a synchronized copy. Inside that folder, open `docs\planning\TERMINAL_COMMANDS.md` for this reference, `docs\SETUP.md` for reproduction, and `Quizzes\sprint-0-quiz.html` in your browser. Pin Merlin to Quick access if useful. If Ubuntu is not running, open Ubuntu first. Do not develop in the old `C:\Users\vipra\Merlin` copy or edit WSL's underlying virtual disk/AppData files.

📚 Learn first: [Microsoft: working across filesystems](https://learn.microsoft.com/en-us/windows/wsl/filesystems), Linux files from Explorer; stop before permissions changes. Official page retrieved October 6, 2026.
↩ Return: open the share path, then open **Merlin Ubuntu** or `code .`; done when VS Code shows `WSL: Ubuntu` and its terminal reports `/home/vipra/Merlin`.

## Open Ubuntu, VS Code and Codex

From **Windows PowerShell**:

```powershell
wsl -d Ubuntu --cd /home/vipra/Merlin
```

From **Ubuntu**:

```bash
cd /home/vipra/Merlin
pwd
code .
codex -C /home/vipra/Merlin
```

`codex -C ...` opens a **new session** in that checkout. To continue an existing session instead:

```bash
codex resume --last
```

Inside the Codex CLI, `/skills` lists available skills; `$caveman` explicitly invokes Caveman. Global Caveman preferences and OmniRoute skill files are installed in this user's Ubuntu and Windows profiles. They are local installations, not automatic cloud/account synchronization. Project instructions may override global defaults. OmniRoute skills do not mean Codex model requests are routed through its gateway; that integration remains unproved.

In the desktop app, start a new Codex chat and select the Ubuntu Merlin folder. First prompt: “Read STATE.md and the Sprint 1 Day 6 plan. Help me complete the next learner-owned task.”

📚 Learn first: [global instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [skills](https://learn.chatgpt.com/docs/build-skills), discovery/precedence; stop before changing providers. Official pages retrieved October 6.
↩ Return: verify the new session reads the canonical checkout and global preferences; preserve the working model connection.

## Daily environment and service checks

```bash
uv run --locked python --version
uv run --locked python tools/doctor.py --static
docker compose config --quiet
uv run --locked python tools/setup_local.py
uv run --locked python tools/doctor.py
docker compose ps
docker compose port postgres 5432
docker compose port redis 6379
```

`setup_local.py` creates ignored private configuration only if absent, then starts services. An existing `.env` is preserved. Doctor reports PASS/WARN/FAIL without printing credentials. `--static` does not require running services; the normal doctor tests the actual runtime. Read [SETUP](../SETUP.md) for prerequisites, isolation and exact five-command fresh-clone instructions.

## Stop and storage retention

```bash
docker compose stop --timeout 30 postgres redis
```

This stops services while retaining containers and volumes. For a deliberate recreation test only:

```bash
uv run --locked python tools/doctor.py
docker compose down
uv run --locked python tools/setup_local.py
uv run --locked python tools/doctor.py
```

Compare PostgreSQL cluster identity before/after. For **the original checkout only**:

```bash
uv run --locked python tools/doctor.py --expect-cluster 7691749973399031842
```

Never add `--volumes` to teardown of the original project. Never delete its data to fix a password. Fresh clones get their own project/network/ports/volumes and a different cluster. Disposable test cleanup must first verify which project is being removed.

📚 Learn first: [Compose down](https://docs.docker.com/reference/cli/docker/compose/down/), named-volume lifecycle; stop before destructive options.
↩ Return: stop safely, or compare identity during a deliberate recreation; preserve the original PostgreSQL volume.

## Locked installs and setup tests

```bash
uv sync --locked
pnpm install --frozen-lockfile --ignore-scripts
uv run --locked python -m unittest discover -s tools -p 'test_*.py'
```

These currently reproduce setup metadata and test setup automation. They do not run application tests. `npm test` is still an unused placeholder and is not the Sprint 0 acceptance command. Only add feature dependencies when the selected learner task requires them; review lock changes.

## Git: review, save and publish

```bash
git status --short
git diff --stat
git diff --check
git log -5 --oneline
git branch --show-current
git check-ignore .env
git ls-files .env
```

Expected: `.env` ignored; the last command returns no tracked `.env`. Review `git diff` privately before staging; do not paste a diff containing a secret. Stage named intended files, for example:

```bash
git add README.md docs/SETUP.md docs/planning/TERMINAL_COMMANDS.md
git diff --cached --stat
git commit -m "docs(setup): clarify local startup"
git push origin HEAD
```

Do not use blanket staging or force-push. A commit saves reviewed files locally; a push publishes those commits to the selected branch. `git push` does not merge a feature into another branch. View actual CI in [GitHub Actions](https://github.com/vipravlipare/Merlin/actions).

## Native clients and private database sign-in

```bash
psql --version
redis-cli --version
```

For manual SQL access, use `psql -X -h 127.0.0.1 -p <published-port> -U <configured-user> -d <configured-database> --password`, substituting nonsecret names/port. Type the password at its private prompt; do not put it into a command, screenshot or chat. Fresh-clone ports can differ from 5432/6379; use Compose's port commands above. Doctor performs automatic authentication checks without displaying passwords.

## Optional global OmniRoute service

```bash
systemctl --user status omniroute.service --no-pager
systemctl --user start omniroute.service
systemctl --user stop omniroute.service
```

Dashboard: `http://localhost:20128`. Starts with the Ubuntu user session; stopping WSL stops it. Installed skills and a healthy gateway do not guarantee every provider, Codex tool call or compression plan works. This optional tool is not required for Merlin database startup. Never print gateway/provider credentials or paste them into this reference.
