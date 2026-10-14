"""Test probe control flow without opening PostgreSQL or reading a password."""

from unittest.mock import MagicMock, call, patch

import psycopg
import pytest

from app import database_connectivity_probe as probe


@pytest.fixture(autouse=True)
def forbid_real_connection(monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("Probe unit tests must not connect to PostgreSQL")
    monkeypatch.setattr(probe.psycopg, "connect", refuse)


def test_probe_is_read_only_before_its_only_query(capsys):
    conn = MagicMock()
    cursor = conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = ("merlin_d6", "merlin_d6")

    def execute(query):
        assert conn.read_only is True
        assert query == "SELECT current_database(), current_user;"

    cursor.execute.side_effect = execute
    with patch.object(probe.getpass, "getpass", return_value="synthetic-secret") as prompt, \
         patch.object(probe.psycopg, "connect") as connect:
        connect.return_value.__enter__.return_value = conn
        with pytest.raises(SystemExit) as result:
            probe.probe_database()
        assert result.value.code == 0
        prompt.assert_called_once_with(prompt="Password: ", stream=None)
        connect.assert_called_once_with(host="127.0.0.1", port=55432, dbname="merlin_d6",
                                       user="merlin_d6", password="synthetic-secret", connect_timeout=3)
        assert connect.return_value.__exit__.call_args.args == (None, None, None)
    assert cursor.execute.call_args_list == [call("SELECT current_database(), current_user;")]
    cursor.fetchone.assert_called_once_with()
    output = capsys.readouterr()
    assert output.out == "PROBE SUCCESS: Connected to database 'merlin_d6' as user 'merlin_d6'.\n"
    assert output.err == ""


@pytest.mark.parametrize("stage", ["connect", "query"])
def test_operational_failure_exits_without_success_or_secret(stage, capsys):
    failure = psycopg.OperationalError("synthetic-private-password")
    conn = MagicMock()
    cursor = conn.cursor.return_value.__enter__.return_value
    with patch.object(probe.getpass, "getpass", return_value="synthetic-private-password"), \
         patch.object(probe.psycopg, "connect") as connect:
        if stage == "connect":
            connect.side_effect = failure
        else:
            connect.return_value.__enter__.return_value = conn
            cursor.execute.side_effect = failure
        with pytest.raises(SystemExit) as result:
            probe.probe_database()
        assert result.value.code == 1
    output = capsys.readouterr()
    assert output.out == ""
    assert "DB Probe Failed:" in output.err
    assert "synthetic-private-password" not in output.err
    if stage == "connect":
        cursor.execute.assert_not_called()
    else:
        assert connect.return_value.__exit__.call_args.args[1] is failure
        cursor.fetchone.assert_not_called()


@pytest.mark.parametrize("stage,error_type", [
    *[(stage, psycopg.OperationalError) for stage in
      ["enter", "read_only", "cursor", "query", "fetch", "exit"]],
    ("query", psycopg.ProgrammingError), ("query", psycopg.DataError),
    ("query", psycopg.InternalError),
], ids=["enter-OperationalError", "read_only-OperationalError", "cursor-OperationalError",
        "query-OperationalError", "fetch-OperationalError", "exit-OperationalError",
        "query-ProgrammingError", "query-DataError", "query-InternalError"])
def test_database_errors_at_each_stage_are_sanitized(error_type, stage, capsys):
    """Cover each stage and exception class under the shared outer handler.

    There is no stage-specific exception handler: repeating all four classes
    at every stage adds no present decision boundary. Keep all six stages and
    all four classes, including fetch and transaction-exit failure.
    """
    failure = error_type("synthetic-private-password")
    manager = MagicMock()
    conn = manager.__enter__.return_value
    cursor_manager = conn.cursor.return_value
    cursor = cursor_manager.__enter__.return_value
    cursor.fetchone.return_value = ("merlin_d6", "merlin_d6")
    if stage == "enter":
        manager.__enter__.side_effect = failure
    elif stage == "read_only":
        from unittest.mock import PropertyMock
        type(conn).read_only = PropertyMock(side_effect=failure)
    elif stage == "cursor":
        cursor_manager.__enter__.side_effect = failure
    elif stage == "query":
        cursor.execute.side_effect = failure
    elif stage == "fetch":
        cursor.fetchone.side_effect = failure
    else:
        manager.__exit__.side_effect = failure
    with patch.object(probe.getpass, "getpass", return_value="synthetic-private-password"), \
         patch.object(probe.psycopg, "connect", return_value=manager):
        with pytest.raises(SystemExit) as result:
            probe.probe_database()
        assert result.value.code == 1
    output = capsys.readouterr()
    assert output.out == ""
    assert output.err.startswith("DB Probe Failed:")
    assert "synthetic-private-password" not in output.err
    if stage in {"enter", "read_only", "cursor"}:
        cursor.execute.assert_not_called()
    if stage in {"enter", "read_only", "cursor", "query"}:
        cursor.fetchone.assert_not_called()


def test_unrelated_programming_bug_is_not_masked():
    with patch.object(probe.getpass, "getpass", return_value="synthetic-secret"), \
         patch.object(probe.psycopg, "connect", side_effect=RuntimeError("programming bug")):
        with pytest.raises(RuntimeError, match="^programming bug$"):
            probe.probe_database()
