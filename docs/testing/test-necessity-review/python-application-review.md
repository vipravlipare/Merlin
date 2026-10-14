# Application Python test and fault necessity review

Reviewed 2026-10-12. No application, test, tool, database or fault edits were made. A finite fixed mutant set cannot prove universal necessity or redundancy. Structural consolidation can preserve every input row; conditional representative candidates require separate approval and contract review before runtime pruning. Negative batch -1 remains KEEP independently of zero: a future nonzero-only guard could accept negatives.

The JSON companion contains exact collected inputs, complete test source, every assertion, concrete overlap IDs and mutated-source/AST fingerprints.

Counts: {"tests": 231, "test_decisions": {"KEEP": 207, "MERGE": 24}, "test_classifications": {"retained behavioral or input partition": 207, "conditional representative candidate": 23, "assertion-subsumed structural duplicate": 1}, "faults": 89, "fault_decisions": {"KEEP": 85, "MERGE": 2, "IMPROVE": 2}}

The 24 probe error-type × stage cases can reduce to nine representatives: OperationalError at each of six lifecycle stages, plus ProgrammingError, DataError and InternalError at query. Connection-construction failure remains separate. This is source-based Cartesian redundancy: all stage operations sit within the same try and share one psycopg.Error handler. It does not justify dropping distinct lifecycle stages.

Keep Unicode whitespace corpus: each of 29 code points is a pinned data-domain contract, and both test families assert different output branches. Surrogate input × public-path reduction is uncertain: callers can regress independently, and position/form coverage is meaningful. No speculative blanket deletion recommended.

Nominal mixed draft title176 shares validator inputs/weight with emoji176; family draft body7004 adds no immediate boundary beyond mixed7001 and independently checked family grapheme counting. The explicit default-save test is not redundant: it omits is_draft and catches a changed default.

Mock connector and context tests prove call contracts only. They do not prove PostgreSQL security, SQL functions, rollback, locking or persistence. Retain actual database evidence separately.

📚 Learn first: [Existing individual case evidence](../case-effectiveness-evidence/python-cases.md).
↩ Return: preserve every retained behavioral class before proposing concrete deletion changes.

## Every collected case

### `tests/test_note_rules_and_maintenance.py::test_display_character_weights[abc !-5]`

**KEEP** — Literal independent expected count covers ordinary text, joined family, skin-tone modifier, regional-indicator flag, keycap or newline. These are distinct grapheme/emoji grammar forms.

Source: `tests/test_note_rules_and_maintenance.py:21`. Inputs: `{"text": "'abc !'", "count": "5"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(text) == count`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_display_character_weights[\U0001f468\u200d\U0001f469\u200d\U0001f467\u200d\U0001f466-4]`

**KEEP** — Literal independent expected count covers ordinary text, joined family, skin-tone modifier, regional-indicator flag, keycap or newline. These are distinct grapheme/emoji grammar forms.

Source: `tests/test_note_rules_and_maintenance.py:21`. Inputs: `{"text": "'\ud83d\udc68\\u200d\ud83d\udc69\\u200d\ud83d\udc67\\u200d\ud83d\udc66'", "count": "4"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(text) == count`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_display_character_weights[\U0001f44d\U0001f3fd-4]`

**KEEP** — Literal independent expected count covers ordinary text, joined family, skin-tone modifier, regional-indicator flag, keycap or newline. These are distinct grapheme/emoji grammar forms.

Source: `tests/test_note_rules_and_maintenance.py:21`. Inputs: `{"text": "'\ud83d\udc4d\ud83c\udffd'", "count": "4"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(text) == count`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_display_character_weights[\U0001f1fa\U0001f1f8-4]`

**KEEP** — Literal independent expected count covers ordinary text, joined family, skin-tone modifier, regional-indicator flag, keycap or newline. These are distinct grapheme/emoji grammar forms.

Source: `tests/test_note_rules_and_maintenance.py:21`. Inputs: `{"text": "'\ud83c\uddfa\ud83c\uddf8'", "count": "4"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(text) == count`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_display_character_weights[1\ufe0f\u20e3-4]`

**KEEP** — Literal independent expected count covers ordinary text, joined family, skin-tone modifier, regional-indicator flag, keycap or newline. These are distinct grapheme/emoji grammar forms.

Source: `tests/test_note_rules_and_maintenance.py:21`. Inputs: `{"text": "'1\ufe0f\u20e3'", "count": "4"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(text) == count`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_display_character_weights[\n-1]`

**KEEP** — Literal independent expected count covers ordinary text, joined family, skin-tone modifier, regional-indicator flag, keycap or newline. These are distinct grapheme/emoji grammar forms.

Source: `tests/test_note_rules_and_maintenance.py:21`. Inputs: `{"text": "'\\n'", "count": "1"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(text) == count`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_title_boundary_with_emoji_sequence`

**KEEP** — Family sequence boundary combines multi-code-point grapheme counting with weighted175 acceptance and176 rejection. Plain title limits cannot establish this integration.

Source: `tests/test_note_rules_and_maintenance.py:25`. Inputs: `{}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (title, '', False) ; pytest.raises(ValueError, match='Title exceeds weighted length 175')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_body_boundary`

**KEEP** — Emoji body accepts weighted7000 and rejects7004. Keep one weighted body integration witness beside exact plain7001 threshold.

Source: `tests/test_note_rules_and_maintenance.py:34`. Inputs: `{}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, body, False) ; pytest.raises(ValueError, match='Body exceeds weighted length 7000')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_wrong_target_never_calls_cleanup[wrong-database]`

**KEEP** — Wrong database only, wrong cluster only and both wrong protect fail-closed fingerprint logic. Single mismatches independently reject an AND-for-OR bug; both wrong retains the explicit double-mismatch refusal contract.

Source: `tests/test_note_rules_and_maintenance.py:49`. Inputs: `{"database": "'merlin'", "cluster": "7694311451826794534"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert cursor.execute.call_args_list == [call('SELECT current_database(), system_identifier FROM pg_control_system()')] ; pytest.raises(RuntimeError, match='Refusing maintenance outside')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_wrong_target_never_calls_cleanup[preserved-cluster]`

**KEEP** — Wrong database only, wrong cluster only and both wrong protect fail-closed fingerprint logic. Single mismatches independently reject an AND-for-OR bug; both wrong retains the explicit double-mismatch refusal contract.

Source: `tests/test_note_rules_and_maintenance.py:49`. Inputs: `{"database": "'merlin_d6'", "cluster": "7691749973399031842"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert cursor.execute.call_args_list == [call('SELECT current_database(), system_identifier FROM pg_control_system()')] ; pytest.raises(RuntimeError, match='Refusing maintenance outside')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_wrong_target_never_calls_cleanup[both-wrong]`

**KEEP** — Wrong database only, wrong cluster only and both wrong protect fail-closed fingerprint logic. Single mismatches independently reject an AND-for-OR bug; both wrong retains the explicit double-mismatch refusal contract.

Source: `tests/test_note_rules_and_maintenance.py:49`. Inputs: `{"database": "'merlin'", "cluster": "7691749973399031842"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert cursor.execute.call_args_list == [call('SELECT current_database(), system_identifier FROM pg_control_system()')] ; pytest.raises(RuntimeError, match='Refusing maintenance outside')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_worker_cycle_verifies_then_uses_bounded_functions`

**KEEP** — Keep exact call sequence, binding, connector target, or exception-context contract. Mock context assertions prove Python ordering/propagation only; they cannot establish SQL atomicity, PostgreSQL read-only mode, permissions or real rollback.

Source: `tests/test_note_rules_and_maintenance.py:65`. Inputs: `{}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert cursor.execute.call_args_list == [call('SELECT current_database(), system_identifier FROM pg_control_system()'), call("SET LOCAL lock_timeout = '2s'"), call("SET LOCAL statement_timeout = '10s'"), call('SELECT public.cleanup_expired_blank_notes(%s)', (25,)), call('SELECT public.purge_deleted_notes(%s)', (25,))] ; assert cursor.fetchone.call_count == 3 ; assert context.__exit__.call_args.args == (None, None, None) ; assert run_once('synthetic-secret', 25) == (2, 3) ; connect.assert_called_once_with(host='127.0.0.1', port=55432, dbname='merlin_d6', user='merlin_d6', connect_timeout=3, password='synthetic-secret')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_more_display_sequences[-0]`

**KEEP** — Literal expected count covers empty identity, punctuation, CJK, CRLF grapheme, additive mixed text, adjacent emoji, variation selector or modifier plus punctuation. Different Unicode segmentation classes need independent examples.

Source: `tests/test_note_rules_and_maintenance.py:97`. Inputs: `{"text": "''", "expected": "0"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(text) == expected`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_more_display_sequences[!@#-3]`

**KEEP** — Literal expected count covers empty identity, punctuation, CJK, CRLF grapheme, additive mixed text, adjacent emoji, variation selector or modifier plus punctuation. Different Unicode segmentation classes need independent examples.

Source: `tests/test_note_rules_and_maintenance.py:97`. Inputs: `{"text": "'!@#'", "expected": "3"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(text) == expected`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_more_display_sequences[\u4e2d\u6587-2]`

**KEEP** — Literal expected count covers empty identity, punctuation, CJK, CRLF grapheme, additive mixed text, adjacent emoji, variation selector or modifier plus punctuation. Different Unicode segmentation classes need independent examples.

Source: `tests/test_note_rules_and_maintenance.py:97`. Inputs: `{"text": "'\u4e2d\u6587'", "expected": "2"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(text) == expected`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_more_display_sequences[\t\r\n-2]`

**KEEP** — Literal expected count covers empty identity, punctuation, CJK, CRLF grapheme, additive mixed text, adjacent emoji, variation selector or modifier plus punctuation. Different Unicode segmentation classes need independent examples.

Source: `tests/test_note_rules_and_maintenance.py:97`. Inputs: `{"text": "'\\t\\r\\n'", "expected": "2"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(text) == expected`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_more_display_sequences[a\U0001f600b-6]`

**KEEP** — Literal expected count covers empty identity, punctuation, CJK, CRLF grapheme, additive mixed text, adjacent emoji, variation selector or modifier plus punctuation. Different Unicode segmentation classes need independent examples.

Source: `tests/test_note_rules_and_maintenance.py:97`. Inputs: `{"text": "'a\ud83d\ude00b'", "expected": "6"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(text) == expected`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_more_display_sequences[\U0001f468\u200d\U0001f469\u200d\U0001f467\u200d\U0001f466\U0001f600-8]`

**KEEP** — Literal expected count covers empty identity, punctuation, CJK, CRLF grapheme, additive mixed text, adjacent emoji, variation selector or modifier plus punctuation. Different Unicode segmentation classes need independent examples.

Source: `tests/test_note_rules_and_maintenance.py:97`. Inputs: `{"text": "'\ud83d\udc68\\u200d\ud83d\udc69\\u200d\ud83d\udc67\\u200d\ud83d\udc66\ud83d\ude00'", "expected": "8"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(text) == expected`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_more_display_sequences[\xa9\ufe0f-4]`

**KEEP** — Literal expected count covers empty identity, punctuation, CJK, CRLF grapheme, additive mixed text, adjacent emoji, variation selector or modifier plus punctuation. Different Unicode segmentation classes need independent examples.

Source: `tests/test_note_rules_and_maintenance.py:97`. Inputs: `{"text": "'\u00a9\ufe0f'", "expected": "4"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(text) == expected`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_more_display_sequences[\U0001f44d\U0001f3fd!-5]`

**KEEP** — Literal expected count covers empty identity, punctuation, CJK, CRLF grapheme, additive mixed text, adjacent emoji, variation selector or modifier plus punctuation. Different Unicode segmentation classes need independent examples.

Source: `tests/test_note_rules_and_maintenance.py:97`. Inputs: `{"text": "'\ud83d\udc4d\ud83c\udffd!'", "expected": "5"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(text) == expected`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_plain_title_limit[174-True]`

**KEEP** — Adjacent 174/175/176 checks distinguish below-limit, inclusive maximum and first rejection, with exact preserved result on accepted inputs.

Source: `tests/test_note_rules_and_maintenance.py:103`. Inputs: `{"size": "174", "accepted": "True"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == ('a' * size, '', False) ; pytest.raises(ValueError, match='Title exceeds weighted length 175')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_plain_title_limit[175-True]`

**KEEP** — Adjacent 174/175/176 checks distinguish below-limit, inclusive maximum and first rejection, with exact preserved result on accepted inputs.

Source: `tests/test_note_rules_and_maintenance.py:103`. Inputs: `{"size": "175", "accepted": "True"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == ('a' * size, '', False) ; pytest.raises(ValueError, match='Title exceeds weighted length 175')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_plain_title_limit[176-False]`

**KEEP** — Adjacent 174/175/176 checks distinguish below-limit, inclusive maximum and first rejection, with exact preserved result on accepted inputs.

Source: `tests/test_note_rules_and_maintenance.py:103`. Inputs: `{"size": "176", "accepted": "False"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == ('a' * size, '', False) ; pytest.raises(ValueError, match='Title exceeds weighted length 175')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_plain_body_limit[6999-True]`

**KEEP** — Adjacent 6999/7000/7001 checks distinguish below-limit, inclusive maximum and first rejection, with exact preserved result on accepted inputs.

Source: `tests/test_note_rules_and_maintenance.py:113`. Inputs: `{"size": "6999", "accepted": "True"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, 'a' * size, False) ; pytest.raises(ValueError, match='Body exceeds weighted length 7000')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_plain_body_limit[7000-True]`

**KEEP** — Adjacent 6999/7000/7001 checks distinguish below-limit, inclusive maximum and first rejection, with exact preserved result on accepted inputs.

Source: `tests/test_note_rules_and_maintenance.py:113`. Inputs: `{"size": "7000", "accepted": "True"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, 'a' * size, False) ; pytest.raises(ValueError, match='Body exceeds weighted length 7000')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_plain_body_limit[7001-False]`

**KEEP** — Adjacent 6999/7000/7001 checks distinguish below-limit, inclusive maximum and first rejection, with exact preserved result on accepted inputs.

Source: `tests/test_note_rules_and_maintenance.py:113`. Inputs: `{"size": "7001", "accepted": "False"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, 'a' * size, False) ; pytest.raises(ValueError, match='Body exceeds weighted length 7000')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_over_limit_title_rejected_even_for_drafts[emoji176]`

**KEEP** — Preserve this exact input class and independently specified outcomes: pytest.raises(ValueError, match='Title exceeds weighted length 175').

Source: `tests/test_note_rules_and_maintenance.py:123`. Inputs: `{"title": "'\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match='Title exceeds weighted length 175')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_over_limit_title_rejected_even_for_drafts[mixed176]`

**MERGE** — Both this input and emoji176 weigh exactly 176 with draft=True and empty body; no validator branch distinguishes all-emoji versus mixed content. Keep emoji176 and accented176, plus separate family boundary and mixed counter cases.

Source: `tests/test_note_rules_and_maintenance.py:123`. Inputs: `{"title": "'\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00\ud83d\ude00abcd'"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `pytest.raises(ValueError, match='Title exceeds weighted length 175')`.

Exact overlap IDs: `tests/test_note_rules_and_maintenance.py::test_over_limit_title_rejected_even_for_drafts[emoji176]`.

### `tests/test_note_rules_and_maintenance.py::test_over_limit_title_rejected_even_for_drafts[accented176]`

**KEEP** — Preserve this exact input class and independently specified outcomes: pytest.raises(ValueError, match='Title exceeds weighted length 175').

Source: `tests/test_note_rules_and_maintenance.py:123`. Inputs: `{"title": {"repeat": "'e\\u0301'", "times": 176, "suffix": "''"}}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match='Title exceeds weighted length 175')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_over_limit_body_rejected_even_for_drafts[family7004]`

**MERGE** — Family grapheme behavior already independently checked in counter and title boundary. Keep mixed7001 for immediate draft body threshold and spaces7001 for length-before-blank decision; family7004 overshoots the exact boundary.

Source: `tests/test_note_rules_and_maintenance.py:129`. Inputs: `{"body": {"repeat": "'\\U0001f468\\u200d\\U0001f469\\u200d\\U0001f467\\u200d\\U0001f466'", "times": 1751, "suffix": "''"}}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `pytest.raises(ValueError, match='Body exceeds weighted length 7000')`.

Exact overlap IDs: `tests/test_note_rules_and_maintenance.py::test_over_limit_body_rejected_even_for_drafts[mixed7001]`.

### `tests/test_note_rules_and_maintenance.py::test_over_limit_body_rejected_even_for_drafts[mixed7001]`

**KEEP** — Preserve this exact input class and independently specified outcomes: pytest.raises(ValueError, match='Body exceeds weighted length 7000').

Source: `tests/test_note_rules_and_maintenance.py:129`. Inputs: `{"body": {"repeat": "'\\U0001f600\\U0001f600'", "times": 875, "suffix": "'a'"}}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match='Body exceeds weighted length 7000')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_over_limit_body_rejected_even_for_drafts[spaces7001]`

**KEEP** — Preserve this exact input class and independently specified outcomes: pytest.raises(ValueError, match='Body exceeds weighted length 7000').

Source: `tests/test_note_rules_and_maintenance.py:129`. Inputs: `{"body": {"repeat": "' '", "times": 7001, "suffix": "''"}}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match='Body exceeds weighted length 7000')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_empty_note_decision[False-None-None]`

**KEEP** — None/empty/ASCII whitespace/NBSP preserve different normalized body values. Draft false requests deletion and draft true forbids deletion. The eight cases are meaningful null/normalization × save-intent contracts.

Source: `tests/test_note_rules_and_maintenance.py:136`. Inputs: `{"draft": "False", "title": "None", "body": "None"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert result.title is None ; assert result.body == ('' if body is None else body) ; assert result.delete_on_save is (not draft)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_empty_note_decision[False--]`

**KEEP** — None/empty/ASCII whitespace/NBSP preserve different normalized body values. Draft false requests deletion and draft true forbids deletion. The eight cases are meaningful null/normalization × save-intent contracts.

Source: `tests/test_note_rules_and_maintenance.py:136`. Inputs: `{"draft": "False", "title": "''", "body": "''"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert result.title is None ; assert result.body == ('' if body is None else body) ; assert result.delete_on_save is (not draft)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_empty_note_decision[False- \t\n- \r\n]`

**KEEP** — None/empty/ASCII whitespace/NBSP preserve different normalized body values. Draft false requests deletion and draft true forbids deletion. The eight cases are meaningful null/normalization × save-intent contracts.

Source: `tests/test_note_rules_and_maintenance.py:136`. Inputs: `{"draft": "False", "title": "' \\t\\n'", "body": "' \\r\\n'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert result.title is None ; assert result.body == ('' if body is None else body) ; assert result.delete_on_save is (not draft)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_empty_note_decision[False-\xa0-\xa0]`

**KEEP** — None/empty/ASCII whitespace/NBSP preserve different normalized body values. Draft false requests deletion and draft true forbids deletion. The eight cases are meaningful null/normalization × save-intent contracts.

Source: `tests/test_note_rules_and_maintenance.py:136`. Inputs: `{"draft": "False", "title": "'\\xa0'", "body": "'\\xa0'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert result.title is None ; assert result.body == ('' if body is None else body) ; assert result.delete_on_save is (not draft)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_empty_note_decision[True-None-None]`

**KEEP** — None/empty/ASCII whitespace/NBSP preserve different normalized body values. Draft false requests deletion and draft true forbids deletion. The eight cases are meaningful null/normalization × save-intent contracts.

Source: `tests/test_note_rules_and_maintenance.py:136`. Inputs: `{"draft": "True", "title": "None", "body": "None"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert result.title is None ; assert result.body == ('' if body is None else body) ; assert result.delete_on_save is (not draft)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_empty_note_decision[True--]`

**KEEP** — None/empty/ASCII whitespace/NBSP preserve different normalized body values. Draft false requests deletion and draft true forbids deletion. The eight cases are meaningful null/normalization × save-intent contracts.

Source: `tests/test_note_rules_and_maintenance.py:136`. Inputs: `{"draft": "True", "title": "''", "body": "''"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert result.title is None ; assert result.body == ('' if body is None else body) ; assert result.delete_on_save is (not draft)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_empty_note_decision[True- \t\n- \r\n]`

**KEEP** — None/empty/ASCII whitespace/NBSP preserve different normalized body values. Draft false requests deletion and draft true forbids deletion. The eight cases are meaningful null/normalization × save-intent contracts.

Source: `tests/test_note_rules_and_maintenance.py:136`. Inputs: `{"draft": "True", "title": "' \\t\\n'", "body": "' \\r\\n'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert result.title is None ; assert result.body == ('' if body is None else body) ; assert result.delete_on_save is (not draft)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_empty_note_decision[True-\xa0-\xa0]`

**KEEP** — None/empty/ASCII whitespace/NBSP preserve different normalized body values. Draft false requests deletion and draft true forbids deletion. The eight cases are meaningful null/normalization × save-intent contracts.

Source: `tests/test_note_rules_and_maintenance.py:136`. Inputs: `{"draft": "True", "title": "'\\xa0'", "body": "'\\xa0'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert result.title is None ; assert result.body == ('' if body is None else body) ; assert result.delete_on_save is (not draft)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_nonblank_note_is_preserved[Title-]`

**KEEP** — Title-only, body-only and both populated protect each side of blank-note decision and exact content preservation.

Source: `tests/test_note_rules_and_maintenance.py:144`. Inputs: `{"title": "'Title'", "body": "''"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (title, body, False)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_nonblank_note_is_preserved[None-body]`

**KEEP** — Title-only, body-only and both populated protect each side of blank-note decision and exact content preservation.

Source: `tests/test_note_rules_and_maintenance.py:144`. Inputs: `{"title": "None", "body": "'body'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (title, body, False)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_nonblank_note_is_preserved[ \U0001f600 - \nbody\n ]`

**KEEP** — Title-only, body-only and both populated protect each side of blank-note decision and exact content preservation.

Source: `tests/test_note_rules_and_maintenance.py:144`. Inputs: `{"title": "' \ud83d\ude00 '", "body": "' \\nbody\\n '"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (title, body, False)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_count_rejects_invalid_text[None]`

**KEEP** — None/int/bytes test strict string validation; sole and embedded NUL distinguish membership checking from start-only checking. Exact messages forbid input echo.

Source: `tests/test_note_rules_and_maintenance.py:150`. Inputs: `{"value": "None"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match=f'^{message}$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_count_rejects_invalid_text[1]`

**KEEP** — None/int/bytes test strict string validation; sole and embedded NUL distinguish membership checking from start-only checking. Exact messages forbid input echo.

Source: `tests/test_note_rules_and_maintenance.py:150`. Inputs: `{"value": "1"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match=f'^{message}$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_count_rejects_invalid_text[text]`

**KEEP** — None/int/bytes test strict string validation; sole and embedded NUL distinguish membership checking from start-only checking. Exact messages forbid input echo.

Source: `tests/test_note_rules_and_maintenance.py:150`. Inputs: `{"value": "b'text'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match=f'^{message}$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_count_rejects_invalid_text[\x00]`

**KEEP** — None/int/bytes test strict string validation; sole and embedded NUL distinguish membership checking from start-only checking. Exact messages forbid input echo.

Source: `tests/test_note_rules_and_maintenance.py:150`. Inputs: `{"value": "'\\x00'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match=f'^{message}$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_count_rejects_invalid_text[hello\x00]`

**KEEP** — None/int/bytes test strict string validation; sole and embedded NUL distinguish membership checking from start-only checking. Exact messages forbid input echo.

Source: `tests/test_note_rules_and_maintenance.py:150`. Inputs: `{"value": "'hello\\x00'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match=f'^{message}$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_note_fields_reject_invalid_text[10-title]`

**KEEP** — Each independently callable title/body path must invoke text validation. Int and bytes are distinct likely accidental inputs; NUL verifies database-text rejection, not only Python type checking.

Source: `tests/test_note_rules_and_maintenance.py:158`. Inputs: `{"value": "10", "field": "'title'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match=f'^{message}$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_note_fields_reject_invalid_text[10-body]`

**KEEP** — Each independently callable title/body path must invoke text validation. Int and bytes are distinct likely accidental inputs; NUL verifies database-text rejection, not only Python type checking.

Source: `tests/test_note_rules_and_maintenance.py:158`. Inputs: `{"value": "10", "field": "'body'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match=f'^{message}$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_note_fields_reject_invalid_text[text-title]`

**KEEP** — Each independently callable title/body path must invoke text validation. Int and bytes are distinct likely accidental inputs; NUL verifies database-text rejection, not only Python type checking.

Source: `tests/test_note_rules_and_maintenance.py:158`. Inputs: `{"value": "b'text'", "field": "'title'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match=f'^{message}$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_note_fields_reject_invalid_text[text-body]`

**KEEP** — Each independently callable title/body path must invoke text validation. Int and bytes are distinct likely accidental inputs; NUL verifies database-text rejection, not only Python type checking.

Source: `tests/test_note_rules_and_maintenance.py:158`. Inputs: `{"value": "b'text'", "field": "'body'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match=f'^{message}$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_note_fields_reject_invalid_text[\x00-title]`

**KEEP** — Each independently callable title/body path must invoke text validation. Int and bytes are distinct likely accidental inputs; NUL verifies database-text rejection, not only Python type checking.

Source: `tests/test_note_rules_and_maintenance.py:158`. Inputs: `{"value": "'\\x00'", "field": "'title'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match=f'^{message}$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_note_fields_reject_invalid_text[\x00-body]`

**KEEP** — Each independently callable title/body path must invoke text validation. Int and bytes are distinct likely accidental inputs; NUL verifies database-text rejection, not only Python type checking.

Source: `tests/test_note_rules_and_maintenance.py:158`. Inputs: `{"value": "'\\x00'", "field": "'body'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match=f'^{message}$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_email_edge_whitespace[None-None]`

**KEEP** — Absent and empty email normalize to None; whitespace-only collapses; mixed-case ASCII edges preserve case; NBSP edges require Unicode stripping.

Source: `tests/test_note_rules_and_maintenance.py:167`. Inputs: `{"raw": "None", "expected": "None"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert normalize_email(raw) == expected`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_email_edge_whitespace[-None]`

**KEEP** — Absent and empty email normalize to None; whitespace-only collapses; mixed-case ASCII edges preserve case; NBSP edges require Unicode stripping.

Source: `tests/test_note_rules_and_maintenance.py:167`. Inputs: `{"raw": "''", "expected": "None"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert normalize_email(raw) == expected`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_email_edge_whitespace[\t\n-None]`

**KEEP** — Absent and empty email normalize to None; whitespace-only collapses; mixed-case ASCII edges preserve case; NBSP edges require Unicode stripping.

Source: `tests/test_note_rules_and_maintenance.py:167`. Inputs: `{"raw": "'\\t\\n'", "expected": "None"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert normalize_email(raw) == expected`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_email_edge_whitespace[ \tMixed@Example.COM\n -Mixed@Example.COM]`

**KEEP** — Absent and empty email normalize to None; whitespace-only collapses; mixed-case ASCII edges preserve case; NBSP edges require Unicode stripping.

Source: `tests/test_note_rules_and_maintenance.py:167`. Inputs: `{"raw": "' \\tMixed@Example.COM\\n '", "expected": "'Mixed@Example.COM'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert normalize_email(raw) == expected`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_email_edge_whitespace[\xa0a@b.test\xa0-a@b.test]`

**KEEP** — Absent and empty email normalize to None; whitespace-only collapses; mixed-case ASCII edges preserve case; NBSP edges require Unicode stripping.

Source: `tests/test_note_rules_and_maintenance.py:167`. Inputs: `{"raw": "'\\xa0a@b.test\\xa0'", "expected": "'a@b.test'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert normalize_email(raw) == expected`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_email_rejects_invalid_database_text[10]`

**KEEP** — Email caller must invoke string and NUL validation before normalization; exact generic message prevents leaking private email input.

Source: `tests/test_note_rules_and_maintenance.py:172`. Inputs: `{"value": "10"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match=f'^{message}$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_email_rejects_invalid_database_text[email]`

**KEEP** — Email caller must invoke string and NUL validation before normalization; exact generic message prevents leaking private email input.

Source: `tests/test_note_rules_and_maintenance.py:172`. Inputs: `{"value": "b'email'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match=f'^{message}$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_email_rejects_invalid_database_text[a\x00@b.test]`

**KEEP** — Email caller must invoke string and NUL validation before normalization; exact generic message prevents leaking private email input.

Source: `tests/test_note_rules_and_maintenance.py:172`. Inputs: `{"value": "'a\\x00@b.test'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match=f'^{message}$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_unicode_rejected_before_persistence[high-surrogate-counter]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:182`. Inputs: `{"value": "'\\ud800'", "path": "'counter'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.__suppress_context__ is True ; pytest.raises(ValueError, match='^Text must be valid UTF-8$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_unicode_rejected_before_persistence[high-surrogate-title]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:182`. Inputs: `{"value": "'\\ud800'", "path": "'title'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.__suppress_context__ is True ; pytest.raises(ValueError, match='^Text must be valid UTF-8$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_unicode_rejected_before_persistence[high-surrogate-body]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:182`. Inputs: `{"value": "'\\ud800'", "path": "'body'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.__suppress_context__ is True ; pytest.raises(ValueError, match='^Text must be valid UTF-8$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_unicode_rejected_before_persistence[high-surrogate-email]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:182`. Inputs: `{"value": "'\\ud800'", "path": "'email'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.__suppress_context__ is True ; pytest.raises(ValueError, match='^Text must be valid UTF-8$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_unicode_rejected_before_persistence[low-surrogate-counter]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:182`. Inputs: `{"value": "'\\udfff'", "path": "'counter'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.__suppress_context__ is True ; pytest.raises(ValueError, match='^Text must be valid UTF-8$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_unicode_rejected_before_persistence[low-surrogate-title]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:182`. Inputs: `{"value": "'\\udfff'", "path": "'title'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.__suppress_context__ is True ; pytest.raises(ValueError, match='^Text must be valid UTF-8$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_unicode_rejected_before_persistence[low-surrogate-body]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:182`. Inputs: `{"value": "'\\udfff'", "path": "'body'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.__suppress_context__ is True ; pytest.raises(ValueError, match='^Text must be valid UTF-8$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_unicode_rejected_before_persistence[low-surrogate-email]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:182`. Inputs: `{"value": "'\\udfff'", "path": "'email'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.__suppress_context__ is True ; pytest.raises(ValueError, match='^Text must be valid UTF-8$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_unicode_rejected_before_persistence[embedded-counter]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:182`. Inputs: `{"value": "'a\\ud800b'", "path": "'counter'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.__suppress_context__ is True ; pytest.raises(ValueError, match='^Text must be valid UTF-8$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_unicode_rejected_before_persistence[embedded-title]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:182`. Inputs: `{"value": "'a\\ud800b'", "path": "'title'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.__suppress_context__ is True ; pytest.raises(ValueError, match='^Text must be valid UTF-8$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_unicode_rejected_before_persistence[embedded-body]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:182`. Inputs: `{"value": "'a\\ud800b'", "path": "'body'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.__suppress_context__ is True ; pytest.raises(ValueError, match='^Text must be valid UTF-8$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_unicode_rejected_before_persistence[embedded-email]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:182`. Inputs: `{"value": "'a\\ud800b'", "path": "'email'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.__suppress_context__ is True ; pytest.raises(ValueError, match='^Text must be valid UTF-8$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_unicode_rejected_before_persistence[surrogate-pair-counter]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:182`. Inputs: `{"value": "'\\ud83d\\ude00'", "path": "'counter'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.__suppress_context__ is True ; pytest.raises(ValueError, match='^Text must be valid UTF-8$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_unicode_rejected_before_persistence[surrogate-pair-title]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:182`. Inputs: `{"value": "'\\ud83d\\ude00'", "path": "'title'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.__suppress_context__ is True ; pytest.raises(ValueError, match='^Text must be valid UTF-8$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_unicode_rejected_before_persistence[surrogate-pair-body]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:182`. Inputs: `{"value": "'\\ud83d\\ude00'", "path": "'body'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.__suppress_context__ is True ; pytest.raises(ValueError, match='^Text must be valid UTF-8$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_unicode_rejected_before_persistence[surrogate-pair-email]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:182`. Inputs: `{"value": "'\\ud83d\\ude00'", "path": "'email'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.__suppress_context__ is True ; pytest.raises(ValueError, match='^Text must be valid UTF-8$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_valid_unicode_preserved_in_every_text_path[\U0001f600-4-counter]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:199`. Inputs: `{"value": "'\ud83d\ude00'", "expected_weight": "4", "path": "'counter'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(value) == expected_weight ; assert (result.title, result.body, result.delete_on_save) == (value, 'body', False) ; assert (result.title, result.body, result.delete_on_save) == ('Title', value, False) ; assert normalize_email(value) == value`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_valid_unicode_preserved_in_every_text_path[\U0001f600-4-title]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:199`. Inputs: `{"value": "'\ud83d\ude00'", "expected_weight": "4", "path": "'title'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(value) == expected_weight ; assert (result.title, result.body, result.delete_on_save) == (value, 'body', False) ; assert (result.title, result.body, result.delete_on_save) == ('Title', value, False) ; assert normalize_email(value) == value`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_valid_unicode_preserved_in_every_text_path[\U0001f600-4-body]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:199`. Inputs: `{"value": "'\ud83d\ude00'", "expected_weight": "4", "path": "'body'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(value) == expected_weight ; assert (result.title, result.body, result.delete_on_save) == (value, 'body', False) ; assert (result.title, result.body, result.delete_on_save) == ('Title', value, False) ; assert normalize_email(value) == value`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_valid_unicode_preserved_in_every_text_path[\U0001f600-4-email]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:199`. Inputs: `{"value": "'\ud83d\ude00'", "expected_weight": "4", "path": "'email'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(value) == expected_weight ; assert (result.title, result.body, result.delete_on_save) == (value, 'body', False) ; assert (result.title, result.body, result.delete_on_save) == ('Title', value, False) ; assert normalize_email(value) == value`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_valid_unicode_preserved_in_every_text_path[\U00010400-1-counter]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:199`. Inputs: `{"value": "'\ud801\udc00'", "expected_weight": "1", "path": "'counter'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(value) == expected_weight ; assert (result.title, result.body, result.delete_on_save) == (value, 'body', False) ; assert (result.title, result.body, result.delete_on_save) == ('Title', value, False) ; assert normalize_email(value) == value`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_valid_unicode_preserved_in_every_text_path[\U00010400-1-title]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:199`. Inputs: `{"value": "'\ud801\udc00'", "expected_weight": "1", "path": "'title'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(value) == expected_weight ; assert (result.title, result.body, result.delete_on_save) == (value, 'body', False) ; assert (result.title, result.body, result.delete_on_save) == ('Title', value, False) ; assert normalize_email(value) == value`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_valid_unicode_preserved_in_every_text_path[\U00010400-1-body]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:199`. Inputs: `{"value": "'\ud801\udc00'", "expected_weight": "1", "path": "'body'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(value) == expected_weight ; assert (result.title, result.body, result.delete_on_save) == (value, 'body', False) ; assert (result.title, result.body, result.delete_on_save) == ('Title', value, False) ; assert normalize_email(value) == value`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_valid_unicode_preserved_in_every_text_path[\U00010400-1-email]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:199`. Inputs: `{"value": "'\ud801\udc00'", "expected_weight": "1", "path": "'email'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(value) == expected_weight ; assert (result.title, result.body, result.delete_on_save) == (value, 'body', False) ; assert (result.title, result.body, result.delete_on_save) == ('Title', value, False) ; assert normalize_email(value) == value`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_valid_unicode_preserved_in_every_text_path[e\u0301-1-counter]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:199`. Inputs: `{"value": "'e\u0301'", "expected_weight": "1", "path": "'counter'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(value) == expected_weight ; assert (result.title, result.body, result.delete_on_save) == (value, 'body', False) ; assert (result.title, result.body, result.delete_on_save) == ('Title', value, False) ; assert normalize_email(value) == value`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_valid_unicode_preserved_in_every_text_path[e\u0301-1-title]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:199`. Inputs: `{"value": "'e\u0301'", "expected_weight": "1", "path": "'title'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(value) == expected_weight ; assert (result.title, result.body, result.delete_on_save) == (value, 'body', False) ; assert (result.title, result.body, result.delete_on_save) == ('Title', value, False) ; assert normalize_email(value) == value`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_valid_unicode_preserved_in_every_text_path[e\u0301-1-body]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:199`. Inputs: `{"value": "'e\u0301'", "expected_weight": "1", "path": "'body'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(value) == expected_weight ; assert (result.title, result.body, result.delete_on_save) == (value, 'body', False) ; assert (result.title, result.body, result.delete_on_save) == ('Title', value, False) ; assert normalize_email(value) == value`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_valid_unicode_preserved_in_every_text_path[e\u0301-1-email]`

**KEEP** — Public path coverage checks that each caller invokes validation; high/low/embedded/paired surrogates cover distinct positions/forms. Valid emoji, supplementary nonemoji, and combining grapheme prevent overbroad rejection. Product reduction is possible but not proven safe for caller-specific regressions.

Source: `tests/test_note_rules_and_maintenance.py:199`. Inputs: `{"value": "'e\u0301'", "expected_weight": "1", "path": "'email'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert weighted_length(value) == expected_weight ; assert (result.title, result.body, result.delete_on_save) == (value, 'body', False) ; assert (result.title, result.body, result.delete_on_save) == ('Title', value, False) ; assert normalize_email(value) == value`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_batch_never_connects[-1]`

**KEEP** — Negative input is a separate partition from zero boundary. Keep -1 to catch a future nonzero-only check that accepts negatives; identical current fault detections do not prove redundancy.

Source: `tests/test_note_rules_and_maintenance.py:215`. Inputs: `{"size": "-1"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `connect.assert_not_called() ; pytest.raises(ValueError, match='^Batch size must be between 1 and 1000$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_batch_never_connects[0]`

**KEEP** — Preserve this exact input class and independently specified outcomes: connect.assert_not_called() ; pytest.raises(ValueError, match='^Batch size must be between 1 and 1000$').

Source: `tests/test_note_rules_and_maintenance.py:215`. Inputs: `{"size": "0"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `connect.assert_not_called() ; pytest.raises(ValueError, match='^Batch size must be between 1 and 1000$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invalid_batch_never_connects[1001]`

**KEEP** — Preserve this exact input class and independently specified outcomes: connect.assert_not_called() ; pytest.raises(ValueError, match='^Batch size must be between 1 and 1000$').

Source: `tests/test_note_rules_and_maintenance.py:215`. Inputs: `{"size": "1001"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `connect.assert_not_called() ; pytest.raises(ValueError, match='^Batch size must be between 1 and 1000$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_allowed_batch_boundaries_and_fixed_target[1]`

**KEEP** — Keep exact call sequence, binding, connector target, or exception-context contract. Mock context assertions prove Python ordering/propagation only; they cannot establish SQL atomicity, PostgreSQL read-only mode, permissions or real rollback.

Source: `tests/test_note_rules_and_maintenance.py:223`. Inputs: `{"size": "1"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert cursor.execute.call_args_list == [call('SELECT current_database(), system_identifier FROM pg_control_system()'), call("SET LOCAL lock_timeout = '2s'"), call("SET LOCAL statement_timeout = '10s'"), call('SELECT public.cleanup_expired_blank_notes(%s)', (size,)), call('SELECT public.purge_deleted_notes(%s)', (size,))] ; assert cursor.fetchone.call_count == 3 ; assert run_once('synthetic-secret', size) == (0, 0) ; connect.assert_called_once_with(host='127.0.0.1', port=55432, dbname='merlin_d6', user='merlin_d6', connect_timeout=3, password='synthetic-secret')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_allowed_batch_boundaries_and_fixed_target[1000]`

**KEEP** — Keep exact call sequence, binding, connector target, or exception-context contract. Mock context assertions prove Python ordering/propagation only; they cannot establish SQL atomicity, PostgreSQL read-only mode, permissions or real rollback.

Source: `tests/test_note_rules_and_maintenance.py:223`. Inputs: `{"size": "1000"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert cursor.execute.call_args_list == [call('SELECT current_database(), system_identifier FROM pg_control_system()'), call("SET LOCAL lock_timeout = '2s'"), call("SET LOCAL statement_timeout = '10s'"), call('SELECT public.cleanup_expired_blank_notes(%s)', (size,)), call('SELECT public.purge_deleted_notes(%s)', (size,))] ; assert cursor.fetchone.call_count == 3 ; assert run_once('synthetic-secret', size) == (0, 0) ; connect.assert_called_once_with(host='127.0.0.1', port=55432, dbname='merlin_d6', user='merlin_d6', connect_timeout=3, password='synthetic-secret')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_cleanup_failure_leaves_transaction_as_error[expiry]`

**KEEP** — Keep exact call sequence, binding, connector target, or exception-context contract. Mock context assertions prove Python ordering/propagation only; they cannot establish SQL atomicity, PostgreSQL read-only mode, permissions or real rollback.

Source: `tests/test_note_rules_and_maintenance.py:247`. Inputs: `{"failure_stage": "'expiry'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert context.__exit__.call_count == 1 ; assert kind is psycopg.OperationalError and error is failure ; assert traceback is not None ; assert not any(('purge_deleted_notes' in call.args[0] for call in cursor.execute.call_args_list)) ; conn.commit.assert_not_called() ; pytest.raises(psycopg.OperationalError, match='synthetic failure')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_cleanup_failure_leaves_transaction_as_error[purge]`

**KEEP** — Keep exact call sequence, binding, connector target, or exception-context contract. Mock context assertions prove Python ordering/propagation only; they cannot establish SQL atomicity, PostgreSQL read-only mode, permissions or real rollback.

Source: `tests/test_note_rules_and_maintenance.py:247`. Inputs: `{"failure_stage": "'purge'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert context.__exit__.call_count == 1 ; assert kind is psycopg.OperationalError and error is failure ; assert traceback is not None ; assert not any(('purge_deleted_notes' in call.args[0] for call in cursor.execute.call_args_list)) ; conn.commit.assert_not_called() ; pytest.raises(psycopg.OperationalError, match='synthetic failure')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_blank_title_with_real_body[]`

**KEEP** — Preserve this exact input class and independently specified outcomes: assert (result.title, result.body, result.delete_on_save) == (None, '  actual writing\n ', False).

Source: `tests/test_note_rules_and_maintenance.py:278`. Inputs: `{"title": "''"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, '  actual writing\n ', False)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_blank_title_with_real_body[ \t\n]`

**KEEP** — Preserve this exact input class and independently specified outcomes: assert (result.title, result.body, result.delete_on_save) == (None, '  actual writing\n ', False).

Source: `tests/test_note_rules_and_maintenance.py:278`. Inputs: `{"title": "' \\t\\n'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, '  actual writing\n ', False)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_combining_characters_accepted_at_display_limit[title-175]`

**KEEP** — Exact title175/body7000 display grapheme boundaries contain twice as many code points, proving public validation uses weighted graphemes rather than raw len.

Source: `tests/test_note_rules_and_maintenance.py:285`. Inputs: `{"field": "'title'", "size": "175"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == ((text, '', False) if field == 'title' else (None, text, False))`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_combining_characters_accepted_at_display_limit[body-7000]`

**KEEP** — Exact title175/body7000 display grapheme boundaries contain twice as many code points, proving public validation uses weighted graphemes rather than raw len.

Source: `tests/test_note_rules_and_maintenance.py:285`. Inputs: `{"field": "'body'", "size": "7000"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == ((text, '', False) if field == 'title' else (None, text, False))`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_noninteger_batch_rejected_before_connecting[boolean]`

**KEEP** — Preserve this exact input class and independently specified outcomes: connect.assert_not_called() ; pytest.raises(ValueError, match='^Batch size must be an integer$').

Source: `tests/test_note_rules_and_maintenance.py:293`. Inputs: `{"size": "True"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `connect.assert_not_called() ; pytest.raises(ValueError, match='^Batch size must be an integer$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_noninteger_batch_rejected_before_connecting[fraction]`

**KEEP** — Preserve this exact input class and independently specified outcomes: connect.assert_not_called() ; pytest.raises(ValueError, match='^Batch size must be an integer$').

Source: `tests/test_note_rules_and_maintenance.py:293`. Inputs: `{"size": "1.5"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `connect.assert_not_called() ; pytest.raises(ValueError, match='^Batch size must be an integer$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_more_wrong_batch_types_rejected[whole-float]`

**KEEP** — Preserve this exact input class and independently specified outcomes: connect.assert_not_called() ; pytest.raises(ValueError, match='^Batch size must be an integer$').

Source: `tests/test_note_rules_and_maintenance.py:304`. Inputs: `{"size": "1.0"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `connect.assert_not_called() ; pytest.raises(ValueError, match='^Batch size must be an integer$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_more_wrong_batch_types_rejected[none]`

**MERGE** — Exact type guard rejects every non-int. Keep True (bool subclass hazard), 1.0 (integral float), 1.5 (fraction), and string; None offers no distinct coercion branch. Removal optional if null input is a separately documented contract.

Source: `tests/test_note_rules_and_maintenance.py:304`. Inputs: `{"size": "None"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `connect.assert_not_called() ; pytest.raises(ValueError, match='^Batch size must be an integer$')`.

Exact overlap IDs: `tests/test_note_rules_and_maintenance.py::test_more_wrong_batch_types_rejected[whole-float]`, `tests/test_note_rules_and_maintenance.py::test_more_wrong_batch_types_rejected[string]`.

### `tests/test_note_rules_and_maintenance.py::test_more_wrong_batch_types_rejected[string]`

**KEEP** — Preserve this exact input class and independently specified outcomes: connect.assert_not_called() ; pytest.raises(ValueError, match='^Batch size must be an integer$').

Source: `tests/test_note_rules_and_maintenance.py:304`. Inputs: `{"size": "'100'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `connect.assert_not_called() ; pytest.raises(ValueError, match='^Batch size must be an integer$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_draft_flag_requires_boolean[text]`

**KEEP** — Text false, integer1 and None must reject before producing a save/delete decision. Integer1 specifically detects bool/int conflation.

Source: `tests/test_note_rules_and_maintenance.py:314`. Inputs: `{"draft": "'false'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match='^is_draft must be a boolean$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_draft_flag_requires_boolean[integer]`

**KEEP** — Text false, integer1 and None must reject before producing a save/delete decision. Integer1 specifically detects bool/int conflation.

Source: `tests/test_note_rules_and_maintenance.py:314`. Inputs: `{"draft": "1"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match='^is_draft must be a boolean$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_draft_flag_requires_boolean[none]`

**KEEP** — Text false, integer1 and None must reject before producing a save/delete decision. Integer1 specifically detects bool/int conflation.

Source: `tests/test_note_rules_and_maintenance.py:314`. Inputs: `{"draft": "None"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match='^is_draft must be a boolean$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_cli_once_runs_one_cycle_without_sleep`

**KEEP** — --once must prompt once, run exactly one cycle with password, print exact counts and skip sleep; mocks bound potentially looping behavior.

Source: `tests/test_note_rules_and_maintenance.py:320`. Inputs: `{}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert output == 'Expired title-only notes: 2; purged deleted notes: 3\n' ; assert 'synthetic-secret' not in output ; prompt.assert_called_once() ; cycle.assert_called_once_with('synthetic-secret') ; sleep.assert_not_called()`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_cli_repeats_at_chosen_interval_and_stops_on_interrupt[args0-60]`

**KEEP** — Default60/custom10 intervals and three-cycle KeyboardInterrupt stop exercise scheduler default, option forwarding and graceful interruption with exact count output.

Source: `tests/test_note_rules_and_maintenance.py:337`. Inputs: `{"args": "[]", "interval": "60"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert cycle.call_args_list == [call('synthetic-secret')] * 3 ; assert sleep.call_args_list == [call(interval), call(interval)] ; assert capsys.readouterr().out == 'Expired title-only notes: 0; purged deleted notes: 1\nExpired title-only notes: 2; purged deleted notes: 0\nMaintenance stopped\n'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_cli_repeats_at_chosen_interval_and_stops_on_interrupt[args1-10]`

**KEEP** — Default60/custom10 intervals and three-cycle KeyboardInterrupt stop exercise scheduler default, option forwarding and graceful interruption with exact count output.

Source: `tests/test_note_rules_and_maintenance.py:337`. Inputs: `{"args": "['--interval', '10']", "interval": "10"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert cycle.call_args_list == [call('synthetic-secret')] * 3 ; assert sleep.call_args_list == [call(interval), call(interval)] ; assert capsys.readouterr().out == 'Expired title-only notes: 0; purged deleted notes: 1\nExpired title-only notes: 2; purged deleted notes: 0\nMaintenance stopped\n'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_cli_rejects_bad_interval_before_password_or_work[-1]`

**MERGE** — Same args.interval < 10 branch as 9; keep 9 boundary and abc argparse conversion. Negative/zero semantics have no separate worker branch.

Source: `tests/test_note_rules_and_maintenance.py:353`. Inputs: `{"interval": "'-1'"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert error.value.code == 2 ; prompt.assert_not_called() ; cycle.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_note_rules_and_maintenance.py::test_cli_rejects_bad_interval_before_password_or_work[9]`, `tests/test_note_rules_and_maintenance.py::test_cli_rejects_bad_interval_before_password_or_work[abc]`.

### `tests/test_note_rules_and_maintenance.py::test_cli_rejects_bad_interval_before_password_or_work[0]`

**MERGE** — Same args.interval < 10 branch as 9; keep 9 boundary and abc argparse conversion. Negative/zero semantics have no separate worker branch.

Source: `tests/test_note_rules_and_maintenance.py:353`. Inputs: `{"interval": "'0'"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert error.value.code == 2 ; prompt.assert_not_called() ; cycle.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_note_rules_and_maintenance.py::test_cli_rejects_bad_interval_before_password_or_work[9]`, `tests/test_note_rules_and_maintenance.py::test_cli_rejects_bad_interval_before_password_or_work[abc]`.

### `tests/test_note_rules_and_maintenance.py::test_cli_rejects_bad_interval_before_password_or_work[9]`

**KEEP** — Preserve this exact input class and independently specified outcomes: assert error.value.code == 2 ; prompt.assert_not_called() ; cycle.assert_not_called() ; pytest.raises(SystemExit).

Source: `tests/test_note_rules_and_maintenance.py:353`. Inputs: `{"interval": "'9'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.code == 2 ; prompt.assert_not_called() ; cycle.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_cli_rejects_bad_interval_before_password_or_work[abc]`

**KEEP** — Preserve this exact input class and independently specified outcomes: assert error.value.code == 2 ; prompt.assert_not_called() ; cycle.assert_not_called() ; pytest.raises(SystemExit).

Source: `tests/test_note_rules_and_maintenance.py:353`. Inputs: `{"interval": "'abc'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert error.value.code == 2 ; prompt.assert_not_called() ; cycle.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_cli_error_hides_credentials_and_stops[connection]`

**KEEP** — OperationalError versus RuntimeError cover two separately caught exception families. Both stop after one attempt without sleep/output and hide secret from SystemExit.

Source: `tests/test_note_rules_and_maintenance.py:366`. Inputs: `{"failure": "'connection'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert 'Maintenance failed' in str(error.value.code) ; assert secret not in str(error.value.code) ; assert (output.out, output.err) == ('', '') ; cycle.assert_called_once() ; sleep.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_cli_error_hides_credentials_and_stops[identity]`

**KEEP** — OperationalError versus RuntimeError cover two separately caught exception families. Both stop after one attempt without sleep/output and hide secret from SystemExit.

Source: `tests/test_note_rules_and_maintenance.py:366`. Inputs: `{"failure": "'identity'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert 'Maintenance failed' in str(error.value.code) ; assert secret not in str(error.value.code) ; assert (output.out, output.err) == ('', '') ; cycle.assert_called_once() ; sleep.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_malformed_identity_stops_before_cleanup[identity0]`

**KEEP** — String conversion failure, None identifier and missing row exercise conversion/unpacking failures. Only fingerprint SQL may occur; cleanup must never follow.

Source: `tests/test_note_rules_and_maintenance.py:388`. Inputs: `{"identity": "('merlin_d6', 'bad')"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert cursor.execute.call_args_list == [call('SELECT current_database(), system_identifier FROM pg_control_system()')] ; pytest.raises(RuntimeError, match='^Refusing malformed Day 6 database identity$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_malformed_identity_stops_before_cleanup[identity1]`

**KEEP** — String conversion failure, None identifier and missing row exercise conversion/unpacking failures. Only fingerprint SQL may occur; cleanup must never follow.

Source: `tests/test_note_rules_and_maintenance.py:388`. Inputs: `{"identity": "('merlin_d6', None)"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert cursor.execute.call_args_list == [call('SELECT current_database(), system_identifier FROM pg_control_system()')] ; pytest.raises(RuntimeError, match='^Refusing malformed Day 6 database identity$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_malformed_identity_stops_before_cleanup[None]`

**KEEP** — String conversion failure, None identifier and missing row exercise conversion/unpacking failures. Only fingerprint SQL may occur; cleanup must never follow.

Source: `tests/test_note_rules_and_maintenance.py:388`. Inputs: `{"identity": "None"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert cursor.execute.call_args_list == [call('SELECT current_database(), system_identifier FROM pg_control_system()')] ; pytest.raises(RuntimeError, match='^Refusing malformed Day 6 database identity$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_identity_query_failure_stops_before_cleanup`

**KEEP** — Fingerprint query error must propagate as identical exception object through connection context, before any cleanup statement.

Source: `tests/test_note_rules_and_maintenance.py:399`. Inputs: `{}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert cursor.execute.call_args_list == [call('SELECT current_database(), system_identifier FROM pg_control_system()')] ; assert error.value is failure ; assert connect.return_value.__exit__.call_args.args[1] is failure ; pytest.raises(psycopg.OperationalError)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[True-title]`

**KEEP** — Each public path already rejects integer and bytes; bool/list/dict all fail the same isinstance(str) guard. Retain boolean and one container per path for realistic accidental coercion; list versus dict is a reducible cross-product.

Source: `tests/test_note_rules_and_maintenance.py:417`. Inputs: `{"value": "True", "field": "'title'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match='^Text must be a string$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[True-body]`

**KEEP** — Each public path already rejects integer and bytes; bool/list/dict all fail the same isinstance(str) guard. Retain boolean and one container per path for realistic accidental coercion; list versus dict is a reducible cross-product.

Source: `tests/test_note_rules_and_maintenance.py:417`. Inputs: `{"value": "True", "field": "'body'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match='^Text must be a string$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[True-email]`

**KEEP** — Each public path already rejects integer and bytes; bool/list/dict all fail the same isinstance(str) guard. Retain boolean and one container per path for realistic accidental coercion; list versus dict is a reducible cross-product.

Source: `tests/test_note_rules_and_maintenance.py:417`. Inputs: `{"value": "True", "field": "'email'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match='^Text must be a string$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[value1-title]`

**KEEP** — Each public path already rejects integer and bytes; bool/list/dict all fail the same isinstance(str) guard. Retain boolean and one container per path for realistic accidental coercion; list versus dict is a reducible cross-product.

Source: `tests/test_note_rules_and_maintenance.py:417`. Inputs: `{"value": "[]", "field": "'title'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match='^Text must be a string$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[value1-body]`

**KEEP** — Each public path already rejects integer and bytes; bool/list/dict all fail the same isinstance(str) guard. Retain boolean and one container per path for realistic accidental coercion; list versus dict is a reducible cross-product.

Source: `tests/test_note_rules_and_maintenance.py:417`. Inputs: `{"value": "[]", "field": "'body'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match='^Text must be a string$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[value1-email]`

**KEEP** — Each public path already rejects integer and bytes; bool/list/dict all fail the same isinstance(str) guard. Retain boolean and one container per path for realistic accidental coercion; list versus dict is a reducible cross-product.

Source: `tests/test_note_rules_and_maintenance.py:417`. Inputs: `{"value": "[]", "field": "'email'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(ValueError, match='^Text must be a string$')`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[value2-title]`

**MERGE** — Each public path already rejects integer and bytes; bool/list/dict all fail the same isinstance(str) guard. Retain boolean and one container per path for realistic accidental coercion; list versus dict is a reducible cross-product.

Source: `tests/test_note_rules_and_maintenance.py:417`. Inputs: `{"value": "{}", "field": "'title'"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `pytest.raises(ValueError, match='^Text must be a string$')`.

Exact overlap IDs: `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[True-title]`, `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[True-body]`, `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[True-email]`, `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[value1-title]`, `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[value1-body]`, `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[value1-email]`.

### `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[value2-body]`

**MERGE** — Each public path already rejects integer and bytes; bool/list/dict all fail the same isinstance(str) guard. Retain boolean and one container per path for realistic accidental coercion; list versus dict is a reducible cross-product.

Source: `tests/test_note_rules_and_maintenance.py:417`. Inputs: `{"value": "{}", "field": "'body'"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `pytest.raises(ValueError, match='^Text must be a string$')`.

Exact overlap IDs: `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[True-title]`, `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[True-body]`, `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[True-email]`, `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[value1-title]`, `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[value1-body]`, `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[value1-email]`.

### `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[value2-email]`

**MERGE** — Each public path already rejects integer and bytes; bool/list/dict all fail the same isinstance(str) guard. Retain boolean and one container per path for realistic accidental coercion; list versus dict is a reducible cross-product.

Source: `tests/test_note_rules_and_maintenance.py:417`. Inputs: `{"value": "{}", "field": "'email'"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `pytest.raises(ValueError, match='^Text must be a string$')`.

Exact overlap IDs: `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[True-title]`, `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[True-body]`, `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[True-email]`, `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[value1-title]`, `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[value1-body]`, `tests/test_note_rules_and_maintenance.py::test_container_and_boolean_text_is_rejected[value1-email]`.

### `tests/test_note_rules_and_maintenance.py::test_default_save_deletes_a_fully_blank_note`

**KEEP** — Exact same None/None input as explicit-draft=False matrix, but omission of keyword uniquely checks the default parameter remains False.

Source: `tests/test_note_rules_and_maintenance.py:427`. Inputs: `{}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, '', True)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_nonblank_draft_keeps_exact_content[Title-]`

**KEEP** — Nonblank drafts must preserve title-only/body-only/both populated content; save-intent change must not strip text or force deletion.

Source: `tests/test_note_rules_and_maintenance.py:433`. Inputs: `{"title": "'Title'", "body": "''"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (title, body, False)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_nonblank_draft_keeps_exact_content[None-body]`

**KEEP** — Nonblank drafts must preserve title-only/body-only/both populated content; save-intent change must not strip text or force deletion.

Source: `tests/test_note_rules_and_maintenance.py:433`. Inputs: `{"title": "None", "body": "'body'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (title, body, False)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_nonblank_draft_keeps_exact_content[ Title - body ]`

**KEEP** — Nonblank drafts must preserve title-only/body-only/both populated content; save-intent change must not strip text or force deletion.

Source: `tests/test_note_rules_and_maintenance.py:433`. Inputs: `{"title": "' Title '", "body": "' body '"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (title, body, False)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_email_normalization_is_idempotent`

**KEEP** — Checks first normalization and normalization of its result against independent literal expected casing; repeated use cannot corrupt display email.

Source: `tests/test_note_rules_and_maintenance.py:438`. Inputs: `{}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert first == 'Mixed@Example.test' ; assert normalize_email(first) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_cli_help_and_bad_flags_do_not_prompt_or_work[args0-0]`

**KEEP** — Help exits0 and unknown option exits2; neither may request credentials, perform work or sleep.

Source: `tests/test_note_rules_and_maintenance.py:445`. Inputs: `{"args": "['--help']", "code": "0"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert result.value.code == code ; prompt.assert_not_called() ; cycle.assert_not_called() ; sleep.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_cli_help_and_bad_flags_do_not_prompt_or_work[args1-2]`

**KEEP** — Help exits0 and unknown option exits2; neither may request credentials, perform work or sleep.

Source: `tests/test_note_rules_and_maintenance.py:445`. Inputs: `{"args": "['--unknown']", "code": "2"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert result.value.code == code ; prompt.assert_not_called() ; cycle.assert_not_called() ; sleep.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+0009]`

**KEEP** — Literal independent Unicode corpus case U+0009. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "9"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+000A]`

**KEEP** — Literal independent Unicode corpus case U+000A. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "10"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+000B]`

**KEEP** — Literal independent Unicode corpus case U+000B. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "11"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+000C]`

**KEEP** — Literal independent Unicode corpus case U+000C. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "12"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+000D]`

**KEEP** — Literal independent Unicode corpus case U+000D. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "13"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+001C]`

**KEEP** — Literal independent Unicode corpus case U+001C. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "28"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+001D]`

**KEEP** — Literal independent Unicode corpus case U+001D. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "29"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+001E]`

**KEEP** — Literal independent Unicode corpus case U+001E. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "30"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+001F]`

**KEEP** — Literal independent Unicode corpus case U+001F. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "31"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+0020]`

**KEEP** — Literal independent Unicode corpus case U+0020. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "32"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+0085]`

**KEEP** — Literal independent Unicode corpus case U+0085. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "133"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+00A0]`

**KEEP** — Literal independent Unicode corpus case U+00A0. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "160"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+1680]`

**KEEP** — Literal independent Unicode corpus case U+1680. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "5760"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+2000]`

**KEEP** — Literal independent Unicode corpus case U+2000. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "8192"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+2001]`

**KEEP** — Literal independent Unicode corpus case U+2001. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "8193"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+2002]`

**KEEP** — Literal independent Unicode corpus case U+2002. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "8194"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+2003]`

**KEEP** — Literal independent Unicode corpus case U+2003. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "8195"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+2004]`

**KEEP** — Literal independent Unicode corpus case U+2004. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "8196"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+2005]`

**KEEP** — Literal independent Unicode corpus case U+2005. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "8197"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+2006]`

**KEEP** — Literal independent Unicode corpus case U+2006. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "8198"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+2007]`

**KEEP** — Literal independent Unicode corpus case U+2007. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "8199"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+2008]`

**KEEP** — Literal independent Unicode corpus case U+2008. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "8200"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+2009]`

**KEEP** — Literal independent Unicode corpus case U+2009. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "8201"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+200A]`

**KEEP** — Literal independent Unicode corpus case U+200A. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "8202"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+2028]`

**KEEP** — Literal independent Unicode corpus case U+2028. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "8232"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+2029]`

**KEEP** — Literal independent Unicode corpus case U+2029. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "8233"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+202F]`

**KEEP** — Literal independent Unicode corpus case U+202F. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "8239"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+205F]`

**KEEP** — Literal independent Unicode corpus case U+205F. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "8287"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_unicode_whitespace_note_and_email_contract[U+3000]`

**KEEP** — Literal independent Unicode corpus case U+3000. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:465`. Inputs: `{"codepoint": "12288"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (result.title, result.body, result.delete_on_save) == (None, space, True) ; assert normalize_email(space + 'Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+0009]`

**KEEP** — Literal independent Unicode corpus case U+0009. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "9"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+000A]`

**KEEP** — Literal independent Unicode corpus case U+000A. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "10"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+000B]`

**KEEP** — Literal independent Unicode corpus case U+000B. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "11"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+000C]`

**KEEP** — Literal independent Unicode corpus case U+000C. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "12"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+000D]`

**KEEP** — Literal independent Unicode corpus case U+000D. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "13"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+001C]`

**KEEP** — Literal independent Unicode corpus case U+001C. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "28"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+001D]`

**KEEP** — Literal independent Unicode corpus case U+001D. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "29"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+001E]`

**KEEP** — Literal independent Unicode corpus case U+001E. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "30"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+001F]`

**KEEP** — Literal independent Unicode corpus case U+001F. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "31"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+0020]`

**KEEP** — Literal independent Unicode corpus case U+0020. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "32"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+0085]`

**KEEP** — Literal independent Unicode corpus case U+0085. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "133"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+00A0]`

**KEEP** — Literal independent Unicode corpus case U+00A0. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "160"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+1680]`

**KEEP** — Literal independent Unicode corpus case U+1680. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "5760"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+2000]`

**KEEP** — Literal independent Unicode corpus case U+2000. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "8192"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+2001]`

**KEEP** — Literal independent Unicode corpus case U+2001. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "8193"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+2002]`

**KEEP** — Literal independent Unicode corpus case U+2002. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "8194"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+2003]`

**KEEP** — Literal independent Unicode corpus case U+2003. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "8195"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+2004]`

**KEEP** — Literal independent Unicode corpus case U+2004. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "8196"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+2005]`

**KEEP** — Literal independent Unicode corpus case U+2005. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "8197"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+2006]`

**KEEP** — Literal independent Unicode corpus case U+2006. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "8198"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+2007]`

**KEEP** — Literal independent Unicode corpus case U+2007. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "8199"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+2008]`

**KEEP** — Literal independent Unicode corpus case U+2008. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "8200"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+2009]`

**KEEP** — Literal independent Unicode corpus case U+2009. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "8201"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+200A]`

**KEEP** — Literal independent Unicode corpus case U+200A. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "8202"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+2028]`

**KEEP** — Literal independent Unicode corpus case U+2028. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "8232"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+2029]`

**KEEP** — Literal independent Unicode corpus case U+2029. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "8233"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+202F]`

**KEEP** — Literal independent Unicode corpus case U+202F. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "8239"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+205F]`

**KEEP** — Literal independent Unicode corpus case U+205F. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "8287"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts[U+3000]`

**KEEP** — Literal independent Unicode corpus case U+3000. Keep pinned contract coverage: distinct code points are data-domain requirements, not interchangeable mocks; second whitespace test adds title/draft/one-sided email branches.

Source: `tests/test_note_rules_and_maintenance.py:473`. Inputs: `{"codepoint": "12288"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False) ; assert (real.title, real.body, real.delete_on_save) == (space + 'Title' + space, space + 'Body' + space, False) ; assert normalize_email(space) is None ; assert normalize_email(space + 'Mixed@Example.test') == 'Mixed@Example.test' ; assert normalize_email('Mixed@Example.test' + space) == 'Mixed@Example.test'`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invisible_nonwhitespace_remains_real_content[\u200b]`

**KEEP** — U+200B/U+FEFF/U+2060 are invisible yet nonwhitespace. Explicit negative classification guards overbroad stripping/deletion.

Source: `tests/test_note_rules_and_maintenance.py:485`. Inputs: `{"text": "'\\u200b'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (note.title, note.body, note.delete_on_save) == (text, text, False) ; assert normalize_email(text) == text`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invisible_nonwhitespace_remains_real_content[\ufeff]`

**KEEP** — U+200B/U+FEFF/U+2060 are invisible yet nonwhitespace. Explicit negative classification guards overbroad stripping/deletion.

Source: `tests/test_note_rules_and_maintenance.py:485`. Inputs: `{"text": "'\\ufeff'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (note.title, note.body, note.delete_on_save) == (text, text, False) ; assert normalize_email(text) == text`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_invisible_nonwhitespace_remains_real_content[\u2060]`

**KEEP** — U+200B/U+FEFF/U+2060 are invisible yet nonwhitespace. Explicit negative classification guards overbroad stripping/deletion.

Source: `tests/test_note_rules_and_maintenance.py:485`. Inputs: `{"text": "'\\u2060'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert (note.title, note.body, note.delete_on_save) == (text, text, False) ; assert normalize_email(text) == text`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_cli_malformed_identity_is_sanitized_and_never_runs_cleanup[identity0]`

**KEEP** — Runs real main plus run_once with mocked connector: malformed identity must become sanitized SystemExit, propagate RuntimeError through context, skip sleep and issue fingerprint query only.

Source: `tests/test_note_rules_and_maintenance.py:493`. Inputs: `{"identity": "('merlin_d6', 'synthetic-private-identifier')"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert cursor.execute.call_args_list == [call('SELECT current_database(), system_identifier FROM pg_control_system()')] ; assert capsys.readouterr() == ('', '') ; assert 'Maintenance failed' in str(result.value.code) ; assert 'synthetic-private' not in str(result.value.code) ; assert connect.return_value.__exit__.call_args.args[0] is RuntimeError ; sleep.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_cli_malformed_identity_is_sanitized_and_never_runs_cleanup[identity1]`

**KEEP** — Runs real main plus run_once with mocked connector: malformed identity must become sanitized SystemExit, propagate RuntimeError through context, skip sleep and issue fingerprint query only.

Source: `tests/test_note_rules_and_maintenance.py:493`. Inputs: `{"identity": "('merlin_d6', None)"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert cursor.execute.call_args_list == [call('SELECT current_database(), system_identifier FROM pg_control_system()')] ; assert capsys.readouterr() == ('', '') ; assert 'Maintenance failed' in str(result.value.code) ; assert 'synthetic-private' not in str(result.value.code) ; assert connect.return_value.__exit__.call_args.args[0] is RuntimeError ; sleep.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_note_rules_and_maintenance.py::test_cli_malformed_identity_is_sanitized_and_never_runs_cleanup[None]`

**KEEP** — Runs real main plus run_once with mocked connector: malformed identity must become sanitized SystemExit, propagate RuntimeError through context, skip sleep and issue fingerprint query only.

Source: `tests/test_note_rules_and_maintenance.py:493`. Inputs: `{"identity": "None"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert cursor.execute.call_args_list == [call('SELECT current_database(), system_identifier FROM pg_control_system()')] ; assert capsys.readouterr() == ('', '') ; assert 'Maintenance failed' in str(result.value.code) ; assert 'synthetic-private' not in str(result.value.code) ; assert connect.return_value.__exit__.call_args.args[0] is RuntimeError ; sleep.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_database_connectivity_probe.py::test_probe_is_read_only_before_its_only_query`

**KEEP** — Keep exact call sequence, binding, connector target, or exception-context contract. Mock context assertions prove Python ordering/propagation only; they cannot establish SQL atomicity, PostgreSQL read-only mode, permissions or real rollback.

Source: `tests/test_database_connectivity_probe.py:18`. Inputs: `{}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert cursor.execute.call_args_list == [call('SELECT current_database(), current_user;')] ; assert output.out == "PROBE SUCCESS: Connected to database 'merlin_d6' as user 'merlin_d6'.\n" ; assert output.err == '' ; assert conn.read_only is True ; assert query == 'SELECT current_database(), current_user;' ; assert result.value.code == 0 ; assert connect.return_value.__exit__.call_args.args == (None, None, None) ; cursor.fetchone.assert_called_once_with() ; prompt.assert_called_once_with(prompt='Password: ', stream=None) ; connect.assert_called_once_with(host='127.0.0.1', port=55432, dbname='merlin_d6', user='merlin_d6', password='synthetic-secret', connect_timeout=3) ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_database_connectivity_probe.py::test_operational_failure_exits_without_success_or_secret[connect]`

**KEEP** — Connection creation versus query failure differ in acquired context. Both exit1 without success/secret; query error must reach context and prevent fetch.

Source: `tests/test_database_connectivity_probe.py:46`. Inputs: `{"stage": "'connect'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert output.out == '' ; assert 'DB Probe Failed:' in output.err ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; assert connect.return_value.__exit__.call_args.args[1] is failure ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_database_connectivity_probe.py::test_operational_failure_exits_without_success_or_secret[query]`

**KEEP** — Connection creation versus query failure differ in acquired context. Both exit1 without success/secret; query error must reach context and prevent fetch.

Source: `tests/test_database_connectivity_probe.py:46`. Inputs: `{"stage": "'query'"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert output.out == '' ; assert 'DB Probe Failed:' in output.err ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; assert connect.return_value.__exit__.call_args.args[1] is failure ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_database_connectivity_probe.py::test_query_permission_error_is_sanitized`

**MERGE** — Same ProgrammingError/query path as matrix case; matrix adds failure prefix and no fetch assertions.

Source: `tests/test_database_connectivity_probe.py:72`. Inputs: `{}`.

Classification: assertion-subsumed structural duplicate; confidence: high for consolidation preserving assertions.

Assertions: `assert output.out == '' ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[query-ProgrammingError]`.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[enter-OperationalError]`

**KEEP** — Lifecycle position matters: enter can fail before/after successful query; require exit 1, no success, no secret, and no later operations where asserted.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'enter'", "error_type": "<class 'psycopg.OperationalError'>"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[enter-ProgrammingError]`

**MERGE** — True Cartesian excess: same surrounding try and except psycopg.Error catches every listed subclass at every stage. Keep OperationalError for this stage and all three other exception subclasses at query. This retains taxonomy against future narrowing to an OperationalError/ProgrammingError tuple; subclass-by-stage interaction is conditionally reducible because no current source branch distinguishes that interaction.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'enter'", "error_type": "<class 'psycopg.ProgrammingError'>"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[enter-OperationalError]`.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[enter-DataError]`

**MERGE** — True Cartesian excess: same surrounding try and except psycopg.Error catches every listed subclass at every stage. Keep OperationalError for this stage and all three other exception subclasses at query. This retains taxonomy against future narrowing to an OperationalError/ProgrammingError tuple; subclass-by-stage interaction is conditionally reducible because no current source branch distinguishes that interaction.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'enter'", "error_type": "<class 'psycopg.DataError'>"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[enter-OperationalError]`.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[enter-InternalError]`

**MERGE** — True Cartesian excess: same surrounding try and except psycopg.Error catches every listed subclass at every stage. Keep OperationalError for this stage and all three other exception subclasses at query. This retains taxonomy against future narrowing to an OperationalError/ProgrammingError tuple; subclass-by-stage interaction is conditionally reducible because no current source branch distinguishes that interaction.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'enter'", "error_type": "<class 'psycopg.InternalError'>"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[enter-OperationalError]`.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[read_only-OperationalError]`

**KEEP** — Lifecycle position matters: read_only can fail before/after successful query; require exit 1, no success, no secret, and no later operations where asserted.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'read_only'", "error_type": "<class 'psycopg.OperationalError'>"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[read_only-ProgrammingError]`

**MERGE** — True Cartesian excess: same surrounding try and except psycopg.Error catches every listed subclass at every stage. Keep OperationalError for this stage and all three other exception subclasses at query. This retains taxonomy against future narrowing to an OperationalError/ProgrammingError tuple; subclass-by-stage interaction is conditionally reducible because no current source branch distinguishes that interaction.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'read_only'", "error_type": "<class 'psycopg.ProgrammingError'>"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[read_only-OperationalError]`.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[read_only-DataError]`

**MERGE** — True Cartesian excess: same surrounding try and except psycopg.Error catches every listed subclass at every stage. Keep OperationalError for this stage and all three other exception subclasses at query. This retains taxonomy against future narrowing to an OperationalError/ProgrammingError tuple; subclass-by-stage interaction is conditionally reducible because no current source branch distinguishes that interaction.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'read_only'", "error_type": "<class 'psycopg.DataError'>"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[read_only-OperationalError]`.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[read_only-InternalError]`

**MERGE** — True Cartesian excess: same surrounding try and except psycopg.Error catches every listed subclass at every stage. Keep OperationalError for this stage and all three other exception subclasses at query. This retains taxonomy against future narrowing to an OperationalError/ProgrammingError tuple; subclass-by-stage interaction is conditionally reducible because no current source branch distinguishes that interaction.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'read_only'", "error_type": "<class 'psycopg.InternalError'>"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[read_only-OperationalError]`.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[cursor-OperationalError]`

**KEEP** — Lifecycle position matters: cursor can fail before/after successful query; require exit 1, no success, no secret, and no later operations where asserted.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'cursor'", "error_type": "<class 'psycopg.OperationalError'>"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[cursor-ProgrammingError]`

**MERGE** — True Cartesian excess: same surrounding try and except psycopg.Error catches every listed subclass at every stage. Keep OperationalError for this stage and all three other exception subclasses at query. This retains taxonomy against future narrowing to an OperationalError/ProgrammingError tuple; subclass-by-stage interaction is conditionally reducible because no current source branch distinguishes that interaction.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'cursor'", "error_type": "<class 'psycopg.ProgrammingError'>"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[cursor-OperationalError]`.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[cursor-DataError]`

**MERGE** — True Cartesian excess: same surrounding try and except psycopg.Error catches every listed subclass at every stage. Keep OperationalError for this stage and all three other exception subclasses at query. This retains taxonomy against future narrowing to an OperationalError/ProgrammingError tuple; subclass-by-stage interaction is conditionally reducible because no current source branch distinguishes that interaction.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'cursor'", "error_type": "<class 'psycopg.DataError'>"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[cursor-OperationalError]`.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[cursor-InternalError]`

**MERGE** — True Cartesian excess: same surrounding try and except psycopg.Error catches every listed subclass at every stage. Keep OperationalError for this stage and all three other exception subclasses at query. This retains taxonomy against future narrowing to an OperationalError/ProgrammingError tuple; subclass-by-stage interaction is conditionally reducible because no current source branch distinguishes that interaction.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'cursor'", "error_type": "<class 'psycopg.InternalError'>"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[cursor-OperationalError]`.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[query-OperationalError]`

**KEEP** — Lifecycle position matters: query can fail before/after successful query; require exit 1, no success, no secret, and no later operations where asserted.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'query'", "error_type": "<class 'psycopg.OperationalError'>"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[query-ProgrammingError]`

**KEEP** — Lifecycle position matters: query can fail before/after successful query; require exit 1, no success, no secret, and no later operations where asserted.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'query'", "error_type": "<class 'psycopg.ProgrammingError'>"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[query-DataError]`

**KEEP** — Lifecycle position matters: query can fail before/after successful query; require exit 1, no success, no secret, and no later operations where asserted.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'query'", "error_type": "<class 'psycopg.DataError'>"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[query-InternalError]`

**KEEP** — Lifecycle position matters: query can fail before/after successful query; require exit 1, no success, no secret, and no later operations where asserted.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'query'", "error_type": "<class 'psycopg.InternalError'>"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[fetch-OperationalError]`

**KEEP** — Lifecycle position matters: fetch can fail before/after successful query; require exit 1, no success, no secret, and no later operations where asserted.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'fetch'", "error_type": "<class 'psycopg.OperationalError'>"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[fetch-ProgrammingError]`

**MERGE** — True Cartesian excess: same surrounding try and except psycopg.Error catches every listed subclass at every stage. Keep OperationalError for this stage and all three other exception subclasses at query. This retains taxonomy against future narrowing to an OperationalError/ProgrammingError tuple; subclass-by-stage interaction is conditionally reducible because no current source branch distinguishes that interaction.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'fetch'", "error_type": "<class 'psycopg.ProgrammingError'>"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[fetch-OperationalError]`.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[fetch-DataError]`

**MERGE** — True Cartesian excess: same surrounding try and except psycopg.Error catches every listed subclass at every stage. Keep OperationalError for this stage and all three other exception subclasses at query. This retains taxonomy against future narrowing to an OperationalError/ProgrammingError tuple; subclass-by-stage interaction is conditionally reducible because no current source branch distinguishes that interaction.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'fetch'", "error_type": "<class 'psycopg.DataError'>"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[fetch-OperationalError]`.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[fetch-InternalError]`

**MERGE** — True Cartesian excess: same surrounding try and except psycopg.Error catches every listed subclass at every stage. Keep OperationalError for this stage and all three other exception subclasses at query. This retains taxonomy against future narrowing to an OperationalError/ProgrammingError tuple; subclass-by-stage interaction is conditionally reducible because no current source branch distinguishes that interaction.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'fetch'", "error_type": "<class 'psycopg.InternalError'>"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[fetch-OperationalError]`.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[exit-OperationalError]`

**KEEP** — Lifecycle position matters: exit can fail before/after successful query; require exit 1, no success, no secret, and no later operations where asserted.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'exit'", "error_type": "<class 'psycopg.OperationalError'>"}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: none independently established.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[exit-ProgrammingError]`

**MERGE** — True Cartesian excess: same surrounding try and except psycopg.Error catches every listed subclass at every stage. Keep OperationalError for this stage and all three other exception subclasses at query. This retains taxonomy against future narrowing to an OperationalError/ProgrammingError tuple; subclass-by-stage interaction is conditionally reducible because no current source branch distinguishes that interaction.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'exit'", "error_type": "<class 'psycopg.ProgrammingError'>"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[exit-OperationalError]`.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[exit-DataError]`

**MERGE** — True Cartesian excess: same surrounding try and except psycopg.Error catches every listed subclass at every stage. Keep OperationalError for this stage and all three other exception subclasses at query. This retains taxonomy against future narrowing to an OperationalError/ProgrammingError tuple; subclass-by-stage interaction is conditionally reducible because no current source branch distinguishes that interaction.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'exit'", "error_type": "<class 'psycopg.DataError'>"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[exit-OperationalError]`.

### `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[exit-InternalError]`

**MERGE** — True Cartesian excess: same surrounding try and except psycopg.Error catches every listed subclass at every stage. Keep OperationalError for this stage and all three other exception subclasses at query. This retains taxonomy against future narrowing to an OperationalError/ProgrammingError tuple; subclass-by-stage interaction is conditionally reducible because no current source branch distinguishes that interaction.

Source: `tests/test_database_connectivity_probe.py:90`. Inputs: `{"stage": "'exit'", "error_type": "<class 'psycopg.InternalError'>"}`.

Classification: conditional representative candidate; confidence: conditional; no deletion approved.

Assertions: `assert output.out == '' ; assert output.err.startswith('DB Probe Failed:') ; assert 'synthetic-private-password' not in output.err ; assert result.value.code == 1 ; cursor.execute.assert_not_called() ; cursor.fetchone.assert_not_called() ; pytest.raises(SystemExit)`.

Exact overlap IDs: `tests/test_database_connectivity_probe.py::test_database_errors_at_each_stage_are_sanitized[exit-OperationalError]`.

### `tests/test_database_connectivity_probe.py::test_unrelated_programming_bug_is_not_masked`

**KEEP** — RuntimeError must escape unchanged; an except Exception handler would hide a programming defect.

Source: `tests/test_database_connectivity_probe.py:126`. Inputs: `{}`.

Classification: retained behavioral or input partition; confidence: contract-based retention; universal necessity unproven.

Assertions: `pytest.raises(RuntimeError, match='^programming bug$')`.

Exact overlap IDs: none independently established.

## Every application fault

### `emoji-weight-one`

**KEEP** — Injects the specific behavioral change '4 if emoji.is_emoji(part) else 1' → '1 if emoji.is_emoji(part) else 1'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:23`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `e43f3fe80abb8025ee6e1c114d69f49d0952a4bdf68f5fdfccf1b829e87138e1`; exact overlaps: none.

Changed expressions: `{"old": "4 if emoji.is_emoji(part) else 1", "new": "1 if emoji.is_emoji(part) else 1"}`.

### `codepoint-instead-of-grapheme`

**KEEP** — Injects the specific behavioral change '_GRAPHEMES.findall(value)' → 'value'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:23`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `6d6d0927e95b65772e3eb0da8a4c561be27cad0cf5984d74c8c2852bb47651b5`; exact overlaps: none.

Changed expressions: `{"old": "_GRAPHEMES.findall(value)", "new": "value"}`.

### `title-bound-relaxed`

**KEEP** — Injects the specific behavioral change 'title_length > 175' → 'title_length > 176'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:53`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `05829dad7ca7d8f3409dad6a5f1f306931f9ed54d3fff7bf49d5192da1db625f`; exact overlaps: none.

Changed expressions: `{"old": "title_length > 175", "new": "title_length > 176"}`.

### `title-bound-too-strict`

**KEEP** — Injects the specific behavioral change 'title_length > 175' → 'title_length >= 175'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:53`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `a20aef334879983e68c6e94a333080127436df01234fdc88b7ad2868bee41d6f`; exact overlaps: none.

Changed expressions: `{"old": "title_length > 175", "new": "title_length >= 175"}`.

### `body-bound-relaxed`

**KEEP** — Injects the specific behavioral change 'weighted_length(body) > 7000' → 'weighted_length(body) > 7001'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:57`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `35de7f3a8420ad91dd317c7b27f8dd6655d0de57611562bd5c39b75ea2d48090`; exact overlaps: none.

Changed expressions: `{"old": "weighted_length(body) > 7000", "new": "weighted_length(body) > 7001"}`.

### `body-bound-too-strict`

**KEEP** — Injects the specific behavioral change 'weighted_length(body) > 7000' → 'weighted_length(body) >= 7000'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:57`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `d75f87e4a061fb0caa4a419e90a79d05335533633371bf34e0be8a0f24accc1a`; exact overlaps: none.

Changed expressions: `{"old": "weighted_length(body) > 7000", "new": "weighted_length(body) >= 7000"}`.

### `body-stripped`

**KEEP** — Injects the specific behavioral change 'body = "" if body is None else body' → 'body = "" if body is None else body.strip()'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:56`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `8c5ac4e638d22b51647622db4b568269ca0e215f243c4bdf77389f59adceeaf1`; exact overlaps: none.

Changed expressions: `{"old": "body = \"\" if body is None else body", "new": "body = \"\" if body is None else body.strip()"}`.

### `real-title-stripped`

**KEEP** — Injects the specific behavioral change 'return ValidatedNote(title, body,' → 'return ValidatedNote(None if title is None else title.strip(), body,'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:60`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `2761c7fe8cb536c4c1e5f80cf44d517e64c67ebc90b65118704955c62cb0574a`; exact overlaps: none.

Changed expressions: `{"old": "return ValidatedNote(title, body,", "new": "return ValidatedNote(None if title is None else title.strip(), body,"}`.

### `email-lowercased`

**KEEP** — Injects the specific behavioral change 'return value.strip() or None' → 'return value.strip().lower() or None'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:32`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `e8fcdd670474812ce7cc2a6fb6e1dfcf91df31c4273e89a58c6f57bf2479b51b`; exact overlaps: none.

Changed expressions: `{"old": "return value.strip() or None", "new": "return value.strip().lower() or None"}`.

### `blank-title-stored-empty`

**KEEP** — Injects the specific behavioral change 'if not title.strip():\n            title = None' → 'if not title.strip():\n            title = ""'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:51`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `d13236340ff6b349a1d514d2a021ef074cb4279f4ceb3935e8cfa0eaf578e799`; exact overlaps: none.

Changed expressions: `{"old": "if not title.strip():\n            title = None", "new": "if not title.strip():\n            title = \"\""}`.

### `draft-delete-protection-removed`

**KEEP** — Injects the specific behavioral change 'not is_draft and title is None and not body.strip()' → 'title is None and not body.strip()'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:60`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `f92d8f625cb7271078dd86c1f8bf12b0193ff5710eb8cb4b2250b00a9bd84ed0`; exact overlaps: none.

Changed expressions: `{"old": "not is_draft and title is None and not body.strip()", "new": "title is None and not body.strip()"}`.

### `nul-check-removed`

**KEEP** — Injects the specific behavioral change 'if "\\x00" in value:' → 'if False:'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:20`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `f68c88b39704ccac2fc2765c327aec52f2b0337bd28fc08da60eb46f15443c1e`; exact overlaps: none.

Changed expressions: `{"old": "if \"\\x00\" in value:", "new": "if False:"}`.

### `target-check-skipped`

**KEEP** — Injects the specific behavioral change '        verify_target(conn)\n' → '        pass\n'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:37`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `b86af6a852d5fd6bc6d01e0a5a6f05a37cc55b331f557e7728495e78e05a1c8a`; exact overlaps: none.

Changed expressions: `{"old": "        verify_target(conn)\n", "new": "        pass\n"}`.

### `identity-or-changed-to-and`

**KEEP** — Injects the specific behavioral change 'database != "merlin_d6" or int(identifier) != EXPECTED_CLUSTER' → 'database != "merlin_d6" and int(identifier) != EXPECTED_CLUSTER'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:25`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `6ebe89bbc5710fc44da2c94b0a827172d6f0dbb9f56beb521b75905532bfe15f`; exact overlaps: none.

Changed expressions: `{"old": "database != \"merlin_d6\" or int(identifier) != EXPECTED_CLUSTER", "new": "database != \"merlin_d6\" and int(identifier) != EXPECTED_CLUSTER"}`.

### `target-port-original-db`

**KEEP** — Injects the specific behavioral change 'port=55432' → 'port=5432'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:11`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `a1697be700df63d52d337b107b893a46ee786a0b57bb5aa48d730a4373cbcb25`; exact overlaps: none.

Changed expressions: `{"old": "port=55432", "new": "port=5432"}`.

### `batch1001-allowed`

**KEEP** — Injects the specific behavioral change '1 <= batch_size <= 1000' → '1 <= batch_size <= 1001'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:33`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `aa470389b7ea3da4f0b16f8375c689bfeed3e60563a1d02af1148fbfc0bd0415`; exact overlaps: none.

Changed expressions: `{"old": "1 <= batch_size <= 1000", "new": "1 <= batch_size <= 1001"}`.

### `lock-timeout-removed`

**KEEP** — Injects the specific behavioral change '            cur.execute("SET LOCAL lock_timeout = \'2s\'")\n' → ''. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:40`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `6110db4204153fe1864b265ba14e1ffaa8d2acdb0d3d3693de6e74b4f3c84727`; exact overlaps: none.

Changed expressions: `{"old": "            cur.execute(\"SET LOCAL lock_timeout = '2s'\")\n", "new": ""}`.

### `wrong-expiry-function`

**KEEP** — Injects the specific behavioral change 'SELECT public.cleanup_expired_blank_notes(%s)' → 'SELECT public.wrong_cleanup(%s)'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:44`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `e8c31c551b4fabdd7890bb6776cab14111ec85667d820e1273b09f33569f5e56`; exact overlaps: none.

Changed expressions: `{"old": "SELECT public.cleanup_expired_blank_notes(%s)", "new": "SELECT public.wrong_cleanup(%s)"}`.

### `once-flag-ignored`

**KEEP** — Injects the specific behavioral change 'if args.once:' → 'if False:'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:66`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `1284612bda930d531ade17e9c924991f128919f73765f8fe17e74b0725422b7f`; exact overlaps: none.

Changed expressions: `{"old": "if args.once:", "new": "if False:"}`.

### `custom-interval-ignored`

**KEEP** — Injects the specific behavioral change 'time.sleep(args.interval)' → 'time.sleep(60)'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:68`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `975d68b4b4e1cebda9d816420ed7a2bd2bbf429301a402ae8274d9ad740196c9`; exact overlaps: none.

Changed expressions: `{"old": "time.sleep(args.interval)", "new": "time.sleep(60)"}`.

### `cli-error-secret-leaked`

**KEEP** — Injects the specific behavioral change 'raise SystemExit("Maintenance failed; check target, migration and permissions. No credentials printed.")' → 'raise SystemExit("Maintenance failed: " + password)'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:73`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `7550578f36e7dd6d15ba826040b6030105d037474e19de3a45e92e581537b187`; exact overlaps: none.

Changed expressions: `{"old": "raise SystemExit(\"Maintenance failed; check target, migration and permissions. No credentials printed.\")", "new": "raise SystemExit(\"Maintenance failed: \" + password)"}`.

### `strict-batch-guard-removed`

**KEEP** — Injects the specific behavioral change 'if type(batch_size) is not int:' → 'if False:'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:31`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `893095e8932f19f592fd692c63a95f33e18412e9e919d236b2200aba9a2bca91`; exact overlaps: none.

Changed expressions: `{"old": "if type(batch_size) is not int:", "new": "if False:"}`.

### `strict-draft-guard-removed`

**KEEP** — Injects the specific behavioral change 'if not isinstance(is_draft, bool):' → 'if False:'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:46`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `b047e53d94cb786ba9928e4e80bb588811062824db7d3ac1b8fdfef7663b252d`; exact overlaps: none.

Changed expressions: `{"old": "if not isinstance(is_draft, bool):", "new": "if False:"}`.

### `utf8-guard-removed`

**KEEP** — Injects the specific behavioral change 'value.encode("utf-8")' → 'pass'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:17`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `53498771c564286b49d3ec7125231e38c7b086445194f86a203097bcc40b7d2f`; exact overlaps: none.

Changed expressions: `{"old": "value.encode(\"utf-8\")", "new": "pass"}`.

### `unexpected-extra-sql`

**KEEP** — Injects the specific behavioral change '            cur.execute("SELECT public.cleanup_expired_blank_notes(%s)", (batch_size,))' → '            cur.execute("SELECT 42")\n            cur.execute("SELECT public.cleanup_expired_blank_notes(%s)", (batch_size,))'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:44`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `df555941e9ac5331b2d2d278582c170c6a6a5fae32c696af6373e90c563fa6f6`; exact overlaps: none.

Changed expressions: `{"old": "            cur.execute(\"SELECT public.cleanup_expired_blank_notes(%s)\", (batch_size,))", "new": "            cur.execute(\"SELECT 42\")\n            cur.execute(\"SELECT public.cleanup_expired_blank_notes(%s)\", (batch_size,))"}`.

### `email-padding-retained`

**KEEP** — Injects the specific behavioral change 'return value.strip() or None' → 'return value or None'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:32`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `f36411166172931c182836588de62a1655b4358895ae165ab01db0dd08bc2cc9`; exact overlaps: none.

Changed expressions: `{"old": "return value.strip() or None", "new": "return value or None"}`.

### `optional-email-empty-string`

**KEEP** — Injects the specific behavioral change 'if value is None:\n        return None' → 'if value is None:\n        return ""'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:28`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `d9725001482294fe838d530c89bd12fa26b77d76f0b5bffae34d57510647c660`; exact overlaps: none.

Changed expressions: `{"old": "if value is None:\n        return None", "new": "if value is None:\n        return \"\""}`.

### `empty-email-empty-string`

**KEEP** — Injects the specific behavioral change 'return value.strip() or None' → 'return value.strip()'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:32`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `92c50b68a308fa56a249543d9137019fe6cd042112ee9fd63ca514f6a6feff91`; exact overlaps: none.

Changed expressions: `{"old": "return value.strip() or None", "new": "return value.strip()"}`.

### `none-body-not-normalized`

**KEEP** — Injects the specific behavioral change 'body = "" if body is None else body' → 'body = body'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:56`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `d823811c5d0b7b7f23483399c854ed996cc97df09c3b2f42e11aa655b42de9fe`; exact overlaps: none.

Changed expressions: `{"old": "body = \"\" if body is None else body", "new": "body = body"}`.

### `draft-title-bypasses-limit`

**KEEP** — Injects the specific behavioral change 'elif title_length > 175:' → 'elif not is_draft and title_length > 175:'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:53`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `665a225f95c962d97878237eac6b97d9fd27dc77e3db0a95f8563240b7a067ca`; exact overlaps: none.

Changed expressions: `{"old": "elif title_length > 175:", "new": "elif not is_draft and title_length > 175:"}`.

### `draft-body-bypasses-limit`

**KEEP** — Injects the specific behavioral change 'if weighted_length(body) > 7000:' → 'if not is_draft and weighted_length(body) > 7000:'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:57`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `62d99cb1b82ff42285f81d0cf1294b0f0e44ed0187cdb1130b568ee225921c26`; exact overlaps: none.

Changed expressions: `{"old": "if weighted_length(body) > 7000:", "new": "if not is_draft and weighted_length(body) > 7000:"}`.

### `save-default-is-draft`

**KEEP** — Injects the specific behavioral change 'is_draft: bool = False' → 'is_draft: bool = True'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:43`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `9038cf3653ff29a83c807e992247d276d3f417dc47f7e7f81904f547c4199aa9`; exact overlaps: none.

Changed expressions: `{"old": "is_draft: bool = False", "new": "is_draft: bool = True"}`.

### `text-type-guard-disabled`

**KEEP** — Injects the specific behavioral change 'if not isinstance(value, str):' → 'if False:'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:14`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `cd7836c210d3aca96e86957fdaa44ed8fbcf7d28ffc95e8c9daeca230aefa2b4`; exact overlaps: none.

Changed expressions: `{"old": "if not isinstance(value, str):", "new": "if False:"}`.

### `valid-unicode-rejected-ascii`

**KEEP** — Injects the specific behavioral change 'value.encode("utf-8")' → 'value.encode("ascii")'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:17`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `4ded038bb4d428ef4ff84ed15250ff91ca05495ee706461b8d00641d468e7866`; exact overlaps: none.

Changed expressions: `{"old": "value.encode(\"utf-8\")", "new": "value.encode(\"ascii\")"}`.

### `nul-only-at-start`

**KEEP** — Injects the specific behavioral change 'if "\\x00" in value:' → 'if value.startswith("\\x00"):'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:20`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `29e8cb1c68b6e706f866aaad0cffba51d50e362b06a96f79e43fcf57d79f3686`; exact overlaps: none.

Changed expressions: `{"old": "if \"\\x00\" in value:", "new": "if value.startswith(\"\\x00\"):"}`.

### `valid-body-erased`

**KEEP** — Injects the specific behavioral change 'return ValidatedNote(title, body,' → 'return ValidatedNote(title, "",'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:60`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `83cd4195989cbc2ae21e7a1e05bb004fb47f7cb610edf3c1d26b6e44a691570f`; exact overlaps: none.

Changed expressions: `{"old": "return ValidatedNote(title, body,", "new": "return ValidatedNote(title, \"\","}`.

### `valid-title-erased`

**KEEP** — Injects the specific behavioral change 'return ValidatedNote(title, body,' → 'return ValidatedNote(None, body,'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:60`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `96497c74d48064f9186c76afe14f7be3249c1ce52a29c235bbed74308bd1ab6d`; exact overlaps: none.

Changed expressions: `{"old": "return ValidatedNote(title, body,", "new": "return ValidatedNote(None, body,"}`.

### `blank-save-never-deletes`

**KEEP** — Injects the specific behavioral change 'not is_draft and title is None and not body.strip()' → 'False'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:60`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `2a5e9d2a3810d7877ecd8050a4e0064fe8056a2d1f1e05ab42fee202546c4e1b`; exact overlaps: none.

Changed expressions: `{"old": "not is_draft and title is None and not body.strip()", "new": "False"}`.

### `target-host-public`

**KEEP** — Injects the specific behavioral change 'host="127.0.0.1"' → 'host="0.0.0.0"'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:11`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `36aff9f386ee5e70763c740f335a24fdcb3e4785fac4a7b245ecfe5c4ebe41c8`; exact overlaps: none.

Changed expressions: `{"old": "host=\"127.0.0.1\"", "new": "host=\"0.0.0.0\""}`.

### `target-database-original`

**KEEP** — Injects the specific behavioral change 'dbname="merlin_d6"' → 'dbname="merlin_db"'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:11`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `c32806ccfd003903007fc9d86f5bb8e66c187f7dfe82c682df547e065133167f`; exact overlaps: none.

Changed expressions: `{"old": "dbname=\"merlin_d6\"", "new": "dbname=\"merlin_db\""}`.

### `target-user-original`

**KEEP** — Injects the specific behavioral change 'user="merlin_d6"' → 'user="merlin"'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:11`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `88e1567552c803533b3e3ab87cbbbf0ceb0b0682ea1e29460f8d149cabfc9047`; exact overlaps: none.

Changed expressions: `{"old": "user=\"merlin_d6\"", "new": "user=\"merlin\""}`.

### `connection-timeout-unbounded`

**KEEP** — Injects the specific behavioral change 'connect_timeout=3' → 'connect_timeout=0'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:11`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `ffb13d390086990bd597287e32e5c74569a6847b2693f49b2f13b77a01c76bc6`; exact overlaps: none.

Changed expressions: `{"old": "connect_timeout=3", "new": "connect_timeout=0"}`.

### `batch-zero-allowed`

**KEEP** — Injects the specific behavioral change '1 <= batch_size <= 1000' → '0 <= batch_size <= 1000'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:33`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `48b833f5af1f9d21e47e367ee65341dfc5ea5b5ca5dbd74a8bd3e814016b6adb`; exact overlaps: none.

Changed expressions: `{"old": "1 <= batch_size <= 1000", "new": "0 <= batch_size <= 1000"}`.

### `batch1000-rejected`

**KEEP** — Injects the specific behavioral change '1 <= batch_size <= 1000' → '1 <= batch_size <= 999'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:33`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `fbdee8d618dae6ee5247247249294a5546aebd750766dcf7d11a505471c0caf9`; exact overlaps: none.

Changed expressions: `{"old": "1 <= batch_size <= 1000", "new": "1 <= batch_size <= 999"}`.

### `statement-timeout-removed`

**KEEP** — Injects the specific behavioral change '            cur.execute("SET LOCAL statement_timeout = \'10s\'")\n' → ''. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:41`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `b83c73d9d0b26b9758b2ff4c20b4b0e4799f2abb5e2249623bf4c236db70a87e`; exact overlaps: none.

Changed expressions: `{"old": "            cur.execute(\"SET LOCAL statement_timeout = '10s'\")\n", "new": ""}`.

### `purge-parameter-altered`

**KEEP** — Injects the specific behavioral change 'cur.execute("SELECT public.purge_deleted_notes(%s)", (batch_size,))' → 'cur.execute("SELECT public.purge_deleted_notes(%s)", (batch_size - 1,))'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:46`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `3a57c303120a5294affc61f4823ee874cddf10d2f03092969993152878b2694a`; exact overlaps: none.

Changed expressions: `{"old": "cur.execute(\"SELECT public.purge_deleted_notes(%s)\", (batch_size,))", "new": "cur.execute(\"SELECT public.purge_deleted_notes(%s)\", (batch_size - 1,))"}`.

### `cleanup-counts-swapped`

**KEEP** — Injects the specific behavioral change 'return expired, purged' → 'return purged, expired'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:48`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `a9d196effe878d904455f9b29707e831f93f4b449b4ad1246785474c955e5cff`; exact overlaps: none.

Changed expressions: `{"old": "return expired, purged", "new": "return purged, expired"}`.

### `early-explicit-commit`

**KEEP** — Injects the specific behavioral change '            expired = cur.fetchone()[0]' → '            expired = cur.fetchone()[0]\n            conn.commit()'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:45`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `d683407554fb737fde1fcee5abf25f4508627c8bcbef3f823c706c1feff5b7a5`; exact overlaps: none.

Changed expressions: `{"old": "            expired = cur.fetchone()[0]", "new": "            expired = cur.fetchone()[0]\n            conn.commit()"}`.

### `default-interval-altered`

**KEEP** — Injects the specific behavioral change 'default=60' → 'default=59'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:54`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `9c11c3bede4f767c8ce3c6193569202d8f8441d4adadc3be73c98f6eb5a44f12`; exact overlaps: none.

Changed expressions: `{"old": "default=60", "new": "default=59"}`.

### `nine-second-interval-allowed`

**KEEP** — Injects the specific behavioral change 'args.interval < 10' → 'args.interval < 9'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:56`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `b9b7e8c55718b974b2dc97a849ec19ec24265f6e48c5c834d42cd9ba27ed38e7`; exact overlaps: none.

Changed expressions: `{"old": "args.interval < 10", "new": "args.interval < 9"}`.

### `ten-second-interval-rejected`

**KEEP** — Injects the specific behavioral change 'args.interval < 10' → 'args.interval < 11'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:56`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `954ce1e447b8b88d69996bdd573b3d83a461915a89e7359492075d2aa280611c`; exact overlaps: none.

Changed expressions: `{"old": "args.interval < 10", "new": "args.interval < 11"}`.

### `runtime-error-not-sanitized`

**KEEP** — Injects the specific behavioral change 'except (psycopg.Error, RuntimeError):' → 'except psycopg.Error:'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:72`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `c6f82df2ca7c0734d0f52df04c9a9d72e9dfd31cb116fda9c34dbd3ad0ecd192`; exact overlaps: none.

Changed expressions: `{"old": "except (psycopg.Error, RuntimeError):", "new": "except psycopg.Error:"}`.

### `output-counts-swapped`

**KEEP** — Injects the specific behavioral change 'Expired title-only notes: {expired}; purged deleted notes: {purged}' → 'Expired title-only notes: {purged}; purged deleted notes: {expired}'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:64`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `2892719611edf4432a6cb70b6a664ea9ab98bba14965bc39079c23ddbfbba871`; exact overlaps: none.

Changed expressions: `{"old": "Expired title-only notes: {expired}; purged deleted notes: {purged}", "new": "Expired title-only notes: {purged}; purged deleted notes: {expired}"}`.

### `interrupt-message-omitted`

**KEEP** — Injects the specific behavioral change 'print("Maintenance stopped")' → 'pass'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:70`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `b7654f955e5b70d50282e56284eaddd84a55f5a0446ae5abf76071abd05232cb`; exact overlaps: none.

Changed expressions: `{"old": "print(\"Maintenance stopped\")", "new": "pass"}`.

### `nul-error-echoes-input`

**KEEP** — Injects the specific behavioral change 'raise ValueError("PostgreSQL text cannot contain NUL")' → 'raise ValueError("PostgreSQL text cannot contain NUL: " + value)'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:21`; evidence status: DETECTED; origin: legacy + exhaustive.

AST proof: `8ce4b3bbd3f9f62238e4b974d3c5a01654a728b1f31381c7f1a9891e1e92dff3`; exact overlaps: none.

Changed expressions: `{"old": "raise ValueError(\"PostgreSQL text cannot contain NUL\")", "new": "raise ValueError(\"PostgreSQL text cannot contain NUL: \" + value)"}`.

### `probe-only-operational-errors`

**KEEP** — Injects the specific behavioral change 'except psycopg.Error:' → 'except psycopg.OperationalError:'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/database_connectivity_probe.py:17`; evidence status: DETECTED; origin: exhaustive.

AST proof: `02a416f97e5a590edd8ce0792a3096fc8365ea6297f5ef20efffd41a1dabb4e5`; exact overlaps: none.

Changed expressions: `{"old": "except psycopg.Error:", "new": "except psycopg.OperationalError:"}`.

### `probe-leaks-error`

**KEEP** — Injects the specific behavioral change 'print("DB Probe Failed: Connection or query failed.", file=sys.stderr)' → 'print("DB Probe Failed: " + password, file=sys.stderr)'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/database_connectivity_probe.py:18`; evidence status: DETECTED; origin: exhaustive.

AST proof: `b4adc8245b8aeb3d0746c985ed971af43aa91f8a9c87f02fbe5b27b55afc0d81`; exact overlaps: none.

Changed expressions: `{"old": "print(\"DB Probe Failed: Connection or query failed.\", file=sys.stderr)", "new": "print(\"DB Probe Failed: \" + password, file=sys.stderr)"}`.

### `probe-wrong-failure-status`

**KEEP** — Injects the specific behavioral change 'sys.exit(1)' → 'sys.exit(0)'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/database_connectivity_probe.py:19`; evidence status: DETECTED; origin: exhaustive.

AST proof: `b9a62e93e51bca293292eeaf6dba6444f13a33dec1dd22d69e5bc554f307886b`; exact overlaps: none.

Changed expressions: `{"old": "sys.exit(1)", "new": "sys.exit(0)"}`.

### `probe-wrong-success-status`

**KEEP** — Injects the specific behavioral change 'sys.exit(0)' → 'sys.exit(1)'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/database_connectivity_probe.py:15`; evidence status: DETECTED; origin: exhaustive.

AST proof: `5f39aa5edf269c27460c320b9a72db2a9464c1835309cb9ce009d818e0f10355`; exact overlaps: none.

Changed expressions: `{"old": "sys.exit(0)", "new": "sys.exit(1)"}`.

### `probe-not-read-only`

**KEEP** — Injects the specific behavioral change 'conn.read_only = True' → 'conn.read_only = False'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/database_connectivity_probe.py:9`; evidence status: DETECTED; origin: exhaustive.

AST proof: `c10c4bba3f5baf318f07264fc028afca6185039c5d82d9be84368418068c8586`; exact overlaps: none.

Changed expressions: `{"old": "conn.read_only = True", "new": "conn.read_only = False"}`.

### `probe-wrong-port`

**KEEP** — Injects the specific behavioral change 'port=55432' → 'port=5432'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/database_connectivity_probe.py:8`; evidence status: DETECTED; origin: exhaustive.

AST proof: `bc05dbe97b448c29b4a97bab1f0061dcd2daf4bdbcbc7a2516d4086ab3abbd84`; exact overlaps: none.

Changed expressions: `{"old": "port=55432", "new": "port=5432"}`.

### `probe-fetch-twice`

**KEEP** — Injects the specific behavioral change 'db_name, db_user = cur.fetchone()' → 'db_name, db_user = cur.fetchone(); cur.fetchone()'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/database_connectivity_probe.py:12`; evidence status: DETECTED; origin: exhaustive.

AST proof: `f192d83d1327b406ffd123ea1e24ef5f879b18c7fc6e2327f89abbb929381099`; exact overlaps: none.

Changed expressions: `{"old": "db_name, db_user = cur.fetchone()", "new": "db_name, db_user = cur.fetchone(); cur.fetchone()"}`.

### `probe-mask-programming-bug`

**KEEP** — Injects the specific behavioral change 'except psycopg.Error:' → 'except Exception:'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/database_connectivity_probe.py:17`; evidence status: DETECTED; origin: exhaustive.

AST proof: `14acb531d05538411eaae614629594f03a5e932b3c7b97373b4e1869a8088b17`; exact overlaps: none.

Changed expressions: `{"old": "except psycopg.Error:", "new": "except Exception:"}`.

### `probe-extra-query`

**KEEP** — Injects the specific behavioral change 'cur.execute("SELECT current_database(), current_user;")' → 'cur.execute("SELECT 42"); cur.execute("SELECT current_database(), current_user;")'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/database_connectivity_probe.py:11`; evidence status: DETECTED; origin: exhaustive.

AST proof: `686788cb80aa99c1480af91d1bf1b253c66b499252702e17b0cd530a0888ba16`; exact overlaps: none.

Changed expressions: `{"old": "cur.execute(\"SELECT current_database(), current_user;\")", "new": "cur.execute(\"SELECT 42\"); cur.execute(\"SELECT current_database(), current_user;\")"}`.

### `probe-error-on-stdout`

**KEEP** — Injects the specific behavioral change 'file=sys.stderr' → 'file=sys.stdout'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/database_connectivity_probe.py:18`; evidence status: DETECTED; origin: exhaustive.

AST proof: `0acc3223e3fb3d6da27052418d0d4ed3cab29e2384117ac4dca856c89a75efc0`; exact overlaps: none.

Changed expressions: `{"old": "file=sys.stderr", "new": "file=sys.stdout"}`.

### `worker-malformed-identity-not-sanitized`

**KEEP** — Injects the specific behavioral change 'raise RuntimeError("Refusing malformed Day 6 database identity") from None' → 'raise'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:24`; evidence status: DETECTED; origin: exhaustive.

AST proof: `fe95298d42a614e2479c31ddb2671463096909f7d0663f1a2e16422cd138872f`; exact overlaps: none.

Changed expressions: `{"old": "raise RuntimeError(\"Refusing malformed Day 6 database identity\") from None", "new": "raise"}`.

### `text-plain-weight-zero`

**KEEP** — Injects the specific behavioral change 'else 1 for part' → 'else 0 for part'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:23`; evidence status: DETECTED; origin: exhaustive.

AST proof: `8868095034348a00fa809aae89e5422e4fb71cfb010957816109d087cee75d59`; exact overlaps: none.

Changed expressions: `{"old": "else 1 for part", "new": "else 0 for part"}`.

### `text-all-empty-rejected`

**KEEP** — Injects the specific behavioral change 'return sum(' → 'if value == "": raise ValueError("Empty text rejected")\n    return sum('. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:23`; evidence status: DETECTED; origin: exhaustive.

AST proof: `830c09b241383c2fc5c91ab6d9c8406b559df3292894d96240fcb14e155b1cdd`; exact overlaps: none.

Changed expressions: `{"old": "return sum(", "new": "if value == \"\": raise ValueError(\"Empty text rejected\")\n    return sum("}`.

### `text-drafts-all-delete`

**KEEP** — Injects the specific behavioral change 'not is_draft and title is None and not body.strip()' → 'is_draft or (title is None and not body.strip())'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:60`; evidence status: DETECTED; origin: exhaustive.

AST proof: `cea70758e38425186001429c2a7c9040bbd44b951a4074199f66607d28232810`; exact overlaps: none.

Changed expressions: `{"old": "not is_draft and title is None and not body.strip()", "new": "is_draft or (title is None and not body.strip())"}`.

### `text-all-emails-null`

**KEEP** — Injects the specific behavioral change 'return value.strip() or None' → 'return None'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:32`; evidence status: DETECTED; origin: exhaustive.

AST proof: `b96e336c7ed80fa4e8cd8b5f7ddf905e8889209291cc0d62c5925a19fdf4480c`; exact overlaps: none.

Changed expressions: `{"old": "return value.strip() or None", "new": "return None"}`.

### `text-whitespace-body-trimmed`

**MERGE** — Exact AST/source duplicate of body-stripped; both replace normalization with body.strip().

Source: `app/note_rules.py:56`; evidence status: DETECTED; origin: exhaustive.

AST proof: `8c5ac4e638d22b51647622db4b568269ca0e215f243c4bdf77389f59adceeaf1`; exact overlaps: `body-stripped`.

Changed expressions: `{"old": "body = \"\" if body is None else body", "new": "body = \"\" if body is None else body.strip()"}`.

### `worker-invalid-interval-falls-back`

**KEEP** — Injects the specific behavioral change 'type=int, default=60' → 'type=lambda value: int(value) if value.isdecimal() else 60, default=60'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:54`; evidence status: DETECTED; origin: exhaustive.

AST proof: `d9a662f3358036e884f8da4768cf654d3292073ededa51b0990bb9e56e8bf151`; exact overlaps: none.

Changed expressions: `{"old": "type=int, default=60", "new": "type=lambda value: int(value) if value.isdecimal() else 60, default=60"}`.

### `worker-help-disabled`

**KEEP** — Injects the specific behavioral change 'argparse.ArgumentParser(description=__doc__)' → 'argparse.ArgumentParser(description=__doc__, add_help=False)'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:52`; evidence status: DETECTED; origin: exhaustive.

AST proof: `e3a71fa2bb4e2b964db0c2fea76f8cce0ee575f0eb55425d1b358eedc2fa5598`; exact overlaps: none.

Changed expressions: `{"old": "argparse.ArgumentParser(description=__doc__)", "new": "argparse.ArgumentParser(description=__doc__, add_help=False)"}`.

### `worker-unknown-flags-ignored`

**KEEP** — Injects the specific behavioral change 'args = parser.parse_args()' → 'args, unknown = parser.parse_known_args()'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:55`; evidence status: DETECTED; origin: exhaustive.

AST proof: `da3384c950867e2592cc3d1412d7d3b372611e44dc208451bdd3e26df6433355`; exact overlaps: none.

Changed expressions: `{"old": "args = parser.parse_args()", "new": "args, unknown = parser.parse_known_args()"}`.

### `ast-database_connectivity_probe-21-11`

**IMPROVE** — Import-guard reversal invokes CLI during exec into an already imported module, before mocks/test collection. INVALID is harness startup failure, not detection; use isolated real CLI invocation with stdin closed and connector patched before startup.

Source: `app/database_connectivity_probe.py:1`; evidence status: INVALID; origin: exhaustive.

AST proof: `34bae3756dcb221f86109a9ae9d7060a093ff605f3cea03f6f8a07928063b284`; exact overlaps: none.

Changed expressions: `[{"original": "__name__ == '__main__'", "mutated": "__name__ != '__main__'", "line": 21}]`.

### `ast-notes_maintenance-76-42`

**IMPROVE** — Import-guard reversal invokes CLI during exec into an already imported module, before mocks/test collection. INVALID is harness startup failure, not detection; use isolated real CLI invocation with stdin closed and connector patched before startup.

Source: `app/notes_maintenance.py:1`; evidence status: INVALID; origin: exhaustive.

AST proof: `12933b06b887502e31f350c18115b3b4dbdabf70fd1135214bc8150e5bbce0f7`; exact overlaps: none.

Changed expressions: `[{"original": "__name__ == '__main__'", "mutated": "__name__ != '__main__'", "line": 76}]`.

### `ast-notes_maintenance-25-60`

**MERGE** — Exact complete-module AST matches identity-or-changed-to-and after mutation (locations excluded); duplicate faulty program, not merely identical detectors.

Source: `app/notes_maintenance.py:1`; evidence status: DETECTED; origin: exhaustive.

AST proof: `6ebe89bbc5710fc44da2c94b0a827172d6f0dbb9f56beb521b75905532bfe15f`; exact overlaps: `identity-or-changed-to-and`.

Changed expressions: `[{"original": "database != 'merlin_d6' or int(identifier) != EXPECTED_CLUSTER", "mutated": "database != 'merlin_d6' and int(identifier) != EXPECTED_CLUSTER", "line": 25}]`.

### `ast-notes_maintenance-31-65`

**KEEP** — Injects the specific behavioral change '"""Foreground scheduler restricted to the known disposable Day 6 cluster."""\n\nimport argparse\nimport getpass\nimport time\n\nimport psycopg\n\n# These fixed settings protect Sprint 0; this worker is for disposable storage only.\nEXPECTED_CLUSTER = 7694311451826794534\nTARGET = dict(host="127.0.0.1", port=55432, dbname="merlin_d6", user="merlin_d6", connect_timeout=3)\n\n\ndef verify_target(conn) -> None:\n    """Fail closed before writes; never accept another database or cluster."""\n    # Read the cluster fingerprint before allowing any cleanup writes.\n    with conn.cursor() as cur:\n        cur.execute("SELECT current_database(), system_identifier FROM pg_control_system()")\n        identity = cur.fetchone()\n    try:\n        database, identifier = identity\n        identifier = int(identifier)\n    except (ValueError, TypeError):\n        raise RuntimeError("Refusing malformed Day 6 database identity") from None\n    if database != "merlin_d6" or int(identifier) != EXPECTED_CLUSTER:\n        raise RuntimeError("Refusing maintenance outside the verified Day 6 cluster")\n\n\ndef run_once(password: str, batch_size: int = 100) -> tuple[int, int]:\n    # Exact type check: rejects floats, strings, and booleans (type(True) is bool)\n    if type(batch_size) is not int:\n        raise ValueError("Batch size must be an integer")\n    if not 1 <= batch_size <= 1000:\n        raise ValueError("Batch size must be between 1 and 1000")\n    # This context commits on success and rolls back both cleanups if either fails.\n    with psycopg.connect(**TARGET, password=password) as conn:\n        verify_target(conn)\n        with conn.cursor() as cur:\n            # Stop a cycle rather than waiting indefinitely for locks or slow queries.\n            cur.execute("SET LOCAL lock_timeout = \'2s\'")\n            cur.execute("SET LOCAL statement_timeout = \'10s\'")\n            # %s binds a value safely; never build SQL by joining user input.\n            # First remove expired title-only notes, then purge old soft deletions.\n            cur.execute("SELECT public.cleanup_expired_blank_notes(%s)", (batch_size,))\n            expired = cur.fetchone()[0]\n            cur.execute("SELECT public.purge_deleted_notes(%s)", (batch_size,))\n            purged = cur.fetchone()[0]\n    return expired, purged\n\n\ndef main() -> None:\n    parser = argparse.ArgumentParser(description=__doc__)\n    parser.add_argument("--once", action="store_true", help="Run one maintenance cycle")\n    parser.add_argument("--interval", type=int, default=60, help="Seconds between cycles")\n    args = parser.parse_args()\n    if args.interval < 10:\n        parser.error("Interval must be at least 10 seconds")\n    # Prompt without echoing the password; do not store it in the source file.\n    password = getpass.getpass("Disposable merlin_d6 password: ")\n    try:\n        # The scheduler runs only while this foreground process remains open.\n        while True:\n            expired, purged = run_once(password)\n            print(f"Expired title-only notes: {expired}; purged deleted notes: {purged}")\n            # --once performs one cycle; otherwise pause before the next cycle.\n            if args.once:\n                break\n            time.sleep(args.interval)\n    except KeyboardInterrupt:\n        print("Maintenance stopped")\n    # Avoid printing connection details or credentials in database errors.\n    except (psycopg.Error, RuntimeError):\n        raise SystemExit("Maintenance failed; check target, migration and permissions. No credentials printed.")\n\n\nif __name__ == "__main__":\n    main()\n' → '"""Foreground scheduler restricted to the known disposable Day 6 cluster."""\n\nimport argparse\nimport getpass\nimport time\n\nimport psycopg\n\n# These fixed settings protect Sprint 0; this worker is for disposable storage only.\nEXPECTED_CLUSTER = 7694311451826794534\nTARGET = dict(host="127.0.0.1", port=55432, dbname="merlin_d6", user="merlin_d6", connect_timeout=3)\n\n\ndef verify_target(conn) -> None:\n    """Fail closed before writes; never accept another database or cluster."""\n    # Read the cluster fingerprint before allowing any cleanup writes.\n    with conn.cursor() as cur:\n        cur.execute("SELECT current_database(), system_identifier FROM pg_control_system()")\n        identity = cur.fetchone()\n    try:\n        database, identifier = identity\n        identifier = int(identifier)\n    except (ValueError, TypeError):\n        raise RuntimeError("Refusing malformed Day 6 database identity") from None\n    if database != "merlin_d6" or int(identifier) != EXPECTED_CLUSTER:\n        raise RuntimeError("Refusing maintenance outside the verified Day 6 cluster")\n\n\ndef run_once(password: str, batch_size: int = 100) -> tuple[int, int]:\n    # Exact type check: rejects floats, strings, and booleans (type(True) is bool)\n    if (type(batch_size) is int):\n        raise ValueError("Batch size must be an integer")\n    if not 1 <= batch_size <= 1000:\n        raise ValueError("Batch size must be between 1 and 1000")\n    # This context commits on success and rolls back both cleanups if either fails.\n    with psycopg.connect(**TARGET, password=password) as conn:\n        verify_target(conn)\n        with conn.cursor() as cur:\n            # Stop a cycle rather than waiting indefinitely for locks or slow queries.\n            cur.execute("SET LOCAL lock_timeout = \'2s\'")\n            cur.execute("SET LOCAL statement_timeout = \'10s\'")\n            # %s binds a value safely; never build SQL by joining user input.\n            # First remove expired title-only notes, then purge old soft deletions.\n            cur.execute("SELECT public.cleanup_expired_blank_notes(%s)", (batch_size,))\n            expired = cur.fetchone()[0]\n            cur.execute("SELECT public.purge_deleted_notes(%s)", (batch_size,))\n            purged = cur.fetchone()[0]\n    return expired, purged\n\n\ndef main() -> None:\n    parser = argparse.ArgumentParser(description=__doc__)\n    parser.add_argument("--once", action="store_true", help="Run one maintenance cycle")\n    parser.add_argument("--interval", type=int, default=60, help="Seconds between cycles")\n    args = parser.parse_args()\n    if args.interval < 10:\n        parser.error("Interval must be at least 10 seconds")\n    # Prompt without echoing the password; do not store it in the source file.\n    password = getpass.getpass("Disposable merlin_d6 password: ")\n    try:\n        # The scheduler runs only while this foreground process remains open.\n        while True:\n            expired, purged = run_once(password)\n            print(f"Expired title-only notes: {expired}; purged deleted notes: {purged}")\n            # --once performs one cycle; otherwise pause before the next cycle.\n            if args.once:\n                break\n            time.sleep(args.interval)\n    except KeyboardInterrupt:\n        print("Maintenance stopped")\n    # Avoid printing connection details or credentials in database errors.\n    except (psycopg.Error, RuntimeError):\n        raise SystemExit("Maintenance failed; check target, migration and permissions. No credentials printed.")\n\n\nif __name__ == "__main__":\n    main()\n'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:1`; evidence status: DETECTED; origin: exhaustive.

AST proof: `b1606d8c8dcc0def349bda9e8bd9ae5aa987234e1791d60e2fa7db8c45f9686f`; exact overlaps: none.

Changed expressions: `[{"original": "type(batch_size) is not int", "mutated": "type(batch_size) is int", "line": 31}]`.

### `ast-notes_maintenance-56-82`

**KEEP** — Injects the specific behavioral change '"""Foreground scheduler restricted to the known disposable Day 6 cluster."""\n\nimport argparse\nimport getpass\nimport time\n\nimport psycopg\n\n# These fixed settings protect Sprint 0; this worker is for disposable storage only.\nEXPECTED_CLUSTER = 7694311451826794534\nTARGET = dict(host="127.0.0.1", port=55432, dbname="merlin_d6", user="merlin_d6", connect_timeout=3)\n\n\ndef verify_target(conn) -> None:\n    """Fail closed before writes; never accept another database or cluster."""\n    # Read the cluster fingerprint before allowing any cleanup writes.\n    with conn.cursor() as cur:\n        cur.execute("SELECT current_database(), system_identifier FROM pg_control_system()")\n        identity = cur.fetchone()\n    try:\n        database, identifier = identity\n        identifier = int(identifier)\n    except (ValueError, TypeError):\n        raise RuntimeError("Refusing malformed Day 6 database identity") from None\n    if database != "merlin_d6" or int(identifier) != EXPECTED_CLUSTER:\n        raise RuntimeError("Refusing maintenance outside the verified Day 6 cluster")\n\n\ndef run_once(password: str, batch_size: int = 100) -> tuple[int, int]:\n    # Exact type check: rejects floats, strings, and booleans (type(True) is bool)\n    if type(batch_size) is not int:\n        raise ValueError("Batch size must be an integer")\n    if not 1 <= batch_size <= 1000:\n        raise ValueError("Batch size must be between 1 and 1000")\n    # This context commits on success and rolls back both cleanups if either fails.\n    with psycopg.connect(**TARGET, password=password) as conn:\n        verify_target(conn)\n        with conn.cursor() as cur:\n            # Stop a cycle rather than waiting indefinitely for locks or slow queries.\n            cur.execute("SET LOCAL lock_timeout = \'2s\'")\n            cur.execute("SET LOCAL statement_timeout = \'10s\'")\n            # %s binds a value safely; never build SQL by joining user input.\n            # First remove expired title-only notes, then purge old soft deletions.\n            cur.execute("SELECT public.cleanup_expired_blank_notes(%s)", (batch_size,))\n            expired = cur.fetchone()[0]\n            cur.execute("SELECT public.purge_deleted_notes(%s)", (batch_size,))\n            purged = cur.fetchone()[0]\n    return expired, purged\n\n\ndef main() -> None:\n    parser = argparse.ArgumentParser(description=__doc__)\n    parser.add_argument("--once", action="store_true", help="Run one maintenance cycle")\n    parser.add_argument("--interval", type=int, default=60, help="Seconds between cycles")\n    args = parser.parse_args()\n    if args.interval < 10:\n        parser.error("Interval must be at least 10 seconds")\n    # Prompt without echoing the password; do not store it in the source file.\n    password = getpass.getpass("Disposable merlin_d6 password: ")\n    try:\n        # The scheduler runs only while this foreground process remains open.\n        while True:\n            expired, purged = run_once(password)\n            print(f"Expired title-only notes: {expired}; purged deleted notes: {purged}")\n            # --once performs one cycle; otherwise pause before the next cycle.\n            if args.once:\n                break\n            time.sleep(args.interval)\n    except KeyboardInterrupt:\n        print("Maintenance stopped")\n    # Avoid printing connection details or credentials in database errors.\n    except (psycopg.Error, RuntimeError):\n        raise SystemExit("Maintenance failed; check target, migration and permissions. No credentials printed.")\n\n\nif __name__ == "__main__":\n    main()\n' → '"""Foreground scheduler restricted to the known disposable Day 6 cluster."""\n\nimport argparse\nimport getpass\nimport time\n\nimport psycopg\n\n# These fixed settings protect Sprint 0; this worker is for disposable storage only.\nEXPECTED_CLUSTER = 7694311451826794534\nTARGET = dict(host="127.0.0.1", port=55432, dbname="merlin_d6", user="merlin_d6", connect_timeout=3)\n\n\ndef verify_target(conn) -> None:\n    """Fail closed before writes; never accept another database or cluster."""\n    # Read the cluster fingerprint before allowing any cleanup writes.\n    with conn.cursor() as cur:\n        cur.execute("SELECT current_database(), system_identifier FROM pg_control_system()")\n        identity = cur.fetchone()\n    try:\n        database, identifier = identity\n        identifier = int(identifier)\n    except (ValueError, TypeError):\n        raise RuntimeError("Refusing malformed Day 6 database identity") from None\n    if database != "merlin_d6" or int(identifier) != EXPECTED_CLUSTER:\n        raise RuntimeError("Refusing maintenance outside the verified Day 6 cluster")\n\n\ndef run_once(password: str, batch_size: int = 100) -> tuple[int, int]:\n    # Exact type check: rejects floats, strings, and booleans (type(True) is bool)\n    if type(batch_size) is not int:\n        raise ValueError("Batch size must be an integer")\n    if not 1 <= batch_size <= 1000:\n        raise ValueError("Batch size must be between 1 and 1000")\n    # This context commits on success and rolls back both cleanups if either fails.\n    with psycopg.connect(**TARGET, password=password) as conn:\n        verify_target(conn)\n        with conn.cursor() as cur:\n            # Stop a cycle rather than waiting indefinitely for locks or slow queries.\n            cur.execute("SET LOCAL lock_timeout = \'2s\'")\n            cur.execute("SET LOCAL statement_timeout = \'10s\'")\n            # %s binds a value safely; never build SQL by joining user input.\n            # First remove expired title-only notes, then purge old soft deletions.\n            cur.execute("SELECT public.cleanup_expired_blank_notes(%s)", (batch_size,))\n            expired = cur.fetchone()[0]\n            cur.execute("SELECT public.purge_deleted_notes(%s)", (batch_size,))\n            purged = cur.fetchone()[0]\n    return expired, purged\n\n\ndef main() -> None:\n    parser = argparse.ArgumentParser(description=__doc__)\n    parser.add_argument("--once", action="store_true", help="Run one maintenance cycle")\n    parser.add_argument("--interval", type=int, default=60, help="Seconds between cycles")\n    args = parser.parse_args()\n    if (args.interval >= 10):\n        parser.error("Interval must be at least 10 seconds")\n    # Prompt without echoing the password; do not store it in the source file.\n    password = getpass.getpass("Disposable merlin_d6 password: ")\n    try:\n        # The scheduler runs only while this foreground process remains open.\n        while True:\n            expired, purged = run_once(password)\n            print(f"Expired title-only notes: {expired}; purged deleted notes: {purged}")\n            # --once performs one cycle; otherwise pause before the next cycle.\n            if args.once:\n                break\n            time.sleep(args.interval)\n    except KeyboardInterrupt:\n        print("Maintenance stopped")\n    # Avoid printing connection details or credentials in database errors.\n    except (psycopg.Error, RuntimeError):\n        raise SystemExit("Maintenance failed; check target, migration and permissions. No credentials printed.")\n\n\nif __name__ == "__main__":\n    main()\n'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:1`; evidence status: DETECTED; origin: exhaustive.

AST proof: `9e5cd6e8dfc32a1a62ce9e53738f979b8863f7e1d24ac0c5520c8e7fb7b12fa4`; exact overlaps: none.

Changed expressions: `[{"original": "args.interval < 10", "mutated": "args.interval >= 10", "line": 56}]`.

### `ast-notes_maintenance-25-111`

**KEEP** — Injects the specific behavioral change '"""Foreground scheduler restricted to the known disposable Day 6 cluster."""\n\nimport argparse\nimport getpass\nimport time\n\nimport psycopg\n\n# These fixed settings protect Sprint 0; this worker is for disposable storage only.\nEXPECTED_CLUSTER = 7694311451826794534\nTARGET = dict(host="127.0.0.1", port=55432, dbname="merlin_d6", user="merlin_d6", connect_timeout=3)\n\n\ndef verify_target(conn) -> None:\n    """Fail closed before writes; never accept another database or cluster."""\n    # Read the cluster fingerprint before allowing any cleanup writes.\n    with conn.cursor() as cur:\n        cur.execute("SELECT current_database(), system_identifier FROM pg_control_system()")\n        identity = cur.fetchone()\n    try:\n        database, identifier = identity\n        identifier = int(identifier)\n    except (ValueError, TypeError):\n        raise RuntimeError("Refusing malformed Day 6 database identity") from None\n    if database != "merlin_d6" or int(identifier) != EXPECTED_CLUSTER:\n        raise RuntimeError("Refusing maintenance outside the verified Day 6 cluster")\n\n\ndef run_once(password: str, batch_size: int = 100) -> tuple[int, int]:\n    # Exact type check: rejects floats, strings, and booleans (type(True) is bool)\n    if type(batch_size) is not int:\n        raise ValueError("Batch size must be an integer")\n    if not 1 <= batch_size <= 1000:\n        raise ValueError("Batch size must be between 1 and 1000")\n    # This context commits on success and rolls back both cleanups if either fails.\n    with psycopg.connect(**TARGET, password=password) as conn:\n        verify_target(conn)\n        with conn.cursor() as cur:\n            # Stop a cycle rather than waiting indefinitely for locks or slow queries.\n            cur.execute("SET LOCAL lock_timeout = \'2s\'")\n            cur.execute("SET LOCAL statement_timeout = \'10s\'")\n            # %s binds a value safely; never build SQL by joining user input.\n            # First remove expired title-only notes, then purge old soft deletions.\n            cur.execute("SELECT public.cleanup_expired_blank_notes(%s)", (batch_size,))\n            expired = cur.fetchone()[0]\n            cur.execute("SELECT public.purge_deleted_notes(%s)", (batch_size,))\n            purged = cur.fetchone()[0]\n    return expired, purged\n\n\ndef main() -> None:\n    parser = argparse.ArgumentParser(description=__doc__)\n    parser.add_argument("--once", action="store_true", help="Run one maintenance cycle")\n    parser.add_argument("--interval", type=int, default=60, help="Seconds between cycles")\n    args = parser.parse_args()\n    if args.interval < 10:\n        parser.error("Interval must be at least 10 seconds")\n    # Prompt without echoing the password; do not store it in the source file.\n    password = getpass.getpass("Disposable merlin_d6 password: ")\n    try:\n        # The scheduler runs only while this foreground process remains open.\n        while True:\n            expired, purged = run_once(password)\n            print(f"Expired title-only notes: {expired}; purged deleted notes: {purged}")\n            # --once performs one cycle; otherwise pause before the next cycle.\n            if args.once:\n                break\n            time.sleep(args.interval)\n    except KeyboardInterrupt:\n        print("Maintenance stopped")\n    # Avoid printing connection details or credentials in database errors.\n    except (psycopg.Error, RuntimeError):\n        raise SystemExit("Maintenance failed; check target, migration and permissions. No credentials printed.")\n\n\nif __name__ == "__main__":\n    main()\n' → '"""Foreground scheduler restricted to the known disposable Day 6 cluster."""\n\nimport argparse\nimport getpass\nimport time\n\nimport psycopg\n\n# These fixed settings protect Sprint 0; this worker is for disposable storage only.\nEXPECTED_CLUSTER = 7694311451826794534\nTARGET = dict(host="127.0.0.1", port=55432, dbname="merlin_d6", user="merlin_d6", connect_timeout=3)\n\n\ndef verify_target(conn) -> None:\n    """Fail closed before writes; never accept another database or cluster."""\n    # Read the cluster fingerprint before allowing any cleanup writes.\n    with conn.cursor() as cur:\n        cur.execute("SELECT current_database(), system_identifier FROM pg_control_system()")\n        identity = cur.fetchone()\n    try:\n        database, identifier = identity\n        identifier = int(identifier)\n    except (ValueError, TypeError):\n        raise RuntimeError("Refusing malformed Day 6 database identity") from None\n    if (database == \'merlin_d6\') or int(identifier) != EXPECTED_CLUSTER:\n        raise RuntimeError("Refusing maintenance outside the verified Day 6 cluster")\n\n\ndef run_once(password: str, batch_size: int = 100) -> tuple[int, int]:\n    # Exact type check: rejects floats, strings, and booleans (type(True) is bool)\n    if type(batch_size) is not int:\n        raise ValueError("Batch size must be an integer")\n    if not 1 <= batch_size <= 1000:\n        raise ValueError("Batch size must be between 1 and 1000")\n    # This context commits on success and rolls back both cleanups if either fails.\n    with psycopg.connect(**TARGET, password=password) as conn:\n        verify_target(conn)\n        with conn.cursor() as cur:\n            # Stop a cycle rather than waiting indefinitely for locks or slow queries.\n            cur.execute("SET LOCAL lock_timeout = \'2s\'")\n            cur.execute("SET LOCAL statement_timeout = \'10s\'")\n            # %s binds a value safely; never build SQL by joining user input.\n            # First remove expired title-only notes, then purge old soft deletions.\n            cur.execute("SELECT public.cleanup_expired_blank_notes(%s)", (batch_size,))\n            expired = cur.fetchone()[0]\n            cur.execute("SELECT public.purge_deleted_notes(%s)", (batch_size,))\n            purged = cur.fetchone()[0]\n    return expired, purged\n\n\ndef main() -> None:\n    parser = argparse.ArgumentParser(description=__doc__)\n    parser.add_argument("--once", action="store_true", help="Run one maintenance cycle")\n    parser.add_argument("--interval", type=int, default=60, help="Seconds between cycles")\n    args = parser.parse_args()\n    if args.interval < 10:\n        parser.error("Interval must be at least 10 seconds")\n    # Prompt without echoing the password; do not store it in the source file.\n    password = getpass.getpass("Disposable merlin_d6 password: ")\n    try:\n        # The scheduler runs only while this foreground process remains open.\n        while True:\n            expired, purged = run_once(password)\n            print(f"Expired title-only notes: {expired}; purged deleted notes: {purged}")\n            # --once performs one cycle; otherwise pause before the next cycle.\n            if args.once:\n                break\n            time.sleep(args.interval)\n    except KeyboardInterrupt:\n        print("Maintenance stopped")\n    # Avoid printing connection details or credentials in database errors.\n    except (psycopg.Error, RuntimeError):\n        raise SystemExit("Maintenance failed; check target, migration and permissions. No credentials printed.")\n\n\nif __name__ == "__main__":\n    main()\n'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:1`; evidence status: DETECTED; origin: exhaustive.

AST proof: `04589e53be986aa48d1e5d6b6c54143b08c3689902658e5d29fc55d6bc2cef8a`; exact overlaps: none.

Changed expressions: `[{"original": "database != 'merlin_d6' or int(identifier) != EXPECTED_CLUSTER", "mutated": "database == 'merlin_d6' or int(identifier) != EXPECTED_CLUSTER", "line": 25}, {"original": "database != 'merlin_d6'", "mutated": "database == 'merlin_d6'", "line": 25}]`.

### `ast-notes_maintenance-25-112`

**KEEP** — Injects the specific behavioral change '"""Foreground scheduler restricted to the known disposable Day 6 cluster."""\n\nimport argparse\nimport getpass\nimport time\n\nimport psycopg\n\n# These fixed settings protect Sprint 0; this worker is for disposable storage only.\nEXPECTED_CLUSTER = 7694311451826794534\nTARGET = dict(host="127.0.0.1", port=55432, dbname="merlin_d6", user="merlin_d6", connect_timeout=3)\n\n\ndef verify_target(conn) -> None:\n    """Fail closed before writes; never accept another database or cluster."""\n    # Read the cluster fingerprint before allowing any cleanup writes.\n    with conn.cursor() as cur:\n        cur.execute("SELECT current_database(), system_identifier FROM pg_control_system()")\n        identity = cur.fetchone()\n    try:\n        database, identifier = identity\n        identifier = int(identifier)\n    except (ValueError, TypeError):\n        raise RuntimeError("Refusing malformed Day 6 database identity") from None\n    if database != "merlin_d6" or int(identifier) != EXPECTED_CLUSTER:\n        raise RuntimeError("Refusing maintenance outside the verified Day 6 cluster")\n\n\ndef run_once(password: str, batch_size: int = 100) -> tuple[int, int]:\n    # Exact type check: rejects floats, strings, and booleans (type(True) is bool)\n    if type(batch_size) is not int:\n        raise ValueError("Batch size must be an integer")\n    if not 1 <= batch_size <= 1000:\n        raise ValueError("Batch size must be between 1 and 1000")\n    # This context commits on success and rolls back both cleanups if either fails.\n    with psycopg.connect(**TARGET, password=password) as conn:\n        verify_target(conn)\n        with conn.cursor() as cur:\n            # Stop a cycle rather than waiting indefinitely for locks or slow queries.\n            cur.execute("SET LOCAL lock_timeout = \'2s\'")\n            cur.execute("SET LOCAL statement_timeout = \'10s\'")\n            # %s binds a value safely; never build SQL by joining user input.\n            # First remove expired title-only notes, then purge old soft deletions.\n            cur.execute("SELECT public.cleanup_expired_blank_notes(%s)", (batch_size,))\n            expired = cur.fetchone()[0]\n            cur.execute("SELECT public.purge_deleted_notes(%s)", (batch_size,))\n            purged = cur.fetchone()[0]\n    return expired, purged\n\n\ndef main() -> None:\n    parser = argparse.ArgumentParser(description=__doc__)\n    parser.add_argument("--once", action="store_true", help="Run one maintenance cycle")\n    parser.add_argument("--interval", type=int, default=60, help="Seconds between cycles")\n    args = parser.parse_args()\n    if args.interval < 10:\n        parser.error("Interval must be at least 10 seconds")\n    # Prompt without echoing the password; do not store it in the source file.\n    password = getpass.getpass("Disposable merlin_d6 password: ")\n    try:\n        # The scheduler runs only while this foreground process remains open.\n        while True:\n            expired, purged = run_once(password)\n            print(f"Expired title-only notes: {expired}; purged deleted notes: {purged}")\n            # --once performs one cycle; otherwise pause before the next cycle.\n            if args.once:\n                break\n            time.sleep(args.interval)\n    except KeyboardInterrupt:\n        print("Maintenance stopped")\n    # Avoid printing connection details or credentials in database errors.\n    except (psycopg.Error, RuntimeError):\n        raise SystemExit("Maintenance failed; check target, migration and permissions. No credentials printed.")\n\n\nif __name__ == "__main__":\n    main()\n' → '"""Foreground scheduler restricted to the known disposable Day 6 cluster."""\n\nimport argparse\nimport getpass\nimport time\n\nimport psycopg\n\n# These fixed settings protect Sprint 0; this worker is for disposable storage only.\nEXPECTED_CLUSTER = 7694311451826794534\nTARGET = dict(host="127.0.0.1", port=55432, dbname="merlin_d6", user="merlin_d6", connect_timeout=3)\n\n\ndef verify_target(conn) -> None:\n    """Fail closed before writes; never accept another database or cluster."""\n    # Read the cluster fingerprint before allowing any cleanup writes.\n    with conn.cursor() as cur:\n        cur.execute("SELECT current_database(), system_identifier FROM pg_control_system()")\n        identity = cur.fetchone()\n    try:\n        database, identifier = identity\n        identifier = int(identifier)\n    except (ValueError, TypeError):\n        raise RuntimeError("Refusing malformed Day 6 database identity") from None\n    if database != "merlin_d6" or (int(identifier) == EXPECTED_CLUSTER):\n        raise RuntimeError("Refusing maintenance outside the verified Day 6 cluster")\n\n\ndef run_once(password: str, batch_size: int = 100) -> tuple[int, int]:\n    # Exact type check: rejects floats, strings, and booleans (type(True) is bool)\n    if type(batch_size) is not int:\n        raise ValueError("Batch size must be an integer")\n    if not 1 <= batch_size <= 1000:\n        raise ValueError("Batch size must be between 1 and 1000")\n    # This context commits on success and rolls back both cleanups if either fails.\n    with psycopg.connect(**TARGET, password=password) as conn:\n        verify_target(conn)\n        with conn.cursor() as cur:\n            # Stop a cycle rather than waiting indefinitely for locks or slow queries.\n            cur.execute("SET LOCAL lock_timeout = \'2s\'")\n            cur.execute("SET LOCAL statement_timeout = \'10s\'")\n            # %s binds a value safely; never build SQL by joining user input.\n            # First remove expired title-only notes, then purge old soft deletions.\n            cur.execute("SELECT public.cleanup_expired_blank_notes(%s)", (batch_size,))\n            expired = cur.fetchone()[0]\n            cur.execute("SELECT public.purge_deleted_notes(%s)", (batch_size,))\n            purged = cur.fetchone()[0]\n    return expired, purged\n\n\ndef main() -> None:\n    parser = argparse.ArgumentParser(description=__doc__)\n    parser.add_argument("--once", action="store_true", help="Run one maintenance cycle")\n    parser.add_argument("--interval", type=int, default=60, help="Seconds between cycles")\n    args = parser.parse_args()\n    if args.interval < 10:\n        parser.error("Interval must be at least 10 seconds")\n    # Prompt without echoing the password; do not store it in the source file.\n    password = getpass.getpass("Disposable merlin_d6 password: ")\n    try:\n        # The scheduler runs only while this foreground process remains open.\n        while True:\n            expired, purged = run_once(password)\n            print(f"Expired title-only notes: {expired}; purged deleted notes: {purged}")\n            # --once performs one cycle; otherwise pause before the next cycle.\n            if args.once:\n                break\n            time.sleep(args.interval)\n    except KeyboardInterrupt:\n        print("Maintenance stopped")\n    # Avoid printing connection details or credentials in database errors.\n    except (psycopg.Error, RuntimeError):\n        raise SystemExit("Maintenance failed; check target, migration and permissions. No credentials printed.")\n\n\nif __name__ == "__main__":\n    main()\n'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/notes_maintenance.py:1`; evidence status: DETECTED; origin: exhaustive.

AST proof: `0cead3cd1313b98853d46a70f92c68addf570fadb9e872382634fedf3e002211`; exact overlaps: none.

Changed expressions: `[{"original": "database != 'merlin_d6' or int(identifier) != EXPECTED_CLUSTER", "mutated": "database != 'merlin_d6' or int(identifier) == EXPECTED_CLUSTER", "line": 25}, {"original": "int(identifier) != EXPECTED_CLUSTER", "mutated": "int(identifier) == EXPECTED_CLUSTER", "line": 25}]`.

### `ast-note_rules-28-56`

**KEEP** — Injects the specific behavioral change '"""Input rules to call before a future API writes notes or account email."""\n\nfrom dataclasses import dataclass\n\nimport emoji\nimport regex\n\n# A grapheme is one displayed character, even when several Unicode parts form it.\n_GRAPHEMES = regex.compile(r"\\X")\n\n\ndef weighted_length(value: str) -> int:\n    """Count a known displayed emoji as four, every other grapheme as one."""\n    if not isinstance(value, str):\n        raise ValueError("Text must be a string")\n    try:\n        value.encode("utf-8")\n    except UnicodeEncodeError:\n        raise ValueError("Text must be valid UTF-8") from None\n    if "\\x00" in value:\n        raise ValueError("PostgreSQL text cannot contain NUL")\n    # The pinned emoji library recognizes complete sequences, such as a family emoji.\n    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))\n\n\ndef normalize_email(value: str | None) -> str | None:\n    """Preserve display casing; database lower(email) enforces uniqueness."""\n    if value is None:\n        return None\n    weighted_length(value)  # Reject invalid text, not validate email ownership.\n    # Remove edge whitespace; an empty result becomes the database NULL value.\n    return value.strip() or None\n\n\n# This result carries a decision; it never writes to or deletes from the database.\n@dataclass(frozen=True)\nclass ValidatedNote:\n    title: str | None\n    body: str\n    delete_on_save: bool\n\n\ndef validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:\n    """Normalize absent text and identify an explicitly saved blank note."""\n    # Enforce strict boolean type checking\n    if not isinstance(is_draft, bool):\n        raise ValueError("is_draft must be a boolean")\n    # A whitespace-only title is absent; keep the original text of a real title.\n    if title is not None:\n        title_length = weighted_length(title)\n        if not title.strip():\n            title = None\n        elif title_length > 175:\n            raise ValueError("Title exceeds weighted length 175")\n    # Do not strip the body: spaces and line breaks may be part of the writing.\n    body = "" if body is None else body\n    if weighted_length(body) > 7000:\n        raise ValueError("Body exceeds weighted length 7000")\n    # Explicitly saving a blank note requests deletion; a blank draft may stay.\n    return ValidatedNote(title, body, not is_draft and title is None and not body.strip())\n' → '"""Input rules to call before a future API writes notes or account email."""\n\nfrom dataclasses import dataclass\n\nimport emoji\nimport regex\n\n# A grapheme is one displayed character, even when several Unicode parts form it.\n_GRAPHEMES = regex.compile(r"\\X")\n\n\ndef weighted_length(value: str) -> int:\n    """Count a known displayed emoji as four, every other grapheme as one."""\n    if not isinstance(value, str):\n        raise ValueError("Text must be a string")\n    try:\n        value.encode("utf-8")\n    except UnicodeEncodeError:\n        raise ValueError("Text must be valid UTF-8") from None\n    if "\\x00" in value:\n        raise ValueError("PostgreSQL text cannot contain NUL")\n    # The pinned emoji library recognizes complete sequences, such as a family emoji.\n    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))\n\n\ndef normalize_email(value: str | None) -> str | None:\n    """Preserve display casing; database lower(email) enforces uniqueness."""\n    if (value is not None):\n        return None\n    weighted_length(value)  # Reject invalid text, not validate email ownership.\n    # Remove edge whitespace; an empty result becomes the database NULL value.\n    return value.strip() or None\n\n\n# This result carries a decision; it never writes to or deletes from the database.\n@dataclass(frozen=True)\nclass ValidatedNote:\n    title: str | None\n    body: str\n    delete_on_save: bool\n\n\ndef validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:\n    """Normalize absent text and identify an explicitly saved blank note."""\n    # Enforce strict boolean type checking\n    if not isinstance(is_draft, bool):\n        raise ValueError("is_draft must be a boolean")\n    # A whitespace-only title is absent; keep the original text of a real title.\n    if title is not None:\n        title_length = weighted_length(title)\n        if not title.strip():\n            title = None\n        elif title_length > 175:\n            raise ValueError("Title exceeds weighted length 175")\n    # Do not strip the body: spaces and line breaks may be part of the writing.\n    body = "" if body is None else body\n    if weighted_length(body) > 7000:\n        raise ValueError("Body exceeds weighted length 7000")\n    # Explicitly saving a blank note requests deletion; a blank draft may stay.\n    return ValidatedNote(title, body, not is_draft and title is None and not body.strip())\n'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:1`; evidence status: DETECTED; origin: exhaustive.

AST proof: `1043b828645fc6646ba6825d6f976c062c2a2eb32f37272a5eb5af7583a589eb`; exact overlaps: none.

Changed expressions: `[{"original": "value is None", "mutated": "value is not None", "line": 28}]`.

### `ast-note_rules-32-59`

**KEEP** — Injects the specific behavioral change '"""Input rules to call before a future API writes notes or account email."""\n\nfrom dataclasses import dataclass\n\nimport emoji\nimport regex\n\n# A grapheme is one displayed character, even when several Unicode parts form it.\n_GRAPHEMES = regex.compile(r"\\X")\n\n\ndef weighted_length(value: str) -> int:\n    """Count a known displayed emoji as four, every other grapheme as one."""\n    if not isinstance(value, str):\n        raise ValueError("Text must be a string")\n    try:\n        value.encode("utf-8")\n    except UnicodeEncodeError:\n        raise ValueError("Text must be valid UTF-8") from None\n    if "\\x00" in value:\n        raise ValueError("PostgreSQL text cannot contain NUL")\n    # The pinned emoji library recognizes complete sequences, such as a family emoji.\n    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))\n\n\ndef normalize_email(value: str | None) -> str | None:\n    """Preserve display casing; database lower(email) enforces uniqueness."""\n    if value is None:\n        return None\n    weighted_length(value)  # Reject invalid text, not validate email ownership.\n    # Remove edge whitespace; an empty result becomes the database NULL value.\n    return value.strip() or None\n\n\n# This result carries a decision; it never writes to or deletes from the database.\n@dataclass(frozen=True)\nclass ValidatedNote:\n    title: str | None\n    body: str\n    delete_on_save: bool\n\n\ndef validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:\n    """Normalize absent text and identify an explicitly saved blank note."""\n    # Enforce strict boolean type checking\n    if not isinstance(is_draft, bool):\n        raise ValueError("is_draft must be a boolean")\n    # A whitespace-only title is absent; keep the original text of a real title.\n    if title is not None:\n        title_length = weighted_length(title)\n        if not title.strip():\n            title = None\n        elif title_length > 175:\n            raise ValueError("Title exceeds weighted length 175")\n    # Do not strip the body: spaces and line breaks may be part of the writing.\n    body = "" if body is None else body\n    if weighted_length(body) > 7000:\n        raise ValueError("Body exceeds weighted length 7000")\n    # Explicitly saving a blank note requests deletion; a blank draft may stay.\n    return ValidatedNote(title, body, not is_draft and title is None and not body.strip())\n' → '"""Input rules to call before a future API writes notes or account email."""\n\nfrom dataclasses import dataclass\n\nimport emoji\nimport regex\n\n# A grapheme is one displayed character, even when several Unicode parts form it.\n_GRAPHEMES = regex.compile(r"\\X")\n\n\ndef weighted_length(value: str) -> int:\n    """Count a known displayed emoji as four, every other grapheme as one."""\n    if not isinstance(value, str):\n        raise ValueError("Text must be a string")\n    try:\n        value.encode("utf-8")\n    except UnicodeEncodeError:\n        raise ValueError("Text must be valid UTF-8") from None\n    if "\\x00" in value:\n        raise ValueError("PostgreSQL text cannot contain NUL")\n    # The pinned emoji library recognizes complete sequences, such as a family emoji.\n    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))\n\n\ndef normalize_email(value: str | None) -> str | None:\n    """Preserve display casing; database lower(email) enforces uniqueness."""\n    if value is None:\n        return None\n    weighted_length(value)  # Reject invalid text, not validate email ownership.\n    # Remove edge whitespace; an empty result becomes the database NULL value.\n    return (value.strip() and None)\n\n\n# This result carries a decision; it never writes to or deletes from the database.\n@dataclass(frozen=True)\nclass ValidatedNote:\n    title: str | None\n    body: str\n    delete_on_save: bool\n\n\ndef validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:\n    """Normalize absent text and identify an explicitly saved blank note."""\n    # Enforce strict boolean type checking\n    if not isinstance(is_draft, bool):\n        raise ValueError("is_draft must be a boolean")\n    # A whitespace-only title is absent; keep the original text of a real title.\n    if title is not None:\n        title_length = weighted_length(title)\n        if not title.strip():\n            title = None\n        elif title_length > 175:\n            raise ValueError("Title exceeds weighted length 175")\n    # Do not strip the body: spaces and line breaks may be part of the writing.\n    body = "" if body is None else body\n    if weighted_length(body) > 7000:\n        raise ValueError("Body exceeds weighted length 7000")\n    # Explicitly saving a blank note requests deletion; a blank draft may stay.\n    return ValidatedNote(title, body, not is_draft and title is None and not body.strip())\n'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:1`; evidence status: DETECTED; origin: exhaustive.

AST proof: `0e959a442808fce95d78829763ae9f5934d295ac53bb5fb07ca1ce29f16085c2`; exact overlaps: none.

Changed expressions: `[{"original": "value.strip() or None", "mutated": "value.strip() and None", "line": 32}]`.

### `ast-note_rules-49-78`

**KEEP** — Injects the specific behavioral change '"""Input rules to call before a future API writes notes or account email."""\n\nfrom dataclasses import dataclass\n\nimport emoji\nimport regex\n\n# A grapheme is one displayed character, even when several Unicode parts form it.\n_GRAPHEMES = regex.compile(r"\\X")\n\n\ndef weighted_length(value: str) -> int:\n    """Count a known displayed emoji as four, every other grapheme as one."""\n    if not isinstance(value, str):\n        raise ValueError("Text must be a string")\n    try:\n        value.encode("utf-8")\n    except UnicodeEncodeError:\n        raise ValueError("Text must be valid UTF-8") from None\n    if "\\x00" in value:\n        raise ValueError("PostgreSQL text cannot contain NUL")\n    # The pinned emoji library recognizes complete sequences, such as a family emoji.\n    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))\n\n\ndef normalize_email(value: str | None) -> str | None:\n    """Preserve display casing; database lower(email) enforces uniqueness."""\n    if value is None:\n        return None\n    weighted_length(value)  # Reject invalid text, not validate email ownership.\n    # Remove edge whitespace; an empty result becomes the database NULL value.\n    return value.strip() or None\n\n\n# This result carries a decision; it never writes to or deletes from the database.\n@dataclass(frozen=True)\nclass ValidatedNote:\n    title: str | None\n    body: str\n    delete_on_save: bool\n\n\ndef validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:\n    """Normalize absent text and identify an explicitly saved blank note."""\n    # Enforce strict boolean type checking\n    if not isinstance(is_draft, bool):\n        raise ValueError("is_draft must be a boolean")\n    # A whitespace-only title is absent; keep the original text of a real title.\n    if title is not None:\n        title_length = weighted_length(title)\n        if not title.strip():\n            title = None\n        elif title_length > 175:\n            raise ValueError("Title exceeds weighted length 175")\n    # Do not strip the body: spaces and line breaks may be part of the writing.\n    body = "" if body is None else body\n    if weighted_length(body) > 7000:\n        raise ValueError("Body exceeds weighted length 7000")\n    # Explicitly saving a blank note requests deletion; a blank draft may stay.\n    return ValidatedNote(title, body, not is_draft and title is None and not body.strip())\n' → '"""Input rules to call before a future API writes notes or account email."""\n\nfrom dataclasses import dataclass\n\nimport emoji\nimport regex\n\n# A grapheme is one displayed character, even when several Unicode parts form it.\n_GRAPHEMES = regex.compile(r"\\X")\n\n\ndef weighted_length(value: str) -> int:\n    """Count a known displayed emoji as four, every other grapheme as one."""\n    if not isinstance(value, str):\n        raise ValueError("Text must be a string")\n    try:\n        value.encode("utf-8")\n    except UnicodeEncodeError:\n        raise ValueError("Text must be valid UTF-8") from None\n    if "\\x00" in value:\n        raise ValueError("PostgreSQL text cannot contain NUL")\n    # The pinned emoji library recognizes complete sequences, such as a family emoji.\n    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))\n\n\ndef normalize_email(value: str | None) -> str | None:\n    """Preserve display casing; database lower(email) enforces uniqueness."""\n    if value is None:\n        return None\n    weighted_length(value)  # Reject invalid text, not validate email ownership.\n    # Remove edge whitespace; an empty result becomes the database NULL value.\n    return value.strip() or None\n\n\n# This result carries a decision; it never writes to or deletes from the database.\n@dataclass(frozen=True)\nclass ValidatedNote:\n    title: str | None\n    body: str\n    delete_on_save: bool\n\n\ndef validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:\n    """Normalize absent text and identify an explicitly saved blank note."""\n    # Enforce strict boolean type checking\n    if not isinstance(is_draft, bool):\n        raise ValueError("is_draft must be a boolean")\n    # A whitespace-only title is absent; keep the original text of a real title.\n    if (title is None):\n        title_length = weighted_length(title)\n        if not title.strip():\n            title = None\n        elif title_length > 175:\n            raise ValueError("Title exceeds weighted length 175")\n    # Do not strip the body: spaces and line breaks may be part of the writing.\n    body = "" if body is None else body\n    if weighted_length(body) > 7000:\n        raise ValueError("Body exceeds weighted length 7000")\n    # Explicitly saving a blank note requests deletion; a blank draft may stay.\n    return ValidatedNote(title, body, not is_draft and title is None and not body.strip())\n'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:1`; evidence status: DETECTED; origin: exhaustive.

AST proof: `8b05b1a9275ce5e1f090b65c0bb4d3829fa3ee96923277f1734f00cab6869d33`; exact overlaps: none.

Changed expressions: `[{"original": "title is not None", "mutated": "title is None", "line": 49}]`.

### `ast-note_rules-57-83`

**KEEP** — Injects the specific behavioral change '"""Input rules to call before a future API writes notes or account email."""\n\nfrom dataclasses import dataclass\n\nimport emoji\nimport regex\n\n# A grapheme is one displayed character, even when several Unicode parts form it.\n_GRAPHEMES = regex.compile(r"\\X")\n\n\ndef weighted_length(value: str) -> int:\n    """Count a known displayed emoji as four, every other grapheme as one."""\n    if not isinstance(value, str):\n        raise ValueError("Text must be a string")\n    try:\n        value.encode("utf-8")\n    except UnicodeEncodeError:\n        raise ValueError("Text must be valid UTF-8") from None\n    if "\\x00" in value:\n        raise ValueError("PostgreSQL text cannot contain NUL")\n    # The pinned emoji library recognizes complete sequences, such as a family emoji.\n    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))\n\n\ndef normalize_email(value: str | None) -> str | None:\n    """Preserve display casing; database lower(email) enforces uniqueness."""\n    if value is None:\n        return None\n    weighted_length(value)  # Reject invalid text, not validate email ownership.\n    # Remove edge whitespace; an empty result becomes the database NULL value.\n    return value.strip() or None\n\n\n# This result carries a decision; it never writes to or deletes from the database.\n@dataclass(frozen=True)\nclass ValidatedNote:\n    title: str | None\n    body: str\n    delete_on_save: bool\n\n\ndef validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:\n    """Normalize absent text and identify an explicitly saved blank note."""\n    # Enforce strict boolean type checking\n    if not isinstance(is_draft, bool):\n        raise ValueError("is_draft must be a boolean")\n    # A whitespace-only title is absent; keep the original text of a real title.\n    if title is not None:\n        title_length = weighted_length(title)\n        if not title.strip():\n            title = None\n        elif title_length > 175:\n            raise ValueError("Title exceeds weighted length 175")\n    # Do not strip the body: spaces and line breaks may be part of the writing.\n    body = "" if body is None else body\n    if weighted_length(body) > 7000:\n        raise ValueError("Body exceeds weighted length 7000")\n    # Explicitly saving a blank note requests deletion; a blank draft may stay.\n    return ValidatedNote(title, body, not is_draft and title is None and not body.strip())\n' → '"""Input rules to call before a future API writes notes or account email."""\n\nfrom dataclasses import dataclass\n\nimport emoji\nimport regex\n\n# A grapheme is one displayed character, even when several Unicode parts form it.\n_GRAPHEMES = regex.compile(r"\\X")\n\n\ndef weighted_length(value: str) -> int:\n    """Count a known displayed emoji as four, every other grapheme as one."""\n    if not isinstance(value, str):\n        raise ValueError("Text must be a string")\n    try:\n        value.encode("utf-8")\n    except UnicodeEncodeError:\n        raise ValueError("Text must be valid UTF-8") from None\n    if "\\x00" in value:\n        raise ValueError("PostgreSQL text cannot contain NUL")\n    # The pinned emoji library recognizes complete sequences, such as a family emoji.\n    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))\n\n\ndef normalize_email(value: str | None) -> str | None:\n    """Preserve display casing; database lower(email) enforces uniqueness."""\n    if value is None:\n        return None\n    weighted_length(value)  # Reject invalid text, not validate email ownership.\n    # Remove edge whitespace; an empty result becomes the database NULL value.\n    return value.strip() or None\n\n\n# This result carries a decision; it never writes to or deletes from the database.\n@dataclass(frozen=True)\nclass ValidatedNote:\n    title: str | None\n    body: str\n    delete_on_save: bool\n\n\ndef validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:\n    """Normalize absent text and identify an explicitly saved blank note."""\n    # Enforce strict boolean type checking\n    if not isinstance(is_draft, bool):\n        raise ValueError("is_draft must be a boolean")\n    # A whitespace-only title is absent; keep the original text of a real title.\n    if title is not None:\n        title_length = weighted_length(title)\n        if not title.strip():\n            title = None\n        elif title_length > 175:\n            raise ValueError("Title exceeds weighted length 175")\n    # Do not strip the body: spaces and line breaks may be part of the writing.\n    body = "" if body is None else body\n    if (weighted_length(body) <= 7000):\n        raise ValueError("Body exceeds weighted length 7000")\n    # Explicitly saving a blank note requests deletion; a blank draft may stay.\n    return ValidatedNote(title, body, not is_draft and title is None and not body.strip())\n'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:1`; evidence status: DETECTED; origin: exhaustive.

AST proof: `581117bc256197af49d93ff883585d336b433ff71129deebda1d0bf3c3d56d75`; exact overlaps: none.

Changed expressions: `[{"original": "weighted_length(body) > 7000", "mutated": "weighted_length(body) <= 7000", "line": 57}]`.

### `ast-note_rules-56-138`

**KEEP** — Injects the specific behavioral change '"""Input rules to call before a future API writes notes or account email."""\n\nfrom dataclasses import dataclass\n\nimport emoji\nimport regex\n\n# A grapheme is one displayed character, even when several Unicode parts form it.\n_GRAPHEMES = regex.compile(r"\\X")\n\n\ndef weighted_length(value: str) -> int:\n    """Count a known displayed emoji as four, every other grapheme as one."""\n    if not isinstance(value, str):\n        raise ValueError("Text must be a string")\n    try:\n        value.encode("utf-8")\n    except UnicodeEncodeError:\n        raise ValueError("Text must be valid UTF-8") from None\n    if "\\x00" in value:\n        raise ValueError("PostgreSQL text cannot contain NUL")\n    # The pinned emoji library recognizes complete sequences, such as a family emoji.\n    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))\n\n\ndef normalize_email(value: str | None) -> str | None:\n    """Preserve display casing; database lower(email) enforces uniqueness."""\n    if value is None:\n        return None\n    weighted_length(value)  # Reject invalid text, not validate email ownership.\n    # Remove edge whitespace; an empty result becomes the database NULL value.\n    return value.strip() or None\n\n\n# This result carries a decision; it never writes to or deletes from the database.\n@dataclass(frozen=True)\nclass ValidatedNote:\n    title: str | None\n    body: str\n    delete_on_save: bool\n\n\ndef validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:\n    """Normalize absent text and identify an explicitly saved blank note."""\n    # Enforce strict boolean type checking\n    if not isinstance(is_draft, bool):\n        raise ValueError("is_draft must be a boolean")\n    # A whitespace-only title is absent; keep the original text of a real title.\n    if title is not None:\n        title_length = weighted_length(title)\n        if not title.strip():\n            title = None\n        elif title_length > 175:\n            raise ValueError("Title exceeds weighted length 175")\n    # Do not strip the body: spaces and line breaks may be part of the writing.\n    body = "" if body is None else body\n    if weighted_length(body) > 7000:\n        raise ValueError("Body exceeds weighted length 7000")\n    # Explicitly saving a blank note requests deletion; a blank draft may stay.\n    return ValidatedNote(title, body, not is_draft and title is None and not body.strip())\n' → '"""Input rules to call before a future API writes notes or account email."""\n\nfrom dataclasses import dataclass\n\nimport emoji\nimport regex\n\n# A grapheme is one displayed character, even when several Unicode parts form it.\n_GRAPHEMES = regex.compile(r"\\X")\n\n\ndef weighted_length(value: str) -> int:\n    """Count a known displayed emoji as four, every other grapheme as one."""\n    if not isinstance(value, str):\n        raise ValueError("Text must be a string")\n    try:\n        value.encode("utf-8")\n    except UnicodeEncodeError:\n        raise ValueError("Text must be valid UTF-8") from None\n    if "\\x00" in value:\n        raise ValueError("PostgreSQL text cannot contain NUL")\n    # The pinned emoji library recognizes complete sequences, such as a family emoji.\n    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))\n\n\ndef normalize_email(value: str | None) -> str | None:\n    """Preserve display casing; database lower(email) enforces uniqueness."""\n    if value is None:\n        return None\n    weighted_length(value)  # Reject invalid text, not validate email ownership.\n    # Remove edge whitespace; an empty result becomes the database NULL value.\n    return value.strip() or None\n\n\n# This result carries a decision; it never writes to or deletes from the database.\n@dataclass(frozen=True)\nclass ValidatedNote:\n    title: str | None\n    body: str\n    delete_on_save: bool\n\n\ndef validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:\n    """Normalize absent text and identify an explicitly saved blank note."""\n    # Enforce strict boolean type checking\n    if not isinstance(is_draft, bool):\n        raise ValueError("is_draft must be a boolean")\n    # A whitespace-only title is absent; keep the original text of a real title.\n    if title is not None:\n        title_length = weighted_length(title)\n        if not title.strip():\n            title = None\n        elif title_length > 175:\n            raise ValueError("Title exceeds weighted length 175")\n    # Do not strip the body: spaces and line breaks may be part of the writing.\n    body = "" if (body is not None) else body\n    if weighted_length(body) > 7000:\n        raise ValueError("Body exceeds weighted length 7000")\n    # Explicitly saving a blank note requests deletion; a blank draft may stay.\n    return ValidatedNote(title, body, not is_draft and title is None and not body.strip())\n'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:1`; evidence status: DETECTED; origin: exhaustive.

AST proof: `a04cad8cbd3955c47738d66aae872a927f407f43b0c37d01722b4de7f4e966ec`; exact overlaps: none.

Changed expressions: `[{"original": "body is None", "mutated": "body is not None", "line": 56}]`.

### `ast-note_rules-60-148`

**KEEP** — Injects the specific behavioral change '"""Input rules to call before a future API writes notes or account email."""\n\nfrom dataclasses import dataclass\n\nimport emoji\nimport regex\n\n# A grapheme is one displayed character, even when several Unicode parts form it.\n_GRAPHEMES = regex.compile(r"\\X")\n\n\ndef weighted_length(value: str) -> int:\n    """Count a known displayed emoji as four, every other grapheme as one."""\n    if not isinstance(value, str):\n        raise ValueError("Text must be a string")\n    try:\n        value.encode("utf-8")\n    except UnicodeEncodeError:\n        raise ValueError("Text must be valid UTF-8") from None\n    if "\\x00" in value:\n        raise ValueError("PostgreSQL text cannot contain NUL")\n    # The pinned emoji library recognizes complete sequences, such as a family emoji.\n    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))\n\n\ndef normalize_email(value: str | None) -> str | None:\n    """Preserve display casing; database lower(email) enforces uniqueness."""\n    if value is None:\n        return None\n    weighted_length(value)  # Reject invalid text, not validate email ownership.\n    # Remove edge whitespace; an empty result becomes the database NULL value.\n    return value.strip() or None\n\n\n# This result carries a decision; it never writes to or deletes from the database.\n@dataclass(frozen=True)\nclass ValidatedNote:\n    title: str | None\n    body: str\n    delete_on_save: bool\n\n\ndef validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:\n    """Normalize absent text and identify an explicitly saved blank note."""\n    # Enforce strict boolean type checking\n    if not isinstance(is_draft, bool):\n        raise ValueError("is_draft must be a boolean")\n    # A whitespace-only title is absent; keep the original text of a real title.\n    if title is not None:\n        title_length = weighted_length(title)\n        if not title.strip():\n            title = None\n        elif title_length > 175:\n            raise ValueError("Title exceeds weighted length 175")\n    # Do not strip the body: spaces and line breaks may be part of the writing.\n    body = "" if body is None else body\n    if weighted_length(body) > 7000:\n        raise ValueError("Body exceeds weighted length 7000")\n    # Explicitly saving a blank note requests deletion; a blank draft may stay.\n    return ValidatedNote(title, body, not is_draft and title is None and not body.strip())\n' → '"""Input rules to call before a future API writes notes or account email."""\n\nfrom dataclasses import dataclass\n\nimport emoji\nimport regex\n\n# A grapheme is one displayed character, even when several Unicode parts form it.\n_GRAPHEMES = regex.compile(r"\\X")\n\n\ndef weighted_length(value: str) -> int:\n    """Count a known displayed emoji as four, every other grapheme as one."""\n    if not isinstance(value, str):\n        raise ValueError("Text must be a string")\n    try:\n        value.encode("utf-8")\n    except UnicodeEncodeError:\n        raise ValueError("Text must be valid UTF-8") from None\n    if "\\x00" in value:\n        raise ValueError("PostgreSQL text cannot contain NUL")\n    # The pinned emoji library recognizes complete sequences, such as a family emoji.\n    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))\n\n\ndef normalize_email(value: str | None) -> str | None:\n    """Preserve display casing; database lower(email) enforces uniqueness."""\n    if value is None:\n        return None\n    weighted_length(value)  # Reject invalid text, not validate email ownership.\n    # Remove edge whitespace; an empty result becomes the database NULL value.\n    return value.strip() or None\n\n\n# This result carries a decision; it never writes to or deletes from the database.\n@dataclass(frozen=True)\nclass ValidatedNote:\n    title: str | None\n    body: str\n    delete_on_save: bool\n\n\ndef validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:\n    """Normalize absent text and identify an explicitly saved blank note."""\n    # Enforce strict boolean type checking\n    if not isinstance(is_draft, bool):\n        raise ValueError("is_draft must be a boolean")\n    # A whitespace-only title is absent; keep the original text of a real title.\n    if title is not None:\n        title_length = weighted_length(title)\n        if not title.strip():\n            title = None\n        elif title_length > 175:\n            raise ValueError("Title exceeds weighted length 175")\n    # Do not strip the body: spaces and line breaks may be part of the writing.\n    body = "" if body is None else body\n    if weighted_length(body) > 7000:\n        raise ValueError("Body exceeds weighted length 7000")\n    # Explicitly saving a blank note requests deletion; a blank draft may stay.\n    return ValidatedNote(title, body, (not is_draft or title is None or (not body.strip())))\n'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:1`; evidence status: DETECTED; origin: exhaustive.

AST proof: `b6625cdad3d4123396d03441aa2046e11cfc4b695702409c6ba04b65d1290eb0`; exact overlaps: none.

Changed expressions: `[{"original": "not is_draft and title is None and (not body.strip())", "mutated": "not is_draft or title is None or (not body.strip())", "line": 60}]`.

### `ast-note_rules-53-195`

**KEEP** — Injects the specific behavioral change '"""Input rules to call before a future API writes notes or account email."""\n\nfrom dataclasses import dataclass\n\nimport emoji\nimport regex\n\n# A grapheme is one displayed character, even when several Unicode parts form it.\n_GRAPHEMES = regex.compile(r"\\X")\n\n\ndef weighted_length(value: str) -> int:\n    """Count a known displayed emoji as four, every other grapheme as one."""\n    if not isinstance(value, str):\n        raise ValueError("Text must be a string")\n    try:\n        value.encode("utf-8")\n    except UnicodeEncodeError:\n        raise ValueError("Text must be valid UTF-8") from None\n    if "\\x00" in value:\n        raise ValueError("PostgreSQL text cannot contain NUL")\n    # The pinned emoji library recognizes complete sequences, such as a family emoji.\n    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))\n\n\ndef normalize_email(value: str | None) -> str | None:\n    """Preserve display casing; database lower(email) enforces uniqueness."""\n    if value is None:\n        return None\n    weighted_length(value)  # Reject invalid text, not validate email ownership.\n    # Remove edge whitespace; an empty result becomes the database NULL value.\n    return value.strip() or None\n\n\n# This result carries a decision; it never writes to or deletes from the database.\n@dataclass(frozen=True)\nclass ValidatedNote:\n    title: str | None\n    body: str\n    delete_on_save: bool\n\n\ndef validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:\n    """Normalize absent text and identify an explicitly saved blank note."""\n    # Enforce strict boolean type checking\n    if not isinstance(is_draft, bool):\n        raise ValueError("is_draft must be a boolean")\n    # A whitespace-only title is absent; keep the original text of a real title.\n    if title is not None:\n        title_length = weighted_length(title)\n        if not title.strip():\n            title = None\n        elif title_length > 175:\n            raise ValueError("Title exceeds weighted length 175")\n    # Do not strip the body: spaces and line breaks may be part of the writing.\n    body = "" if body is None else body\n    if weighted_length(body) > 7000:\n        raise ValueError("Body exceeds weighted length 7000")\n    # Explicitly saving a blank note requests deletion; a blank draft may stay.\n    return ValidatedNote(title, body, not is_draft and title is None and not body.strip())\n' → '"""Input rules to call before a future API writes notes or account email."""\n\nfrom dataclasses import dataclass\n\nimport emoji\nimport regex\n\n# A grapheme is one displayed character, even when several Unicode parts form it.\n_GRAPHEMES = regex.compile(r"\\X")\n\n\ndef weighted_length(value: str) -> int:\n    """Count a known displayed emoji as four, every other grapheme as one."""\n    if not isinstance(value, str):\n        raise ValueError("Text must be a string")\n    try:\n        value.encode("utf-8")\n    except UnicodeEncodeError:\n        raise ValueError("Text must be valid UTF-8") from None\n    if "\\x00" in value:\n        raise ValueError("PostgreSQL text cannot contain NUL")\n    # The pinned emoji library recognizes complete sequences, such as a family emoji.\n    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))\n\n\ndef normalize_email(value: str | None) -> str | None:\n    """Preserve display casing; database lower(email) enforces uniqueness."""\n    if value is None:\n        return None\n    weighted_length(value)  # Reject invalid text, not validate email ownership.\n    # Remove edge whitespace; an empty result becomes the database NULL value.\n    return value.strip() or None\n\n\n# This result carries a decision; it never writes to or deletes from the database.\n@dataclass(frozen=True)\nclass ValidatedNote:\n    title: str | None\n    body: str\n    delete_on_save: bool\n\n\ndef validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:\n    """Normalize absent text and identify an explicitly saved blank note."""\n    # Enforce strict boolean type checking\n    if not isinstance(is_draft, bool):\n        raise ValueError("is_draft must be a boolean")\n    # A whitespace-only title is absent; keep the original text of a real title.\n    if title is not None:\n        title_length = weighted_length(title)\n        if not title.strip():\n            title = None\n        elif (title_length <= 175):\n            raise ValueError("Title exceeds weighted length 175")\n    # Do not strip the body: spaces and line breaks may be part of the writing.\n    body = "" if body is None else body\n    if weighted_length(body) > 7000:\n        raise ValueError("Body exceeds weighted length 7000")\n    # Explicitly saving a blank note requests deletion; a blank draft may stay.\n    return ValidatedNote(title, body, not is_draft and title is None and not body.strip())\n'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:1`; evidence status: DETECTED; origin: exhaustive.

AST proof: `e11b04571307bdb62c2f2285c4bc65e7bf975cf5c89783a999b0c452f2fbe168`; exact overlaps: none.

Changed expressions: `[{"original": "title_length > 175", "mutated": "title_length <= 175", "line": 53}]`.

### `ast-note_rules-60-210`

**KEEP** — Injects the specific behavioral change '"""Input rules to call before a future API writes notes or account email."""\n\nfrom dataclasses import dataclass\n\nimport emoji\nimport regex\n\n# A grapheme is one displayed character, even when several Unicode parts form it.\n_GRAPHEMES = regex.compile(r"\\X")\n\n\ndef weighted_length(value: str) -> int:\n    """Count a known displayed emoji as four, every other grapheme as one."""\n    if not isinstance(value, str):\n        raise ValueError("Text must be a string")\n    try:\n        value.encode("utf-8")\n    except UnicodeEncodeError:\n        raise ValueError("Text must be valid UTF-8") from None\n    if "\\x00" in value:\n        raise ValueError("PostgreSQL text cannot contain NUL")\n    # The pinned emoji library recognizes complete sequences, such as a family emoji.\n    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))\n\n\ndef normalize_email(value: str | None) -> str | None:\n    """Preserve display casing; database lower(email) enforces uniqueness."""\n    if value is None:\n        return None\n    weighted_length(value)  # Reject invalid text, not validate email ownership.\n    # Remove edge whitespace; an empty result becomes the database NULL value.\n    return value.strip() or None\n\n\n# This result carries a decision; it never writes to or deletes from the database.\n@dataclass(frozen=True)\nclass ValidatedNote:\n    title: str | None\n    body: str\n    delete_on_save: bool\n\n\ndef validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:\n    """Normalize absent text and identify an explicitly saved blank note."""\n    # Enforce strict boolean type checking\n    if not isinstance(is_draft, bool):\n        raise ValueError("is_draft must be a boolean")\n    # A whitespace-only title is absent; keep the original text of a real title.\n    if title is not None:\n        title_length = weighted_length(title)\n        if not title.strip():\n            title = None\n        elif title_length > 175:\n            raise ValueError("Title exceeds weighted length 175")\n    # Do not strip the body: spaces and line breaks may be part of the writing.\n    body = "" if body is None else body\n    if weighted_length(body) > 7000:\n        raise ValueError("Body exceeds weighted length 7000")\n    # Explicitly saving a blank note requests deletion; a blank draft may stay.\n    return ValidatedNote(title, body, not is_draft and title is None and not body.strip())\n' → '"""Input rules to call before a future API writes notes or account email."""\n\nfrom dataclasses import dataclass\n\nimport emoji\nimport regex\n\n# A grapheme is one displayed character, even when several Unicode parts form it.\n_GRAPHEMES = regex.compile(r"\\X")\n\n\ndef weighted_length(value: str) -> int:\n    """Count a known displayed emoji as four, every other grapheme as one."""\n    if not isinstance(value, str):\n        raise ValueError("Text must be a string")\n    try:\n        value.encode("utf-8")\n    except UnicodeEncodeError:\n        raise ValueError("Text must be valid UTF-8") from None\n    if "\\x00" in value:\n        raise ValueError("PostgreSQL text cannot contain NUL")\n    # The pinned emoji library recognizes complete sequences, such as a family emoji.\n    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))\n\n\ndef normalize_email(value: str | None) -> str | None:\n    """Preserve display casing; database lower(email) enforces uniqueness."""\n    if value is None:\n        return None\n    weighted_length(value)  # Reject invalid text, not validate email ownership.\n    # Remove edge whitespace; an empty result becomes the database NULL value.\n    return value.strip() or None\n\n\n# This result carries a decision; it never writes to or deletes from the database.\n@dataclass(frozen=True)\nclass ValidatedNote:\n    title: str | None\n    body: str\n    delete_on_save: bool\n\n\ndef validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:\n    """Normalize absent text and identify an explicitly saved blank note."""\n    # Enforce strict boolean type checking\n    if not isinstance(is_draft, bool):\n        raise ValueError("is_draft must be a boolean")\n    # A whitespace-only title is absent; keep the original text of a real title.\n    if title is not None:\n        title_length = weighted_length(title)\n        if not title.strip():\n            title = None\n        elif title_length > 175:\n            raise ValueError("Title exceeds weighted length 175")\n    # Do not strip the body: spaces and line breaks may be part of the writing.\n    body = "" if body is None else body\n    if weighted_length(body) > 7000:\n        raise ValueError("Body exceeds weighted length 7000")\n    # Explicitly saving a blank note requests deletion; a blank draft may stay.\n    return ValidatedNote(title, body, not is_draft and (title is not None) and not body.strip())\n'. Keep this source-level negative witness for the affected validation, output, identity, timing, connection or transaction contract; detection count is corroboration, not necessity.

Source: `app/note_rules.py:1`; evidence status: DETECTED; origin: exhaustive.

AST proof: `9403bf9b3e6c2771d5b143b63e285b52352f5685a4af0616bfa21bd695029760`; exact overlaps: none.

Changed expressions: `[{"original": "not is_draft and title is None and (not body.strip())", "mutated": "not is_draft and title is not None and (not body.strip())", "line": 60}, {"original": "title is None", "mutated": "title is not None", "line": 60}]`.

