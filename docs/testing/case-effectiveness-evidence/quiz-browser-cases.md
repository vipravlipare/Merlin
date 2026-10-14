# Real Chromium workflow cases

Each row is an individually executed case. PASS means the current implementation passed its assertions; fault IDs name experiments in which that same case failed.

| Case | Requirement / location | Baseline | Detected faults |
|---|---|---|---|
| fresh quiz renders 35 questions and 140 choices | tools/audit_quiz_browser.mjs | PASS | UI-M001 |
| missing answers block results and focus the first missing question | tools/audit_quiz_browser.mjs | PASS | UI-M002 |
| radio change updates progress and saves the exact answer | tools/audit_quiz_browser.mjs | PASS | UI-M003 |
| partial progress and choice order survive reload | tools/audit_quiz_browser.mjs | PASS | UI-M004 |
| all correct answers show honest score and lock controls | tools/audit_quiz_browser.mjs | PASS | UI-M005 |
| double submission never duplicates feedback | tools/audit_quiz_browser.mjs | PASS | UI-M006 |
| retry contains only mistakes and clears previous answers | tools/audit_quiz_browser.mjs | PASS | UI-M007 |
| retry score uses its own denominator and practice wording | tools/audit_quiz_browser.mjs | PASS | UI-M008 |
| restart restores full bank and clears completed progress | tools/audit_quiz_browser.mjs | PASS | UI-M009 |
| completed attempts restore results after reload | tools/audit_quiz_browser.mjs | PASS | UI-M010 |
| incomplete submitted cache resets and remains usable | tools/audit_quiz_browser.mjs | PASS | UI-M011 |
| malformed cache resets without script errors | tools/audit_quiz_browser.mjs | PASS | UI-M012 |
| array answer cache resets rather than silently losing progress | tools/audit_quiz_browser.mjs | PASS | UI-M013 |
| storage unavailable still allows completing a quiz | tools/audit_quiz_browser.mjs | PASS | UI-M014 |
| critical mistake shows warning despite a high score | tools/audit_quiz_browser.mjs | PASS | UI-M015 |
| print control invokes the browser print action once | tools/audit_quiz_browser.mjs | PASS | UI-M016 |

[Fault catalogue](fault-catalogue.md) · [Audit report](../case-effectiveness-audit.md)
