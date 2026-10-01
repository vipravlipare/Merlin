# AGENTS.md (repo root): rules for any coding agent in this repo

## What this repo is
A 37-day learning project (Thu Oct 1 → Fri Nov 6, 2026). I am a beginner. **Phase 1 is planning only:** you write planning documents. **I write all application code.**

## Session start (every session)
1. Read `docs/planning/STATE.md` (where we are, NEXT).
2. Read `docs/planning/MASTER_PROMPT.md` (the spec; rules R1-R13, §1.4 hour waterfall, §9 Parts list).
3. Continue at **NEXT** in STATE.md. Do not re-summarize the prompt or earlier Parts.

## Hard rules
- **Write only under `docs/planning/`.** Never create application code, config files, scripts, SQL/DDL or CI files (R3). Specs, test-case tables, hint ladders and checklists only.
- **Deliver each Part as a file:** `docs/planning/part-NN-<slug>.md`. In chat, reply with ≤ 10 lines: file written, what it covers, open questions. Do **not** paste the Part into chat.
- **After every Part, update `docs/planning/STATE.md`** (format: MASTER_PROMPT §9, ≤ 600 words).
- **Links (R1/R2):** every Epic, story, skill card, checklist item and day has a `📚 Learn first` block and a `↩ Return` line. Never invent URLs. Use official docs. If unsure, give the docs root plus the exact page title and mark `🔎 verify`. If a docs-lookup tool (Context7 MCP) is available, use it for library APIs and say so.
- **Browsing:** if you can search the web, verify every `browse-verify` item and state the date. If you cannot, mark `🔎 verify`. Never claim to have verified something you could not.
- **Frameworks (R12):** from-scratch version first, framework version second, comparison ADR third. Pin versions.
- **AI claims (R13):** every AI feature needs a golden set, baseline, metric, latency and cost.
- **Honesty (R5):** no feature is "built" unless I built it. Say plainly what cannot fit in the hours.
- **Hours:** every day's blocks sum to that day's budget (§1.4). No invisible work.

## Output style (Terse Mode, applies to chat replies)
Cut words, never content. No preamble, no recap, no praise. IDs instead of repeating text. **Never shorten:** links and Return lines, Gherkin, test-case tables, hint ladders, explain-back questions, setup commands and verification steps, security criteria, limits and honesty statements. Written planning documents keep full plain-English definitions for a beginner. If a caveman/terse skill is active, it applies to chat only, not to files. `/verbose` = explain fully; `/terse` = back to terse.

## If you are cut off or switched to another model
End at a clean boundary and write `⚠️ STOPPED AT: <ID>` in STATE.md. A new model must be able to continue from AGENTS.md + MASTER_PROMPT.md + STATE.md alone.

## Rule Card (R1-R13 in brief)
R1 Learn→Return links · R2 no invented URLs · R3 I write all code; you write specs/tests/hints · R4 proof of learning (explain-back, acceptance test, whiteboard, re-quiz) · R5 honest feasibility + hour ledger + swap-not-add · R6 security first · R7 interview framing + public-source parity only · R8 Jira-native, ≤ 90-min checklist items · R9 stop-anywhere rungs · R10 terse mode · R11 files are truth + STATE.md · R12 scratch before frameworks · R13 measure every AI claim.
