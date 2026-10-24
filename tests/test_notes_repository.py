"""Focused unit checks for the internal, read-only notes-list repository."""

from datetime import datetime, timezone
from unittest.mock import MagicMock, call
from uuid import UUID

import pytest
from psycopg.pq import TransactionStatus

from app.note_rules import MAX_TITLE_WEIGHTED_LENGTH, truncate_weighted
from app.notes_repository import ActiveNoteListItem, list_active_notes


ACTOR_ID = UUID("11111111-1111-4111-8111-111111111111")
NOTE_ID = UUID("22222222-2222-4222-8222-222222222222")
OTHER_NOTE_ID = UUID("33333333-3333-4333-8333-333333333333")
UPDATED_AT = datetime(2026, 10, 23, 12, 0, tzinfo=timezone.utc)


def make_connection(rows=(), *, status=TransactionStatus.IDLE):
    """Build a database-shaped mock; this helper never connects to PostgreSQL."""
    connection = MagicMock()
    connection.info.transaction_status = status
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = list(rows)
    return connection, cursor


def test_weighted_prefix_keeps_complete_display_units():
    """The shared title cap counts emoji as four and never splits graphemes."""
    family = "👨‍👩‍👧‍👦"
    flag = "🇺🇸"
    accent = "e\u0301"

    assert truncate_weighted("a😀b", 5) == "a😀"
    assert truncate_weighted("a😀b", 4) == "a"
    assert truncate_weighted(accent + flag + family + "z", 9) == accent + flag + family
    assert truncate_weighted("😀", 3) == ""
    assert truncate_weighted("anything", 0) == ""
    assert MAX_TITLE_WEIGHTED_LENGTH == 175

    with pytest.raises(ValueError, match="^Text limit must be a nonnegative integer$"):
        truncate_weighted("text", True)
    with pytest.raises(ValueError, match="^Text limit must be a nonnegative integer$"):
        truncate_weighted("text", -1)


def test_active_note_list_uses_body_prefix_when_title_is_missing():
    """Untitled rows show a weighted-length body preview; real titles stay intact."""
    family = "👨‍👩‍👧‍👦"
    body = "a" * 171 + family + "tail"
    connection, cursor = make_connection([
        (NOTE_ID, None, body, UPDATED_AT),
        (OTHER_NOTE_ID, "Saved title", "body must not replace title", UPDATED_AT),
    ])

    items = list_active_notes(connection, ACTOR_ID)

    assert items == [
        ActiveNoteListItem(NOTE_ID, "a" * 171 + family, UPDATED_AT),
        ActiveNoteListItem(OTHER_NOTE_ID, "Saved title", UPDATED_AT),
    ]
    query = " ".join(cursor.execute.call_args_list[2].args[0].split())
    assert "SELECT id, title, body, updated_at" in query
    assert "ORDER BY updated_at DESC, id ASC" in query


def test_active_note_list_sets_owner_and_uses_read_only_active_query():
    """Owner, active-view, and deterministic ordering rules reach SQL parameters."""
    connection, cursor = make_connection([
        (NOTE_ID, "Newest", "body", UPDATED_AT),
        (OTHER_NOTE_ID, "Older", "body", UPDATED_AT),
    ])

    list_active_notes(connection, ACTOR_ID)

    statements = cursor.execute.call_args_list
    assert statements[0] == call("SET TRANSACTION READ ONLY")
    assert statements[1] == call(
        "SELECT set_config('merlin.actor_id', %s, true)", (str(ACTOR_ID),)
    )
    query = " ".join(statements[2].args[0].split())
    assert query == (
        "SELECT id, title, body, updated_at FROM public.active_notes "
        "WHERE user_id = %s ORDER BY updated_at DESC, id ASC"
    )
    assert statements[2].args[1] == (ACTOR_ID,)
    connection.transaction.assert_called_once_with()
    connection.transaction.return_value.__exit__.assert_called_once_with(None, None, None)
    connection.close.assert_not_called()


def test_active_note_list_rejects_missing_actor_and_busy_connection_before_query():
    """No identity or caller-owned transaction may reach the database query."""
    connection, cursor = make_connection()
    with pytest.raises(ValueError, match="^A trusted actor UUID is required$"):
        list_active_notes(connection, None)
    connection.transaction.assert_not_called()
    cursor.execute.assert_not_called()

    busy, busy_cursor = make_connection(status=TransactionStatus.INTRANS)
    with pytest.raises(RuntimeError, match="^Notes listing requires an idle database connection$"):
        list_active_notes(busy, ACTOR_ID)
    busy.transaction.assert_not_called()
    busy_cursor.execute.assert_not_called()


def test_active_note_list_rejects_malformed_actor_before_query():
    """A request-shaped string cannot be treated as the trusted UUID actor."""
    connection, cursor = make_connection()

    with pytest.raises(ValueError, match="^A trusted actor UUID is required$"):
        list_active_notes(connection, str(ACTOR_ID))

    connection.transaction.assert_not_called()
    cursor.execute.assert_not_called()


def test_active_note_list_binds_each_actor_when_connection_is_reused():
    """Each call sets and filters by its own actor on the same idle connection."""
    actor_b = UUID("44444444-4444-4444-8444-444444444444")
    connection, cursor = make_connection()
    cursor.fetchall.side_effect = [
        [(NOTE_ID, "Actor A note", "body A", UPDATED_AT)],
        [(OTHER_NOTE_ID, "Actor B note", "body B", UPDATED_AT)],
    ]

    actor_a_items = list_active_notes(connection, ACTOR_ID)
    actor_b_items = list_active_notes(connection, actor_b)

    assert actor_a_items == [ActiveNoteListItem(NOTE_ID, "Actor A note", UPDATED_AT)]
    assert actor_b_items == [ActiveNoteListItem(OTHER_NOTE_ID, "Actor B note", UPDATED_AT)]
    statements = cursor.execute.call_args_list
    assert statements[1] == call(
        "SELECT set_config('merlin.actor_id', %s, true)", (str(ACTOR_ID),)
    )
    assert statements[2].args[1] == (ACTOR_ID,)
    assert statements[4] == call(
        "SELECT set_config('merlin.actor_id', %s, true)", (str(actor_b),)
    )
    assert statements[5].args[1] == (actor_b,)
    assert connection.transaction.call_count == 2
    connection.close.assert_not_called()
