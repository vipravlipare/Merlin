# Part 04 — D13 Environment Setup Guide

Status: planning/specification only. The learner types every command and writes every configuration file. Primary route: Windows 11 + WSL2 Ubuntu, 16 GB RAM, RTX 3050 4 GB VRAM. Disk, driver and admin rights are checked first.

## 1. Setup contract

Do not install optional tools during S0. Core setup only: Git/SSH, editor, WSL2 shell, Python through uv, Node LTS + pnpm, Docker Desktop/Compose, PostgreSQL and Redis through learner-written Compose specs, GitHub/Jira, AWS account/MFA/budget alarm, and CI skeleton. Ollama and model download move to Day 8. MongoDB, Java/Maven, kind/kubectl, n8n, Chroma/Qdrant, Hugging Face/Colab/Kaggle, Playwright and k6 are just-in-time.

Done means a fresh clone can run the learner’s doctor checklist and the core stack can start or fail with a documented reason. Installed versions are evidence only after the learner records them and resolves a lockfile.

📚 Learn first (Must read): [Microsoft Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install), read requirements and install overview; stop before optional distributions; why: WSL is the primary shell boundary (~10 min).
↩ Return to build: Day 1, record Windows edition, WSL version, Ubuntu distribution, architecture, free disk, RAM and GPU visibility; done when unknown fields are named; time box: 20 min; if stuck: keep the smallest model path and log the blocker.

## 2. Windows + WSL2 primary path

The learner checks Windows Update, virtualization in firmware, Virtual Machine Platform and WSL2. Use an Ubuntu LTS distribution supplied by the official WSL route. Keep repository files inside the Linux filesystem for normal development; avoid mixing Windows and Linux package managers for one environment.

Verification evidence:
- Windows terminal reports WSL version and distribution state.
- Ubuntu shell reports architecture and Python/Node tool locations.
- WSL can see the NVIDIA device only after the driver and Docker GPU path are verified; no CUDA claim is made from a device name alone.
- Docker Desktop WSL integration is enabled only for the selected distribution.
- The learner records free disk before model downloads.

📚 Learn first (Must read): [Docker WSL 2 backend](https://docs.docker.com/desktop/features/wsl/), read WSL integration and resource settings; stop before Kubernetes; why: Docker and WSL share memory on a 16 GB machine (~10 min; 🔎 verify current page at first use).
↩ Return to build: Day 1, write a hardware doctor checklist and a Docker/WSL evidence row; done when CPU/RAM/disk/GPU status has a timestamp; time box: 20 min; if stuck: use CPU-only local models.

## 3. macOS and Ubuntu alternatives

macOS: use the official Terminal, Git/SSH, uv, Node LTS/pnpm and Docker Desktop; Apple Silicon or Intel must be recorded, and Ollama GPU assumptions differ. Ubuntu: use the official Ubuntu install path, native Git/SSH, uv, Node LTS/pnpm and Docker Engine/Compose; exact package versions and user-group setup are verified at first use. Neither alternative changes the ledger.

📚 Learn first (Must read): [Docker Get Started](https://docs.docker.com/get-started/get-docker/), read platform prerequisites; stop before optional products; why: Docker availability differs by OS (~8 min).
↩ Return to build: Part 4 alternative branch in setup notes; done when one non-Windows path is documented without claiming it was executed; time box: 15 min; if stuck: mark the unexecuted path as unverified.

## 4. Accounts and identity

Create or verify GitHub and Atlassian accounts. Use a unique password and MFA. Keep repository visibility unchanged until a publication decision exists. GitHub Free private-branch protection may be limited; document manual merge gates if needed.

AWS: create or verify the account only if the learner accepts the terms and any payment-method or temporary-hold requirement. Enable MFA and a budget alert, but remember alerts are not hard spending caps. Stop before paid-plan enrollment if zero out-of-pocket is mandatory.

Never paste tokens into shell history, commits, issue comments, screenshots or logs. Store secrets through the learner’s local secret mechanism specified later; commit only an example-name specification.

📚 Learn first (Must read): [GitHub SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh), read key generation and testing; stop before deploy keys; why: Git identity must not depend on passwords in scripts (~10 min). [AWS account signup](https://docs.aws.amazon.com/accounts/latest/reference/sign-in-new.html), read plan/payment information; stop before enrollment; why: account eligibility is conditional (~8 min).
↩ Return to build: Day 2, record account status, MFA, repository visibility and AWS blocker/eligibility; done when no paid assumption is hidden; time box: 25 min; if stuck: local-only route.

## 5. Git, editor and shell

Git identity must use a learner-owned name/email. SSH key files stay outside the repository. Configure the editor to use the WSL interpreter and terminal. Use one shell for a task; do not copy Windows paths into Linux commands without deliberate translation.

Evidence commands/spec checks:
- Git version and configured identity recorded.
- SSH test reaches GitHub without printing private key material.
- Editor opens the repository in the intended environment.
- Line endings and executable-bit expectations are documented.
- Branch/commit naming follows D10.

📚 Learn first (Must read): [Git About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control), read repository and commit concepts; stop before branching details; why: the learner must understand the history being created (~10 min).
↩ Return to build: Day 1–3, make a setup-only branch and PR; done when the PR shows learner-authored setup notes and no secrets; time box: 30 min; if stuck: manual copy of the verification output without credentials.

## 6. Python through uv

Use uv as the Python environment manager. Planning candidate: Python 3.12.15 and uv 0.12.21, both rechecked at installation. Python 3.12.15 upstream availability through uv is 🔎 verify because the release is source-oriented. The learner records interpreter path, version, project environment and lock resolution.

Spec requirements:
- one project environment;
- explicit Python constraint;
- lockfile generated by the learner;
- no global feature dependencies;
- separate optional groups for later AI/framework tools;
- clean install from lockfile;
- no secrets in project metadata.

📚 Learn first (Must read): [uv Python management](https://docs.astral.sh/uv/guides/install-python/), read managed Python and version selection; stop before package examples; why: reproducible Python setup (~10 min).
↩ Return to build: Day 1, create the learner’s environment and record interpreter/lock output; done when a clean shell resolves the same direct dependencies or the mismatch is documented; time box: 30 min; if stuck: use an installed compatible 3.12 patch and record the swap.

## 7. Node LTS and pnpm

Planning candidate: Node 24.21.0 LTS and pnpm 12.8.1, rechecked at first use. Use Node only for hooks and later React tooling during its scheduled day. Do not install frontend dependencies in S0.

Evidence:
- node and pnpm versions;
- package-manager store path;
- project package manager field;
- clean install and lockfile;
- no globally installed project dependencies except the documented manager.

📚 Learn first (Must read): [Node.js releases](https://nodejs.org/en/about/previous-releases), read LTS status; stop before community installers; why: use supported runtime; [pnpm installation](https://pnpm.io/installation), read supported methods; stop before workspace features (~10 min total).
↩ Return to build: Day 3, record versions and hook prerequisite only; done when no React feature package is installed early; time box: 20 min; if stuck: defer app tooling to Day 13.

## 8. Docker, Compose, PostgreSQL and Redis

Planning candidate: Docker Desktop 4.93.0 and Compose version supplied by that install; recheck at first use. Compose spec must define only the core services at first: API placeholder owned by learner later, PostgreSQL with persistent volume, Redis with persistent policy only if needed. Do not write the Compose file in this Part.

Required specification fields: service name/image digest, ports bound to loopback, network, health check, resource limits, volume, non-root intent, environment names without values, startup dependency, logs, stop command and teardown. PostgreSQL uses a learner-chosen supported 17.x image; pgvector is added at its scheduled first use. Redis is not a claim of a cache/queue implementation.

Verification:
- Docker engine and Compose versions;
- compose config validation;
- services healthy;
- psql reaches the database over the intended local port;
- Redis responds locally;
- volumes and teardown are understood;
- no service is exposed publicly.

📚 Learn first (Must read): [Docker Compose application model](https://docs.docker.com/compose/intro/compose-application-model/), read services, networks, volumes, secrets; stop before examples; why: container configuration is a design contract (~12 min). [PostgreSQL tutorial](https://www.postgresql.org/docs/17/tutorial.html), read installation/access basics; stop before advanced features (~10 min).
↩ Return to build: Day 4, write a Compose specification and learner-authored verification checklist; done when config validation, health and local psql/Redis checks are named; time box: 30 min; if stuck: one database service before Redis.

## 9. Just-in-time install map

| Tool | First-use window | Gate |
|---|---|---|
| Ollama + Qwen3 0.6B/1.7B + nomic embedding | Day 8/16 | hardware, digest, memory, TTFT, tokens/sec |
| MongoDB | Conditional Day 31 | scratch traces and swap funded |
| JDK 21 + Maven + Spring Boot | Conditional Day 31 | Mongo/Spring swap funded |
| kind + kubectl | Conditional Day 32 | core complete, hardware and swap |
| n8n | Conditional Day 28 | handwritten workflow passes and license check |
| Chroma/Qdrant | Conditional comparison | same corpus/golden set and swap |
| Hugging Face + Colab/Kaggle | Conditional Day 30 | dataset/model license and quota check |
| AWS CLI beyond account alarm | Day 25 or 32 if eligible | least-privilege identity and local fallback |
| Playwright browsers | Day 34 if swapped | concrete browser gap |
| k6 | Day 34 if swapped | concrete load gap |

📚 Learn first (Must read): [Ollama API introduction](https://docs.ollama.com/api/introduction), read API base URL; stop before model downloads; why: local provider starts after core setup (~5 min).
↩ Return to build: place each optional install in its scheduled Jira task; done when no optional dependency enters the lockfile early; time box: 15 min planning; if stuck: defer the tool, do not install “just in case.”

## 10. Doctor specification

The learner writes a doctor command/script later. It must check, without printing secrets:

- OS/WSL distribution and architecture;
- free disk and RAM;
- Git identity and SSH connectivity;
- Python/uv interpreter and lockfile;
- Node/pnpm versions when frontend tools are active;
- Docker/Compose engine;
- PostgreSQL and Redis health;
- Ollama process/model/digest only after Day 8;
- repository cleanliness, branch and current commit;
- required environment variable names present, values redacted;
- clock/time zone and filesystem permissions.

Each check returns pass, warn or fail; output names the first safe fix. A doctor failure is evidence, not permission to skip a gate.

📚 Learn first (Must read): [GitHub Actions concepts](https://docs.github.com/en/actions/get-started/understand-github-actions), read jobs and steps; stop before advanced workflows; why: local doctor checks later become CI-friendly checks (~10 min).
↩ Return to build: Day 4, write doctor input/output/error specifications; done when every check has an expected result and secret-redaction rule; time box: 25 min; if stuck: four checks first—Git, Python, Docker, database.

## 11. Fresh-clone test

The learner performs this after the repository skeleton and again before each rung release:

1. Use a clean directory or disposable clone.
2. Follow the README setup in no more than five commands after prerequisites.
3. Run doctor.
4. Start the local core profile.
5. Run health, database and test checks.
6. Seed only documented synthetic data.
7. Run the smallest acceptance/eval case.
8. Stop and remove services; verify no secret or private data entered the clone.
9. Record elapsed setup time, failure and fix.

A failed fresh clone blocks the release claim until fixed or explicitly listed as a limitation.

📚 Learn first (Must read): [GitHub README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes), read setup/documentation expectations; stop before formatting; why: reproducibility is part of Done (~8 min).
↩ Return to build: Day 4 and every release, execute the learner-written fresh-clone checklist; done when the log has command count, result and known limitation; time box: 30 min; if stuck: stop at the first failed command and document it.

## 12. Troubleshooting table

| Symptom | First check | Safe first fix |
|---|---|---|
| WSL distribution will not start | virtualization, WSL version, disk | reboot/update or use documented Ubuntu path; no random installers |
| Docker cannot reach WSL | selected integration and distro state | restart Docker/WSL; record version; CPU-only fallback |
| GPU invisible | driver, WSL pass-through, Docker support | run CPU model; do not claim GPU use |
| Out of memory | Docker limit, concurrent services, model context | stop services, shorten context, use Qwen3 0.6B |
| Port already used | learner’s process/Compose list | choose documented local port; never expose publicly |
| psql auth failure | environment names, service health, volume state | inspect redacted config; avoid deleting volumes without backup |
| uv cannot resolve | Python availability, direct pins, platform marker | use compatible patch and record pin change |
| pnpm lock mismatch | Node/pnpm versions and lockfile | use declared manager/version; do not regenerate silently |
| AWS asks for payment | account plan/eligibility | stop; local release is valid fallback |
| Fresh clone fails | first failing command | fix one prerequisite; update setup/README evidence |

📚 Learn first (Must read): [Docker troubleshooting](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/), read diagnostic basics; stop before unrelated support features; why: failure recovery must preserve evidence (~8 min; 🔎 verify page at first use).
↩ Return to build: add the first observed symptom and fix to the learner’s troubleshooting log; done when the table contains a real reproduction or says unobserved; time box: 10 min in C-02; if stuck: preserve logs, stop destructive cleanup.

## 13. SETUP.md and README v0 outlines

SETUP.md sections: scope/OS route; prerequisites; account/MFA; Git/SSH; Python/uv; Node/pnpm; Docker/Compose; local services; environment names; doctor; fresh clone; stop/teardown; troubleshooting; data/privacy warning; optional tools by first-use day.

README v0 sections: one-sentence problem; planned rung; local-only status; architecture placeholder; five-command target; tests/evals planned; honest not-built list; license/attribution placeholder; link to planning files.

📚 Learn first (Must read): [12factor.net](https://12factor.net/), read Config and Dev/prod parity; stop before other factors; why: setup must separate configuration from code (~8 min).
↩ Return to build: Day 4, outline SETUP.md and README v0 in learner-owned files; done when a fresh clone can follow the outline without hidden commands; time box: 25 min; if stuck: write prerequisites before prose.

## 14. Acceptance and resources

D13 passes when the learner has a verified primary OS route, account/secret boundary, reproducible core tool versions, Compose/health specification, doctor specification, fresh-clone test and troubleshooting log. No installer, config, script, SQL or CI file is created by this Part.

Resources checked 2026-10-01: [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) verified; [Docker Get Docker](https://docs.docker.com/get-started/get-docker/) verified; [Docker Compose model](https://docs.docker.com/compose/intro/compose-application-model/) verified; [uv install](https://docs.astral.sh/uv/getting-started/installation/) verified; [uv Python management](https://docs.astral.sh/uv/guides/install-python/) verified; [Node releases](https://nodejs.org/en/about/previous-releases) verified; [pnpm install](https://pnpm.io/installation) verified; [GitHub SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) verified; [AWS signup](https://docs.aws.amazon.com/accounts/latest/reference/sign-in-new.html) verified; [AWS budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html) verified; Docker WSL page 🔎 verify at first use.

NEXT: Part 5 — D11 Component Breakdown.

