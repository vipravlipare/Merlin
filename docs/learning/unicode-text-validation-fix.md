# Reject text that cannot encode as UTF-8

## Latest verification

October 10, 2026, after the learner edit: twelve direct checks across counter/title/body/email deliberately reject high, low and embedded surrogates with the expected UTF-8 ValueError. Three valid Unicode controls preserve text. The unchanged pytest suite reports 90 passed in 0.40 seconds. The observed surrogate gap is fixed; persistent regression tests remain to be added. These fifteen direct checks are separate from the collected pytest count.

## Earlier observed result

October 10, 2026: unchanged unit suite reports 90 passed in 0.46 seconds. Separate direct checks show that weighted_length, the title path, the body path and normalize_email each accept U+D800 and U+DFFF. All eight invalid-input checks therefore fail the proposed rejection contract. Valid smiley, supplementary letter and decomposed accent controls remain accepted and UTF-8 encodable.

These are direct helper observations, not eight new collected pytest cases or real database tests. Application code and executable tests were not edited.

## Smallest change for the learner

Inside `app/note_rules.py`, in `weighted_length`, after rejecting non-string input and before counting graphemes, attempt strict UTF-8 encoding of the text using `value.encode("utf-8")`.

Catch only UnicodeEncodeError from that attempt and raise a deliberate ValueError with the message `Text must be valid UTF-8`. Suppress the original exception chain so a traceback does not repeat the invalid text. Preserve the existing NUL rejection and weighting behavior. Do not use ignore or replace encoding modes: they silently lose or alter text.

This central check covers titles, bodies and non-None emails because each path already calls weighted_length. Do not duplicate the same guard in every caller. None remains valid for optional fields and is normalized by the existing callers.

## Regression expectations

The learner should add tests that require ValueError with the UTF-8 message for high and low surrogate code points, including one embedded inside otherwise normal text, through counter/title/body/email. Keep acceptance controls for actual supplementary characters such as an emoji and U+10400, plus decomposed accents; those are valid Unicode and must not be rejected. Keep existing NUL behavior unchanged.

Run from `/home/vipra/Merlin` after editing:

```bash
.venv/bin/python -m pytest tests/test_note_rules_and_maintenance.py -q
```

The unchanged suite alone cannot establish this fix because it lacks surrogate regressions. Repeat the direct checks or add the specified regressions before recording the gap as fixed. Required result: deliberate ValueError for invalid surrogates, acceptance for valid controls, and the existing suite still passing.

📚 Learn first: Python Unicode HOWTO, https://docs.python.org/3/howto/unicode.html ; exact topic: encoding Unicode strings and UnicodeEncodeError. Reference link; not reverified online this turn.

↩ Return: explain why strict rejection is safer than replacing invalid text, then write the central guard and rerun the checks. No database changes are needed for this helper fix.
