# Committed reconnect and two-session cases

Each row is an individually executed case. PASS means the current implementation passed its assertions; fault IDs name experiments in which that same case failed.

| Case | Requirement / location | Baseline | Detected faults |
|---|---|---|---|
| committed-reconnect-cascade | tools/audit_database_lifecycle.py | PASS | LIFE-M001 |
| expiry-skips-locked | tools/audit_database_lifecycle.py | PASS | LIFE-M002 |
| purge-skips-locked | tools/audit_database_lifecycle.py | PASS | LIFE-M003 |
| expiry-batch-limit | tools/audit_database_lifecycle.py | PASS | LIFE-M004 |
| second-operation-failure-rolls-back-cleanup | tools/audit_database_lifecycle.py | PASS | LIFE-M005 |

[Fault catalogue](fault-catalogue.md) · [Audit report](../case-effectiveness-audit.md)
