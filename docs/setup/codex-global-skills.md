# Global Codex skills: Terminal and Windows desktop

Verified October 11, 2026. This is an environment audit, not evidence that Merlin features are complete.

## Persistent setup already present

| Environment | Global instructions | Personal skills |
|---|---|---|
| Ubuntu / WSL Terminal | `/home/vipra/.codex/AGENTS.md` | `/home/vipra/.agents/skills/` |
| Windows desktop / native Terminal | `C:\Users\vipra\.codex\AGENTS.md` | `C:\Users\vipra\.agents\skills\` |

Both global instruction files already request Caveman by default in every session and every project. They keep normal English in persisted files and learning explanations. Both request the matching OmniRoute skill for routing, providers, compression and gateway health. OmniRoute is a family of skills, rather than one skill named `Omniroute`.

All 46 relevant personal skill directories exist in both environments: Caveman, the `cli-*` and `omni-*` families, and `config-codex-cli`. Their `SKILL.md` contents match byte for byte. Neither inspected Codex configuration contains a skills disable setting. No global override file was found in either inspected home. Global instructions and skills required no replacement.

## What was tested

Installed Ubuntu tools report `codex-cli 0.162.1` and OmniRoute `3.8.51`. A fresh local Codex app-server answered `skills/list` for Merlin: 90 Caveman/OmniRoute entries, none disabled, and zero discovery errors. The count includes repository and personal copies; it does not mean 90 distinct skills. This read-only protocol check sent no model inference request. Startup required access outside the workspace sandbox to normal Codex state.

The current workspace session also exposes the personal and repository skill families. Caveman instructions were read and used. Windows skill files and preferences were inspected from WSL, but the desktop application's skill selector and a fresh desktop conversation were not exercised. Windows installation is verified; desktop activation remains a manual check.

An OmniRoute health check outside the sandbox returned exit status 1: `Server not running. Start with: omniroute serve`. Skills can be discovered without that service. Commands that need the gateway cannot work until the service and required provider authentication are available. No provider, routing default, startup service, credential or inference setting was changed. Neither token savings nor active routing was demonstrated.

## Latest OmniRoute service check

On October 11, 2026, the WSL CLI and an HTTP connection check both confirmed that no service was listening on port 20128. The existing OmniRoute 3.8.51 installation was started with `omniroute serve --daemon --no-open --no-tray`. Its subsequent health response at 19:12 UTC (15:12 America/New_York) was **healthy**; the dashboard is `http://localhost:20128` and the API base is `http://localhost:20128/v1`. No provider, credential, model connection, routing default or autostart configuration was changed.

The quota-status response explicitly reported no live inference request, zero quota pools, zero authoritative/header quota monitors and unknown upstream quota status. The health response had zero observed Codex account pools. The cooldown command returned an empty result. These checks verify a running local gateway, not this conversation's inference route, token savings, or a Codex account-limit reset. The user identified the 3:09 reset as a Codex usage limit; that account's reset was not observed by these tools. Starting this daemon does not establish persistence after WSL or Windows restarts.

## Fresh-session verification

📚 Learn first: [Build skills](https://learn.chatgpt.com/docs/build-skills), read “How ChatGPT and Codex use skills” and “Where Codex loads local skills”; stop before creating a skill. [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), read “How Codex discovers guidance”; stop before project overrides. These official pages were opened October 11, 2026.
↩ Return: start a fresh Terminal or desktop session outside Merlin and check the personal skills and global preferences; done when Caveman is available and the assistant identifies the global default and selects a matching OmniRoute skill for a relevant task. Time box: 5 minutes per environment. If missing, follow the profile and environment checks below.

1. In Ubuntu Terminal, start `codex` from another project. Run `/skills` and look for `caveman` and `cli-health`. Ask: “Read the Caveman skill. Identify my global instruction file and Caveman default. Use cli-health to check OmniRoute and distinguish installed skills from active routing.” A gateway-down result is valid evidence of a service problem, not a discovery failure.
2. In Windows desktop, start a new local Codex session outside Merlin. Open Skills in the sidebar and inspect Caveman and an OmniRoute skill. Ask the same verification prompt. Where supported, explicitly select skills with `@`; Codex Terminal supports `$caveman` and `$cli-health`.
3. If the app does not show updated preferences, restart it and start a fresh conversation. Instructions are loaded at session startup. Record the actual result rather than treating file presence as proof of activation.

## Environment boundaries

📚 Learn first: [ChatGPT desktop app for Windows](https://learn.chatgpt.com/docs/windows/windows-app), read “Windows Subsystem for Linux (WSL)” and “Share config, auth, and sessions with WSL”; stop before changing settings. Verified October 11, 2026.
↩ Return: inspect the desktop app's Agent environment setting; done when you know whether its agent runs natively on Windows or inside WSL. Time box: 3 minutes. If uncertain, ask the new desktop session to identify its actual home directory and active global instruction file.

The Windows app can run a native agent or a WSL agent. Its integrated terminal setting is separate. Windows and Ubuntu homes are separate; the existing personal files cover both. Do not merge credentials or change `CODEX_HOME` merely to share skills. A custom home or another machine needs its own verification.

Global preferences are instructions, not a guarantee that every model always follows them. Project instructions, explicit normal-mode requests, unavailable environments and application updates can change behavior. Ordinary cloud chats do not establish access to these local directories. Portable plugin distribution is a separate workflow, not something this audit installed.

## Merlin handoff

The previous session saved 411 passing and 16 failing checks. Three defect groups remain: probe query-error handling, Python/PostgreSQL Unicode whitespace consistency, and quiz answer-state validation. The older `docs/testing/pre-repair-verification-results.md` describes an earlier run; the capsule and [current failure guide](../planning/historical-failure-repair-guide.md) describe the later saved audit. No application test was rerun here.

The checkout is accessible in this agent. Windows-to-WSL and VS Code recovery remains unverified. Preserve both database cluster identities in `STATE.md`. Resume learner-owned probe repair after access is confirmed; no application implementation starts during this skills audit.
