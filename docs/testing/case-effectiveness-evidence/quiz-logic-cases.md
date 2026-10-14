# Quiz logic cases

Each row is an individually executed case. PASS means the current implementation passed its assertions; fault IDs name experiments in which that same case failed.

| Case | Requirement / location | Baseline | Detected faults |
|---|---|---|---|
| the complete browser script parses | tests/quiz.test.js | PASS | JS-M001 |
| the bank has 35 distinct questions and valid choice indexes | tests/quiz.test.js | PASS | JS-M002, JS-M003 |
| all correct answers score 35/35 with no missing or critical errors | tests/quiz.test.js | PASS | JS-M002, JS-M004, JS-M017, JS-M018 |
| exactly 80 percent passes when critical answers are correct | tests/quiz.test.js | PASS | JS-M002, JS-M004, JS-M005, JS-M006, JS-M016 |
| one more noncritical error falls below the pass threshold | tests/quiz.test.js | PASS | JS-M002, JS-M004, JS-M005, JS-M007, JS-M016 |
| critical question 15 prevents passing even at 97 percent | tests/quiz.test.js | PASS | JS-M002, JS-M003, JS-M004, JS-M005, JS-M008, JS-M013, JS-M016 |
| critical question 17 prevents passing even at 97 percent | tests/quiz.test.js | PASS | JS-M002, JS-M003, JS-M004, JS-M005, JS-M008, JS-M013, JS-M016 |
| critical question 21 prevents passing even at 97 percent | tests/quiz.test.js | PASS | JS-M002, JS-M003, JS-M004, JS-M005, JS-M008, JS-M013, JS-M016 |
| absent answer counts as missing, never as correct | tests/quiz.test.js | PASS | JS-M009, JS-M012 |
| null answer counts as missing, never as correct | tests/quiz.test.js | PASS | JS-M009, JS-M012 |
| string answer counts as missing, never as correct | tests/quiz.test.js | PASS | JS-M009, JS-M012 |
| boolean answer counts as missing, never as correct | tests/quiz.test.js | PASS | JS-M009, JS-M012 |
| negative answer counts as missing, never as correct | tests/quiz.test.js | PASS | JS-M009, JS-M010 |
| too large answer counts as missing, never as correct | tests/quiz.test.js | PASS | JS-M009, JS-M011 |
| fraction answer counts as missing, never as correct | tests/quiz.test.js | PASS | JS-M009, JS-M012 |
| NaN answer counts as missing, never as correct | tests/quiz.test.js | PASS | JS-M009, JS-M012 |
| empty attempts cannot pass and unknown questions reject | tests/quiz.test.js | PASS | JS-M013, JS-M014 |
| retry scoring uses the selected questions rather than the full bank | tests/quiz.test.js | PASS | JS-M002, JS-M004, JS-M015 |
| valid partial saved answers restore and validation does not mutate them | tests/quiz.test.js | PASS | JS-M002, JS-M019, JS-M035 |
| submitted saved attempts require an answer to every selected question | tests/quiz.test.js | PASS | JS-M002, JS-M019, JS-M020, JS-M032 |
| saved state rejects empty ids | tests/quiz.test.js | PASS | JS-M020, JS-M021 |
| saved state rejects duplicate ids | tests/quiz.test.js | PASS | JS-M020, JS-M022 |
| saved state rejects unknown id | tests/quiz.test.js | PASS | JS-M020, JS-M023 |
| saved state rejects missing answers | tests/quiz.test.js | PASS | JS-M020, JS-M024 |
| saved state rejects invalid answer | tests/quiz.test.js | PASS | JS-M020, JS-M030, JS-M031, JS-M035 |
| saved state rejects missing order | tests/quiz.test.js | PASS | JS-M020, JS-M026 |
| saved state rejects short permutation | tests/quiz.test.js | PASS | JS-M020 |
| saved state rejects long permutation | tests/quiz.test.js | PASS | JS-M020, JS-M027 |
| saved state rejects duplicate choice | tests/quiz.test.js | PASS | JS-M020, JS-M028 |
| saved state rejects out of range choice | tests/quiz.test.js | PASS | JS-M020, JS-M029 |
| saved state rejects fractional choice | tests/quiz.test.js | PASS | JS-M020, JS-M030 |
| absent or unparsable saved-state shape cannot restore | tests/quiz.test.js | PASS | JS-M020 |
| shuffling preserves choices and uses the injected random source | tests/quiz.test.js | PASS | JS-M033, JS-M034 |
| one missing answer blocks an otherwise correct attempt | tests/quiz.test.js | PASS | JS-M002, JS-M004, JS-M009, JS-M012, JS-M013 |
| all wrong answers populate every error and topic total | tests/quiz.test.js | PASS | JS-M002, JS-M003, JS-M005, JS-M016, JS-M017 |
| saved state rejects an answer array that loses progress after saving | tests/quiz.test.js | PASS | JS-M020, JS-M024, JS-M025 |
| wrong answers must not modify the caller answer map | tests/quiz.test.js | PASS | JS-M002, JS-M016 |
| saved state rejects empty answer arrays before any reload | tests/quiz.test.js | PASS | JS-M020, JS-M024, JS-M025 |
| saved state rejects dense answer arrays before any reload | tests/quiz.test.js | PASS | JS-M020, JS-M024, JS-M025 |
| saved state rejects sparse answer arrays before any reload | tests/quiz.test.js | PASS | JS-M020, JS-M024, JS-M025 |
| valid answer objects preserve exact progress across repeated JSON reloads | tests/quiz.test.js | PASS | JS-M002, JS-M019, JS-M035 |
| ordinary object state restores across JavaScript execution contexts | tests/quiz.test.js | PASS | JS-M002, JS-M019 |

[Fault catalogue](fault-catalogue.md) · [Audit report](../case-effectiveness-audit.md)
