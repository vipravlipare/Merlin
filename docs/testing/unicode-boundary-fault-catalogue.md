# Expanded fault review: 511 scenario entries

## What was actually checked

October 10, 2026: reread every function and parameter row in the current 90-case suite against the current helper and maintenance worker. Reran the unchanged suite: **90 passed in 0.42 seconds**. Application and test files were not edited. No database operations or additional mutation experiments were executed.

The [strict testing policy](testing-policy-and-fault-catalogue.md) records the assessment of every function and F001–F150. Those 150 proposals remain the broad risk catalogue: integrity, Unicode, ownership, privileges, transactions, cleanup, concurrency, CLI, probe and migration. The full-command, full-result and CLI-output assertion improvements are still unimplemented. Passing 90 tests does not close those gaps.

## Confirmed additional validation gap: F151

A direct helper check supplied a body containing the lone surrogate U+D800. validate_note accepted it; encoding the accepted body as UTF-8 raised UnicodeEncodeError. PostgreSQL text communication needs encodable text. This demonstrates a Python validation gap, not an observed SQL write or production failure.

Required learner decision and fix specification: reject lone surrogates with a deliberate text-validation ValueError before persistence. Add public-path regressions for title, body and email, including valid supplementary characters as acceptance controls. NUL rejection alone does not establish UTF-8 compatibility. Do not weaken expected errors to accept later transport failures.

## Scope and count

This document extends F001–F150 with F151 and 360 explicit boundary/interactions below: **511 scenario entries**. This is not 511 distinct root causes or 511 executed fault injections. Several entries deliberately exercise the same defect family in different Unicode forms, fields, states or SQL paths. Some overlap existing tests. Do not count overlap as new coverage. Choose cases by demonstrated sensitivity; remove redundant combinations when equivalent detection is established.

Every new row is **PENDING**. No count-based guarantee is possible for all inputs, versions, outages or future features. Existing authentication, deployment and complete backend behavior cannot be tested because they are not implemented here.

## Exact input and oracle for the 360 boundary scenarios

Use the fixed sequence weight in the table below, not the production counting helper, to construct independent inputs. For desired weighted size N and sequence weight W, repeat the sequence floor(N/W) times, then append N modulo W ordinary ASCII letters. This reaches exactly N without fractional emojis. For the decomposed accent, use the actual letter followed by U+0301, not the explanatory text.

Each sequence is real nonblank text. For title cases, keep body equal to the literal text "body". For body cases, keep title equal to "Title". Below/at limits must preserve exact text and both companion fields; delete_on_save must be False. Above-limit helper calls must raise the field-specific ValueError. Draft flags are actual Booleans.

Each insert/update row calls for BOTH the Python validator and a direct SQL operation that bypasses that validator. The SQL operation must run only in fingerprint-verified disposable storage. For update cases, start with a valid existing row in the SAME draft state; change only the tested content and any required device-edit metadata. Do not accidentally test the forbidden saved-to-draft transition instead of a length limit.

SQL rejection must be attributable to the length constraint (check SQLSTATE/constraint identity) and leave the prior row unchanged; test valid controls with all other required fields satisfied. Accepted SQL cases must reconnect and read the exact content. Draft/saved and insert/update cases expose distinct bypass opportunities even though some share a counter defect.

The emoji choices below use an explicit proposed weight of four, based on the established rule. Confirm each added sequence against the pinned Unicode recognition contract before executable tests; do not derive the expected value from emoji.is_emoji in the same test. A disagreement is a contract/library compatibility finding, not permission to silently change the oracle.

| Form | Sequence | Fixed weight |
|---|---|---:|
| ASCII letter | a | 1 |
| ASCII punctuation | ! | 1 |
| CJK ideograph | 中 | 1 |
| precomposed accent | é | 1 |
| decomposed accent | e + U+0301 | 1 |
| supplementary nonemoji letter | U+10400 | 1 |
| smiley | 😀 | 4 |
| family ZWJ | 👨‍👩‍👧‍👦 | 4 |
| skin-tone sequence | 👍🏽 | 4 |
| regional flag | 🇺🇸 | 4 |
| keycap | 1️⃣ | 4 |
| copyright emoji | ©️ | 4 |
| rainbow flag | 🏳️‍🌈 | 4 |
| woman technologist | 👩‍💻 | 4 |
| heart emoji | ❤️ | 4 |

| ID | Form | Field | State | SQL path | Weighted size | Expected helper / SQL result | Status |
|---|---|---|---|---|---:|---|---|
| F152 | ASCII letter | title | saved | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F153 | ASCII letter | title | saved | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F154 | ASCII letter | title | saved | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F155 | ASCII letter | title | saved | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F156 | ASCII letter | title | saved | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F157 | ASCII letter | title | saved | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F158 | ASCII letter | title | draft | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F159 | ASCII letter | title | draft | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F160 | ASCII letter | title | draft | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F161 | ASCII letter | title | draft | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F162 | ASCII letter | title | draft | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F163 | ASCII letter | title | draft | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F164 | ASCII letter | body | saved | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F165 | ASCII letter | body | saved | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F166 | ASCII letter | body | saved | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F167 | ASCII letter | body | saved | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F168 | ASCII letter | body | saved | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F169 | ASCII letter | body | saved | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F170 | ASCII letter | body | draft | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F171 | ASCII letter | body | draft | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F172 | ASCII letter | body | draft | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F173 | ASCII letter | body | draft | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F174 | ASCII letter | body | draft | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F175 | ASCII letter | body | draft | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F176 | ASCII punctuation | title | saved | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F177 | ASCII punctuation | title | saved | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F178 | ASCII punctuation | title | saved | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F179 | ASCII punctuation | title | saved | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F180 | ASCII punctuation | title | saved | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F181 | ASCII punctuation | title | saved | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F182 | ASCII punctuation | title | draft | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F183 | ASCII punctuation | title | draft | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F184 | ASCII punctuation | title | draft | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F185 | ASCII punctuation | title | draft | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F186 | ASCII punctuation | title | draft | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F187 | ASCII punctuation | title | draft | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F188 | ASCII punctuation | body | saved | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F189 | ASCII punctuation | body | saved | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F190 | ASCII punctuation | body | saved | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F191 | ASCII punctuation | body | saved | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F192 | ASCII punctuation | body | saved | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F193 | ASCII punctuation | body | saved | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F194 | ASCII punctuation | body | draft | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F195 | ASCII punctuation | body | draft | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F196 | ASCII punctuation | body | draft | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F197 | ASCII punctuation | body | draft | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F198 | ASCII punctuation | body | draft | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F199 | ASCII punctuation | body | draft | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F200 | CJK ideograph | title | saved | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F201 | CJK ideograph | title | saved | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F202 | CJK ideograph | title | saved | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F203 | CJK ideograph | title | saved | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F204 | CJK ideograph | title | saved | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F205 | CJK ideograph | title | saved | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F206 | CJK ideograph | title | draft | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F207 | CJK ideograph | title | draft | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F208 | CJK ideograph | title | draft | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F209 | CJK ideograph | title | draft | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F210 | CJK ideograph | title | draft | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F211 | CJK ideograph | title | draft | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F212 | CJK ideograph | body | saved | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F213 | CJK ideograph | body | saved | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F214 | CJK ideograph | body | saved | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F215 | CJK ideograph | body | saved | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F216 | CJK ideograph | body | saved | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F217 | CJK ideograph | body | saved | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F218 | CJK ideograph | body | draft | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F219 | CJK ideograph | body | draft | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F220 | CJK ideograph | body | draft | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F221 | CJK ideograph | body | draft | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F222 | CJK ideograph | body | draft | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F223 | CJK ideograph | body | draft | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F224 | precomposed accent | title | saved | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F225 | precomposed accent | title | saved | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F226 | precomposed accent | title | saved | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F227 | precomposed accent | title | saved | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F228 | precomposed accent | title | saved | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F229 | precomposed accent | title | saved | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F230 | precomposed accent | title | draft | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F231 | precomposed accent | title | draft | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F232 | precomposed accent | title | draft | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F233 | precomposed accent | title | draft | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F234 | precomposed accent | title | draft | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F235 | precomposed accent | title | draft | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F236 | precomposed accent | body | saved | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F237 | precomposed accent | body | saved | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F238 | precomposed accent | body | saved | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F239 | precomposed accent | body | saved | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F240 | precomposed accent | body | saved | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F241 | precomposed accent | body | saved | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F242 | precomposed accent | body | draft | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F243 | precomposed accent | body | draft | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F244 | precomposed accent | body | draft | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F245 | precomposed accent | body | draft | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F246 | precomposed accent | body | draft | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F247 | precomposed accent | body | draft | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F248 | decomposed accent | title | saved | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F249 | decomposed accent | title | saved | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F250 | decomposed accent | title | saved | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F251 | decomposed accent | title | saved | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F252 | decomposed accent | title | saved | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F253 | decomposed accent | title | saved | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F254 | decomposed accent | title | draft | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F255 | decomposed accent | title | draft | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F256 | decomposed accent | title | draft | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F257 | decomposed accent | title | draft | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F258 | decomposed accent | title | draft | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F259 | decomposed accent | title | draft | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F260 | decomposed accent | body | saved | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F261 | decomposed accent | body | saved | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F262 | decomposed accent | body | saved | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F263 | decomposed accent | body | saved | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F264 | decomposed accent | body | saved | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F265 | decomposed accent | body | saved | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F266 | decomposed accent | body | draft | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F267 | decomposed accent | body | draft | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F268 | decomposed accent | body | draft | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F269 | decomposed accent | body | draft | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F270 | decomposed accent | body | draft | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F271 | decomposed accent | body | draft | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F272 | supplementary nonemoji letter | title | saved | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F273 | supplementary nonemoji letter | title | saved | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F274 | supplementary nonemoji letter | title | saved | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F275 | supplementary nonemoji letter | title | saved | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F276 | supplementary nonemoji letter | title | saved | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F277 | supplementary nonemoji letter | title | saved | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F278 | supplementary nonemoji letter | title | draft | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F279 | supplementary nonemoji letter | title | draft | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F280 | supplementary nonemoji letter | title | draft | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F281 | supplementary nonemoji letter | title | draft | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F282 | supplementary nonemoji letter | title | draft | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F283 | supplementary nonemoji letter | title | draft | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F284 | supplementary nonemoji letter | body | saved | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F285 | supplementary nonemoji letter | body | saved | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F286 | supplementary nonemoji letter | body | saved | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F287 | supplementary nonemoji letter | body | saved | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F288 | supplementary nonemoji letter | body | saved | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F289 | supplementary nonemoji letter | body | saved | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F290 | supplementary nonemoji letter | body | draft | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F291 | supplementary nonemoji letter | body | draft | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F292 | supplementary nonemoji letter | body | draft | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F293 | supplementary nonemoji letter | body | draft | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F294 | supplementary nonemoji letter | body | draft | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F295 | supplementary nonemoji letter | body | draft | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F296 | smiley | title | saved | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F297 | smiley | title | saved | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F298 | smiley | title | saved | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F299 | smiley | title | saved | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F300 | smiley | title | saved | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F301 | smiley | title | saved | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F302 | smiley | title | draft | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F303 | smiley | title | draft | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F304 | smiley | title | draft | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F305 | smiley | title | draft | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F306 | smiley | title | draft | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F307 | smiley | title | draft | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F308 | smiley | body | saved | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F309 | smiley | body | saved | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F310 | smiley | body | saved | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F311 | smiley | body | saved | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F312 | smiley | body | saved | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F313 | smiley | body | saved | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F314 | smiley | body | draft | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F315 | smiley | body | draft | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F316 | smiley | body | draft | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F317 | smiley | body | draft | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F318 | smiley | body | draft | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F319 | smiley | body | draft | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F320 | family ZWJ | title | saved | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F321 | family ZWJ | title | saved | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F322 | family ZWJ | title | saved | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F323 | family ZWJ | title | saved | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F324 | family ZWJ | title | saved | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F325 | family ZWJ | title | saved | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F326 | family ZWJ | title | draft | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F327 | family ZWJ | title | draft | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F328 | family ZWJ | title | draft | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F329 | family ZWJ | title | draft | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F330 | family ZWJ | title | draft | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F331 | family ZWJ | title | draft | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F332 | family ZWJ | body | saved | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F333 | family ZWJ | body | saved | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F334 | family ZWJ | body | saved | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F335 | family ZWJ | body | saved | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F336 | family ZWJ | body | saved | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F337 | family ZWJ | body | saved | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F338 | family ZWJ | body | draft | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F339 | family ZWJ | body | draft | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F340 | family ZWJ | body | draft | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F341 | family ZWJ | body | draft | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F342 | family ZWJ | body | draft | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F343 | family ZWJ | body | draft | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F344 | skin-tone sequence | title | saved | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F345 | skin-tone sequence | title | saved | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F346 | skin-tone sequence | title | saved | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F347 | skin-tone sequence | title | saved | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F348 | skin-tone sequence | title | saved | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F349 | skin-tone sequence | title | saved | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F350 | skin-tone sequence | title | draft | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F351 | skin-tone sequence | title | draft | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F352 | skin-tone sequence | title | draft | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F353 | skin-tone sequence | title | draft | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F354 | skin-tone sequence | title | draft | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F355 | skin-tone sequence | title | draft | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F356 | skin-tone sequence | body | saved | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F357 | skin-tone sequence | body | saved | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F358 | skin-tone sequence | body | saved | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F359 | skin-tone sequence | body | saved | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F360 | skin-tone sequence | body | saved | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F361 | skin-tone sequence | body | saved | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F362 | skin-tone sequence | body | draft | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F363 | skin-tone sequence | body | draft | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F364 | skin-tone sequence | body | draft | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F365 | skin-tone sequence | body | draft | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F366 | skin-tone sequence | body | draft | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F367 | skin-tone sequence | body | draft | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F368 | regional flag | title | saved | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F369 | regional flag | title | saved | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F370 | regional flag | title | saved | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F371 | regional flag | title | saved | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F372 | regional flag | title | saved | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F373 | regional flag | title | saved | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F374 | regional flag | title | draft | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F375 | regional flag | title | draft | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F376 | regional flag | title | draft | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F377 | regional flag | title | draft | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F378 | regional flag | title | draft | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F379 | regional flag | title | draft | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F380 | regional flag | body | saved | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F381 | regional flag | body | saved | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F382 | regional flag | body | saved | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F383 | regional flag | body | saved | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F384 | regional flag | body | saved | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F385 | regional flag | body | saved | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F386 | regional flag | body | draft | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F387 | regional flag | body | draft | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F388 | regional flag | body | draft | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F389 | regional flag | body | draft | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F390 | regional flag | body | draft | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F391 | regional flag | body | draft | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F392 | keycap | title | saved | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F393 | keycap | title | saved | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F394 | keycap | title | saved | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F395 | keycap | title | saved | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F396 | keycap | title | saved | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F397 | keycap | title | saved | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F398 | keycap | title | draft | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F399 | keycap | title | draft | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F400 | keycap | title | draft | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F401 | keycap | title | draft | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F402 | keycap | title | draft | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F403 | keycap | title | draft | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F404 | keycap | body | saved | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F405 | keycap | body | saved | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F406 | keycap | body | saved | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F407 | keycap | body | saved | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F408 | keycap | body | saved | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F409 | keycap | body | saved | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F410 | keycap | body | draft | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F411 | keycap | body | draft | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F412 | keycap | body | draft | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F413 | keycap | body | draft | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F414 | keycap | body | draft | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F415 | keycap | body | draft | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F416 | copyright emoji | title | saved | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F417 | copyright emoji | title | saved | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F418 | copyright emoji | title | saved | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F419 | copyright emoji | title | saved | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F420 | copyright emoji | title | saved | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F421 | copyright emoji | title | saved | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F422 | copyright emoji | title | draft | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F423 | copyright emoji | title | draft | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F424 | copyright emoji | title | draft | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F425 | copyright emoji | title | draft | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F426 | copyright emoji | title | draft | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F427 | copyright emoji | title | draft | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F428 | copyright emoji | body | saved | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F429 | copyright emoji | body | saved | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F430 | copyright emoji | body | saved | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F431 | copyright emoji | body | saved | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F432 | copyright emoji | body | saved | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F433 | copyright emoji | body | saved | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F434 | copyright emoji | body | draft | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F435 | copyright emoji | body | draft | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F436 | copyright emoji | body | draft | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F437 | copyright emoji | body | draft | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F438 | copyright emoji | body | draft | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F439 | copyright emoji | body | draft | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F440 | rainbow flag | title | saved | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F441 | rainbow flag | title | saved | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F442 | rainbow flag | title | saved | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F443 | rainbow flag | title | saved | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F444 | rainbow flag | title | saved | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F445 | rainbow flag | title | saved | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F446 | rainbow flag | title | draft | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F447 | rainbow flag | title | draft | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F448 | rainbow flag | title | draft | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F449 | rainbow flag | title | draft | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F450 | rainbow flag | title | draft | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F451 | rainbow flag | title | draft | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F452 | rainbow flag | body | saved | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F453 | rainbow flag | body | saved | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F454 | rainbow flag | body | saved | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F455 | rainbow flag | body | saved | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F456 | rainbow flag | body | saved | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F457 | rainbow flag | body | saved | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F458 | rainbow flag | body | draft | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F459 | rainbow flag | body | draft | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F460 | rainbow flag | body | draft | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F461 | rainbow flag | body | draft | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F462 | rainbow flag | body | draft | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F463 | rainbow flag | body | draft | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F464 | woman technologist | title | saved | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F465 | woman technologist | title | saved | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F466 | woman technologist | title | saved | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F467 | woman technologist | title | saved | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F468 | woman technologist | title | saved | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F469 | woman technologist | title | saved | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F470 | woman technologist | title | draft | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F471 | woman technologist | title | draft | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F472 | woman technologist | title | draft | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F473 | woman technologist | title | draft | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F474 | woman technologist | title | draft | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F475 | woman technologist | title | draft | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F476 | woman technologist | body | saved | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F477 | woman technologist | body | saved | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F478 | woman technologist | body | saved | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F479 | woman technologist | body | saved | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F480 | woman technologist | body | saved | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F481 | woman technologist | body | saved | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F482 | woman technologist | body | draft | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F483 | woman technologist | body | draft | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F484 | woman technologist | body | draft | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F485 | woman technologist | body | draft | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F486 | woman technologist | body | draft | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F487 | woman technologist | body | draft | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F488 | heart emoji | title | saved | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F489 | heart emoji | title | saved | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F490 | heart emoji | title | saved | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F491 | heart emoji | title | saved | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F492 | heart emoji | title | saved | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F493 | heart emoji | title | saved | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F494 | heart emoji | title | draft | insert | 174 | Preserve exact content / persist and reconnect | PENDING |
| F495 | heart emoji | title | draft | insert | 175 | Preserve exact content / persist and reconnect | PENDING |
| F496 | heart emoji | title | draft | insert | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F497 | heart emoji | title | draft | update | 174 | Preserve exact content / persist and reconnect | PENDING |
| F498 | heart emoji | title | draft | update | 175 | Preserve exact content / persist and reconnect | PENDING |
| F499 | heart emoji | title | draft | update | 176 | Title ValueError / length CHECK rejects, row unchanged | PENDING |
| F500 | heart emoji | body | saved | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F501 | heart emoji | body | saved | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F502 | heart emoji | body | saved | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F503 | heart emoji | body | saved | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F504 | heart emoji | body | saved | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F505 | heart emoji | body | saved | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F506 | heart emoji | body | draft | insert | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F507 | heart emoji | body | draft | insert | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F508 | heart emoji | body | draft | insert | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |
| F509 | heart emoji | body | draft | update | 6999 | Preserve exact content / persist and reconnect | PENDING |
| F510 | heart emoji | body | draft | update | 7000 | Preserve exact content / persist and reconnect | PENDING |
| F511 | heart emoji | body | draft | update | 7001 | Body ValueError / length CHECK rejects, row unchanged | PENDING |

## Priority and exact next action

First, write a failing surrogate regression through the real validate_note entry point; confirm the current helper accepts the invalid text, then implement deliberate rejection and rerun unchanged existing cases plus the regression. The agent provides this specification; current AGENTS.md reserves executable code/tests to the learner.

Then strengthen worker tests to compare the complete five-query sequence, exact connector settings and error identity. Add real probe tests and resolve oversized blank-title/Unicode-whitespace contracts. The 360 SQL boundary interactions remain blocked until the isolated PL/Python and runtime dependencies are available. Do not begin migration testing on preserved Sprint 0 storage.

Keep a per-case evidence ledger: scenario ID, executable test node, independent oracle, baseline result, injected fault, mutant result and proof layer. A failing mutant only counts when a rule assertion detects it; pre-existing failures, collection errors and timeouts are separate outcomes. Existing historical evidence remains 21 detected mutations, not 511.

The 360-minute Day 6 cap and 39-minute verification allocation remain unchanged. Actual learning minutes are unknown. This catalogue is reusable backlog; extra work displaces later scope rather than adding hidden hours. AWS and DSA remain deferred.

📚 Learn first: Python Unicode HOWTO, https://docs.python.org/3/howto/unicode.html ; Python unittest.mock, https://docs.python.org/3/library/unittest.mock.html . Reference links; not reverified online this turn.

↩ Return: explain why a passing mocked unit suite cannot prove SQL integrity, and why 511 scenario entries are not 511 detected defects.
