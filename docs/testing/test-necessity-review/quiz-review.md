# Quiz test and fault necessity review

Reviewed2026-10-12. Read-only review; no runtime reruns or application/test/tool changes. All42 JS cases,35 JS faults,16 browser cases and16 browser faults assessed individually.

KEEP preserves a distinct contract; MERGE preserves its expectations in a shared case/catalogue; IMPROVE repairs evidence attribution or clarifies requirement. No unconditional whole-case removals recommended.

JavaScript evidence hashes match current HTML/tests. Browser artifact lacks hashes; matching names and mutations cannot prove current-source run identity.

## Findings

- JS-C38 repeats JS-C36 empty-array rejection. JS-C41 repeats JSON serialization three times without invoking application persistence. Merge those assertions; keep dense/sparse arrays and actual browser reload independently.
- JS-C01 uniquely compiles the full script in the offline Node suite; its top-level VM extraction excludes UI code. Keep this cheap UI syntax gate, complementary to real browser execution. Browser availability/version preflight does not compile the product. Hardcoded35/140 and ordering are editorial contracts rather than universal scoring requirements. Every scoring fixture assumes correct index0.
- JS-F30 globally disables both permutation and answer integer checks; JS-F29 similarly disables two bounds checks. JS-F13 removes missing/critical gates alongside empty guard. JS-F03 changes all three critical flags. These are composite faults requiring narrower attribution.
- JS-C27 cannot isolate length checking because three choices also violate distinct count. Its broad all-accepted kill is not proof each guard matters independently.
- BR-F14 still completes the quiz and fails only generic no-pageerrors check. BR-F12 aborts initialization. Valid containment evidence, but do not call either a precise completion/scoring fault. BR-C16 proves print invocation, not print layout.
- All35 JS transforms change current source; none yield byte-identical transformed copies. This rules out literal duplicates only. Same kill sets never justify removal by themselves. Pure logic and browser layers generally protect complementary paths.

## Individual decisions

### JS-C01 — KEEP: the complete browser script parses

Requirement: Whole script compiles.

Expectation: Whole script compiles.

Assessment: This is the offline Node suite’s only full-script compilation check. Top-level VM evaluation stops at the UI boundary, so a syntax defect in UI code can otherwise escape the pure-logic suite. The cheap syntax gate complements actual browser execution; browser availability/version preflight does not compile the product.

Overlap IDs: BR-C01, BR-C02, BR-C03, BR-C04, BR-C05, BR-C06, BR-C07, BR-C08, BR-C09, BR-C10, BR-C11, BR-C12, BR-C13, BR-C14, BR-C15, BR-C16

Source: tests/quiz.test.js:21, quizzes/sprint-0-quiz.html:83

### JS-C02 — IMPROVE: the bank has 35 distinct questions and valid choice indexes

Requirement: IDs1–35 in order; four distinct choices, integer correct0–3, nonempty text, critical IDs15,17,21.

Expectation: IDs1–35 in order; four distinct choices, integer correct0–3, nonempty text, critical IDs15,17,21.

Assessment: Real bank invariants matter; exact35/ordering/critical IDs are editorial contract. Generic scoring fixtures assume every correct index0; document content contract and distinguish maintenance coupling.

Overlap IDs: BR-C01

Source: tests/quiz.test.js:25, quizzes/sprint-0-quiz.html:83

### JS-C03 — KEEP: all correct answers score 35/35 with no missing or critical errors

Requirement: 35/35,100%,pass; empty missing/missed/critical lists; Workspace2/2.

Expectation: 35/35,100%,pass; empty missing/missed/critical lists; Workspace2/2.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: BR-C05

Source: tests/quiz.test.js:36, quizzes/sprint-0-quiz.html:83

### JS-C04 — KEEP: exactly 80 percent passes when critical answers are correct

Requirement: 28/35,80%,pass; missed IDs1–7.

Expectation: 28/35,80%,pass; missed IDs1–7.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:46, quizzes/sprint-0-quiz.html:83

### JS-C05 — KEEP: one more noncritical error falls below the pass threshold

Requirement: 27/35,77%,fail.

Expectation: 27/35,77%,fail.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:56, quizzes/sprint-0-quiz.html:83

### JS-C06 — KEEP: critical question 15 prevents passing even at 97 percent

Requirement: Wrong critical ID15 yields97%,fail,criticalMissed=[15].

Expectation: Wrong critical ID15 yields97%,fail,criticalMissed=[15].

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: JS-C07, JS-C08, BR-C15

Source: tests/quiz.test.js:66, quizzes/sprint-0-quiz.html:83

### JS-C07 — KEEP: critical question 17 prevents passing even at 97 percent

Requirement: Wrong critical ID17 yields97%,fail,criticalMissed=[17].

Expectation: Wrong critical ID17 yields97%,fail,criticalMissed=[17].

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: JS-C06, JS-C08, BR-C15

Source: tests/quiz.test.js:66, quizzes/sprint-0-quiz.html:83

### JS-C08 — KEEP: critical question 21 prevents passing even at 97 percent

Requirement: Wrong critical ID21 yields97%,fail,criticalMissed=[21].

Expectation: Wrong critical ID21 yields97%,fail,criticalMissed=[21].

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: JS-C06, JS-C07, BR-C15

Source: tests/quiz.test.js:66, quizzes/sprint-0-quiz.html:83

### JS-C09 — KEEP: absent answer counts as missing, never as correct

Requirement: undefined yields missing=[1],correct0,pass=false.

Expectation: undefined yields missing=[1],correct0,pass=false.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:78, quizzes/sprint-0-quiz.html:83

### JS-C10 — KEEP: null answer counts as missing, never as correct

Requirement: null yields missing=[1],correct0,pass=false.

Expectation: null yields missing=[1],correct0,pass=false.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:78, quizzes/sprint-0-quiz.html:83

### JS-C11 — KEEP: string answer counts as missing, never as correct

Requirement: string0 yields missing=[1],correct0,pass=false.

Expectation: string0 yields missing=[1],correct0,pass=false.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:78, quizzes/sprint-0-quiz.html:83

### JS-C12 — KEEP: boolean answer counts as missing, never as correct

Requirement: true yields missing=[1],correct0,pass=false.

Expectation: true yields missing=[1],correct0,pass=false.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:78, quizzes/sprint-0-quiz.html:83

### JS-C13 — KEEP: negative answer counts as missing, never as correct

Requirement: -1 yields missing=[1],correct0,pass=false.

Expectation: -1 yields missing=[1],correct0,pass=false.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:78, quizzes/sprint-0-quiz.html:83

### JS-C14 — KEEP: too large answer counts as missing, never as correct

Requirement: 4 yields missing=[1],correct0,pass=false.

Expectation: 4 yields missing=[1],correct0,pass=false.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:78, quizzes/sprint-0-quiz.html:83

### JS-C15 — KEEP: fraction answer counts as missing, never as correct

Requirement: 1.5 yields missing=[1],correct0,pass=false.

Expectation: 1.5 yields missing=[1],correct0,pass=false.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:78, quizzes/sprint-0-quiz.html:83

### JS-C16 — KEEP: NaN answer counts as missing, never as correct

Requirement: NaN yields missing=[1],correct0,pass=false.

Expectation: NaN yields missing=[1],correct0,pass=false.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:78, quizzes/sprint-0-quiz.html:83

### JS-C17 — IMPROVE: empty attempts cannot pass and unknown questions reject

Requirement: Empty attempt fails; unknown999 throws Unknown question.

Expectation: Empty attempt fails; unknown999 throws Unknown question.

Assessment: Split two independent negative contracts for case-level proof.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:86, quizzes/sprint-0-quiz.html:83

### JS-C18 — KEEP: retry scoring uses the selected questions rather than the full bank

Requirement: IDs1,2 yield2/2,100%; input unchanged.

Expectation: IDs1,2 yield2/2,100%; input unchanged.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: BR-C08

Source: tests/quiz.test.js:91, quizzes/sprint-0-quiz.html:83

### JS-C19 — KEEP: valid partial saved answers restore and validation does not mutate them

Requirement: Valid partial state accepts without mutation.

Expectation: Valid partial state accepts without mutation.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: JS-C41, JS-C42, BR-C04

Source: tests/quiz.test.js:100, quizzes/sprint-0-quiz.html:84

### JS-C20 — KEEP: submitted saved attempts require an answer to every selected question

Requirement: Incomplete submitted cache rejects; adding answer2 accepts.

Expectation: Incomplete submitted cache rejects; adding answer2 accepts.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: BR-C11

Source: tests/quiz.test.js:107, quizzes/sprint-0-quiz.html:84

### JS-C21 — KEEP: saved state rejects empty ids

Requirement: Saved state rejects empty IDs.

Expectation: Saved state rejects empty IDs.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:128, quizzes/sprint-0-quiz.html:84

### JS-C22 — KEEP: saved state rejects duplicate ids

Requirement: Saved state rejects duplicate IDs.

Expectation: Saved state rejects duplicate IDs.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:128, quizzes/sprint-0-quiz.html:84

### JS-C23 — KEEP: saved state rejects unknown id

Requirement: Saved state rejects unknown999.

Expectation: Saved state rejects unknown999.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:128, quizzes/sprint-0-quiz.html:84

### JS-C24 — KEEP: saved state rejects missing answers

Requirement: Saved state rejects absent answers.

Expectation: Saved state rejects absent answers.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:128, quizzes/sprint-0-quiz.html:84

### JS-C25 — KEEP: saved state rejects invalid answer

Requirement: Saved state rejects string answer0.

Expectation: Saved state rejects string answer0.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: JS-C11

Source: tests/quiz.test.js:128, quizzes/sprint-0-quiz.html:84

### JS-C26 — KEEP: saved state rejects missing order

Requirement: Saved state rejects absent order.

Expectation: Saved state rejects absent order.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:128, quizzes/sprint-0-quiz.html:84

### JS-C27 — IMPROVE: saved state rejects short permutation

Requirement: Saved state rejects three choices.

Expectation: Saved state rejects three choices.

Assessment: Three choices fail distinct-count too; length-removal fault does not kill this case. Do not claim independent length guard proof.

Overlap IDs: JS-C28, JS-C29

Source: tests/quiz.test.js:128, quizzes/sprint-0-quiz.html:84

### JS-C28 — KEEP: saved state rejects long permutation

Requirement: Saved state rejects five choices.

Expectation: Saved state rejects five choices.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: JS-C27, JS-C29

Source: tests/quiz.test.js:128, quizzes/sprint-0-quiz.html:84

### JS-C29 — KEEP: saved state rejects duplicate choice

Requirement: Saved state rejects duplicate choice2.

Expectation: Saved state rejects duplicate choice2.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: JS-C27, JS-C28

Source: tests/quiz.test.js:128, quizzes/sprint-0-quiz.html:84

### JS-C30 — KEEP: saved state rejects out of range choice

Requirement: Saved state rejects out-of-range4.

Expectation: Saved state rejects out-of-range4.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:128, quizzes/sprint-0-quiz.html:84

### JS-C31 — KEEP: saved state rejects fractional choice

Requirement: Saved state rejects fractional2.5.

Expectation: Saved state rejects fractional2.5.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:128, quizzes/sprint-0-quiz.html:84

### JS-C32 — KEEP: absent or unparsable saved-state shape cannot restore

Requirement: Reject null,undefined,{},string,array top-level states.

Expectation: Reject null,undefined,{},string,array top-level states.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:135, quizzes/sprint-0-quiz.html:84

### JS-C33 — IMPROVE: shuffling preserves choices and uses the injected random source

Requirement: random0 gives[1,2,3,0],three calls; random0.999 gives[0,1,2,3].

Expectation: random0 gives[1,2,3,0],three calls; random0.999 gives[0,1,2,3].

Assessment: Exact shuffle sequence/three calls pins Fisher–Yates; retain permutation/random-source contract and document algorithm requirement.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:139, quizzes/sprint-0-quiz.html:82

### JS-C34 — KEEP: one missing answer blocks an otherwise correct attempt

Requirement: Missing1 yields34 correct,fail,missing=[1].

Expectation: Missing1 yields34 correct,fail,missing=[1].

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:147, quizzes/sprint-0-quiz.html:83

### JS-C35 — KEEP: all wrong answers populate every error and topic total

Requirement: All wrong yields0%,fail,all IDs missed,critical15,17,21,no missing; every topic correct0 and correct total.

Expectation: All wrong yields0%,fail,all IDs missed,critical15,17,21,no missing; every topic correct0 and correct total.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: None identified beyond generic harness overlap.

Source: tests/quiz.test.js:157, quizzes/sprint-0-quiz.html:83

### JS-C36 — KEEP: saved state rejects an answer array that loses progress after saving

Requirement: Array answer1 serializes[null,0]; persisted and original empty arrays reject.

Expectation: Array answer1 serializes[null,0]; persisted and original empty arrays reject.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: JS-C38, JS-C39, JS-C40, BR-C13

Source: tests/quiz.test.js:175, quizzes/sprint-0-quiz.html:84

### JS-C37 — KEEP: wrong answers must not modify the caller answer map

Requirement: Wrong-answer map unchanged after grading.

Expectation: Wrong-answer map unchanged after grading.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: JS-C04, JS-C05, JS-C35

Source: tests/quiz.test.js:186, quizzes/sprint-0-quiz.html:83

### JS-C38 — MERGE: saved state rejects empty answer arrays before any reload

Requirement: Empty answer array rejects before reload.

Expectation: Empty answer array rejects before reload.

Assessment: Exact empty-array rejection already asserted by JS-C36; retain that expectation there.

Overlap IDs: JS-C36

Source: tests/quiz.test.js:194, quizzes/sprint-0-quiz.html:84

### JS-C39 — KEEP: saved state rejects dense answer arrays before any reload

Requirement: Dense[0,1] answer array rejects before reload.

Expectation: Dense[0,1] answer array rejects before reload.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: JS-C36, JS-C38, JS-C40, BR-C13

Source: tests/quiz.test.js:194, quizzes/sprint-0-quiz.html:84

### JS-C40 — KEEP: saved state rejects sparse answer arrays before any reload

Requirement: Sparse answer1=0 array rejects before reload.

Expectation: Sparse answer1=0 array rejects before reload.

Assessment: Distinct input shape, type, boundary or transition can fail independently despite shared mutation kills. Preserve exact assertion.

Overlap IDs: JS-C36, JS-C38, JS-C39, BR-C13

Source: tests/quiz.test.js:194, quizzes/sprint-0-quiz.html:84

### JS-C41 — MERGE: valid answer objects preserve exact progress across repeated JSON reloads

Requirement: Empty object accepts; answers1=0,2=3 preserve equality/validity through three JSON roundtrips.

Expectation: Empty object accepts; answers1=0,2=3 preserve equality/validity through three JSON roundtrips.

Assessment: Three repeated JSON roundtrips exercise no application persistence. Merge one object compatibility fixture into JS-C19/42; BR-C04 proves actual reload.

Overlap IDs: JS-C19, JS-C42, BR-C04

Source: tests/quiz.test.js:201, quizzes/sprint-0-quiz.html:84

### JS-C42 — KEEP: ordinary object state restores across JavaScript execution contexts

Requirement: Fresh-VM validator accepts caller-realm JSON object.

Expectation: Fresh-VM validator accepts caller-realm JSON object.

Assessment: Cross-realm compatibility prevents instanceof/prototype identity rejection; necessary harness/API contract, not actual persistence proof.

Overlap IDs: JS-C19, JS-C41

Source: tests/quiz.test.js:215, quizzes/sprint-0-quiz.html:84

### JS-F01 — KEEP: script-syntax-error

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C01

Assessment: The isolated UI syntax mutation proves the offline full-script compile gate detects syntax defects beyond the pure-logic extraction boundary. Browser execution provides complementary coverage.

Overlap IDs: JS-C01

Source: tools/audit_quiz_cases.py:16, quizzes/sprint-0-quiz.html:98

Mutation: `render();if(submitted)showResults(false);` → `render(;if(submitted)showResults(false);`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F02 — KEEP: bank-duplicate-id

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C02,JS-C03,JS-C04,JS-C05,JS-C06,JS-C07,JS-C08,JS-C18,JS-C19,JS-C20,JS-C34,JS-C35,JS-C37,JS-C41,JS-C42

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:17, quizzes/sprint-0-quiz.html:79

Mutation: `"id": 2,` → `"id": 1,`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F03 — IMPROVE: bank-critical-removed

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C02,JS-C06,JS-C07,JS-C08,JS-C35

Assessment: All three critical flags change together; inject each separately before claiming per-ID fault effectiveness.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:18, quizzes/sprint-0-quiz.html:79

Mutation: `"critical": true` → `"critical": false`. Matches: 3. Changes source: True. Historical status: DETECTED.

### JS-F04 — KEEP: answers-always-wrong

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C03,JS-C04,JS-C05,JS-C06,JS-C07,JS-C08,JS-C18,JS-C34

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:19, quizzes/sprint-0-quiz.html:83

Mutation: `answers[id]===q.correct` → `false`. Matches: 2. Changes source: True. Historical status: DETECTED.

### JS-F05 — KEEP: answers-always-correct

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C04,JS-C05,JS-C06,JS-C07,JS-C08,JS-C35

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:20, quizzes/sprint-0-quiz.html:83

Mutation: `answers[id]===q.correct` → `true`. Matches: 2. Changes source: True. Historical status: DETECTED.

### JS-F06 — KEEP: threshold-too-strict

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C04

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:21, quizzes/sprint-0-quiz.html:83

Mutation: `correct/ids.length>=.8` → `correct/ids.length>.8`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F07 — KEEP: threshold-too-permissive

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C05

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:22, quizzes/sprint-0-quiz.html:83

Mutation: `correct/ids.length>=.8` → `correct/ids.length>=.7`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F08 — KEEP: critical-errors-ignored

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C06,JS-C07,JS-C08

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:23, quizzes/sprint-0-quiz.html:83

Mutation: `criticalMissed.length===0` → `true`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F09 — IMPROVE: invalid-answers-accepted

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C09,JS-C10,JS-C11,JS-C12,JS-C13,JS-C14,JS-C15,JS-C16,JS-C34

Assessment: Broad sabotage proves harness reachability; narrower existing guards and assertions should carry independent necessity proof.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:24, quizzes/sprint-0-quiz.html:83

Mutation: `!Number.isInteger(answers[id])||answers[id]<0||answers[id]>3` → `false`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F10 — KEEP: negative-answer-accepted

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C13

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:25, quizzes/sprint-0-quiz.html:83

Mutation: `answers[id]<0` → `false`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F11 — KEEP: too-large-answer-accepted

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C14

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:26, quizzes/sprint-0-quiz.html:83

Mutation: `answers[id]>3` → `false`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F12 — KEEP: integer-check-removed

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C09,JS-C10,JS-C11,JS-C12,JS-C15,JS-C16,JS-C34

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:27, quizzes/sprint-0-quiz.html:83

Mutation: `!Number.isInteger(answers[id])` → `false`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F13 — IMPROVE: empty-attempt-passes

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C06,JS-C07,JS-C08,JS-C17,JS-C34

Assessment: Also removes missing-answer and critical gates; their kills do not independently prove empty-attempt guard. Mutate empty condition alone.

Overlap IDs: JS-F08, JS-C34

Source: tools/audit_quiz_cases.py:28, quizzes/sprint-0-quiz.html:83

Mutation: `ids.length>0&&missing.length===0&&correct/ids.length>=.8&&criticalMissed.length===0` → `ids.length===0||correct/ids.length>=.8`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F14 — KEEP: unknown-question-ignored

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C17

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:29, quizzes/sprint-0-quiz.html:83

Mutation: `if(!q)throw new Error('Unknown question');` → `if(!q)continue;`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F15 — KEEP: full-bank-denominator

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C18

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:30, quizzes/sprint-0-quiz.html:83

Mutation: `total:ids.length` → `total:QUESTIONS.length`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F16 — KEEP: caller-answers-overwritten

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C04,JS-C05,JS-C06,JS-C07,JS-C08,JS-C35,JS-C37

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:31, quizzes/sprint-0-quiz.html:83

Mutation: `const ok=answers[id]===q.correct;` → `answers[id]=q.correct;const ok=answers[id]===q.correct;`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F17 — KEEP: topic-totals-not-counted

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C03,JS-C35

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:32, quizzes/sprint-0-quiz.html:83

Mutation: `topics[q.topic].total++` → `topics[q.topic].total+=0`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F18 — KEEP: topic-correct-not-counted

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C03

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:33, quizzes/sprint-0-quiz.html:83

Mutation: `topics[q.topic].correct+=ok?1:0` → `topics[q.topic].correct+=0`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F19 — IMPROVE: saved-states-all-rejected

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C19,JS-C20,JS-C41,JS-C42

Assessment: Broad sabotage proves harness reachability; narrower existing guards and assertions should carry independent necessity proof.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:34, quizzes/sprint-0-quiz.html:84

Mutation: `function validSaved(saved){` → `function validSaved(saved){return false;`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F20 — IMPROVE: saved-states-all-accepted

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C20,JS-C21,JS-C22,JS-C23,JS-C24,JS-C25,JS-C26,JS-C27,JS-C28,JS-C29,JS-C30,JS-C31,JS-C32,JS-C36,JS-C38,JS-C39,JS-C40

Assessment: Broad sabotage proves harness reachability; narrower existing guards and assertions should carry independent necessity proof.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:35, quizzes/sprint-0-quiz.html:84

Mutation: `function validSaved(saved){` → `function validSaved(saved){return true;`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F21 — KEEP: empty-ids-accepted

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C21

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:36, quizzes/sprint-0-quiz.html:84

Mutation: `!saved.ids.length` → `false`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F22 — KEEP: duplicate-ids-accepted

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C22

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:37, quizzes/sprint-0-quiz.html:84

Mutation: `new Set(saved.ids).size!==saved.ids.length` → `false`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F23 — KEEP: unknown-ids-accepted

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C23

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:38, quizzes/sprint-0-quiz.html:84

Mutation: `saved.ids.some(id=>!ids.has(id))` → `false`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F24 — IMPROVE: answers-not-required

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C24,JS-C36,JS-C38,JS-C39,JS-C40

Assessment: Broad sabotage proves harness reachability; narrower existing guards and assertions should carry independent necessity proof.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:39, quizzes/sprint-0-quiz.html:84

Mutation: `!saved.answers||typeof saved.answers!=='object'||Array.isArray(saved.answers)` → `false`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F25 — KEEP: answer-arrays-accepted

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C36,JS-C38,JS-C39,JS-C40

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:40, quizzes/sprint-0-quiz.html:84

Mutation: `Array.isArray(saved.answers)` → `false`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F26 — KEEP: order-not-required

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C26

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:41, quizzes/sprint-0-quiz.html:84

Mutation: `!saved.order||typeof saved.order!=='object'` → `false`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F27 — KEEP: permutation-length-ignored

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C28

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:42, quizzes/sprint-0-quiz.html:84

Mutation: `saved.order[id].length===4` → `true`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F28 — KEEP: permutation-duplicates-ignored

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C29

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:43, quizzes/sprint-0-quiz.html:84

Mutation: `new Set(saved.order[id]).size===4` → `true`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F29 — IMPROVE: permutation-bounds-ignored

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C30

Assessment: Global replacement changes bounds in both permutation and saved answers. Scope responsible permutation callback.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:44, quizzes/sprint-0-quiz.html:84

Mutation: `v>=0&&v<=3` → `true`. Matches: 2. Changes source: True. Historical status: DETECTED.

### JS-F30 — IMPROVE: permutation-integers-ignored

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C25,JS-C31

Assessment: Global replacement changes BOTH permutation and saved-answer integer validation. JS-C25 detection is collateral. Scope permutation site; JS-F31 covers answer values.

Overlap IDs: JS-F31

Source: tools/audit_quiz_cases.py:45, quizzes/sprint-0-quiz.html:84

Mutation: `Number.isInteger(v)` → `true`. Matches: 2. Changes source: True. Historical status: DETECTED.

### JS-F31 — KEEP: saved-answer-types-ignored

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C25

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:46, quizzes/sprint-0-quiz.html:84

Mutation: `Object.values(saved.answers).every(v=>Number.isInteger(v)&&v>=0&&v<=3)` → `true`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F32 — KEEP: partial-submitted-cache-accepted

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C20

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:47, quizzes/sprint-0-quiz.html:84

Mutation: `if(saved.submitted===true&&saved.ids.some(id=>!Object.hasOwn(saved.answers,id)))return false;` → ``. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F33 — KEEP: shuffle-disabled

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C33

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:48, quizzes/sprint-0-quiz.html:82

Mutation: `const j=Math.floor(random()*(i+1))` → `const j=i`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F34 — KEEP: shuffle-loses-choice

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C33

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:49, quizzes/sprint-0-quiz.html:82

Mutation: `return a;}` → `return [0,0,2,3];}`. Matches: 1. Changes source: True. Historical status: DETECTED.

### JS-F35 — KEEP: partial-saved-state-modified

Requirement: Preserve expectations in each named detecting case.

Expectation: Reject altered behavior in JS-C19,JS-C25,JS-C41

Assessment: Transform changes responsible code and named cases observe a contract violation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_cases.py:50, quizzes/sprint-0-quiz.html:84

Mutation: `return saved.ids.every` → `saved.answers[1]=3;return saved.ids.every`. Matches: 1. Changes source: True. Historical status: DETECTED.

### BR-C01 — IMPROVE: fresh quiz renders 35 questions and 140 choices

Requirement: fresh quiz renders 35 questions and 140 choices

Expectation: check:async p=>{assert.equal(await count(p),35);assert.equal(await p.locator('input[type=radio]').count(),140);assert.match(await p.locator('#progress-label').innerText(),/^0 \/ 35 answered/);}},

Assessment: Rendering invariant matters;35/140 couples to content edits. Separate editorial count from generic per-question rendering.

Overlap IDs: JS-C02

Source: tools/audit_quiz_browser.mjs:21, quizzes/sprint-0-quiz.html:92

### BR-F01 — KEEP: fresh quiz renders 35 questions and 140 choices

Requirement: fresh quiz renders 35 questions and 140 choices

Expectation: BR-C01 rejects altered contract.

Assessment: Recorded failure observes concrete output/control violation caused by responsible UI mutation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:21, quizzes/sprint-0-quiz.html:92

Mutation: `for(const [number,id] of ids.entries())` → `for(const [number,id] of ids.slice(1).entries())`. Matches: 1. Changes source: True. Historical status: DETECTED.

Recorded failure: Expected values to be strictly equal:  34 !== 35 

### BR-C02 — KEEP: missing answers block results and focus the first missing question

Requirement: missing answers block results and focus the first missing question

Expectation: check:async p=>{await submit(p);assert.equal(await visibleResults(p),false);assert.match(await p.locator('#notice').innerText(),/remaining 35/);assert.equal(await p.evaluate(()=>document.activeElement.name),'q1');assert.equal((await state(p)).submitted,false);}},

Assessment: Actual DOM, events, storage and control-state integration complement pure-logic coverage.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:23, quizzes/sprint-0-quiz.html:93

### BR-F02 — KEEP: missing answers block results and focus the first missing question

Requirement: missing answers block results and focus the first missing question

Expectation: BR-C02 rejects altered contract.

Assessment: Recorded failure observes concrete output/control violation caused by responsible UI mutation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:23, quizzes/sprint-0-quiz.html:93

Mutation: `if(lastGrade.missing.length){` → `if(false){`. Matches: 1. Changes source: True. Historical status: DETECTED.

Recorded failure: Expected values to be strictly equal:  true !== false 

### BR-C03 — KEEP: radio change updates progress and saves the exact answer

Requirement: radio change updates progress and saves the exact answer

Expectation: check:async p=>{await p.locator('#question-1 input[value="2"]').check();assert.equal((await state(p)).answers[1],2);assert.match(await p.locator('#progress-label').innerText(),/^1 \/ 35/);}},

Assessment: Actual DOM, events, storage and control-state integration complement pure-logic coverage.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:25, quizzes/sprint-0-quiz.html:92

### BR-F03 — KEEP: radio change updates progress and saves the exact answer

Requirement: radio change updates progress and saves the exact answer

Expectation: BR-C03 rejects altered contract.

Assessment: Recorded failure observes concrete output/control violation caused by responsible UI mutation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:25, quizzes/sprint-0-quiz.html:92

Mutation: `answers[id]=index;` → `answers[id]=0;`. Matches: 1. Changes source: True. Historical status: DETECTED.

Recorded failure: Expected values to be strictly equal:  0 !== 2 

### BR-C04 — KEEP: partial progress and choice order survive reload

Requirement: partial progress and choice order survive reload

Expectation: check:async p=>{assert.equal(await count(p),2);assert.equal(await p.locator('#question-1 input[value="0"]').isChecked(),true);assert.deepEqual(await p.locator('#question-2 input').evaluateAll(ns=>ns.map(n=>Number(n.value))),[3,2,1,0]);await p.locator('#question-2 input[value="2"]').check();await p.reload();assert.equal(await p.locator('#question-2 input[value="2"]').isChecked(),true);assert.match(await p.locator('#progress-label').innerText(),/^2 \/ 2/);}},

Assessment: Actual DOM, events, storage and control-state integration complement pure-logic coverage.

Overlap IDs: JS-C19, JS-C41

Source: tools/audit_quiz_browser.mjs:27, quizzes/sprint-0-quiz.html:92

### BR-F04 — KEEP: partial progress and choice order survive reload

Requirement: partial progress and choice order survive reload

Expectation: BR-C04 rejects altered contract.

Assessment: Recorded failure observes concrete output/control violation caused by responsible UI mutation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:27, quizzes/sprint-0-quiz.html:92

Mutation: `input.checked=answers[id]===index;` → `input.checked=false;`. Matches: 1. Changes source: True. Historical status: DETECTED.

Recorded failure: Expected values to be strictly equal:  false !== true 

### BR-C05 — KEEP: all correct answers show honest score and lock controls

Requirement: all correct answers show honest score and lock controls

Expectation: check:async p=>{await submit(p);assert.equal(await visibleResults(p),true);assert.match(await p.locator('#score').innerText(),/^35 \/ 35 · 100%$/);assert.match(await p.locator('#result-message').innerText(),/does not certify full Sprint 0 completion/);assert.equal(await p.locator('input:disabled').count(),140);assert.equal(await p.locator('#submit').isDisabled(),true);assert.equal(await p.locator('#retry').isDisabled(),true);assert.equal(await p.locator('.feedback').count(),35);}},

Assessment: Actual DOM, events, storage and control-state integration complement pure-logic coverage.

Overlap IDs: JS-C03

Source: tools/audit_quiz_browser.mjs:29, quizzes/sprint-0-quiz.html:93

### BR-F05 — KEEP: all correct answers show honest score and lock controls

Requirement: all correct answers show honest score and lock controls

Expectation: BR-C05 rejects altered contract.

Assessment: Recorded failure observes concrete output/control violation caused by responsible UI mutation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:29, quizzes/sprint-0-quiz.html:93

Mutation: `box.querySelectorAll('input').forEach(n=>n.disabled=true);` → ``. Matches: 1. Changes source: True. Historical status: DETECTED.

Recorded failure: Expected values to be strictly equal:  0 !== 140 

### BR-C06 — KEEP: double submission never duplicates feedback

Requirement: double submission never duplicates feedback

Expectation: check:async p=>{await submit(p);await p.locator('#quiz').evaluate(form=>form.dispatchEvent(new Event('submit',{bubbles:true,cancelable:true})));assert.equal(await p.locator('.feedback').count(),35);}},

Assessment: Actual DOM, events, storage and control-state integration complement pure-logic coverage.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:31, quizzes/sprint-0-quiz.html:94

### BR-F06 — KEEP: double submission never duplicates feedback

Requirement: double submission never duplicates feedback

Expectation: BR-C06 rejects altered contract.

Assessment: Recorded failure observes concrete output/control violation caused by responsible UI mutation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:31, quizzes/sprint-0-quiz.html:94

Mutation: `if(!submitted)showResults();` → `showResults();`. Matches: 1. Changes source: True. Historical status: DETECTED.

Recorded failure: Expected values to be strictly equal:  70 !== 35 

### BR-C07 — KEEP: retry contains only mistakes and clears previous answers

Requirement: retry contains only mistakes and clears previous answers

Expectation: check:async p=>{await submit(p);await p.locator('#retry').click();assert.equal(await count(p),2);assert.deepEqual((await state(p)).ids,[1,15]);assert.deepEqual((await state(p)).answers,{});assert.equal(await p.locator('input:checked').count(),0);assert.equal(await visibleResults(p),false);assert.equal(await p.locator('#submit').isDisabled(),false);assert.equal((await state(p)).submitted,false);}},

Assessment: Actual DOM, events, storage and control-state integration complement pure-logic coverage.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:33, quizzes/sprint-0-quiz.html:95

### BR-F07 — KEEP: retry contains only mistakes and clears previous answers

Requirement: retry contains only mistakes and clears previous answers

Expectation: BR-C07 rejects altered contract.

Assessment: Recorded failure observes concrete output/control violation caused by responsible UI mutation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:33, quizzes/sprint-0-quiz.html:95

Mutation: `ids=[...lastGrade.missed];` → `ids=QUESTIONS.map(q=>q.id);`. Matches: 1. Changes source: True. Historical status: DETECTED.

Recorded failure: Expected values to be strictly equal:  35 !== 2 

### BR-C08 — KEEP: retry score uses its own denominator and practice wording

Requirement: retry score uses its own denominator and practice wording

Expectation: check:async p=>{await submit(p);await p.locator('#retry').click();await answerAll(p);await submit(p);assert.match(await p.locator('#score').innerText(),/^2 \/ 2 · 100%$/);assert.match(await p.locator('#result-message').innerText(),/^Practice threshold met/);}},

Assessment: Actual DOM, events, storage and control-state integration complement pure-logic coverage.

Overlap IDs: JS-C18

Source: tools/audit_quiz_browser.mjs:35, quizzes/sprint-0-quiz.html:93

### BR-F08 — KEEP: retry score uses its own denominator and practice wording

Requirement: retry score uses its own denominator and practice wording

Expectation: BR-C08 rejects altered contract.

Assessment: Recorded failure observes concrete output/control violation caused by responsible UI mutation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:35, quizzes/sprint-0-quiz.html:93

Mutation: `ids.length<QUESTIONS.length?'Practice threshold met':'Quiz threshold met'` → `'Quiz threshold met'`. Matches: 1. Changes source: True. Historical status: DETECTED.

Recorded failure: The input did not match the regular expression /^Practice threshold met/. Input:  'Quiz threshold met. Explain the reasons in your own words; this does not certify full Sprint 0 completion.' 

### BR-C09 — KEEP: restart restores full bank and clears completed progress

Requirement: restart restores full bank and clears completed progress

Expectation: check:async p=>{await submit(p);await p.locator('#restart').click();assert.equal(await count(p),35);assert.equal(await p.locator('input:checked').count(),0);assert.equal(await p.locator('input:disabled').count(),0);assert.equal(await visibleResults(p),false);assert.equal((await state(p)).submitted,false);}},

Assessment: Actual DOM, events, storage and control-state integration complement pure-logic coverage.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:37, quizzes/sprint-0-quiz.html:96

### BR-F09 — KEEP: restart restores full bank and clears completed progress

Requirement: restart restores full bank and clears completed progress

Expectation: BR-C09 rejects altered contract.

Assessment: Recorded failure observes concrete output/control violation caused by responsible UI mutation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:37, quizzes/sprint-0-quiz.html:96

Mutation: `ids=QUESTIONS.map(q=>q.id);answers={};order={};submitted=false;lastGrade=null;` → `ids=[1];answers={};order={};submitted=false;lastGrade=null;`. Matches: 1. Changes source: True. Historical status: DETECTED.

Recorded failure: Expected values to be strictly equal:  1 !== 35 

### BR-C10 — KEEP: completed attempts restore results after reload

Requirement: completed attempts restore results after reload

Expectation: check:async p=>{assert.equal(await visibleResults(p),true);assert.equal(await p.locator('input:disabled').count(),140);await p.reload();assert.equal(await visibleResults(p),true);assert.equal(await p.locator('.feedback').count(),35);}},

Assessment: Actual DOM, events, storage and control-state integration complement pure-logic coverage.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:39, quizzes/sprint-0-quiz.html:98

### BR-F10 — KEEP: completed attempts restore results after reload

Requirement: completed attempts restore results after reload

Expectation: BR-C10 rejects altered contract.

Assessment: Recorded failure observes concrete output/control violation caused by responsible UI mutation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:39, quizzes/sprint-0-quiz.html:98

Mutation: `if(submitted)showResults(false);` → ``. Matches: 1. Changes source: True. Historical status: DETECTED.

Recorded failure: Expected values to be strictly equal:  false !== true 

### BR-C11 — KEEP: incomplete submitted cache resets and remains usable

Requirement: incomplete submitted cache resets and remains usable

Expectation: check:async p=>{assert.equal(await count(p),35);await answerAll(p);await submit(p);assert.equal(await visibleResults(p),true);assert.match(await p.locator('#score').innerText(),/100%/);}},

Assessment: Actual DOM, events, storage and control-state integration complement pure-logic coverage.

Overlap IDs: JS-C20, JS-F32

Source: tools/audit_quiz_browser.mjs:41, quizzes/sprint-0-quiz.html:84

### BR-F11 — MERGE: incomplete submitted cache resets and remains usable

Requirement: incomplete submitted cache resets and remains usable

Expectation: BR-C11 rejects altered contract.

Assessment: Duplicate underlying validation mutation at JS layer; share fault catalogue entry while preserving distinct browser integration application.

Overlap IDs: JS-F32

Source: tools/audit_quiz_browser.mjs:41, quizzes/sprint-0-quiz.html:84

Mutation: `if(saved.submitted===true&&saved.ids.some(id=>!Object.hasOwn(saved.answers,id)))return false;` → ``. Matches: 1. Changes source: True. Historical status: DETECTED.

Recorded failure: Expected values to be strictly equal:  2 !== 35 

### BR-C12 — KEEP: malformed cache resets without script errors

Requirement: malformed cache resets without script errors

Expectation: check:async p=>{assert.equal(await count(p),35);await p.locator('#question-1 input[value="1"]').check();assert.equal((await state(p)).answers[1],1);}},

Assessment: Actual DOM, events, storage and control-state integration complement pure-logic coverage.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:43, quizzes/sprint-0-quiz.html:88

### BR-F12 — IMPROVE: malformed cache resets without script errors

Requirement: malformed cache resets without script errors

Expectation: BR-C12 rejects altered contract.

Assessment: Throw in JSON catch aborts initialization:0 versus35 fieldsets and page error. Valid error containment fault but crude crash sabotage; pair with reset failure without crash.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:43, quizzes/sprint-0-quiz.html:88

Mutation: `}catch{}
function save()` → `}catch{throw new Error("cache failure");}
function save()`. Matches: 1. Changes source: True. Historical status: DETECTED.

Recorded failure: Expected values to be strictly equal:  0 !== 35 

### BR-C13 — KEEP: array answer cache resets rather than silently losing progress

Requirement: array answer cache resets rather than silently losing progress

Expectation: check:async p=>{assert.equal(await count(p),35);assert.equal(await p.locator('input:checked').count(),0);}},

Assessment: Actual DOM, events, storage and control-state integration complement pure-logic coverage.

Overlap IDs: JS-C36, JS-C38, JS-C39, JS-C40, JS-F25

Source: tools/audit_quiz_browser.mjs:45, quizzes/sprint-0-quiz.html:84

### BR-F13 — MERGE: array answer cache resets rather than silently losing progress

Requirement: array answer cache resets rather than silently losing progress

Expectation: BR-C13 rejects altered contract.

Assessment: Duplicate underlying validation mutation at JS layer; share fault catalogue entry while preserving distinct browser integration application.

Overlap IDs: JS-F25

Source: tools/audit_quiz_browser.mjs:45, quizzes/sprint-0-quiz.html:84

Mutation: `Array.isArray(saved.answers)` → `false`. Matches: 1. Changes source: True. Historical status: DETECTED.

Recorded failure: Expected values to be strictly equal:  2 !== 35 

### BR-C14 — IMPROVE: storage unavailable still allows completing a quiz

Requirement: storage unavailable still allows completing a quiz

Expectation: check:async p=>{assert.equal(await count(p),35);await answerAll(p);await submit(p);assert.equal(await visibleResults(p),true);assert.match(await p.locator('#score').innerText(),/100%/);}},

Assessment: Baseline proves completion with blocked storage. Mutant also completes; generic pageErrors assertion alone kills it. Label containment evidence precisely.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:47, quizzes/sprint-0-quiz.html:89

### BR-F14 — IMPROVE: storage unavailable still allows completing a quiz

Requirement: storage unavailable still allows completing a quiz

Expectation: BR-C14 rejects altered contract.

Assessment: Score/completion checks pass;36 storage failure page errors alone kill mutant. Valid uncaught-error containment proof, not completion failure proof.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:47, quizzes/sprint-0-quiz.html:89

Mutation: `}catch{}}
function el` → `}catch{throw new Error("storage failure");}}
function el`. Matches: 1. Changes source: True. Historical status: DETECTED.

Recorded failure: Expected values to be strictly deep-equal: + actual - expected  + [ +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failure', +   'storage failur

### BR-C15 — KEEP: critical mistake shows warning despite a high score

Requirement: critical mistake shows warning despite a high score

Expectation: check:async p=>{await submit(p);assert.match(await p.locator('#score').innerText(),/97%/);assert.match(await p.locator('#result-message').innerText(),/missed critical secret\/authentication\/storage/);}},

Assessment: Actual DOM, events, storage and control-state integration complement pure-logic coverage.

Overlap IDs: JS-C06, JS-C07, JS-C08

Source: tools/audit_quiz_browser.mjs:49, quizzes/sprint-0-quiz.html:93

### BR-F15 — KEEP: critical mistake shows warning despite a high score

Requirement: critical mistake shows warning despite a high score

Expectation: BR-C15 rejects altered contract.

Assessment: Recorded failure observes concrete output/control violation caused by responsible UI mutation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:49, quizzes/sprint-0-quiz.html:93

Mutation: `lastGrade.criticalMissed.length?' Review the missed critical secret/authentication/storage questions even if the percentage is high.':''` → `''`. Matches: 1. Changes source: True. Historical status: DETECTED.

Recorded failure: The input did not match the regular expression /missed critical secret\/authentication\/storage/. Input:  'Keep practicing. Read the explanations below, then retry the missed questions.' 

### BR-C16 — IMPROVE: print control invokes the browser print action once

Requirement: print control invokes the browser print action once

Expectation: check:async p=>{await submit(p);await p.evaluate(()=>{window.print=()=>{window.printCalls=(window.printCalls||0)+1;};});await p.locator('#print').click();assert.equal(await p.evaluate(()=>window.printCalls),1);}},

Assessment: Stub proves exactly one window.print call only; does not prove print layout or readability.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:51, quizzes/sprint-0-quiz.html:97

### BR-F16 — KEEP: print control invokes the browser print action once

Requirement: print control invokes the browser print action once

Expectation: BR-C16 rejects altered contract.

Assessment: Recorded failure observes concrete output/control violation caused by responsible UI mutation.

Overlap IDs: None identified beyond generic harness overlap.

Source: tools/audit_quiz_browser.mjs:51, quizzes/sprint-0-quiz.html:97

Mutation: `()=>window.print()` → `()=>{}`. Matches: 1. Changes source: True. Historical status: DETECTED.

Recorded failure: Expected values to be strictly equal:  undefined !== 1 

