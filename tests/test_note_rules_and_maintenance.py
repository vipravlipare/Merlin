"""Unit tests: real validation, simulated database connections; no SQL runs here."""

from unittest.mock import MagicMock, call, patch

import pytest

from app.note_rules import normalize_email, validate_note, weighted_length
from app.notes_maintenance import run_once


# No test in this file may open a real database connection.
@pytest.fixture(autouse=True)
def forbid_real_database_connection(monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("This unit test attempted a real database connection")
    monkeypatch.setattr("app.notes_maintenance.psycopg.connect", refuse)


# Parametrize runs the same check once for each input/expected-count pair.
@pytest.mark.parametrize("text, count", [("abc !", 5), ("👨‍👩‍👧‍👦", 4), ("👍🏽", 4), ("🇺🇸", 4), ("1️⃣", 4), ("\n", 1)])
def test_display_character_weights(text, count):
    assert weighted_length(text) == count


def test_title_boundary_with_emoji_sequence():
    # 43 emoji × 4 + 3 ordinary characters = 175; one more must fail.
    title = "👨‍👩‍👧‍👦" * 43 + "abc"
    result = validate_note(title, "")
    assert (result.title, result.body, result.delete_on_save) == (title, "", False)
    with pytest.raises(ValueError, match="Title exceeds weighted length 175"):
        validate_note("👨‍👩‍👧‍👦" * 43 + "abcd", "")


def test_body_boundary():
    # Exactly 7,000 passes; the next emoji adds four and must fail.
    body = "😀" * 1750
    result = validate_note(None, body)
    assert (result.title, result.body, result.delete_on_save) == (None, body, False)
    with pytest.raises(ValueError, match="Body exceeds weighted length 7000"):
        validate_note(None, "😀" * 1751)


# Check the real worker, not just its helper: refusal must prevent every cleanup call.
@pytest.mark.parametrize("database, cluster", [
    pytest.param("merlin", 7694311451826794534, id="wrong-database"),
    pytest.param("merlin_d6", 7691749973399031842, id="preserved-cluster"),
    pytest.param("merlin", 7691749973399031842, id="both-wrong"),
])
def test_wrong_target_never_calls_cleanup(database, cluster):
    # MagicMock stands in for a connection; it never reaches PostgreSQL.
    conn = MagicMock()
    cursor = conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = (database, cluster)
    # Replace the real connector so this test cannot connect or delete data.
    with patch("app.notes_maintenance.psycopg.connect") as connect:
        connect.return_value.__enter__.return_value = conn
        with pytest.raises(RuntimeError, match="Refusing maintenance outside"):
            run_once("synthetic-secret")
    # Only the fingerprint query ran; no cleanup command followed the refusal.
    assert cursor.execute.call_args_list == [
        call("SELECT current_database(), system_identifier FROM pg_control_system()"),
    ]


def test_worker_cycle_verifies_then_uses_bounded_functions():
    # MagicMock stands in for a connection; it never reaches PostgreSQL.
    conn = MagicMock()
    cursor = conn.cursor.return_value.__enter__.return_value
    # Return a valid fingerprint and invented cleanup counts in call order.
    cursor.fetchone.side_effect = [("merlin_d6", 7694311451826794534), (2,), (3,)]
    # Replace the real connector so this test cannot connect or delete data.
    with patch("app.notes_maintenance.psycopg.connect") as connect:
        connect.return_value.__enter__.return_value = conn
        assert run_once("synthetic-secret", 25) == (2, 3)
    # Reject extra SQL as well as missing, reordered or incorrectly bound calls.
    assert cursor.execute.call_args_list == [
        call("SELECT current_database(), system_identifier FROM pg_control_system()"),
        call("SET LOCAL lock_timeout = '2s'"),
        call("SET LOCAL statement_timeout = '10s'"),
        call("SELECT public.cleanup_expired_blank_notes(%s)", (25,)),
        call("SELECT public.purge_deleted_notes(%s)", (25,)),
    ]
    connect.assert_called_once_with(
        host="127.0.0.1", port=55432, dbname="merlin_d6", user="merlin_d6",
        connect_timeout=3, password="synthetic-secret",
    )
    assert cursor.fetchone.call_count == 3
    context = connect.return_value
    assert context.__exit__.call_args.args == (None, None, None)


# Each input has a known answer; we never ask the helper to calculate its own expected result.
@pytest.mark.parametrize("text, expected", [
    ("", 0), ("!@#", 3), ("中文", 2), ("\t\r\n", 2),
    ("a😀b", 6), ("👨‍👩‍👧‍👦😀", 8), ("©️", 4), ("👍🏽!", 5),
])
def test_more_display_sequences(text, expected):
    assert weighted_length(text) == expected


# Check just below, exactly at, and just above each limit through the public validator.
@pytest.mark.parametrize("size, accepted", [(174, True), (175, True), (176, False)])
def test_plain_title_limit(size, accepted):
    if accepted:
        result = validate_note("a" * size, "")
        assert (result.title, result.body, result.delete_on_save) == ("a" * size, "", False)
    else:
        with pytest.raises(ValueError, match="Title exceeds weighted length 175"):
            validate_note("a" * size, "")


@pytest.mark.parametrize("size, accepted", [(6999, True), (7000, True), (7001, False)])
def test_plain_body_limit(size, accepted):
    if accepted:
        result = validate_note(None, "a" * size)
        assert (result.title, result.body, result.delete_on_save) == (None, "a" * size, False)
    else:
        with pytest.raises(ValueError, match="Body exceeds weighted length 7000"):
            validate_note(None, "a" * size)


@pytest.mark.parametrize("title", ["😀" * 44, "😀" * 43 + "abcd", "e\u0301" * 176], ids=["emoji176", "mixed176", "accented176"])
def test_over_limit_title_rejected_even_for_drafts(title):
    with pytest.raises(ValueError, match="Title exceeds weighted length 175"):
        validate_note(title, "", is_draft=True)


@pytest.mark.parametrize("body", ["👨‍👩‍👧‍👦" * 1751, "😀" * 1750 + "a", " " * 7001], ids=["family7004", "mixed7001", "spaces7001"])
def test_over_limit_body_rejected_even_for_drafts(body):
    with pytest.raises(ValueError, match="Body exceeds weighted length 7000"):
        validate_note(None, body, is_draft=True)


@pytest.mark.parametrize("title, body", [(None, None), ("", ""), (" \t\n", " \r\n"), ("\u00a0", "\u00a0")])
@pytest.mark.parametrize("draft", [False, True])
def test_empty_note_decision(title, body, draft):
    result = validate_note(title, body, is_draft=draft)
    assert result.title is None
    assert result.body == ("" if body is None else body)
    assert result.delete_on_save is (not draft)


@pytest.mark.parametrize("title, body", [("Title", ""), (None, "body"), (" 😀 ", " \nbody\n ")])
def test_nonblank_note_is_preserved(title, body):
    result = validate_note(title, body)
    assert (result.title, result.body, result.delete_on_save) == (title, body, False)


@pytest.mark.parametrize("value", [None, 1, b"text", "\x00", "hello\x00"])
def test_count_rejects_invalid_text(value):
    message = "PostgreSQL text cannot contain NUL" if isinstance(value, str) else "Text must be a string"
    with pytest.raises(ValueError, match=f"^{message}$"):
        weighted_length(value)


@pytest.mark.parametrize("field", ["title", "body"])
@pytest.mark.parametrize("value", [10, b"text", "\x00"])
def test_note_fields_reject_invalid_text(field, value):
    values = dict(title="Title", body="body")
    values[field] = value
    message = "PostgreSQL text cannot contain NUL" if isinstance(value, str) else "Text must be a string"
    with pytest.raises(ValueError, match=f"^{message}$"):
        validate_note(**values)


@pytest.mark.parametrize("raw, expected", [(None, None), ("", None), ("\t\n", None), (" \tMixed@Example.COM\n ", "Mixed@Example.COM"), ("\u00a0a@b.test\u00a0", "a@b.test")])
def test_email_edge_whitespace(raw, expected):
    assert normalize_email(raw) == expected


@pytest.mark.parametrize("value", [10, b"email", "a\x00@b.test"])
def test_email_rejects_invalid_database_text(value):
    message = "PostgreSQL text cannot contain NUL" if isinstance(value, str) else "Text must be a string"
    with pytest.raises(ValueError, match=f"^{message}$"):
        normalize_email(value)


# Exercise every public text path; the counter alone cannot prove caller validation.
@pytest.mark.parametrize("path", ["counter", "title", "body", "email"])
@pytest.mark.parametrize("value", ["\ud800", "\udfff", "a\ud800b", "\ud83d\ude00"],
                         ids=["high-surrogate", "low-surrogate", "embedded", "surrogate-pair"])
def test_invalid_unicode_rejected_before_persistence(path, value):
    with pytest.raises(ValueError, match="^Text must be valid UTF-8$") as error:
        if path == "counter":
            weighted_length(value)
        elif path == "title":
            validate_note(value, "body")
        elif path == "body":
            validate_note("Title", value)
        else:
            normalize_email(value)
    # Do not chain an encoding error that can repeat invalid/private input.
    assert error.value.__suppress_context__ is True


# Valid supplementary characters must survive; rejecting all Unicode is not a fix.
@pytest.mark.parametrize("path", ["counter", "title", "body", "email"])
@pytest.mark.parametrize("value, expected_weight", [("😀", 4), ("𐐀", 1), ("e\u0301", 1)])
def test_valid_unicode_preserved_in_every_text_path(path, value, expected_weight):
    if path == "counter":
        assert weighted_length(value) == expected_weight
    elif path == "title":
        result = validate_note(value, "body")
        assert (result.title, result.body, result.delete_on_save) == (value, "body", False)
    elif path == "body":
        result = validate_note("Title", value)
        assert (result.title, result.body, result.delete_on_save) == ("Title", value, False)
    else:
        # This helper preserves display text; it does not verify email syntax/ownership.
        assert normalize_email(value) == value


# Bad batch sizes must fail before the worker even attempts a connection.
@pytest.mark.parametrize("size", [-1, 0, 1001])
def test_invalid_batch_never_connects(size):
    with patch("app.notes_maintenance.psycopg.connect") as connect:
        with pytest.raises(ValueError, match="^Batch size must be between 1 and 1000$"):
            run_once("synthetic-secret", size)
        connect.assert_not_called()


@pytest.mark.parametrize("size", [1, 1000])
def test_allowed_batch_boundaries_and_fixed_target(size):
    conn = MagicMock()
    cursor = conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.side_effect = [("merlin_d6", 7694311451826794534), (0,), (0,)]
    with patch("app.notes_maintenance.psycopg.connect") as connect:
        connect.return_value.__enter__.return_value = conn
        assert run_once("synthetic-secret", size) == (0, 0)
        connect.assert_called_once_with(
            host="127.0.0.1", port=55432, dbname="merlin_d6", user="merlin_d6",
            connect_timeout=3, password="synthetic-secret",
        )
    assert cursor.execute.call_args_list == [
        call("SELECT current_database(), system_identifier FROM pg_control_system()"),
        call("SET LOCAL lock_timeout = '2s'"),
        call("SET LOCAL statement_timeout = '10s'"),
        call("SELECT public.cleanup_expired_blank_notes(%s)", (size,)),
        call("SELECT public.purge_deleted_notes(%s)", (size,)),
    ]
    assert cursor.fetchone.call_count == 3


# A simulated cleanup failure must escape through the transaction context.
# This checks Python control flow, not an actual PostgreSQL rollback.
@pytest.mark.parametrize("failure_stage", ["expiry", "purge"])
def test_cleanup_failure_leaves_transaction_as_error(failure_stage):
    import psycopg

    conn = MagicMock()
    cursor = conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.side_effect = [("merlin_d6", 7694311451826794534), (1,)]

    failure = psycopg.OperationalError("synthetic failure")

    def execute(query, *args):
        selected = "cleanup_expired_blank_notes" if failure_stage == "expiry" else "purge_deleted_notes"
        if selected in query:
            raise failure

    cursor.execute.side_effect = execute
    with patch("app.notes_maintenance.psycopg.connect") as connect:
        context = connect.return_value
        context.__enter__.return_value = conn
        with pytest.raises(psycopg.OperationalError, match="synthetic failure"):
            run_once("synthetic-secret")
        assert context.__exit__.call_count == 1
        kind, error, traceback = context.__exit__.call_args.args
        assert kind is psycopg.OperationalError and error is failure
        assert traceback is not None
        conn.commit.assert_not_called()
    if failure_stage == "expiry":
        assert not any("purge_deleted_notes" in call.args[0] for call in cursor.execute.call_args_list)


# Blank-title normalization must not erase an otherwise valid body.
@pytest.mark.parametrize("title", ["", " \t\n"])
def test_blank_title_with_real_body(title):
    result = validate_note(title, "  actual writing\n ")
    assert (result.title, result.body, result.delete_on_save) == (None, "  actual writing\n ", False)


# Code-point counting in validate_note would wrongly reject these valid boundary inputs.
@pytest.mark.parametrize("field, size", [("title", 175), ("body", 7000)])
def test_combining_characters_accepted_at_display_limit(field, size):
    text = "e\u0301" * size
    result = validate_note(text, "") if field == "title" else validate_note(None, text)
    assert (result.title, result.body, result.delete_on_save) == ((text, "", False) if field == "title" else (None, text, False))


# SQL requires an integer batch, so the worker must reject these before connecting.
@pytest.mark.parametrize("size", [pytest.param(True, id="boolean"), pytest.param(1.5, id="fraction")])
def test_noninteger_batch_rejected_before_connecting(size):
    with patch("app.notes_maintenance.psycopg.connect") as connect:
        # Any connection attempt proves the required validation did not happen.
        connect.side_effect = AssertionError("Invalid batch reached the database connector")
        with pytest.raises(ValueError, match="^Batch size must be an integer$"):
            run_once("synthetic-secret", size)
        connect.assert_not_called()


# Wrong batch types must produce a validation error, not a connector call or TypeError.
@pytest.mark.parametrize("size", [pytest.param(1.0, id="whole-float"), pytest.param(None, id="none"), pytest.param("100", id="string")])
def test_more_wrong_batch_types_rejected(size):
    with patch("app.notes_maintenance.psycopg.connect") as connect:
        connect.side_effect = AssertionError("Invalid batch reached the database connector")
        with pytest.raises(ValueError, match="^Batch size must be an integer$"):
            run_once("synthetic-secret", size)
        connect.assert_not_called()


# A text value such as "false" must not silently behave as a true draft flag.
@pytest.mark.parametrize("draft", [pytest.param("false", id="text"), pytest.param(1, id="integer"), pytest.param(None, id="none")])
def test_draft_flag_requires_boolean(draft):
    with pytest.raises(ValueError, match="^is_draft must be a boolean$"):
        validate_note(None, "", is_draft=draft)


# These checks run main(), but replace all database work and waiting.
def test_cli_once_runs_one_cycle_without_sleep(monkeypatch, capsys):
    from app import notes_maintenance as worker

    monkeypatch.setattr("sys.argv", ["notes_maintenance", "--once"])
    with patch.object(worker.getpass, "getpass", return_value="synthetic-secret") as prompt, \
         patch.object(worker, "run_once", side_effect=[(2, 3), AssertionError("Unexpected second cycle")]) as cycle, \
         patch.object(worker.time, "sleep") as sleep:
        worker.main()
    prompt.assert_called_once()
    cycle.assert_called_once_with("synthetic-secret")
    sleep.assert_not_called()
    output = capsys.readouterr().out
    assert output == "Expired title-only notes: 2; purged deleted notes: 3\n"
    assert "synthetic-secret" not in output


@pytest.mark.parametrize("args, interval", [([], 60), (["--interval", "10"], 10)])
def test_cli_repeats_at_chosen_interval_and_stops_on_interrupt(args, interval, monkeypatch, capsys):
    from app import notes_maintenance as worker

    monkeypatch.setattr("sys.argv", ["notes_maintenance", *args])
    with patch.object(worker.getpass, "getpass", return_value="synthetic-secret"), \
         patch.object(worker, "run_once", side_effect=[(0, 1), (2, 0), KeyboardInterrupt]) as cycle, \
         patch.object(worker.time, "sleep") as sleep:
        worker.main()
    assert cycle.call_args_list == [call("synthetic-secret")] * 3
    assert sleep.call_args_list == [call(interval), call(interval)]
    assert capsys.readouterr().out == ("Expired title-only notes: 0; purged deleted notes: 1\n"
                                         "Expired title-only notes: 2; purged deleted notes: 0\n"
                                         "Maintenance stopped\n")


@pytest.mark.parametrize("interval", ["-1", "0", "9", "abc"])
def test_cli_rejects_bad_interval_before_password_or_work(interval, monkeypatch):
    from app import notes_maintenance as worker

    monkeypatch.setattr("sys.argv", ["notes_maintenance", "--interval", interval])
    with patch.object(worker.getpass, "getpass") as prompt, patch.object(worker, "run_once") as cycle:
        with pytest.raises(SystemExit) as error:
            worker.main()
    assert error.value.code == 2
    prompt.assert_not_called()
    cycle.assert_not_called()


@pytest.mark.parametrize("failure", ["connection", "identity"])
def test_cli_error_hides_credentials_and_stops(failure, monkeypatch, capsys):
    import psycopg
    from app import notes_maintenance as worker

    secret = "synthetic-private-password"
    exception = psycopg.OperationalError(secret) if failure == "connection" else RuntimeError(secret)
    monkeypatch.setattr("sys.argv", ["notes_maintenance"])
    with patch.object(worker.getpass, "getpass", return_value=secret), \
         patch.object(worker, "run_once", side_effect=exception) as cycle, \
         patch.object(worker.time, "sleep") as sleep:
        with pytest.raises(SystemExit) as error:
            worker.main()
    assert "Maintenance failed" in str(error.value.code)
    assert secret not in str(error.value.code)
    output = capsys.readouterr()
    assert (output.out, output.err) == ("", "")
    cycle.assert_called_once()
    sleep.assert_not_called()


# Invalid identity responses or failed identity reads never reach cleanup.
@pytest.mark.parametrize("identity", [("merlin_d6", "bad"), ("merlin_d6", None), None])
def test_malformed_identity_stops_before_cleanup(identity):
    conn = MagicMock()
    cursor = conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = identity
    with patch("app.notes_maintenance.psycopg.connect") as connect:
        connect.return_value.__enter__.return_value = conn
        with pytest.raises(RuntimeError, match="^Refusing malformed Day 6 database identity$"):
            run_once("synthetic-secret")
    assert cursor.execute.call_args_list == [call("SELECT current_database(), system_identifier FROM pg_control_system()")]


def test_identity_query_failure_stops_before_cleanup():
    import psycopg
    failure = psycopg.OperationalError("synthetic identity failure")
    conn = MagicMock()
    cursor = conn.cursor.return_value.__enter__.return_value
    cursor.execute.side_effect = failure
    with patch("app.notes_maintenance.psycopg.connect") as connect:
        connect.return_value.__enter__.return_value = conn
        with pytest.raises(psycopg.OperationalError) as error:
            run_once("synthetic-secret")
        assert error.value is failure
        assert connect.return_value.__exit__.call_args.args[1] is failure
    assert cursor.execute.call_args_list == [call("SELECT current_database(), system_identifier FROM pg_control_system()")]


# Containers and booleans must not be coerced into database text.
@pytest.mark.parametrize("field", ["title", "body", "email"])
@pytest.mark.parametrize("value", [True, [], {}])
def test_container_and_boolean_text_is_rejected(field, value):
    with pytest.raises(ValueError, match="^Text must be a string$"):
        if field == "email":
            normalize_email(value)
        else:
            values = dict(title="Title", body="body")
            values[field] = value
            validate_note(**values)


def test_default_save_deletes_a_fully_blank_note():
    result = validate_note(None, None)
    assert (result.title, result.body, result.delete_on_save) == (None, "", True)


@pytest.mark.parametrize("title,body", [("Title", ""), (None, "body"), (" Title ", " body ")])
def test_nonblank_draft_keeps_exact_content(title, body):
    result = validate_note(title, body, is_draft=True)
    assert (result.title, result.body, result.delete_on_save) == (title, body, False)


def test_email_normalization_is_idempotent():
    first = normalize_email("  Mixed@Example.test  ")
    assert first == "Mixed@Example.test"
    assert normalize_email(first) == "Mixed@Example.test"


@pytest.mark.parametrize("args,code", [(["--help"], 0), (["--unknown"], 2)])
def test_cli_help_and_bad_flags_do_not_prompt_or_work(args, code, monkeypatch):
    from app import notes_maintenance as worker
    monkeypatch.setattr("sys.argv", ["notes_maintenance", *args])
    with patch.object(worker.getpass, "getpass") as prompt, patch.object(worker, "run_once") as cycle, \
         patch.object(worker.time, "sleep") as sleep:
        with pytest.raises(SystemExit) as result:
            worker.main()
    assert result.value.code == code
    prompt.assert_not_called()
    cycle.assert_not_called()
    sleep.assert_not_called()


# Literal corpus of all 29 whitespace code points recognized by pinned Python 3.12.
# Keep this independent from the helper so a narrow nonbreaking-space patch cannot pass.
WHITESPACE_CODEPOINTS = [*range(0x09, 0x0E), *range(0x1C, 0x20), 0x20, 0x85, 0xA0,
                         0x1680, *range(0x2000, 0x200B), 0x2028, 0x2029, 0x202F, 0x205F, 0x3000]


@pytest.mark.parametrize("codepoint", WHITESPACE_CODEPOINTS, ids=lambda value: f"U+{value:04X}")
def test_unicode_whitespace_note_and_email_contract(codepoint):
    space = chr(codepoint)
    result = validate_note(None, space)
    assert (result.title, result.body, result.delete_on_save) == (None, space, True)
    assert normalize_email(space + "Mixed@Example.test" + space) == "Mixed@Example.test"


@pytest.mark.parametrize("codepoint", WHITESPACE_CODEPOINTS, ids=lambda value: f"U+{value:04X}")
def test_every_whitespace_class_normalizes_title_preserves_real_content_and_drafts(codepoint):
    space = chr(codepoint)
    blank = validate_note(space, space, is_draft=True)
    assert (blank.title, blank.body, blank.delete_on_save) == (None, space, False)
    real = validate_note(space + "Title" + space, space + "Body" + space)
    assert (real.title, real.body, real.delete_on_save) == (space + "Title" + space, space + "Body" + space, False)
    assert normalize_email(space) is None
    assert normalize_email(space + "Mixed@Example.test") == "Mixed@Example.test"
    assert normalize_email("Mixed@Example.test" + space) == "Mixed@Example.test"


@pytest.mark.parametrize("text", ["\u200b", "\ufeff", "\u2060"])
def test_invisible_nonwhitespace_remains_real_content(text):
    note = validate_note(text, text)
    assert (note.title, note.body, note.delete_on_save) == (text, text, False)
    assert normalize_email(text) == text


@pytest.mark.parametrize("identity", [("merlin_d6", "synthetic-private-identifier"),
                                      ("merlin_d6", None), None])
def test_cli_malformed_identity_is_sanitized_and_never_runs_cleanup(identity, monkeypatch, capsys):
    from app import notes_maintenance as worker
    conn = MagicMock()
    cursor = conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = identity
    monkeypatch.setattr("sys.argv", ["notes_maintenance", "--once"])
    with patch.object(worker.getpass, "getpass", return_value="synthetic-secret"), \
         patch.object(worker.psycopg, "connect") as connect, \
         patch.object(worker.time, "sleep") as sleep:
        connect.return_value.__enter__.return_value = conn
        with pytest.raises(SystemExit) as result:
            worker.main()
        assert "Maintenance failed" in str(result.value.code)
        assert "synthetic-private" not in str(result.value.code)
        assert connect.return_value.__exit__.call_args.args[0] is RuntimeError
    assert cursor.execute.call_args_list == [call("SELECT current_database(), system_identifier FROM pg_control_system()")]
    sleep.assert_not_called()
    assert capsys.readouterr() == ("", "")
