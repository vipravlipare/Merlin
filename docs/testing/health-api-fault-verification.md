# Health API fault effectiveness — Day 7 step 4.2

The learner authored the scratch API. The assistant strengthened the API tests with explicit authorization, then implemented these five requested permanent faults in the existing Python audit. No application source file was changed or faulty implementation installed in the running server. Actual minutes are unknown; 15 minutes was the planned allocation, not measured elapsed work.

📚 Learn first: [the health API contract](../architecture/health-api-contract.md), API-01 through API-07; [the existing suite commands](test-suite-commands.md), isolated faults and result validation.
↩ Return: inspect the required case and actual assertion failure in [the synthetic evidence](health-api-fault-results.json), then integrate the reviewed inventory and remaining coverage in step 4.3.

## Observed results

The unmodified baseline passed all 349 Python case/subtest IDs. The five faults all compiled and applied; every corresponding case failed in its test call at the required assertion. There were **5 DETECTED, 0 SURVIVED, 0 INVALID, 0 TIMEOUT and 0 UNAPPLIED** results. No setup or teardown error was counted as detection. Existing non-database Python regressions also passed: **346 tests and 3 subtests in 4.30 seconds**. All **97 runner controls** passed, including four new attribution controls.

| Isolated fault | Required contract case | Intended observed failure |
|---|---|---|
| `health-api-wrong-status` | Healthy GET | HTTP 201 differs from required 200. |
| `health-api-wrong-body` | Healthy GET | JSON status `broken` differs from `ok`. |
| `health-api-post-accepted` | Unsupported POST | HTTP 200 differs from required 405. PUT is not changed by this fault. |
| `health-api-file-disclosure` | Sensitive-path GET | The body contains the synthetic temporary file contents instead of the exact generic error object. HTTP 404 remains correct, so a status-only test would miss this disclosure. |
| `health-api-error-leak` | Forced handler failure | JSON contains the invented error sentinel instead of the generic internal-server-error message. HTTP 500 remains correct. |

The audit now requires each named fault's corresponding test and assertion category. A failure elsewhere cannot substitute. Counterfactual controls verified that the correct assertion produces DETECTED, the wrong case or wrong assertion produces SURVIVED, and a fixture setup error produces INVALID. These controls are part of the existing runner verification.

## Isolation and repeat command

Faults are compiled into module memory in fresh child processes. The server binds only to temporary loopback ports; the file disclosure fault reads the test-created synthetic file in its temporary working directory and refuses a non-temporary path. No real private file or credential is needed. Child-process execution remains bounded by the existing audit timeouts. Source hashes were compared after execution and remained unchanged.

```bash
.venv/bin/python tools/audit_python_cases.py --only health-api- --out /tmp/merlin-health-api-faults.json
```

This command selects the five named faults and records the ordinary Python baseline. Its report is not the complete fault matrix: only cases exercised by those five faults receive detection evidence in that focused run. Inspect statuses and `intended_detection`; the parent complete-suite result validator is the normal final gate.

## Remaining work

Step 4.2's requested representative faults are complete. Step 4.3 remains pending: integrate all new API case/fault IDs into the reviewed suite inventory, complete any additional API effectiveness requirements, review dependency scope so unrelated old faults need not repeatedly run socket tests, and execute the full guarded suite. Do not regenerate inventories at runtime or hide failures to obtain green results. No hosted CI coverage for the uncommitted API files is claimed. Passing this finite experiment does not prove every possible API fault is covered.
