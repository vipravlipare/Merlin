# Day 8 handoff — local model readiness and retained verification

Recorded October 19, 2026. Tracker: [MER-9](https://vipravlipare.atlassian.net/browse/MER-9). Day 8 names the learning sequence, not a claim that all activity occurred within one planned day. Actual total learner/assistant minutes, installation minutes and review/handoff minutes are **unknown**. The planned 20-minute handoff allocation is not an observed duration. No extra hours or story completion are inferred.

📚 Learn first: [readiness contract and actual results](../evals/local-model-readiness.md), measured outcomes, limits and first failures; [next scratch provider contract](../architecture/local-provider-contract.md), unimplemented protocol/security requirements.
↩ Return: complete the learner explain-back in section 5.3, then resolve the publication/hosted-CI blocker below before declaring the day complete. Do not implement an adapter, enlarge the model or start deployment from this handoff alone.

## Authorship and actual work

| Work | Authorship and limits |
|---|---|
| Initial hardware inspection and failed inference | Learner ran terminal commands, supplied resource/listener/model evidence and the 60-second failed-request logs. Learner confirmed Ubuntu/WSL as the runtime. |
| Requirements and evidence planning | Assistant authored the local readiness contract, evidence destinations, future provider protocol contract and Jira/local records at explicit request. These are planning artifacts, not an implemented provider client. |
| Installation and download | Assistant installed the approved pinned user-local runtime and downloaded only the selected model under explicit authorization, verifying release/model/blob identities and license. |
| Follow-up inference and measurements | Assistant executed the authorized managed CUDA comparison, one cold/three warm benchmark, healthy/negative cases and cleanup. Do not attribute these executions to the learner or infer learner understanding from them. |
| Existing Merlin application | The scratch health API remains learner-authored. Later explicit authorization permitted assistant type hints/spacing, redundant-comment removal and connection-call formatting only. Source behavior was preserved; note validation/maintenance were not refactored. |
| Test inventory and verification | Assistant synchronized the relocated probe diagnostic ID, retained all cases/faults, and ran focused/full guarded checks. No provider parser/test/fault implementation was added. |

## Runtime and artifact identity

- Runtime: Ubuntu/WSL2, Linux x86_64; Ollama **0.40.6** installed under the learner's user-local tools, available as `ollama` on PATH. No autostart service was enabled.
- Release archive SHA-256: `c164ab8b1b28e2a247c29719b8e404c423c5b83ae64c3ab4e59d50c7ff7fc5e0`.
- Only model: **qwen3:0.6b**, **Q4_K_M**, **Apache-2.0**, attribution Qwen Team / Qwen3-0.6B. Installed model inventory reports 522,653,767 bytes. Preserve the installed license/notice when redistributing.
- Full model digest: `sha256:7df6b6e09427a769808717c0a93cadc4ae99ed4eb8bf5ca557c90846becea435`. All six referenced blobs passed independent hash/size checks. Installed augmented-manifest hash is distinct; see the recorded verification correction rather than substituting it for this model digest.
- Explicit **cuda_v12** is the provisional per-session diagnostic choice. Neither a permanent override nor a proven general speed advantage was installed. Runtime/model/driver pins were not changed to hide the original failure.

## Observed outcomes and timings

| Outcome | Status / observed evidence |
|---|---|
| 2.1–2.4 inspection, selection, probe contract and evidence plan | COMPLETE for their respective inspection/planning scope. |
| 3.1 pinned installation | PASS for executable/version verification; actual elapsed minutes and 20-minute compliance unknown. |
| 3.2 single model download | PASS; timed download/first verification attempt 92.346 s, followed by separately recorded corrective manifest verification. |
| Original learner request | FAIL: curl 28, zero response bytes, HTTP placeholder 000 after **60.002684 s**; GPU-discovery watchdog and 40.36-second runner startup observed. |
| 3.3 controlled CUDA follow-ups | PASS generation/identity/GPU placement: CUDA 13 request **17.452 s**, CUDA 12 **4.441 s**. Original intermittent cause unresolved. |
| 3.4 model-unloaded cold / three warm | PASS measurement scope: request walls **3.227785 / 0.043842 / 0.054822 / 0.057639 s**. Full experiment including discovery/cleanup **10.213 s**. Warm requests cached 23 of 24 input tokens. |
| Exact READY content | FAIL: Ready. returned instead. Retained separately from generation success; no quality claim. |
| 3.5 review and authorized small refactor | Review complete. **232 focused tests** passed before/after. No new project dependency/adapter/global configuration added. |
| 4.1 healthy and negative cases | PASS expected outcomes: healthy 200/**4.408811 s**, missing model 404/**0.002334 s**, unavailable service curl 7/**0.000154 s**, forced deadline curl 28/**0.001483 s**. Entire experiment **10.422 s**. |
| Timeout cleanup | Owned-server group exited in **0.165 s**; no listener/process/GPU allocation afterward. This does not establish automatic in-flight cancellation from client close. |
| 4.2 streaming/error requirements | COMPLETE for specification only. All 24 planned protocol cases/faults remain PENDING implementation/execution. |
| 4.3 retained local suite | PASS all ten stages in **51.164283 s**; 729 Python/database tests plus three subtests, 40 JavaScript cases, 349 demonstrated Python case IDs, 250 canonical Python faults detected. Source preservation and cleanup passed. |
| 4.3 latest published CI | PASS **8602ccf14311142549a2e7b0f5d2527961872b6e**, [run 39198877902](https://github.com/vipravlipare/Merlin/actions/runs/39198877902), required setup job/every step. Newer refactor/docs are unpublished: exact hosted proof PENDING. |
| 4.4 actual status/cost record | COMPLETE; finite observations and open failures retained. No AI feature-evaluation gate claimed. |
| 5.1 publication/resource review | COMPLETE within scan/review scope; no findings, no owned model/API listener/process, both protected volumes and pre-existing services preserved. No commit made. |
| 5.2 handoff | COMPLETE as this assistant-authored artifact. |
| 5.3 learner explain-back | PENDING; cannot be completed by assistant-authored explanation or successful model output. |

The full evidence record preserves API timing/token/rate details. First byte was measured; **first generated-content/token latency remains PENDING**. Samples do not establish exact RAM/VRAM peaks. Four tiny repeated requests do not establish sustained throughput, p95, quality or global production capacity. Observed new service purchases for these operations were $0; unrelated billing was not audited, and hardware/electricity/network costs are unknown.

## First failures and current blocker

The first setup attempt returned command-not-found/exit 127. After installation, the download verifier initially compared the API digest with an augmented local manifest; corrected verification proved the preserved original manifest/configuration/layer relationship, without changing model bytes. The learner's first generation then timed out. The later controlled backends worked, but that does not prove the original watchdog cause was repaired. A temporary backend preflight also hit a recently used address; it was corrected by checking actual listener ownership/address reuse rather than killing an unknown process. All failed attempts remain visible in the readiness record.

**First current completion blocker: unpublished refactor's hosted verification (4.3).** Existing local proof matches current source hashes, but an older green hosted commit cannot certify later source changes. No separate publication authorization for the later refactor/docs has been received. The learner requested finishing the section 5 review/handoff before committing; no commit/push is performed by this handoff task.

## Work carried forward

- **Learner understanding:** 5.3 request path, memory/context/latency tradeoffs and checklist review remain open. Earlier Day 7 corrected explanations exist in chat; saved contract answers still need reconciliation without inventing learner text.
- **CI/publication:** review the final current diff/secret handling after handoff; obtain specific publication authorization, push normally and observe exact new-commit CI. Keep 4.3 open until then.
- **Provider software:** no application model client, streaming parser, retry/cancellation implementation, automated protocol tests or isolated provider faults exists. The 24 proposed cases are specifications, not executed checks. Implement only in a separately agreed learner-owned slice with synthetic CI fixtures independent of GPU/downloaded models/private services.
- **Model failures:** original intermittent watchdog cause unresolved; exact uppercase/punctuation instruction compliance FAIL. Do not increase deadlines, weaken expectations or silently use cloud inference to close them.
- **Evaluation:** ≥20 labeled task-quality cases, baseline, named metric/predeclared threshold, meaningful latency/cost and production load/security evaluation PENDING. Protocol test tables are not a quality golden set.
- **Hardware/cancellation proof:** first-token latency, exact peaks, repeatable cold-cache performance and dependable in-flight server cancellation remain unproven. Continue rechecking resource gates before model loading; do not infer active swapping from occupied swap alone.
- **Existing application boundary:** authenticated ownership-denial checks remain PENDING until the application has that boundary. SQL checks and process liveness do not establish API authorization.
- **Unrelated carryover:** permanent OmniRoute client defaults remain pending; AWS/DSA remain deferred. Do not expand Day 8 automatically to include them.

## Preservation and exact restart action

No experiment-owned Ollama/model/API process or listener remained at the latest review. Keep the downloaded runtime/model for reuse. Preserve both database volumes and all pre-existing services; do not rerun installed migrations, undo them on protected storage, uninstall shared tools or change coding-agent routing. Publication scan found no known-value/pattern findings within its finite scope; raw temporary logs/private configuration are not publication artifacts. Re-review newly added material before a future commit.

**Exact next action:** the learner completes section 5.3 in their own words: describe Merlin client → local Ollama → model → response, explain why download size differs from runtime memory, distinguish model-unloaded cold from cached warm measurements and explain why timeout/200 alone do not prove quality or cancellation. Review those answers and the final diff/checklist. Then, if specifically authorized, commit and normally push the reviewed refactor/docs and verify required CI for that exact commit; record it before checking off 4.3 or considering the story Done. A complete handoff is not a completed implementation/evaluation story.

## Final learner confirmation and publication authorization

October 19, 2026: the learner explicitly confirmed **1.1 and 5.3 complete**, and authorized finishing 4.3 so Day 8 can close. Record these as learner-confirmed, not assistant independently administered exam results. Earlier PENDING/authorization statements above describe prior snapshots and are superseded by this update. Historical initial contract answers are labeled as such without inventing learner text. Section 1's local tracking is reconciled with learner-confirmed Jira items.

Publication of the reviewed later source cleanup and documentation is now authorized. Current exact next action: finish the pre-publication review, commit and normally push, observe the required CI job for that exact commit, then reconcile 4.3 and the story status. Until that hosted result exists, 4.3 remains PENDING. All deferred provider implementation, quality, cancellation, first-token and production claims remain unchanged; the readiness story does not claim those future capabilities.
